# backend/app/routes/calculations.py
"""مسیرهای محاسبات (Calculations)"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from app.database import get_db
from app.models import User, Calculation
from app.schemas import (
    CalculationCreate, CalculationUpdate, CalculationResponse,
    HomeSummaryResponse, IonBalanceRequest, IonBalanceResponse,
    FinalSolutionRequest, FinalSolutionResponse,
    ReservoirRequest, ReservoirResponse,
    UnitConversionRequest, UnitConversionResponse,
    InterpretationResponse
)
import app.crud as crud
from app.security import get_current_user
from app.services import (
    calculate_ion_balance,
    calculate_final_solution,
    calculate_reservoir_data,
    generate_interpretation,
    convert_units,
    ELEMENTS
)

# ===== تنظیمات Logger =====
logger = logging.getLogger(__name__)

# ===== ایجاد Router =====
calculations_router = APIRouter(prefix="/calculations", tags=["Calculations"])

# ============================================================
# 🆕 APIهای محاسباتی ثابت (بدون پارامتر)
# ⚠️ باید قبل از endpoint های پارامتری باشند
# ============================================================

@calculations_router.get("/home-summary", response_model=HomeSummaryResponse)
def get_home_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """🆕 دریافت خلاصه داشبورد - تمام محاسبات در بک‌اند انجام می‌شود"""
    try:
        logger.info(f"Getting home summary for user {current_user.id}")
        
        # دریافت آخرین گزارش کاربر
        reports = crud.get_reports_by_user(db, current_user.id, skip=0, limit=1)
        if not reports:
            return HomeSummaryResponse(
                has_data=False,
                message="هنوز گزارشی ایجاد نشده است"
            )
        
        report = reports[0]
        water_analysis = crud.get_water_analysis_by_report(db, report.id)
        water_salinity = water_analysis.water_salinity if water_analysis else 0
        calculation = crud.get_calculation_by_report(db, report.id)
        
        if not calculation:
            return HomeSummaryResponse(
                has_data=False,
                message="هنوز محاسباتی انجام نشده است"
            )
        
        target_values = calculation.target_values or {}
        final_values = calculation.final_values or {}
        reservoir_data = calculation.reservoir_data or {}
        
        # محاسبه تعادل یونی از طریق service
        cation, anion, is_balanced = calculate_ion_balance(target_values, unit="ppm")
        
        # محاسبه آمار
        active_elements_count = sum(1 for v in target_values.values() if v and v > 0)
        total_elements = len(ELEMENTS)
        
        active_reservoirs_count = 0
        if reservoir_data.get('A') and len(reservoir_data['A']) > 0:
            active_reservoirs_count += 1
        if reservoir_data.get('B') and len(reservoir_data['B']) > 0:
            active_reservoirs_count += 1
        if reservoir_data.get('C') and len(reservoir_data['C']) > 0:
            active_reservoirs_count += 1
        
        # محاسبه مجموع هزینه
        total_cost = 0
        if calculation.calc_rows:
            for row in calculation.calc_rows:
                total_cost += row.get('cost', 0)
        
        # محاسبه مجموع وزن مخازن
        total_reservoir_weight = 0
        for reservoir_items in reservoir_data.values():
            if isinstance(reservoir_items, list):
                for item in reservoir_items:
                    total_reservoir_weight += item.get('amount', 0)
        
        # تولید توصیه‌ها در بک‌اند
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
        for element in ELEMENTS:
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
        
        # آماده‌سازی داده عناصر برای جدول
        elements_data = []
        for element in ELEMENTS:
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت خلاصه: {str(e)}"
        )

@calculations_router.post("/calculate-ion-balance", response_model=IonBalanceResponse)
def api_calculate_ion_balance(
    data: IonBalanceRequest,
    current_user: User = Depends(get_current_user)
):
    """🆕 محاسبه تعادل یونی"""
    try:
        cation, anion, is_balanced = calculate_ion_balance(data.elements, unit=data.unit)
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
    """🆕 محاسبه محلول نهایی"""
    try:
        final_values = calculate_final_solution(
            target_values=data.target_values,
            water_values=data.water_values,
            fertilizer_contributions=data.fertilizer_contributions
        )
        cation, anion, is_balanced = calculate_ion_balance(final_values, unit="ppm")
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
    """🆕 محاسبه توزیع مخازن"""
    try:
        reservoir_data = calculate_reservoir_data(data.fertilizers)
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
    """🆕 تبدیل واحد"""
    try:
        converted_value = convert_units(
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
# endpoint های پارامتری (با پارامتر)
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
        cation, anion, is_balanced = calculate_ion_balance(target_values)
        interpretation = generate_interpretation(
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