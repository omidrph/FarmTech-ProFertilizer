<!-- frontend/src/components/features/PhCalculatorTab.vue -->
<!--
  تب «PH» — اصلاح pH با اسید/باز (ویزارد ۴ مرحله‌ای، هم‌سبک «محاسبه کود»)
  ------------------------------------------------------------
  سناریوی گلخانه: استوک ساخته و در مخزن اصلی ریخته شده؛ مقداری از محلول (نمونه، مثلاً ۵ لیتر)
  برداشته می‌شود، مرحله‌به‌مرحله اسید/باز می‌ریزیم و pH می‌خوانیم تا به هدف برسد؛ مقدار نهایی
  با نسبت حجم مخزن به نمونه به کل مخزن تعمیم می‌یابد.

    ۱) ماده و مخزن   ۲) نمونه و pH   ۳) آزمون   ۴) نتیجه

  اگر مقدار اسید/باز را از قبل می‌دانید، آن را در «محاسبه کود → انتخاب کود» وارد کنید.
  همه‌ی محاسبات در بک‌اند (app/core/ph_calculator) انجام می‌شود.
-->
<template>
  <div>

    <!-- ===================== نوار مراحل ===================== -->
    <nav class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-3 sm:p-4 mb-4">
      <ol class="flex items-stretch gap-1.5 sm:gap-2">
        <li v-for="(step, index) in steps" :key="step.id" class="flex items-start flex-1 min-w-0">
          <button
            type="button"
            @click="goToStep(step.id)"
            :disabled="!isStepReachable(step.id)"
            class="flex flex-col sm:flex-row items-center justify-center sm:justify-start gap-1 sm:gap-2 min-w-0 w-full text-center sm:text-right rounded-lg border px-2 py-2 sm:py-2.5 min-h-[52px] transition-colors disabled:cursor-not-allowed"
            :class="currentStep === step.id
              ? 'bg-primary-50 dark:bg-primary-900/20 border-primary-200 dark:border-primary-800 shadow-sm'
              : 'bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-700 hover:bg-gray-50 dark:hover:bg-gray-700/40 disabled:hover:bg-white dark:disabled:hover:bg-gray-800'"
          >
            <span class="w-7 h-7 sm:w-8 sm:h-8 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 transition-colors" :class="stepCircleClass(step.id)">
              <svg v-if="isStepDone(step.id)" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" /></svg>
              <template v-else>{{ index + 1 }}</template>
            </span>
            <span class="min-w-0">
              <span class="block text-[11px] sm:text-sm font-semibold truncate leading-tight" :class="currentStep === step.id ? 'text-primary-700 dark:text-primary-400' : 'text-gray-700 dark:text-gray-300'">{{ step.title }}</span>
              <span class="hidden sm:block text-[11px] text-gray-400 truncate">{{ step.subtitle }}</span>
            </span>
          </button>
          <span v-if="index < steps.length - 1" class="h-0.5 flex-1 mx-1 sm:mx-2 mt-3.5 sm:mt-4 rounded-full transition-colors" :class="isStepDone(step.id) ? 'bg-primary-500' : 'bg-gray-200 dark:bg-gray-700'"></span>
        </li>
      </ol>

      <!-- ناوبری در جای ثابت (بالا): قبلی | شروع دوباره | دکمهٔ اصلی هر مرحله -->
      <div class="mt-3 pt-3 border-t border-gray-100 dark:border-gray-700 flex items-center gap-2">
        <button type="button" @click="goToStep(currentStep - 1)" :disabled="currentStep === 1"
          class="inline-flex items-center gap-1.5 h-10 px-3 sm:px-4 text-sm font-medium rounded-lg border border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
          قبلی
        </button>
        <button type="button" @click="resetAll" class="inline-flex items-center gap-1.5 h-10 px-3 text-sm font-medium rounded-lg text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h5M20 20v-5h-5M5.6 15A8 8 0 0018.4 9M18.4 9A8 8 0 005.6 15" /></svg>
          <span class="hidden sm:inline">شروع دوباره</span>
        </button>
        <div class="flex-1"></div>
        <button v-if="currentStep === 1" type="button" @click="next1" class="primary-btn">ادامه: نمونه و pH <span aria-hidden="true">‹</span></button>
        <button v-else-if="currentStep === 2" type="button" @click="next2" class="primary-btn">ادامه: آزمون <span aria-hidden="true">‹</span></button>
        <button v-else-if="currentStep === 3" type="button" @click="calculate" :disabled="phStore.isCalculating" class="primary-btn">{{ phStore.isCalculating ? 'در حال محاسبه…' : 'محاسبه مقدار برای مخزن' }}</button>
        <button v-else type="button" @click="save" :disabled="!canSave" class="primary-btn">{{ phStore.isSaving ? 'در حال ثبت…' : 'ثبت و اعمال در محاسبه کود' }}</button>
      </div>
    </nav>

    <!-- تاریخچهٔ این گزارش (همیشه در ابتدا؛ قابل ویرایش و حذف) -->
    <PhHistoryPanel v-if="reportStore.hasActiveReport" class="mb-4" :items="phStore.history" @reuse="reuse" @apply="(id) => toggleApply(id, true)" @unapply="(id) => toggleApply(id, false)" @delete="onDelete" @update="onUpdate" />

    <!-- پیام‌های وضعیت گزارش -->
    <div v-if="!reportStore.hasActiveReport" class="mb-3 rounded-lg border border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20 px-3 py-2 text-xs leading-6 text-amber-800 dark:text-amber-200">
      گزارشی باز نیست؛ محاسبه کار می‌کند ولی ثبت در تاریخچه و اعمال در محاسبهٔ کود نیاز به یک گزارش دارد.
    </div>
    <div v-if="activeBanner" class="mb-3 rounded-lg border border-emerald-200 dark:border-emerald-800 bg-emerald-50 dark:bg-emerald-900/20 px-3 py-2 text-xs leading-6 text-emerald-800 dark:text-emerald-200">
      اصلاح فعال این گزارش: <strong>{{ activeBanner.chemical_name }}</strong> — {{ fmtDose(activeBanner.dose_tank, activeBanner.dose_unit) }} برای {{ fmt(activeBanner.tank_volume_l, 0) }} لیتر؛ در «محاسبه کود» لحاظ می‌شود.
    </div>

    <Transition name="step" mode="out-in">

      <!-- ===================== مرحله ۱: ماده و مخزن ===================== -->
      <div v-if="currentStep === 1" key="s1" class="space-y-4">
        <div class="grid grid-cols-1 lg:grid-cols-5 gap-4">
          <section class="lg:col-span-3 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-5 space-y-4">
            <header class="flex items-center gap-2">
              <span class="w-8 h-8 sm:w-10 sm:h-10 rounded-lg bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center flex-shrink-0">
                <svg class="w-4 h-4 sm:w-5 sm:h-5 text-amber-600 dark:text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3h6M10 3v6l-5 9a2 2 0 001.8 3h10.4a2 2 0 001.8-3l-5-9V3" /></svg>
              </span>
              <div class="min-w-0">
                <h3 class="text-base font-semibold text-gray-900 dark:text-white">اسید یا باز</h3>
                <p class="text-xs text-gray-500 dark:text-gray-400">از پایگاه‌داده کود شما</p>
              </div>
            </header>

            <p v-if="phStore.isLoadingAdjusters" class="text-sm text-gray-500">در حال بارگذاری…</p>
            <div v-else-if="phStore.adjusters.length === 0" class="rounded-xl border border-dashed border-gray-300 dark:border-gray-600 px-4 py-6 text-center">
              <p class="text-sm text-gray-700 dark:text-gray-200">هنوز اسید یا بازی در پایگاه‌داده کود شما ثبت نشده است.</p>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1 leading-6">از «پایگاه‌داده کود» یک اسید (مثل نیتریک) یا باز (مثل KOH) اضافه کنید و تیک «اسید است» یا «باز است» را بزنید.</p>
            </div>
            <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              <button
                v-for="opt in phStore.adjusters" :key="opt.fertilizer_id" type="button" @click="selectAdjuster(opt.fertilizer_id)"
                class="text-right rounded-xl border px-3 py-2.5 transition-colors"
                :class="form.fertilizerId === opt.fertilizer_id
                  ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 ring-1 ring-primary-500'
                  : 'border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-700'"
              >
                <span class="flex items-center gap-2">
                  <span class="text-[10px] px-1.5 py-0.5 rounded font-medium" :class="opt.kind === 'acid' ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300' : 'bg-sky-100 text-sky-700 dark:bg-sky-900/40 dark:text-sky-300'">{{ opt.kind === 'acid' ? 'اسید' : 'باز' }}</span>
                  <span class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ opt.name }}</span>
                </span>
                <span class="block text-[11px] text-gray-500 dark:text-gray-400 mt-1">
                  خلوص {{ fmt(opt.concentration, 1) }}٪ · مصرف به {{ opt.dose_unit === 'ml' ? 'میلی‌لیتر' : 'گرم' }}
                </span>
              </button>
            </div>

            <div v-if="selected && selected.warnings.length" class="space-y-1.5">
              <div v-for="(w, i) in selected.warnings" :key="i" class="rounded-lg border border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20 px-3 py-2 text-xs leading-6 text-amber-800 dark:text-amber-200">{{ w }}</div>
            </div>

            <div class="pt-1">
              <label class="field-label">حجم مخزن اصلی (لیتر)</label>
              <input v-model="form.tankVolume" inputmode="decimal" class="field-input" :class="{ 'field-invalid': touched1 && !isPos(form.tankVolume) }" placeholder="مثلاً ۵۰۰۰" />
              <p v-if="phStore.context?.tank_volume_l" class="text-[11px] text-gray-400 mt-1">از محاسبهٔ کود این گزارش برداشته شد؛ در صورت نیاز تغییر دهید.</p>
            </div>
          </section>

          <div class="lg:col-span-2">
            <PhSchematic :tank-volume="num(form.tankVolume)" :kind="selected?.kind ?? null" caption="مخزن اصلی که استوک در آن ریخته شده است" />
          </div>
        </div>
      </div>

      <!-- ===================== مرحله ۲: نمونه و pH ===================== -->
      <div v-else-if="currentStep === 2" key="s2" class="space-y-4">
        <div class="grid grid-cols-1 lg:grid-cols-5 gap-4">
          <section class="lg:col-span-3 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-5 space-y-4">
            <header class="flex items-center gap-2">
              <span class="w-8 h-8 sm:w-10 sm:h-10 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
                <svg class="w-4 h-4 sm:w-5 sm:h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16l-2 11a2 2 0 01-2 1.7H8A2 2 0 016 19L4 8zm2-3h12" /></svg>
              </span>
              <div class="min-w-0">
                <h3 class="text-base font-semibold text-gray-900 dark:text-white">نمونه و pH</h3>
                <p class="text-xs text-gray-500 dark:text-gray-400">مقداری از محلول مخزن را در یک سطل بردارید</p>
              </div>
            </header>

            <div>
              <label class="field-label">حجم نمونه (لیتر)</label>
              <div class="flex flex-wrap items-center gap-2">
                <input v-model="form.sampleVolume" inputmode="decimal" class="field-input !w-32" :class="{ 'field-invalid': touched2 && !isPos(form.sampleVolume) }" placeholder="۵" />
                <button v-for="v in samplePresets" :key="v" type="button" @click="form.sampleVolume = String(v)"
                  class="h-[42px] px-3 rounded-lg border text-xs font-medium transition-colors"
                  :class="num(form.sampleVolume) === v ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300' : 'border-gray-200 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700/50'">
                  {{ fmt(v) }} لیتر
                </button>
              </div>
              <p class="text-[11px] text-gray-500 dark:text-gray-400 mt-1.5 leading-5">نمونهٔ بزرگ‌تر دقت بیشتری می‌دهد، چون خطای کوچک اندازه‌گیری در مخزن چند برابر نمی‌شود.</p>
              <p v-if="scale" class="mt-2 text-xs text-gray-600 dark:text-gray-300">ضریب مقیاس‌دهی به مخزن: <strong class="tabular-nums text-gray-900 dark:text-white">×{{ fmt(scale, scale < 10 ? 1 : 0) }}</strong></p>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label class="field-label">pH فعلی محلول (در نمونه)</label>
                <input v-model="form.initialPh" inputmode="decimal" class="field-input" :class="{ 'field-invalid': touched2 && !phOk(form.initialPh) }" placeholder="مثلاً ۷٫۸" />
              </div>
              <div>
                <label class="field-label">pH هدف</label>
                <input v-model="form.targetPh" inputmode="decimal" class="field-input" :class="{ 'field-invalid': touched2 && !phOk(form.targetPh) }" placeholder="مثلاً ۶٫۰" />
                <p v-if="phRangeText" class="text-[11px] text-gray-400 mt-1">بازهٔ مطلوب معمول: {{ phRangeText }}</p>
              </div>
            </div>

            <div v-if="directionWarning" class="rounded-lg border border-rose-200 dark:border-rose-800 bg-rose-50 dark:bg-rose-900/20 px-3 py-2 text-xs leading-6 text-rose-800 dark:text-rose-200">{{ directionWarning }}</div>
          </section>

          <div class="lg:col-span-2">
            <PhSchematic :tank-volume="num(form.tankVolume)" :sample-volume="num(form.sampleVolume)" :scale="scale" :ph="num(form.initialPh)" :target-ph="num(form.targetPh)" :kind="selected?.kind ?? null" caption="نمونه را از مخزن اصلی بردارید و pH آن را بخوانید" />
          </div>
        </div>
      </div>

      <!-- ===================== مرحله ۳: آزمون ===================== -->
      <div v-else-if="currentStep === 3" key="s3" class="space-y-4">
        <div class="grid grid-cols-1 lg:grid-cols-5 gap-4">
          <section class="lg:col-span-3 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-5 space-y-4">
            <header class="flex items-center gap-2">
              <span class="w-8 h-8 sm:w-10 sm:h-10 rounded-lg bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center flex-shrink-0">
                <svg class="w-4 h-4 sm:w-5 sm:h-5 text-emerald-600 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3.5s6 6.2 6 10.5a6 6 0 11-12 0c0-4.3 6-10.5 6-10.5z" /></svg>
              </span>
              <div class="min-w-0">
                <h3 class="text-base font-semibold text-gray-900 dark:text-white">آزمون روی نمونه</h3>
                <p class="text-xs text-gray-500 dark:text-gray-400">کمی {{ unitWord }} بریزید، هم بزنید، pH را بخوانید و ثبت کنید</p>
              </div>
            </header>

            <!-- وضعیت لحظه‌ای -->
            <div class="grid grid-cols-3 gap-2 text-center">
              <div class="rounded-lg border border-gray-200 dark:border-gray-700 p-2">
                <p class="text-[11px] text-gray-500 dark:text-gray-400">pH فعلی</p>
                <p class="text-base font-bold tabular-nums" :class="phStatusClass">{{ latestPh != null ? fmt(latestPh, 2) : '—' }}</p>
              </div>
              <div class="rounded-lg border border-gray-200 dark:border-gray-700 p-2">
                <p class="text-[11px] text-gray-500 dark:text-gray-400">هدف</p>
                <p class="text-base font-bold tabular-nums text-gray-900 dark:text-white">{{ fmt(num(form.targetPh) ?? 0, 2) }}</p>
              </div>
              <div class="rounded-lg border border-gray-200 dark:border-gray-700 p-2">
                <p class="text-[11px] text-gray-500 dark:text-gray-400">مصرف تاکنون</p>
                <p class="text-base font-bold tabular-nums text-gray-900 dark:text-white">{{ fmt(cumulative, 2) }} <span class="text-[10px] font-normal text-gray-400">{{ unitShort }}</span></p>
              </div>
            </div>

            <div v-if="nextHint" class="rounded-lg bg-primary-50/70 dark:bg-primary-900/10 border border-primary-200 dark:border-primary-800 px-3 py-2 text-xs leading-6 text-primary-800 dark:text-primary-200">{{ nextHint }}</div>

            <!-- مراحل -->
            <div class="space-y-2">
              <div v-for="(row, i) in form.steps" :key="row.id" class="grid grid-cols-[1.5rem_1fr_1fr_auto] gap-2 items-center">
                <span class="text-[11px] text-gray-400 text-center tabular-nums">{{ fmt(i + 1) }}</span>
                <div class="relative">
                  <input v-model="row.amount" inputmode="decimal" class="field-input !pl-11" :class="{ 'field-invalid': touched3 && rowInvalid(row, true) }" :placeholder="`اضافه شد (${unitShort})`" />
                  <span class="absolute left-3 top-1/2 -translate-y-1/2 text-[11px] text-gray-400">{{ unitShort }}</span>
                </div>
                <input v-model="row.ph" inputmode="decimal" class="field-input" :class="{ 'field-invalid': touched3 && rowInvalid(row, true) }" placeholder="pH بعد از افزودن" />
                <button type="button" @click="removeStep(row.id)" :disabled="form.steps.length === 1" class="w-8 h-8 rounded-lg text-gray-400 hover:text-rose-500 disabled:opacity-30" aria-label="حذف مرحله">✕</button>
              </div>
            </div>
            <div class="flex items-center justify-between">
              <button type="button" @click="addStep" :disabled="form.steps.length >= MAX_STEPS" class="text-xs font-medium text-primary-600 dark:text-primary-400 disabled:opacity-40">+ مرحلهٔ بعد</button>
              <span class="text-[11px] text-gray-400">مقدار هر مرحله «اضافه‌شده در همان مرحله» است</span>
            </div>

            <details v-if="livePoints.length >= 2 && num(form.targetPh) != null" class="group rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-900/20">
              <summary class="cursor-pointer select-none px-3 py-2.5 text-sm font-medium text-gray-700 dark:text-gray-200 flex items-center justify-between">
                نمودار منحنی pH
                <svg class="w-4 h-4 transition-transform group-open:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
              </summary>
              <div class="px-2 pb-2"><PhCurveChart :points="livePoints" :target-ph="num(form.targetPh) as number" :unit-label="unitShort" /></div>
            </details>
          </section>

          <div class="lg:col-span-2 space-y-4">
            <PhSchematic :tank-volume="num(form.tankVolume)" :sample-volume="num(form.sampleVolume)" :scale="scale" :ph="latestPh" :target-ph="num(form.targetPh)" :kind="selected?.kind ?? null" :show-dropper="true" caption="اسید/باز را کم‌کم و همراه با هم‌زدن اضافه کنید" />
            <details v-if="selected && selected.dose_unit === 'ml'" class="rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 py-3">
              <summary class="cursor-pointer text-xs font-medium text-gray-600 dark:text-gray-300 select-none">چگالی دقیق ماده (اختیاری)</summary>
              <div class="mt-2">
                <input v-model="form.density" inputmode="decimal" class="field-input" :placeholder="selected.density_g_ml ? `ثبت‌شده/مرجع: ${fmt(selected.density_g_ml, 3)} g/mL` : 'از برگهٔ مشخصات (SDS)'" />
                <p class="text-[11px] text-gray-500 dark:text-gray-400 mt-1.5 leading-5">فقط برای تبدیل میلی‌لیتر به گرم و محاسبهٔ عناصر واردشده است. بهتر است آن را یک‌بار در پایگاه‌داده کود ثبت کنید.</p>
              </div>
            </details>
          </div>
        </div>
      </div>

      <!-- ===================== مرحله ۴: نتیجه ===================== -->
      <div v-else key="s4" class="space-y-4">
        <div v-if="phStore.errorMessage" ref="errorRef" role="alert" class="rounded-xl border border-rose-200 dark:border-rose-800 bg-rose-50 dark:bg-rose-900/20 px-4 py-3">
          <p class="text-sm text-rose-800 dark:text-rose-200 leading-6">{{ phStore.errorMessage }}</p>
          <button type="button" @click="goToStep(3)" class="mt-2 text-xs font-medium text-rose-700 dark:text-rose-300 underline">بازگشت به آزمون</button>
        </div>

        <template v-if="phStore.result">
          <div class="grid grid-cols-1 lg:grid-cols-5 gap-4">
            <div class="lg:col-span-3 space-y-4">
              <PhResultPanel :result="phStore.result" />
            </div>
            <div class="lg:col-span-2 space-y-4">
              <PhSchematic :tank-volume="phStore.result.tank_volume_l" :sample-volume="phStore.result.sample_volume_l ?? null" :scale="phStore.result.scale_factor ?? null" :ph="phStore.result.final_ph ?? null" :target-ph="phStore.result.target_ph ?? null" :kind="phStore.result.kind" :dose-label="doseLabel" caption="مقدار نهایی را مرحله‌ای در مخزن اصلی بریزید و pH را بخوانید" />

              <section class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 space-y-3">
                <h3 class="text-sm font-semibold text-gray-900 dark:text-white">ثبت این اصلاح</h3>
                <div>
                  <label class="field-label">یادداشت (اختیاری)</label>
                  <input v-model="saveForm.note" maxlength="500" class="field-input" placeholder="مثلاً: آب چاه، ساخت دوم" />
                </div>
                <div class="grid grid-cols-2 gap-2">
                  <div>
                    <label class="field-label">EC قبل (اختیاری)</label>
                    <input v-model="saveForm.ecBefore" inputmode="decimal" class="field-input" placeholder="dS/m" />
                  </div>
                  <div>
                    <label class="field-label">EC بعد (اختیاری)</label>
                    <input v-model="saveForm.ecAfter" inputmode="decimal" class="field-input" placeholder="dS/m" />
                  </div>
                </div>
                <p class="text-[11px] text-gray-500 dark:text-gray-400 leading-5">با دکمهٔ «ثبت و اعمال در محاسبه کود» (بالای صفحه) نتیجه ثبت می‌شود و مستقیماً در محاسبه کود اعمال می‌گردد؛ یعنی عناصر این اسید/باز مثل آب منبع پایه لحاظ شوند: سهم کودهای دیگر کم می‌شود و تعادل یونی و EC دوباره محاسبه می‌گردد. در هر گزارش فقط یک اصلاح فعال است.</p>
                <p v-if="!reportStore.hasActiveReport" class="text-[11px] text-amber-700 dark:text-amber-300">برای ثبت، ابتدا یک گزارش باز یا ذخیره کنید.</p>
                <p v-if="saveError" class="text-xs text-rose-600 dark:text-rose-400">{{ saveError }}</p>
                <p v-if="saveMessage" class="text-xs text-emerald-700 dark:text-emerald-300">{{ saveMessage }}</p>
              </section>
            </div>
          </div>
        </template>

      </div>
    </Transition>

  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, nextTick, onMounted } from 'vue';
