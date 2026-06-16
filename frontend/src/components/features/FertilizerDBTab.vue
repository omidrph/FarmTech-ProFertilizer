<template>
  <div class="space-y-6">
    <!-- Info Box -->
    <div class="bg-primary-50 dark:bg-primary-900/20 border-r-4 border-primary-500 rounded-lg p-4">
      <p class="text-gray-700 dark:text-gray-300 text-sm">
        اطلاعات مربوط به کودها در جدول زیر قابل مشاهده و ویرایش است. همچنین با فشردن دکمه "افزودن" می‌توانید کود جدید اضافه کنید.
      </p>
    </div>

    <!-- Actions -->
    <div class="flex flex-wrap gap-3">
      <button @click="showAddModal" class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
        ➕ افزودن کود جدید
      </button>
      <button @click="loadSampleFertilizers" class="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors">
        📥 بارگذاری نمونه
      </button>
      <button @click="printReport" class="px-4 py-2 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 transition-colors">
        🖨️ چاپ
      </button>
    </div>

    <!-- Table -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <div class="overflow-x-auto">
        <table class="w-full text-xs">
          <thead>
            <tr>
              <th class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border-b border-gray-200 dark:border-gray-600 text-right min-w-[100px]">نام کود</th>
              <th class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border-b border-gray-200 dark:border-gray-600 text-center min-w-[80px]">قیمت (تومان)</th>
              <th v-for="el in elements" :key="el" class="px-1 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border-b border-gray-200 dark:border-gray-600 text-center min-w-[50px]">
                {{ el }} (%)
              </th>
              <th class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border-b border-gray-200 dark:border-gray-600 text-center min-w-[80px]">عملیات</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="fertilizer in fertilizers" :key="fertilizer.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
              <td class="px-2 py-2 border-b border-gray-100 dark:border-gray-700 text-right font-medium">{{ fertilizer.name }}</td>
              <td class="px-2 py-2 border-b border-gray-100 dark:border-gray-700 text-center">{{ fertilizer.pricePerKg.toLocaleString() }}</td>
              <td v-for="el in elements" :key="el" class="px-1 py-2 border-b border-gray-100 dark:border-gray-700 text-center">
                {{ fertilizer.elements && fertilizer.elements[el] ? fertilizer.elements[el].toFixed(2) : '0.00' }}
              </td>
              <td class="px-2 py-2 border-b border-gray-100 dark:border-gray-700 text-center">
                <button @click="editFertilizer(fertilizer.id)" class="text-primary-600 hover:text-primary-800 dark:text-primary-400 dark:hover:text-primary-300 transition-colors px-1">
                  ✏️
                </button>
                <button @click="deleteFertilizer(fertilizer.id)" class="text-danger-600 hover:text-danger-800 dark:text-danger-400 dark:hover:text-danger-300 transition-colors px-1">
                  🗑️
                </button>
              </td>
            </tr>
            <tr v-if="fertilizers.length === 0">
              <td :colspan="elements.length + 3" class="px-4 py-8 text-center text-gray-500 dark:text-gray-400">
                هیچ کودی تعریف نشده است. دکمه "افزودن" را بزنید.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// ===== Props =====
interface Props {
  fertilizers: any[];
}

const props = defineProps<Props>();
const emit = defineEmits<{
  (e: 'update:fertilizers', value: any[]): void;
  (e: 'show-add-modal'): void;
}>();

// ===== Data =====
const elements = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'];

// ===== Methods =====
const showAddModal = () => {
  emit('show-add-modal');
};

const loadSampleFertilizers = () => {
  const samples = [
    {
      id: '1',
      name: 'کلسیم نیترات + آمونیوم',
      pricePerKg: 25000,
      elements: { 'N-NO3': 14.5, 'N-NH4': 1.5, 'Ca': 19 }
    },
    {
      id: '2',
      name: 'پتاسیم نیترات',
      pricePerKg: 32000,
      elements: { 'N-NO3': 13, 'K': 38 }
    },
    {
      id: '3',
      name: 'فسفات پتاسیم',
      pricePerKg: 28000,
      elements: { 'P': 22, 'K': 28 }
    },
    {
      id: '4',
      name: 'سولفات منیزیم',
      pricePerKg: 15000,
      elements: { 'S': 13, 'Mg': 10 }
    }
  ];
  emit('update:fertilizers', samples);
};

const deleteFertilizer = (id: string) => {
  if (confirm('آیا از حذف این کود اطمینان دارید؟')) {
    emit('update:fertilizers', props.fertilizers.filter(f => f.id !== id));
  }
};

const editFertilizer = (id: string) => {
  alert('ویرایش کود (در حال توسعه)');
};

const printReport = () => {
  window.print();
};
</script>