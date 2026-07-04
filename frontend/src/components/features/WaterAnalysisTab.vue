<template>
<div class="space-y-6">
<!-- ============================================================ -->
<!-- هدر با توضیحات و وضعیت ذخیره‌سازی -->
<!-- ============================================================ -->
<div class="bg-primary-50 dark:bg-primary-900/20 border-r-4 border-primary-500 rounded-lg p-4 flex justify-between items-start">
<div>
<p class="text-gray-700 dark:text-gray-300 text-sm leading-relaxed">
مقادیر آب و پساب را در جدول زیر وارد کنید. نرم‌افزار به صورت خودکار مقادیر تامینی را محاسبه می‌کند.
<br>
<span class="text-xs text-primary-600 dark:text-primary-400 font-medium mt-1 inline-block">
تغییرات شما به صورت خودکار و لحظه‌ای ذخیره می‌شوند.
</span>
</p>
</div>
<!-- نشانگر وضعیت ذخیره‌سازی -->
<div v-if="isSaving || saveStatus === 'success'" class="flex items-center gap-2 text-xs animate-fade-in">
<span v-if="isSaving" class="flex items-center gap-1 text-gray-500 dark:text-gray-400">
<svg class="animate-spin h-3 w-3" fill="none" viewBox="0 0 24 24">
<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
</svg>
در حال ذخیره...
</span>
<span v-else-if="saveStatus === 'success'" class="flex items-center gap-1 text-success-600 dark:text-success-400">
<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
</svg>
ذخیره شد
</span>
</div>
</div>

<!-- ============================================================ -->
<!-- بخش تنظیمات درصد -->
<!-- ============================================================ -->
<div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-5">
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4">
<!-- درصد آب -->
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">استفاده از آب (%)</label>
<div class="relative">
<input
type="number"
:value="waterPercentage"
@input="updateWaterPercentage($event)"
min="0"
max="100"
class="w-full px-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
/>
<span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm">%</span>
</div>
</div>
<!-- درصد پساب -->
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">استفاده از پساب (%)</label>
<div class="relative">
<input
type="number"
:value="wastewaterPercentage"
@input="updateWastewaterPercentage($event)"
min="0"
max="100"
class="w-full px-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
/>
<span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm">%</span>
</div>
</div>
</div>

<!-- هشدار مجموع درصد -->
<div v-if="totalPercentage !== 100" class="mt-4 bg-yellow-50 dark:bg-yellow-900/20 border-r-4 border-yellow-500 rounded-lg p-3 flex items-start gap-2">
<svg class="w-5 h-5 text-yellow-600 dark:text-yellow-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
</svg>
<p class="text-yellow-700 dark:text-yellow-400 text-sm">
مجموع درصد آب و پساب باید برابر ۱۰۰ باشد. (فعلاً {{ totalPercentage }}٪)
<br>
<span class="text-xs opacity-80">نرم‌افزار به صورت خودکار درصد پساب را تنظیم می‌کند.</span>
</p>
</div>
</div>

<!-- ============================================================ -->
<!-- نوار ابزار (واحد + دکمه قالب) - بهبود یافته برای موبایل -->
<!-- ============================================================ -->
<div class="flex flex-wrap items-center gap-3 bg-white dark:bg-gray-800 p-3 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
  <!-- بخش چپ: عنوان + واحد -->
  <div class="flex flex-wrap items-center gap-2 flex-1 min-w-[200px]">
    <h3 class="text-base font-semibold text-gray-900 dark:text-white flex items-center gap-2 whitespace-nowrap">
      <svg class="w-5 h-5 text-primary-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
      </svg>
      <span class="hidden xs:inline">جدول آنالیز عناصر</span>
      <span class="xs:hidden">آنالیز</span>
    </h3>
    
    <!-- انتخاب واحد -->
    <div class="flex items-center gap-1.5 mr-1 sm:mr-0">
      <label class="text-xs sm:text-sm text-gray-500 dark:text-gray-400">واحد:</label>
      <select
        v-model="currentUnit"
        class="px-1.5 sm:px-3 py-1 sm:py-1.5 text-xs sm:text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 transition-all"
      >
        <option value="ppm">PPM</option>
        <option value="meq">MEQ/L</option>
        <option value="mmol">MMOL/L</option>
      </select>
    </div>
  </div>

  <!-- بخش راست: دکمه‌ها -->
  <div class="flex items-center gap-1.5 sm:gap-2 flex-wrap w-full sm:w-auto justify-end">
    <!-- دکمه ذخیره قالب جدید -->
    <button
      @click="openSaveTemplateModal"
      class="flex-1 sm:flex-none px-2.5 sm:px-4 py-1.5 sm:py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors text-xs sm:text-sm flex items-center justify-center gap-1 sm:gap-1.5 shadow-sm hover:shadow-md min-w-[70px] sm:min-w-0"
    >
      <svg class="w-3.5 h-3.5 sm:w-4 sm:h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/>
      </svg>
      <span class="hidden xs:inline">ذخیره قالب جدید</span>
      <span class="xs:hidden">ذخیره قالب</span>
    </button>
    
    <!-- دکمه بازنشانی -->
    <button
      @click="resetWaterAnalysis"
      class="flex-1 sm:flex-none px-2.5 sm:px-4 py-1.5 sm:py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors text-xs sm:text-sm flex items-center justify-center gap-1 sm:gap-1.5 min-w-[60px] sm:min-w-0"
      title="بازنشانی تمام مقادیر"
    >
      <svg class="w-3.5 h-3.5 sm:w-4 sm:h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
      </svg>
      <span class="hidden xs:inline">بازنشانی</span>
      <span class="xs:hidden">بازنشانی</span>
    </button>
  </div>
