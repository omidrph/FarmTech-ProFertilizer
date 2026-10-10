<!-- frontend/src/components/features/fertilizer-db/FertilizerStatsAndTable.vue -->
<template>
  <div>
    <!-- ============================================================ -->
    <!-- نوار ابزار فشرده: دسته‌ها + جستجو + عملیات (یک نوار باریک) -->
    <!-- ============================================================ -->
    <div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-2.5 space-y-2.5">
      <!-- دسته‌ها (فیلتر سریع): اسیدها و بازها کنار هم -->
      <div class="flex items-center gap-1.5 overflow-x-auto no-scrollbar -mx-0.5 px-0.5">
        <button
          v-for="chip in categoryChips"
          :key="chip.key ?? 'all'"
          type="button"
          @click="setFilter(chip.key)"
          class="flex-shrink-0 h-8 px-3 rounded-lg text-xs font-medium border transition-colors flex items-center gap-1.5"
          :class="activeFilter === chip.key
            ? chip.activeClass
            : 'border-gray-200 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700/50'"
        >
          <span class="w-1.5 h-1.5 rounded-full" :class="chip.dot"></span>
          {{ chip.label }}
          <span class="tabular-nums opacity-70">{{ chip.count }}</span>
        </button>
      </div>

      <div class="flex items-center gap-2">
        <!-- جستجو -->
        <div class="relative flex-1 min-w-0">
          <svg class="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11a6 6 0 11-12 0 6 6 0 0112 0z" />
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="جستجو در نام، برند یا دسته…"
            class="w-full h-9 pr-9 pl-8 text-sm border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-gray-900 dark:text-gray-100 placeholder-gray-400 outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
          />
          <button v-if="searchQuery" type="button" @click="searchQuery = ''" class="absolute left-2 top-1/2 -translate-y-1/2 w-5 h-5 rounded text-gray-400 hover:text-gray-600 text-xs" aria-label="پاک کردن جستجو">✕</button>
        </div>

        <!-- فیلتر -->
        <button
          type="button"
          @click="openFilterModal"
          class="h-9 px-3 rounded-lg border text-sm font-medium flex items-center gap-1.5 flex-shrink-0 transition-colors"
          :class="advancedFilterCount
            ? 'border-primary-400 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300'
            : 'border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700/50'"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4h18M6 12h12M10 20h4" /></svg>
          <span class="hidden sm:inline">فیلتر</span>
          <span v-if="advancedFilterCount" class="min-w-[18px] h-[18px] px-1 rounded-full bg-primary-600 text-white text-[10px] flex items-center justify-center tabular-nums">{{ advancedFilterCount }}</span>
        </button>

        <!-- افزودن -->
        <button
          type="button"
          @click="$emit('open-modal')"
          class="h-9 px-3.5 rounded-lg bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium flex items-center gap-1.5 flex-shrink-0 transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M12 4v16m8-8H4" /></svg>
          <span>افزودن<span class="hidden sm:inline"> کود</span></span>
        </button>

        <!-- پاک کردن همهٔ کودها -->
        <button
          v-if="userFertilizers.length > 0"
          type="button"
          @click="clearTable"
          class="h-9 w-9 rounded-lg border border-gray-200 dark:border-gray-600 text-gray-400 hover:text-rose-600 hover:border-rose-300 dark:hover:border-rose-800 flex items-center justify-center flex-shrink-0 transition-colors"
          title="پاک کردن همهٔ کودهای شخصی"
          aria-label="پاک کردن همهٔ کودهای شخصی"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.87 12.14A2 2 0 0116.14 21H7.86a2 2 0 01-1.99-1.86L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
        </button>
      </div>

      <div class="flex items-center justify-between text-[11px] text-gray-500 dark:text-gray-400 px-0.5">
        <span class="tabular-nums">{{ filteredFertilizers.length.toLocaleString('fa-IR') }} کود نمایش داده می‌شود<template v-if="hasActiveFilters"> (از {{ userFertilizers.length.toLocaleString('fa-IR') }})</template></span>
        <button v-if="hasActiveFilters" type="button" @click="clearAllFilters" class="text-primary-600 dark:text-primary-400 hover:underline">پاک کردن فیلترها</button>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- نمایش نتایج -->
    <!-- ============================================================ -->
    <div v-if="filteredFertilizers.length > 0" class="mt-3">
      <!-- ============================================================ -->
      <!-- دسکتاپ: جدول -->
      <!-- ============================================================ -->
      <div class="hidden sm:block bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
        <div class="max-h-[520px] overflow-y-auto custom-scrollbar">
          <div class="overflow-x-auto">
            <table class="w-full text-sm border-collapse">
              <thead>
                <tr class="bg-gray-50 dark:bg-gray-700/50">
                  <th class="sticky right-0 z-10 bg-gray-50 dark:bg-gray-700/50 px-4 py-3 text-right text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[200px]">
                    نام / برند
                  </th>
                  <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[80px]">
                    فرم
                  </th>
                  <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[80px]">
                    خلوص
                  </th>
                  <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[80px]">
                    pH
                  </th>
                  <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[120px]">
                    قیمت
                  </th>
                  <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[180px]">
                    عناصر
                  </th>
                  <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[80px]">
                    عملیات
                  </th>
                </tr>
              </thead>

              <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
                <tr
                  v-for="fertilizer in filteredFertilizers"
                  :key="fertilizer.id"
                  class="hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors group"
                >
                  <td class="sticky right-0 z-10 bg-white dark:bg-gray-800 px-4 py-3 text-right">
                    <div class="flex items-center gap-3">
                      <div
                        class="w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0"
                        :class="getFormColorClass(fertilizer)"
                      >
                        <component
                          :is="getFormIcon(fertilizer)"
                          class="w-5 h-5"
                          :class="getFormIconColorClass(fertilizer)"
                        />
                      </div>

                      <div class="min-w-0">
                        <p class="font-medium text-gray-900 dark:text-white truncate">
                          {{ fertilizer.name }}
                        </p>

                        <div class="flex items-center gap-2 mt-0.5 flex-wrap">
                          <span
                            v-if="fertilizer.brand"
                            class="text-[10px] text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-700 px-1.5 py-0.5 rounded"
                          >
                            {{ fertilizer.brand }}
                          </span>

                          <span
                            v-if="fertilizer.isAcid"
                            class="text-[10px] px-1.5 py-0.5 bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300 rounded"
                          >
                            اسید
                          </span>
                          <span
                            v-if="fertilizer.isBase"
                            class="text-[10px] px-1.5 py-0.5 bg-sky-100 dark:bg-sky-900/30 text-sky-700 dark:text-sky-300 rounded"
                          >
                            باز
                          </span>

                          <span
                            v-if="fertilizer.sourceSystemId"
                            
                           :class="isCompanyFert(fertilizer) ? 'bg-teal-100 text-teal-700 dark:bg-teal-900/30 dark:text-teal-300' : 'bg-indigo-100 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-300'" class="text-[10px] px-1.5 py-0.5 rounded">{{ isCompanyFert(fertilizer) ? 'شرکتی' : 'سیستمی' }}</span>
                        </div>
                      </div>
                    </div>
                  </td>

                  <!-- فرم -->
                  <td class="px-4 py-3 text-center">
                    <span
                      class="text-xs font-medium px-2 py-1 rounded-full"
                      :class="getFormBadgeClass(fertilizer)"
                    >
                      {{ getFormLabel(fertilizer.form) }}
                    </span>
                  </td>

                  <!-- خلوص -->
                  <td class="px-4 py-3 text-center">
                    <span class="font-semibold text-gray-900 dark:text-white tabular-nums">
                      {{ fertilizer.concentration || 100 }}%
                    </span>
                  </td>

                  <!-- pH -->
                  <td class="px-4 py-3 text-center">
                    <span
                      v-if="fertilizer.phLevel !== undefined && fertilizer.phLevel !== null"
                      class="font-semibold text-gray-900 dark:text-white tabular-nums"
                    >
                      {{ fertilizer.phLevel }}
                    </span>
                    <span
                      v-else
                      class="text-gray-400 dark:text-gray-500 text-xs"
                    >
                      -
                    </span>
                  </td>

                  <!-- قیمت -->
                  <td class="px-4 py-3 text-center">
                    <span class="font-semibold text-gray-900 dark:text-white tabular-nums">
                      {{ priceText(fertilizer) }}
                    </span>
                    <span class="block text-[10px] text-gray-400">{{ priceUnitText(fertilizer) }}</span>
                  </td>

                  <!-- عناصر -->
                  <td class="px-4 py-3">
                    <div class="flex flex-wrap gap-1 justify-center">
                      <template v-if="hasElements(fertilizer)">
                        <span
                          v-for="[element, percentage] in topElements(fertilizer)"
                          :key="element"
                          class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium border"
                          :class="getElementBadgeClass(element)"
                        >
                          <span class="font-bold">{{ element }}</span>
                          <span class="mx-1 text-gray-400">|</span>
                          <span>{{ percentage }}%</span>
                        </span>
                        <!-- بقیهٔ عناصر: با هاور، فهرست کامل -->
                        <span
                          v-if="elementCount(fertilizer) > 3"
                          class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium border border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-300 cursor-pointer bg-gray-50 dark:bg-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-600"
                          @mouseenter="showTip($event, fertilizer)" @mouseleave="tip = null" @focus="showTip($event, fertilizer)" @blur="tip = null" tabindex="0"
                        >+{{ elementCount(fertilizer) - 3 }}</span>
                      </template>

                      <span
                        v-else
                        class="text-xs text-gray-400 dark:text-gray-500 italic"
                      >
                        -
                      </span>
                    </div>
                  </td>

                  <!-- عملیات -->
                  <td class="px-4 py-3 text-center">
                    <div class="flex items-center justify-center gap-1">
                      <button
                        @click="$emit('edit-fertilizer', fertilizer)"
                        class="p-1.5 rounded-lg text-primary-600 hover:text-primary-800 hover:bg-primary-50 dark:hover:bg-primary-900/30 transition-colors"
                        title="ویرایش"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                        </svg>
                      </button>

                      <button
                        @click="$emit('delete-fertilizer', fertilizer.id)"
                        class="p-1.5 rounded-lg text-danger-600 hover:text-danger-800 hover:bg-danger-50 dark:hover:bg-danger-900/30 transition-colors"
                        title="حذف"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- ============================================================ -->
      <!-- موبایل: کارت‌ها -->
      <!-- ============================================================ -->
      <div class="sm:hidden max-h-[520px] overflow-y-auto custom-scrollbar space-y-3 pr-1">
        <div
          v-for="fertilizer in filteredFertilizers"
          :key="fertilizer.id"
          class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4"
        >
          <div class="flex items-start justify-between">
            <div class="flex items-center gap-3 flex-1 min-w-0">
              <!-- آیکون فرم -->
              <div
                class="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0"
                :class="getFormColorClass(fertilizer)"
              >
                <component
                  :is="getFormIcon(fertilizer)"
                  class="w-5 h-5"
                  :class="getFormIconColorClass(fertilizer)"
                />
              </div>

              <div class="min-w-0 flex-1">
                <p class="font-semibold text-gray-900 dark:text-white truncate">
                  {{ fertilizer.name }}
                </p>

                <div class="flex items-center gap-1.5 mt-0.5 flex-wrap">
                  <span
                    v-if="fertilizer.brand"
                    class="text-[10px] text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-700 px-1.5 py-0.5 rounded"
                  >
                    {{ fertilizer.brand }}
                  </span>

                  <span
                    class="text-[10px] font-medium px-1.5 py-0.5 rounded-full"
                    :class="getFormBadgeClass(fertilizer)"
                  >
                    {{ getFormLabel(fertilizer.form) }}
                  </span>

                  <span
                    v-if="fertilizer.isAcid"
                    class="text-[10px] px-1.5 py-0.5 bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300 rounded"
                  >
                    اسید
                  </span>

                  <span
                    v-if="fertilizer.isBase"
                    class="text-[10px] px-1.5 py-0.5 bg-sky-100 dark:bg-sky-900/30 text-sky-700 dark:text-sky-300 rounded"
                  >
                    باز
                  </span>

                  <span
                    v-if="fertilizer.sourceSystemId"
                    
                   :class="isCompanyFert(fertilizer) ? 'bg-teal-100 text-teal-700 dark:bg-teal-900/30 dark:text-teal-300' : 'bg-indigo-100 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-300'" class="text-[10px] px-1.5 py-0.5 rounded">{{ isCompanyFert(fertilizer) ? 'شرکتی' : 'سیستمی' }}</span>
                </div>
              </div>
            </div>

            <div class="flex items-center gap-1 flex-shrink-0">
              <button
                @click="$emit('edit-fertilizer', fertilizer)"
                class="p-1.5 rounded-lg text-primary-600 hover:text-primary-800 hover:bg-primary-50 dark:hover:bg-primary-900/30 transition-colors"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                </svg>
              </button>

              <button
                @click="$emit('delete-fertilizer', fertilizer.id)"
                class="p-1.5 rounded-lg text-danger-600 hover:text-danger-800 hover:bg-danger-50 dark:hover:bg-danger-900/30 transition-colors"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 01-1 1v3M4 7h16"/>
                </svg>
              </button>
            </div>
          </div>

          <!-- جزئیات کارت موبایل -->
          <div class="mt-3 pt-3 border-t border-gray-100 dark:border-gray-700 grid grid-cols-3 gap-2 text-center">
            <div>
              <p class="text-[10px] text-gray-400 dark:text-gray-500">خلوص</p>
              <p class="text-sm font-semibold text-gray-900 dark:text-white">
                {{ fertilizer.concentration || 100 }}%
              </p>
            </div>

            <div>
              <p class="text-[10px] text-gray-400 dark:text-gray-500">pH</p>
              <p class="text-sm font-semibold text-gray-900 dark:text-white">
                {{ fertilizer.phLevel || '-' }}
              </p>
            </div>

            <div>
              <p class="text-[10px] text-gray-400 dark:text-gray-500">قیمت</p>
              <p class="text-sm font-semibold text-gray-900 dark:text-white">
                {{ priceText(fertilizer) }}
                <span class="block text-[10px] font-normal text-gray-400">{{ priceUnitText(fertilizer) }}</span>
              </p>
            </div>
          </div>

          <!-- عناصر در موبایل -->
          <div class="mt-2 pt-2 border-t border-gray-100 dark:border-gray-700">
            <p class="text-[10px] text-gray-400 dark:text-gray-500 mb-1.5">
              عناصر تشکیل‌دهنده
            </p>

            <div class="flex flex-wrap gap-1">
              <template v-if="hasElements(fertilizer)">
                <span
                  v-for="[element, percentage] in topElements(fertilizer)"
                  :key="element"
                  class="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-medium border"
                  :class="getElementBadgeClass(element)"
                >
                  {{ element }}: {{ percentage }}%
                </span>
                <span v-if="elementCount(fertilizer) > 3" class="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] border border-gray-300 dark:border-gray-600 text-gray-500" :title="allElementsText(fertilizer)">+{{ elementCount(fertilizer) - 3 }}</span>
              </template>

              <span
                v-else
                class="text-xs text-gray-400 dark:text-gray-500 italic"
              >
                بدون عنصر
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- پیام خالی بودن -->
    <!-- ============================================================ -->
    <div
      v-else-if="!isLoading"
      class="mt-4 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-12 text-center"
    >
      <div class="w-20 h-20 mx-auto mb-4 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
        <svg class="w-10 h-10 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
        </svg>
      </div>

      <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
        {{ hasActiveFilters ? 'نتیجه‌ای یافت نشد' : 'هنوز کود شخصی ایجاد نکرده‌اید' }}
      </h4>

      <p class="text-sm text-gray-500 dark:text-gray-400 max-w-md mx-auto">
        {{ hasActiveFilters ? 'لطفاً فیلترها را تغییر دهید.' : 'با کلیک روی دکمه "افزودن کود" شروع کنید.' }}
      </p>

      <div class="mt-6 flex justify-center gap-3 flex-wrap">
        <button
          v-if="hasActiveFilters"
          @click="clearAllFilters"
          class="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors inline-flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
          پاک کردن فیلترها
        </button>

        <button
          v-else
          @click="$emit('open-modal')"
          class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors inline-flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
          افزودن کود
        </button>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- مودال فیلتر -->
    <!-- ============================================================ -->
    <AppModal :open="showFilterModal" size="sm" title="فیلترهای پیشرفته" @close="closeFilterModal">
      <template #icon>
        <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"/>
        </svg>
      </template>

      <div class="space-y-4">

              <!-- فرم فیزیکی -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
                  فرم فیزیکی
                </label>

                <select
                  v-model="filterForm"
                  class="w-full h-10 px-3 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-sm text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                >
                  <option value="all">همه فرم‌ها</option>
                  <option value="powder">پودری</option>
                  <option value="crystal">کریستالی</option>
                  <option value="liquid">مایع</option>
                  <option value="granular">گرانول</option>
                </select>
              </div>

              <!-- محدوده قیمت -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
                  محدوده قیمت (تومان)
                </label>

                <div class="flex items-center gap-3">
                  <div class="flex-1 relative">
                    <span class="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-gray-400">
                      از
                    </span>

                    <input
                      v-model.number="priceMin"
                      type="number"
                      placeholder="۰"
                      min="0"
                      class="w-full h-10 px-3 pr-8 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-sm text-gray-900 dark:text-gray-100 outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                    />
                  </div>

                  <span class="text-gray-400">تا</span>

                  <div class="flex-1 relative">
                    <span class="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-gray-400">
                      تا
                    </span>

                    <input
                      v-model.number="priceMax"
                      type="number"
                      placeholder="∞"
                      min="0"
                      class="w-full h-10 px-3 pr-8 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-sm text-gray-900 dark:text-gray-100 outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                    />
                  </div>
                </div>
              </div>

              <!-- عناصر خاص -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
                  دارای عنصر خاص
                </label>

                <select
                  v-model="filterElement"
                  class="w-full h-10 px-3 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-sm text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                >
                  <option value="all">همه عناصر</option>
                  <option value="Ca">کلسیم (Ca)</option>
                  <option value="K">پتاسیم (K)</option>
                  <option value="P">فسفر (P)</option>
                  <option value="N-NO3">نیترات (NO3)</option>
                  <option value="N-NH4">آمونیوم (NH4)</option>
                  <option value="Mg">منیزیم (Mg)</option>
                  <option value="Fe">آهن (Fe)</option>
                  <option value="Zn">روی (Zn)</option>
                  <option value="B">بر (B)</option>
                  <option value="Mn">منگنز (Mn)</option>
                  <option value="Cu">مس (Cu)</option>
                  <option value="Mo">مولیبدن (Mo)</option>
                </select>
              </div>

              <!-- نوع کود: اسید و باز کنار هم -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">نوع کود</label>
                <div class="grid grid-cols-4 gap-1.5">
                  <button v-for="opt in typeOptions" :key="opt.value" type="button" @click="filterType = opt.value"
                    class="h-9 rounded-lg border text-xs font-medium transition-colors"
                    :class="filterType === opt.value ? opt.activeClass : 'border-gray-200 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700/50'">
                    {{ opt.label }}
                  </button>
                </div>
              </div>

              <!-- شرکت / برند -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">شرکت / برند</label>
                <select v-model="filterBrand" class="w-full h-10 px-3 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-sm text-gray-900 dark:text-gray-100 outline-none focus:ring-2 focus:ring-primary-500">
                  <option value="all">همهٔ شرکت‌ها</option>
                  <option v-for="b in brandOptions" :key="b" :value="b">{{ b }}</option>
                </select>
              </div>

              <!-- منشأ کود -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">منشأ کود</label>
                <div class="grid grid-cols-3 gap-1.5">
                  <button v-for="opt in sourceOptions" :key="opt.value" type="button" @click="filterSource = opt.value"
                    class="h-9 rounded-lg border text-xs font-medium transition-colors"
                    :class="filterSource === opt.value
                      ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300'
                      : 'border-gray-200 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700/50'">
                    {{ opt.label }}
                  </button>
                </div>
              </div>
      </div>

      <template #footer>
        <div class="app-modal-actions">
          <button type="button" @click="resetFilters" class="app-modal-btn app-modal-btn-secondary">بازنشانی</button>
          <button type="button" @click="applyFilters" class="app-modal-btn app-modal-btn-primary">اعمال فیلتر</button>
        </div>
      </template>
    </AppModal>
  </div>
  <!-- پاپ‌اور همهٔ عناصر (Teleport به body؛ از هر ردیفی که +N را هاور کنید) -->
  <Teleport to="body">
    <div v-if="tip" class="fixed z-[80] pointer-events-none w-max max-w-[300px] rounded-xl bg-gray-900 text-white text-xs leading-6 p-3 shadow-2xl"
      :style="{ left: tip.x + 'px', top: tip.y + 'px', transform: tip.up ? 'translate(-50%, -100%)' : 'translate(-50%, 0)' }">
      <p class="font-semibold mb-1.5 text-gray-300 truncate max-w-[270px]">{{ tip.name }}</p>
      <div class="grid grid-cols-2 gap-x-5 gap-y-0.5 tabular-nums">
        <div v-for="[el, pct] in tip.items" :key="el" class="flex justify-between gap-3"><span class="font-medium">{{ el }}</span><span class="text-gray-300">{{ pct }}%</span></div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import AppModal from '@/components/common/AppModal.vue';
