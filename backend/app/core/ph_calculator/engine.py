# backend/app/core/ph_calculator/engine.py
"""
موتور محاسبهٔ «اصلاح pH» (توابع خالص - بدون دیتابیس)
============================================================
دو حالت ورودی داریم که هر دو به یک خروجی یکسان می‌رسند: «مقدار ماده برای کل مخزن».

۱) حالت «دوز مشخص» (رسپی): کاربر می‌داند برای این رسپی چقدر اسید لازم است
   (مثلاً ۸۰۰ میلی‌لیتر برای هر ۱۰۰۰ لیتر) → فقط مقیاس‌دهی به حجم مخزن.

۲) حالت «آزمون و خطا روی نمونه»: کاربر مقداری از محلول ساخته‌شده را (مثلاً ۵ لیتر
   از مخزن ۵۰۰۰ لیتری) برمی‌دارد، مرحله‌به‌مرحله اسید/باز اضافه می‌کند و بعد از
   هر مرحله pH را می‌خواند. وقتی pH به هدف رسید، مقدار مصرفی نمونه با ضریب
   (حجم مخزن ÷ حجم نمونه) به کل مخزن تعمیم داده می‌شود.

هیچ مدل تئوریکی (کربنات و ...) در کار نیست: pH محلول غذایی (فسفات، آمونیوم،
کلات‌ها) با فرمول قابل پیش‌بینی نیست و فقط اندازه‌گیری واقعی قابل‌اتکاست.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional

PH_MIN, PH_MAX = 0.0, 14.0
# اگر هیچ نقطه‌ای دقیقاً به هدف نرسیده باشد، نزدیک‌ترین نقطه تا این فاصله پذیرفته می‌شود
CLOSE_ENOUGH_PH = 0.15
# فاصلهٔ بین دو نقطهٔ متوالی که میان‌یابی روی آن قابل‌اتکا نیست
WIDE_SEGMENT_PH = 0.8
# بیشتر از این ضریب مقیاس، خطای اندازه‌گیری نمونه خیلی تقویت می‌شود
HIGH_SCALE_FACTOR = 2000
LOW_SAMPLE_VOLUME_L = 1.0

# سهم دوز که در مرحلهٔ اول به مخزن اضافه می‌شود (بقیه پس از اختلاط و اندازه‌گیری)
STAGE_FIRST_FRACTION = 0.7


class AdjustmentError(Exception):
    """خطای اعتبارسنجی/محاسبه؛ پیام مستقیماً قابل نمایش به کاربر است."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


@dataclass
class TrialStep:
    amount: float  # مقدار «اضافه‌شده در همین مرحله» (mL یا g)
    ph: float      # pH پس از همین مرحله


@dataclass
class TrialSolution:
    direction: Literal["acid", "base"]
    sample_dose: float          # مقدار تجمعی لازم برای هدف (در نمونه)
    final_ph: float             # pH واقعی/برآورد‌شده در آن مقدار
    method: Literal["interpolated", "measured"]
    curve: List[Dict[str, float]]   # [{amount, ph}] تجمعی، شامل نقطهٔ صفر
    warnings: List[str] = field(default_factory=list)


def direction_of(initial_ph: float, target_ph: float) -> Literal["acid", "base"]:
    return "acid" if target_ph < initial_ph else "base"


def validate_ph(value: float, label: str) -> None:
    if value is None or not (PH_MIN <= value <= PH_MAX):
        raise AdjustmentError(f"{label} باید بین ۰ تا ۱۴ باشد.")


def check_direction(kind: str, initial_ph: float, target_ph: float) -> None:
    """ماده‌ی انتخاب‌شده باید با جهت تغییر pH سازگار باشد."""
    if abs(initial_ph - target_ph) < 1e-9:
        raise AdjustmentError("pH فعلی و pH هدف یکسان‌اند؛ اصلاحی لازم نیست.")
    needed = direction_of(initial_ph, target_ph)
    if needed != kind:
        if needed == "acid":
            raise AdjustmentError("برای کاهش pH باید یک «اسید» انتخاب کنید.")
        raise AdjustmentError("برای افزایش pH باید یک «باز» انتخاب کنید.")


