# backend/app/routes/calculations/home_summary.py
"""
مسیر دریافت خلاصه داشبورد (Home Summary)
"""

import logging
import json
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import HomeSummaryResponse
import app.crud as crud
from app.security import get_current_user
from app.core import (
    calculate_ion_balance,
    calculate_ec,
    calculate_ph,
    get_ec_ph_status,
    ALL_ELEMENTS
)

logger = logging.getLogger(__name__)


# ============================================================
# ✅ بدون دکوراتور - فقط تابع خالص
# ============================================================

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
        
        # ===== محاسبه تعادل یونی با استفاده از core =====
        cation, anion, is_balanced, ion_details = calculate_ion_balance(
            target_values, unit="ppm"
        )
        
        # ===== محاسبه EC و pH =====
        ec_result = calculate_ec(final_values, unit="ppm")
        ph_result = calculate_ph(final_values, unit="ppm", water_ph=None)
        ec_ph_status = get_ec_ph_status(
            ec=ec_result['ec'],
            ph=ph_result['ph'],
            water_ec=water_salinity,
            water_ph=None
        )
        
        # ===== محاسبه آمار =====
        active_elements_count = sum(1 for v in target_values.values() if v and v > 0)
        total_elements = len(ALL_ELEMENTS)
        
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
        
        # توصیه‌های EC
        if ec_result['status'] in ['low', 'high', 'critical']:
            recommendations.append({
                'type': ec_result['color'],
                'title': f'EC {ec_result["status_label"]}',
                'description': ec_result['recommendation']
            })
        
        # توصیه‌های pH
        if ph_result['status'] in ['low', 'high', 'critical_low', 'critical_high']:
            recommendations.append({
                'type': ph_result['color'],
                'title': f'pH {ph_result["status_label"]}',
                'description': ph_result['recommendation']
            })
        
        deficient_elements = []
        excessive_elements = []
        for element in ALL_ELEMENTS:
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
        for element in ALL_ELEMENTS:
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