import { ref, computed } from 'vue';
import {
  IconPowder,
  IconLiquid,
  IconCrystal,
  IconGranular,
  IconAcid,
  IconDefault
} from './FertilizerIcons.ts';

// ============================================================
// Props
// ============================================================
const props = defineProps<{
  userFertilizers: any[];
  systemFertilizers: any[];
  isLoading: boolean;
  activeFilter: string | null;
}>();

// ============================================================
// Emits
// ============================================================
const emit = defineEmits<{
  (e: 'refresh'): void;
  (e: 'open-modal'): void;
  (e: 'edit-fertilizer', fertilizer: any): void;
  (e: 'delete-fertilizer', id: string): void;
  (e: 'filter-change', filter: string | null): void;
  (e: 'clear-table'): void;
}>();

// ============================================================
// State - فیلترها
// ============================================================
const searchQuery = ref('');
const filterForm = ref<'all' | 'powder' | 'crystal' | 'liquid' | 'granular'>('all');
const priceMin = ref<number | null>(null);
const priceMax = ref<number | null>(null);
const filterElement = ref<string>('all');
const filterType = ref<'all' | 'normal' | 'acid' | 'base'>('all');
const filterSource = ref<'all' | 'user' | 'system'>('all');
const filterBrand = ref('all');
const brandOptions = computed(() => [...new Set(props.userFertilizers.map((f: any) => (f.brand || '').trim()).filter(Boolean))].sort());
const showFilterModal = ref(false);