</div>

<!-- ============================================================ -->
<!-- جدول آنالیز آب و پساب (ظاهر کاملاً ساده و تخت) -->
<!-- ============================================================ -->
<div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
<div class="overflow-x-auto custom-scrollbar">
<table class="w-full text-sm border-collapse min-w-[800px]">
<thead>
<tr>
<th class="sticky right-0 z-10 bg-gray-50 dark:bg-gray-700 px-4 py-3 text-right text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[100px] shadow-sm">
عنصر
</th>
<th v-for="el in waterElements" :key="el" class="px-3 py-3 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border-b border-gray-200 dark:border-gray-600 text-center min-w-[90px]">
<div class="flex flex-col items-center gap-1">
<span>{{ el }}</span>
<!-- واحد EC فقط برای ستون EC -->
<select
v-if="el === 'EC'"
v-model="ecUnit"
class="text-[10px] bg-transparent border-none focus:ring-0 cursor-pointer text-primary-600 dark:text-primary-400 font-bold p-0 h-auto"
>
<option value="dS/m">dS/m</option>
<option value="mS/cm">mS/cm</option>
<option value="μS/cm">μS/cm</option>
</select>
</div>
</th>
</tr>
</thead>
<tbody>
<!-- ردیف پساب -->
<tr v-if="showWastewaterRow" class="hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors group">
<td class="sticky right-0 z-10 bg-white dark:bg-gray-800 px-4 py-2 text-right font-medium text-gray-600 dark:text-gray-400 border-l border-gray-100 dark:border-gray-700 shadow-sm">
<div class="flex items-center gap-2">
<span class="w-2 h-2 rounded-full bg-orange-400"></span>
پساب
</div>
</td>
<td v-for="el in waterElements" :key="'waste-'+el" class="px-2 py-2 border-l border-gray-100 dark:border-gray-700 text-center relative">
<!-- ورودی عددی برای همه عناصر (شامل EC و pH) -->
<input
type="number"
:value="getDisplayValue('waste', el)"
@input="updateWastewaterValue(el, $event)"
step="0.01"
min="0"
class="w-full max-w-[80px] mx-auto px-2 py-1.5 text-center bg-transparent border border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 rounded transition-all duration-200 text-gray-700 dark:text-gray-300"
placeholder="۰"
/>
</td>
</tr>
<!-- ردیف آب -->
<tr class="hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors group">
<td class="sticky right-0 z-10 bg-white dark:bg-gray-800 px-4 py-2 text-right font-medium text-gray-600 dark:text-gray-400 border-l border-gray-100 dark:border-gray-700 shadow-sm">
<div class="flex items-center gap-2">
<span class="w-2 h-2 rounded-full bg-blue-500"></span>
آب تازه
</div>
</td>
<td v-for="el in waterElements" :key="'water-'+el" class="px-2 py-2 border-l border-gray-100 dark:border-gray-700 text-center relative">
<!-- ورودی عددی برای همه عناصر (شامل EC و pH) -->
<input
type="number"
:value="getDisplayValue('water', el)"
@input="updateWaterValue(el, $event)"
step="0.01"
min="0"
class="w-full max-w-[80px] mx-auto px-2 py-1.5 text-center bg-transparent border border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 rounded transition-all duration-200 text-gray-700 dark:text-gray-300"
placeholder="۰"
/>
</td>
</tr>
<!-- ردیف مقادیر تامینی (محاسباتی) -->
<tr class="bg-primary-50 dark:bg-primary-900/10 border-t-2 border-primary-100 dark:border-primary-900/30">
<td class="sticky right-0 z-10 bg-primary-50 dark:bg-primary-900/20 px-4 py-3 text-right font-bold text-primary-700 dark:text-primary-400 border-l border-primary-100 dark:border-primary-900/30 shadow-sm">
<div class="flex items-center gap-2">
<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
</svg>
مقادیر تامینی
</div>
</td>
<td v-for="el in waterElements" :key="'final-'+el" class="px-3 py-3 border-l border-primary-100 dark:border-primary-900/30 text-center font-bold text-primary-700 dark:text-primary-400 tabular-nums">
{{ getFinalDisplayValue(el) }}
</td>
</tr>
</tbody>
</table>
</div>
</div>

