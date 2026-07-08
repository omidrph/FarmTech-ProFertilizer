# backend/app/routes/calculations/ion_balance.py
"""
مسیر محاسبه تعادل یونی
"""

import logging
from fastapi import Depends, HTTPException, status
from app.schemas import IonBalanceRequest, IonBalanceResponse
from app.security import get_current_user
from app.models import User
from app.core import calculate_ion_balance

logger = logging.getLogger(__name__)


def api_calculate_ion_balance(
    data: IonBalanceRequest,
    current_user: User = Depends(get_current_user)
):
    """محاسبه تعادل یونی با استفاده از core"""
    try:
        cation, anion, is_balanced, details = calculate_ion_balance(
            data.elements, unit=data.unit
        )
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