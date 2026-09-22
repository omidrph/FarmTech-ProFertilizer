
# backend/app/routes/calculations/recalculate.py
"""
مسیر محاسبه مجدد نتیجه پس از ویرایش دستی وزن یک کود
======================================================

🆕 این مسیر جدید برای ویژگی درخواستی کاربر است:
«وقتی کاربر روی محاسبه می‌زند بتواند مستقیم از روی همان نتیجه‌ها وزن
(گرم) هر کود را تغییر دهد و بقیه مقادیر (غلظت عناصر، EC، pH، تعادل
یونی، هزینه، درصد تحقق اهداف، هشدارها) به‌درستی و بر همان مبنای علمی
دوباره محاسبه شوند.»

این مسیر عمداً از منطق NNLS دوباره استفاده نمی‌کند (چون کاربر خودش وزن
را دستی مشخص کرده)، بلکه دقیقاً همان توابع علمی که در فرایند
بهینه‌سازی خودکار استفاده می‌شوند را روی وزن‌های جدید اجرا می‌کند تا
نتیجه کاملاً سازگار و صحیح (بدون خطای علمی) بماند.
"""

import logging
import time
import traceback
from typing import Dict, Any

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.security import get_current_user
import app.crud as crud
from app.schemas import (
    ManualWeightRecalculateRequest, OptimizationResponse,
    IonBalanceResponse
)
from app.core import (
    calculate_ion_balance,
    calculate_ec,
    calculate_ph,
    calculate_target_achievement,
    calculate_reservoir_data,
    check_precipitation,
    check_nutrient_interactions,
    ALL_ELEMENTS,
)
from app.core.optimizer.matrix_builder import prepare_fertilizer_data, calculate_full_solution_concentrations

logger = logging.getLogger(__name__)


def _calculate_concentrations_from_weights(
    prepared_fertilizers,
    weights: Dict[str, float],
    water_values: Dict[str, float]
) -> Dict[str, float]:
    """
    محاسبه غلظت نهایی هر عنصر از روی وزن واقعی (گرم) هر کود.

    نکته: `weights` اینجا وزن واقعی برای کل حجم مخزن است (نه وزن به ازای
    ۱۰۰۰ لیتر)، پس برای برگرداندن آن به مبنای غلظت (ppm) باید بر
    scale_factor تقسیم شود؛ این تابع خودش scale_factor را از بیرون
    می‌گیرد و روی weight تقسیم می‌کند.
    """
    concentrations: Dict[str, float] = {}
    for element in ALL_ELEMENTS:
        total = water_values.get(element, 0) or 0
        for fert in prepared_fertilizers:
            fert_id = fert['id']
            w = weights.get(fert_id, 0) or 0
            if w <= 0:
                continue
            pct = fert['elements'].get(element, 0) or 0
            if pct <= 0:
                continue
            contribution = (pct / 100) * fert['purity_factor'] * w
            total += contribution
        if total > 0:
            concentrations[element] = total
    return concentrations


