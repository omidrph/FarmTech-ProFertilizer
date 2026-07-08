# backend/app/routes/calculations/interpretation.py
"""
مسیر تولید تفسیر داده‌ها
"""

import logging
from typing import Dict, Any, Tuple
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import InterpretationResponse, IonBalanceResponse
import app.crud as crud
from app.security import get_current_user
from app.core import calculate_ion_balance, ALL_ELEMENTS

logger = logging.getLogger(__name__)


def calculate_and_interpret(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """تولید تفسیر کامل با استفاده از core"""
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
        
        # استفاده از core برای محاسبه تعادل یونی
        cation, anion, is_balanced, _ = calculate_ion_balance(
            target_values, unit="ppm"
        )
        
        # تولید تفسیر
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


# ============================================================
# تابع کمکی برای تولید تفسیر
# ============================================================

def generate_interpretation(
    target_values: Dict[str, float],
    final_values: Dict[str, float],
    water_analysis: Dict[str, float],
    ion_balance: Tuple[float, float, bool]
) -> Dict[str, Any]:
    """
    تولید تفسیر از داده‌ها
    """
    cation, anion, is_balanced = ion_balance
    
    # وضعیت عناصر
    element_status = []
    for element in ALL_ELEMENTS:
        target = target_values.get(element, 0)
        actual = final_values.get(element, 0)
        diff = actual - target
        
        if target == 0:
            status = 'sufficient'
            message = 'نیازی به تنظیم ندارد'
        else:
            percent = (actual / target) * 100
            if percent < 70:
                status = 'deficient'
                message = 'کمبود دارد'
            elif percent > 130:
                status = 'excessive'
                message = 'بیش‌بود دارد'
            else:
                status = 'sufficient'
                message = 'در محدوده مطلوب'
        
        element_status.append({
            'element': element,
            'target': target,
            'actual': actual,
            'difference': diff,
            'status': status,
            'message': message
        })
    
    # کیفیت آب
    salinity = water_analysis.get('water_salinity', 0)
    if salinity < 0.75:
        water_impact = 'مناسب'
        water_recommendation = 'کیفیت آب عالی است'
    elif salinity < 2.0:
        water_impact = 'متوسط'
        water_recommendation = 'کیفیت آب قابل قبول است، اما مراقب باشید'
    else:
        water_impact = 'بالا'
        water_recommendation = 'شوری آب بالا است، از کودهای با EC پایین استفاده کنید'
    
    # توصیه‌های کودی
    recommendations = []
    for status in element_status:
        if status['status'] == 'deficient':
            recommendations.append({
                'issue': f'کمبود {status["element"]}',
                'suggestion': f'کود حاوی {status["element"]} را افزایش دهید',
                'priority': 'high'
            })
        elif status['status'] == 'excessive':
            recommendations.append({
                'issue': f'بیش‌بود {status["element"]}',
                'suggestion': f'مصرف کود حاوی {status["element"]} را کاهش دهید',
                'priority': 'medium'
            })
    
    if not is_balanced:
        recommendations.append({
            'issue': 'عدم تعادل یونی',
            'suggestion': 'تعادل کاتیون و آنیون را برقرار کنید',
            'priority': 'high'
        })
    
    # خلاصه
    summary_lines = [
        "📊 **خلاصه تفسیر**",
        "",
        f"⚖️ **تعادل یونی:** {'✅ متعادل' if is_balanced else '⚠️ نامتعادل'}",
        f"   کاتیون: {cation:.2f} meq/L | آنیون: {anion:.2f} meq/L",
        f"💧 **کیفیت آب:** {water_impact} (EC: {salinity:.2f} dS/m)",
        "",
        "📈 **وضعیت عناصر:**"
    ]
    
    for status in element_status[:8]:
        if status['target'] > 0:
            summary_lines.append(f"   - {status['element']}: {status['message']}")
    
    if recommendations:
        summary_lines.append("")
        summary_lines.append("💡 **توصیه‌ها:**")
        for rec in recommendations[:3]:
            summary_lines.append(f"   - {rec['suggestion']}")
    
    return {
        'ion_balance': IonBalanceResponse(
            cation=cation,
            anion=anion,
            is_balanced=is_balanced,
            message='تعادل یونی برقرار است ✅' if is_balanced else 'تعادل یونی برقرار نیست ⚠️'
        ),
        'element_status': element_status,
        'water_quality': {
            'salinity': salinity,
            'impact': water_impact,
            'recommendation': water_recommendation
        },
        'fertilizer_recommendation': recommendations,
        'summary': "\n".join(summary_lines)
    }