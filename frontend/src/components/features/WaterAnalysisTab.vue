<template>
  <div class="space-y-6">
    <!-- وضعیت ذخیره‌سازی -->
    <div class="flex justify-end min-h-[1.5rem]">
      <!-- نشانگر وضعیت ذخیره‌سازی -->
      <div
        v-if="isSaving || saveStatus === 'success'"
        class="flex items-center gap-2 text-xs animate-fade-in"
      >
        <span
          v-if="isSaving"
          class="flex items-center gap-1 text-gray-500 dark:text-gray-400"
        >
          <svg class="animate-spin h-3 w-3" fill="none" viewBox="0 0 24 24">
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            ></circle>
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
            ></path>
          </svg>
          در حال ذخیره...
        </span>

        <span
          v-else-if="saveStatus === 'success'"
          class="flex items-center gap-1 text-success-600 dark:text-success-400"
        >
          <svg
            class="w-4 h-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M5 13l4 4L19 7"
            />
          </svg>
          ذخیره شد
        </span>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- بخش تنظیمات درصد -->
    <!-- ============================================================ -->
    <div
      class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-5"
    >
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4">
        <!-- درصد آب -->
        <div>
          <label
            class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5"
          >
            استفاده از آب (%)
          </label>

          <div class="relative">
            <input
              type="number"
              :value="waterPercentage"
              @input="updateWaterPercentage($event)"
              min="0"
              max="100"
              class="w-full px-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            />
            <span
              class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm"
            >
              %
            </span>
          </div>
        </div>

        <!-- درصد پساب -->
        <div>
          <label
            class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5"
          >
            استفاده از پساب (%)
          </label>

          <div class="relative">
            <input
              type="number"
              :value="wastewaterPercentage"
              @input="updateWastewaterPercentage($event)"
              min="0"
              max="100"
              class="w-full px-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            />
            <span
              class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm"
            >
              %
            </span>
          </div>
        </div>
      </div>

      <!-- هشدار مجموع درصد -->
      <div
        v-if="totalPercentage !== 100"
        class="mt-4 bg-yellow-50 dark:bg-yellow-900/20 border-r-4 border-yellow-500 rounded-lg p-3 flex items-start gap-2"
      >
        <svg
          class="w-5 h-5 text-yellow-600 dark:text-yellow-400 flex-shrink-0 mt-0.5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
          />
        </svg>

        <p class="text-yellow-700 dark:text-yellow-400 text-sm">
          مجموع درصد آب و پساب باید برابر ۱۰۰ باشد. (فعلاً
          {{ totalPercentage }}٪)
          <br />
          <span class="text-xs opacity-80">
            نرم‌افزار به صورت خودکار درصد پساب را تنظیم می‌کند.
          </span>
        </p>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- نوار ابزار -->
    <!-- ============================================================ -->
    <div
      class="flex flex-wrap items-center gap-3 bg-white dark:bg-gray-800 p-3 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm"
    >
      <!-- بخش چپ: عنوان + واحد -->
      <div class="flex flex-wrap items-center gap-2 flex-1 min-w-[200px]">
        <h3
          class="text-base font-semibold text-gray-900 dark:text-white flex items-center gap-2 whitespace-nowrap"
        >
          <svg
            class="w-5 h-5 text-primary-600 flex-shrink-0"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>

          <span class="hidden xs:inline">جدول آنالیز عناصر</span>
          <span class="xs:hidden">آنالیز</span>
        </h3>

        <!-- انتخاب واحد -->
        <div class="flex items-center gap-1.5 mr-1 sm:mr-0">
          <label class="text-xs sm:text-sm text-gray-500 dark:text-gray-400">
            واحد:
          </label>

          <select
            v-model="currentUnit"
            class="px-1.5 sm:px-3 py-1 sm:py-1.5 text-xs sm:text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 transition-all"
          >
            <option value="ppm">mg/L</option>
            <option value="meq">meq/L</option>
            <option value="mmol">mmol/L</option>
            <option value="umol">µmol/L</option>
          </select>
        </div>
      </div>

      <!-- بخش راست: دکمه‌ها -->
      <div
        class="flex items-center gap-1.5 sm:gap-2 flex-wrap w-full sm:w-auto justify-end"
      >
        <!-- دکمه بازنشانی -->
        <button
          @click="resetWaterAnalysis"
          class="flex-1 sm:flex-none px-2.5 sm:px-4 py-1.5 sm:py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors text-xs sm:text-sm flex items-center justify-center gap-1 sm:gap-1.5 min-w-[60px] sm:min-w-0"
          title="بازنشانی تمام مقادیر"
        >
          <svg
            class="w-3.5 h-3.5 sm:w-4 sm:h-4 flex-shrink-0"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
            />
          </svg>

          <span>بازنشانی</span>
        </button>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- جدول آنالیز آب و پساب -->
    <!-- ============================================================ -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div class="overflow-x-auto custom-scrollbar">
        <table class="w-full text-sm border-collapse min-w-[800px]">
          <thead>
            <tr>
              <th class="sticky right-0 z-10 bg-gray-50 dark:bg-gray-700 px-4 py-3 text-right text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[100px] shadow-sm">عنصر</th>
              <th v-for="row in allRows" :key="row.key" class="px-3 py-3 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border-b border-gray-200 dark:border-gray-600 text-center min-w-[90px]">
                <div class="flex flex-col items-center gap-1">
                  <span>{{ row.key === 'Alkalinity' ? 'قلیائیت' : row.key }}</span>
                  <button type="button" @click="openFormMenu(row, $event)" dir="ltr"
                    class="flex items-center gap-0.5 text-[10px] font-bold text-primary-600 dark:text-primary-400"
                    :class="row.forms.length > 1 ? 'cursor-pointer' : 'cursor-default'">
                    {{ currentForm(row).label }}
                    <svg v-if="row.forms.length > 1" class="w-2.5 h-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7" /></svg>
                  </button>
                </div>
              </th>
              <th class="px-3 py-3 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border-b border-gray-200 dark:border-gray-600 text-center min-w-[90px]">
                <div class="flex flex-col items-center gap-1">
                  <span>EC</span>
                  <select v-model="ecUnit" @change="triggerAutoSave" class="text-[10px] bg-transparent border-none focus:ring-0 cursor-pointer text-primary-600 dark:text-primary-400 font-bold p-0 h-auto">
                    <option value="dS/m">dS/m</option>
                    <option value="mS/cm">mS/cm</option>
                    <option value="μS/cm">μS/cm</option>
                  </select>
                </div>
              </th>
              <th class="px-3 py-3 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border-b border-gray-200 dark:border-gray-600 text-center min-w-[90px]">
                <div class="flex flex-col items-center gap-1">
                  <span>pH</span>
                  <span class="text-[10px] font-normal text-gray-400">اختیاری</span>
                </div>
              </th>
            </tr>
          </thead>
          <tbody>
            <!-- ردیف پساب -->
            <tr v-if="showWastewaterRow" class="hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors group">
              <td class="sticky right-0 z-10 bg-white dark:bg-gray-800 px-4 py-2 text-right font-medium text-gray-600 dark:text-gray-400 border-l border-gray-100 dark:border-gray-700 shadow-sm">
                <div class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-orange-400"></span>پساب</div>
              </td>
              <td v-for="row in allRows" :key="'waste-' + row.key" class="px-2 py-2 border-l border-gray-100 dark:border-gray-700 text-center relative">
                <input type="text" inputmode="decimal" dir="ltr" :value="cellText('waste', row)" @change="onCellChange('waste', row, $event)" @keydown.enter="($event.target as HTMLInputElement).blur()" class="w-full max-w-[80px] mx-auto px-2 py-1.5 text-center tabular-nums bg-transparent border border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 rounded transition-all duration-200 text-gray-700 dark:text-gray-300" placeholder="۰" />
              </td>
              <td class="px-2 py-2 border-l border-gray-100 dark:border-gray-700 text-center relative text-gray-300 dark:text-gray-600">—</td>
              <td class="px-2 py-2 border-l border-gray-100 dark:border-gray-700 text-center relative text-gray-300 dark:text-gray-600">—</td>
            </tr>
            <!-- ردیف آب تازه -->
            <tr v-if="showFreshWaterRow" class="hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors group">
              <td class="sticky right-0 z-10 bg-white dark:bg-gray-800 px-4 py-2 text-right font-medium text-gray-600 dark:text-gray-400 border-l border-gray-100 dark:border-gray-700 shadow-sm">
                <div class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-blue-500"></span>آب تازه</div>
              </td>
              <td v-for="row in allRows" :key="'water-' + row.key" class="px-2 py-2 border-l border-gray-100 dark:border-gray-700 text-center relative">
                <input type="text" inputmode="decimal" dir="ltr" :value="cellText('water', row)" @change="onCellChange('water', row, $event)" @keydown.enter="($event.target as HTMLInputElement).blur()" class="w-full max-w-[80px] mx-auto px-2 py-1.5 text-center tabular-nums bg-transparent border border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 rounded transition-all duration-200 text-gray-700 dark:text-gray-300" placeholder="۰" />
              </td>
              <td class="px-2 py-2 border-l border-gray-100 dark:border-gray-700 text-center relative">
                <input type="text" inputmode="decimal" dir="ltr" :value="ecText" @change="onEcChange" @keydown.enter="($event.target as HTMLInputElement).blur()" class="w-full max-w-[80px] mx-auto px-2 py-1.5 text-center tabular-nums bg-transparent border border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 rounded transition-all duration-200 text-gray-700 dark:text-gray-300" />
              </td>
              <td class="px-2 py-2 border-l border-gray-100 dark:border-gray-700 text-center relative">
                <input type="text" inputmode="decimal" dir="ltr" :value="phText" @change="onPhChange" @keydown.enter="($event.target as HTMLInputElement).blur()" class="w-full max-w-[80px] mx-auto px-2 py-1.5 text-center tabular-nums bg-transparent border border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 rounded transition-all duration-200 text-gray-700 dark:text-gray-300" />
              </td>
            </tr>
            <!-- ردیف مقادیر تامینی -->
            <tr class="bg-primary-50 dark:bg-primary-900/10 border-t-2 border-primary-100 dark:border-primary-900/30">
              <td class="sticky right-0 z-10 bg-primary-50 dark:bg-primary-900/20 px-4 py-3 text-right font-bold text-primary-700 dark:text-primary-400 border-l border-primary-100 dark:border-primary-900/30 shadow-sm">
                <div class="flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                  مقادیر تامینی
                </div>
              </td>
              <td v-for="row in allRows" :key="'final-' + row.key" class="px-3 py-3 border-l border-primary-100 dark:border-primary-900/30 text-center font-bold text-primary-700 dark:text-primary-400 tabular-nums">{{ suppliedText(row) }}</td>
              <td class="px-3 py-3 border-l border-primary-100 dark:border-primary-900/30 text-center font-bold text-primary-700 dark:text-primary-400">-</td>
              <td class="px-3 py-3 text-center font-bold text-primary-700 dark:text-primary-400">-</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- منوی انتخاب فرم عنصر -->
    <template v-if="menu && menuRow">
      <div class="fixed inset-0 z-40" @click="menu = null"></div>
      <div class="fixed z-50 w-60 rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-800 shadow-xl p-1" :style="{ top: menu.top + 'px', left: menu.left + 'px' }">
        <button v-for="fm in menuRow.forms" :key="fm.key" type="button" @click="selectForm(menuRow, fm.key)"
          class="w-full flex items-center justify-between gap-3 px-3 py-2 rounded-md text-sm transition-colors hover:bg-gray-50 dark:hover:bg-gray-700"
          :class="formChoice[menuRow.key] === fm.key ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300' : 'text-gray-700 dark:text-gray-300'">
          <span>{{ fm.hint }}</span>
          <span class="font-semibold" dir="ltr">{{ fm.label }}</span>
        </button>
      </div>
    </template>

    <!-- ============================================================ -->
    <!-- بخش قالب‌های ذخیره شده -->
    <!-- ============================================================ -->
    <div
      class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-5"
    >
      <div class="flex items-center justify-between mb-4">
        <h3
          class="text-base font-semibold text-gray-900 dark:text-white flex items-center gap-2"
        >
          <svg
            class="w-5 h-5 text-indigo-600 dark:text-indigo-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
            />
          </svg>
          قالب‌های ذخیره شده من
          <span class="text-[11px] font-normal text-gray-400 tabular-nums">{{ waterTemplates.length.toLocaleString('fa-IR') }} از ۶</span>
        </h3>
        <button
          type="button"
          @click="openSaveTemplateModal"
          class="inline-flex items-center gap-1.5 h-9 px-3 rounded-lg border border-indigo-200 dark:border-indigo-800 text-indigo-700 dark:text-indigo-300 hover:bg-indigo-50 dark:hover:bg-indigo-900/20 text-xs sm:text-sm font-medium transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
          افزودن قالب جدید
        </button>
      </div>
      <p class="-mt-2 mb-3 text-[11px] leading-5 text-gray-500 dark:text-gray-400">قالب، نسخهٔ آمادهٔ مقادیر فعلی برای استفادهٔ مجدد است.</p>
      <Transition name="fade">
        <div v-if="templateStatus" class="mb-3 rounded-lg border px-3 py-2 text-xs"
          :class="templateStatus.type === 'success' ? 'border-emerald-200 dark:border-emerald-800 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-800 dark:text-emerald-200' : 'border-rose-200 dark:border-rose-800 bg-rose-50 dark:bg-rose-900/20 text-rose-800 dark:text-rose-200'">
          {{ templateStatus.text }}
        </div>
      </Transition>

      <!-- لیست قالب‌ها -->
      <div
        v-if="waterTemplates.length > 0"
        class="max-h-[320px] overflow-y-auto custom-scrollbar pl-1 pr-1"
      >
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          <div
            v-for="template in waterTemplates"
            :key="template.id"
            class="group relative bg-gray-50 dark:bg-gray-700/30 rounded-lg p-3 border border-gray-200 dark:border-gray-600 hover:border-indigo-300 dark:hover:border-indigo-700 transition-all hover:shadow-md"
          >
            <div class="flex items-start justify-between mb-2">
              <h4
                class="font-medium text-gray-900 dark:text-white text-sm truncate pl-16 sm:pl-0"
              >
                {{ template.name }}
              </h4>

              <div
                class="absolute top-2 left-2 flex gap-1 sm:opacity-0 sm:group-hover:opacity-100 sm:focus-within:opacity-100 transition-opacity"
              >
                <button
                  @click="loadWaterTemplate(template)"
                  class="p-1.5 rounded bg-white dark:bg-gray-600 text-indigo-600 dark:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-gray-500 shadow-sm"
                  title="بارگذاری"
                >
                  <svg
                    class="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
                    />
                  </svg>
                </button>

                <button
                  @click="deleteWaterTemplate(template.id)"
                  class="p-1.5 rounded bg-white dark:bg-gray-600 text-danger-600 dark:text-danger-400 hover:bg-danger-50 dark:hover:bg-gray-500 shadow-sm"
                  title="حذف"
                >
                  <svg
                    class="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                    />
                  </svg>
                </button>
              </div>
            </div>

            <!-- نمایش جزئیات کامل قالب -->
            <div
              class="space-y-1 text-[10px] text-gray-500 dark:text-gray-400 bg-white dark:bg-gray-700/50 rounded p-2"
            >
              <div class="flex justify-between">
                <span>آب: {{ template.water_percentage }}%</span>
                <span>
                  EC: {{ template.water_salinity }}
                  {{ template.water_salinity_unit }}
                </span>
              </div>

              <div
                v-if="template.description"
                class="mt-1 pt-1 border-t border-gray-200 dark:border-gray-600 italic text-gray-600 dark:text-gray-300"
              >
                "{{ template.description }}"
              </div>

              <!-- نمایش تعداد عناصر وارد شده -->
              <div class="mt-1 flex gap-2">
                <span
                  v-if="
                    template.water_values &&
                    Object.keys(template.water_values).length > 0
                  "
                  class="bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 px-1.5 rounded"
                >
                  {{
                    Object.keys(template.water_values).filter(
                      (k) => template.water_values[k] > 0 && !k.startsWith('lt:') && k !== 'pH'
                    ).length
                  }}
                  عنصر آب
                </span>

                <span
                  v-if="
                    template.wastewater_values &&
                    Object.keys(template.wastewater_values).length > 0
                  "
                  class="bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-400 px-1.5 rounded"
                >
                  {{
                    Object.keys(template.wastewater_values).filter(
                      (k) => template.wastewater_values[k] > 0 && !k.startsWith('lt:')
                    ).length
                  }}
                  عنصر پساب
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div
        v-else
        class="text-center py-8 bg-gray-50 dark:bg-gray-700/20 rounded-lg border-2 border-dashed border-gray-200 dark:border-gray-600"
      >
        <svg
          class="w-10 h-10 mx-auto text-gray-300 dark:text-gray-500 mb-2"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"
          />
        </svg>

        <p class="text-gray-500 dark:text-gray-400 text-sm">
          هنوز قالبی ذخیره نشده است
        </p>

        <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">
          با کلیک روی دکمه "ذخیره قالب جدید" شروع کنید
        </p>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- مودال ذخیره قالب -->
    <!-- ============================================================ -->
    <AppModal
      :open="showSaveTemplateModal"
      size="sm"
      title="ذخیره تنظیمات فعلی"
      subtitle="مقادیر فعلی به‌عنوان قالب ذخیره می‌شود"
      @close="closeSaveTemplateModal"
    >
      <template #icon>
        <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/>
        </svg>
      </template>

      <div class="space-y-4">
                <div>
                  <label
                    class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5"
                  >
                    نام قالب
                    <span class="text-danger-500">*</span>
                  </label>

                  <input
                    type="text"
                    v-model="templateForm.name"
                    class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                    placeholder="مثال: آب چاه شماره ۱ - تابستان"
                    autofocus
                  />
                </div>

                <div>
                  <label
                    class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5"
                  >
                    توضیحات (اختیاری)
                  </label>

                  <textarea
                    v-model="templateForm.description"
                    rows="2"
                    class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
                    placeholder="توضیحات تکمیلی..."
                  ></textarea>
                </div>

                <div
                  class="bg-primary-50 dark:bg-primary-900/20 rounded-lg p-3 text-xs text-primary-700 dark:text-primary-300 border border-primary-100 dark:border-primary-800"
                >
                  <p class="flex items-center gap-1.5">
                    <svg
                      class="w-4 h-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                      />
                    </svg>

                    تمام مقادیر جاری (درصد آب، EC و عناصر) در این قالب ذخیره
                    خواهند شد.
                  </p>
                </div>
      </div>

      <template #footer>
        <div class="app-modal-actions">
          <button type="button" @click="closeSaveTemplateModal" class="app-modal-btn app-modal-btn-secondary">انصراف</button>
          <button
            type="button"
            @click="saveWaterTemplate"
            :disabled="isSavingTemplate || !templateForm.name"
            class="app-modal-btn app-modal-btn-primary"
          >
            <svg v-if="isSavingTemplate" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            {{ isSavingTemplate ? 'در حال ذخیره...' : 'ذخیره قالب' }}
          </button>
        </div>
      </template>
    </AppModal>

    <!-- ============================================================ -->
    <!-- پیام Toast -->
    <!-- ============================================================ -->
    <Transition name="fade">
      <div
        v-if="toastMessage"
        class="fixed bottom-6 left-1/2 -translate-x-1/2 z-[200] px-6 py-3 rounded-xl shadow-2xl flex items-center gap-3 text-sm font-medium"
        :class="
          toastType === 'success'
            ? 'bg-success-600 text-white'
            : 'bg-danger-600 text-white'
        "
      >
        <svg
          v-if="toastType === 'success'"
          class="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M5 13l4 4L19 7"
          />
        </svg>

        <svg
          v-else
          class="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
          />
        </svg>

        <span>{{ toastMessage }}</span>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import AppModal from '@/components/common/AppModal.vue';