import { usePhStore } from '@/store/modules/phStore';
import { useReportStore } from '@/store/modules/reportStore';
import type { PhAdjustmentItem, PhAdjustmentRequest } from '@/services/apiService';
import { parseNum, fmt, fmtDose } from './ph/phFormat';
import PhResultPanel from './ph/PhResultPanel.vue';
import PhCurveChart from './ph/PhCurveChart.vue';
import PhHistoryPanel from './ph/PhHistoryPanel.vue';
import PhSchematic from './ph/PhSchematic.vue';

const emit = defineEmits<{ (e: 'applied', id: number): void }>();
const MAX_STEPS = 30;
const samplePresets = [5, 10, 20];

const phStore = usePhStore();
const reportStore = useReportStore();

// ===== مراحل =====
type StepId = 1 | 2 | 3 | 4;
const steps: Array<{ id: StepId; title: string; subtitle: string }> = [
  { id: 1, title: 'ماده و مخزن', subtitle: 'اسید/باز و حجم مخزن' },
  { id: 2, title: 'نمونه و pH', subtitle: 'نمونه، pH فعلی و هدف' },
  { id: 3, title: 'آزمون', subtitle: 'افزودن مرحله‌ای و خواندن pH' },
  { id: 4, title: 'نتیجه', subtitle: 'مقدار مخزن و ثبت' }
];
const currentStep = ref<StepId>(1);
const touched1 = ref(false);
const touched2 = ref(false);
const touched3 = ref(false);

