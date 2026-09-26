# backend/app/routes/ph_calculator.py
"""
مسیرهای «ماشین‌حساب pH»
============================================================
این تب عمداً خارج از چرخه‌ی رسمی محاسبه‌ی کود قرار دارد (طبق تصمیم
محصول: کاربر پس از ساخت محلول/استوک، جداگانه و چند بار به این صفحه
سر می‌زند تا اصلاح‌های لازم را انجام دهد) اما همچنان:
  • داده‌ی خودش را از سیستم اصلی می‌خواند (کودهای اسیدی واقعی از
    پایگاه‌داده‌ی کود، و به‌صورت اطلاعاتی از آنالیز آب/عناصر هدف)
  • می‌تواند داده‌ی خودش (تاریخچه‌ی محاسبات) را ثبت کند
بدون این‌که صفحات آنالیز آب یا عناصر هدف دست‌کاری شوند.
"""
from __future__ import annotations

from typing import List, Optional

import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

import app.crud as crud
from app.core.ph_calculator import (
    KNOWN_ACID_BASE_CONSTANTS,
    calculate_theoretical,
    calculate_titration,
    normalize_alkalinity_to_mgl,
    resolve_density_g_ml,
)
from app.core.ph_calculator.dose import (
    Chemical as EngineChemical,
    DoseError,
    DoseResult,
    TheoreticalInput,
    TitrationInput,
    TitrationPoint,
)
from app.database import get_db
from app.models import User
from app.schemas import (
    AcidOption,
    ChemicalInput,
    ChemicalOutput,
    DoseResponse,
    MonitoringRequest,
    MonitoringResponse,
    PhContextResponse,
    PhHistoryItem,
    TheoreticalRequest,
    TitrationRequest,
)
from app.security import get_current_user

logger = logging.getLogger(__name__)

ph_calculator_router = APIRouter(prefix="/ph-calculator", tags=["PH Calculator"])

# عناصری که حضورشان در عناصر هدف نشان می‌دهد محلول یک «محلول غذایی/ترکیبی»
# است و مدل کربناتی ساده (فقط آب) دیگر قابل‌اتکا نیست.
COMPLEX_INDICATOR_ELEMENTS = ("P", "N-NH4")


# ============================================================
# کمکی: ساخت Chemical موتور محاسباتی از ورودی کاربر
# ============================================================
def _build_engine_chemical(
    db: Session, chem_in: ChemicalInput, user_id: int
) -> tuple[EngineChemical, bool, bool, Optional[dict]]:
    """
    Returns: (EngineChemical, density_is_reference, density_extrapolated, fertilizer_elements)
    fertilizer_elements: دیکشنری عنصر->درصد وزنی محصول تجاری (از Fertilizer.elements)،
    فقط وقتی ماده از پایگاه‌داده انتخاب شده باشد - برای محاسبه‌ی سهم تغذیه‌ای دوز اصلاحی.
    """
    density_is_reference = False
    density_extrapolated = False

    if chem_in.fertilizer_id is not None:
        fert = crud.get_fertilizer_owned_or_system(db, chem_in.fertilizer_id, user_id)
        if not fert:
            raise HTTPException(status_code=404, detail="کود اسیدی/بازی انتخاب‌شده یافت نشد.")
        if not fert.is_acid:
            raise HTTPException(status_code=400, detail="کود انتخاب‌شده در پایگاه‌داده به عنوان اسید علامت‌گذاری نشده است.")

        acid_type = fert.acid_type
        spec = KNOWN_ACID_BASE_CONSTANTS.get(acid_type) if acid_type else None
        purity_pct = chem_in.purity_pct if chem_in.purity_pct is not None else (fert.concentration or 100.0)

        if spec:
            mw = chem_in.mw if chem_in.mw is not None else spec.mw
            z = chem_in.z if chem_in.z is not None else spec.z
            kind = spec.kind
            name = fert.name
            formula = spec.formula
        else:
            # نوع ناشناخته (کود اسیدی سفارشی بدون acid_type استاندارد) -> باید دستی داده شود
            if chem_in.mw is None or chem_in.z is None:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"نوع اسید «{fert.name}» در جدول ثابت‌های شیمیایی شناخته‌شده نیست "
                        "(acid_type نامشخص یا غیراستاندارد است). لطفاً جرم مولی (mw) و "
                        "ظرفیت مؤثر (z) را دستی وارد کنید."
                    ),
                )
            mw = chem_in.mw
            z = chem_in.z
            kind = "acid"
            name = fert.name
            formula = acid_type or "—"

        if chem_in.density_g_ml is not None:
            density = chem_in.density_g_ml
        elif spec:
            density, density_extrapolated = resolve_density_g_ml(acid_type, purity_pct)
            density_is_reference = True
            if density is None:
                raise HTTPException(
                    status_code=400,
                    detail="چگالی محصول برای این نوع اسید در جدول مرجع موجود نیست؛ لطفاً چگالی (g/mL) را دستی وارد کنید.",
                )
        else:
            raise HTTPException(status_code=400, detail="چگالی (density_g_ml) برای این ماده‌ی سفارشی الزامی است.")

        return (
            EngineChemical(
                id=f"fert-{fert.id}",
                name=name,
                formula=formula,
                kind=kind,
                mw=mw,
                z=z,
                purity_pct=purity_pct,
                density_g_ml=density,
                source="fertilizer_db",
                fertilizer_id=fert.id,
            ),
            density_is_reference,
            density_extrapolated,
            fert.elements if isinstance(fert.elements, dict) else None,
        )

    # ---- ماده‌ی کاملاً سفارشی (بدون fertilizer_id) ----
    missing = [
        field_name
        for field_name, value in (
            ("kind", chem_in.kind),
            ("mw", chem_in.mw),
            ("z", chem_in.z),
            ("purity_pct", chem_in.purity_pct),
            ("density_g_ml", chem_in.density_g_ml),
        )
        if value is None
    ]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"برای ماده‌ی شیمیایی سفارشی (بدون fertilizer_id)، این فیلدها الزامی‌اند: {', '.join(missing)}",
        )

    return (
        EngineChemical(
            id="custom",
            name=chem_in.name or "ماده‌ی سفارشی",
            formula="—",
            kind=chem_in.kind,
            mw=chem_in.mw,
            z=chem_in.z,
            purity_pct=chem_in.purity_pct,
            density_g_ml=chem_in.density_g_ml,
            source="manual",
            fertilizer_id=None,
        ),
        False,
        False,
        None,
    )


