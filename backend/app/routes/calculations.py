# backend/app/routes/calculations.py
"""مسیرهای محاسبات (Calculations) - نسخه کامل با بهینه‌سازی"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import logging
import time
import json
from typing import List, Optional

from app.database import get_db
from app.models import User, Calculation, OptimizationLog
from app.schemas import (
    CalculationCreate, CalculationUpdate, CalculationResponse,
    HomeSummaryResponse, IonBalanceRequest, IonBalanceResponse,
    FinalSolutionRequest, FinalSolutionResponse,
    ReservoirRequest, ReservoirResponse,
    UnitConversionRequest, UnitConversionResponse,
    InterpretationResponse,
    OptimizationRequest, OptimizationResponse,
    OptimizationOptions, OptimizationLogResponse,
    PrecipitationCheckRequest, PrecipitationCheckResponse
)
import app.crud as crud
from app.security import get_current_user
from app import services

# ===== تنظیمات Logger =====
logger = logging.getLogger(__name__)

# ===== ایجاد Router =====
calculations_router = APIRouter(prefix="/calculations", tags=["Calculations"])


# ============================================================
# 🆕 APIهای محاسباتی ثابت (بدون پارامتر)
# ============================================================

@calculations_router.get("/home-summary", response_model=HomeSummaryResponse)
def get_home_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    دریافت خلاصه داشبورد - تمام محاسبات در بک‌اند انجام می‌شود
    """
    try:
        logger.info(f"Getting home summary for user {current_user.id}")
        
        # دریافت آخرین گزارش کاربر
        reports = crud.get_reports_by_user(db, current_user.id, skip=0, limit=1)
        if not reports:
            logger.info(f"No reports found for user {current_user.id}")
            return HomeSummaryResponse(
                has_data=False,
                message="هنوز گزارشی ایجاد نشده است"
            )
        
        report = reports[0]
        logger.info(f"Found report: {report.id} - {report.report_name}")
        
        water_analysis = crud.get_water_analysis_by_report(db, report.id)
        water_salinity = water_analysis.water_salinity if water_analysis else 0
        
        calculation = crud.get_calculation_by_report(db, report.id)
        
        if not calculation:
            logger.info(f"No calculation found for report {report.id}")
            return HomeSummaryResponse(
                has_data=False,
                message="هنوز محاسباتی انجام نشده است"
            )
        
        # ===== گرفتن داده‌ها از دیتابیس =====
        target_values = calculation.target_values or {}
        final_values = calculation.final_values or {}
        reservoir_data = calculation.reservoir_data or {}
        
        logger.info(f"Raw target_values: {target_values}")
        logger.info(f"Raw final_values: {final_values}")
        logger.info(f"Raw reservoir_data: {reservoir_data}")
        
        # ===== تبدیل JSON رشته به دیکشنری =====
        if isinstance(target_values, str):
            try:
                target_values = json.loads(target_values)
                logger.info(f"Converted target_values from JSON string")
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse target_values JSON: {e}")
                target_values = {}
        
        if isinstance(final_values, str):
            try:
                final_values = json.loads(final_values)
                logger.info(f"Converted final_values from JSON string")
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse final_values JSON: {e}")
                final_values = {}
        
        if isinstance(reservoir_data, str):
            try:
                reservoir_data = json.loads(reservoir_data)
                logger.info(f"Converted reservoir_data from JSON string")
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse reservoir_data JSON: {e}")
                reservoir_data = {'A': [], 'B': [], 'C': []}
        
        # ===== اگر final_values خالی است، از calc_rows محاسبه کن =====
        if not final_values or len(final_values) == 0:
            logger.info("final_values is empty, calculating from calc_rows")
            calc_rows = calculation.calc_rows or []
            
            if isinstance(calc_rows, str):
                try:
                    calc_rows = json.loads(calc_rows)
                    logger.info(f"Converted calc_rows from JSON string, found {len(calc_rows)} rows")
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse calc_rows JSON: {e}")
                    calc_rows = []
            
            final_values = {}
            for row in calc_rows:
                if row and isinstance(row, dict):
                    elements = row.get('elements', {})
                    if isinstance(elements, str):
                        try:
                            elements = json.loads(elements)
                        except json.JSONDecodeError:
                            elements = {}
                    
                    weight = row.get('weight', 0)
                    purity = row.get('purity', 100) / 100
                    
                    for element, percentage in elements.items():
                        if percentage and percentage > 0:
                            contribution = (percentage / 100) * weight * purity
                            final_values[element] = final_values.get(element, 0) + contribution
            
            logger.info(f"Calculated final_values: {final_values}")
        
        # ===== اطمینان از اینکه reservoir_data ساختار درست دارد =====
        if not reservoir_data or not isinstance(reservoir_data, dict):
            reservoir_data = {'A': [], 'B': [], 'C': []}
        
        for key in ['A', 'B', 'C']:
            if key not in reservoir_data:
                reservoir_data[key] = []
            if not isinstance(reservoir_data[key], list):
                reservoir_data[key] = []
        
        # ===== محاسبه تعادل یونی =====
        cation, anion, is_balanced = services.calculate_ion_balance(target_values, unit="ppm")
        
        # ===== محاسبه آمار =====
        active_elements_count = sum(1 for v in target_values.values() if v and v > 0)
        total_elements = len(services.ELEMENTS)
        
        active_reservoirs_count = 0
        if reservoir_data.get('A') and len(reservoir_data['A']) > 0:
            active_reservoirs_count += 1
        if reservoir_data.get('B') and len(reservoir_data['B']) > 0:
            active_reservoirs_count += 1
        if reservoir_data.get('C') and len(reservoir_data['C']) > 0:
            active_reservoirs_count += 1
        
        # ===== محاسبه مجموع هزینه =====
        total_cost = 0
        if calculation.calc_rows:
            calc_rows = calculation.calc_rows
            if isinstance(calc_rows, str):
                try:
                    calc_rows = json.loads(calc_rows)
                except json.JSONDecodeError:
                    calc_rows = []
            
            for row in calc_rows:
                if row and isinstance(row, dict):
                    total_cost += row.get('cost', 0)
        
        # ===== محاسبه مجموع وزن مخازن =====
        total_reservoir_weight = 0
        for reservoir_items in reservoir_data.values():
            if isinstance(reservoir_items, list):
                for item in reservoir_items:
                    if item and isinstance(item, dict):
                        total_reservoir_weight += item.get('amount', 0)
        
        # ===== تولید توصیه‌ها =====
        recommendations = []
        
        if not is_balanced:
            diff = abs(cation - anion)
            recommendations.append({
                'type': 'danger',
                'title': 'عدم تعادل یونی',
                'description': f'اختلاف کاتیون و آنیون {diff:.2f} meq/L است.'
            })
        
        deficient_elements = []
        excessive_elements = []
        for element in services.ELEMENTS:
            target = target_values.get(element, 0)
            actual = final_values.get(element, 0)
            if target == 0:
                continue
            percent = (actual / target) * 100 if target > 0 else 0
            if percent < 70:
                deficient_elements.append(element)
            elif percent > 130:
                excessive_elements.append(element)
        
        if deficient_elements:
            recommendations.append({
                'type': 'warning',
                'title': f'{len(deficient_elements)} عنصر با کمبود شدید',
                'description': f'عناصر {", ".join(deficient_elements[:3])}{" و..." if len(deficient_elements) > 3 else ""} کمتر از 70% مقدار هدف هستند.'
            })
        
        if excessive_elements:
            recommendations.append({
                'type': 'warning',
                'title': f'{len(excessive_elements)} عنصر با بیش‌بود',
                'description': f'عناصر {", ".join(excessive_elements[:3])}{" و..." if len(excessive_elements) > 3 else ""} بیشتر از 130% مقدار هدف هستند.'
            })
        
        if water_salinity > 2.5:
            recommendations.append({
                'type': 'danger',
                'title': 'شوری آب بالا',
                'description': f'شوری آب {water_salinity:.2f} dS/m است. استفاده از منابع آب با کیفیت‌تر توصیه می‌شود.'
            })
        elif water_salinity > 1.5:
            recommendations.append({
                'type': 'warning',
                'title': 'شوری آب متوسط',
                'description': f'شوری آب {water_salinity:.2f} dS/m است. مراقب تجمع عناصر سمی باشید.'
            })
        
        if not recommendations:
            recommendations.append({
                'type': 'success',
                'title': 'وضعیت مطلوب',
                'description': 'تمام پارامترها در محدوده مناسب قرار دارند.'
            })
        
        # ===== آماده‌سازی داده عناصر برای جدول =====
        elements_data = []
        for element in services.ELEMENTS:
            target = target_values.get(element, 0)
            actual = final_values.get(element, 0)
            diff = actual - target
            percent = (actual / target * 100) if target > 0 else 0
            elements_data.append({
                'element': element,
                'target': target,
                'actual': actual,
                'difference': diff,
                'progress_percent': min(percent, 150)
            })
        
        return HomeSummaryResponse(
            has_data=True,
            ion_balance={
                'cation': cation,
                'anion': anion,
                'is_balanced': is_balanced,
                'message': 'تعادل یونی برقرار است ✅' if is_balanced else 'تعادل یونی برقرار نیست ⚠️'
            },
            active_elements_count=active_elements_count,
            total_elements=total_elements,
            active_reservoirs_count=active_reservoirs_count,
            total_cost=total_cost,
            total_reservoir_weight=total_reservoir_weight,
            reservoir_data=reservoir_data,
            elements_data=elements_data,
            recommendations=recommendations,
            water_salinity=water_salinity
        )
    except Exception as e:
        logger.error(f"Error in get_home_summary: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت خلاصه: {str(e)}"
        )


