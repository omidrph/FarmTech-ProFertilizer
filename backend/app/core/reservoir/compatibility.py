"""
بررسی سازگاری شیمیایی در مخازن
===============================

این فایل شامل توابع بررسی سازگاری شیمیایی مواد در مخازن است.
"""

from typing import Dict, List, Any, Optional, Tuple
from .distributor import RESERVOIR_RULES


def check_reservoir_compatibility(
    reservoir_data: Dict[str, List[Dict[str, Any]]],
    fertilizers: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    بررسی سازگاری شیمیایی مواد در هر مخزن
    
    قوانین:
    - مخزن A: نباید حاوی فسفات یا سولفات باشد (رسوب با کلسیم)
    - مخزن B: نباید حاوی کلسیم باشد (با فسفات و سولفات رسوب می‌دهد)
    - مخزن C: فقط اسیدها
    
    Args:
        reservoir_data: داده‌های توزیع مخازن
        fertilizers: لیست کامل کودها
    
    Returns:
        Dict: شامل وضعیت سازگاری و هشدارها
    """
    warnings = []
    issues = []
    is_compatible = True
    
    # دریافت قوانین
    rules = RESERVOIR_RULES
    
    # بررسی مخزن A
    for item in reservoir_data.get('A', []):
        fert_id = item.get('fertilizer_id')
        fert = next((f for f in fertilizers if str(f.get('id', '')) == fert_id), None)
        if fert:
            elements = fert.get('elements', {})
            # بررسی عناصر ممنوع در مخزن A
            for forbidden in rules['A']['forbidden_elements']:
                if elements.get(forbidden, 0) > 0:
                    is_compatible = False
                    issues.append({
                        'reservoir': 'A',
                        'fertilizer': item['name'],
                        'issue': f'حاوی {forbidden} است که با کلسیم رسوب می‌دهد',
                        'suggestion': f'کود {item["name"]} را به مخزن B منتقل کنید'
                    })
                    warnings.append(f'کود {item["name"]} حاوی {forbidden} است و باید به مخزن B منتقل شود')
    
    # بررسی مخزن B
    for item in reservoir_data.get('B', []):
        fert_id = item.get('fertilizer_id')
        fert = next((f for f in fertilizers if str(f.get('id', '')) == fert_id), None)
        if fert:
            elements = fert.get('elements', {})
            # بررسی وجود کلسیم در مخزن B
            if elements.get('Ca', 0) > 0:
                # این مورد معمولاً نباید اتفاق بیفتد چون کلسیم‌ها به مخزن A می‌روند
                is_compatible = False
                issues.append({
                    'reservoir': 'B',
                    'fertilizer': item['name'],
                    'issue': 'کلسیم در مخزن B قرار دارد',
                    'suggestion': f'کود {item["name"]} را به مخزن A منتقل کنید'
                })
                warnings.append(f'کود {item["name"]} حاوی کلسیم است و باید به مخزن A منتقل شود')
    
    # بررسی مخزن C
    for item in reservoir_data.get('C', []):
        if not item.get('is_acid', False):
            is_compatible = False
            issues.append({
                'reservoir': 'C',
                'fertilizer': item['name'],
                'issue': 'مخزن C فقط برای اسیدها است',
                'suggestion': f'کود {item["name"]} را به مخزن B منتقل کنید'
            })
            warnings.append(f'کود {item["name"]} اسید نیست و نباید در مخزن C باشد')
    
    return {
        'is_compatible': is_compatible,
        'has_issues': len(issues) > 0,
        'has_warnings': len(warnings) > 0,
        'issues': issues,
        'warnings': warnings,
        'suggestions': [issue['suggestion'] for issue in issues]
    }


def get_compatibility_warnings(
    reservoir_data: Dict[str, List[Dict[str, Any]]],
    fertilizers: List[Dict[str, Any]]
) -> List[str]:
    """
    دریافت هشدارهای سازگاری به صورت لیست ساده
    
    Args:
        reservoir_data: داده‌های توزیع مخازن
        fertilizers: لیست کامل کودها
    
    Returns:
        List[str]: لیست هشدارها
    """
    result = check_reservoir_compatibility(reservoir_data, fertilizers)
    return result.get('warnings', [])


def get_reservoir_recommendation(
    reservoir_data: Dict[str, List[Dict[str, Any]]],
    fertilizers: List[Dict[str, Any]]
) -> str:
    """
    دریافت توصیه کلی برای بهبود توزیع مخازن
    
    Args:
        reservoir_data: داده‌های توزیع مخازن
        fertilizers: لیست کامل کودها
    
    Returns:
        str: توصیه کلی
    """
    result = check_reservoir_compatibility(reservoir_data, fertilizers)
    
    if result['is_compatible']:
        return "✅ توزیع مخازن از نظر شیمیایی سازگار است"
    
    suggestions = result.get('suggestions', [])
    if suggestions:
        return "⚠️ " + " | ".join(suggestions[:3])
    
    return "⚠️ برخی مشکلات در توزیع مخازن وجود دارد. لطفاً بررسی کنید."