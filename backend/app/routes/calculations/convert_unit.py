# backend/app/routes/calculations/convert_unit.py
"""
مسیر تبدیل واحدها
"""

import logging
from fastapi import Depends, HTTPException, status
from app.schemas import UnitConversionRequest, UnitConversionResponse
from app.security import get_current_user
from app.models import User
from app.core import convert_units as core_convert_units

logger = logging.getLogger(__name__)


def api_convert_unit(
    data: UnitConversionRequest,
    current_user: User = Depends(get_current_user)
):
    """تبدیل واحد با استفاده از core"""
    try:
        converted_value = core_convert_units(
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