def _compute_element_contributions(
    commercial_mass_g: float, elements_pct: Optional[dict], volume_l: float
) -> Optional[dict]:
    """
    غلظت اضافه‌شده‌ی هر عنصر (mg/L) در محلول نهایی، از جرم ماده‌ی تجاریِ افزوده‌شده.
    elements_pct: {element: درصد وزنی در محصول تجاری} (همان Fertilizer.elements،
    که در سراسر برنامه به همین شکل برای محاسبه‌ی مقدار عنصر از جرم کود استفاده می‌شود).
        mg عنصر = جرم تجاری (g) × (درصد/100) × 1000
        mg/L    = mg عنصر ÷ حجم (L)
    """
    if not elements_pct or not (volume_l > 0) or not (commercial_mass_g > 0):
        return None
    result = {}
    for element, pct in elements_pct.items():
        try:
            pct_f = float(pct)
        except (TypeError, ValueError):
            continue
        if pct_f <= 0:
            continue
        mg = commercial_mass_g * (pct_f / 100) * 1000
        result[element] = mg / volume_l
    return result or None


def _chemical_output(chem: EngineChemical, density_is_reference: bool, density_extrapolated: bool) -> ChemicalOutput:
    return ChemicalOutput(
        id=chem.id,
        name=chem.name,
        formula=chem.formula,
        kind=chem.kind,
        mw=chem.mw,
        z=("phosphoric" if chem.z == "phosphoric" else str(chem.z)),
        purity_pct=chem.purity_pct,
        density_g_ml=chem.density_g_ml,
        source=chem.source,
        fertilizer_id=chem.fertilizer_id,
        density_is_reference=density_is_reference,
        density_extrapolated=density_extrapolated,
    )


def _result_to_response(
    result: DoseResult, chemical_out: ChemicalOutput, element_contributions_mg_l: Optional[dict] = None
) -> DoseResponse:
    return DoseResponse(
        ok=True,
        method=result.method,
        direction=result.direction,
        total_meq=result.total_meq,
        effective_z=result.effective_z,
        pure_mass_g=result.pure_mass_g,
        commercial_mass_g=result.commercial_mass_g,
        commercial_volume_l=result.commercial_volume_l,
        warnings=result.warnings,
        sensitivity=result.sensitivity,
        theoretical=result.theoretical,
        titration=result.titration,
        chemical=chemical_out,
        element_contributions_mg_l=element_contributions_mg_l,
    )