<!-- ============================================================ -->
<!-- بخش قالب‌های ذخیره شده -->
<!-- ============================================================ -->
<div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-5">
<div class="flex items-center justify-between mb-4">
<h3 class="text-base font-semibold text-gray-900 dark:text-white flex items-center gap-2">
<svg class="w-5 h-5 text-indigo-600 dark:text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
</svg>
قالب‌های ذخیره شده من
</h3>
</div>

<!-- لیست قالب‌ها -->
<div v-if="waterTemplates.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
<div
v-for="template in waterTemplates"
:key="template.id"
class="group relative bg-gray-50 dark:bg-gray-700/30 rounded-lg p-3 border border-gray-200 dark:border-gray-600 hover:border-indigo-300 dark:hover:border-indigo-700 transition-all hover:shadow-md"
>
<div class="flex items-start justify-between mb-2">
<h4 class="font-medium text-gray-900 dark:text-white text-sm truncate pr-6">
{{ template.name }}
</h4>
<div class="absolute top-2 left-2 flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
<button
@click="loadWaterTemplate(template)"
class="p-1.5 rounded bg-white dark:bg-gray-600 text-indigo-600 dark:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-gray-500 shadow-sm"
title="بارگذاری"
>
<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/>
</svg>
</button>
<button
@click="deleteWaterTemplate(template.id)"
class="p-1.5 rounded bg-white dark:bg-gray-600 text-danger-600 dark:text-danger-400 hover:bg-danger-50 dark:hover:bg-gray-500 shadow-sm"
title="حذف"
>
<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
</svg>
</button>
</div>
</div>
<!-- نمایش جزئیات کامل قالب -->
<div class="space-y-1 text-[10px] text-gray-500 dark:text-gray-400 bg-white dark:bg-gray-700/50 rounded p-2">
<div class="flex justify-between">
<span>آب: {{ template.water_percentage }}%</span>
<span>EC: {{ template.water_salinity }} {{ template.water_salinity_unit }}</span>
</div>
<div v-if="template.water_ph" class="flex justify-between">
<span>pH آب: {{ template.water_ph }}</span>
</div>
<div v-if="template.description" class="mt-1 pt-1 border-t border-gray-200 dark:border-gray-600 italic text-gray-600 dark:text-gray-300">
"{{ template.description }}"
</div>
<!-- نمایش تعداد عناصر وارد شده -->
<div class="mt-1 flex gap-2">
<span v-if="template.water_values && Object.keys(template.water_values).length > 0" class="bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 px-1.5 rounded">
{{ Object.keys(template.water_values).filter(k => template.water_values[k] > 0).length }} عنصر آب
</span>
<span v-if="template.wastewater_values && Object.keys(template.wastewater_values).length > 0" class="bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-400 px-1.5 rounded">
{{ Object.keys(template.wastewater_values).filter(k => template.wastewater_values[k] > 0).length }} عنصر پساب
</span>
</div>
</div>
</div>
</div>
<div v-else class="text-center py-8 bg-gray-50 dark:bg-gray-700/20 rounded-lg border-2 border-dashed border-gray-200 dark:border-gray-600">
<svg class="w-10 h-10 mx-auto text-gray-300 dark:text-gray-500 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/>
</svg>
<p class="text-gray-500 dark:text-gray-400 text-sm">هنوز قالبی ذخیره نشده است</p>
<p class="text-xs text-gray-400 dark:text-gray-500 mt-1">با کلیک روی دکمه "ذخیره قالب جدید" شروع کنید</p>
</div>
</div>