def solve_trial(initial_ph: float, target_ph: float, steps: List[TrialStep]) -> TrialSolution:
    """مقدار تجمعی ماده در نمونه برای رسیدن به pH هدف (میان‌یابی روی منحنی واقعی)."""
    validate_ph(initial_ph, "pH اولیهٔ نمونه")
    validate_ph(target_ph, "pH هدف")
    if not steps:
        raise AdjustmentError("حداقل یک مرحله (مقدار اضافه‌شده و pH پس از آن) وارد کنید.")

    direction = direction_of(initial_ph, target_ph)
    if abs(initial_ph - target_ph) < 1e-9:
        raise AdjustmentError("pH اولیه و pH هدف یکسان‌اند؛ اصلاحی لازم نیست.")

    curve: List[Dict[str, float]] = [{"amount": 0.0, "ph": float(initial_ph)}]
    total = 0.0
    for i, s in enumerate(steps, start=1):
        if not (s.amount and s.amount > 0):
            raise AdjustmentError(f"مقدار اضافه‌شده در مرحلهٔ {i} باید بزرگ‌تر از صفر باشد.")
        validate_ph(s.ph, f"pH مرحلهٔ {i}")
        total += s.amount
        curve.append({"amount": total, "ph": float(s.ph)})

    warnings: List[str] = []

    # جهت حرکت pH باید با جهت مطلوب سازگار باشد
    first_move = curve[1]["ph"] - curve[0]["ph"]
    if (direction == "acid" and first_move > 0) or (direction == "base" and first_move < 0):
        raise AdjustmentError(
            "با افزودن ماده، pH باید به سمت هدف حرکت کند؛ داده‌ها با جهت مورد انتظار سازگار نیستند "
            "(نوع ماده یا pH اولیه را بررسی کنید)."
        )
    for a, b in zip(curve, curve[1:]):
        step = b["ph"] - a["ph"]
        if (direction == "acid" and step > 0.02) or (direction == "base" and step < -0.02):
            warnings.append(
                "در بعضی مراحل pH خلاف جهت انتظار حرکت کرده است؛ هم‌زدن کافی و قرائت‌های دستگاه را بررسی کنید."
            )
            break

    # ۱) اگر هدف بین دو نقطه قرار گرفته: میان‌یابی خطی
    for a, b in zip(curve, curve[1:]):
        lo, hi = sorted((a["ph"], b["ph"]))
        if lo <= target_ph <= hi and a["ph"] != b["ph"]:
            frac = (target_ph - a["ph"]) / (b["ph"] - a["ph"])
            amount = a["amount"] + frac * (b["amount"] - a["amount"])
            exact = abs(b["ph"] - target_ph) < 1e-9 or abs(a["ph"] - target_ph) < 1e-9
            if abs(b["ph"] - a["ph"]) > WIDE_SEGMENT_PH and not exact:
                warnings.append(
                    "فاصلهٔ pH بین دو نقطهٔ اطراف هدف زیاد است؛ برای دقت بیشتر یک نقطهٔ میانی هم اندازه بگیرید."
                )
            return TrialSolution(
                direction=direction, sample_dose=amount, final_ph=float(target_ph),
                method="measured" if exact else "interpolated", curve=curve, warnings=warnings,
            )

    # ۲) هیچ نقطه‌ای هدف را در بر نمی‌گیرد: نزدیک‌ترین نقطهٔ اندازه‌گیری‌شده اگر به اندازهٔ کافی نزدیک باشد
    best = min(curve[1:], key=lambda p: abs(p["ph"] - target_ph))
    gap = abs(best["ph"] - target_ph)
    if gap <= CLOSE_ENOUGH_PH:
        warnings.append(
            f"pH هدف دقیقاً اندازه‌گیری نشد؛ نزدیک‌ترین نقطه ({best['ph']:.2f}) به‌عنوان مبنا استفاده شد."
        )
        return TrialSolution(
            direction=direction, sample_dose=best["amount"], final_ph=best["ph"],
            method="measured", curve=curve, warnings=warnings,
        )

    last = curve[-1]["ph"]
    side = "هنوز بالاتر" if direction == "acid" else "هنوز پایین‌تر"
    raise AdjustmentError(
        f"pH نمونه ({last:.2f}) {side} از هدف ({target_ph:.2f}) است. "
        "ماده را مرحله‌ای ادامه دهید و نقطهٔ بعدی را ثبت کنید تا pH به هدف برسد."
    )


@dataclass
class TankDose:
    amount: float                 # مقدار برای کل مخزن (mL یا g)
    scale_factor: float
    per_1000_l: float             # مقدار به‌ازای هر ۱۰۰۰ لیتر (برای ذخیره در رسپی)
    stage_first: float            # مقدار مرحلهٔ اول (۷۰٪)
    stage_rest: float
    warnings: List[str] = field(default_factory=list)


def scale_to_tank(amount_basis: float, basis_volume_l: float, tank_volume_l: float) -> TankDose:
    if not (amount_basis > 0):
        raise AdjustmentError("مقدار ماده باید بزرگ‌تر از صفر باشد.")
    if not (basis_volume_l > 0):
        raise AdjustmentError("حجم مبنا (نمونه یا رسپی) باید بزرگ‌تر از صفر باشد.")
    if not (tank_volume_l > 0):
        raise AdjustmentError("حجم مخزن باید بزرگ‌تر از صفر باشد.")

    factor = tank_volume_l / basis_volume_l
    amount = amount_basis * factor
    warnings: List[str] = []
    if factor > HIGH_SCALE_FACTOR:
        warnings.append(
            f"ضریب مقیاس‌دهی {factor:,.0f} برابر است؛ خطای کوچک در اندازه‌گیری نمونه در مخزن چند ده برابر می‌شود. "
            "حجم نمونهٔ بزرگ‌تر (مثلاً ۱۰ لیتر) دقت بهتری می‌دهد."
        )
    return TankDose(
        amount=amount,
        scale_factor=factor,
        per_1000_l=amount * 1000.0 / tank_volume_l,
        stage_first=amount * STAGE_FIRST_FRACTION,
        stage_rest=amount * (1 - STAGE_FIRST_FRACTION),
        warnings=warnings,
    )
