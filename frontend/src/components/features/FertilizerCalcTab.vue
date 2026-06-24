<template>
  <div class="space-y-6">
    <!-- ============================================================ -->
    <!-- هدر با توضیحات (بدون آیکون) -->
    <!-- ============================================================ -->
    <div class="bg-primary-50 dark:bg-primary-900/20 border-r-4 border-primary-500 rounded-lg p-4">
      <p class="text-gray-700 dark:text-gray-300 text-sm leading-relaxed">
        کودهای مورد نظر خود را انتخاب کرده و تنظیمات استوک را وارد کنید. نرم‌افزار مقدار دقیق کود برای ساخت محلول استوک را محاسبه می‌کند.
      </p>
    </div>

    <!-- ============================================================ -->
    <!-- بخش تنظیمات استوک (مهم‌ترین بخش) -->
    <!-- ============================================================ -->
    <div class="bg-gradient-to-br from-primary-50 to-white dark:from-primary-900/20 dark:to-gray-800 rounded-xl shadow-sm border border-primary-200 dark:border-primary-800 p-5">
      <div class="flex items-center gap-2 mb-4">
        <div class="w-10 h-10 rounded-lg bg-primary-500 text-white flex items-center justify-center">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
          </svg>
        </div>
        <div>
          <h3 class="text-base font-bold text-gray-900 dark:text-white">تنظیمات استوک (Stock Solution)</h3>
          <p class="text-xs text-gray-500 dark:text-gray-400">محاسبه مقدار کود برای ساخت محلول استوک غلیظ</p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- حجم مخزن اصلی -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
            <div class="flex items-center gap-1.5">
              <svg class="w-4 h-4 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/>
              </svg>
              حجم مخزن اصلی (لیتر)
            </div>
          </label>
          <input
            type="number"
            v-model.number="mainTankVolume"
            min="1"
            class="w-full px-3 py-2.5 border-2 border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
            placeholder="مثال: 10000"
          />
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">حجم کل محلول نهایی در مخزن اصلی</p>
        </div>

        <!-- حجم استوک -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
            <div class="flex items-center gap-1.5">
              <svg class="w-4 h-4 text-success-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
              </svg>
              حجم مخزن استوک (لیتر)
            </div>
          </label>
          <input
            type="number"
            v-model.number="stockVolume"
            min="1"
            class="w-full px-3 py-2.5 border-2 border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
            placeholder="مثال: 100"
          />
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">حجم محلول استوک غلیظ که می‌سازید</p>
        </div>

        <!-- نسبت تزریق -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
            <div class="flex items-center gap-1.5">
              <svg class="w-4 h-4 text-warning-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
              نسبت تزریق (Proportional)
            </div>
          </label>
          <div class="flex gap-2">
            <input
              type="number"
              v-model.number="injectionRatio"
              min="1"
              class="flex-1 px-3 py-2.5 border-2 border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
              placeholder="100"
            />
            <span class="flex items-center px-3 text-gray-500 dark:text-gray-400 text-sm">:1</span>
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">1 لیتر استوک → {{ injectionRatio }} لیتر محلول نهایی</p>
        </div>
      </div>

      <!-- نمایش ضریب غلظت محاسبه شده -->
      <div class="mt-4 p-3 bg-white dark:bg-gray-700/50 rounded-lg border border-primary-200 dark:border-primary-700">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div class="flex items-center gap-2">
            <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
            </svg>
            <span class="text-sm font-medium text-gray-700 dark:text-gray-300">ضریب غلظت استوک:</span>
          </div>
          <span class="text-2xl font-bold text-primary-600 dark:text-primary-400 tabular-nums">
            {{ concentrationFactor.toFixed(2) }}×
          </span>
          <div class="text-xs text-gray-500 dark:text-gray-400">
            ({{ mainTankVolume }} ÷ {{ stockVolume }} × {{ injectionRatio }})
          </div>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- بخش انتخاب کود -->
    <!-- ============================================================ -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center gap-2">
          <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
          </svg>
          <h3 class="text-base font-semibold text-gray-900 dark:text-white">انتخاب کود</h3>
        </div>
        <div class="flex items-center gap-2">
          <button
            @click="toggleSelectAll"
            class="px-3 py-1.5 text-xs bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 rounded-lg hover:bg-primary-200 dark:hover:bg-primary-900/50 transition-colors font-medium"
          >
            {{ isAllSelected ? 'لغو انتخاب همه' : 'انتخاب همه' }}
          </button>
          <span class="text-xs text-gray-500 dark:text-gray-400">
            {{ selectedFertilizers.length }} از {{ fertilizers.length }} کود
          </span>
        </div>
      </div>

      <!-- جستجو در لیست کودها -->
      <div class="relative mb-4">
        <svg class="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
        <input
          v-model="fertilizerSearchQuery"
          type="text"
          placeholder="جستجوی نام کود یا برند..."
          class="w-full pr-10 pl-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
        />
      </div>

      <!-- لیست کودها (Grid) -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 max-h-[350px] overflow-y-auto custom-scrollbar p-1">
        <div
          v-for="fertilizer in filteredFertilizersForSelection"
          :key="fertilizer.id"
          @click="toggleFertilizerSelection(fertilizer.id)"
          class="relative cursor-pointer rounded-lg border-2 p-3 transition-all hover:shadow-md"
          :class="selectedFertilizers.includes(fertilizer.id)
            ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 shadow-sm'
            : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:border-primary-300 dark:hover:border-primary-700'"
        >
          <!-- Checkbox -->
          <div class="absolute top-2 left-2">
            <div
              class="w-5 h-5 rounded border-2 flex items-center justify-center transition-all"
              :class="selectedFertilizers.includes(fertilizer.id)
                ? 'bg-primary-500 border-primary-500'
                : 'bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600'"
            >
              <svg
                v-if="selectedFertilizers.includes(fertilizer.id)"
                class="w-3 h-3 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/>
              </svg>
            </div>
          </div>

          <!-- محتوا -->
          <div class="pr-6">
            <p class="font-medium text-sm text-gray-900 dark:text-white truncate">
              {{ fertilizer.name }}
            </p>
            <div class="flex items-center gap-2 mt-1 flex-wrap">
              <span
                class="text-[10px] px-1.5 py-0.5 rounded"
                :class="fertilizer.isAcid
                  ? 'bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400'
                  : 'bg-success-100 dark:bg-success-900/30 text-success-700 dark:text-success-400'"
              >
                {{ fertilizer.isAcid ? 'اسید' : 'کود' }}
              </span>
              <span v-if="fertilizer.brand" class="text-[10px] text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-700 px-1.5 py-0.5 rounded">
                {{ fertilizer.brand }}
              </span>
              <span class="text-[10px] text-gray-500 dark:text-gray-400">
                {{ Number(fertilizer.pricePerKg || 0).toLocaleString('fa-IR') }} تومان/kg
              </span>
            </div>
            <!-- عناصر اصلی -->
            <div v-if="getMainElements(fertilizer).length > 0" class="flex flex-wrap gap-1 mt-2">
              <span
                v-for="el in getMainElements(fertilizer)"
                :key="el.symbol"
                class="text-[9px] px-1.5 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded"
              >
                {{ el.symbol }}: {{ el.value }}%
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- پیام خالی بودن -->
      <div v-if="filteredFertilizersForSelection.length === 0" class="text-center py-8">
        <svg class="w-12 h-12 mx-auto text-gray-300 dark:text-gray-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
        </svg>
        <p class="text-sm text-gray-500 dark:text-gray-400">هیچ کودی یافت نشد</p>
      </div>

      <!-- دکمه افزودن به جدول -->
      <div class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
        <button
          @click="addSelectedFertilizersToTable"
          :disabled="selectedFertilizers.length === 0"
          class="w-full px-4 py-2.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors flex items-center justify-center gap-2 shadow-sm hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
          افزودن به جدول محاسبه ({{ selectedFertilizers.length }} کود)
        </button>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- جدول محاسبه استوک -->
    <!-- ============================================================ -->
    <div v-if="calcRows.length > 0" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <!-- هدر جدول -->
      <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between bg-gray-50 dark:bg-gray-700/50">
        <div class="flex items-center gap-2">
          <svg class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
          </svg>
          <h3 class="text-base font-semibold text-gray-900 dark:text-white">
            جدول محاسبه استوک
            <span class="text-sm font-normal text-gray-500 dark:text-gray-400 mr-2">({{ calcRows.length }} ردیف)</span>
          </h3>
        </div>
        <button
          @click="clearAllRows"
          class="text-xs text-danger-600 hover:text-danger-800 dark:text-danger-400 dark:hover:text-danger-300 transition-colors flex items-center gap-1"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
          </svg>
          حذف همه
        </button>
      </div>

      <!-- کارت‌های محاسبه (برای موبایل) -->
      <div class="block lg:hidden p-4 space-y-3">
        <div
          v-for="row in calcRows"
          :key="row.id"
          class="bg-gray-50 dark:bg-gray-700/30 rounded-lg p-3 border border-gray-200 dark:border-gray-600"
        >
          <!-- نام ماده -->
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-2">
              <div
                class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
                :class="row.isAcid ? 'bg-warning-50 dark:bg-warning-900/30' : 'bg-primary-50 dark:bg-primary-900/30'"
              >
                <svg
                  class="w-4 h-4"
                  :class="row.isAcid ? 'text-warning-600 dark:text-warning-400' : 'text-primary-600 dark:text-primary-400'"
                  fill="none" stroke="currentColor" viewBox="0 0 24 24"
                >
                  <path v-if="row.isAcid" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
                  <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
                </svg>
              </div>
              <div>
                <p class="font-medium text-sm text-gray-900 dark:text-white">{{ row.materialName }}</p>
                <p class="text-[10px] text-gray-400 dark:text-gray-500">
                  {{ row.isAcid ? 'اسید' : 'کود' }}
                </p>
              </div>
            </div>
            <button
              @click="removeCalcRow(row.id)"
              class="p-1.5 rounded-lg text-danger-600 hover:text-danger-800 hover:bg-danger-50 dark:hover:bg-danger-900/30 transition-colors"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
              </svg>
            </button>
          </div>

          <!-- فیلدها -->
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">
                وزن در استوک (گرم)
                <span v-if="row.weight > 0" class="text-success-600">✓</span>
              </label>
              <input
                type="number"
                :value="row.weight"
                @input="updateRowWeight(row.id, $event)"
                step="0.001"
                min="0"
                :class="[
                  'w-full px-2 py-1.5 text-center border rounded text-sm transition-all',
                  row.weight > 0 
                    ? 'border-success-400 bg-success-50 dark:bg-success-900/20 text-success-700 dark:text-success-400' 
                    : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100'
                ]"
              />
            </div>
            <div>
              <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">
                خلوص (%)
                <span v-if="row.purity > 0 && row.purity !== 100" class="text-warning-600">!</span>
              </label>
              <input
                type="number"
                :value="row.purity"
                @input="updateRowPurity(row.id, $event)"
                step="0.1"
                min="0"
                max="100"
                :class="[
                  'w-full px-2 py-1.5 text-center border rounded text-sm transition-all',
                  row.purity > 0 && row.purity !== 100
                    ? 'border-warning-400 bg-warning-50 dark:bg-warning-900/20 text-warning-700 dark:text-warning-400'
                    : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100'
                ]"
              />
            </div>
          </div>

          <!-- هزینه -->
          <div class="mt-2 pt-2 border-t border-gray-200 dark:border-gray-600 flex items-center justify-between">
            <span class="text-xs text-gray-600 dark:text-gray-400">هزینه:</span>
            <span class="font-semibold text-sm text-gray-900 dark:text-white tabular-nums">
              {{ row.cost ? Number(row.cost).toLocaleString('fa-IR') : '0' }} تومان
            </span>
          </div>

          <!-- عناصر -->
          <div v-if="row.elements && Object.keys(row.elements).length > 0" class="mt-2 pt-2 border-t border-gray-200 dark:border-gray-600">
            <p class="text-xs text-gray-600 dark:text-gray-400 mb-1">عناصر تامین شده در استوک:</p>
            <div class="flex flex-wrap gap-1">
              <span
                v-for="(value, el) in row.elements"
                :key="el"
                class="text-[10px] px-1.5 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded"
              >
                {{ el }}: {{ Number(value).toFixed(3) }}g
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- جدول دسکتاپ -->
      <div class="hidden lg:block overflow-x-auto">
        <table class="w-full text-sm border-collapse">
          <thead>
            <tr class="bg-gray-50 dark:bg-gray-700/50">
              <th class="sticky right-0 z-10 bg-gray-50 dark:bg-gray-700/50 px-3 py-3 text-right text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[150px]">
                ماده
              </th>
              <th class="px-3 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[120px]">
                <div class="flex items-center justify-center gap-1">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3"/>
                  </svg>
                  وزن در استوک (گرم)
                </div>
              </th>
              <th class="px-3 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[90px]">
                خلوص (%)
              </th>
              <th class="px-3 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[120px]">
                <div class="flex items-center justify-center gap-1">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  هزینه (تومان)
                </div>
              </th>
              <th
                v-for="el in elements"
                :key="el"
                class="px-2 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[70px]"
              >
                {{ el }}
              </th>
              <th class="px-3 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[70px]">
                عملیات
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
            <tr
              v-for="row in calcRows"
              :key="row.id"
              class="hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors"
            >
              <!-- نام ماده -->
              <td class="sticky right-0 z-10 bg-white dark:bg-gray-800 px-3 py-2 text-right">
                <div class="flex items-center gap-2">
                  <div
                    class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
                    :class="row.isAcid ? 'bg-warning-50 dark:bg-warning-900/30' : 'bg-primary-50 dark:bg-primary-900/30'"
                  >
                    <svg
                      class="w-4 h-4"
                      :class="row.isAcid ? 'text-warning-600 dark:text-warning-400' : 'text-primary-600 dark:text-primary-400'"
                      fill="none" stroke="currentColor" viewBox="0 0 24 24"
                    >
                      <path v-if="row.isAcid" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
                      <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
                    </svg>
                  </div>
                  <div class="min-w-0">
                    <p class="font-medium text-gray-900 dark:text-white text-sm truncate">{{ row.materialName }}</p>
                    <p class="text-[10px] text-gray-400 dark:text-gray-500">
                      {{ row.isAcid ? 'اسید' : 'کود' }}
                    </p>
                  </div>
                </div>
              </td>

              <!-- وزن در استوک -->
              <td class="px-3 py-2 text-center">
                <input
                  type="number"
                  :value="row.weight"
                  @input="updateRowWeight(row.id, $event)"
                  step="0.001"
                  min="0"
                  :class="[
                    'w-full max-w-[100px] px-2 py-1.5 text-center border-2 rounded transition-all duration-200 tabular-nums',
                    row.weight > 0
                      ? 'border-success-400 bg-success-50 dark:bg-success-900/20 text-success-700 dark:text-success-400 font-semibold'
                      : 'border-transparent bg-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500'
                  ]"
                />
              </td>

              <!-- خلوص -->
              <td class="px-3 py-2 text-center">
                <input
                  type="number"
                  :value="row.purity"
                  @input="updateRowPurity(row.id, $event)"
                  step="0.1"
                  min="0"
                  max="100"
                  :class="[
                    'w-full max-w-[80px] px-2 py-1.5 text-center border-2 rounded transition-all duration-200 tabular-nums',
                    row.purity > 0 && row.purity !== 100
                      ? 'border-warning-400 bg-warning-50 dark:bg-warning-900/20 text-warning-700 dark:text-warning-400 font-semibold'
                      : 'border-transparent bg-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500'
                  ]"
                />
              </td>

              <!-- هزینه -->
              <td class="px-3 py-2 text-center">
                <span class="font-semibold text-gray-900 dark:text-white tabular-nums text-sm">
                  {{ row.cost ? Number(row.cost).toLocaleString('fa-IR') : '0' }}
                </span>
              </td>

              <!-- عناصر -->
              <td
                v-for="el in elements"
                :key="el"
                class="px-2 py-2 text-center text-xs font-mono tabular-nums"
                :class="[
                  row.elements && row.elements[el] && row.elements[el] > 0
                    ? 'text-primary-600 dark:text-primary-400 font-semibold bg-primary-50 dark:bg-primary-900/20'
                    : 'text-gray-700 dark:text-gray-300'
                ]"
              >
                {{ row.elements && row.elements[el] ? Number(row.elements[el]).toFixed(3) : '0.000' }}
              </td>

              <!-- عملیات -->
              <td class="px-3 py-2 text-center">
                <button
                  @click="removeCalcRow(row.id)"
                  class="p-1.5 rounded-lg text-danger-600 hover:text-danger-800 hover:bg-danger-50 dark:hover:bg-danger-900/30 transition-colors"
                  title="حذف"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                  </svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- خطاها -->
    <!-- ============================================================ -->
    <div v-if="calcErrors.length > 0" class="bg-danger-50 dark:bg-danger-900/20 border-r-4 border-danger-500 rounded-lg p-4">
      <div class="flex items-start gap-3">
        <svg class="w-5 h-5 text-danger-600 dark:text-danger-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
        </svg>
        <div class="flex-1 space-y-1">
          <div v-for="err in calcErrors" :key="err" class="text-danger-700 dark:text-danger-400 text-sm">
            {{ err }}
          </div>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- دکمه‌های اقدام -->
    <!-- ============================================================ -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <div class="flex flex-wrap gap-3">
        <button
          @click="calculateFertilizer"
          :disabled="isCalculating || calcRows.length === 0"
          class="px-4 py-2 bg-success-600 text-white rounded-lg hover:bg-success-700 transition-colors flex items-center gap-2 shadow-sm hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg v-if="!isCalculating" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
          </svg>
          <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
          {{ isCalculating ? 'در حال محاسبه...' : 'محاسبه استوک' }}
        </button>

        <button
          @click="resetAll"
          class="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors flex items-center gap-2"
          title="پاک کردن همه داده‌ها و شروع مجدد"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
          شروع مجدد
        </button>

        <button
          @click="printReport"
          class="px-4 py-2 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 transition-colors flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/>
          </svg>
          چاپ
        </button>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- خلاصه محاسبات -->
    <!-- ============================================================ -->
    <div v-if="calcRows.length > 0 && totalCost > 0" class="grid grid-cols-1 sm:grid-cols-4 gap-3">
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
        </div>
        <div>
          <p class="text-xs text-gray-500 dark:text-gray-400">تعداد مواد</p>
          <p class="text-xl font-bold text-gray-900 dark:text-white tabular-nums">{{ calcRows.length }}</p>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-warning-50 dark:bg-warning-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 text-warning-600 dark:text-warning-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <div>
          <p class="text-xs text-gray-500 dark:text-gray-400">مجموع هزینه</p>
          <p class="text-xl font-bold text-warning-600 dark:text-warning-400 tabular-nums">{{ Number(totalCost).toLocaleString('fa-IR') }} <span class="text-xs font-normal">تومان</span></p>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-success-50 dark:bg-success-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 text-success-600 dark:text-success-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/>
          </svg>
        </div>
        <div>
          <p class="text-xs text-gray-500 dark:text-gray-400">حجم استوک</p>
          <p class="text-xl font-bold text-gray-900 dark:text-white tabular-nums">{{ stockVolume }} <span class="text-xs font-normal">لیتر</span></p>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-indigo-50 dark:bg-indigo-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 text-indigo-600 dark:text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
          </svg>
        </div>
        <div>
          <p class="text-xs text-gray-500 dark:text-gray-400">ضریب غلظت</p>
          <p class="text-xl font-bold text-indigo-600 dark:text-indigo-400 tabular-nums">{{ concentrationFactor.toFixed(1) }}× <span class="text-xs font-normal">استوک</span></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useCalcStore } from '@/store/modules/calcStore';