<!-- ============================================================ -->
<!-- مودال ذخیره قالب -->
<!-- ============================================================ -->
<Teleport to="body">
<Transition name="modal">
<div v-if="showSaveTemplateModal" class="fixed inset-0 z-[100] overflow-y-auto" role="dialog">
<div class="fixed inset-0 bg-gray-900/75 backdrop-blur-sm" @click="closeSaveTemplateModal"></div>
<div class="flex min-h-full items-center justify-center p-4">
<div class="relative w-full max-w-md bg-white dark:bg-gray-800 rounded-2xl shadow-2xl overflow-hidden transform transition-all">
<div class="bg-gradient-to-l from-indigo-600 to-indigo-700 dark:from-indigo-800 dark:to-indigo-900 px-6 py-4 flex items-center justify-between">
<h3 class="text-lg font-bold text-white flex items-center gap-2">
<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/>
</svg>
ذخیره تنظیمات فعلی
</h3>
<button @click="closeSaveTemplateModal" class="text-white/80 hover:text-white transition-colors">
<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
</svg>
</button>
</div>
<div class="p-6 space-y-4">
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">نام قالب <span class="text-danger-500">*</span></label>
<input
type="text"
v-model="templateForm.name"
class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
placeholder="مثال: آب چاه شماره ۱ - تابستان"
autofocus
/>
</div>
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">توضیحات (اختیاری)</label>
<textarea
v-model="templateForm.description"
rows="2"
class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all resize-none"
placeholder="توضیحات تکمیلی..."
></textarea>
</div>
<div class="bg-indigo-50 dark:bg-indigo-900/20 rounded-lg p-3 text-xs text-indigo-700 dark:text-indigo-300 border border-indigo-100 dark:border-indigo-800">
<p class="flex items-center gap-1.5">
<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
تمام مقادیر جاری (درصد آب، EC، pH و عناصر) در این قالب ذخیره خواهند شد.
</p>
</div>
</div>
<div class="bg-gray-50 dark:bg-gray-700/30 px-6 py-4 flex flex-row-reverse gap-3">
<button
@click="saveWaterTemplate"
:disabled="isSavingTemplate || !templateForm.name"
class="px-5 py-2.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium flex items-center gap-2 shadow-lg shadow-indigo-500/30"
>
<svg v-if="isSavingTemplate" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
</svg>
{{ isSavingTemplate ? 'در حال ذخیره...' : 'ذخیره قالب' }}
</button>
<button
@click="closeSaveTemplateModal"
class="px-5 py-2.5 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-600 border border-gray-300 dark:border-gray-600 transition-colors font-medium"
>
انصراف
</button>
</div>
</div>
</div>
</div>
</Transition>
</Teleport>

<!-- ============================================================ -->
<!-- پیام Toast -->
<!-- ============================================================ -->
<Transition name="fade">
<div v-if="toastMessage" class="fixed bottom-6 left-1/2 -translate-x-1/2 z-[200] px-6 py-3 rounded-xl shadow-2xl flex items-center gap-3 text-sm font-medium"
:class="toastType === 'success' ? 'bg-success-600 text-white' : 'bg-danger-600 text-white'"
>
<svg v-if="toastType === 'success'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
</svg>
<svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
</svg>
<span>{{ toastMessage }}</span>
</div>
</Transition>
</div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useWaterStore, EC_STANDARDS, convertECUnit, calculateTDS } from '@/store/modules/waterStore';
import { apiService } from '@/services/apiService';
import { useReportStore } from '@/store/modules/reportStore';

// ===== Store =====
const waterStore = useWaterStore();
const reportStore = useReportStore();

// ===== State =====
const waterElements = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo', 'EC', 'pH'];
const currentUnit = ref<'ppm' | 'meq' | 'mmol'>('ppm');

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
const templateForm = ref({ name: '', description: '' });

// ===== Computed =====
const waterPercentage = computed({
get: () => waterStore.waterMixData.waterPercentage,
set: (val: number) => waterStore.setWaterMix({ waterPercentage: val })
});

const wastewaterPercentage = computed({
get: () => waterStore.waterMixData.wastewaterPercentage,
set: (val: number) => waterStore.setWaterMix({ wastewaterPercentage: val })
});

const waterSalinity = computed({
get: () => waterStore.waterMixData.waterSalinity,
set: (val: number) => waterStore.setWaterMix({ waterSalinity: val })
});

const ecUnit = computed({
get: () => waterStore.ecUnit,
set: (val: any) => waterStore.setECUnit(val)
});

