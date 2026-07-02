"""
ساخت ماتریس ضرایب برای بهینه‌سازی
================================

این فایل شامل توابع ساخت ماتریس ضرایب و بردار هدف برای الگوریتم NNLS است.
"""

import json
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
import logging

from ..ion_balance import ALL_ELEMENTS

logger = logging.getLogger(__name__)


def prepare_fertilizer_data(fertilizers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    آماده‌سازی داده‌های کودها برای ساخت ماتریس
    
    Args:
        fertilizers: لیست کودها با عناصر و مشخصات
    
    Returns:
        List[Dict]: لیست کودهای آماده شده با ساختار یکسان
    
    مثال:
        >>> fertilizers = [
        ...     {'id': '1', 'name': 'KNO3', 'elements': {'K': 38, 'N-NO3': 13}, 'price_per_kg': 750000}
        ... ]
        >>> prepared = prepare_fertilizer_data(fertilizers)
        >>> print(prepared[0]['name'])
        'KNO3'
    """
    prepared = []
    
    for fert in fertilizers:
        # استخراج عناصر
        elements = fert.get('elements', {})
        if isinstance(elements, str):
            try:
                elements = json.loads(elements)
            except json.JSONDecodeError:
                elements = {}
        
        # محاسبه خلوص
        purity = fert.get('purity', 100)
        if purity is None:
            purity = 100
        purity_factor = purity / 100
        
        # آماده‌سازی ساختار یکسان
        prepared_fert = {
            'id': str(fert.get('id', '')),
            'name': fert.get('name', 'نامشخص'),
            'elements': elements,
            'price_per_kg': fert.get('price_per_kg', 0),
            'purity': purity,
            'purity_factor': purity_factor,
            'is_acid': fert.get('is_acid', False),
            'is_system_default': fert.get('is_system_default', False),
            'fixed_weight': fert.get('fixed_weight', None)
        }
        
        prepared.append(prepared_fert)
    
    return prepared


def build_optimization_matrix(
    target_values: Dict[str, float],
    fertilizers: List[Dict[str, Any]],
    water_values: Optional[Dict[str, float]] = None
) -> Tuple[np.ndarray, np.ndarray, List[str], List[str], Dict[str, int]]:
    """
    ساخت ماتریس ضرایب برای بهینه‌سازی
    
    این تابع ماتریس A (ضرایب) و بردار b (اهداف) را برای الگوریتم NNLS می‌سازد.
    
    Args:
        target_values: عناصر هدف (ppm)
        fertilizers: لیست کودها با عناصر و قیمت
        water_values: عناصر موجود در آب (اختیاری)
    
    Returns:
        Tuple شامل:
            - np.ndarray: ماتریس A (m × n)
            - np.ndarray: بردار b (m)
            - List[str]: لیست عناصر فعال
            - List[str]: لیست اسامی کودها
            - Dict: اطلاعات آماری
    
    Raises:
        ValueError: اگر هیچ عنصر هدفی تعریف نشده باشد
        ValueError: اگر هیچ کودی انتخاب نشده باشد
    
    مثال:
        >>> target = {'K': 250, 'N-NO3': 200}
        >>> ferts = [{'id': '1', 'name': 'KNO3', 'elements': {'K': 38, 'N-NO3': 13}, 'price_per_kg': 750000}]
        >>> A, b, elements, names, stats = build_optimization_matrix(target, ferts)
        >>> print(A.shape)
        (2, 1)
    """
    water_values = water_values or {}
    
    # فیلتر کردن عناصر با هدف مثبت
    active_elements = [el for el in ALL_ELEMENTS if target_values.get(el, 0) > 0]
    
    if not active_elements:
        raise ValueError("هیچ عنصر هدفی تعریف نشده است")
    
    # آماده‌سازی کودها
    prepared_fertilizers = prepare_fertilizer_data(fertilizers)
    
    if not prepared_fertilizers:
        raise ValueError("هیچ کودی انتخاب نشده است")
    
    # ساخت ماتریس A و بردار b
    A = []
    b = []
    fertilizer_names = []
    element_index = {}
    
    for i, element in enumerate(active_elements):
        target = target_values.get(element, 0)
        water = water_values.get(element, 0)
        b.append(max(0, target - water))  # کسر کیفیت آب
        element_index[element] = i
        
        row = []
        for fert in prepared_fertilizers:
            # محاسبه سهم عنصر از کود (با در نظر گرفتن خلوص)
            element_pct = fert['elements'].get(element, 0)
            contribution = (element_pct / 100) * fert['purity_factor']
            row.append(contribution)
        A.append(row)
    
    # جمع‌آوری اسامی کودها
    fertilizer_names = [fert.get('name', f'کود {i}') for i, fert in enumerate(prepared_fertilizers)]
    
    # اطلاعات آماری
    stats = {
        'num_elements': len(active_elements),
        'num_fertilizers': len(prepared_fertilizers),
        'element_names': active_elements,
        'fertilizer_names': fertilizer_names,
        'has_water_values': len(water_values) > 0
    }
    
    logger.info(f"📊 ماتریس ساخته شد: {len(active_elements)} عنصر × {len(prepared_fertilizers)} کود")
    
    return np.array(A), np.array(b), active_elements, fertilizer_names, stats


def apply_element_weights(
    A: np.ndarray,
    b: np.ndarray,
    element_weights: Dict[str, float],
    active_elements: List[str]
) -> Tuple[np.ndarray, np.ndarray]:
    """
    اعمال وزن‌دهی به عناصر در ماتریس
    
    Args:
        A: ماتریس ضرایب
        b: بردار هدف
        element_weights: وزن هر عنصر
        active_elements: لیست عناصر فعال
    
    Returns:
        Tuple: (ماتریس وزن‌دهی شده, بردار وزن‌دهی شده)
    """
    weight_matrix = np.diag([element_weights.get(el, 1.0) for el in active_elements])
    A_weighted = np.dot(weight_matrix, A)
    b_weighted = np.dot(weight_matrix, b)
    
    return A_weighted, b_weighted


def apply_fixed_weights_constraints(
    fertilizers: List[Dict[str, Any]]
) -> Dict[str, float]:
    """
    اعمال محدودیت‌های وزن ثابت برای کودها
    
    Args:
        fertilizers: لیست کودها
    
    Returns:
        Dict: دیکشنری {fertilizer_id: fixed_weight}
    """
    fixed_weights = {}
    for fert in fertilizers:
        fixed_weight = fert.get('fixed_weight')
        if fixed_weight is not None and fixed_weight > 0:
            fixed_weights[str(fert.get('id', ''))] = fixed_weight
    
    return fixed_weights