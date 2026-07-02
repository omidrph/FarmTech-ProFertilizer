<template>
  <div class="space-y-6">
    <!-- ============================================================ -->
    <!-- تب‌های رسپی -->
    <!-- ============================================================ -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div class="border-b border-gray-200 dark:border-gray-700">
        <div class="flex overflow-x-auto scrollbar-hide">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            class="flex items-center gap-2 px-4 sm:px-6 py-3 text-sm font-medium whitespace-nowrap border-b-2 transition-colors flex-shrink-0"
            :class="activeTab === tab.id
              ? 'border-primary-500 text-primary-600 dark:text-primary-400 bg-white dark:bg-gray-800'
              : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800'"
          >
            <div v-html="tab.icon" class="w-4 h-4"></div>
            <span>{{ tab.label }}</span>
            <span
              v-if="tab.id === 'system'"
              class="px-2 py-0.5 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 rounded-full text-xs"
            >
              {{ systemRecipes.length }}
            </span>
            <span
              v-if="tab.id === 'personal'"
              class="px-2 py-0.5 bg-success-100 dark:bg-success-900/30 text-success-700 dark:text-success-400 rounded-full text-xs"
            >
              {{ userRecipes.length }}
            </span>
          </button>
        </div>
      </div>

      <!-- ============================================================ -->
      <!-- محتوای تب سیستمی -->
      <!-- ============================================================ -->
      <div v-if="activeTab === 'system'" class="p-4 sm:p-6">
        <!-- Loading -->
        <div v-if="isLoading" class="flex justify-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <span class="mr-2 text-gray-600 dark:text-gray-400">در حال بارگذاری...</span>
        </div>

        <!-- Empty State -->
        <div v-else-if="systemRecipes.length === 0" class="text-center py-12">
          <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
            <svg class="w-8 h-8 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
          </div>
          <p class="text-gray-500 dark:text-gray-400">هیچ رسپی سیستمی موجود نیست</p>
          <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">با تیم پشتیبانی تماس بگیرید</p>
        </div>

        <!-- لیست رسپی‌های سیستمی -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="recipe in systemRecipes"
            :key="recipe.id"
            class="bg-gray-50 dark:bg-gray-700/30 rounded-xl p-4 border border-gray-200 dark:border-gray-600 hover:shadow-md transition-all duration-200 group"
          >
            <!-- Header -->
            <div class="flex items-start justify-between mb-3">
              <div class="flex-1 min-w-0">
                <h4 class="font-semibold text-gray-900 dark:text-white text-sm truncate">{{ recipe.name }}</h4>
                <div class="flex items-center gap-2 mt-1 flex-wrap">
                  <span
                    v-if="recipe.category"
                    class="text-[10px] px-2 py-0.5 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 rounded-full"
                  >
                    {{ recipe.category }}
                  </span>
                  <span
                    v-if="recipe.stage"
                    class="text-[10px] px-2 py-0.5 bg-gray-200 dark:bg-gray-600 text-gray-600 dark:text-gray-300 rounded-full"
                  >
                    {{ recipe.stage }}
                  </span>
                  <span class="text-[10px] px-2 py-0.5 bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-400 rounded-full">
                    سیستمی
                  </span>
                </div>
              </div>
            </div>

            <!-- Description -->
            <p v-if="recipe.description" class="text-xs text-gray-500 dark:text-gray-400 mb-3 line-clamp-2">
              {{ recipe.description }}
            </p>

            <!-- Elements Preview with Hover Tooltip -->
            <div class="relative mb-3">
              <div class="flex flex-wrap gap-1">
                <span
                  v-for="(value, element) in getTopElements(recipe.target_values, 4)"
                  :key="element"
                  class="text-[10px] px-1.5 py-0.5 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded border border-gray-200 dark:border-gray-600"
                >
                  {{ element }}: {{ Number(value).toFixed(1) }}
                </span>
                <span
                  v-if="Object.keys(recipe.target_values).length > 4"
                  class="text-[10px] px-1.5 py-0.5 bg-gray-200 dark:bg-gray-600 text-gray-600 dark:text-gray-300 rounded border border-gray-200 dark:border-gray-600 cursor-help relative group/tooltip"
                >
                  +{{ Object.keys(recipe.target_values).length - 4 }} عنصر
                  <!-- Tooltip با تمام عناصر -->
                  <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover/tooltip:block z-50 min-w-[200px] max-w-[280px]">
                    <div class="bg-gray-900 dark:bg-gray-800 text-white text-xs rounded-lg shadow-2xl p-3 border border-gray-700 dark:border-gray-600">
                      <p class="font-semibold text-primary-400 mb-2 text-center">تمام عناصر</p>
                      <div class="grid grid-cols-2 gap-x-4 gap-y-1">
                        <div
                          v-for="(value, element) in recipe.target_values"
                          :key="'tooltip-'+element"
                          class="flex justify-between items-center"
                          :class="{ 'text-gray-400': value === 0 }"
                        >
                          <span class="font-medium">{{ element }}</span>
                          <span class="font-mono tabular-nums">{{ Number(value).toFixed(2) }}</span>
                        </div>
                      </div>
                      <div class="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-full">
                        <div class="border-8 border-transparent border-t-gray-900 dark:border-t-gray-800"></div>
                      </div>
                    </div>
                  </div>
                </span>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex items-center gap-2">
              <button
                @click="applyRecipe(recipe.id)"
                class="flex-1 px-3 py-1.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-xs flex items-center justify-center gap-1"
              >
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                اعمال
              </button>
              <button
                @click="copyRecipe(recipe.id)"
                class="px-3 py-1.5 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors text-xs flex items-center gap-1"
                title="کپی به رسپی‌های شخصی"
              >
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- ============================================================ -->
      <!-- محتوای تب شخصی -->
      <!-- ============================================================ -->
      <div v-if="activeTab === 'personal'" class="p-4 sm:p-6">
        <!-- عنوان -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-base font-semibold text-gray-900 dark:text-white flex items-center gap-2">
            <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            رسپی‌های شخصی من
            <span class="text-xs font-normal text-gray-400">({{ userRecipes.length }})</span>
          </h3>
          <!-- دکمه رسپی جدید - فقط در حالت غیر خالی نمایش داده می‌شود -->
          <button
            v-if="userRecipes.length > 0"
            @click="openCreateModal"
            class="px-3 py-1.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm flex items-center gap-1 shadow-sm hover:shadow-md"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            رسپی جدید
          </button>
        </div>

        <!-- Loading -->
        <div v-if="isLoading" class="flex justify-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <span class="mr-2 text-gray-600 dark:text-gray-400">در حال بارگذاری...</span>
        </div>

        <!-- Empty State با دکمه ساخت رسپی -->
        <div v-else-if="userRecipes.length === 0" class="text-center py-12">
          <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
            <svg class="w-8 h-8 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
            </svg>
          </div>
          <p class="text-gray-500 dark:text-gray-400 mb-2">هنوز رسپی شخصی ندارید</p>
          <p class="text-xs text-gray-400 dark:text-gray-500 mb-4">از رسپی‌های سیستمی کپی کنید یا یک رسپی جدید بسازید</p>
          <button
            @click="openCreateModal"
            class="px-5 py-2.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm flex items-center gap-2 shadow-sm hover:shadow-md mx-auto"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            ساخت رسپی جدید
          </button>
        </div>

        <!-- لیست رسپی‌های شخصی -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="recipe in userRecipes"
            :key="recipe.id"
            class="bg-gray-50 dark:bg-gray-700/30 rounded-xl p-4 border border-gray-200 dark:border-gray-600 hover:shadow-md transition-all duration-200 group"
          >
            <!-- Header -->
            <div class="flex items-start justify-between mb-3">
              <div class="flex-1 min-w-0">
                <h4 class="font-semibold text-gray-900 dark:text-white text-sm truncate">{{ recipe.name }}</h4>
                <div class="flex items-center gap-2 mt-1 flex-wrap">
                  <span
                    v-if="recipe.category"
                    class="text-[10px] px-2 py-0.5 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 rounded-full"
                  >
                    {{ recipe.category }}
                  </span>
                  <span
                    v-if="recipe.stage"
                    class="text-[10px] px-2 py-0.5 bg-gray-200 dark:bg-gray-600 text-gray-600 dark:text-gray-300 rounded-full"
                  >
                    {{ recipe.stage }}
                  </span>
                  <span class="text-[10px] px-2 py-0.5 bg-success-100 dark:bg-success-900/30 text-success-700 dark:text-success-400 rounded-full">
                    شخصی
                  </span>
                </div>
              </div>
              <div class="flex items-center gap-1 flex-shrink-0">
                <button
                  @click="editRecipe(recipe)"
                  class="p-1.5 rounded-lg text-primary-600 hover:text-primary-800 hover:bg-primary-50 dark:hover:bg-primary-900/30 transition-colors"
                  title="ویرایش"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                  </svg>
                </button>
                <button
                  @click="deleteRecipe(recipe.id)"
                  class="p-1.5 rounded-lg text-danger-600 hover:text-danger-800 hover:bg-danger-50 dark:hover:bg-danger-900/30 transition-colors"
                  title="حذف"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Description -->
            <p v-if="recipe.description" class="text-xs text-gray-500 dark:text-gray-400 mb-3 line-clamp-2">
              {{ recipe.description }}
            </p>

            <!-- Elements Preview with Hover Tooltip -->
            <div class="relative mb-3">
              <div class="flex flex-wrap gap-1">
                <span
                  v-for="(value, element) in getTopElements(recipe.target_values, 4)"
                  :key="element"
                  class="text-[10px] px-1.5 py-0.5 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded border border-gray-200 dark:border-gray-600"
                >
                  {{ element }}: {{ Number(value).toFixed(1) }}
                </span>
                <span
                  v-if="Object.keys(recipe.target_values).length > 4"
                  class="text-[10px] px-1.5 py-0.5 bg-gray-200 dark:bg-gray-600 text-gray-600 dark:text-gray-300 rounded border border-gray-200 dark:border-gray-600 cursor-help relative group/tooltip"
                >
                  +{{ Object.keys(recipe.target_values).length - 4 }} عنصر
                  <!-- Tooltip با تمام عناصر -->
                  <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover/tooltip:block z-50 min-w-[200px] max-w-[280px]">
                    <div class="bg-gray-900 dark:bg-gray-800 text-white text-xs rounded-lg shadow-2xl p-3 border border-gray-700 dark:border-gray-600">
                      <p class="font-semibold text-primary-400 mb-2 text-center">تمام عناصر</p>
                      <div class="grid grid-cols-2 gap-x-4 gap-y-1">
                        <div
                          v-for="(value, element) in recipe.target_values"
                          :key="'tooltip-'+element"
                          class="flex justify-between items-center"
                          :class="{ 'text-gray-400': value === 0 }"
                        >
                          <span class="font-medium">{{ element }}</span>
                          <span class="font-mono tabular-nums">{{ Number(value).toFixed(2) }}</span>
                        </div>
                      </div>
                      <div class="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-full">
                        <div class="border-8 border-transparent border-t-gray-900 dark:border-t-gray-800"></div>
                      </div>
                    </div>
                  </div>
                </span>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex items-center gap-2">
              <button
                @click="applyRecipe(recipe.id)"
                class="flex-1 px-3 py-1.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-xs flex items-center justify-center gap-1"
              >
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                اعمال
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- مودال ایجاد/ویرایش رسپی -->
    <!-- ============================================================ -->
    <Teleport to="body">
      <div
        v-if="showModal"
        class="fixed inset-0 z-[100] overflow-y-auto"
        role="dialog"
        aria-modal="true"
      >
        <!-- Backdrop -->
        <div
          class="fixed inset-0 bg-gray-900/75 backdrop-blur-sm transition-opacity"
          @click="closeModal"
        ></div>

        <!-- Modal Container -->
        <div class="flex min-h-full items-center justify-center p-0 sm:p-4">
          <div class="relative w-full h-full sm:h-auto sm:max-w-4xl sm:my-8 bg-white dark:bg-gray-800 sm:rounded-2xl shadow-2xl overflow-hidden">
            
            <!-- Header -->
            <div class="bg-gradient-to-l from-primary-600 to-primary-700 dark:from-primary-800 dark:to-primary-900 px-4 sm:px-6 py-4 flex items-center justify-between sticky top-0 z-10">
              <h3 class="text-lg sm:text-xl font-bold text-white flex items-center gap-2">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                {{ isEditing ? 'ویرایش رسپی' : 'ساخت رسپی جدید' }}
              </h3>
              <button
                @click="closeModal"
                class="text-white/80 hover:text-white transition-colors p-1 rounded-full hover:bg-white/10"
              >
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>

            <!-- Body -->
            <div class="px-4 sm:px-6 py-5 max-h-[calc(100vh-140px)] sm:max-h-[calc(100vh-200px)] overflow-y-auto custom-scrollbar">
              <div class="space-y-4">
                <!-- نام رسپی -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    نام رسپی <span class="text-danger-500">*</span>
                  </label>
                  <input
                    type="text"
                    v-model="formData.name"
                    placeholder="مثال: گوجه فرنگی مرحله گلدهی"
                    class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                  />
                </div>

                <!-- توضیحات -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    توضیحات
                  </label>
                  <textarea
                    v-model="formData.description"
                    rows="2"
                    placeholder="توضیحات مربوط به این رسپی..."
                    class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
                  ></textarea>
                </div>

                <!-- دسته‌بندی و مرحله رشد -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      دسته‌بندی
                    </label>
                    <input
                      type="text"
                      v-model="formData.category"
                      placeholder="مثال: گوجه فرنگی"
                      class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      مرحله رشد
                    </label>
                    <input
                      type="text"
                      v-model="formData.stage"
                      placeholder="مثال: گلدهی"
                      class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                    />
                  </div>
                </div>

                <!-- جدول عناصر هدف -->
                <div>
                  <div class="flex items-center justify-between mb-2">
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                      مقادیر عناصر هدف (ppm)
                    </label>
                    <button
                      @click="clearElements"
                      type="button"
                      class="text-xs text-danger-600 hover:text-danger-800 dark:hover:text-danger-400 transition-colors"
                    >
                      پاک کردن همه
                    </button>
                  </div>

                  <div class="overflow-x-auto">
                    <table class="w-full text-sm border-collapse">
                      <thead>
                        <tr>
                          <th class="px-3 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border border-gray-200 dark:border-gray-600 text-center min-w-[80px]">
                            عنصر
                          </th>
                          <th
                            v-for="element in elements"
                            :key="element"
                            class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border border-gray-200 dark:border-gray-600 text-center min-w-[70px]"
                          >
                            {{ element }}
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td class="px-3 py-2 bg-gray-50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600 text-center font-medium text-gray-600 dark:text-gray-400 text-xs">
                            مقدار هدف
                          </td>
                          <td
                            v-for="element in elements"
                            :key="'value-'+element"
                            class="px-2 py-1 border border-gray-200 dark:border-gray-600 text-center"
                          >
                            <input
                              type="number"
                              :value="formData.target_values[element] || 0"
                              @input="updateElementValue(element, $event)"
                              step="0.001"
                              min="0"
                              class="w-full max-w-[70px] px-1.5 py-1 text-center bg-transparent border-2 border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500 rounded transition-all duration-200"
                              placeholder="۰"
                            />
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>

            <!-- Footer -->
            <div class="bg-gray-50 dark:bg-gray-700/30 px-4 sm:px-6 py-4 border-t border-gray-200 dark:border-gray-600 flex flex-col-reverse sm:flex-row gap-3 justify-end sticky bottom-0">
              <button
                @click="closeModal"
                class="w-full sm:w-auto px-6 py-2.5 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 transition-colors font-medium"
              >
                انصراف
              </button>
              <button
                @click="saveRecipe"
                :disabled="isSaving || !formData.name"
                class="w-full sm:w-auto px-6 py-2.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium flex items-center justify-center gap-2 shadow-lg shadow-primary-500/30"
              >
                <svg v-if="isSaving" class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
                {{ isSaving ? 'در حال ذخیره...' : (isEditing ? 'ذخیره تغییرات' : 'ساخت رسپی') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- ============================================================ -->
    <!-- پیام موفقیت/خطا -->
    <!-- ============================================================ -->
    <Teleport to="body">
      <Transition name="fade">
        <div
          v-if="toastMessage"
          class="fixed bottom-4 left-1/2 -translate-x-1/2 z-[200] px-6 py-3 rounded-xl shadow-2xl flex items-center gap-2"
          :class="toastType === 'success'
            ? 'bg-success-600 text-white'
            : 'bg-danger-600 text-white'"
        >
          <svg v-if="toastType === 'success'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
          <span class="text-sm font-medium">{{ toastMessage }}</span>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';
import { useRecipeStore } from '@/store/modules/recipeStore';
import { useTargetStore } from '@/store/modules/targetStore';

// ===== Props & Emits =====
const emit = defineEmits<{
  (e: 'recipe-applied'): void;
}>();

// ===== Stores =====
const recipeStore = useRecipeStore();
const targetStore = useTargetStore();

// ===== Computed =====
const systemRecipes = computed(() => recipeStore.systemRecipes);
const userRecipes = computed(() => recipeStore.userRecipes);
const isLoading = computed(() => recipeStore.isLoading);
const error = computed(() => recipeStore.error);

// ===== State =====
const activeTab = ref<'system' | 'personal'>('system');
const showModal = ref(false);
const isEditing = ref(false);
const isSaving = ref(false);
const toastMessage = ref<string | null>(null);
const toastType = ref<'success' | 'error'>('success');
const editingId = ref<number | null>(null);

const elements = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'];

const formData = reactive({
  name: '',
  description: '',
  category: '',
  stage: '',
  target_values: {} as Record<string, number>
});

// ===== Tabs =====
const tabs = [
  {
    id: 'system' as const,
    label: 'رسپی‌های سیستمی',
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>`
  },
  {
    id: 'personal' as const,
    label: 'رسپی‌های شخصی',
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>`
  }
];

// ===== Methods =====
const getTopElements = (targetValues: Record<string, number>, count: number) => {
  const entries = Object.entries(targetValues)
    .filter(([_, value]) => value > 0)
    .sort((a, b) => b[1] - a[1])
    .slice(0, count);
  return Object.fromEntries(entries);
};

const updateElementValue = (element: string, event: Event) => {
  const target = event.target as HTMLInputElement;
  const value = parseFloat(target.value) || 0;
  formData.target_values[element] = value;
};

const clearElements = () => {
  if (confirm('آیا از پاک کردن تمام عناصر اطمینان دارید؟')) {
    formData.target_values = {};
  }
};

const resetForm = () => {
  formData.name = '';
  formData.description = '';
  formData.category = '';
  formData.stage = '';
  formData.target_values = {};
  isEditing.value = false;
  editingId.value = null;
};

const openCreateModal = () => {
  resetForm();
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  resetForm();
};

const showToast = (message: string, type: 'success' | 'error' = 'success') => {
  toastMessage.value = message;
  toastType.value = type;
  setTimeout(() => {
    toastMessage.value = null;
  }, 3000);
};

const editRecipe = (recipe: any) => {
  resetForm();
  isEditing.value = true;
  editingId.value = recipe.id;
  formData.name = recipe.name;
  formData.description = recipe.description || '';
  formData.category = recipe.category || '';
  formData.stage = recipe.stage || '';
  formData.target_values = { ...recipe.target_values };
  showModal.value = true;
};

const saveRecipe = async () => {
  if (!formData.name) {
    showToast('لطفاً نام رسپی را وارد کنید', 'error');
    return;
  }

  if (Object.keys(formData.target_values).filter(k => formData.target_values[k] > 0).length === 0) {
    showToast('لطفاً حداقل یک عنصر با مقدار مثبت وارد کنید', 'error');
    return;
  }

  isSaving.value = true;

  try {
    const data = {
      name: formData.name,
      description: formData.description || null,
      category: formData.category || null,
      stage: formData.stage || null,
      target_values: formData.target_values
    };

    let result = null;

    if (isEditing.value && editingId.value !== null) {
      result = await recipeStore.updateRecipe(editingId.value, data);
      if (result) {
        showToast('رسپی با موفقیت به‌روزرسانی شد', 'success');
      }
    } else {
      result = await recipeStore.createRecipe(data);
      if (result) {
        showToast('رسپی با موفقیت ایجاد شد', 'success');
      }
    }

    if (result) {
      closeModal();
      await recipeStore.loadAllRecipes();
    }
  } catch (error: any) {
    showToast(error.message || 'خطا در ذخیره رسپی', 'error');
  } finally {
    isSaving.value = false;
  }
};

const applyRecipe = async (id: number) => {
  try {
    const result = await recipeStore.applyRecipe(id);
    if (result) {
      for (const [element, value] of Object.entries(result)) {
        targetStore.setTargetElement(element as any, value);
      }
      showToast('رسپی با موفقیت اعمال شد', 'success');
      emit('recipe-applied');
    }
  } catch (error: any) {
    showToast(error.message || 'خطا در اعمال رسپی', 'error');
  }
};

const copyRecipe = async (id: number) => {
  try {
    const result = await recipeStore.copySystemRecipe(id);
    if (result) {
      showToast(`رسپی "${result.name}" با موفقیت کپی شد`, 'success');
      await recipeStore.loadAllRecipes();
    }
  } catch (error: any) {
    showToast(error.message || 'خطا در کپی رسپی', 'error');
  }
};

const deleteRecipe = async (id: number) => {
  if (!confirm('آیا از حذف این رسپی اطمینان دارید؟')) {
    return;
  }

  try {
    const success = await recipeStore.deleteRecipe(id);
    if (success) {
      showToast('رسپی با موفقیت حذف شد', 'success');
      await recipeStore.loadAllRecipes();
    }
  } catch (error: any) {
    showToast(error.message || 'خطا در حذف رسپی', 'error');
  }
};

// ===== Lifecycle =====
onMounted(async () => {
  await recipeStore.loadAllRecipes();
});
</script>

<style scoped>
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

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-clamp: 2;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
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

.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}

/* Tooltip Arrow */
.group\/tooltip .absolute {
  pointer-events: none;
}

.group\/tooltip:hover .absolute {
  pointer-events: auto;
}
</style>