const waterPH = computed({
get: () => waterStore.waterPH,
set: (val: number | null) => waterStore.setWaterPH(val)
});

const totalPercentage = computed(() => {
return (waterPercentage.value || 0) + (wastewaterPercentage.value || 0);
});

// ردیف پساب فقط وقتی درصد پساب > 0 یا مقداری وارد شده نمایش داده می‌شود
const showWastewaterRow = computed(() => {
if (wastewaterPercentage.value > 0) return true;
return Object.values(waterStore.wastewaterValues).some(v => v > 0);
});

// ===== Helper Functions for Unit Conversion =====
// وزن مولکولی و ظرفیت برای تبدیل واحد
const ELEMENT_DATA: Record<string, { mw: number; valence: number }> = {
'N-NO3': { mw: 62.0049, valence: 1 },
'P': { mw: 30.9738, valence: 1 }, // فرض بر PO4
'S': { mw: 32.065, valence: 1 }, // فرض بر SO4
'N-NH4': { mw: 18.0385, valence: 1 },
'K': { mw: 39.0983, valence: 1 },
'Ca': { mw: 40.078, valence: 2 },
'Fe': { mw: 55.845, valence: 2 },
'Mn': { mw: 54.938, valence: 2 },
'Zn': { mw: 65.38, valence: 2 },
'B': { mw: 10.81, valence: 1 },
'Cu': { mw: 63.546, valence: 2 },
'Mo': { mw: 95.95, valence: 2 }
};

function convertToDisplay(value: number, element: string, unit: string): number {
if (element === 'EC' || element === 'pH') return value;
if (!ELEMENT_DATA[element]) return value;

const { mw, valence } = ELEMENT_DATA[element];

if (unit === 'ppm') return value;
if (unit === 'meq') return (value * valence) / mw;
if (unit === 'mmol') return value / mw;

return value;
}

function convertFromDisplay(displayValue: number, element: string, unit: string): number {
if (element === 'EC' || element === 'pH') return displayValue;
if (!ELEMENT_DATA[element]) return displayValue;

const { mw, valence } = ELEMENT_DATA[element];

if (unit === 'ppm') return displayValue;
if (unit === 'meq') return (displayValue * mw) / valence;
if (unit === 'mmol') return displayValue * mw;

return displayValue;
}

// ===== Methods =====

/**
* دریافت مقدار نمایشی برای جدول (با تبدیل واحد)
*/
const getDisplayValue = (type: 'water' | 'waste', element: string): number => {
let rawValue = 0;
if (type === 'water') {
if (element === 'EC') rawValue = waterSalinity.value;
else if (element === 'pH') rawValue = waterPH.value || 0;
else rawValue = (waterStore.waterValues as any)[element] || 0;
} else {
rawValue = (waterStore.wastewaterValues as any)[element] || 0;
}
return parseFloat(convertToDisplay(rawValue, element, currentUnit.value).toFixed(3));
};

/**
* دریافت مقدار نهایی نمایشی (با تبدیل واحد)
*/
const getFinalDisplayValue = (element: string): string => {
if (element === 'EC' || element === 'pH') return '-';
const waterPct = (waterPercentage.value || 0) / 100;
const wastePct = (wastewaterPercentage.value || 0) / 100;
const waterVal = (waterStore.waterValues as any)[element] || 0;
const wasteVal = (waterStore.wastewaterValues as any)[element] || 0;
const finalPpm = (waterVal * waterPct) + (wasteVal * wastePct);
const converted = convertToDisplay(finalPpm, element, currentUnit.value);
return converted.toFixed(2);
};

/**
* به‌روزرسانی مقدار آب (با تبدیل واحد معکوس)
*/
const updateWaterValue = (element: string, event: Event) => {
const target = event.target as HTMLInputElement;
const displayValue = parseFloat(target.value) || 0;
const realValue = convertFromDisplay(displayValue, element, currentUnit.value);

if (element === 'EC') {
waterStore.setWaterMix({ waterSalinity: realValue });
} else if (element === 'pH') {
waterStore.setWaterPH(realValue);
} else {
waterStore.setWaterValue(element, realValue);
}
triggerAutoSave();
};

