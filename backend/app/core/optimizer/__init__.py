"""
ماژول بهینه‌سازی فرمول کود (NNLS)
================================

این ماژول شامل تمام توابع مربوط به بهینه‌سازی فرمول کود است:
- ساخت ماتریس ضرایب
- حل‌کننده‌های مختلف (NNLS, LSQ-Linear, Cost-based)
- پردازش نتایج
- اعتبارسنجی نتایج
- تابع اصلی بهینه‌سازی
"""

from .matrix_builder import (
    build_optimization_matrix,
    prepare_fertilizer_data
)

from .nnls_solver import (
    optimize_with_nnls,
    optimize_with_lsq_linear,
    optimize_with_cost,
    solve_optimization
)

from .result_processor import (
    calculate_final_concentrations,
    calculate_target_achievement,
    generate_optimization_summary,
    validate_optimization_result,
    process_optimization_result
)

from .main import optimize_fertilizers

__all__ = [
    # Matrix Builder
    'build_optimization_matrix',
    'prepare_fertilizer_data',
    # NNLS Solver
    'optimize_with_nnls',
    'optimize_with_lsq_linear',
    'optimize_with_cost',
    'solve_optimization',
    # Result Processor
    'calculate_final_concentrations',
    'calculate_target_achievement',
    'generate_optimization_summary',
    'validate_optimization_result',
    'process_optimization_result',
    # Main
    'optimize_fertilizers'
]