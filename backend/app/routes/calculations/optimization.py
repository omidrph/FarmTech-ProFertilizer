# backend/app/routes/calculations/optimization.py
"""
مسیر بهینه‌سازی خودکار فرمول کود
این فایل قلب تپنده سیستم بهینه‌سازی است
"""

import logging
import time
import traceback
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import (
    OptimizationRequest, OptimizationResponse,
    IonBalanceResponse, EcPhStatusResponse
)
import app.crud as crud
from app.security import get_current_user
from app.core import (
    optimize_fertilizers as core_optimize_fertilizers,
    calculate_ec,
    calculate_ph,
    get_ec_ph_status
)
from app.core.optimizer.result_processor import validate_optimization_result

logger = logging.getLogger(__name__)


def optimize_fertilizers_endpoint(
    request: OptimizationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    🚀 بهینه‌سازی خودکار فرمول کود با استفاده از الگوریتم NNLS (core)
    با قابلیت تعادل یونی خودکار
    """
    try:
        logger.info(f"🚀 Starting optimization for user {current_user.id}")
        logger.info(f"   Targets: {len(request.target_values)} elements")
        logger.info(f"   Fertilizers: {len(request.fertilizers)} items")
        logger.info(f"   Method: {request.options.method if request.options else 'nnls'}")
        
        start_time = time.time()
        
        # ۱. آماده‌سازی داده‌ها
        target_values = request.target_values
        water_values = request.water_values or {}
        
        # تبدیل کودها به فرمت مورد نیاز
        fertilizers = []
        for fert in request.fertilizers:
            fertilizers.append({
                'id': fert.id,
                'name': fert.name,
                'elements': fert.elements,
                'price_per_kg': fert.price_per_kg,
                'purity': fert.purity,
                'is_acid': fert.is_acid,
                'is_system_default': fert.is_system_default,
                'fixed_weight': fert.fixed_weight if hasattr(fert, 'fixed_weight') else None
            })
        
        # تنظیمات بهینه‌سازی
        options = request.options.dict() if request.options else {}
        
        # 🆕 اضافه کردن گزینه auto_balance (پیش‌فرض فعال)
        if 'auto_balance' not in options:
            options['auto_balance'] = True
        
        # ۲. اجرای بهینه‌سازی با استفاده از core
        result = core_optimize_fertilizers(
            target_values=target_values,
            fertilizers=fertilizers,
            water_values=water_values,
            options=options
        )
        
        if 'error' in result:
            logger.error(f"Optimization error: {result['error']}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result['error']
            )
        
        # ============================================================
        # 🆕 ذخیره final_values و reservoir_data در دیتابیس
        # ============================================================
        try:
            # دریافت آخرین گزارش کاربر
            reports = crud.get_reports_by_user(db, current_user.id, skip=0, limit=1)
            if reports:
                report = reports[0]
                
                # دریافت یا ایجاد محاسبات
                calculation = crud.get_calculation_by_report(db, report.id)
                
                if calculation:
                    # ساخت calc_rows از روی weights
                    calc_rows = []
                    for fert_id, weight in result.get('weights', {}).items():
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
                    
                    # به‌روزرسانی محاسبات
                    from app.schemas import CalculationUpdate
                    update_data = {
                        'final_values': result.get('concentrations', {}),
                        'reservoir_data': result.get('reservoir_data', {'A': [], 'B': [], 'C': []}),
                        'calc_rows': calc_rows
                    }
                    calc_update = CalculationUpdate(**update_data)
                    crud.update_calculation(db, calculation.id, calc_update)
                    
                    logger.info(f"✅ Updated calculation {calculation.id} with final_values and reservoir_data")
                    
        except Exception as e:
            logger.warning(f"Could not save optimization result to database: {e}")
            traceback.print_exc()
        
        # ۳. اعتبارسنجی نتایج
        validation = validate_optimization_result(result)
        if not validation['is_valid']:
            logger.warning(f"Validation errors: {validation['errors']}")
        
        # ۴. ذخیره تاریخچه
        try:
            # ساخت لیست کودهای انتخاب شده برای تاریخچه
            fertilizers_selected = []
            for fert in fertilizers:
                fertilizers_selected.append({
                    'id': fert.get('id'),
                    'name': fert.get('name'),
                    'elements': fert.get('elements'),
                    'price_per_kg': fert.get('price_per_kg'),
                    'purity': fert.get('purity'),
                    'is_acid': fert.get('is_acid')
                })
            
            crud.save_optimization_log(
                db=db,
                user_id=current_user.id,
                report_id=None,
                target_values=target_values,
                water_values=water_values,
                fertilizers_selected=fertilizers_selected,
                optimization_options=options,
                result=result
            )
        except Exception as e:
            logger.warning(f"Could not save optimization log: {e}")
        
        # ============================================================
        # 🆕 ۵. محاسبه EC و pH نهایی
        # ============================================================
        concentrations = result.get('concentrations', {})
        
        # محاسبه EC
        ec_result = calculate_ec(concentrations, unit="ppm")
        
        # محاسبه pH (با استفاده از pH آب کاربر یا پیش‌فرض)
        water_ph = water_values.get('pH', 7.0) if water_values else 7.0
        ph_result = calculate_ph(concentrations, unit="ppm", water_ph=water_ph)
        
        # وضعیت ترکیبی
        water_ec = water_values.get('EC', 0) if water_values else 0
        ec_ph_status = get_ec_ph_status(
            ec=ec_result['ec'],
            ph=ph_result['ph'],
            water_ec=water_ec,
            water_ph=water_ph
        )
        
        # ساخت EcPhStatusResponse
        ec_ph_response = EcPhStatusResponse(
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
        )
        
        # ۶. ساخت پاسخ
        response = OptimizationResponse(
            weights=result['weights'],
            concentrations=result['concentrations'],
            residual_error=result['residual_error'],
            cost_total=result['cost_total'],
            ion_balance=IonBalanceResponse(
                cation=result['ion_balance']['cation'],
                anion=result['ion_balance']['anion'],
                is_balanced=result['ion_balance']['is_balanced'],
                message=result['ion_balance']['message']
            ),
            target_achievement=result['target_achievement'],
            warnings=result.get('warnings', []),
            suggestions=result.get('suggestions', []),
            reservoir_data=result.get('reservoir_data', {'A': [], 'B': [], 'C': []}),
            iterations=result['iterations'],
            convergence_time_ms=result['convergence_time_ms'],
            is_converged=result['is_converged'],
            summary=result['summary'],
            # 🆕 فیلدهای EC و pH
            ec=ec_result['ec'],
            ph=ph_result['ph'],
            ec_status=ec_result['status_label'],
            ph_status=ph_result['status_label'],
            ec_ph_status=ec_ph_response
        )
        
        logger.info(f"✅ Optimization completed in {response.convergence_time_ms:.2f}ms")
        logger.info(f"   Residual error: {response.residual_error:.4f}")
        logger.info(f"   Total cost: {response.cost_total:,.0f} تومان")
        logger.info(f"   Iterations: {response.iterations}")
        logger.info(f"   🆕 EC: {response.ec} dS/m | pH: {response.ph}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in optimize_fertilizers_endpoint: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در بهینه‌سازی: {str(e)}"
        )