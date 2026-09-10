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


def optimize_sparse_nnls(
    A: np.ndarray,
    b: np.ndarray,
    costs: Optional[np.ndarray] = None,
    max_fertilizers: Optional[int] = None,
    max_residual_increase_pct: float = 25.0
) -> Dict[str, Any]:
    """
    🆕 نسخه «کم‌تعداد» بهینه‌سازی: ترکیبی با کمترین تعداد کود ممکن.

    چرا لازم است: NNLS به‌خودی‌خود sparse (کم‌تعداد) نیست — معمولاً از
    هر کود موجود مقداری استفاده می‌کند، حتی مقادیر خیلی کوچک و
    غیرعملی. خیلی از کشاورزان توانایی/تمایل تهیه ۱۵-۲۰ نوع کود مختلف را
    ندارند و ترجیح می‌دهند با مثلاً ۵-۶ کود اصلی کار کنند، حتی با کمی
    خطای بیشتر نسبت به هدف.

    الگوریتم: حذف تدریجی (Greedy Backward Elimination)
        ۱. ابتدا NNLS معمولی روی همه کودها اجرا می‌شود (baseline).
        ۲. در هر مرحله، کودی که کمترین وزن غیرصفر را دارد به‌طور
           آزمایشی حذف می‌شود و دوباره NNLS روی بقیه کودها اجرا می‌شود.
        ۳. اگر افزایش خطا (residual) از سقف مجاز (`max_residual_increase_pct`)
           بیشتر نشود، حذف قطعی می‌شود و ادامه می‌دهیم.
        ۴. متوقف می‌شویم وقتی: به `max_fertilizers` رسیدیم، یا دیگر
           حذفی بدون افزایش بیش‌ازحد خطا ممکن نیست.

    این روش بهینهٔ مطلق (که نیازمند بررسی تمام زیرمجموعه‌ها و از نظر
    محاسباتی غیرعملی است) نیست، اما یک تقریب استاندارد و رایج
    (greedy sparse approximation) برای این نوع مسئله است.

    Args:
        A: ماتریس ضرایب (m × n)
        b: بردار هدف (m)
        costs: هزینه هر کود (برای ترجیح حذف کودهای گران‌تر در تساوی خطا - اختیاری)
        max_fertilizers: حداکثر تعداد کود مجاز در جواب نهایی
        max_residual_increase_pct: حداکثر درصد مجاز افزایش خطا نسبت به
            جواب کامل NNLS (پیش‌فرض ۲۵٪)

    Returns:
        Dict: مشابه optimize_with_nnls، به‌علاوه 'removed_count' و
            'baseline_residual'
    """
    start_time = time.time()
    n = A.shape[1]

    baseline = optimize_with_nnls(A, b)
    baseline_residual = baseline['residual']
    weights = baseline['weights'].copy()

    active_indices = list(np.where(weights > 1e-9)[0])
    removed_count = 0

    def _current_nonzero_count(idx_list, w):
        return sum(1 for i in idx_list if w[i] > 1e-9)

    while True:
        nonzero_count = _current_nonzero_count(active_indices, weights)

        if max_fertilizers is not None and nonzero_count <= max_fertilizers:
            break
        if len(active_indices) <= 1:
            break

        # کاندیدهای حذف: کودهای فعال، به ترتیب کوچک‌ترین وزن اول
        candidates = sorted(active_indices, key=lambda i: weights[i])

        removed_this_round = False
        for candidate in candidates:
            trial_indices = [i for i in active_indices if i != candidate]
            if not trial_indices:
                continue

            A_trial = A[:, trial_indices]
            trial_result = optimize_with_nnls(A_trial, b)
            trial_residual = trial_result['residual']

            residual_increase_pct = (
                ((trial_residual - baseline_residual) / baseline_residual * 100)
                if baseline_residual > 1e-9 else
                (0 if trial_residual < 1e-6 else float('inf'))
            )

            # اگر هنوز به سقف تعداد نرسیده‌ایم، فقط وقتی حذف می‌کنیم که
            # خطا بیش‌ازحد مجاز افزایش نیابد؛ اگر کاربر صریحاً سقف تعداد
            # داده (max_fertilizers)، حتی با خطای بیشتر هم به آن سقف
            # می‌رسیم (چون این خواستهٔ صریح کاربر است).
            must_reduce = max_fertilizers is not None and nonzero_count > max_fertilizers
            if must_reduce or residual_increase_pct <= max_residual_increase_pct:
                active_indices = trial_indices
                new_weights = np.zeros(n)
                new_weights[trial_indices] = trial_result['weights']
                weights = new_weights
                removed_count += 1
                removed_this_round = True
                break

        if not removed_this_round:
            # هیچ حذفی بدون افزایش بیش‌ازحد خطا ممکن نبود
            break

    final_residual = float(np.sum((np.dot(A, weights) - b) ** 2)) ** 0.5 if A.shape[0] > 0 else 0.0

    return {
        'weights': weights,
        'residual': final_residual,
        'iterations': removed_count + 1,
        'convergence_time_ms': (time.time() - start_time) * 1000,
        'is_converged': True,
        'method': 'nnls_sparse',
        'status': 'success',
        'removed_count': removed_count,
        'baseline_residual': baseline_residual,
        'final_fertilizer_count': _current_nonzero_count(active_indices, weights)
    }


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
    active_elements: Optional[List[str]] = None,
    prefer_fewer_fertilizers: bool = False,
    max_fertilizers_count: Optional[int] = None,
    prefer_cheapest: bool = False
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
        prefer_fewer_fertilizers: 🆕 اگر فعال باشد، از الگوریتم حذف
            تدریجی (greedy sparse) برای رسیدن به کمترین تعداد کود ممکن
            استفاده می‌شود.
        max_fertilizers_count: 🆕 حداکثر تعداد کود مجاز (فقط وقتی
            prefer_fewer_fertilizers فعال است معنا دارد)
        prefer_cheapest: 🆕 اگر فعال باشد و costs موجود باشد، از روش
            cost-aware (lsq_linear_with_cost با ضریب هزینهٔ بالاتر)
            استفاده می‌شود تا ارزان‌ترین ترکیب معقول انتخاب شود.

    Returns:
        Dict: نتیجه بهینه‌سازی

    Raises:
        ValueError: اگر روش نامعتبر باشد
    """
    logger.info(f"🔄 Starting optimization with method: {method}")

    # 🆕 اولویت با «کم‌تعداد کود» - این حالت جایگزین روش انتخابی می‌شود
    # چون هدف آن مستقیماً کاهش تعداد است، نه فقط کمینه‌کردن خطا
    if prefer_fewer_fertilizers:
        return optimize_sparse_nnls(
            A, b, costs=costs, max_fertilizers=max_fertilizers_count
        )

    # 🆕 اولویت با «ارزان‌ترین ترکیب» - از روش هزینه‌محور با ضریب هزینهٔ
    # بالاتر از حالت پیش‌فرض استفاده می‌شود تا واقعاً به‌سمت ارزان‌ترین
    # جواب معقول متمایل شود (نه فقط یک تعدیل جزئی).
    if prefer_cheapest and costs is not None:
        boosted_cost_weight = max(cost_weight, 0.15)
        return optimize_with_cost(A, b, costs, boosted_cost_weight, max_iterations, tolerance)

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