// ===== فرم =====
let rowSeq = 0;
const newStep = () => ({ id: ++rowSeq, amount: '', ph: '' });
const defaultForm = () => ({
  fertilizerId: null as number | null,
  tankVolume: '',
  sampleVolume: '5',
  initialPh: '',
  targetPh: '',
  steps: [newStep(), newStep()],
  density: ''
});
const form = reactive(defaultForm());
const saveForm = reactive({ note: '', ecBefore: '', ecAfter: '' });
const saveMessage = ref('');
const stale = ref(false);
const errorRef = ref<HTMLElement | null>(null);

// ===== کمکی =====
const num = (v: string | number | null | undefined): number | null =>
  v === null || v === undefined ? null : typeof v === 'number' ? v : parseNum(v);
const isPos = (v: string): boolean => {
  const n = parseNum(v);
  return n !== null && n > 0;
};
const phOk = (v: string): boolean => {
  const n = parseNum(v);
  return n !== null && n >= 0 && n <= 14;
};
const rowInvalid = (r: { amount: string; ph: string }, strict = false): boolean => {
  const empty = r.amount.trim() === '' && r.ph.trim() === '';
  if (empty) return strict ? false : false;
  const a = parseNum(r.amount);
  return !(a !== null && a > 0 && phOk(r.ph));
};