import { ref, reactive, computed, onMounted } from 'vue';
import { useWaterStore, EC_STANDARDS, convertECUnit } from '@/store/modules/waterStore';
import { WATER_GROUPS, toStored, fromStored, normalizeNumberText, fmtPlain, type WaterRow, type WaterForm, type WaterUnit } from '@/utils/waterForms';
import { apiService } from '@/services/apiService';
import { useReportStore } from '@/store/modules/reportStore';

// ===== Store =====
const waterStore = useWaterStore();
const reportStore = useReportStore();

// ===== State =====
// pH و Alkalinity هر دو از جدول حذف شده‌اند.
const currentUnit = ref<WaterUnit>('ppm');

// Auto-save State
const isSaving = ref(false);
const saveStatus = ref<'idle' | 'saving' | 'success'>('idle');
let saveTimeout: ReturnType<typeof setTimeout> | null = null;

// Toast State
const toastMessage = ref<string | null>(null);
const toastType = ref<'success' | 'error'>('success');

// Template State
const waterTemplates = ref<any[]>([]);
const showSaveTemplateModal = ref(false);
const isSavingTemplate = ref(false);
const templateStatus = ref<null | { type: 'success' | 'error'; text: string }>(null);
let templateStatusTimer: ReturnType<typeof setTimeout> | null = null;
const setTemplateStatus = (type: 'success' | 'error', text: string) => {
  templateStatus.value = { type, text };
  if (templateStatusTimer) clearTimeout(templateStatusTimer);
  templateStatusTimer = setTimeout(() => (templateStatus.value = null), 5000);
};
const templateForm = ref({
  name: '',
  description: ''
});

