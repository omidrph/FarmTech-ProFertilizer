# backend/app/schemas/__init__.py
"""
ماژول طرح‌های Pydantic
همه طرح‌ها از اینجا export می‌شوند تا فایل‌های دیگر نیازی به تغییر نداشته باشند
"""

# ============================================================
# Export از auth.py
# ============================================================
from .auth import (
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
    Token,
    TokenData,
    ChangePasswordRequest,
    ChangePasswordResponse,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    ResetPasswordRequest,
    ResetPasswordResponse,
    Enable2FARequest,
    Enable2FAResponse,
    Verify2FARequest,
    Verify2FAResponse,
    Disable2FARequest,
    Disable2FAResponse,
)

# ============================================================
# Export از fertilizer.py
# ============================================================
from .fertilizer import (
    FertilizerCreate,
    FertilizerUpdate,
    FertilizerResponse,
)

# ============================================================
# Export از report.py
# ============================================================
from .report import (
    ReportCreate,
    ReportUpdate,
    ReportResponse,
)

# ============================================================
# Export از water_analysis.py
# ============================================================
from .water_analysis import (
    WaterAnalysisCreate,
    WaterAnalysisUpdate,
    WaterAnalysisResponse,
)

# ============================================================
# Export از calculation.py
# ============================================================
from .calculation import (
    CalculationCreate,
    CalculationUpdate,
    CalculationResponse,
)

# ============================================================
# Export از recipe.py
# ============================================================
from .recipe import (
    RecipeBase,
    RecipeCreate,
    RecipeUpdate,
    RecipeResponse,
    RecipeListResponse,
)

# ============================================================
# Export از water_template.py
# ============================================================
from .water_template import (
    WaterAnalysisTemplateCreate,
    WaterAnalysisTemplateUpdate,
    WaterAnalysisTemplateResponse,
)

# ============================================================
# Export از optimization.py
# ============================================================
from .optimization import (
    OptimizationOptions,
    OptimizationFertilizerInput,
    OptimizationRequest,
    OptimizationResponse,
    EcPhStatusResponse,
    OptimizationLogResponse,
    PrecipitationCheckRequest,
    PrecipitationRiskItem,
    PrecipitationCheckResponse,
    ManualWeightRecalculateRequest,
)

# ============================================================
# Export از interpretation.py
# ============================================================
from .interpretation import (
    ElementStatusResponse,
    WaterQualityResponse,
    RecommendationResponse,
    InterpretationResponse,
)

# ============================================================
# Export از common.py
# ============================================================
from .common import (
    IonBalanceRequest,
    IonBalanceResponse,
    FinalSolutionRequest,
    FinalSolutionResponse,
    ReservoirRequest,
    ReservoirResponse,
    UnitConversionRequest,
    UnitConversionResponse,
    HomeSummaryElementData,
    HomeSummaryRecommendation,
    HomeSummaryResponse,
    MessageResponse,
    PaginatedResponse,
)

# ============================================================
# Export از base.py
# ============================================================
from .base import (
    SecureString,
    validate_phone_number,
    validate_password_strength,
    validate_name,
    validate_element_name,
    validate_code,
)

# ============================================================
# لیست همه موارد Export شده
# ============================================================
__all__ = [
    # Auth
    'UserCreate',
    'UserLogin',
    'UserResponse',
    'UserUpdate',
    'Token',
    'TokenData',
    'ChangePasswordRequest',
    'ChangePasswordResponse',
    'ForgotPasswordRequest',
    'ForgotPasswordResponse',
    'ResetPasswordRequest',
    'ResetPasswordResponse',
    'Enable2FARequest',
    'Enable2FAResponse',
    'Verify2FARequest',
    'Verify2FAResponse',
    'Disable2FARequest',
    'Disable2FAResponse',
    
    # Fertilizer
    'FertilizerCreate',
    'FertilizerUpdate',
    'FertilizerResponse',
    
    # Report
    'ReportCreate',
    'ReportUpdate',
    'ReportResponse',
    
    # Water Analysis
    'WaterAnalysisCreate',
    'WaterAnalysisUpdate',
    'WaterAnalysisResponse',
    
    # Calculation
    'CalculationCreate',
    'CalculationUpdate',
    'CalculationResponse',
    
    # Recipe
    'RecipeBase',
    'RecipeCreate',
    'RecipeUpdate',
    'RecipeResponse',
    'RecipeListResponse',
    
    # Water Template
    'WaterAnalysisTemplateCreate',
    'WaterAnalysisTemplateUpdate',
    'WaterAnalysisTemplateResponse',
    
    # Optimization
    'OptimizationOptions',
    'OptimizationFertilizerInput',
    'OptimizationRequest',
    'OptimizationResponse',
    'EcPhStatusResponse',
    'OptimizationLogResponse',
    'ManualWeightRecalculateRequest',
    'PrecipitationCheckRequest',
    'PrecipitationRiskItem',
    'PrecipitationCheckResponse',
    
    # Interpretation
    'ElementStatusResponse',
    'WaterQualityResponse',
    'RecommendationResponse',
    'InterpretationResponse',
    
    # Common
    'IonBalanceRequest',
    'IonBalanceResponse',
    'FinalSolutionRequest',
    'FinalSolutionResponse',
    'ReservoirRequest',
    'ReservoirResponse',
    'UnitConversionRequest',
    'UnitConversionResponse',
    'HomeSummaryElementData',
    'HomeSummaryRecommendation',
    'HomeSummaryResponse',
    'MessageResponse',
    'PaginatedResponse',
    
    # Base
    'SecureString',
    'validate_phone_number',
    'validate_password_strength',
    'validate_name',
    'validate_element_name',
    'validate_code',
]