// ===== مشتقات =====
const selected = computed(() => phStore.adjusters.find((a) => a.fertilizer_id === form.fertilizerId) || null);
const unitShort = computed(() => (selected.value?.dose_unit === 'g' ? 'g' : 'mL'));
const unitWord = computed(() => (selected.value?.kind === 'base' ? 'باز' : 'اسید'));
const activeBanner = computed(() => phStore.context?.active || null);
const phRangeText = computed(() => {
  const r = phStore.context?.target_ph_range;
  return r && r.length === 2 ? `${fmt(r[0], 1)} تا ${fmt(r[1], 1)}` : '';
});
const scale = computed(() => {
  const t = num(form.tankVolume);
  const s = num(form.sampleVolume);
  return t && s && t > 0 && s > 0 ? t / s : null;
});

const directionWarning = computed(() => {
  const i = num(form.initialPh);
  const t = num(form.targetPh);
  const kind = selected.value?.kind;
  if (i == null || t == null || !kind) return '';
  if (Math.abs(i - t) < 1e-9) return 'pH فعلی و هدف یکسان‌اند؛ اصلاحی لازم نیست.';
  if (t < i && kind === 'base') return 'برای کاهش pH باید «اسید» انتخاب کنید؛ به مرحلهٔ ۱ برگردید.';
  if (t > i && kind === 'acid') return 'برای افزایش pH باید «باز» انتخاب کنید؛ به مرحلهٔ ۱ برگردید.';
  return '';
});