// ===== Computed =====
const waterPercentage = computed({
  get: () => waterStore.waterMixData.waterPercentage,
  set: (val: number) => waterStore.setWaterMix({ waterPercentage: val })
});

const wastewaterPercentage = computed({
  get: () => waterStore.waterMixData.wastewaterPercentage,
  set: (val: number) =>
    waterStore.setWaterMix({ wastewaterPercentage: val })
});

const waterSalinity = computed({
  get: () => waterStore.waterMixData.waterSalinity,
  set: (val: number) => waterStore.setWaterMix({ waterSalinity: val })
});

const ecUnit = computed({
  get: () => waterStore.ecUnit,
  set: (val: any) => waterStore.setECUnit(val)
});

const totalPercentage = computed(() => {
  return (waterPercentage.value || 0) + (wastewaterPercentage.value || 0);
});

// ردیف پساب فقط وقتی درصد پساب > 0 یا مقداری وارد شده نمایش داده می‌شود
const showWastewaterRow = computed(() => {
  if (wastewaterPercentage.value > 0) return true;

  return Object.values(waterStore.wastewaterValues).some(
    (v) => v > 0
  );
});

const showFreshWaterRow = computed(() => {
  if (wastewaterPercentage.value >= 100) return false;
  if (waterPercentage.value <= 0) return false;

  return true;
});

