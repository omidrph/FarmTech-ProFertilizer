# backend/app/routes/calculations/reservoir.py
"""
مسیر محاسبه توزیع مخازن
"""

import logging
from fastapi import Depends, HTTPException, status
from app.schemas import ReservoirRequest, ReservoirResponse
from app.security import get_current_user
from app.models import User
from app.core import calculate_reservoir_data

logger = logging.getLogger(__name__)


def api_calculate_reservoir(
    data: ReservoirRequest,
    current_user: User = Depends(get_current_user)
):
    """محاسبه توزیع مخازن با استفاده از core"""
    try:
        # تبدیل داده‌های ورودی به فرمت مورد نیاز
        fertilizers = []
        for item in data.fertilizers:
            fert = item.get('fertilizer', {})
            weight = item.get('weight', 0)
            fertilizers.append({
                'id': fert.get('id', ''),
                'name': fert.get('name', 'نامشخص'),
                'elements': fert.get('elements', {}),
                'is_acid': fert.get('is_acid', False)
            })
        
        # ساخت دیکشنری وزن‌ها
        weights = {}
        for item in data.fertilizers:
            fert_id = str(item.get('fertilizer', {}).get('id', ''))
            weight = item.get('weight', 0)
            if fert_id and weight > 0:
                weights[fert_id] = weight
        
        reservoir_data = calculate_reservoir_data(fertilizers, weights)
        
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