const validRows = computed(() =>
  form.steps
    .map((r) => ({ amount: parseNum(r.amount), ph: parseNum(r.ph) }))
    .filter((r) => r.amount !== null && (r.amount as number) > 0 && r.ph !== null && r.ph >= 0 && r.ph <= 14) as Array<{ amount: number; ph: number }>
);

const livePoints = computed(() => {
  const init = num(form.initialPh);
  if (init == null) return [];
  const pts = [{ amount: 0, ph: init }];
  let total = 0;
  for (const r of form.steps) {
    const a = parseNum(r.amount);
    const p = parseNum(r.ph);
    if (a == null || a <= 0 || p == null) break;
    total += a;
    pts.push({ amount: total, ph: p });
  }
  return pts;
});
const latestPh = computed(() => (livePoints.value.length ? livePoints.value[livePoints.value.length - 1].ph : num(form.initialPh)));
const cumulative = computed(() => (livePoints.value.length ? livePoints.value[livePoints.value.length - 1].amount : 0));

const phStatusClass = computed(() => {
  const p = latestPh.value;
  const t = num(form.targetPh);
  if (p == null || t == null) return 'text-gray-900 dark:text-white';
  const d = Math.abs(p - t);
  return d <= 0.1 ? 'text-emerald-600 dark:text-emerald-400' : d <= 0.5 ? 'text-amber-600 dark:text-amber-400' : 'text-gray-900 dark:text-white';
});