@calculations_router.post("/calculate-ion-balance", response_model=IonBalanceResponse)
def api_calculate_ion_balance(
    data: IonBalanceRequest,
    current_user: User = Depends(get_current_user)
):
    """محاسبه تعادل یونی"""
    try:
        cation, anion, is_balanced = services.calculate_ion_balance(data.elements, unit=data.unit)
        message = "تعادل یونی برقرار است ✅" if is_balanced else "تعادل یونی برقرار نیست ⚠️"
        return IonBalanceResponse(
            cation=cation,
            anion=anion,
            is_balanced=is_balanced,
            message=message
        )
    except Exception as e:
        logger.error(f"Error in calculate_ion_balance: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در محاسبه تعادل یونی: {str(e)}"
        )


@calculations_router.post("/calculate-final-solution", response_model=FinalSolutionResponse)
def api_calculate_final_solution(
    data: FinalSolutionRequest,
    current_user: User = Depends(get_current_user)
):
    """محاسبه محلول نهایی"""
    try:
        final_values = services.calculate_final_solution(
            target_values=data.target_values,
            water_values=data.water_values,
            fertilizer_contributions=data.fertilizer_contributions
        )
        cation, anion, is_balanced = services.calculate_ion_balance(final_values, unit="ppm")
        return FinalSolutionResponse(
            final_values=final_values,
            ion_balance=IonBalanceResponse(
                cation=cation,
                anion=anion,
                is_balanced=is_balanced,
                message="متعادل" if is_balanced else "نامتعادل"
            )
        )
    except Exception as e:
        logger.error(f"Error in calculate_final_solution: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در محاسبه محلول نهایی: {str(e)}"
        )