import { useCalculations } from '@/composables/useCalculations';

// ===== Props =====
const props = defineProps<{
  fertilizers: any[];
  selectedFertilizers: string[];
  tankVolume: number;
  dilutionFactor: number;
  calcRows: any[];
  calcErrors: string[];
}>();

// ===== Emits =====
const emit = defineEmits<{
  (e: 'update:selectedFertilizers', value: string[]): void;
  (e: 'update:tankVolume', value: number): void;
  (e: 'update:dilutionFactor', value: number): void;
  (e: 'update:calcRows', value: any[]): void;
  (e: 'update:calcErrors', value: string[]): void;
}>();

// ===== Store & Composables =====
const calcStore = useCalcStore();
const { calculateReservoir, isCalculating } = useCalculations();

// ===== State =====
const fertilizerSearchQuery = ref('');

// 🆕 تنظیمات استوک (به جای tankVolume و dilutionFactor قدیمی)
const mainTankVolume = ref(10000);  // حجم مخزن اصلی (لیتر)
const stockVolume = ref(100);       // حجم مخزن استوک (لیتر)
const injectionRatio = ref(100);    // نسبت تزریق (1:100)

// ===== Data =====
const elements = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'];

// ===== Computed =====

/**
 * محاسبه ضریب غلظت استوک
 * فرمول: (حجم مخزن اصلی ÷ حجم استوک) × نسبت تزریق
 */
