<!-- frontend/src/components/features/fertilizer-db/FertilizerStatsAndTable.vue -->
<template>
  <div>
    <!-- ============================================================ -->
    <!-- کارت‌های آماری - تعاملی با فیلتر -->
    <!-- ============================================================ -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
      <!-- همه کودها -->
      <div 
        @click="setFilter(null)"
        class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border-2 p-4 flex items-center gap-3 cursor-pointer transition-all hover:shadow-md"
        :class="activeFilter === null ? 'border-primary-500 dark:border-primary-400' : 'border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-700'"
      >
        <div class="w-10 h-10 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
          <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
          </svg>
        </div>
        <div>
          <p class="text-xs text-gray-500 dark:text-gray-400">همه کودها</p>
          <p class="text-xl font-bold text-gray-900 dark:text-white tabular-nums">{{ userFertilizers.length }}</p>
        </div>
        <span v-if="activeFilter === null" class="mr-auto w-2 h-2 rounded-full bg-primary-500"></span>
      </div>
      
      <!-- کودهای معمولی -->
      <div 
        @click="setFilter('normal')"
        class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border-2 p-4 flex items-center gap-3 cursor-pointer transition-all hover:shadow-md"
        :class="activeFilter === 'normal' ? 'border-success-500 dark:border-success-400' : 'border-gray-200 dark:border-gray-700 hover:border-success-300 dark:hover:border-success-700'"
      >
        <div class="w-10 h-10 rounded-lg bg-success-50 dark:bg-success-900/30 flex items-center justify-center flex-shrink-0">
          <svg class="w-5 h-5 text-success-600 dark:text-success-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
        </div>
        <div>
          <p class="text-xs text-gray-500 dark:text-gray-400">معمولی</p>
          <p class="text-xl font-bold text-success-600 dark:text-success-400 tabular-nums">{{ normalFertilizersCount }}</p>
        </div>
        <span v-if="activeFilter === 'normal'" class="mr-auto w-2 h-2 rounded-full bg-success-500"></span>
      </div>

      <!-- اسیدها -->
      <div 
        @click="setFilter('acid')"
        class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border-2 p-4 flex items-center gap-3 cursor-pointer transition-all hover:shadow-md"
        :class="activeFilter === 'acid' ? 'border-warning-500 dark:border-warning-400' : 'border-gray-200 dark:border-gray-700 hover:border-warning-300 dark:hover:border-warning-700'"
      >
        <div class="w-10 h-10 rounded-lg bg-warning-50 dark:bg-warning-900/30 flex items-center justify-center flex-shrink-0">
          <svg class="w-5 h-5 text-warning-600 dark:text-warning-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
          </svg>
        </div>
        <div>
          <p class="text-xs text-gray-500 dark:text-gray-400">اسیدها</p>
          <p class="text-xl font-bold text-warning-600 dark:text-warning-400 tabular-nums">{{ acidFertilizersCount }}</p>
        </div>
        <span v-if="activeFilter === 'acid'" class="mr-auto w-2 h-2 rounded-full bg-warning-500"></span>
      </div>

      <!-- کودهای سیستمی (کپی شده از سیستم) -->
      <div 
        @click="setFilter('system')"
        class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border-2 p-4 flex items-center gap-3 cursor-pointer transition-all hover:shadow-md"
        :class="activeFilter === 'system' ? 'border-indigo-500 dark:border-indigo-400' : 'border-gray-200 dark:border-gray-700 hover:border-indigo-300 dark:hover:border-indigo-700'"
      >
        <div class="w-10 h-10 rounded-lg bg-indigo-50 dark:bg-indigo-900/30 flex items-center justify-center flex-shrink-0">
          <svg class="w-5 h-5 text-indigo-600 dark:text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
          </svg>
        </div>
        <div>
          <p class="text-xs text-gray-500 dark:text-gray-400">کپی از سیستمی</p>
          <p class="text-xl font-bold text-indigo-600 dark:text-indigo-400 tabular-nums">{{ systemCopiedCount }}</p>
        </div>
        <span v-if="activeFilter === 'system'" class="mr-auto w-2 h-2 rounded-full bg-indigo-500"></span>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- نوار ابزار -->
    <!-- ============================================================ -->
    <div class="mt-4 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <div class="flex flex-col sm:flex-row gap-3 items-center justify-between">
        
        <!-- جستجو -->
        <div class="relative flex-1 w-full sm:max-w-xs">
          <svg class="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="جستجو..."
            class="w-full pr-10 pl-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
          />
        </div>

        <!-- دکمه‌های عملیاتی -->
        <div class="flex flex-wrap gap-2 w-full sm:w-auto justify-end">
          <!-- دکمه فیلتر -->
          <button
            @click="openFilterModal"
            class="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors flex items-center gap-2 border border-gray-200 dark:border-gray-600"
            :class="hasActiveFilters ? 'border-primary-400 dark:border-primary-400 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300' : ''"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"/>
            </svg>
            <span>فیلتر</span>
            <span v-if="hasActiveFilters" class="w-2 h-2 rounded-full bg-primary-500"></span>
          </button>

          <!-- دکمه افزودن کود -->
          <button
            @click="$emit('open-modal')"
            class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors flex items-center gap-2 shadow-sm hover:shadow-md"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            <span class="hidden sm:inline">افزودن کود</span>
            <span class="sm:hidden">افزودن</span>
          </button>

          <!-- دکمه پاک کردن جدول -->
          <button
            @click="clearTable"
            v-if="userFertilizers.length > 0"
            class="px-4 py-2 bg-danger-50 dark:bg-danger-900/20 text-danger-600 dark:text-danger-400 rounded-lg hover:bg-danger-100 dark:hover:bg-danger-900/40 transition-colors flex items-center gap-2 border border-danger-200 dark:border-danger-800"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
            <span class="hidden sm:inline">پاک کردن</span>
          </button>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- نمایش نتایج -->
    <!-- ============================================================ -->
    <div v-if="filteredFertilizers.length > 0" class="mt-4">
      <!-- هدر نتایج -->
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center gap-2">
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
            {{ filteredFertilizers.length }} کود
          </span>
          <span v-if="hasActiveFilters" class="text-xs text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/20 px-2 py-0.5 rounded-full">
            فیلتر فعال
          </span>
        </div>
        <button
          v-if="hasActiveFilters"
          @click="clearAllFilters"
          class="text-xs text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 transition-colors"
        >
          پاک کردن فیلترها
        </button>
      </div>

      <!-- ============================================================ -->
      <!-- دسکتاپ: جدول -->
      <!-- ============================================================ -->
      <div class="hidden sm:block bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
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
                    <!-- آیکون فرم با رنگ مناسب -->
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
                      <p class="font-medium text-gray-900 dark:text-white truncate">{{ fertilizer.name }}</p>
                      <div class="flex items-center gap-2 mt-0.5 flex-wrap">
                        <span v-if="fertilizer.brand" class="text-[10px] text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-700 px-1.5 py-0.5 rounded">
                          {{ fertilizer.brand }}
                        </span>
                        <!-- برچسب اسید -->
                        <span v-if="fertilizer.isAcid" class="text-[10px] px-1.5 py-0.5 bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400 rounded">
                          اسید
                        </span>
                        <!-- برچسب سیستمی - برای کودهای کپی شده از سیستم -->
                        <span v-if="fertilizer.sourceSystemId" class="text-[10px] px-1.5 py-0.5 bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-400 rounded border border-indigo-200 dark:border-indigo-800">
                          سیستمی
                        </span>
                      </div>
                    </div>
                  </div>
                </td>
                
                <!-- فرم -->
                <td class="px-4 py-3 text-center">
                  <span class="text-xs font-medium px-2 py-1 rounded-full" :class="getFormBadgeClass(fertilizer)">
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
                  <span v-if="fertilizer.phLevel !== undefined && fertilizer.phLevel !== null" class="font-semibold text-gray-900 dark:text-white tabular-nums">
                    {{ fertilizer.phLevel }}
                  </span>
                  <span v-else class="text-gray-400 dark:text-gray-500 text-xs">-</span>
                </td>
                
                <!-- قیمت -->
                <td class="px-4 py-3 text-center">
                  <span class="font-semibold text-gray-900 dark:text-white tabular-nums">
                    {{ Number(fertilizer.pricePerKg || 0).toLocaleString('fa-IR') }}
                  </span>
                </td>
                
                <!-- عناصر -->
                <td class="px-4 py-3">
                  <div class="flex flex-wrap gap-1 justify-center">
                    <template v-if="hasElements(fertilizer)">
                      <span
                        v-for="(percentage, element) in getActiveElements(fertilizer)"
                        :key="element"
                        class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium border"
                        :class="getElementBadgeClass(element)"
                        :title="`${element}: ${percentage}%`"
                      >
                        <span class="font-bold">{{ element }}</span>
                        <span class="mx-1 text-gray-400">|</span>
                        <span>{{ percentage }}%</span>
                      </span>
                    </template>
                    <span v-else class="text-xs text-gray-400 dark:text-gray-500 italic">-</span>
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

      <!-- ============================================================ -->
      <!-- موبایل: کارت‌ها -->
      <!-- ============================================================ -->
      <div class="sm:hidden space-y-3">
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
                <p class="font-semibold text-gray-900 dark:text-white truncate">{{ fertilizer.name }}</p>
                <div class="flex items-center gap-1.5 mt-0.5 flex-wrap">
                  <span v-if="fertilizer.brand" class="text-[10px] text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-700 px-1.5 py-0.5 rounded">
                    {{ fertilizer.brand }}
                  </span>
                  <span class="text-[10px] font-medium px-1.5 py-0.5 rounded-full" :class="getFormBadgeClass(fertilizer)">
                    {{ getFormLabel(fertilizer.form) }}
                  </span>
                  <span v-if="fertilizer.isAcid" class="text-[10px] px-1.5 py-0.5 bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400 rounded">
                    اسید
                  </span>
                  <span v-if="fertilizer.sourceSystemId" class="text-[10px] px-1.5 py-0.5 bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-400 rounded border border-indigo-200 dark:border-indigo-800">
                    سیستمی
                  </span>
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
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
              </button>
            </div>
          </div>
          
          <!-- جزئیات کارت موبایل -->
          <div class="mt-3 pt-3 border-t border-gray-100 dark:border-gray-700 grid grid-cols-3 gap-2 text-center">
            <div>
              <p class="text-[10px] text-gray-400 dark:text-gray-500">خلوص</p>
              <p class="text-sm font-semibold text-gray-900 dark:text-white">{{ fertilizer.concentration || 100 }}%</p>
            </div>
            <div>
              <p class="text-[10px] text-gray-400 dark:text-gray-500">pH</p>
              <p class="text-sm font-semibold text-gray-900 dark:text-white">{{ fertilizer.phLevel || '-' }}</p>
            </div>
            <div>
              <p class="text-[10px] text-gray-400 dark:text-gray-500">قیمت</p>
              <p class="text-sm font-semibold text-gray-900 dark:text-white">{{ Number(fertilizer.pricePerKg || 0).toLocaleString('fa-IR') }}</p>
            </div>
          </div>
          
          <!-- عناصر در موبایل -->
          <div class="mt-2 pt-2 border-t border-gray-100 dark:border-gray-700">
            <p class="text-[10px] text-gray-400 dark:text-gray-500 mb-1.5">عناصر تشکیل‌دهنده</p>
            <div class="flex flex-wrap gap-1">
              <template v-if="hasElements(fertilizer)">
                <span
                  v-for="(percentage, element) in getActiveElements(fertilizer)"
                  :key="element"
                  class="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-medium border"
                  :class="getElementBadgeClass(element)"
                >
                  {{ element }}: {{ percentage }}%
                </span>
              </template>
              <span v-else class="text-xs text-gray-400 dark:text-gray-500 italic">بدون عنصر</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- پیام خالی بودن -->
    <!-- ============================================================ -->
    <div v-else-if="!isLoading" class="mt-4 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-12 text-center">
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
    <Teleport to="body">
      <div
        v-if="showFilterModal"
        class="fixed inset-0 z-[100] overflow-y-auto"
        role="dialog"
        aria-modal="true"
      >
        <div class="fixed inset-0 bg-gray-900/60 backdrop-blur-sm" @click="closeFilterModal"></div>
        <div class="flex min-h-full items-center justify-center p-4">
          <div class="relative w-full max-w-md bg-white dark:bg-gray-800 rounded-xl shadow-2xl overflow-hidden">
            <!-- هدر مودال -->
            <div class="bg-gradient-to-l from-primary-600 to-primary-700 dark:from-primary-800 dark:to-primary-900 px-6 py-4 flex items-center justify-between">
              <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"/>
                </svg>
                <h3 class="text-lg font-bold text-white">فیلترهای پیشرفته</h3>
              </div>
              <button
                @click="closeFilterModal"
                class="text-white/70 hover:text-white transition-colors p-1 rounded-lg hover:bg-white/10"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>

            <!-- بدنه مودال -->
            <div class="p-6 space-y-4 max-h-[60vh] overflow-y-auto custom-scrollbar">
              <!-- فرم فیزیکی -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
                  فرم فیزیکی
                </label>
                <select
                  v-model="filterForm"
                  class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
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
                    <span class="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-gray-400">از</span>
                    <input
                      v-model.number="priceMin"
                      type="number"
                      placeholder="۰"
                      min="0"
                      class="w-full px-3 py-2.5 pr-8 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                    />
                  </div>
                  <span class="text-gray-400">تا</span>
                  <div class="flex-1 relative">
                    <span class="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-gray-400">تا</span>
                    <input
                      v-model.number="priceMax"
                      type="number"
                      placeholder="∞"
                      min="0"
                      class="w-full px-3 py-2.5 pr-8 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
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
                  class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
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

              <!-- وضعیت اسید -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
                  نوع کود
                </label>
                <div class="flex gap-3">
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      v-model="filterType"
                      value="all"
                      class="w-4 h-4 text-primary-600 focus:ring-primary-500"
                    />
                    <span class="text-sm text-gray-700 dark:text-gray-300">همه</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      v-model="filterType"
                      value="normal"
                      class="w-4 h-4 text-success-600 focus:ring-success-500"
                    />
                    <span class="text-sm text-gray-700 dark:text-gray-300">معمولی</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      v-model="filterType"
                      value="acid"
                      class="w-4 h-4 text-warning-600 focus:ring-warning-500"
                    />
                    <span class="text-sm text-gray-700 dark:text-gray-300">اسید</span>
                  </label>
                </div>
              </div>

              <!-- وضعیت سیستمی -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
                  منشأ کود
                </label>
                <div class="flex gap-3">
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      v-model="filterSource"
                      value="all"
                      class="w-4 h-4 text-primary-600 focus:ring-primary-500"
                    />
                    <span class="text-sm text-gray-700 dark:text-gray-300">همه</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      v-model="filterSource"
                      value="user"
                      class="w-4 h-4 text-success-600 focus:ring-success-500"
                    />
                    <span class="text-sm text-gray-700 dark:text-gray-300">شخصی</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      v-model="filterSource"
                      value="system"
                      class="w-4 h-4 text-indigo-600 focus:ring-indigo-500"
                    />
                    <span class="text-sm text-gray-700 dark:text-gray-300">سیستمی</span>
                  </label>
                </div>
              </div>
            </div>

            <!-- فوتر مودال -->
            <div class="bg-gray-50 dark:bg-gray-700/30 px-6 py-4 border-t border-gray-200 dark:border-gray-600 flex gap-3">
              <button
                @click="resetFilters"
                class="flex-1 px-4 py-2.5 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors text-sm font-medium"
              >
                بازنشانی
              </button>
              <button
                @click="applyFilters"
                class="flex-1 px-4 py-2.5 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors text-sm font-medium shadow-sm hover:shadow-md"
              >
                اعمال فیلتر
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
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
const filterType = ref<'all' | 'normal' | 'acid'>('all');
const filterSource = ref<'all' | 'user' | 'system'>('all');
const showFilterModal = ref(false);