// ===== Helper Functions for Unit Conversion =====
// ---------- جدول: فرم و واحد ورود ----------
const allRows: WaterRow[] = WATER_GROUPS.flatMap((g) => g.rows);
const formChoice = reactive<Record<string, string>>({});
for (const g of WATER_GROUPS) for (const r of g.rows) formChoice[r.key] = r.defaultForm;
const menu = ref<{ key: string; top: number; left: number } | null>(null);
const menuRow = computed(() => (menu.value ? allRows.find((r) => r.key === menu.value!.key) || null : null));
const openFormMenu = (row: WaterRow, e: MouseEvent) => {
  if (row.forms.length < 2) return;
  if (menu.value?.key === row.key) { menu.value = null; return; }
  const r = (e.currentTarget as HTMLElement).getBoundingClientRect();
  menu.value = { key: row.key, top: r.bottom + 4, left: Math.max(8, Math.min(r.left, window.innerWidth - 248)) };
};

const currentForm = (row: WaterRow): WaterForm =>
  row.forms.find((f) => f.key === formChoice[row.key]) || row.forms[0];
const selectForm = (row: WaterRow, key: string) => {
  formChoice[row.key] = key;
  menu.value = null;
};

type Col = 'water' | 'waste';
const bag = (c: Col) =>
  (c === 'water' ? waterStore.waterValues : waterStore.wastewaterValues) as Record<string, number>;
