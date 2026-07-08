// frontend/src/components/features/fertilizer-db/FertilizerIcons.ts
import { defineComponent, h } from 'vue';

// ============================================================
// آیکون فرم مایع - لوله آزمایش ساده و استاندارد
// ============================================================
export const IconLiquid = defineComponent({
  name: 'IconLiquid',
  setup() {
    return () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24',
      xmlns: 'http://www.w3.org/2000/svg',
      'stroke-width': '1.5',
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round'
    }, [
      // لوله آزمایش
      h('path', { d: 'M9 3v12a4 4 0 0 0 8 0V3' }),
      // دهانه لوله
      h('path', { d: 'M9 3h8' }),
      // کف گرد لوله
      h('path', { d: 'M9 15a4 4 0 0 0 8 0' }),
      // خطوط مایع داخل لوله
      h('path', { d: 'M10 11h6' }),
      h('path', { d: 'M10 13h6' })
    ]);
  }
});

// ============================================================
// آیکون فرم پودری - کاسه حاوی پودر
// ============================================================
export const IconPowder = defineComponent({
  name: 'IconPowder',
  setup() {
    return () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24',
      xmlns: 'http://www.w3.org/2000/svg',
      'stroke-width': '1.5',
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round'
    }, [
      // سطح پودر
      h('path', { d: 'M7 11C8.5 9.8 10 10.2 12 9.8C14 9.4 15.5 10.3 17 11' }),
      // کاسه
      h('path', { d: 'M5 11C5.6 16 7.8 19 12 19C16.2 19 18.4 16 19 11' }),
      // لبه کاسه
      h('path', { d: 'M5 11H19' }),
      // دانه‌های پودر
      h('circle', { cx: '8.4', cy: '9.9', r: '0.35', fill: 'currentColor', stroke: 'none' }),
      h('circle', { cx: '10.2', cy: '9.4', r: '0.35', fill: 'currentColor', stroke: 'none' }),
      h('circle', { cx: '12', cy: '9.2', r: '0.35', fill: 'currentColor', stroke: 'none' }),
      h('circle', { cx: '13.8', cy: '9.5', r: '0.35', fill: 'currentColor', stroke: 'none' }),
      h('circle', { cx: '15.6', cy: '10', r: '0.35', fill: 'currentColor', stroke: 'none' })
    ]);
  }
});

// ============================================================
// آیکون فرم کریستالی - کریستال درخشان
// ============================================================
export const IconCrystal = defineComponent({
  name: 'IconCrystal',
  setup() {
    return () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24',
      xmlns: 'http://www.w3.org/2000/svg',
      'stroke-width': '1.5',
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round'
    }, [
      h('path', { d: 'M12 3l5 5-5 13-5-13 5-5z' }),
      h('path', { d: 'M7 8h10' }),
      h('path', { d: 'M12 3v18' }),
      h('path', { d: 'M5 5v1' }),
      h('path', { d: 'M3.5 6.5h1' }),
      h('path', { d: 'M19 4v1' }),
      h('path', { d: 'M20.5 5.5h1' }),
      h('path', { d: 'M18.5 18v1' })
    ]);
  }
});

// ============================================================
// آیکون فرم گرانول - دانه‌های گرد
// ============================================================
export const IconGranular = defineComponent({
  name: 'IconGranular',
  setup() {
    return () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24',
      xmlns: 'http://www.w3.org/2000/svg',
      'stroke-width': '1.5',
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round'
    }, [
      h('circle', { cx: '12', cy: '12', r: '2.2' }),
      h('circle', { cx: '7', cy: '9', r: '1.3' }),
      h('circle', { cx: '17', cy: '9', r: '1.1' }),
      h('circle', { cx: '8', cy: '17', r: '1.5' }),
      h('circle', { cx: '17', cy: '16', r: '1.2' })
    ]);
  }
});

// ============================================================
// آیکون اسید - لوله آزمایش با اسید
// ============================================================
export const IconAcid = defineComponent({
  name: 'IconAcid',
  setup() {
    return () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24',
      xmlns: 'http://www.w3.org/2000/svg',
      'stroke-width': '1.5',
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round'
    }, [
      h('path', { d: 'M9 3v12a4 4 0 0 0 8 0V3' }),
      h('path', { d: 'M9 3h8' }),
      h('path', { d: 'M9 15a4 4 0 0 0 8 0' }),
      h('path', { d: 'M10 10h6' }),
      h('path', { d: 'M10 12h6' }),
      h('circle', { cx: '13', cy: '8', r: '0.5', fill: 'currentColor', stroke: 'none' }),
      h('circle', { cx: '11', cy: '11', r: '0.4', fill: 'currentColor', stroke: 'none' }),
      h('circle', { cx: '15', cy: '11', r: '0.4', fill: 'currentColor', stroke: 'none' })
    ]);
  }
});