@calculations_router.post("/calculate-reservoir", response_model=ReservoirResponse)
def api_calculate_reservoir(
    data: ReservoirRequest,
    current_user: User = Depends(get_current_user)
):
    """محاسبه توزیع مخازن"""
    try:
        reservoir_data = services.calculate_reservoir_data(data.fertilizers)
        totals = {
            'A': sum(item['amount'] for item in reservoir_data.get('A', [])),
            'B': sum(item['amount'] for item in reservoir_data.get('B', [])),
            'C': sum(item['amount'] for item in reservoir_data.get('C', []))
        }
        return ReservoirResponse(
            reservoir_data=reservoir_data,
            totals=totals
        )
    except Exception as e:
        logger.error(f"Error in calculate_reservoir: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در محاسبه مخازن: {str(e)}"
        )


@calculations_router.post("/convert-unit", response_model=UnitConversionResponse)
def api_convert_unit(
    data: UnitConversionRequest,
    current_user: User = Depends(get_current_user)
):
    """تبدیل واحد"""
    try:
        converted_value = services.convert_units(
            value=data.value,
            from_unit=data.from_unit,
            to_unit=data.to_unit,
            element=data.element
        )
        return UnitConversionResponse(
            original_value=data.value,
            converted_value=converted_value,
            from_unit=data.from_unit,
            to_unit=data.to_unit,
            element=data.element
        )
    except Exception as e:
        logger.error(f"Error in convert_unit: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در تبدیل واحد: {str(e)}"
        )


