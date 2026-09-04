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

from fastapi import HTTPException, status

from app.schemas import (
    ManualWeightRecalculateRequest, OptimizationResponse,
    IonBalanceResponse, EcPhStatusResponse
)
from app.core import (
    calculate_ion_balance,
    calculate_ec,
    calculate_ph,
    get_ec_ph_status,
    calculate_target_achievement,
    calculate_reservoir_data,
    check_precipitation,
    ALL_ELEMENTS,
)
from app.core.optimizer.matrix_builder import prepare_fertilizer_data

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


def recalculate_manual_weights(request: ManualWeightRecalculateRequest):
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

        # هزینه کل بر مبنای وزن واقعی
        cost_total = 0.0
        for fert in prepared:
            w = actual_weights.get(fert['id'], 0)
            cost_total += (w / 1000.0) * fert.get('price_per_kg', 0)

        # تعادل یونی
        cation, anion, is_balanced, ion_details = calculate_ion_balance(final_concentrations, unit="ppm")

        # رسوب
        precipitation_result = check_precipitation(final_concentrations)

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

        warnings.append('⚠️ این نتیجه بر اساس ویرایش دستی وزن است، نه بهینه‌سازی خودکار.')

        warnings = list(dict.fromkeys(warnings))
        suggestions = list(dict.fromkeys(suggestions))

        # EC / pH
        ec_result = calculate_ec(final_concentrations, unit="ppm")
        water_ph = water_values.get('pH', 7.0) if water_values else 7.0
        ph_result = calculate_ph(final_concentrations, unit="ppm", water_ph=water_ph)
        water_ec = water_values.get('EC', 0) if water_values else 0
        ec_ph_status = get_ec_ph_status(
            ec=ec_result['ec'], ph=ph_result['ph'], water_ec=water_ec, water_ph=water_ph
        )

        weights_dict = {fert['id']: actual_weights.get(fert['id'], 0.0) for fert in prepared}

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
            ph=ph_result['ph'],
            ec_status=ec_result['status_label'],
            ph_status=ph_result['status_label'],
            ec_ph_status=EcPhStatusResponse(
                status=ec_ph_status['status'],
                status_label=ec_ph_status['status_label'],
                color=ec_ph_status['color'],
                message=ec_ph_status['message'],
                issues=ec_ph_status['issues'],
                recommendations=ec_ph_status['recommendations'],
                ec=ec_ph_status['ec'],
                ph=ec_ph_status['ph'],
                water_ec=ec_ph_status.get('water_ec'),
                water_ph=ec_ph_status.get('water_ph'),
                ec_status=ec_ph_status.get('ec_status', ''),
                ec_label=ec_ph_status.get('ec_label', ''),
                ph_status=ec_ph_status.get('ph_status', ''),
                ph_label=ec_ph_status.get('ph_label', '')
            ),
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
