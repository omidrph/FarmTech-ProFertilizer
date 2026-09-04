// frontend/src/types/index.ts

// ============================================================
// ENUMS
// ============================================================
export enum Unit {
    PPM = 'ppm',
    MEQ = 'meq',
    MMOL = 'mmol'
}

export enum ElementName {
    N_NO3 = 'N-NO3',
    P = 'P',
    S = 'S',
    N_NH4 = 'N-NH4',
    K = 'K',
    Ca = 'Ca',
    Mg = 'Mg',
    Na = 'Na',
    Cl = 'Cl',
    Fe = 'Fe',
    Mn = 'Mn',
    Zn = 'Zn',
    B = 'B',
    Cu = 'Cu',
    Mo = 'Mo'
}

export enum ReservoirType {
    A = 'A',
    B = 'B',
    C = 'C'
}

export enum TabType {
    HOME = 'home',
    WATER_ANALYSIS = 'water-analysis',
    TARGET_ELEMENTS = 'target-elements',
    FERTILIZER_CALC = 'fertilizer-calc',
    FERTILIZER_DB = 'fertilizer-db',
    INTERPRETATION = 'interpretation'
}

// ============================================================
// INTERFACES
// ============================================================
export interface ElementRow {
    name: ElementName | string;
    targetValue: number;
    finalValue: number;
}

export interface WaterAnalysisRow {
    element: ElementName | string;
    wastewater: number;
    water: number;
    finalValue: number;
}

// ============================================================
// Fertilizer Interface - نسخه نهایی
// ============================================================
export interface Fertilizer {
    id: string;
    user_id: number | null;
    name: string;
    
    // فیلدهای اطلاعاتی
    brand?: string;
    category?: string;
    form?: 'liquid' | 'powder' | 'crystal' | 'granular';
    
    // فیلدهای محاسباتی
    concentration: number;          // درصد خلوص/غلظت
    elements: Partial<Record<ElementName, number>>;
    pricePerKg: number;
    
    // فیلدهای اسید و pH
    isAcid: boolean;
    acidType?: 'H3PO4' | 'HNO3' | 'H2SO4' | string;
    phLevel?: number;               // pH محلول
    
    // توضیحات
    description?: string;
    
    // فیلدهای سیستمی
    isSystemDefault: boolean;
    sourceSystemId?: number;        // ID کود سیستمی مبدا
    
    // تاریخ‌ها
    createdAt: Date;
    updatedAt: Date;
}

export interface FertilizerCreate {
    name: string;
    brand?: string;
    category?: string;
    form?: 'liquid' | 'powder' | 'crystal' | 'granular';
    concentration?: number;
    elements?: Partial<Record<ElementName, number>>;
    pricePerKg?: number;
    isAcid?: boolean;
    acidType?: 'H3PO4' | 'HNO3' | 'H2SO4' | string;
    phLevel?: number;
    description?: string;
}

export interface FertilizerUpdate {
    name?: string;
    brand?: string;
    category?: string;
    form?: 'liquid' | 'powder' | 'crystal' | 'granular';
    concentration?: number;
    elements?: Partial<Record<ElementName, number>>;
    pricePerKg?: number;
    isAcid?: boolean;
    acidType?: 'H3PO4' | 'HNO3' | 'H2SO4' | string;
    phLevel?: number;
    description?: string;
}

// ============================================================
// Interfaces مربوط به محاسبات
// ============================================================
export interface ReservoirItem {
    name: string;
    amount: number;
    purity?: number;
    fertilizer_id?: string;  // ✅ اضافه شد - شناسه کود برای تطابق با مخزن
    has_calcium?: boolean;
    is_acid?: boolean;
}

export interface StockSettings {
    tankVolume: number;
    stockVolume: number;
    injectionRatio: number;
}

