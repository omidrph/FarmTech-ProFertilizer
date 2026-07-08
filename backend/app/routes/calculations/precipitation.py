# backend/app/routes/calculations/precipitation.py
"""
مسیر بررسی رسوب احتمالی
"""

import logging
from fastapi import Depends, HTTPException, status
from app.schemas import PrecipitationCheckRequest, PrecipitationCheckResponse
from app.security import get_current_user
from app.models import User
from app.core import check_precipitation

logger = logging.getLogger(__name__)


def check_precipitation_endpoint(
    request: PrecipitationCheckRequest,
    current_user: User = Depends(get_current_user)
):
    """بررسی رسوب احتمالی در ترکیب عناصر با استفاده از core"""
    try:
        result = check_precipitation(request.concentrations)
        
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