/**
* به‌روزرسانی مقدار پساب (با تبدیل واحد معکوس)
*/
const updateWastewaterValue = (element: string, event: Event) => {
const target = event.target as HTMLInputElement;
const displayValue = parseFloat(target.value) || 0;
const realValue = convertFromDisplay(displayValue, element, currentUnit.value);
waterStore.setWastewaterValue(element, realValue);
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

// Auto-save Logic
const triggerAutoSave = () => {
if (saveTimeout) clearTimeout(saveTimeout);
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
water_percentage: waterStore.waterMixData.waterPercentage,
wastewater_percentage: waterStore.waterMixData.wastewaterPercentage,
water_salinity: waterStore.waterMixData.waterSalinity,
water_values: waterStore.waterValues,
wastewater_values: waterStore.wastewaterValues
};
let existingAnalysis = null;
try {
existingAnalysis = await apiService.getWaterAnalysis(String(reportStore.currentReportId));
} catch (e) {}

if (existingAnalysis) {
await apiService.updateWaterAnalysis(String(existingAnalysis.id), waterPayload);
} else {
await apiService.createWaterAnalysis(String(reportStore.currentReportId), waterPayload);
}
saveStatus.value = 'success';
setTimeout(() => { saveStatus.value = 'idle'; }, 2000);
} catch (error: any) {
console.error('Auto-save error:', error);
saveStatus.value = 'idle';
} finally {
isSaving.value = false;
}
};

const showToast = (msg: string, type: 'success' | 'error' = 'success') => {
toastMessage.value = msg;
toastType.value = type;
setTimeout(() => { toastMessage.value = null; }, 3000);
};

// Template Methods
const loadWaterTemplates = async () => {
try {
const templates = await apiService.get('/water-templates');
waterTemplates.value = Array.isArray(templates) ? templates : [];
} catch (error) { console.error(error); }
};

const openSaveTemplateModal = () => {
templateForm.value = { name: '', description: '' };
showSaveTemplateModal.value = true;
};

const closeSaveTemplateModal = () => {
showSaveTemplateModal.value = false;
};

const saveWaterTemplate = async () => {
if (!templateForm.value.name) return;
isSavingTemplate.value = true;
try {
await apiService.post('/water-templates', {
name: templateForm.value.name,
description: templateForm.value.description || null,
water_percentage: waterPercentage.value,
wastewater_percentage: wastewaterPercentage.value,
water_salinity: waterSalinity.value,
water_salinity_unit: ecUnit.value,
water_ph: waterPH.value,
water_values: waterStore.waterValues,
wastewater_values: waterStore.wastewaterValues
});
await loadWaterTemplates();
closeSaveTemplateModal();
showToast('قالب با موفقیت ذخیره شد', 'success');
} catch (error: any) {
showToast('خطا در ذخیره قالب', 'error');
} finally {
isSavingTemplate.value = false;
}
};

const loadWaterTemplate = async (template: any) => {
waterPercentage.value = template.water_percentage;
wastewaterPercentage.value = template.wastewater_percentage;
waterSalinity.value = template.water_salinity;
waterStore.setECUnit(template.water_salinity_unit || 'dS/m');
waterStore.setWaterPH(template.water_ph);
waterStore.wastewaterValues = {};
waterStore.waterValues = {};
if (template.water_values) {
for (const [key, value] of Object.entries(template.water_values)) {
waterStore.setWaterValue(key, value as number);
}
}
if (template.wastewater_values) {
for (const [key, value] of Object.entries(template.wastewater_values)) {
waterStore.setWastewaterValue(key, value as number);
}
}
showToast(`قالب "${template.name}" بارگذاری شد`, 'success');
triggerAutoSave();
};

const deleteWaterTemplate = async (templateId: number) => {
try {
await apiService.delete(`/water-templates/${templateId}`);
await loadWaterTemplates();
showToast('قالب حذف شد', 'success');
} catch (error) {
showToast('خطا در حذف قالب', 'error');
}
};

onMounted(() => {
loadWaterTemplates();
});
</script>

<style scoped>
.modal-enter-active, .modal-leave-active { transition: all 0.3s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-from .relative, .modal-leave-to .relative { transform: scale(0.95); }
.fade-enter-active, .fade-leave-active { transition: all 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translate(-50%, 10px); }
.custom-scrollbar::-webkit-scrollbar { height: 6px; width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 3px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #c1c1c1; border-radius: 3px; }
.dark .custom-scrollbar::-webkit-scrollbar-track { background: #374151; }
.dark .custom-scrollbar::-webkit-scrollbar-thumb { background: #4b5563; }
.tabular-nums { font-variant-numeric: tabular-nums; font-feature-settings: "tnum"; }
.animate-fade-in { animation: fadeIn 0.5s ease-out; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
</style>