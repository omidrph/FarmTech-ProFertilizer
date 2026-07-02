"""
حل‌کننده‌های الگوریتم بهینه‌سازی
================================

این فایل شامل پیاده‌سازی‌های مختلف الگوریتم بهینه‌سازی است:
- NNLS (Non-Negative Least Squares)
- LSQ-Linear (Least Squares with Bounds)
- Cost-based Optimization
"""

import time
import logging
import numpy as np
from typing import Dict, Any, Optional, Tuple, List
from scipy.optimize import nnls, lsq_linear, minimize

logger = logging.getLogger(__name__)


def optimize_with_nnls(
    A: np.ndarray,
    b: np.ndarray,
    element_weights: Optional[Dict[str, float]] = None,
    active_elements: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    بهینه‌سازی با روش NNLS (Non-Negative Least Squares)
    
    مزیت: تضمین وزن‌های غیرمنفی
    
    Args:
        A: ماتریس ضرایب (m × n)
        b: بردار هدف (m)
        element_weights: وزن‌دهی به عناصر (اختیاری)
        active_elements: لیست عناصر فعال (برای وزن‌دهی)
    
    Returns:
        Dict: شامل وزن‌ها، خطا، آمار و اطلاعات اجرا
    
    مثال:
        >>> weights, residual, iterations, time_ms = optimize_with_nnls(A, b)
        >>> print(f"Residual: {residual:.4f}, Iterations: {iterations}")
    """
    start_time = time.time()
    
    # اعمال وزن‌دهی به عناصر (اگر ارائه شده باشد)
    if element_weights and active_elements:
        from .matrix_builder import apply_element_weights
        A_weighted, b_weighted = apply_element_weights(
            A, b, element_weights, active_elements
        )
    else:
        A_weighted = A
        b_weighted = b
    
    try:
        # اجرای NNLS
        weights, residual = nnls(A_weighted, b_weighted)
        
        # اطمینان از غیرمنفی بودن وزن‌ها
        weights = np.maximum(weights, 0)
        
        # محاسبه زمان اجرا
        convergence_time_ms = (time.time() - start_time) * 1000
        
        return {
            'weights': weights,
            'residual': residual,
            'iterations': 1,  # NNLS مستقیم حل می‌کند
            'convergence_time_ms': convergence_time_ms,
            'is_converged': True,
            'method': 'nnls',
            'status': 'success'
        }
        
    except Exception as e:
        logger.error(f"Error in NNLS optimization: {e}")
        return {
            'weights': np.zeros(A.shape[1]),
            'residual': float('inf'),
            'iterations': 0,
            'convergence_time_ms': (time.time() - start_time) * 1000,
            'is_converged': False,
            'method': 'nnls',
            'status': 'error',
            'error_message': str(e)
        }


def optimize_with_lsq_linear(
    A: np.ndarray,
    b: np.ndarray,
    max_iterations: int = 1000,
    tolerance: float = 1e-6
) -> Dict[str, Any]:
    """
    بهینه‌سازی با روش Least Squares با کران‌ها
    
    مزیت: سرعت بالا برای مسائل بزرگ
    
    Args:
        A: ماتریس ضرایب (m × n)
        b: بردار هدف (m)
        max_iterations: حداکثر تعداد تکرار
        tolerance: تلرانس همگرایی
    
    Returns:
        Dict: شامل وزن‌ها، خطا، آمار و اطلاعات اجرا
    """
    start_time = time.time()
    
    try:
        result = lsq_linear(
            A,
            b,
            bounds=(0, np.inf),
            max_iter=max_iterations,
            tol=tolerance,
            method='trf'  # Trust Region Reflective
        )
        
        # اطمینان از غیرمنفی بودن وزن‌ها
        weights = np.maximum(result.x, 0)
        
        convergence_time_ms = (time.time() - start_time) * 1000
        
        return {
            'weights': weights,
            'residual': result.cost,
            'iterations': result.nit,
            'convergence_time_ms': convergence_time_ms,
            'is_converged': result.success,
            'method': 'lsq_linear',
            'status': 'success' if result.success else 'warning',
            'message': result.message if hasattr(result, 'message') else ''
        }
        
    except Exception as e:
        logger.error(f"Error in lsq_linear optimization: {e}")
        return {
            'weights': np.zeros(A.shape[1]),
            'residual': float('inf'),
            'iterations': 0,
            'convergence_time_ms': (time.time() - start_time) * 1000,
            'is_converged': False,
            'method': 'lsq_linear',
            'status': 'error',
            'error_message': str(e)
        }


def optimize_with_cost(
    A: np.ndarray,
    b: np.ndarray,
    costs: np.ndarray,
    cost_weight: float = 0.01,
    max_iterations: int = 1000,
    tolerance: float = 1e-6
) -> Dict[str, Any]:
    """
    بهینه‌سازی با در نظر گرفتن هزینه
    
    تابع هدف: min ||Ax - b||² + λ * cost(x)
    
    مزیت: انتخاب ارزان‌ترین ترکیب در صورت وجود چند جواب
    
    Args:
        A: ماتریس ضرایب (m × n)
        b: بردار هدف (m)
        costs: هزینه هر کود (تومان)
        cost_weight: ضریب اهمیت هزینه (λ)
        max_iterations: حداکثر تعداد تکرار
        tolerance: تلرانس همگرایی
    
    Returns:
        Dict: شامل وزن‌ها، خطا، آمار و اطلاعات اجرا
    """
    start_time = time.time()
    
    def objective(x):
        """تابع هدف: خطا + هزینه"""
        error = np.sum((np.dot(A, x) - b) ** 2)
        cost = np.sum(x * costs)
        return error + cost_weight * cost
    
    def gradient(x):
        """گرادیان تابع هدف"""
        grad_error = 2 * np.dot(A.T, np.dot(A, x) - b)
        grad_cost = costs
        return grad_error + cost_weight * np.array(grad_cost)
    
    try:
        result = minimize(
            objective,
            x0=np.zeros(A.shape[1]),
            method='L-BFGS-B',
            jac=gradient,
            bounds=[(0, None)] * A.shape[1],
            options={
                'maxiter': max_iterations,
                'ftol': tolerance,
                'gtol': tolerance,
                'disp': False
            }
        )
        
        # اطمینان از غیرمنفی بودن وزن‌ها
        weights = np.maximum(result.x, 0)
        
        convergence_time_ms = (time.time() - start_time) * 1000
        
        # محاسبه residual نهایی
        residual = np.sum((np.dot(A, weights) - b) ** 2)
        
        return {
            'weights': weights,
            'residual': residual,
            'iterations': result.nit,
            'convergence_time_ms': convergence_time_ms,
            'is_converged': result.success,
            'method': 'lsq_linear_with_cost',
            'status': 'success' if result.success else 'warning',
            'message': result.message if hasattr(result, 'message') else '',
            'cost_weight': cost_weight
        }
        
    except Exception as e:
        logger.error(f"Error in cost optimization: {e}")
        return {
            'weights': np.zeros(A.shape[1]),
            'residual': float('inf'),
            'iterations': 0,
            'convergence_time_ms': (time.time() - start_time) * 1000,
            'is_converged': False,
            'method': 'lsq_linear_with_cost',
            'status': 'error',
            'error_message': str(e)
        }


def solve_optimization(
    A: np.ndarray,
    b: np.ndarray,
    method: str = 'nnls',
    costs: Optional[np.ndarray] = None,
    cost_weight: float = 0.01,
    max_iterations: int = 1000,
    tolerance: float = 1e-6,
    element_weights: Optional[Dict[str, float]] = None,
    active_elements: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    حل‌کننده اصلی بهینه‌سازی با انتخاب روش
    
    Args:
        A: ماتریس ضرایب
        b: بردار هدف
        method: روش بهینه‌سازی ('nnls', 'lsq_linear', 'lsq_linear_with_cost')
        costs: هزینه هر کود (برای روش cost-based)
        cost_weight: ضریب اهمیت هزینه
        max_iterations: حداکثر تعداد تکرار
        tolerance: تلرانس همگرایی
        element_weights: وزن‌دهی به عناصر
        active_elements: لیست عناصر فعال
    
    Returns:
        Dict: نتیجه بهینه‌سازی
    
    Raises:
        ValueError: اگر روش نامعتبر باشد
    """
    logger.info(f"🔄 Starting optimization with method: {method}")
    
    if method == 'nnls':
        return optimize_with_nnls(A, b, element_weights, active_elements)
    
    elif method == 'lsq_linear':
        return optimize_with_lsq_linear(A, b, max_iterations, tolerance)
    
    elif method == 'lsq_linear_with_cost':
        if costs is None:
            raise ValueError("برای روش cost-based، هزینه‌ها باید ارائه شوند")
        return optimize_with_cost(
            A, b, costs, cost_weight, max_iterations, tolerance
        )
    
    else:
        raise ValueError(f"روش {method} پشتیبانی نمی‌شود")