const concentrationFactor = computed(() => {
  if (stockVolume.value === 0) return 0;
  return (mainTankVolume.value / stockVolume.value) * injectionRatio.value;
});

const totalCost = computed(() => {
  return props.calcRows.reduce((sum: number, row: any) => sum + (row.cost || 0), 0);
});

const filteredFertilizersForSelection = computed(() => {
  let result = props.fertilizers;
  
  if (fertilizerSearchQuery.value.trim()) {
    const query = fertilizerSearchQuery.value.trim().toLowerCase();
    result = result.filter((f: any) =>
      f.name.toLowerCase().includes(query) ||
      (f.brand && f.brand.toLowerCase().includes(query))
    );
  }
  
  return result;
});

/**
 * آیا همه کودها انتخاب شده‌اند؟
 */
const isAllSelected = computed(() => {
  return props.fertilizers.length > 0 && 
         props.selectedFertilizers.length === props.fertilizers.length;
});

// ===== Methods =====

/**
 * دریافت عناصر اصلی یک کود (حداکثر 3 عنصر با بیشترین درصد)
 */
const getMainElements = (fertilizer: any): Array<{ symbol: string; value: number }> => {
  if (!fertilizer.elements) return [];
  
  const entries = Object.entries(fertilizer.elements)
    .filter(([_, value]) => value && (value as number) > 0)
    .map(([symbol, value]) => ({ symbol, value: value as number }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 3);
  
  return entries;
};

/**
 * انتخاب/عدم انتخاب یک کود
 */
const toggleFertilizerSelection = (id: string) => {
  const current = [...props.selectedFertilizers];
  const index = current.indexOf(id);
  
  if (index === -1) {
    current.push(id);
  } else {
    current.splice(index, 1);
  }
  
  emit('update:selectedFertilizers', current);
};

/**
 * 🆕 انتخاب همه کودها
 */
const toggleSelectAll = () => {
  if (isAllSelected.value) {
    // لغو انتخاب همه
    emit('update:selectedFertilizers', []);
  } else {
    // انتخاب همه
    const allIds = props.fertilizers.map((f: any) => f.id);
    emit('update:selectedFertilizers', allIds);
  }
};

/**
 * افزودن کودهای انتخاب شده به جدول
 */
const addSelectedFertilizersToTable = () => {
  const selected = props.fertilizers.filter((f: any) => props.selectedFertilizers.includes(f.id));
  
  const newRows = selected.map((f: any) => ({
    id: `row-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`,
    materialName: f.name,
    weight: 0,  // کاربر باید وزن را وارد کند
    purity: 100,  // پیش‌فرض 100%
    cost: 0,
    elements: { ...f.elements },
    isAcid: f.isAcid || false,
    acidType: f.acidType || null,
    fertilizerId: f.id
  }));
  
  emit('update:calcRows', [...props.calcRows, ...newRows]);
  emit('update:selectedFertilizers', []);
  
  // پاک کردن جستجو
  fertilizerSearchQuery.value = '';
};

/**
 * به‌روزرسانی وزن یک ردیف
 */
const updateRowWeight = (id: string, event: Event) => {
  const target = event.target as HTMLInputElement;
  const weight = parseFloat(target.value) || 0;
  
  const newRows = props.calcRows.map((row: any) => {
    if (row.id === id) {
      const updatedRow = { ...row, weight };
      
      // محاسبه عناصر تامین شده در استوک
      if (updatedRow.elements) {
        const newElements: Record<string, number> = {};
        for (const [el, pct] of Object.entries(updatedRow.elements)) {
          if (pct) {
            // مقدار عنصر = وزن × (درصد عنصر / 100) × (خلوص / 100)
            newElements[el] = (weight * (pct as number / 100) * (updatedRow.purity / 100));
          }
        }
        updatedRow.elements = newElements;
      }
      
      // محاسبه هزینه
      const fertilizer = props.fertilizers.find((f: any) => f.id === updatedRow.fertilizerId);
      if (fertilizer) {
        updatedRow.cost = (weight / 1000) * fertilizer.pricePerKg;
      }
      
      return updatedRow;
    }
    return row;
  });
  
  emit('update:calcRows', newRows);
};

/**
 * به‌روزرسانی خلوص یک ردیف
 */
const updateRowPurity = (id: string, event: Event) => {
  const target = event.target as HTMLInputElement;
  const purity = parseFloat(target.value) || 0;
  
  const newRows = props.calcRows.map((row: any) => {
    if (row.id === id) {
      const updatedRow = { ...row, purity };
      
      // محاسبه مجدد عناصر
      if (updatedRow.elements && updatedRow.weight) {
        const newElements: Record<string, number> = {};
        for (const [el, pct] of Object.entries(updatedRow.elements)) {
          if (pct) {
            newElements[el] = (updatedRow.weight * (pct as number / 100) * (purity / 100));
          }
        }
        updatedRow.elements = newElements;
      }
      
      return updatedRow;
    }
    return row;
  });
  
  emit('update:calcRows', newRows);
};

/**
 * حذف یک ردیف
 */
const removeCalcRow = (id: string) => {
  emit('update:calcRows', props.calcRows.filter((r: any) => r.id !== id));
};

/**
 * پاک کردن همه ردیف‌ها
 */
const clearAllRows = () => {
  if (confirm('آیا از حذف همه ردیف‌ها اطمینان دارید؟')) {
    emit('update:calcRows', []);
    emit('update:calcErrors', []);
  }
};

/**
 * 🆕 محاسبه نهایی - validation اصلاح شده
 */
const calculateFertilizer = async () => {
  const errors: string[] = [];
  
  // بررسی تنظیمات استوک
  if (mainTankVolume.value <= 0) {
    errors.push('حجم مخزن اصلی باید بزرگتر از صفر باشد');
  }
  if (stockVolume.value <= 0) {
    errors.push('حجم مخزن استوک باید بزرگتر از صفر باشد');
  }
  if (injectionRatio.value <= 0) {
    errors.push('نسبت تزریق باید بزرگتر از صفر باشد');
  }
  
  // بررسی ردیف‌ها - فقط ردیف‌هایی که وزن دارند
  const rowsWithWeight = props.calcRows.filter(row => row.weight > 0);
  
  if (rowsWithWeight.length === 0) {
    errors.push('حداقل یک کود باید وزن داشته باشد');
  }
  
  // بررسی خلوص
  for (const row of rowsWithWeight) {
    if (!row.purity || row.purity <= 0 || row.purity > 100) {
      errors.push(`خلوص کود "${row.materialName}" باید بین 1 تا 100 باشد`);
    }
  }
  
  emit('update:calcErrors', errors);
  
  if (errors.length === 0) {
    // ذخیره در store
    calcStore.calculationRows = props.calcRows;
    
    // محاسبه مخازن از طریق API
    const fertilizers = rowsWithWeight.map(row => ({
      fertilizer: {
        name: row.materialName,
        is_acid: row.isAcid || false
      },
      weight: row.weight,
      purity: row.purity
    }));
    
    const reservoirResult = await calculateReservoir(fertilizers);
    if (reservoirResult) {
      calcStore.reservoirData = reservoirResult.reservoir_data;
    }
    
    alert('✅ محاسبات با موفقیت انجام شد!');
  }
};

/**
 * 🆕 بازنشانی کامل - شروع مجدد
 */
const resetAll = () => {
  if (confirm('آیا از شروع مجدد اطمینان دارید؟ تمام داده‌ها پاک خواهند شد.')) {
    emit('update:calcRows', []);
    emit('update:calcErrors', []);
    emit('update:selectedFertilizers', []);
    mainTankVolume.value = 10000;
    stockVolume.value = 100;
    injectionRatio.value = 100;
    fertilizerSearchQuery.value = '';
  }
};

/**
 * چاپ گزارش
 */
const printReport = () => {
  window.print();
};
</script>

<style scoped>
.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}

.overflow-x-auto::-webkit-scrollbar {
  height: 6px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.dark .overflow-x-auto::-webkit-scrollbar-track {
  background: #374151;
}

.dark .overflow-x-auto::-webkit-scrollbar-thumb {
  background: #4b5563;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

.dark .custom-scrollbar::-webkit-scrollbar-track {
  background: #374151;
}

.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background: #4b5563;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>