# ============================================================
# 🆕 API بهینه‌سازی خودکار
# ============================================================

@calculations_router.post("/optimize", response_model=OptimizationResponse)
def optimize_fertilizers_endpoint(
    request: OptimizationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    🚀 بهینه‌سازی خودکار فرمول کود با استفاده از الگوریتم NNLS
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
                'is_system_default': fert.is_system_default
            })
        
        # تنظیمات بهینه‌سازی
        options = request.options.dict() if request.options else {}
        
        # ۲. اجرای بهینه‌سازی
        result = services.optimize_fertilizers(
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
                    update_data = {
                        'final_values': result.get('concentrations', {}),
                        'reservoir_data': result.get('reservoir_data', {'A': [], 'B': [], 'C': []}),
                        'calc_rows': calc_rows
                    }
                    
                    from app.schemas import CalculationUpdate
                    calc_update = CalculationUpdate(**update_data)
                    crud.update_calculation(db, calculation.id, calc_update)
                    
                    logger.info(f"✅ Updated calculation {calculation.id} with final_values and reservoir_data")
                    
        except Exception as e:
            logger.warning(f"Could not save optimization result to database: {e}")
            import traceback
            traceback.print_exc()
        
        # ۳. اعتبارسنجی نتایج
        validation = services.validate_optimization_result(result)
        if not validation['is_valid']:
            logger.warning(f"Validation errors: {validation['errors']}")
        
        # ۴. ذخیره تاریخچه
        try:
            crud.save_optimization_log(
                db=db,
                user_id=current_user.id,
                report_id=None,
                target_values=target_values,
                water_values=water_values,
                fertilizers_selected=fertilizers,
                optimization_options=options,
                result=result
            )
        except Exception as e:
            logger.warning(f"Could not save optimization log: {e}")
        
        # ۵. ساخت پاسخ
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
            summary=result['summary']
        )
        
        logger.info(f"✅ Optimization completed in {response.convergence_time_ms:.2f}ms")
        logger.info(f"   Residual error: {response.residual_error:.4f}")
        logger.info(f"   Total cost: {response.cost_total:,.0f} تومان")
        logger.info(f"   Iterations: {response.iterations}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in optimize_fertilizers_endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در بهینه‌سازی: {str(e)}"
        )


@calculations_router.post("/check-precipitation", response_model=PrecipitationCheckResponse)
def check_precipitation_endpoint(
    request: PrecipitationCheckRequest,
    current_user: User = Depends(get_current_user)
):
    """بررسی رسوب احتمالی در ترکیب عناصر"""
    try:
        result = services.check_precipitation(request.concentrations)
        
        return PrecipitationCheckResponse(
            is_safe=result['is_safe'],
            risks=result['risks'],
            suggestions=result['suggestions']
        )
    except Exception as e:
        logger.error(f"Error in check_precipitation_endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در بررسی رسوب: {str(e)}"
        )