/** پیشنهاد مقدار مرحلهٔ بعد: از شیب دو نقطهٔ آخر (محافظه‌کارانه تا از هدف رد نشود) */
const nextHint = computed(() => {
  const t = num(form.targetPh);
  const pts = livePoints.value;
  if (t == null || pts.length === 0) return '';
  const last = pts[pts.length - 1];
  const kind = selected.value?.kind;
  if (pts.length === 1) return `با مقدار کم شروع کنید (مثلاً ۱ ${unitShort.value} برای نمونه) و بعد از هم‌زدن pH را بخوانید.`;
  const overshoot = kind === 'acid' ? last.ph < t - 0.05 : kind === 'base' ? last.ph > t + 0.05 : false;
  if (overshoot) return 'pH از هدف رد شده است. می‌توانید همین داده‌ها را محاسبه کنید (مقدار با میان‌یابی تخمین زده می‌شود) یا یک نمونهٔ تازه بیازمایید.';
  if (Math.abs(last.ph - t) <= 0.1) return 'به هدف رسیدید. می‌توانید «محاسبه مقدار برای مخزن» را بزنید.';
  const prev = pts[pts.length - 2];
  const slope = (last.ph - prev.ph) / (last.amount - prev.amount);
  if (!Number.isFinite(slope) || Math.abs(slope) < 1e-9) return '';
  const remaining = (t - last.ph) / slope;
  if (!(remaining > 0)) return '';
  const suggested = Math.max(remaining * (Math.abs(last.ph - t) > 0.4 ? 0.6 : 0.9), 0);
  return `برای مرحلهٔ بعد حدود ${fmt(suggested, 2)} ${unitShort.value} اضافه کنید (تخمین از شیب قبلی؛ منحنی pH خطی نیست، پس محتاطانه است).`;
});