// ============================================================
// Computed
// ============================================================
const normalFertilizersCount = computed(() => {
  return props.userFertilizers.filter((f: any) => !f.isAcid).length;
});

const acidFertilizersCount = computed(() => {
  return props.userFertilizers.filter((f: any) => f.isAcid).length;
});

// تعداد کودهای کپی شده از سیستم
const systemCopiedCount = computed(() => {
  return props.userFertilizers.filter((f: any) => f.sourceSystemId).length;
});

const hasActiveFilters = computed(() => {
  return !!(searchQuery.value || 
    filterForm.value !== 'all' || 
    priceMin.value || 
    priceMax.value || 
    filterElement.value !== 'all' ||
    filterType.value !== 'all' ||
    filterSource.value !== 'all' ||
    props.activeFilter);
});

const filteredFertilizers = computed(() => {
  let result = props.userFertilizers;
  
  // فیلتر از کارت‌ها
  if (props.activeFilter === 'normal') {
    result = result.filter((f: any) => !f.isAcid);
  } else if (props.activeFilter === 'acid') {
    result = result.filter((f: any) => f.isAcid);
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
    result = result.filter((f: any) => (f.pricePerKg || 0) >= priceMin.value!);
  }
  if (priceMax.value !== null && priceMax.value > 0) {
    result = result.filter((f: any) => (f.pricePerKg || 0) <= priceMax.value!);
  }
  
  // عناصر خاص
  if (filterElement.value !== 'all') {
    result = result.filter((f: any) => {
      if (!f.elements) return false;
      return f.elements[filterElement.value] && f.elements[filterElement.value] > 0;
    });
  }
  
  // نوع کود (اسید/معمولی)
  if (filterType.value === 'acid') {
    result = result.filter((f: any) => f.isAcid);
  } else if (filterType.value === 'normal') {
    result = result.filter((f: any) => !f.isAcid);
  }
  
  // منشأ کود (شخصی/سیستمی)
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
  return classes[fertilizer.form] || 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400';
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
  return classes[fertilizer.form] || 'text-gray-600 dark:text-gray-400';
};

const getElementBadgeClass = (element: string): string => {
  const cationElements = ['N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Fe', 'Mn', 'Zn', 'Cu'];
  const anionElements = ['N-NO3', 'P', 'S', 'Cl', 'B', 'Mo'];
  
  if (cationElements.includes(element)) {
    return 'bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-800';
  } else if (anionElements.includes(element)) {
    return 'bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300 border-red-200 dark:border-red-800';
  }
  return 'bg-gray-50 dark:bg-gray-700 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-600';
};

const hasElements = (fertilizer: any): boolean => {
  if (!fertilizer.elements) return false;
  return Object.values(fertilizer.elements).some((v: any) => v && v > 0);
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
  if (filterForm.value !== 'all' || priceMin.value || priceMax.value || filterElement.value !== 'all' || filterType.value !== 'all' || filterSource.value !== 'all') {
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
  searchQuery.value = '';
};

const clearAllFilters = () => {
  resetFilters();
  emit('filter-change', null);
  closeFilterModal();
};

const clearTable = () => {
  if (confirm('آیا از پاک کردن تمام کودهای شخصی اطمینان دارید؟ این عملیات غیرقابل بازگشت است.')) {
    emit('clear-table');
  }
};
</script>

<style scoped>
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