const setIn = (c: Col, k: string, v: number) =>
  c === 'water' ? waterStore.setWaterValue(k, v) : waterStore.setWastewaterValue(k, v);
const delIn = (c: Col, k: string) =>
  c === 'water' ? waterStore.removeWaterValue(k) : waterStore.removeWastewaterValue(k);

/** متن سلول: مقدار در فرم/واحد انتخابی، یا «<x» برای زیر حد تشخیص */
const cellText = (c: Col, row: WaterRow): string => {
  const v = bag(c)[row.key] || 0;
  if (v > 0) return fmtPlain(fromStored(currentForm(row), currentUnit.value, v));
  const lt = bag(c)['lt:' + row.key] || 0;
  return lt > 0 ? '<' + fmtPlain(fromStored(currentForm(row), currentUnit.value, lt)) : '';
};

const suppliedText = (row: WaterRow): string => {
  const wp = (waterPercentage.value || 0) / 100;
  const ep = (wastewaterPercentage.value || 0) / 100;
  const v = (waterStore.waterValues[row.key] || 0) * wp + (waterStore.wastewaterValues[row.key] || 0) * ep;
  return v > 0 ? fmtPlain(fromStored(currentForm(row), currentUnit.value, v)) : '—';
};

const onCellChange = (c: Col, row: WaterRow, e: Event) => {
  const input = e.target as HTMLInputElement;
  const raw = normalizeNumberText(input.value);
  const below = raw.startsWith('<') || raw.startsWith('≤');
  const n = parseFloat(below ? raw.slice(1) : raw);

  if (raw === '') {
    delIn(c, row.key);
    delIn(c, 'lt:' + row.key);
  } else if (!Number.isFinite(n) || n < 0) {
    input.value = cellText(c, row);
    return;
  } else if (below) {
    delIn(c, row.key);
    if (n > 0) setIn(c, 'lt:' + row.key, toStored(currentForm(row), currentUnit.value, n));
    else delIn(c, 'lt:' + row.key);
  } else {
    delIn(c, 'lt:' + row.key);
    if (n > 0) setIn(c, row.key, toStored(currentForm(row), currentUnit.value, n));
    else delIn(c, row.key);
  }
  input.value = cellText(c, row);
  triggerAutoSave();
};

