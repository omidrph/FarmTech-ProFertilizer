# backend/app/routes/ph_calculator.py
"""
مسیرهای تب «PH» - اصلاح pH با اسید/باز
============================================================
دو حالت ورودی (هر دو به «مقدار برای کل مخزن» می‌رسند):
  • known : رسپی/دوز مشخص (مقیاس‌دهی به حجم مخزن)
  • trial : آزمون و خطا روی نمونه (مثلاً ۵ لیتر از مخزن ۵۰۰۰ لیتری) و تعمیم به مخزن

تب pH مستقل است (کاربر پس از ساخت محلول به آن می‌آید)، اما نتیجه‌اش وقتی
«اعمال» شود وارد چرخهٔ محاسبه می‌گردد: عناصر اسید/باز مثل آب یک منبع پایه
لحاظ می‌شوند (core/ph_calculator/integration.py) و سهم کودهای دیگر، تعادل یونی
و EC با آن‌ها دوباره محاسبه می‌شود.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

import app.crud as crud
from app.core.ph_calculator import (
    DISCOURAGED,
    AdjustmentError,
    TrialStep,
    alkalinity_check,
    check_direction,
    default_dose_unit,
    derive_elements_pct,
    ec_delta_ds_m,
    element_contributions_mg_l,
    get_spec,
    neutralization_strength_meq_l,
    resolve_density_g_ml,
    scale_to_tank,
    solve_trial,
    summary_from_record,
)
from app.database import get_db
from app.models import Fertilizer, User
from app.schemas import (
    ActiveAdjustmentSummary,
    AdjusterOption,
    AdjustmentItem,
    AdjustmentRequest,
    AdjustmentResult,
    AdjustmentSaveRequest,
    PhContextResponse,
)
from app.security import get_current_user

logger = logging.getLogger(__name__)

ph_calculator_router = APIRouter(prefix="/ph-calculator", tags=["PH Calculator"])

SUGGESTED_TARGET_PH = 6.0
TARGET_PH_RANGE = [5.5, 6.5]


# ============================================================
# کمکی‌ها
# ============================================================
def _clean_elements(raw: Any) -> Dict[str, float]:
    out: Dict[str, float] = {}
    if isinstance(raw, dict):
        for k, v in raw.items():
            try:
                f = float(v)
            except (TypeError, ValueError):
                continue
            if f > 0:
                out[str(k)] = f
    return out


def _describe_fertilizer(fert: Fertilizer) -> Dict[str, Any]:
    """مشخصات مؤثر یک اسید/باز از روی کود پایگاه‌داده (مشترک بین لیست و محاسبه)."""
    spec = get_spec(fert.acid_type)
    warnings: List[str] = []

    if fert.is_base and not fert.is_acid:
        kind = "base"
    elif fert.is_acid and not fert.is_base:
        kind = "acid"
    else:
        kind = spec.kind if spec else ("base" if fert.is_base else "acid")
    if spec and spec.kind != kind:
        warnings.append(
            f"نوع ثبت‌شده برای «{fert.name}» با فرمول {fert.acid_type} هم‌خوان نیست؛ بر اساس فرمول «{'اسید' if spec.kind == 'acid' else 'باز'}» در نظر گرفته شد."
        )
        kind = spec.kind

    purity = float(fert.concentration or 100.0)
    db_elements = _clean_elements(fert.elements)

    # درصد وزنی عناصر در «محصول تجاری»:
    #  • اسید/بازِ شناخته‌شده → از فرمول و خلوص (دقیق و مستقل از نحوهٔ ثبت درصدها؛ در پایگاه‌داده‌ی
    #    فعلی درصد عناصر اسیدها از قبل در خلوص ضرب شده ولی برای کودهای دیگر «ماده خالص» است)
    #  • ناشناخته (سفارشی) → درصد ثبت‌شده، طبق قرارداد برنامه («ماده خالص») × خلوص
    derived = derive_elements_pct(fert.acid_type, purity)
    if derived:
        elements, source = derived, "derived"
        main = next(iter(derived))
        db_main = db_elements.get(main)
        if db_main and abs(db_main - derived[main]) / derived[main] > 0.05:
            warnings.append(
                f"درصد {main} ثبت‌شده در پایگاه‌داده ({db_main:.2f}٪) با فرمول و خلوص این ماده "
                f"({derived[main]:.2f}٪) هم‌خوان نیست؛ مقدار محاسبه‌شده از فرمول استفاده شد."
            )
    elif db_elements:
        elements = {k: v * purity / 100.0 for k, v in db_elements.items()}
        source = "database"
    else:
        elements, source = {}, "missing"
        warnings.append("درصد عناصر این کود ثبت نشده و نوع آن شناخته‌شده نیست؛ ابتدا آن را در پایگاه‌داده کود کامل کنید.")

    unit = default_dose_unit(fert.form, kind)
    density, extrapolated = (None, False)
    if unit == "ml":
        density, extrapolated = resolve_density_g_ml(fert.acid_type, purity)

    if fert.acid_type in DISCOURAGED:
        warnings.append(DISCOURAGED[fert.acid_type])

    return {
        "kind": kind,
        "spec": spec,
        "purity": purity,
        "elements": elements,
        "elements_source": source,
        "unit": unit,
        "density": density,
        "density_extrapolated": extrapolated,
        "warnings": warnings,
    }


def _get_owned_report(db: Session, report_id: Optional[int], user: User):
    if not report_id:
        return None
    report = crud.get_report_by_id(db, report_id)
    if not report or report.user_id != user.id:
        return None
    return report


def _report_context(db: Session, report_id: Optional[int], user: User) -> Dict[str, Any]:
    """tank_volume، pH و آلکالینیتی آب، EC پایه (بدون اصلاح فعال)، نام گیاه."""
    ctx: Dict[str, Any] = {
        "plant_name": None, "tank_volume_l": None, "water_ph": None,
        "water_alkalinity_ppm": None, "base_ec": None,
    }
    report = _get_owned_report(db, report_id, user)
    if not report:
        return ctx
    ctx["plant_name"] = report.plant_name

    water = crud.get_water_analysis_by_report(db, report.id)
    if water and isinstance(water.water_values, dict):
        wv = water.water_values
        ctx["water_ph"] = wv.get("pH") or None
        ctx["water_alkalinity_ppm"] = wv.get("Alkalinity") or None

    calc = crud.get_calculation_by_report(db, report.id)
    if calc:
        rd = calc.reservoir_data if isinstance(calc.reservoir_data, dict) else {}
        settings = rd.get("settings") if isinstance(rd.get("settings"), dict) else {}
        ctx["tank_volume_l"] = settings.get("tank_volume") or None
        res = calc.optimization_result if isinstance(calc.optimization_result, dict) else {}
        saved_ec = res.get("ec")
        if isinstance(saved_ec, (int, float)) and saved_ec > 0:
            applied = res.get("ph_adjustment") if isinstance(res.get("ph_adjustment"), dict) else {}
            applied_delta = applied.get("ec_delta") or 0
            ctx["base_ec"] = round(max(0.0, saved_ec - applied_delta), 3)
    return ctx


def _compute(db: Session, user: User, req: AdjustmentRequest) -> Tuple[AdjustmentResult, Fertilizer]:
    fert = crud.get_user_fertilizer(db, req.fertilizer_id, user.id)
    if not fert:
        raise HTTPException(status_code=404, detail="اسید/باز انتخاب‌شده در پایگاه‌داده کود شما یافت نشد.")
    if not (fert.is_acid or fert.is_base):
        raise HTTPException(status_code=400, detail="کود انتخاب‌شده به‌عنوان اسید یا باز علامت‌گذاری نشده است.")

    info = _describe_fertilizer(fert)
    if info["elements_source"] == "missing":
        raise HTTPException(status_code=400, detail=info["warnings"][-1])

    kind: str = info["kind"]
    unit: str = info["unit"]
    density = req.density_g_ml if (req.density_g_ml and unit == "ml") else info["density"]
    density_is_reference = bool(unit == "ml" and not req.density_g_ml)
    if unit == "ml" and not density:
        raise HTTPException(
            status_code=400,
            detail=f"چگالی «{fert.name}» ناشناخته است؛ چگالی دقیق (g/mL) را از برگهٔ مشخصات محصول وارد کنید.",
        )

    warnings: List[str] = list(info["warnings"])
    if density_is_reference:
        warnings.append("چگالی از جدول مرجع تقریبی برداشته شده؛ برای دقت بیشتر مقدار برگهٔ مشخصات (SDS) محصول را وارد کنید.")

    try:
        trial_info: Dict[str, Any] = {}
        if req.mode == "trial":
            check_direction(kind, req.initial_ph, req.target_ph)
            solution = solve_trial(
                req.initial_ph, req.target_ph, [TrialStep(s.amount, s.ph) for s in req.steps]
            )
            tank = scale_to_tank(solution.sample_dose, req.sample_volume_l, req.tank_volume_l)
            final_ph = solution.final_ph
            warnings += solution.warnings + tank.warnings
            if req.sample_volume_l < 1:
                warnings.append("حجم نمونه کمتر از ۱ لیتر است؛ نمونهٔ بزرگ‌تر دقت بهتری می‌دهد.")
            trial_info = {
                "sample_volume_l": req.sample_volume_l,
                "scale_factor": tank.scale_factor,
                "sample_dose": solution.sample_dose,
                "trial_method": solution.method,
                "curve": solution.curve,
            }
        else:
            if (
                req.initial_ph is not None
                and req.target_ph is not None
                and abs(req.initial_ph - req.target_ph) > 1e-9
            ):
                check_direction(kind, req.initial_ph, req.target_ph)
            basis = req.dose_basis_volume_l or req.tank_volume_l
            tank = scale_to_tank(req.dose_amount, basis, req.tank_volume_l)
            final_ph = req.target_ph
            warnings += tank.warnings
            trial_info = {"dose_basis_volume_l": basis}
    except AdjustmentError as e:
        raise HTTPException(status_code=422, detail=e.message)

    commercial_mass_g = tank.amount * density if unit == "ml" else tank.amount
    pure_mass_g = commercial_mass_g * info["purity"] / 100.0
    contrib = element_contributions_mg_l(commercial_mass_g, info["elements"], req.tank_volume_l)
    strength = neutralization_strength_meq_l(contrib, kind)
    ec_delta = ec_delta_ds_m(contrib)

    ctx = _report_context(db, req.report_id, user)
    alk_meq, alk_warnings = alkalinity_check(strength, kind, ctx["water_alkalinity_ppm"])
    warnings += alk_warnings
    base_ec = ctx["base_ec"]

    snapshot = {
        "fertilizer_id": fert.id,
        "name": fert.name,
        "kind": kind,
        "acid_type": fert.acid_type,
        "form": fert.form,
        "purity_pct": info["purity"],
        "density_g_ml": density if unit == "ml" else None,
        "density_is_reference": density_is_reference,
        "elements_pct": info["elements"],
        "elements_source": info["elements_source"],
    }

    result = AdjustmentResult(
        mode=req.mode, kind=kind, chemical=snapshot, dose_unit=unit,
        tank_volume_l=req.tank_volume_l, initial_ph=req.initial_ph, target_ph=req.target_ph, final_ph=final_ph,
        dose_tank=tank.amount, dose_per_1000l=tank.per_1000_l,
        commercial_mass_g=commercial_mass_g, pure_mass_g=pure_mass_g,
        stage_first=tank.stage_first, stage_rest=tank.stage_rest,
        element_contributions=contrib, strength_meq_l=strength,
        water_alkalinity_meq_l=alk_meq, ec_delta=ec_delta,
        base_ec=base_ec, predicted_ec=round(base_ec + ec_delta, 3) if base_ec is not None else None,
        warnings=list(dict.fromkeys(warnings)),
        **trial_info,
    )
    return result, fert


def _to_item(record) -> AdjustmentItem:
    return AdjustmentItem.model_validate(record)


# ============================================================
# GET /ph-calculator/adjusters  - اسید/بازهای پایگاه‌داده کود کاربر
# ============================================================
@ph_calculator_router.get("/adjusters", response_model=List[AdjusterOption])
def list_adjusters(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    options: List[AdjusterOption] = []
    for f in crud.list_adjuster_fertilizers(db, current_user.id):
        info = _describe_fertilizer(f)
        options.append(
            AdjusterOption(
                fertilizer_id=f.id, name=f.name, kind=info["kind"], acid_type=f.acid_type, form=f.form,
                concentration=info["purity"], dose_unit=info["unit"], elements_pct=info["elements"],
                elements_source=info["elements_source"], density_g_ml=info["density"],
                density_is_reference=info["unit"] == "ml" and info["density"] is not None,
                density_extrapolated=info["density_extrapolated"], recognized=info["spec"] is not None,
                warnings=info["warnings"],
            )
        )
    return options


# ============================================================
# GET /ph-calculator/context
# ============================================================
@ph_calculator_router.get("/context", response_model=PhContextResponse)
def get_context(
    report_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ctx = _report_context(db, report_id, current_user)
    active = None
    if _get_owned_report(db, report_id, current_user):
        rec = crud.get_active_adjustment(db, current_user.id, report_id)
        if rec:
            active = ActiveAdjustmentSummary(**summary_from_record(rec))
    return PhContextResponse(
        plant_name=ctx["plant_name"], tank_volume_l=ctx["tank_volume_l"], water_ph=ctx["water_ph"],
        water_alkalinity_ppm=ctx["water_alkalinity_ppm"], base_ec=ctx["base_ec"],
        suggested_target_ph=SUGGESTED_TARGET_PH, target_ph_range=TARGET_PH_RANGE, active=active,
    )


# ============================================================
# POST /ph-calculator/preview  (بدون ذخیره)
# ============================================================
@ph_calculator_router.post("/preview", response_model=AdjustmentResult)
def preview_adjustment(
    payload: AdjustmentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result, _ = _compute(db, current_user, payload)
    return result


# ============================================================
# POST /ph-calculator/adjustments  (محاسبه + ذخیره در تاریخچه، اختیاری اعمال)
# ============================================================
@ph_calculator_router.post("/adjustments", response_model=AdjustmentItem, status_code=status.HTTP_201_CREATED)
def save_adjustment(
    payload: AdjustmentSaveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not _get_owned_report(db, payload.report_id, current_user):
        raise HTTPException(status_code=404, detail="گزارش یافت نشد.")

    result, fert = _compute(db, current_user, payload)
    data = dict(
        mode=result.mode, kind=result.kind, fertilizer_id=fert.id, chemical_name=fert.name[:100],
        chemical=result.chemical.model_dump(),
        tank_volume_l=result.tank_volume_l, initial_ph=result.initial_ph, target_ph=result.target_ph,
        final_ph=result.final_ph, sample_volume_l=result.sample_volume_l,
        trial_steps=[s.model_dump() for s in payload.steps] if payload.mode == "trial" else None,
        dose_unit=result.dose_unit, dose_tank=result.dose_tank, dose_per_1000l=result.dose_per_1000l,
        element_contributions=result.element_contributions, ec_delta=result.ec_delta,
        ec_before=payload.ec_before, ec_after=payload.ec_after, note=payload.note,
    )
    record = crud.create_adjustment(db, current_user.id, payload.report_id, data, activate=payload.apply)
    return _to_item(record)


# ============================================================
# تاریخچه و فعال/غیرفعال‌سازی
# ============================================================
@ph_calculator_router.get("/adjustments", response_model=List[AdjustmentItem])
def list_history(
    report_id: int = Query(...),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not _get_owned_report(db, report_id, current_user):
        return []
    return [_to_item(r) for r in crud.list_adjustments(db, current_user.id, report_id, limit)]


def _owned_or_404(db: Session, adj_id: int, user: User):
    rec = crud.get_adjustment(db, adj_id, user.id)
    if not rec:
        raise HTTPException(status_code=404, detail="رکورد یافت نشد.")
    return rec


@ph_calculator_router.post("/adjustments/{adj_id}/apply", response_model=AdjustmentItem)
def apply_adjustment(adj_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rec = _owned_or_404(db, adj_id, current_user)
    return _to_item(crud.set_adjustment_active(db, rec, True))


@ph_calculator_router.post("/adjustments/{adj_id}/unapply", response_model=AdjustmentItem)
def unapply_adjustment(adj_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rec = _owned_or_404(db, adj_id, current_user)
    return _to_item(crud.set_adjustment_active(db, rec, False))


@ph_calculator_router.delete("/adjustments/{adj_id}")
def delete_adjustment_route(adj_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rec = _owned_or_404(db, adj_id, current_user)
    crud.delete_adjustment(db, rec)
    return {"success": True}


# ============================================================
# GET /ph-calculator/active  - برای صفحهٔ محاسبهٔ کود
# ============================================================
@ph_calculator_router.get("/active", response_model=Optional[ActiveAdjustmentSummary])
def get_active(
    report_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not _get_owned_report(db, report_id, current_user):
        return None
    rec = crud.get_active_adjustment(db, current_user.id, report_id)
    return ActiveAdjustmentSummary(**summary_from_record(rec)) if rec else None