export interface ReservoirData {
    A: ReservoirItem[];
    B: ReservoirItem[];
    C: ReservoirItem[];
    // 🆕 تنظیمات استوک (حجم مخزن، حجم سطل استوک، نسبت تزریق) اینجا هم
    // ذخیره می‌شود تا با ذخیره/بارگذاری گزارش گم نشود (بدون نیاز به
    // migration پایگاه‌داده، چون reservoir_data یک ستون JSON آزاد است).
    settings?: {
        tank_volume: number;
        stock_volume: number;
        injection_ratio: number;
    };
}

export interface CalculationRow {
    id: string;
    materialName: string;
    weight: number;
    purity: number;
    cost: number;
    elements: Partial<Record<ElementName, number>>;
    isAcid?: boolean;
    acidType?: string;
    isFixedRow?: boolean;
    fertilizerId?: string;
}

export interface CalculationInputs {
    tankVolume: number;
    dilutionFactor: number;
    totalLiter: number;
}

export interface IonBalance {
    cation: number;
    anion: number;
    isBalanced: boolean;
}

export interface ReportData {
    reportName: string;
    plantName: string;
    season: string;
    growthStage: string;
    date: string;
}

export interface WaterMixData {
    waterPercentage: number;
    wastewaterPercentage: number;
    waterSalinity: number;
}

export interface TargetElementData {
    elements: Partial<Record<ElementName, number>>;
    unit: Unit;
}

export interface ElementStatus {
    element: ElementName;
    target: number;
    actual: number;
    difference: number;
    status: 'deficient' | 'sufficient' | 'excessive' | 'toxic';
    message: string;
}

export interface InterpretationResult {
    ionBalance: {
        cation: number;
        anion: number;
        isBalanced: boolean;
        message: string;
    };
    elementStatus: ElementStatus[];
    waterQuality: {
        salinity: number;
        impact: string;
        recommendation: string;
    };
    fertilizerRecommendation: {
        issue: string;
        suggestion: string;
        priority: 'low' | 'medium' | 'high';
    }[];
    summary: string;
}

// ============================================================
// RECIPE TYPES
// ============================================================
export interface Recipe {
    id: number;
    name: string;
    description?: string;
    target_values: Record<string, number>;
    category?: string;
    stage?: string;
    is_system: boolean;
    user_id?: number;
    created_at: string;
    updated_at?: string;
}

export interface RecipeCreate {
    name: string;
    description?: string;
    target_values: Record<string, number>;
    category?: string;
    stage?: string;
}

export interface RecipeUpdate {
    name?: string;
    description?: string;
    target_values?: Record<string, number>;
    category?: string;
    stage?: string;
}

export interface RecipeListResponse {
    system_recipes: Recipe[];
    user_recipes: Recipe[];
}

// ============================================================
// 🆕 OPTIMIZATION TYPES (بهینه‌سازی خودکار) با EC و pH و auto_balance
// ============================================================

export interface OptimizationOptions {
    method?: 'nnls' | 'lsq_linear' | 'lsq_linear_with_cost';
    element_weights?: Record<string, number>;
    max_cost?: number;
    allow_zero_weights?: boolean;
    max_iterations?: number;
    tolerance?: number;
    cost_weight?: number;
    use_precipitation_check?: boolean;
    use_ion_balance_check?: boolean;
    reservoir_mode?: 'auto' | 'manual';
    auto_balance?: boolean;
}

export interface OptimizationFertilizerInput {
    id: string;
    name: string;
    elements: Record<string, number>;
    price_per_kg: number;
    purity: number;
    is_acid: boolean;
    is_system_default: boolean;
    fixed_weight?: number;
}

export interface OptimizationRequest {
    target_values: Record<string, number>;
    water_values?: Record<string, number>;
    fertilizers: OptimizationFertilizerInput[];
    options?: OptimizationOptions;
    tank_volume?: number;
    stock_volume?: number;
    injection_ratio?: number;
}

export interface EcPhStatus {
    status: 'optimal' | 'warning' | 'critical';
    status_label: string;
    color: 'success' | 'warning' | 'danger';
    message: string;
    issues: string[];
    recommendations: string[];
    ec: number;
    ph: number;
    water_ec?: number;
    water_ph?: number;
    ec_status: string;
    ec_label: string;
    ph_status: string;
    ph_label: string;
}