// ---------- EC (همیشه عدد معتبر) و pH (اختیاری) ----------
const ecText = computed(() => fmtPlain(waterSalinity.value));
const onEcChange = (e: Event) => {
  const input = e.target as HTMLInputElement;
  const n = parseFloat(normalizeNumberText(input.value));
  waterSalinity.value =
    Number.isFinite(n) && n > 0 ? n : convertECUnit(EC_STANDARDS.DEFAULT_EC, 'dS/m', ecUnit.value);
  input.value = fmtPlain(waterSalinity.value);
  triggerAutoSave();
};

const phText = computed(() => (waterStore.waterPH == null ? '' : fmtPlain(waterStore.waterPH)));
const onPhChange = (e: Event) => {
  const input = e.target as HTMLInputElement;
  const raw = normalizeNumberText(input.value);
  if (raw === '') {
    waterStore.setWaterPH(null);
  } else {
    const n = parseFloat(raw);
    if (!Number.isFinite(n) || n <= 0 || n > 14) {
      input.value = phText.value;
      return;
    }
    waterStore.setWaterPH(n);
  }
  input.value = phText.value;
  triggerAutoSave();
};

const updateWaterPercentage = (event: Event) => {
  const target = event.target as HTMLInputElement;

  let value = parseFloat(target.value) || 0;

  if (value > 100) value = 100;
  if (value < 0) value = 0;

  waterPercentage.value = value;
  wastewaterPercentage.value = 100 - value;

  triggerAutoSave();
};

