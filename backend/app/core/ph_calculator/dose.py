# backend/app/core/ph_calculator/dose.py
"""
محاسبه‌ی دوز اصلاح pH (توابع خالص - پورت‌شده از widgets/ph/phDose.ts)
============================================================
مسیر ۱) مدل تئوریک سیستم کربنات (فقط آب ساده)
مسیر ۲) تیتراسیون واقعی نمونه (روش پیشنهادی برای محلول‌های غذایی/ترکیبی)

اصل مهم (بدون تغییر نسبت به نسخه‌ی قبلی): هیچ جدول عمومیِ
«pH هدف → آلکالینیتی» استفاده نمی‌شود؛ همه‌چیز از ترمودینامیک تعادل
کربنات یا از داده‌ی تیتراسیون واقعیِ خودِ کاربر مشتق می‌شود.

نکته‌ی معماری: این ماژول به دیتابیس یا FastAPI وابسته نیست (تست‌پذیری
بالا). لایه‌ی routes/ph_calculator.py مسئول واکشی داده از دیتابیس
(کود اسیدی انتخاب‌شده) و تبدیل آن به Chemical است.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal, Optional, Union

from .chemistry import (
    alkalinity_from_ct,
    carbonate_constants,
    phosphoric_effective_z,
    total_carbon_from_alkalinity,
)

ChemicalKindT = Literal["acid", "base"]

PH_TOLERANCE = 0.005
PH_MIN = 3.0
PH_MAX = 11.0


@dataclass
class Chemical:
    id: str
    name: str
    formula: str
    kind: ChemicalKindT
    mw: float  # g/mol
    z: Union[float, Literal["phosphoric"]]
    purity_pct: float  # درصد خلوص وزنی محصول تجاری
    density_g_ml: float  # چگالی محصول تجاری g/mL
    source: Literal["fertilizer_db", "manual"] = "manual"
    fertilizer_id: Optional[int] = None


@dataclass
class DoseInputBase:
    volume_l: float
    current_ph: float
    target_ph: float
    temperature_c: float
    chemical: Chemical


@dataclass
class TheoreticalInput(DoseInputBase):
    alkalinity_mg_l: float = 0.0  # همیشه به mg/L معادل CaCO₃ نرمال‌شده می‌رسد
    sample_type: Literal["simple", "complex"] = "simple"


@dataclass
class TitrationPoint:
    volume_ml: float
    ph: float


@dataclass
class TitrationInput(DoseInputBase):
    points: List[TitrationPoint] = field(default_factory=list)
    normality: float = 0.1
    sample_volume_ml: float = 100.0


class DoseError(Exception):
    """خطای اعتبارسنجی یا محاسبه؛ پیام آن مستقیماً قابل نمایش به کاربر است."""

    def __init__(self, message: str, need_titration: bool = False):
        super().__init__(message)
        self.message = message
        self.need_titration = need_titration


@dataclass
class DoseResult:
    ok: bool
    method: Literal["theoretical", "titration", "no-adjustment"]
    direction: Literal["acid", "base", "none"]
    total_meq: float
    effective_z: float
    pure_mass_g: float
    commercial_mass_g: float
    commercial_volume_l: float
    warnings: List[str] = field(default_factory=list)
    sensitivity: Optional[dict] = None  # {"min_l": .., "max_l": ..}
    theoretical: Optional[dict] = None
    titration: Optional[dict] = None


# ------------------------------------------------------------
# اعتبارسنجی مشترک
# ------------------------------------------------------------
def validate_base(inp: DoseInputBase) -> None:
    if not (inp.volume_l > 0):
        raise DoseError("حجم محلول باید بزرگ‌تر از صفر باشد.")
    if not (PH_MIN <= inp.current_ph <= PH_MAX):
        raise DoseError(f"pH فعلی باید بین {PH_MIN:g} تا {PH_MAX:g} باشد.")
    if not (PH_MIN <= inp.target_ph <= PH_MAX):
        raise DoseError(f"pH هدف باید بین {PH_MIN:g} تا {PH_MAX:g} باشد.")
    if not (0 <= inp.temperature_c <= 60):
        raise DoseError("دما باید بین ۰ تا ۶۰ درجه‌ی سانتی‌گراد باشد.")

    c = inp.chemical
    if not (c.mw > 0):
        raise DoseError("جرم مولی ماده شیمیایی نامعتبر است.")
    if c.z != "phosphoric" and not (c.z > 0):
        raise DoseError("ظرفیت مؤثر ماده شیمیایی نامعتبر است.")
    if not (0 < c.purity_pct <= 100):
        raise DoseError("خلوص باید بین ۰ تا ۱۰۰ درصد باشد.")
    if not (c.density_g_ml > 0):
        raise DoseError("چگالی ماده شیمیایی نامعتبر است.")

    if abs(inp.current_ph - inp.target_ph) >= PH_TOLERANCE:
        needed: ChemicalKindT = "acid" if inp.target_ph < inp.current_ph else "base"
        if c.kind != needed:
            if needed == "acid":
                raise DoseError('برای کاهش pH باید یک «اسید» انتخاب کنید.')
            raise DoseError('برای افزایش pH باید یک «باز» انتخاب کنید.')


def _zero_result() -> DoseResult:
    return DoseResult(
        ok=True,
        method="no-adjustment",
        direction="none",
        total_meq=0.0,
        effective_z=1.0,
        pure_mass_g=0.0,
        commercial_mass_g=0.0,
        commercial_volume_l=0.0,
        warnings=[],
    )


def equivalents_to_commercial(total_meq: float, chemical: Chemical, target_ph: float) -> dict:
    """
    تبدیل معادل شیمیایی به ماده‌ی خالص و ماده‌ی تجاری:
        جرم خالص (g)   = meq × (MW / z) ÷ 1000
        حجم تجاری (L)  = جرم تجاری ÷ (چگالی × 1000)
    """
    z = phosphoric_effective_z(target_ph) if chemical.z == "phosphoric" else chemical.z
    pure_mass_g = (total_meq * (chemical.mw / z)) / 1000
    purity = chemical.purity_pct / 100
    commercial_mass_g = pure_mass_g / purity
    commercial_volume_l = commercial_mass_g / chemical.density_g_ml / 1000
    return {
        "effective_z": z,
        "pure_mass_g": pure_mass_g,
        "commercial_mass_g": commercial_mass_g,
        "commercial_volume_l": commercial_volume_l,
    }


def _direction_of(current_ph: float, target_ph: float) -> Literal["acid", "base"]:
    return "acid" if target_ph < current_ph else "base"


def _common_warnings(inp: DoseInputBase) -> List[str]:
    warnings: List[str] = []
    if inp.chemical.z == "phosphoric":
        warnings.append(
            "برای اسید فسفریک ظرفیت ثابت ۳ استفاده نشده است؛ ظرفیت مؤثر بر اساس "
            "گونه‌بندی فسفات در pH هدف محاسبه شد."
        )
    if inp.chemical.kind == "base":
        warnings.append(
            "در افزایش pH، خروج CO₂ و ترکیب محلول می‌تواند دوز واقعی را تغییر دهد؛ "
            "حتماً مرحله‌ای تزریق و اندازه‌گیری کنید."
        )
    return warnings


# ------------------------------------------------------------
# مسیر ۱: مدل تئوریک کربنات
# ------------------------------------------------------------
def _theoretical_total_meq(
    alk_mg_l: float, current_ph: float, target_ph: float, temperature_c: float, volume_l: float
) -> Optional[dict]:
    c = carbonate_constants(temperature_c)
    alk_eq_l = alk_mg_l / 50000  # mg/L CaCO3 -> eq/L
    ct = total_carbon_from_alkalinity(current_ph, alk_eq_l, c)
    if not (ct > 0):
        return None

    target_alk_eq_l = alkalinity_from_ct(target_ph, ct, c)
    acid = target_ph < current_ph
    delta_eq_l = (alk_eq_l - target_alk_eq_l) if acid else (target_alk_eq_l - alk_eq_l)
    if not (delta_eq_l > 0):
        return None

    return {
        "total_meq": delta_eq_l * 1000 * volume_l,
        "delta_meq_l": delta_eq_l * 1000,
        "ct_mmol_l": ct * 1000,
        "target_alk_mg_l": target_alk_eq_l * 50000,
        "pK1": c.pK1,
        "pK2": c.pK2,
    }


def calculate_theoretical(inp: TheoreticalInput) -> DoseResult:
    validate_base(inp)

    if abs(inp.current_ph - inp.target_ph) < PH_TOLERANCE:
        return _zero_result()

    if inp.sample_type == "complex":
        raise DoseError(
            "برای محلول غذایی یا ترکیبی، مدل عمومی کربناتی قابل اتکا نیست "
            "(فسفات، آمونیوم و اسیدهای آلی بر ظرفیت اسیدی/بازی اثر دارند). "
            "لطفاً از روش «تیتراسیون واقعی» استفاده کنید.",
            need_titration=True,
        )

    if not (inp.alkalinity_mg_l > 0):
        raise DoseError(
            "آلکالینیتی باید بزرگ‌تر از صفر باشد. اگر آلکالینیتی نمونه بسیار کم "
            "است، مدل کربناتی مناسب نیست و تیتراسیون واقعی لازم است.",
            need_titration=True,
        )

    core = _theoretical_total_meq(
        inp.alkalinity_mg_l, inp.current_ph, inp.target_ph, inp.temperature_c, inp.volume_l
    )
    if not core:
        raise DoseError(
            "با این ورودی‌ها مدل کربناتی نتیجه‌ی معتبری نمی‌دهد (آلکالینیتی و pH "
            "با هم سازگار نیستند). مقادیر را بررسی کنید یا از تیتراسیون واقعی "
            "استفاده کنید.",
            need_titration=True,
        )

    conv = equivalents_to_commercial(core["total_meq"], inp.chemical, inp.target_ph)

    # حساسیت به خطای اندازه‌گیری: آلکالینیتی ±۱۰٪ و pH فعلی ±۰٫۱
    volumes: List[float] = []
    for alk_factor in (0.9, 1.0, 1.1):
        for ph_shift in (-0.1, 0.0, 0.1):
            r = _theoretical_total_meq(
                inp.alkalinity_mg_l * alk_factor,
                inp.current_ph + ph_shift,
                inp.target_ph,
                inp.temperature_c,
                inp.volume_l,
            )
            if r:
                volumes.append(
                    equivalents_to_commercial(r["total_meq"], inp.chemical, inp.target_ph)[
                        "commercial_volume_l"
                    ]
                )

    warnings = _common_warnings(inp)
    if inp.current_ph < 6 or inp.current_ph > 9.5:
        warnings.append("pH فعلی خارج از محدوده‌ی معمول آب‌های کربناتی (۶ تا ۹٫۵) است؛ دقت مدل کمتر می‌شود.")
    if inp.target_ph < 5 or inp.target_ph > 9.5:
        warnings.append("pH هدف در ناحیه‌ای است که فرض‌های مدل کربناتی ضعیف‌تر می‌شوند.")

    return DoseResult(
        ok=True,
        method="theoretical",
        direction=_direction_of(inp.current_ph, inp.target_ph),
        total_meq=core["total_meq"],
        effective_z=conv["effective_z"],
        pure_mass_g=conv["pure_mass_g"],
        commercial_mass_g=conv["commercial_mass_g"],
        commercial_volume_l=conv["commercial_volume_l"],
        sensitivity={"min_l": min(volumes), "max_l": max(volumes)} if volumes else None,
        theoretical={
            "ct_mmol_l": core["ct_mmol_l"],
            "initial_alk_mg_l": inp.alkalinity_mg_l,
            "target_alk_mg_l": core["target_alk_mg_l"],
            "delta_meq_l": core["delta_meq_l"],
            "pK1": core["pK1"],
            "pK2": core["pK2"],
        },
        warnings=warnings,
    )


# ------------------------------------------------------------
# مسیر ۲: تیتراسیون واقعی (میان‌یابی خطی روی منحنی pH-حجم)
# ------------------------------------------------------------
def calculate_titration(inp: TitrationInput) -> DoseResult:
    validate_base(inp)

    if abs(inp.current_ph - inp.target_ph) < PH_TOLERANCE:
        return _zero_result()

    if not (inp.normality > 0):
        raise DoseError("نرمالیته‌ی تیترانت باید بزرگ‌تر از صفر باشد.")
    if not (inp.sample_volume_ml > 0):
        raise DoseError("حجم نمونه‌ی تیتراسیون باید بزرگ‌تر از صفر باشد.")
    if not inp.points:
        raise DoseError("حداقل یک نقطه‌ی تیتراسیون (حجم و pH) وارد کنید.")

    for p in inp.points:
        if not (p.volume_ml > 0):
            raise DoseError("حجم تیترانت در هر نقطه باید بزرگ‌تر از صفر باشد.")
        if not (0 <= p.ph <= 14):
            raise DoseError("pH هر نقطه باید بین ۰ تا ۱۴ باشد.")

    curve = sorted(
        [TitrationPoint(0.0, inp.current_ph)] + list(inp.points), key=lambda p: p.volume_ml
    )
    for i in range(1, len(curve)):
        if curve[i].volume_ml == curve[i - 1].volume_ml:
            raise DoseError("حجم‌های تیترانت باید متفاوت باشند (حجم تکراری وجود دارد).")

    direction = _direction_of(inp.current_ph, inp.target_ph)
    warnings = _common_warnings(inp)

    found = None
    for i in range(len(curve) - 1):
        a, b = curve[i], curve[i + 1]
        if (a.ph - inp.target_ph) * (b.ph - inp.target_ph) <= 0 and a.ph != b.ph:
            fraction = (inp.target_ph - a.ph) / (b.ph - a.ph)
            found = {"i": i, "volume_ml": a.volume_ml + fraction * (b.volume_ml - a.volume_ml)}
            break

    if not found:
        phs = [p.ph for p in curve]
        raise DoseError(
            f"pH هدف خارج از محدوده‌ی داده‌های تیتراسیون شما ({min(phs):.2f} تا "
            f"{max(phs):.2f}) است. برای پرهیز از برون‌یابی، تیتراسیون را تا رسیدن "
            "به pH هدف ادامه دهید و نقطه‌های بیشتری ثبت کنید."
        )

    moves_toward_target = (
        curve[1].ph < curve[0].ph if direction == "acid" else curve[1].ph > curve[0].ph
    )
    if not moves_toward_target:
        if direction == "acid":
            raise DoseError('با افزودن تیترانت، pH باید کاهش یابد؛ داده‌ها با تیتراسیون «اسیدی» سازگار نیستند.')
        raise DoseError('با افزودن تیترانت، pH باید افزایش یابد؛ داده‌ها با تیتراسیون «بازی» سازگار نیستند.')

    for i in range(len(curve) - 1):
        step = curve[i + 1].ph - curve[i].ph
        if (direction == "acid" and step > 0) or (direction == "base" and step < 0):
            warnings.append(
                "منحنی تیتراسیون یکنواخت نیست (در برخی نقاط pH خلاف جهت انتظار "
                "حرکت کرده)؛ اختلاط و قرائت‌ها را بررسی کنید."
            )
            break

    meq_per_l = (found["volume_ml"] * inp.normality) / (inp.sample_volume_ml / 1000)
    total_meq = meq_per_l * inp.volume_l
    conv = equivalents_to_commercial(total_meq, inp.chemical, inp.target_ph)

    if len(curve) < 4:
        warnings.append("تعداد نقاط کم است؛ با نقاط بیشتر، میان‌یابی دقیق‌تر می‌شود.")

    return DoseResult(
        ok=True,
        method="titration",
        direction=direction,
        total_meq=total_meq,
        effective_z=conv["effective_z"],
        pure_mass_g=conv["pure_mass_g"],
        commercial_mass_g=conv["commercial_mass_g"],
        commercial_volume_l=conv["commercial_volume_l"],
        titration={
            "from_volume_ml": curve[found["i"]].volume_ml,
            "to_volume_ml": curve[found["i"] + 1].volume_ml,
            "dose_ml": found["volume_ml"],
            "meq_per_l": meq_per_l,
        },
        warnings=warnings,
    )