export interface OptimizationResponse {
    weights: Record<string, number>;
    concentrations: Record<string, number>;
    residual_error: number;
    cost_total: number;
    ion_balance: IonBalance;
    target_achievement: Record<string, number>;
    warnings: string[];
    suggestions: string[];
    reservoir_data: ReservoirData;
    iterations: number;
    convergence_time_ms: number;
    is_converged: boolean;
    summary: string;
    ec: number;
    ph: number;
    ec_status: string;
    ph_status: string;
    ec_ph_status: EcPhStatus;
}

export interface PrecipitationRiskItem {
    compound: string;
    ion_product: number;
    ksp: number;
    is_risky: boolean;
    suggestion: string;
}

export interface PrecipitationCheckResponse {
    is_safe: boolean;
    risks: PrecipitationRiskItem[];
    suggestions: string[];
}

export interface OptimizationLogResponse {
    id: number;
    user_id: number;
    report_id?: number;
    target_values: Record<string, number>;
    water_values?: Record<string, number>;
    fertilizers_selected?: Record<string, any>;
    optimized_weights?: Record<string, number>;
    final_concentrations?: Record<string, number>;
    residual_error?: number;
    cost_total?: number;
    iterations?: number;
    convergence_time_ms?: number;
    ion_balance?: IonBalance;
    warnings?: string[];
    suggestions?: string[];
    is_successful: boolean;
    error_message?: string;
    created_at: string;
}

// ============================================================
// TYPE ALIASES
// ============================================================
export type ElementValues = Partial<Record<ElementName, number>>;
export type ElementList = ElementName[];
export type UnitType = Unit.PPM | Unit.MEQ | Unit.MMOL;
export type ThemeType = 'light' | 'dark';
export type LanguageType = 'fa' | 'en';

// ============================================================
// CONSTANTS AS TYPES
// ============================================================
export const ELEMENTS_LIST: ElementName[] = [
    ElementName.N_NO3,
    ElementName.P,
    ElementName.S,
    ElementName.N_NH4,
    ElementName.K,
    ElementName.Ca,
    ElementName.Mg,
    ElementName.Na,
    ElementName.Cl,
    ElementName.Fe,
    ElementName.Mn,
    ElementName.Zn,
    ElementName.B,
    ElementName.Cu,
    ElementName.Mo
];

export const WATER_ELEMENTS_LIST: string[] = [
    'N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo', 'EC', 'pH'
];

export const UNIT_OPTIONS: Unit[] = [Unit.PPM, Unit.MEQ, Unit.MMOL];

export const RESERVOIR_TYPES: ReservoirType[] = [
    ReservoirType.A,
    ReservoirType.B,
    ReservoirType.C
];

// ============================================================
// EDUCATION TYPES
// ============================================================
export interface FAQItem {
    id: string;
    question: string;
    answer: string;
    category: string;
    tags: string[];
    createdAt: Date;
    updatedAt: Date;
}

export interface QuickStartStep {
    id: string;
    title: string;
    description: string;
    details: string[];
    tips: string[];
    warnings: string[];
    order: number;
}

export interface EducationState {
    faqItems: FAQItem[];
    quickStartSteps: QuickStartStep[];
    searchQuery: string;
    activeCategory: string;
}

export const FAQ_CATEGORIES = [
    'همه',
    'پایگاه داده',
    'تنظیمات',
    'تغذیه',
    'گزارش',
    'عمومی',
    'محاسبات',
    'پشتیبانی'
];

export const QUICK_START_TOTAL_STEPS = 6;

// ============================================================
// AUTH TYPES
// ============================================================
export interface LoginCredentials {
    phone_number: string;
    password: string;
}

export interface RegisterData {
    first_name: string;
    last_name: string;
    phone_number: string;
    password: string;
}

export interface AuthResponse {
    access_token: string;
    token_type: string;
    expires_in: number;
}

export interface User {
    id: number;
    first_name: string;
    last_name: string;
    phone_number: string;
    is_active: boolean;
    created_at: string;
    updated_at?: string;
    full_name: string;
}