# ============================================================
# GET /ph-calculator/acids - لیست اسیدهای واقعی پایگاه‌داده (dropdown)
# ============================================================
@ph_calculator_router.get("/acids", response_model=List[AcidOption])
def list_acid_options(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    اسیدهای واقعیِ ثبت‌شده در پایگاه‌داده‌ی کود (سیستمی + شخصی کاربر)
    که is_acid=True دارند - یعنی همان کودهایی که در محاسبه‌ی اصلی وارد
    «مخزن C» می‌شوند. جایگزین لیست ثابت و هاردکد نسخه‌ی قبلی.
    """
    fertilizers = crud.get_acid_fertilizers_for_user(db, current_user.id)
    options: List[AcidOption] = []
    for f in fertilizers:
        spec = KNOWN_ACID_BASE_CONSTANTS.get(f.acid_type) if f.acid_type else None
        density = None
        extrapolated = False
        if spec:
            density, extrapolated = resolve_density_g_ml(f.acid_type, f.concentration or 100.0)
        options.append(
            AcidOption(
                fertilizer_id=f.id,
                name=f.name,
                acid_type=f.acid_type,
                concentration=f.concentration or 100.0,
                form=f.form,
                is_system_default=f.is_system_default,
                recognized=spec is not None,
                suggested_mw=spec.mw if spec else None,
                suggested_z=("phosphoric" if spec and spec.z == "phosphoric" else (str(spec.z) if spec else None)),
                suggested_density_g_ml=density,
                density_extrapolated=extrapolated,
            )
        )
    return options


# ============================================================
# GET /ph-calculator/context - داده‌ی زمینه از آنالیز آب/عناصر هدف
# (فقط خواندن؛ صفحات دیگر دست‌کاری نمی‌شوند)
# ============================================================
@ph_calculator_router.get("/context", response_model=PhContextResponse)
def get_ph_context(
    report_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    water_salinity = None
    water_values = None
    target_elements = None
    target_unit = None
    latest_reservoir_c = None
    is_recirculating_system = None

    if report_id is not None:
        report = crud.get_report_by_id(db, report_id)
        if report and report.user_id == current_user.id:
            is_recirculating_system = report.is_recirculating_system

        water_analysis = crud.get_water_analysis_by_report(db, report_id)
        if water_analysis:
            water_salinity = water_analysis.water_salinity
            water_values = water_analysis.water_values or {}

        calculation = crud.get_calculation_by_report(db, report_id)
        if calculation:
            target_elements = calculation.target_values or {}
            reservoir_data = calculation.reservoir_data or {}
            if isinstance(reservoir_data, dict):
                latest_reservoir_c = reservoir_data.get("C")

    complex_indicators = []
    if target_elements:
        for el in COMPLEX_INDICATOR_ELEMENTS:
            if target_elements.get(el, 0):
                complex_indicators.append(el)

    return PhContextResponse(
        water_salinity=water_salinity,
        water_values=water_values,
        target_elements=target_elements,
        target_unit=target_unit,
        is_likely_complex_solution=bool(complex_indicators),
        complex_indicator_elements=complex_indicators,
        latest_reservoir_c=latest_reservoir_c,
        is_recirculating_system=is_recirculating_system,
    )


# ============================================================
# POST /ph-calculator/theoretical
# ============================================================
@ph_calculator_router.post("/theoretical", response_model=DoseResponse)
def calculate_theoretical_endpoint(
    payload: TheoreticalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    chem, density_is_ref, density_extrapolated, fert_elements = _build_engine_chemical(
        db, payload.chemical, current_user.id
    )
    alk_mg_l = normalize_alkalinity_to_mgl(payload.alkalinity_value, payload.alkalinity_unit)

    engine_input = TheoreticalInput(
        volume_l=payload.volume_l,
        current_ph=payload.current_ph,
        target_ph=payload.target_ph,
        temperature_c=payload.temperature_c,
        chemical=chem,
        alkalinity_mg_l=alk_mg_l,
        sample_type=payload.sample_type,
    )

    try:
        result = calculate_theoretical(engine_input)
    except DoseError as e:
        raise HTTPException(
            status_code=422,
            detail={"error": e.message, "need_titration": e.need_titration},
        )

    chemical_out = _chemical_output(chem, density_is_ref, density_extrapolated)
    element_contributions = _compute_element_contributions(result.commercial_mass_g, fert_elements, payload.volume_l)
    response = _result_to_response(result, chemical_out, element_contributions)

    if payload.save:
        record = crud.save_ph_calculation(
            db,
            user_id=current_user.id,
            report_id=payload.report_id,
            method=result.method,
            direction=result.direction,
            inputs=payload.model_dump(),
            outputs=response.model_dump(),
            chemical_name=chem.name,
            fertilizer_id=chem.fertilizer_id,
            note=payload.note,
            record_type="correction",
            ec_ms_cm=payload.ec_ms_cm,
        )
        response.saved_id = record.id

    return response


# ============================================================
# POST /ph-calculator/titration
# ============================================================
@ph_calculator_router.post("/titration", response_model=DoseResponse)
def calculate_titration_endpoint(
    payload: TitrationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    chem, density_is_ref, density_extrapolated, fert_elements = _build_engine_chemical(
        db, payload.chemical, current_user.id
    )

    engine_input = TitrationInput(
        volume_l=payload.volume_l,
        current_ph=payload.current_ph,
        target_ph=payload.target_ph,
        temperature_c=payload.temperature_c,
        chemical=chem,
        points=[TitrationPoint(volume_ml=p.volume_ml, ph=p.ph) for p in payload.points],
        normality=payload.normality,
        sample_volume_ml=payload.sample_volume_ml,
    )

    try:
        result = calculate_titration(engine_input)
    except DoseError as e:
        raise HTTPException(
            status_code=422,
            detail={"error": e.message, "need_titration": e.need_titration},
        )

    chemical_out = _chemical_output(chem, density_is_ref, density_extrapolated)
    element_contributions = _compute_element_contributions(result.commercial_mass_g, fert_elements, payload.volume_l)
    response = _result_to_response(result, chemical_out, element_contributions)

    if payload.save:
        record = crud.save_ph_calculation(
            db,
            user_id=current_user.id,
            report_id=payload.report_id,
            method=result.method,
            direction=result.direction,
            inputs=payload.model_dump(),
            outputs=response.model_dump(),
            chemical_name=chem.name,
            fertilizer_id=chem.fertilizer_id,
            note=payload.note,
            record_type="correction",
            ec_ms_cm=payload.ec_ms_cm,
        )
        response.saved_id = record.id

    return response


# ============================================================
# 🆕 POST /ph-calculator/monitoring - ثبت سریع یک اندازه‌گیری
# (بدون محاسبه‌ی دوز) - برای پایش روند در سیستم‌های بازچرخشی
# ============================================================
@ph_calculator_router.post("/monitoring", response_model=MonitoringResponse)
def log_monitoring_point(
    payload: MonitoringRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = crud.save_ph_calculation(
        db,
        user_id=current_user.id,
        report_id=payload.report_id,
        method=None,
        direction=None,
        inputs=payload.model_dump(),
        outputs={"ph": payload.ph, "ec_ms_cm": payload.ec_ms_cm},
        chemical_name=None,
        fertilizer_id=None,
        note=payload.note,
        record_type="monitoring",
        ec_ms_cm=payload.ec_ms_cm,
    )
    return MonitoringResponse(ok=True, id=record.id, created_at=record.created_at)


# ============================================================
# 🆕 GET /ph-calculator/latest-correction - برای نمایش در «مخزن C»
# صفحه‌ی محاسبه کود (خواندنی؛ بازتریگر بهینه‌ساز نمی‌کند)
# ============================================================
@ph_calculator_router.get("/latest-correction", response_model=Optional[PhHistoryItem])
def get_latest_correction_endpoint(
    report_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = crud.get_latest_correction(db, current_user.id, report_id)
    return record


# ============================================================
# تاریخچه
# ============================================================
@ph_calculator_router.get("/history", response_model=List[PhHistoryItem])
def get_history(
    report_id: Optional[int] = Query(None),
    record_type: Optional[str] = Query(None, pattern="^(correction|monitoring)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    records = crud.get_ph_calculations(
        db, current_user.id, report_id=report_id, record_type=record_type, skip=skip, limit=limit
    )
    return records


@ph_calculator_router.delete("/history/{calc_id}")
def delete_history_item(
    calc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ok = crud.delete_ph_calculation(db, calc_id, current_user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="رکورد یافت نشد.")
    return {"success": True}