const updateWastewaterPercentage = (event: Event) => {
  const target = event.target as HTMLInputElement;

  let value = parseFloat(target.value) || 0;

  if (value > 100) value = 100;
  if (value < 0) value = 0;

  wastewaterPercentage.value = value;
  waterPercentage.value = 100 - value;

  triggerAutoSave();
};

const resetWaterAnalysis = () => {
  waterStore.resetWaterData();
  showToast('تنظیمات بازنشانی شد', 'success');
  triggerAutoSave();
};

// ===== Auto-save Logic =====

const triggerAutoSave = () => {
  if (saveTimeout) {
    clearTimeout(saveTimeout);
  }

  saveStatus.value = 'saving';

  saveTimeout = setTimeout(async () => {
    await performSave();
  }, 1000);
};

const performSave = async () => {
  if (!reportStore.currentReportId) {
    saveStatus.value = 'idle';
    return;
  }

  isSaving.value = true;

  try {
    const waterPayload = {
      water_percentage:
        waterStore.waterMixData.waterPercentage,

      wastewater_percentage:
        waterStore.waterMixData.wastewaterPercentage,

      water_salinity:
        waterStore.waterMixData.waterSalinity,

      water_values:
        waterStore.waterValues,

      wastewater_values:
        waterStore.wastewaterValues
    };

    let existingAnalysis = null;

    try {
      existingAnalysis =
        await apiService.getWaterAnalysis(
          String(reportStore.currentReportId)
        );
    } catch (e) {
      // اگر آنالیز قبلی وجود نداشت، ایجاد خواهد شد.
    }

    if (existingAnalysis) {
      await apiService.updateWaterAnalysis(
        String(existingAnalysis.id),
        waterPayload
      );
    } else {
      await apiService.createWaterAnalysis(
        String(reportStore.currentReportId),
        waterPayload
      );
    }

    saveStatus.value = 'success';

    setTimeout(() => {
      saveStatus.value = 'idle';
    }, 2000);
  } catch (error: any) {
    console.error('Auto-save error:', error);
    saveStatus.value = 'idle';
  } finally {
    isSaving.value = false;
  }
};

// ===== Toast =====

const showToast = (
  msg: string,
  type: 'success' | 'error' = 'success'
) => {
  toastMessage.value = msg;
  toastType.value = type;

  setTimeout(() => {
    toastMessage.value = null;
  }, 3000);
};