// ============================================================
// آیکون پیش‌فرض - برگ
// ============================================================
export const IconDefault = defineComponent({
  name: 'IconDefault',
  setup() {
    return () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24',
      xmlns: 'http://www.w3.org/2000/svg',
      'stroke-width': '1.5',
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round'
    }, [
      h('path', { d: 'M12 20V10' }),
      h('path', { d: 'M12 10c0-4 3-6 7-6 0 4-2 7-7 7' }),
      h('path', { d: 'M12 14c0-3-2-5-6-5 0 4 2 6 6 6' })
    ]);
  }
});

// ============================================================
// آیکون‌های اضافی برای استفاده در جاهای دیگر
// ============================================================

// آیکون پلاس (افزودن)
export const IconPlus = defineComponent({
  name: 'IconPlus',
  setup() {
    return () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24',
      xmlns: 'http://www.w3.org/2000/svg',
      'stroke-width': '2',
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round'
    }, [
      h('path', { d: 'M12 4v16M4 12h16' })
    ]);
  }
});

// آیکون جستجو
export const IconSearch = defineComponent({
  name: 'IconSearch',
  setup() {
    return () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24',
      xmlns: 'http://www.w3.org/2000/svg',
      'stroke-width': '2',
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round'
    }, [
      h('circle', { cx: '11', cy: '11', r: '8' }),
      h('path', { d: 'M16.5 16.5L21 21' })
    ]);
  }
});

// آیکون فیلتر
export const IconFilter = defineComponent({
  name: 'IconFilter',
  setup() {
    return () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24',
      xmlns: 'http://www.w3.org/2000/svg',
      'stroke-width': '1.5',
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round'
    }, [
      h('path', { d: 'M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z' })
    ]);
  }
});

// آیکون حذف/سطل زباله
export const IconTrash = defineComponent({
  name: 'IconTrash',
  setup() {
    return () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24',
      xmlns: 'http://www.w3.org/2000/svg',
      'stroke-width': '1.5',
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round'
    }, [
      h('path', { d: 'M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16' })
    ]);
  }
});

// آیکون ویرایش
export const IconEdit = defineComponent({
  name: 'IconEdit',
  setup() {
    return () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24',
      xmlns: 'http://www.w3.org/2000/svg',
      'stroke-width': '1.5',
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round'
    }, [
      h('path', { d: 'M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z' })
    ]);
  }
});

// آیکون کپی
export const IconCopy = defineComponent({
  name: 'IconCopy',
  setup() {
    return () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24',
      xmlns: 'http://www.w3.org/2000/svg',
      'stroke-width': '1.5',
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round'
    }, [
      h('path', { d: 'M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3' })
    ]);
  }
});

// آیکون چک (تأیید)
export const IconCheck = defineComponent({
  name: 'IconCheck',
  setup() {
    return () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24',
      xmlns: 'http://www.w3.org/2000/svg',
      'stroke-width': '2',
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round'
    }, [
      h('path', { d: 'M5 13l4 4L19 7' })
    ]);
  }
});

// آیکون بستن (X)
export const IconClose = defineComponent({
  name: 'IconClose',
  setup() {
    return () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24',
      xmlns: 'http://www.w3.org/2000/svg',
      'stroke-width': '2',
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round'
    }, [
      h('path', { d: 'M6 18L18 6M6 6l12 12' })
    ]);
  }
});

// آیکون اطلاع‌رسانی
export const IconInfo = defineComponent({
  name: 'IconInfo',
  setup() {
    return () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24',
      xmlns: 'http://www.w3.org/2000/svg',
      'stroke-width': '1.5',
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round'
    }, [
      h('circle', { cx: '12', cy: '12', r: '10' }),
      h('path', { d: 'M12 16v-4' }),
      h('path', { d: 'M12 8h.01' })
    ]);
  }
});

// ============================================================
// آبجکت برای دسترسی آسان به همه آیکون‌ها
// ============================================================
export const Icons = {
  powder: IconPowder,
  liquid: IconLiquid,
  crystal: IconCrystal,
  granular: IconGranular,
  acid: IconAcid,
  default: IconDefault,
  plus: IconPlus,
  search: IconSearch,
  filter: IconFilter,
  trash: IconTrash,
  edit: IconEdit,
  copy: IconCopy,
  check: IconCheck,
  close: IconClose,
  info: IconInfo
};

export default Icons;