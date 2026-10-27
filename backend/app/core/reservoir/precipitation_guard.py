# backend/app/core/reservoir/precipitation_guard.py
"""
سیستم هشدار ترکیبات رسوب‌زا (P0)
============================================================
سه لایهٔ بررسی، با خروجی ساختاریافته (شدت، محل، علت، راه‌حل):

۱) داخل «استوک» (غلظت‌شده): هر مخزن A/B/C با غلظت واقعی استوک بررسی می‌شود؛
   خطرناک‌ترین رسوب‌ها (گچ، فسفات کلسیم، فسفات منیزیم/آهن) اینجا رخ می‌دهد.
۲) «محلول نهایی» (رقیق): با ثابت‌های حلالیت و pH واقعی.
۳) «آب منبع»: قلیائیت/بی‌کربنات بالا + کلسیم، و pH بالا + فسفر.

هر هشدار: {id, severity: danger|warn|info, scope: stock|final|water, tank,
          title, detail, solution, elements}
هیچ خطایی در این ماژول نباید محاسبهٔ اصلی را بشکند.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from app.core.ion_balance.constants import MOLECULAR_WEIGHTS
from app.core.ion_balance.validators import check_precipitation

logger = logging.getLogger(__name__)

# حلالیت تقریبی گچ در آب (mol/L)؛ در استوک غلظت‌های شیمیایی بالاتر از رقیق رخ می‌دهد
_CASO4_STOCK_LIMIT_MOLAR2 = 6e-3  # حاصل‌ضرب [Ca][SO4] در استوک (تقریب عملی با اثر قدرت یونی)
_SEVERITY_ORDER = {"danger": 0, "warn": 1, "info": 2}


def _mol_per_l(ppm: float, element: str) -> float:
    mw = MOLECULAR_WEIGHTS.get(element, 0) or 0
    return ppm / (mw * 1000.0) if mw else 0.0


def _alert(aid: str, severity: str, scope: str, title: str, detail: str, solution: str,
           elements: Optional[List[str]] = None, tank: Optional[str] = None) -> Dict[str, Any]:
    return {
        "id": aid, "severity": severity, "scope": scope, "tank": tank,
        "title": title, "detail": detail, "solution": solution, "elements": elements or [],
    }


def _is_chelated_fe(f: Dict[str, Any]) -> bool:
    name = (f.get("name") or "").lower()
    return (f.get("elements", {}) or {}).get("Fe", 0) > 0 and any(
        k in name for k in ("کلات", "edta", "dtpa", "eddha", "chelate")
    )


def _tank_elements(
    items: List[Dict[str, Any]], fert_by_id: Dict[str, Dict[str, Any]], stock_liters: float
) -> Dict[str, float]:
    """غلظت (ppm) عناصر در استوک یک مخزن؛ items.amount = گرم کود برای کل حجم مخزن اصلی."""
    out: Dict[str, float] = {}
    if not stock_liters or stock_liters <= 0:
        return out
    for it in items:
        f = fert_by_id.get(str(it.get("fertilizer_id")))
        if not f:
            continue
        grams = float(it.get("amount") or 0)
        pf = (f.get("purity") if f.get("purity") is not None else 100) / 100.0
        for el, pct in (f.get("elements") or {}).items():
            if pct and pct > 0:
                out[el] = out.get(el, 0.0) + grams * (pct / 100.0) * pf * 1000.0 / stock_liters
    return out


def build_precipitation_alerts(
    concentrations: Dict[str, float],
    reservoir_data: Optional[Dict[str, List[Dict[str, Any]]]],
    fertilizers: List[Dict[str, Any]],
    stock_liters: Optional[float],
    water_values: Optional[Dict[str, float]] = None,
    ph: Optional[float] = None,
) -> List[Dict[str, Any]]:
    try:
        return _build(concentrations, reservoir_data or {}, fertilizers, stock_liters, water_values or {}, ph)
    except Exception as e:  # pragma: no cover - حفاظتی
        logger.warning(f"precipitation guard failed: {e}")
        return []


def _build(conc, reservoir, fertilizers, stock_liters, water, ph) -> List[Dict[str, Any]]:
    alerts: List[Dict[str, Any]] = []
    fert_by_id = {str(f.get("id")): f for f in fertilizers}
    ph_used = ph if ph else (water.get("pH") or 6.0)

    # ---------- ۱) داخل استوک ----------
    for tank, items in reservoir.items():
        if tank not in ("A", "B", "C") or not items:
            continue
        el = _tank_elements(items, fert_by_id, stock_liters or 0)
        ca, so4 = _mol_per_l(el.get("Ca", 0), "Ca"), _mol_per_l(el.get("S", 0), "S")
        p = _mol_per_l(el.get("P", 0), "P")
        mg, fe = _mol_per_l(el.get("Mg", 0), "Mg"), _mol_per_l(el.get("Fe", 0), "Fe")

        if ca > 0 and so4 > 0:
            prod = ca * so4
            sev = "danger" if prod > _CASO4_STOCK_LIMIT_MOLAR2 else "warn"
            if prod > _CASO4_STOCK_LIMIT_MOLAR2 * 0.25:
                alerts.append(_alert(
                    f"stock-gypsum-{tank}", sev, "stock",
                    f"گچ (CaSO₄) در استوک مخزن {tank}",
                    "کلسیم و سولفات در یک استوک غلیظ‌اند و رسوب سفید گچ تشکیل می‌شود که با هم‌زدن حل نمی‌شود.",
                    "کودهای سولفاتی (یا اسید سولفوریک) را به مخزن B ببرید و کلسیم را تنها در مخزن A نگه دارید.",
                    ["Ca", "S"], tank))
        if ca > 0 and p > 0:
            alerts.append(_alert(
                f"stock-capo4-{tank}", "danger", "stock",
                f"فسفات کلسیم در استوک مخزن {tank}",
                "فسفر و کلسیم در یک استوک رسوب سفید و غیرقابل‌برگشت می‌دهند و فسفر قابل‌جذب را از دست می‌دهید.",
                "منبع فسفر را در مخزن جدا (B) یا مخزن اسید قرار دهید؛ هرگز با کلسیم نیترات یکجا نگذارید.",
                ["Ca", "P"], tank))
        if mg > 0 and p > 0 and tank != "C":
            if (mg * p) > 0.03:
                alerts.append(_alert(
                    f"stock-mgpo4-{tank}", "info", "stock",
                    f"فسفات منیزیم در استوک مخزن {tank}",
                    "در استوک‌های غلیظ با pH بالاتر از حدود ۶، فسفات منیزیم کدر و رسوبی می‌شود.",
                    "استوک را با کمی اسید به pH زیر ۵٫۵ برسانید یا غلظت استوک را کم کنید (نسبت تزریق بیشتر).",
                    ["Mg", "P"], tank))
        if fe > 0 and p > 0 and tank != "C":
            members = [fert_by_id.get(str(i.get("fertilizer_id"))) for i in items]
            if any(m and (m.get("elements") or {}).get("Fe", 0) > 0 and not _is_chelated_fe(m) for m in members):
                alerts.append(_alert(
                    f"stock-fepo4-{tank}", "danger", "stock",
                    f"فسفات آهن در استوک مخزن {tank}",
                    "آهن غیرکلاته با فسفات رسوب نامحلول می‌دهد و آهن از دسترس گیاه خارج می‌شود.",
                    "از آهن کلاته (EDTA/DTPA/EDDHA) استفاده کنید یا آهن را در مخزن جدا بدهید.",
                    ["Fe", "P"], tank))
        if tank == "C":
            acid_names = [i.get("name") for i in items]
            if ca > 0:
                alerts.append(_alert(
                    "stock-acid-ca", "danger", "stock", "کلسیم در مخزن اسید",
                    "اسید سولفوریک/فسفریک با کلسیم رسوب می‌دهد.",
                    "کلسیم را از مخزن اسید جدا کنید.", ["Ca"], tank))
            if len(acid_names) > 1:
                alerts.append(_alert(
                    "stock-multi-acid", "info", "stock", "چند اسید در یک مخزن",
                    "مخلوط‌کردن چند اسید غلیظ در یک ظرف گرما و ریسک ایمنی دارد.",
                    "اسیدها را جداگانه و همیشه «اسید را به آب» اضافه کنید.", [], tank))

    # ---------- ۲) محلول نهایی ----------
    has_chelate = any(_is_chelated_fe(f) for f in fertilizers)
    final = check_precipitation(
        conc, ph=ph_used, has_chelated_iron=has_chelate,
        alkalinity_ppm_caco3=water.get("Alkalinity"),
    )
    for r in final.get("risks", []):
        sev = "danger" if r.get("severity") in ("critical", "high") else "warn"
        alerts.append(_alert(
            f"final-{r.get('compound')}", sev, "final",
            f"خطر رسوب {r.get('name') or r.get('compound')} در محلول نهایی",
            r.get("note") or f"حاصل‌ضرب یونی از حد حلالیت ({r.get('compound')}) بیشتر است.",
            r.get("suggestion") or "غلظت را کاهش دهید.",
            [], None))

    ca_m, so4_m = _mol_per_l(conc.get("Ca", 0), "Ca"), _mol_per_l(conc.get("S", 0), "S")
    if ca_m > 0 and so4_m > 0 and not any(a["id"] == "final-CaSO4" for a in alerts):
        ratio = ca_m * so4_m / 2.4e-5
        if ratio > 0.5:
            alerts.append(_alert(
                "final-gypsum-near", "info", "final", "نزدیک اشباع گچ",
                f"حاصل‌ضرب Ca×SO₄ حدود {ratio * 100:.0f}٪ حد حلالیت است؛ در آب سرد یا غلظت بالاتر ممکن است رسوب کند.",
                "سولفات را کم کنید یا کلسیم و سولفات را همزمان با رقیق‌سازی کافی مخلوط کنید.", ["Ca", "S"]))
    if conc.get("Ca", 0) > 150 and conc.get("P", 0) > 50 and ph_used > 6.5:
        alerts.append(_alert(
            "final-brushite", "warn", "final", "ریسک فسفات کلسیم (pH بالا)",
            f"با Ca={conc.get('Ca', 0):.0f} و P={conc.get('P', 0):.0f} ppm در pH {ph_used:.1f}، فسفات کلسیم می‌تواند کدر شود.",
            "pH نهایی را به حدود ۵٫۵ تا ۶ برسانید (تب PH).", ["Ca", "P"]))

    # ---------- ۳) آب منبع ----------
    alk = water.get("Alkalinity") or 0
    if alk > 150 and conc.get("Ca", 0) > 100:
        alerts.append(_alert(
            "water-alk-ca", "warn", "water", "قلیائیت بالای آب + کلسیم",
            f"قلیائیت آب {alk:.0f} ppm CaCO₃ است و با کلسیم رسوب آهک و گرفتگی قطره‌چکان‌ها ایجاد می‌کند.",
            "با اسید قلیائیت را به حدود ۵۰ تا ۸۰ ppm برسانید (تب PH).", ["Ca"]))

    alerts.sort(key=lambda a: (_SEVERITY_ORDER.get(a["severity"], 9), a["scope"]))
    seen, out = set(), []
    for a in alerts:
        if a["id"] in seen:
            continue
        seen.add(a["id"])
        out.append(a)
    return out