// ============================================================
// Computed
// ============================================================
const isAdjusterFert = (f: any) => !!(f.isAcid || f.isBase);

// عناصر: ۳ عنصر اصلی (بیشترین درصد) نمایش داده می‌شود و بقیه در پاپ‌اور هاور
const sortedElements = (f: any): Array<[string, number]> =>
  Object.entries(getActiveElements(f) as Record<string, number>).sort((a, b) => b[1] - a[1]);
const topElements = (f: any) => sortedElements(f).slice(0, 3);
const elementCount = (f: any) => sortedElements(f).length;
// ---- پاپ‌اور عناصر ----
const tip = ref<null | { x: number; y: number; up: boolean; name: string; items: Array<[string, number]> }>(null);
const showTip = (e: Event, f: any) => {
  const r = (e.currentTarget as HTMLElement).getBoundingClientRect();
  const up = r.top > 220;
  tip.value = { x: Math.min(Math.max(r.left + r.width / 2, 160), window.innerWidth - 160), y: up ? r.top - 8 : r.bottom + 8, up, name: f.name, items: sortedElements(f) };
};
const isCompanyFert = (f: any) => !!f.brand && f.brand !== 'استاندارد';
const allElementsText = (f: any) => sortedElements(f).map(([e, p]) => `${e}: ${p}%`).join('، ');