// ===== Template Methods =====

const loadWaterTemplates = async () => {
  try {
    const templates = await apiService.get('/water-templates/', { params: { limit: 6 } });

    waterTemplates.value = Array.isArray(templates)
      ? templates
      : [];
  } catch (error) {
    console.error('Load water templates error:', error);
    showToast('دریافت قالب‌ها ناموفق بود؛ صفحه را دوباره باز کنید', 'error');
  }
};

// فقط مقدارهای عددی معتبر به سرور فرستاده می‌شوند (مقدار خالی یا NaN باعث خطای 422 می‌شد)
const toNumberMap = (source: Record<string, any> | null | undefined): Record<string, number> => {
  const result: Record<string, number> = {};
  for (const [key, value] of Object.entries(source || {})) {
    const num = Number(value);
    if (value !== null && value !== '' && Number.isFinite(num)) result[key] = num;
  }
  return result;
};

const extractErrorMessage = (error: any, fallback: string): string => {
  const detail = error?.response?.data?.detail;
  if (typeof detail === 'string') return detail;
  return error?.message && !String(error.message).startsWith('Request failed') ? error.message : fallback;
};

const openSaveTemplateModal = () => {
  templateForm.value = {
    name: '',
    description: ''
  };

  showSaveTemplateModal.value = true;
};

const closeSaveTemplateModal = () => {
  showSaveTemplateModal.value = false;
};

const saveWaterTemplate = async () => {
  if (!templateForm.value.name) return;

  if (waterTemplates.value.length >= 6) {
    showToast(
      'ظرفیت قالب‌های آنالیز آب تکمیل شده است',
      'error'
    );
    return;
  }

  isSavingTemplate.value = true;

  try {
    await apiService.post('/water-templates/', {
      name: templateForm.value.name,
      description:
        templateForm.value.description || null,

      water_percentage:
        waterPercentage.value,

      wastewater_percentage:
        wastewaterPercentage.value,

      water_salinity:
        waterSalinity.value,

      water_salinity_unit:
        ecUnit.value,

      water_values:
        toNumberMap(waterStore.waterValues),

      wastewater_values:
        toNumberMap(waterStore.wastewaterValues)
    });

    await loadWaterTemplates();

    closeSaveTemplateModal();

    setTemplateStatus('success', `قالب «${templateForm.value.name}» ذخیره شد (این کار گزارش را ذخیره نکرد).`);
  } catch (error: any) {
    console.error('Save water template error:', error);

    setTemplateStatus('error', extractErrorMessage(error, 'خطا در ذخیره قالب'));
  } finally {
    isSavingTemplate.value = false;
  }
};

const loadWaterTemplate = async (
  template: any
) => {
  waterPercentage.value =
    template.water_percentage;

  wastewaterPercentage.value =
    template.wastewater_percentage;

  waterSalinity.value =
    template.water_salinity;

  waterStore.setECUnit(
    template.water_salinity_unit || 'dS/m'
  );

  waterStore.wastewaterValues = {};
  waterStore.waterValues = {};

  if (template.water_values) {
    for (const [key, value] of Object.entries(
      template.water_values
    )) {
      waterStore.setWaterValue(
        key,
        value as number
      );
    }
  }

  if (template.wastewater_values) {
    for (const [key, value] of Object.entries(
      template.wastewater_values
    )) {
      waterStore.setWastewaterValue(
        key,
        value as number
      );
    }
  }

  showToast(
    `قالب "${template.name}" بارگذاری شد`,
    'success'
  );

  triggerAutoSave();
};

const deleteWaterTemplate = async (
  templateId: number
) => {
  try {
    await apiService.delete(
      `/water-templates/${templateId}`
    );

    await loadWaterTemplates();

    showToast(
      'قالب حذف شد',
      'success'
    );
  } catch (error) {
    console.error(
      'Delete water template error:',
      error
    );

    showToast(
      'خطا در حذف قالب',
      'error'
    );
  }
};

onMounted(() => {
  loadWaterTemplates();
});
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .relative,
.modal-leave-to .relative {
  transform: scale(0.95);
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translate(-50%, 10px);
}

.custom-scrollbar::-webkit-scrollbar {
  height: 6px;
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

.dark .custom-scrollbar::-webkit-scrollbar-track {
  background: #374151;
}

.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background: #4b5563;
}

.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}
</style>