const doseLabel = computed(() => (phStore.result ? fmtDose(phStore.result.dose_tank, phStore.result.dose_unit) : ''));
const canSave = computed(() => !!phStore.result && !stale.value && reportStore.hasActiveReport && !phStore.isSaving);

// ===== ناوبری مراحل =====
const step1Done = computed(() => !!form.fertilizerId && isPos(form.tankVolume));
const step2Done = computed(() => step1Done.value && isPos(form.sampleVolume) && phOk(form.initialPh) && phOk(form.targetPh) && !directionWarning.value);
const step3Done = computed(() => !!phStore.result && !stale.value);

const isStepDone = (id: StepId): boolean => (id === 1 ? step1Done.value && currentStep.value > 1 : id === 2 ? step2Done.value && currentStep.value > 2 : id === 3 ? step3Done.value : step3Done.value && currentStep.value === 4);
const isStepReachable = (id: StepId): boolean => {
  if (id === 1) return true;
  if (id === 2) return step1Done.value;
  if (id === 3) return step2Done.value;
  return !!phStore.result;
};
const stepCircleClass = (id: StepId): string => {
  if (isStepDone(id)) return 'bg-emerald-500 text-white';
  if (currentStep.value === id) return 'bg-primary-600 text-white';
  return 'bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400';
};
const goToStep = (id: number) => {
  const target = id as StepId;
  if (!isStepReachable(target)) return;
  currentStep.value = target;
  nextTick(() => typeof window !== 'undefined' && window.scrollTo({ top: 0, behavior: 'smooth' }));
};

const next1 = () => {
  touched1.value = true;
  if (!form.fertilizerId) {
    phStore.errorMessage = 'ابتدا اسید یا باز را انتخاب کنید.';
    return;
  }
  phStore.errorMessage = null;
  if (step1Done.value) goToStep(2);
};
const next2 = () => {
  touched2.value = true;
  if (step2Done.value) goToStep(3);
};

// ===== اقدامات =====
function selectAdjuster(id: number) {
  form.fertilizerId = id;
  form.density = '';
  phStore.errorMessage = null;
}
function addStep() {
  if (form.steps.length < MAX_STEPS) form.steps.push(newStep());
}
function removeStep(id: number) {
  if (form.steps.length > 1) form.steps.splice(form.steps.findIndex((r) => r.id === id), 1);
}

function buildPayload(): PhAdjustmentRequest | null {
  const tank = num(form.tankVolume);
  const sample = num(form.sampleVolume);
  const initial = num(form.initialPh);
  const target = num(form.targetPh);
  if (!form.fertilizerId || !tank || !sample || initial == null || target == null) {
    phStore.errorMessage = 'مراحل قبل را کامل کنید.';
    return null;
  }
  const filled = form.steps.filter((r) => r.amount.trim() !== '' || r.ph.trim() !== '');
  if (filled.length === 0 || filled.some((r) => rowInvalid(r))) {
    touched3.value = true;
    phStore.errorMessage = 'هر مرحله باید هم مقدار (بزرگ‌تر از صفر) و هم pH معتبر داشته باشد.';
    return null;
  }
  return {
    mode: 'trial',
    fertilizer_id: form.fertilizerId,
    tank_volume_l: tank,
    initial_ph: initial,
    target_ph: target,
    density_g_ml: num(form.density),
    sample_volume_l: sample,
    steps: filled.map((r) => ({ amount: parseNum(r.amount) as number, ph: parseNum(r.ph) as number }))
  };
}

