# backend/app/crud/__init__.py
"""
ماژول CRUD - عملیات پایه دیتابیس برای همه مدل‌ها
همه توابع از اینجا export می‌شوند تا فایل‌های دیگر نیازی به تغییر نداشته باشند
"""

# ============================================================
# Export از user.py
# ============================================================
from .user import (
    create_user,
    get_user_by_id,
    get_user_by_phone,
    get_users,
    update_user,
    delete_user,
)

# ============================================================
# Export از report.py
# ============================================================
from .report import (
    create_report,
    get_report_by_id,
    get_reports_by_user,
    update_report,
    delete_report,
)

# ============================================================
# Export از fertilizer.py
# ============================================================
from .fertilizer import (
    create_fertilizer,
    get_fertilizer_by_id,
    get_fertilizers_by_user,
    get_system_fertilizers,
    get_all_fertilizers_for_user,
    update_fertilizer,
    delete_fertilizer,
    copy_system_fertilizer_to_user,
    copy_all_system_fertilizers_to_user,
)

# ============================================================
# Export از water_analysis.py
# ============================================================
from .water_analysis import (
    create_water_analysis,
    get_water_analysis_by_report,
    update_water_analysis,
    delete_water_analysis,
)

# ============================================================
# Export از calculation.py
# ============================================================
from .calculation import (
    create_calculation,
    get_calculation_by_report,
    update_calculation,
    delete_calculation,
)

# ============================================================
# Export از recipe.py
# ============================================================
from .recipe import (
    create_recipe,
    get_recipe_by_id,
    get_system_recipes,
    get_user_recipes,
    get_all_recipes_for_user,
    update_recipe,
    delete_recipe,
    apply_recipe_to_targets,
)

# ============================================================
# Export از water_template.py
# ============================================================
from .water_template import (
    create_water_template,
    get_water_templates_by_user,
    get_water_template_by_id,
    update_water_template,
    delete_water_template,
)

# ============================================================
# Export از optimization_log.py
# ============================================================
from .optimization_log import (
    save_optimization_log,
    get_optimization_history,
    get_optimization_log_by_id,
    delete_optimization_log,
)

# ============================================================
# Export از base.py
# ============================================================
from .base import (
    safe_json_loads,
    safe_json_dumps,
    process_calculation_data,
)

# ============================================================
# لیست همه موارد Export شده
# ============================================================
__all__ = [
    # User
    'create_user',
    'get_user_by_id',
    'get_user_by_phone',
    'get_users',
    'update_user',
    'delete_user',
    
    # Report
    'create_report',
    'get_report_by_id',
    'get_reports_by_user',
    'update_report',
    'delete_report',
    
    # Fertilizer
    'create_fertilizer',
    'get_fertilizer_by_id',
    'get_fertilizers_by_user',
    'get_system_fertilizers',
    'get_all_fertilizers_for_user',
    'update_fertilizer',
    'delete_fertilizer',
    'copy_system_fertilizer_to_user',
    'copy_all_system_fertilizers_to_user',
    
    # Water Analysis
    'create_water_analysis',
    'get_water_analysis_by_report',
    'update_water_analysis',
    'delete_water_analysis',
    
    # Calculation
    'create_calculation',
    'get_calculation_by_report',
    'update_calculation',
    'delete_calculation',
    
    # Recipe
    'create_recipe',
    'get_recipe_by_id',
    'get_system_recipes',
    'get_user_recipes',
    'get_all_recipes_for_user',
    'update_recipe',
    'delete_recipe',
    'apply_recipe_to_targets',
    
    # Water Template
    'create_water_template',
    'get_water_templates_by_user',
    'get_water_template_by_id',
    'update_water_template',
    'delete_water_template',
    
    # Optimization Log
    'save_optimization_log',
    'get_optimization_history',
    'get_optimization_log_by_id',
    'delete_optimization_log',
    
    # Base
    'safe_json_loads',
    'safe_json_dumps',
    'process_calculation_data',
]