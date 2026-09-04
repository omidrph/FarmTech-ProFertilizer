# backend/app/routes/calculations/router.py
"""
Router اصلی ماژول محاسبات
تمام مسیرها در اینجا ثبت می‌شوند
"""

from typing import List
from fastapi import APIRouter

from app.schemas import (
    HomeSummaryResponse,
    IonBalanceResponse,
    FinalSolutionResponse,
    ReservoirResponse,
    UnitConversionResponse,
    OptimizationResponse,
    PrecipitationCheckResponse,
    OptimizationLogResponse,
    CalculationResponse,
    InterpretationResponse
)

from .home_summary import get_home_summary
from .ion_balance import api_calculate_ion_balance
from .final_solution import api_calculate_final_solution
from .reservoir import api_calculate_reservoir
from .convert_unit import api_convert_unit
from .optimization import optimize_fertilizers_endpoint
from .recalculate import recalculate_manual_weights
from .precipitation import check_precipitation_endpoint
from .history import get_optimization_history_endpoint
from .crud_calculations import create_calculation, get_calculation, update_calculation
from .interpretation import calculate_and_interpret

# ===== ایجاد Router =====
calculations_router = APIRouter(prefix="/calculations", tags=["Calculations"])

# ============================================================
# ثبت همه مسیرها با دکوراتور
# ============================================================

# ---- مسیرهای محاسباتی بدون پارامتر ----
calculations_router.get("/home-summary", response_model=HomeSummaryResponse)(get_home_summary)
calculations_router.post("/calculate-ion-balance", response_model=IonBalanceResponse)(api_calculate_ion_balance)
calculations_router.post("/calculate-final-solution", response_model=FinalSolutionResponse)(api_calculate_final_solution)
calculations_router.post("/calculate-reservoir", response_model=ReservoirResponse)(api_calculate_reservoir)
calculations_router.post("/convert-unit", response_model=UnitConversionResponse)(api_convert_unit)

# ---- مسیرهای بهینه‌سازی ----
calculations_router.post("/optimize", response_model=OptimizationResponse)(optimize_fertilizers_endpoint)
# 🆕 محاسبه مجدد پس از ویرایش دستی وزن یک کود در جدول نتیجه
calculations_router.post("/recalculate-manual", response_model=OptimizationResponse)(recalculate_manual_weights)
calculations_router.post("/check-precipitation", response_model=PrecipitationCheckResponse)(check_precipitation_endpoint)
calculations_router.get("/optimization-history", response_model=List[OptimizationLogResponse])(get_optimization_history_endpoint)

# ---- مسیرهای CRUD ----
calculations_router.post("/{report_id}", response_model=CalculationResponse)(create_calculation)
calculations_router.get("/{report_id}", response_model=CalculationResponse)(get_calculation)
calculations_router.put("/{calc_id}", response_model=CalculationResponse)(update_calculation)

# ---- مسیر تفسیر ----
calculations_router.post("/{report_id}/calculate", response_model=InterpretationResponse)(calculate_and_interpret)