@calculations_router.get("/optimization-history", response_model=List[OptimizationLogResponse])
def get_optimization_history_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    report_id: Optional[int] = Query(None, description="فیلتر بر اساس گزارش"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """دریافت تاریخچه بهینه‌سازی‌های انجام شده توسط کاربر"""
    try:
        logs = crud.get_optimization_history(
            db=db,
            user_id=current_user.id,
            skip=skip,
            limit=limit,
            report_id=report_id
        )
        
        return logs
    except Exception as e:
        logger.error(f"Error in get_optimization_history_endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت تاریخچه: {str(e)}"
        )


# ============================================================
# endpoint های پارامتری
# ============================================================

@calculations_router.post("/{report_id}", response_model=CalculationResponse)
def create_calculation(
    report_id: int,
    calc_data: CalculationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ایجاد محاسبات برای یک گزارش"""
    try:
        report = crud.get_report_by_id(db, report_id)
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="گزارش پیدا نشد"
            )
        if report.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="شما دسترسی به این گزارش ندارید"
            )
        existing = crud.get_calculation_by_report(db, report_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="این گزارش قبلاً محاسبات دارد"
            )
        calculation = crud.create_calculation(db, calc_data, report_id)
        return calculation
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in create_calculation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در ایجاد محاسبات: {str(e)}"
        )


@calculations_router.get("/{report_id}", response_model=CalculationResponse)
def get_calculation(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """دریافت محاسبات یک گزارش"""
    try:
        report = crud.get_report_by_id(db, report_id)
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="گزارش پیدا نشد"
            )
        if report.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="شما دسترسی به این گزارش ندارید"
            )
        calculation = crud.get_calculation_by_report(db, report_id)
        if not calculation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="محاسبات برای این گزارش پیدا نشد"
            )
        return calculation
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_calculation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت محاسبات: {str(e)}"
        )


@calculations_router.put("/{calc_id}", response_model=CalculationResponse)
def update_calculation(
    calc_id: int,
    calc_data: CalculationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """به‌روزرسانی محاسبات"""
    try:
        calculation = db.query(Calculation).filter(Calculation.id == calc_id).first()
        if not calculation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="محاسبات پیدا نشد"
            )
        report = crud.get_report_by_id(db, calculation.report_id)
        if report.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="شما دسترسی به این محاسبات ندارید"
            )
        updated_calculation = crud.update_calculation(db, calc_id, calc_data)
        return updated_calculation
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_calculation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در به‌روزرسانی محاسبات: {str(e)}"
        )


@calculations_router.post("/{report_id}/calculate", response_model=InterpretationResponse)
def calculate_and_interpret(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """تولید تفسیر کامل"""
    try:
        report = crud.get_report_by_id(db, report_id)
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="گزارش پیدا نشد"
            )
        if report.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="شما دسترسی به این گزارش ندارید"
            )
        water_analysis = crud.get_water_analysis_by_report(db, report_id)
        if not water_analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="لطفاً ابتدا آنالیز آب را وارد کنید"
            )
        calculation = crud.get_calculation_by_report(db, report_id)
        if not calculation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="لطفاً ابتدا محاسبات را انجام دهید"
            )
        target_values = calculation.target_values or {}
        final_values = calculation.final_values or {}
        water_data = {
            'water_salinity': water_analysis.water_salinity,
            'water_percentage': water_analysis.water_percentage,
            'wastewater_percentage': water_analysis.wastewater_percentage
        }
        cation, anion, is_balanced = services.calculate_ion_balance(target_values)
        interpretation = services.generate_interpretation(
            target_values=target_values,
            final_values=final_values,
            water_analysis=water_data,
            ion_balance=(cation, anion, is_balanced)
        )
        calculation.interpretation = interpretation['summary']
        db.commit()
        return interpretation
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in calculate_and_interpret: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در تولید تفسیر: {str(e)}"
        )