def recalculate_manual_weights(
    request: ManualWeightRecalculateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    🆕 محاسبه مجدد کامل نتیجه بعد از ویرایش دستی وزن یک یا چند کود
    توسط کاربر، بدون اجرای مجدد الگوریتم NNLS.
    """
    try:
        start_time = time.time()

        tank_volume = request.tank_volume if request.tank_volume and request.tank_volume > 0 else 1000.0
        scale_factor = tank_volume / 1000.0

        fertilizers = [
            {
                'id': f.id,
                'name': f.name,
                'elements': f.elements,
                'price_per_kg': f.price_per_kg,
                'purity': f.purity,
                'is_acid': f.is_acid,
                'is_system_default': f.is_system_default,
            }
            for f in request.fertilizers
        ]
        prepared = prepare_fertilizer_data(fertilizers)

        # وزن‌های واقعی (برای کل حجم مخزن) که کاربر ویرایش کرده
        actual_weights = {str(k): float(v) for k, v in request.weights.items() if v and v > 0}

        # برای محاسبه غلظت‌ها باید وزن را به مبنای «به ازای ۱۰۰۰ لیتر» برگردانیم
        weights_per_1000L = {k: v / scale_factor for k, v in actual_weights.items()}

        water_values = request.water_values or {}

        final_concentrations = _calculate_concentrations_from_weights(
            prepared, weights_per_1000L, water_values
        )

        # 🆕 مثل مسیر optimize: تعادل یونی/EC/رسوب باید بر مبنای ترکیب
        # شیمیایی کامل محلول باشند (نه فقط عناصر هدف)، وگرنه آنیون‌هایی
        # مثل S/Cl که هدف ندارند دوباره ناقص محاسبه می‌شوند.
        import numpy as np
        weights_array = np.array([weights_per_1000L.get(f['id'], 0.0) for f in prepared])
        full_concentrations = calculate_full_solution_concentrations(
            weights_array, fertilizers, water_values
        )

        # هزینه کل بر مبنای وزن واقعی
        cost_total = 0.0
        for fert in prepared:
            w = actual_weights.get(fert['id'], 0)
            cost_total += (w / 1000.0) * fert.get('price_per_kg', 0)

        # تعادل یونی
        cation, anion, is_balanced, ion_details = calculate_ion_balance(full_concentrations, unit="ppm")

        # 🆕 تخمین pH پیش از بررسی رسوب (لازم برای [OH-] واقعی و کسر PO4³⁻ درست)
        water_ph_for_precip = water_values.get('pH', 7.0) if water_values else 7.0
        prelim_ph_result = calculate_ph(full_concentrations, unit="ppm", water_ph=water_ph_for_precip)
        has_chelated_iron = any(
            fert.get('elements', {}).get('Fe', 0) > 0 and (
                'کلات' in fert.get('name', '') or
                'edta' in fert.get('name', '').lower() or
                'dtpa' in fert.get('name', '').lower() or
                'eddha' in fert.get('name', '').lower() or
                'chelate' in fert.get('name', '').lower()
            )
            for fert in fertilizers
        )

        # رسوب
        precipitation_result = check_precipitation(
            final_concentrations,
            ph=prelim_ph_result.get('ph'),
            has_chelated_iron=has_chelated_iron,
            alkalinity_ppm_caco3=water_values.get('Alkalinity')
        )

        # درصد تحقق اهداف
        achievement = calculate_target_achievement(request.target_values, final_concentrations)

        # توزیع مخازن بر مبنای وزن واقعی
        reservoir_data = calculate_reservoir_data(fertilizers, actual_weights)

        # هشدار و پیشنهاد
        warnings = []
        suggestions = []
        if not is_balanced:
            diff = abs(cation - anion)
            warnings.append(f'تعادل یونی برقرار نیست (اختلاف: {diff:.2f} meq/L)')
            if cation > anion:
                suggestions.append('برای برقراری تعادل، آنیون‌ها را افزایش دهید')
            else:
                suggestions.append('برای برقراری تعادل، کاتیون‌ها را افزایش دهید')

        if precipitation_result and not precipitation_result.get('is_safe', True):
            for risk in precipitation_result.get('risks', []):
                warnings.append(f'خطر رسوب: {risk["compound"]}')
            suggestions.extend(precipitation_result.get('suggestions', []))

        for element, pct in achievement.items():
            if pct < 70 and request.target_values.get(element, 0) > 0:
                warnings.append(f'عنصر {element}: {pct:.0f}% تحقق')
                suggestions.append(f'افزایش {element} با استفاده از کود مناسب')
            elif pct > 130 and request.target_values.get(element, 0) > 0:
                warnings.append(f'عنصر {element}: {pct:.0f}% تحقق (بیش‌بود)')
                suggestions.append(f'کاهش {element} یا استفاده از کود با درصد کمتر')

        # EC (pH دیگر بخشی از پاسخ این صفحه نیست؛ prelim_ph_result فقط
        # برای هشدارهای شیمیایی داخلی زیر استفاده می‌شود)
        water_ec = water_values.get('EC', 0) if water_values else 0
        ec_result = calculate_ec(full_concentrations, unit="ppm", water_ec=water_ec)
        ph_result = prelim_ph_result

        if ph_result.get('nh4_warning'):
            warnings.append(ph_result['nh4_warning'])

        # 🆕 تداخلات تغذیه‌ای/شیمیایی (آهن+فسفر، قفل ریزمغذی در pH بالا، کلر/سدیم/بور، K/Ca)
        warnings.extend(check_nutrient_interactions(final_concentrations, ph_estimate=ph_result.get('ph')))

        warnings.append('⚠️ این نتیجه بر اساس ویرایش دستی وزن است، نه بهینه‌سازی خودکار.')

        warnings = list(dict.fromkeys(warnings))
        suggestions = list(dict.fromkeys(suggestions))

        weights_dict = {fert['id']: actual_weights.get(fert['id'], 0.0) for fert in prepared}

        # ============================================================
        # 🆕 ذخیره وضعیت به‌روزشده در دیتابیس (همان الگوی optimize)
        # ============================================================
        # ✅ رفع باگ: قبلاً ویرایش دستی وزن اصلاً در دیتابیس ذخیره نمی‌شد؛
        # با رفرش یا بازکردن دوبارهٔ گزارش، وزن ویرایش‌شده گم می‌شد و به
        # نتیجهٔ خودکار قبلی برمی‌گشت.
        if request.report_id:
            try:
                report = crud.get_report_by_id(db, request.report_id)
                if report and report.user_id == current_user.id:
                    calculation = crud.get_calculation_by_report(db, report.id)

                    calc_rows = []
                    for fert_id, weight in weights_dict.items():
                        if weight > 0:
                            fert = next((f for f in fertilizers if f.get('id') == fert_id), None)
                            if fert:
                                cost = (weight / 1000) * fert.get('price_per_kg', 0)
                                calc_rows.append({
                                    'materialName': fert.get('name', ''),
                                    'weight': weight,
                                    'purity': fert.get('purity', 100),
                                    'cost': cost,
                                    'elements': fert.get('elements', {}),
                                    'isAcid': fert.get('is_acid', False),
                                    'fertilizerId': fert_id,
                                    'isFixedRow': False
                                })

                    reservoir_data_to_save = dict(reservoir_data or {'A': [], 'B': [], 'C': []})
                    reservoir_data_to_save['settings'] = {
                        'tank_volume': tank_volume,
                        'stock_volume': request.stock_volume,
                        'injection_ratio': reservoir_data_to_save.get('settings', {}).get('injection_ratio', 100)
                    }

                    optimization_result_to_save = {
                        'weights': weights_dict,
                        'concentrations': final_concentrations,
                        'residual_error': 0.0,
                        'cost_total': float(cost_total),
                        'ion_balance': {
                            'cation': cation,
                            'anion': anion,
                            'is_balanced': is_balanced
                        },
                        'target_achievement': achievement,
                        'warnings': warnings,
                        'suggestions': suggestions,
                        'iterations': 0,
                        'convergence_time_ms': (time.time() - start_time) * 1000,
                        'is_converged': True,
                        'summary': 'نتیجه با وزن ویرایش‌شدهٔ دستی محاسبه شد.',
                        'ec': ec_result['ec'],
                        'ec_status': ec_result['status_label'],
                        'stock_info': {'tank_volume': tank_volume, 'manual_edit': True}
                    }

                    from app.schemas import CalculationUpdate, CalculationCreate
                    update_data = {
                        'target_values': request.target_values,
                        'final_values': final_concentrations,
                        'reservoir_data': reservoir_data_to_save,
                        'calc_rows': calc_rows,
                        'selected_fertilizer_ids': [f['id'] for f in fertilizers],
                        'optimization_result': optimization_result_to_save
                    }

                    if calculation:
                        crud.update_calculation(db, calculation.id, CalculationUpdate(**update_data))
                        logger.info(f"✅ Updated calculation {calculation.id} after manual weight edit")
                    else:
                        crud.create_calculation(db, CalculationCreate(**update_data), report.id)
                        logger.info(f"✅ Created calculation for report {report.id} after manual weight edit")
                else:
                    logger.warning(f"report_id {request.report_id} not found or not owned by user {current_user.id}; skipping auto-save")
            except Exception as e:
                logger.warning(f"Could not save manual recalculation result to database: {e}")
                traceback.print_exc()

        response = OptimizationResponse(
            weights=weights_dict,
            concentrations=final_concentrations,
            residual_error=0.0,
            cost_total=float(cost_total),
            ion_balance=IonBalanceResponse(
                cation=cation,
                anion=anion,
                is_balanced=is_balanced,
                message='تعادل یونی برقرار است ✅' if is_balanced else 'تعادل یونی برقرار نیست ⚠️'
            ),
            target_achievement=achievement,
            warnings=warnings,
            suggestions=suggestions,
            reservoir_data=reservoir_data,
            iterations=0,
            convergence_time_ms=(time.time() - start_time) * 1000,
            is_converged=True,
            summary='نتیجه با وزن ویرایش‌شدهٔ دستی محاسبه شد.',
            ec=ec_result['ec'],
            ec_status=ec_result['status_label'],
            stock_info={
                'tank_volume': tank_volume,
                'manual_edit': True
            }
        )

        return response

    except Exception as e:
        logger.error(f"Error in recalculate_manual_weights: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در محاسبه مجدد: {str(e)}"
        )