const normalFertilizersCount = computed(() => props.userFertilizers.filter((f: any) => !isAdjusterFert(f)).length);
const acidFertilizersCount = computed(() => props.userFertilizers.filter((f: any) => f.isAcid).length);
const baseFertilizersCount = computed(() => props.userFertilizers.filter((f: any) => f.isBase).length);
const systemCopiedCount = computed(() => props.userFertilizers.filter((f: any) => f.sourceSystemId).length);

// دسته‌های فیلتر سریع (اسید و باز کنار هم)
const categoryChips = computed(() => [
  { key: null as string | null, label: 'همه', count: props.userFertilizers.length, dot: 'bg-primary-500', activeClass: 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300' },
  { key: 'normal', label: 'معمولی', count: normalFertilizersCount.value, dot: 'bg-emerald-500', activeClass: 'border-emerald-500 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-300' },
  { key: 'acid', label: 'اسیدها', count: acidFertilizersCount.value, dot: 'bg-amber-500', activeClass: 'border-amber-500 bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-300' },
  { key: 'base', label: 'بازها', count: baseFertilizersCount.value, dot: 'bg-sky-500', activeClass: 'border-sky-500 bg-sky-50 dark:bg-sky-900/20 text-sky-700 dark:text-sky-300' },
  { key: 'system', label: 'کپی از سیستمی', count: systemCopiedCount.value, dot: 'bg-indigo-500', activeClass: 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/20 text-indigo-700 dark:text-indigo-300' }
]);

const typeOptions: Array<{ value: 'all' | 'normal' | 'acid' | 'base'; label: string; activeClass: string }> = [
  { value: 'all', label: 'همه', activeClass: 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300' },
  { value: 'normal', label: 'معمولی', activeClass: 'border-emerald-500 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-300' },
  { value: 'acid', label: 'اسید', activeClass: 'border-amber-500 bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-300' },
  { value: 'base', label: 'باز', activeClass: 'border-sky-500 bg-sky-50 dark:bg-sky-900/20 text-sky-700 dark:text-sky-300' }
];
const sourceOptions: Array<{ value: 'all' | 'user' | 'system'; label: string }> = [
  { value: 'all', label: 'همه' },
  { value: 'user', label: 'شخصی' },
  { value: 'system', label: 'کپی از سیستمی' }
];

// قیمت: ذخیره همیشه به‌ازای کیلوگرم؛ کود مایع با چگالی به‌ازای لیتر نمایش داده می‌شود
const priceIsPerLiter = (f: any) => f.form === 'liquid' && f.densityGMl > 0 && f.priceUnit === 'l';
const priceText = (f: any): string => {
  const perKg = Number(f.pricePerKg || 0);
  const v = priceIsPerLiter(f) ? perKg * f.densityGMl : perKg;
  return Math.round(v).toLocaleString('fa-IR');
};
const priceUnitText = (f: any): string => (priceIsPerLiter(f) ? 'هر لیتر' : 'هر کیلوگرم');

// تعداد فیلترهای پیشرفتهٔ فعال (برای نشان روی دکمهٔ فیلتر)
const advancedFilterCount = computed(() =>
  [
    filterForm.value !== 'all',
    !!priceMin.value,
    !!priceMax.value,
    filterElement.value !== 'all',
    filterType.value !== 'all',
    filterSource.value !== 'all',
    filterBrand.value !== 'all'
  ].filter(Boolean).length
);

const hasActiveFilters = computed(() => {
  return !!(
    searchQuery.value ||
    filterForm.value !== 'all' ||
    priceMin.value ||
    priceMax.value ||
    filterElement.value !== 'all' ||
    filterType.value !== 'all' ||
    filterSource.value !== 'all' ||
    props.activeFilter
  );
});

const filteredFertilizers = computed(() => {
  let result = props.userFertilizers;

  // فیلتر از کارت‌ها
  if (props.activeFilter === 'normal') {
    result = result.filter((f: any) => !isAdjusterFert(f));
  } else if (props.activeFilter === 'acid') {
    result = result.filter((f: any) => f.isAcid);
  } else if (props.activeFilter === 'base') {
    result = result.filter((f: any) => f.isBase);
  } else if (props.activeFilter === 'system') {
    result = result.filter((f: any) => f.sourceSystemId);
  }

  // جستجو
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.trim().toLowerCase();

    result = result.filter((f: any) =>
      f.name.toLowerCase().includes(query) ||
      (f.brand && f.brand.toLowerCase().includes(query)) ||
      (f.category && f.category.toLowerCase().includes(query))
    );
  }

  // فرم فیزیکی
  if (filterForm.value !== 'all') {
    result = result.filter((f: any) => f.form === filterForm.value);
  }

  // محدوده قیمت
  if (priceMin.value !== null && priceMin.value > 0) {
    result = result.filter(
      (f: any) => (f.pricePerKg || 0) >= priceMin.value!
    );
  }

  if (priceMax.value !== null && priceMax.value > 0) {
    result = result.filter(
      (f: any) => (f.pricePerKg || 0) <= priceMax.value!
    );
  }

  // عناصر خاص
  if (filterElement.value !== 'all') {
    result = result.filter((f: any) => {
      if (!f.elements) return false;
      return (
        f.elements[filterElement.value] &&
        f.elements[filterElement.value] > 0
      );
    });
  }

  // نوع کود
  if (filterType.value === 'acid') {
    result = result.filter((f: any) => f.isAcid);
  } else if (filterType.value === 'base') {
    result = result.filter((f: any) => f.isBase);
  } else if (filterType.value === 'normal') {
    result = result.filter((f: any) => !isAdjusterFert(f));
  }

  // شرکت / برند
  if (filterBrand.value !== 'all') {
    result = result.filter((f: any) => (f.brand || '').trim() === filterBrand.value);
  }

  // منشأ کود
  if (filterSource.value === 'system') {
    result = result.filter((f: any) => f.sourceSystemId);
  } else if (filterSource.value === 'user') {
    result = result.filter((f: any) => !f.sourceSystemId);
  }

  return result;
});

// ============================================================
// Methods - فرم‌ها و آیکون‌ها
// ============================================================
const getFormLabel = (form: string | undefined): string => {
  const labels: Record<string, string> = {
    liquid: 'مایع',
    powder: 'پودر',
    crystal: 'کریستال',
    granular: 'گرانول'
  };

  return form ? labels[form] || form : 'نامشخص';
};

const getFormIcon = (fertilizer: any) => {
  if (fertilizer.isAcid) return IconAcid;

  const icons: Record<string, any> = {
    liquid: IconLiquid,
    powder: IconPowder,
    crystal: IconCrystal,
    granular: IconGranular
  };

  return icons[fertilizer.form] || IconDefault;
};

const getFormBadgeClass = (fertilizer: any): string => {
  if (fertilizer.isAcid) {
    return 'bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400';
  }

  const classes: Record<string, string> = {
    liquid: 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400',
    powder: 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400',
    crystal: 'bg-cyan-100 dark:bg-cyan-900/30 text-cyan-700 dark:text-cyan-400',
    granular: 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400'
  };

  return classes[fertilizer.form] ||
    'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400';
};

const getFormColorClass = (fertilizer: any): string => {
  if (fertilizer.isAcid) {
    return 'bg-warning-50 dark:bg-warning-900/30';
  }

  const classes: Record<string, string> = {
    liquid: 'bg-blue-50 dark:bg-blue-900/30',
    powder: 'bg-purple-50 dark:bg-purple-900/30',
    crystal: 'bg-cyan-50 dark:bg-cyan-900/30',
    granular: 'bg-emerald-50 dark:bg-emerald-900/30'
  };

  return classes[fertilizer.form] || 'bg-gray-50 dark:bg-gray-700/30';
};

const getFormIconColorClass = (fertilizer: any): string => {
  if (fertilizer.isAcid) {
    return 'text-warning-600 dark:text-warning-400';
  }

  const classes: Record<string, string> = {
    liquid: 'text-blue-600 dark:text-blue-400',
    powder: 'text-purple-600 dark:text-purple-400',
    crystal: 'text-cyan-600 dark:text-cyan-400',
    granular: 'text-emerald-600 dark:text-emerald-400'
  };

  return classes[fertilizer.form] ||
    'text-gray-600 dark:text-gray-400';
};

const getElementBadgeClass = (element: string): string => {
  const cationElements = [
    'N-NH4',
    'K',
    'Ca',
    'Mg',
    'Na',
    'Fe',
    'Mn',
    'Zn',
    'Cu'
  ];

  const anionElements = [
    'N-NO3',
    'P',
    'S',
    'Cl',
    'B',
    'Mo'
  ];

  if (cationElements.includes(element)) {
    return 'bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-800';
  }

  if (anionElements.includes(element)) {
    return 'bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300 border-red-200 dark:border-red-800';
  }

  return 'bg-gray-50 dark:bg-gray-700 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-600';
};

const hasElements = (fertilizer: any): boolean => {
  if (!fertilizer.elements) return false;

  return Object.values(fertilizer.elements).some(
    (v: any) => v && v > 0
  );
};

const getActiveElements = (fertilizer: any): Record<string, number> => {
  if (!fertilizer.elements) return {};

  const result: Record<string, number> = {};

  for (const [key, value] of Object.entries(fertilizer.elements)) {
    if (value && (value as number) > 0) {
      result[key] = value as number;
    }
  }

  return result;
};

// ============================================================
// Methods - Filters
// ============================================================
const setFilter = (filter: string | null) => {
  emit('filter-change', filter);
};

const openFilterModal = () => {
  showFilterModal.value = true;
};

const closeFilterModal = () => {
  showFilterModal.value = false;
};

const applyFilters = () => {
  closeFilterModal();

  if (
    filterForm.value !== 'all' ||
    priceMin.value ||
    priceMax.value ||
    filterElement.value !== 'all' ||
    filterType.value !== 'all' ||
    filterSource.value !== 'all'
  ) {
    if (props.activeFilter !== null) {
      emit('filter-change', null);
    }
  }
};

const resetFilters = () => {
  filterForm.value = 'all';
  priceMin.value = null;
  priceMax.value = null;
  filterElement.value = 'all';
  filterType.value = 'all';
  filterSource.value = 'all';
  filterBrand.value = 'all';
  searchQuery.value = '';
};

const clearAllFilters = () => {
  resetFilters();
  emit('filter-change', null);
  closeFilterModal();
};

const clearTable = () => {
  if (
    confirm(
      'آیا از پاک کردن تمام کودهای شخصی اطمینان دارید؟ این عملیات غیرقابل بازگشت است.'
    )
  ) {
    emit('clear-table');
  }
};
</script>

<style scoped>
.no-scrollbar { scrollbar-width: none; }
.no-scrollbar::-webkit-scrollbar { display: none; }
.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
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
</style>
