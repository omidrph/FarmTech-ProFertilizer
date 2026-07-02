"""
توزیع مواد در مخازن A, B, C
============================

این فایل شامل توابع توزیع کودها در مخازن مختلف بر اساس سازگاری شیمیایی است.
"""

from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

# ============================================================
# قوانین توزیع مخازن
# ============================================================
RESERVOIR_RULES = {
    'A': {
        'name': 'مخزن کلسیم',
        'description': 'کودهای حاوی کلسیم و مواد قلیایی',
        'elements': ['Ca'],
        'forbidden_elements': ['P', 'S'],  # فسفات و سولفات با کلسیم رسوب می‌دهند
        'types': ['calcium', 'alkaline']
    },
    'B': {
        'name': 'مخزن اصلی',
        'description': 'سایر کودها (پتاسیم، منیزیم، نیترات، فسفات، سولفات)',
        'elements': ['K', 'Mg', 'N-NO3', 'P', 'S', 'N-NH4', 'Na', 'Cl'],
        'forbidden_elements': [],
        'types': ['potassium', 'magnesium', 'nitrate', 'phosphate', 'sulfate']
    },
    'C': {
        'name': 'مخزن اسید',
        'description': 'اسیدها و مواد اسیدی (تنظیم pH)',
        'elements': [],
        'forbidden_elements': [],
        'types': ['acid']
    }
}


def calculate_reservoir_data(
    fertilizers: List[Dict[str, Any]],
    weights: Dict[str, float]
) -> Dict[str, List[Dict[str, Any]]]:
    """
    محاسبه توزیع مواد در مخازن A, B, C
    
    قوانین توزیع:
    - مخزن A: کودهای کلسیمی (Ca)
    - مخزن B: سایر کودها (پتاسیم، منیزیم، فسفات، نیترات، سولفات)
    - مخزن C: اسیدها (H3PO4, HNO3, H2SO4)
    
    Args:
        fertilizers: لیست کودها با مشخصات کامل
        weights: دیکشنری وزن‌های بهینه {fertilizer_id: weight}
    
    Returns:
        Dict: توزیع مواد در سه مخزن
    
    مثال:
        >>> fertilizers = [
        ...     {'id': '1', 'name': 'Calcium Nitrate', 'elements': {'Ca': 19, 'N-NO3': 15}},
        ...     {'id': '2', 'name': 'Potassium Nitrate', 'elements': {'K': 38, 'N-NO3': 13}}
        ... ]
        >>> weights = {'1': 10.5, '2': 5.2}
        >>> reservoir = calculate_reservoir_data(fertilizers, weights)
        >>> print(reservoir['A'][0]['name'])
        'Calcium Nitrate'
    """
    reservoir_a = []
    reservoir_b = []
    reservoir_c = []
    
    for fert in fertilizers:
        fert_id = str(fert.get('id', ''))
        weight = weights.get(fert_id, 0)
        
        if weight <= 0:
            continue
        
        name = fert.get('name', 'نامشخص')
        is_acid = fert.get('is_acid', False)
        elements = fert.get('elements', {})
        
        # ===== مخزن C: اسیدها =====
        if is_acid:
            reservoir_c.append({
                'name': name,
                'amount': round(weight, 3),
                'fertilizer_id': fert_id,
                'is_acid': True
            })
            continue
        
        # ===== مخزن A: کودهای کلسیمی =====
        if 'Ca' in elements and elements.get('Ca', 0) > 0:
            reservoir_a.append({
                'name': name,
                'amount': round(weight, 3),
                'fertilizer_id': fert_id,
                'has_calcium': True
            })
            continue
        
        # ===== مخزن B: بقیه کودها =====
        reservoir_b.append({
            'name': name,
            'amount': round(weight, 3),
            'fertilizer_id': fert_id,
            'has_calcium': False,
            'is_acid': False
        })
    
    # مرتب‌سازی بر اساس نام برای خوانایی بهتر
    reservoir_a.sort(key=lambda x: x['name'])
    reservoir_b.sort(key=lambda x: x['name'])
    reservoir_c.sort(key=lambda x: x['name'])
    
    result = {
        'A': reservoir_a,
        'B': reservoir_b,
        'C': reservoir_c
    }
    
    logger.info(f"🗄️ Reservoir distribution:")
    logger.info(f"   A: {len(reservoir_a)} items")
    logger.info(f"   B: {len(reservoir_b)} items")
    logger.info(f"   C: {len(reservoir_c)} items")
    
    return result


def get_reservoir_summary(
    reservoir_data: Dict[str, List[Dict[str, Any]]]
) -> Dict[str, Any]:
    """
    دریافت خلاصه توزیع مخازن
    
    Args:
        reservoir_data: داده‌های توزیع مخازن
    
    Returns:
        Dict: خلاصه شامل تعداد و وزن کل هر مخزن
    """
    summary = {}
    
    for reservoir, items in reservoir_data.items():
        total_weight = sum(item.get('amount', 0) for item in items)
        summary[reservoir] = {
            'count': len(items),
            'total_weight': total_weight,
            'items': items
        }
    
    # وزن کل
    total_all = sum(summary[r]['total_weight'] for r in ['A', 'B', 'C'])
    summary['total'] = total_all
    
    return summary