async function calculate() {
  touched3.value = true;
  phStore.errorMessage = null;
  saveMessage.value = '';
  const payload = buildPayload();
  if (!payload) return;
  const ok = await phStore.calculate(payload);
  stale.value = false;
  currentStep.value = 4;
  await nextTick();
  if (!ok) errorRef.value?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  else if (typeof window !== 'undefined') window.scrollTo({ top: 0, behavior: 'smooth' });
}

const saveError = ref('');
async function save() {
  saveError.value = '';
  const payload = buildPayload();
  if (!payload) return;
  const item = await phStore.save({
    ...payload,
    note: saveForm.note.trim() || null,
    ec_before: num(saveForm.ecBefore),
    ec_after: num(saveForm.ecAfter),
    apply: true
  });
  if (item) {
    phStore.pendingRecalc = true;       // صفحهٔ محاسبه کود یک‌بار خودکار دوباره محاسبه می‌کند
    emit('applied', item.id);            // رفتن به «محاسبه کود»
  } else {
    saveError.value = phStore.errorMessage || 'ثبت انجام نشد.';
  }
}

async function toggleApply(id: number, applied: boolean) {
  const ok = await phStore.setApplied(id, applied);
  if (ok) saveMessage.value = applied ? 'اعمال شد؛ در «محاسبه کود» دوباره «محاسبه» را بزنید.' : 'اعمال لغو شد؛ محاسبهٔ بعدی بدون آن انجام می‌شود.';
}
async function onUpdate(id: number, data: { note: string | null; ec_before: number | null; ec_after: number | null }) {
  await phStore.updateMeta(id, data);
}
async function onDelete(id: number) {
  await phStore.remove(id);
}

function reuse(item: PhAdjustmentItem) {
  if (item.mode !== 'trial') return;
  Object.assign(form, defaultForm());
  form.fertilizerId = item.fertilizer_id ?? null;
  form.tankVolume = String(item.tank_volume_l);
  form.sampleVolume = item.sample_volume_l != null ? String(item.sample_volume_l) : '5';
  form.initialPh = item.initial_ph != null ? String(item.initial_ph) : '';
  form.targetPh = item.target_ph != null ? String(item.target_ph) : '';
  form.steps = (item.trial_steps || []).map((s) => ({ id: ++rowSeq, amount: String(s.amount), ph: String(s.ph) }));
  if (form.steps.length === 0) form.steps = [newStep()];
  phStore.clearResult();
  currentStep.value = 3;
  if (typeof window !== 'undefined') window.scrollTo({ top: 0, behavior: 'smooth' });
}

function resetAll() {
  const keepTank = form.tankVolume;
  const keepFert = form.fertilizerId;
  Object.assign(form, defaultForm());
  form.tankVolume = keepTank;
  form.fertilizerId = keepFert;
  form.targetPh = phStore.context ? String(phStore.context.suggested_target_ph) : '';
  saveForm.note = saveForm.ecBefore = saveForm.ecAfter = '';
  touched1.value = touched2.value = touched3.value = false;
  stale.value = false;
  saveMessage.value = '';
  phStore.clearResult();
  currentStep.value = 1;
}

// تغییر ورودی‌ها بعد از محاسبه → نتیجهٔ قبلی قدیمی می‌شود
watch(() => JSON.stringify(form), () => {
  if (phStore.result) stale.value = true;
  saveMessage.value = '';
});

function prefillFromContext() {
  const ctx = phStore.context;
  if (!ctx) return;
  if (!form.tankVolume && ctx.tank_volume_l) form.tankVolume = String(ctx.tank_volume_l);
  if (!form.targetPh) form.targetPh = String(ctx.suggested_target_ph);
}

onMounted(async () => {
  phStore.clearResult();
  await phStore.refreshAll();
  prefillFromContext();
});

watch(() => reportStore.currentReportId, async () => {
  phStore.reset();
  form.tankVolume = '';
  form.targetPh = '';
  currentStep.value = 1;
  await phStore.refreshAll();
  prefillFromContext();
});
</script>

<style scoped>
.field-label { @apply block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1.5; }
.field-input {
  @apply w-full px-3 py-2.5 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition;
}
.field-invalid { @apply border-rose-400 dark:border-rose-500 bg-rose-50/60 dark:bg-rose-900/10; }
.primary-btn { @apply inline-flex items-center gap-1.5 h-10 px-4 sm:px-5 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg transition-colors; }
.tabular-nums { font-variant-numeric: tabular-nums; }
.step-enter-active, .step-leave-active { transition: opacity .18s ease, transform .18s ease; }
.step-enter-from { opacity: 0; transform: translateY(6px); }
.step-leave-to { opacity: 0; transform: translateY(-6px); }
</style>
