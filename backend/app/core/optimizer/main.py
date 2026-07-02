"""
تابع اصلی بهینه‌سازی فرمول کود
================================

این فایل شامل تابع اصلی `optimize_fertilizers` است که قلب تپنده سیستم بهینه‌سازی است.
"""

import time
import logging
import numpy as np
from typing import Dict, List, Any, Optional

from .matrix_builder import build_optimization_matrix
from .nnls_solver import solve_optimization
from .result_processor import process_optimization_result

logger = logging.getLogger(__name__)


def optimize_fertilizers(
    target_values: Dict[str, float],
    fertilizers: List[Dict[str, Any]],
    water_values: Optional[Dict[str, float]] = None,
    options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    🎯 تابع اصلی بهینه‌سازی ترکیب کودها
    
    این تابع قلب تپنده FarmTech است. با استفاده از الگوریتم NNLS،
    بهترین ترکیب کودها را محاسبه می‌کند.
    
    Args:
        target_values: عناصر هدف (ppm)
        fertilizers: لیست کودها با عناصر و قیمت
        water_values: عناصر موجود در آب (اختیاری)
        options: تنظیمات بهینه‌سازی (اختیاری)
    
    Returns:
        Dict: شامل وزن‌ها، غلظت‌ها، خطا، تحلیل و توصیه‌ها
    
    Raises:
        ValueError: اگر هیچ عنصر هدفی تعریف نشده باشد
        ValueError: اگر هیچ کودی انتخاب نشده باشد
    
    مثال:
        >>> targets = {'K': 250, 'N-NO3': 200}
        >>> ferts = [{'id': '1', 'name': 'KNO3', 'elements': {'K': 38, 'N-NO3': 13}, 'price_per_kg': 750000}]
        >>> result = optimize_fertilizers(targets, ferts)
        >>> print(result['summary'])
        ...
    """
    start_time = time.time()
    
    # ===== ۱. آماده‌سازی =====
    water_values = water_values or {}
    options = options or {}
    
    # تنظیمات پیش‌فرض
    method = options.get('method', 'nnls')
    element_weights = options.get('element_weights', {})
    max_iterations = options.get('max_iterations', 1000)
    tolerance = options.get('tolerance', 1e-6)
    cost_weight = options.get('cost_weight', 0.01)
    use_precipitation_check = options.get('use_precipitation_check', True)
    use_ion_balance_check = options.get('use_ion_balance_check', True)
    
    logger.info(f"🚀 Starting optimization with method: {method}")
    logger.info(f"   Targets: {len(target_values)} elements")
    logger.info(f"   Fertilizers: {len(fertilizers)} items")
    
    # ===== ۲. ساخت ماتریس =====
    try:
        A, b, active_elements, fertilizer_names, matrix_stats = build_optimization_matrix(
            target_values, fertilizers, water_values
        )
    except ValueError as e:
        return {
            'error': str(e),
            'weights': {},
            'concentrations': {},
            'residual_error': 0,
            'cost_total': 0,
            'ion_balance': {'cation': 0, 'anion': 0, 'is_balanced': False, 'message': ''},
            'target_achievement': {},
            'warnings': [],
            'suggestions': [],
            'iterations': 0,
            'convergence_time_ms': (time.time() - start_time) * 1000,
            'is_converged': False,
            'summary': f"❌ خطا: {str(e)}"
        }
    
    if A.shape[1] == 0:
        return {
            'error': 'هیچ کودی انتخاب نشده است',
            'weights': {},
            'concentrations': {},
            'residual_error': 0,
            'cost_total': 0,
            'ion_balance': {'cation': 0, 'anion': 0, 'is_balanced': False, 'message': ''},
            'target_achievement': {},
            'warnings': [],
            'suggestions': [],
            'iterations': 0,
            'convergence_time_ms': (time.time() - start_time) * 1000,
            'is_converged': False,
            'summary': '❌ هیچ کودی انتخاب نشده است. لطفاً حداقل یک کود را انتخاب کنید.'
        }
    
    # ===== ۳. آماده‌سازی هزینه‌ها =====
    costs = np.array([fert.get('price_per_kg', 0) / 1000 for fert in fertilizers])
    
    # ===== ۴. اجرای بهینه‌سازی =====
    try:
        solver_result = solve_optimization(
            A=A,
            b=b,
            method=method,
            costs=costs,
            cost_weight=cost_weight,
            max_iterations=max_iterations,
            tolerance=tolerance,
            element_weights=element_weights,
            active_elements=active_elements
        )
    except Exception as e:
        logger.error(f"Optimization error: {e}")
        return {
            'error': f'خطا در بهینه‌سازی: {str(e)}',
            'weights': {},
            'concentrations': {},
            'residual_error': 0,
            'cost_total': 0,
            'ion_balance': {'cation': 0, 'anion': 0, 'is_balanced': False, 'message': ''},
            'target_achievement': {},
            'warnings': [],
            'suggestions': [],
            'iterations': 0,
            'convergence_time_ms': (time.time() - start_time) * 1000,
            'is_converged': False,
            'summary': f"❌ خطا در بهینه‌سازی: {str(e)}"
        }
    
    # ===== ۵. پردازش نتایج =====
    try:
        # اضافه کردن تنظیمات به options برای پردازش
        options['use_precipitation_check'] = use_precipitation_check
        options['use_ion_balance_check'] = use_ion_balance_check
        
        result = process_optimization_result(
            solver_result=solver_result,
            A=A,
            active_elements=active_elements,
            fertilizer_names=fertilizer_names,
            fertilizers=fertilizers,
            target_values=target_values,
            water_values=water_values,
            costs=costs,
            options=options
        )
        
        # اضافه کردن زمان کل
        result['total_time_ms'] = (time.time() - start_time) * 1000
        
        logger.info(f"✅ Optimization completed in {result['convergence_time_ms']:.2f}ms")
        logger.info(f"   Residual error: {result['residual_error']:.4f}")
        logger.info(f"   Total cost: {result['cost_total']:,.0f} تومان")
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing optimization result: {e}")
        return {
            'error': f'خطا در پردازش نتایج: {str(e)}',
            'weights': {},
            'concentrations': {},
            'residual_error': 0,
            'cost_total': 0,
            'ion_balance': {'cation': 0, 'anion': 0, 'is_balanced': False, 'message': ''},
            'target_achievement': {},
            'warnings': [],
            'suggestions': [],
            'iterations': 0,
            'convergence_time_ms': (time.time() - start_time) * 1000,
            'is_converged': False,
            'summary': f"❌ خطا در پردازش نتایج: {str(e)}"
        }