# backend/app/routes/calculations/final_solution.py
"""
مسیر محاسبه محلول نهایی
"""

import logging
import numpy as np
from fastapi import Depends, HTTPException, status
from app.schemas import FinalSolutionRequest, FinalSolutionResponse, IonBalanceResponse
from app.security import get_current_user
from app.models import User
from app.core import calculate_ion_balance
from app.core.optimizer.result_processor import calculate_final_concentrations

logger = logging.getLogger(__name__)


def api_calculate_final_solution(
    data: FinalSolutionRequest,
    current_user: User = Depends(get_current_user)
):
    """محاسبه محلول نهایی"""
    try:
        active_elements = list(data.target_values.keys())
        A = np.array([[1.0 if el in data.fertilizer_contributions else 0.0 for el in active_elements]])
        weights = np.array([1.0])
        
        final_values = calculate_final_concentrations(
            weights=weights,
            A=A,
            water_values=data.water_values,
            active_elements=active_elements
        )
        
        cation, anion, is_balanced, _ = calculate_ion_balance(
            final_values, unit="ppm"
        )
        
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