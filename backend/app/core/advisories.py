# backend/app/core/advisories.py
"""
📋 مرجع واحد هشدارها و نکته‌ها (Advisories)
============================================================
قبلاً هشدارها از چند مسیر موازی و با قالب‌های مختلف تولید می‌شدند (رشته‌های warnings، پیام‌های
انتخاب دستی، تداخل‌های تغذیه‌ای، هشدارهای ساختاریافتهٔ رسوب، EC گیاه) و در صفحهٔ خانه با هم قاطی
و تکراری می‌شدند (مثلاً «خطر رسوب» برای یک پیام کلی انتخاب کود).

اکنون همهٔ آن‌ها در «یک فهرست استاندارد» جمع می‌شوند و فرانت‌اند فقط همین فهرست را نمایش می‌دهد:

    {id, severity: danger|warn|info, category, title, detail, solution, scope, tank, elements}

قواعد:
  • هر مسئله فقط یک‌بار می‌آید (id یکتا)؛ مورد دقیق‌تر بر مورد کلی‌تر برتری دارد
    (مثلاً «گچ در استوک مخزن B» جای پیام کلی «کلسیم + سولفات انتخاب شده‌اند» را می‌گیرد).
  • پیام‌هایی که در بخش‌های دیگر صفحه نمایش داده می‌شوند (درصد تحقق عناصر، تعادل یونی، همگرایی…) حذف می‌شوند.
  • عنوان کوتاه و جدا از توضیح و راه‌حل است؛ هیچ پیام چندخطی/ستاره‌دار داخل عنوان نمی‌رود.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from app.core.reservoir.compatibility import NUTRIENT_INTERACTION_RULES

_SEV = {"danger": 0, "warn": 1, "info": 2}

# پیام‌هایی که جای دیگری از صفحه نشان داده می‌شوند یا کلی و بی‌اثرند
_COVERED = [
    r"^عنصر .+:\s*(تنها\s*)?\d+\s*%", r"^تعادل یونی برقرار نیست", r"^الگوریتم به جواب کامل نرسید",
    r"^\d+ کود در ترکیب نهایی استفاده نشدند", r"^خطای باقی‌مانده بالا است", r"^\d+ عنصر با مقدار صفر",
    r"^\d+ عنصر در داده‌ها وجود ندارد", r"^فقط (کاتیون|آنیون) وجود دارد", r"^هیچ کاتیون یا آنیونی",
    # رسوب: از هشدارهای ساختاریافتهٔ رسوب می‌آید
    r"^خطر رسوب\s*[:：]", r"^\d+ خطر رسوب شناسایی شده است", r"^رسوب .+ ممکن است تشکیل شود",
]
_GENERIC = [
    r"^افزایش .+ با استفاده از کود مناسب$", r"^کاهش .+ یا استفاده از کود با درصد کمتر$", r"^لطفاً ",
    r"^دوباره بهینه", r"^تعداد تکرارها", r"^کودهای بیشتری", r"^عناصر هدف را با کودهای موجود", r"^قیمت کودها را بررسی کنید$",
]

# عنوان و راه‌حل هر قانون تداخل تغذیه‌ای (شناسه‌ها از NUTRIENT_INTERACTION_RULES)
_RULE_META: Dict[str, Dict[str, Any]] = {
    "fe_p_lockout": {"title": "آهن و فسفر هم‌زمان بالا هستند", "sev": "warn", "els": ["Fe", "P"],
                     "solution": "از آهن کلاته (EDTA/DTPA/EDDHA) استفاده کنید و تزریق آهن را از فسفر جدا کنید."},
    "high_ph_micronutrient_lockout": {"title": "pH بالا؛ جذب ریزمغذی‌ها کم می‌شود", "sev": "warn", "els": ["Fe", "Mn", "Zn", "Cu"],
                                     "solution": "pH را با اسید پایین بیاورید (تب PH) یا از آهن کلاتهٔ مقاوم به pH بالا استفاده کنید."},
    "excess_chloride": {"title": "کلر بالاتر از حد معمول", "sev": "warn", "els": ["Cl"],
                        "solution": "کودهای کلریدی (مثل KCl) را کم یا با فرم سولفاتی/نیتراتی جایگزین کنید."},
    "excess_sodium": {"title": "سدیم بالاتر از حد معمول", "sev": "warn", "els": ["Na"],
                      "solution": "منبع سدیم (آب یا کود) را بررسی کنید؛ در صورت امکان آب با سدیم کمتر به‌کار ببرید."},
    "boron_toxicity": {"title": "بور نزدیک به حد سمیت", "sev": "warn", "els": ["B"],
                       "solution": "مقدار کود بور را کم کنید و دوز را با دقت تنظیم کنید."},
    "excess_ammonium": {"title": "سهم آمونیوم از نیتروژن بالا است", "sev": "warn", "els": ["N-NH4"],
                        "solution": "سهم نیتروژن نیتراتی را بیشتر کنید (مثلاً نیترات کلسیم/پتاسیم به‌جای سولفات آمونیوم)."},
    "low_calcium_high_potassium": {"title": "نسبت K به Ca بالا است", "sev": "warn", "els": ["K", "Ca"],
                                   "solution": "کلسیم را بیشتر یا پتاسیم را کمتر کنید تا نسبت متعادل شود."},
}


def _clean(text: Any) -> str:
    t = str(text or "")
    t = re.sub(r"^[^\w\u0600-\u06FF]+", "", t)               # شکلک/ستاره/نقطهٔ ابتدای پیام
    t = re.sub(r"\s*\n\s*[*•\-]\s*", " ", t)                 # بولت‌های چندخطی
    return re.sub(r"\s+", " ", t).strip()


def _adv(aid: str, severity: str, category: str, title: str, detail: str = "", solution: str = "",
         scope: Optional[str] = None, tank: Optional[str] = None, elements: Optional[List[str]] = None) -> Dict[str, Any]:
    return {"id": aid, "severity": severity, "category": category, "title": title, "detail": detail[:420],
            "solution": solution, "scope": scope, "tank": tank, "elements": elements or []}


def _matches(patterns: List[str], text: str) -> bool:
    return any(re.search(p, text) for p in patterns)


def build_advisories(
    concentrations: Dict[str, float],
    ph: Optional[float],
    fertilizers: List[Dict[str, Any]],
    precipitation_alerts: Optional[List[Dict[str, Any]]],
    legacy_warnings: Optional[List[str]],
) -> List[Dict[str, Any]]:
    """فهرست یکپارچه و بدون تکرار هشدارها؛ هرگز استثنا پرتاب نمی‌کند."""
    try:
        return _build(concentrations or {}, ph, fertilizers or [], precipitation_alerts or [], legacy_warnings or [])
    except Exception:  # pragma: no cover - حفاظتی
        return []


def _build(conc, ph, fertilizers, p_alerts, legacy) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []

    # ۱) رسوب (مرجع: هشدارهای ساختاریافتهٔ رسوب)
    for a in p_alerts:
        out.append(_adv(a["id"], a.get("severity", "warn"), "precipitation", a["title"], a.get("detail", ""),
                        a.get("solution", ""), a.get("scope"), a.get("tank"), a.get("elements")))
    precip_pairs = {frozenset(a.get("elements") or []) for a in p_alerts if a.get("scope") == "stock"}

    # ۲) تداخل‌های تغذیه‌ای روی غلظت نهایی
    for rule in NUTRIENT_INTERACTION_RULES:
        meta = _RULE_META.get(rule["id"])
        if not meta:
            continue
        try:
            if rule["id"] == "high_ph_micronutrient_lockout":
                hit, msg = rule["check"](conc, ph), (rule["message"](conc, ph) if rule["check"](conc, ph) else "")
            else:
                hit, msg = rule["check"](conc), (rule["message"](conc) if rule["check"](conc) else "")
        except Exception:
            continue
        if hit:
            out.append(_adv(f"nutrient-{rule['id']}", meta["sev"], "nutrient", meta["title"], _clean(msg), meta["solution"],
                            "final", None, meta["els"]))

    # ۳) احتیاط‌های انتخاب کود (کلی)؛ اگر هشدار دقیق استوک برای همان جفت وجود دارد، لازم نیست
    def has(el: str) -> bool:
        return any((f.get("elements") or {}).get(el, 0) > 0 for f in fertilizers)
    if has("Ca") and has("S") and frozenset(["Ca", "S"]) not in precip_pairs:
        out.append(_adv("selection-ca-so4", "info", "selection", "کلسیم و سولفات هر دو در کودهای انتخابی هستند",
                        "این دو در سطل غلیظ رسوب گچ می‌دهند. سیستم آن‌ها را در سطل‌های جدا قرار می‌دهد.",
                        "هرگز این دو گروه را مستقیم در یک سطل حل نکنید.", "stock", None, ["Ca", "S"]))
    if has("Ca") and has("P") and frozenset(["Ca", "P"]) not in precip_pairs:
        out.append(_adv("selection-ca-po4", "info", "selection", "کلسیم و فسفات هر دو در کودهای انتخابی هستند",
                        "این دو در حالت غلیظ رسوب فسفات کلسیم می‌دهند. سیستم آن‌ها را در سطل‌های جدا قرار می‌دهد.",
                        "هرگز این دو گروه را مستقیم با هم مخلوط نکنید.", "stock", None, ["Ca", "P"]))
    acids = sum(1 for f in fertilizers if f.get("is_acid"))
    if acids > 1 and not any(a["id"] == "stock-multi-acid" for a in out):
        out.append(_adv("selection-multi-acid", "warn", "selection", f"{acids} نوع اسید انتخاب شده است",
                        "مخلوط‌کردن مستقیم اسیدهای مختلف می‌تواند واکنش گرمازا و خطرناک ایجاد کند.",
                        "هر اسید را جداگانه و با احتیاط («اسید را به آب») رقیق کنید.", "stock", "C", []))

    # ۴) بقیهٔ پیام‌های قدیمی (EC گیاه، آمونیوم pH و...) بعد از حذف تکراری/کلی/پوشش‌داده‌شده
    known_texts = ("در میان کودهای انتخابی", "شما ", "آهن (", "pH تخمینی بالا", "کلر (", "سدیم (", "بور (", "سهم نیتروژن آمونیومی", "نسبت پتاسیم به کلسیم")
    for w in legacy:
        t = _clean(w)
        if len(t) < 4 or _matches(_COVERED, t) or _matches(_GENERIC, t):
            continue
        if any(t.startswith(k) for k in known_texts) or "کودهای انتخابی" in t:
            continue                                     # همین موارد بالا ساختاریافته تولید شده‌اند
        if "EC محاسبه‌شده" in t:
            out.append(_adv("plant-ec", "warn", "plant_ec", "EC با نیاز گیاه همخوان نیست", t,
                            "غلظت کل کود را تغییر دهید یا EC هدف را با منبع تخصصی گیاه مقایسه کنید.", "final"))
            continue
        aid = "note-" + re.sub(r"\W+", "-", t)[:40]
        out.append(_adv(aid, "danger" if re.search(r"خطر|مسمومیت|سمیت", t) else "info", "general",
                        "نکته", t, "", None))

    # حذف تکراری (اولین = دقیق‌ترین/شدیدترین) و مرتب‌سازی
    out.sort(key=lambda a: _SEV.get(a["severity"], 9))
    seen, uniq = set(), []
    for a in out:
        if a["id"] in seen:
            continue
        seen.add(a["id"])
        uniq.append(a)
    return uniq
