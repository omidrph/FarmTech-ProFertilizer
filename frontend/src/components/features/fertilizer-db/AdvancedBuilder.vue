
<!-- frontend/src/components/features/fertilizer-db/AdvancedBuilder.vue -->
<!--
  حالت «پیشرفته»: هر ترکیب و هر تعداد جزء را آزادانه بنویسید؛ برنامه خودش عنصرهای اصلی را بیرون می‌کشد.
  هر ردیف = «فرمول شیمیایی» + «درصد وزنیِ آن جزء در محصول»
  مثال‌ها:  KNO3 ۵۰٪  +  Ca(NO3)2·4H2O ۳۰٪   |   K2O ۲۰٪ (فرم اکسیدی)   |   (NH4)2SO4 ۱۰۰٪
-->
<template>
  <div class="rounded-2xl border border-teal-200 dark:border-teal-800/50 bg-gradient-to-b from-teal-50/80 to-white dark:from-teal-900/15 dark:to-gray-800/40 p-3.5 space-y-3.5 shadow-sm">
    <!-- سربرگ -->
    <header class="flex items-start gap-3">
      <span class="w-9 h-9 rounded-xl bg-gradient-to-br from-teal-500 to-emerald-500 text-white flex items-center justify-center flex-shrink-0 shadow-sm shadow-teal-500/30">
        <svg class="w-[18px] h-[18px]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.7"><path stroke-linecap="round" stroke-linejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" /></svg>
      </span>
      <div class="min-w-0 flex-1">
        <h5 class="text-sm font-bold text-teal-900 dark:text-teal-200">ساخت ترکیب دلخواه</h5>
        <p class="text-[12px] leading-5 text-gray-600 dark:text-gray-400">برای هر ماده فرمولش را بنویسید و بگویید چند درصد وزن محصول است؛ برنامه درصد هر عنصر را حساب می‌کند. اگر مقدار یک عنصر را خودتان می‌دانید، همان را مستقیم وارد کنید.</p>
      </div>
      <button type="button" @click="showHelp = !showHelp" class="flex-shrink-0 px-2.5 py-1 rounded-lg text-[11px] font-medium border transition-colors"
        :class="showHelp ? 'bg-teal-600 border-teal-600 text-white' : 'border-teal-200 dark:border-teal-700 text-teal-700 dark:text-teal-300 hover:bg-teal-50 dark:hover:bg-teal-900/30'">راهنما</button>
    </header>

    <!-- راهنما + نمونه‌ها -->
    <Transition name="ab">
      <div v-if="showHelp" class="rounded-xl bg-white/80 dark:bg-gray-800/60 border border-teal-100 dark:border-teal-800/40 p-3 space-y-2.5 text-[12px] leading-6 text-gray-600 dark:text-gray-300">
        <div class="rounded-lg bg-teal-50 dark:bg-teal-900/20 border border-teal-100 dark:border-teal-800/40 p-2.5 text-[12px] leading-6">
          <b class="text-teal-800 dark:text-teal-200">«سهم از محصول» یعنی چه؟</b>
          هر ردیف یک «ماده» است و سهم آن یعنی <b>چند درصد از وزن کل محصول</b> را همان ماده تشکیل می‌دهد. مثلاً کودی که نصف آن نیترات پتاسیم و ۳۰٪ آن نیترات کلسیم است:
          <span dir="ltr" class="font-mono">KNO3 = 50٪</span> و <span dir="ltr" class="font-mono">Ca(NO3)2·4H2O = 30٪</span> (۲۰٪ باقی‌مانده حامل/ناخالصی است). اگر کل محصول فقط یک ماده است، ۱۰۰ بگذارید.
          اگر درصد خودِ عنصر را از روی برچسب می‌دانید (مثلاً «۱۰٪ آهن»)، به‌جای سهم از «تنظیم دقیق عنصرها» یا «افزودن عنصر مستقیم» استفاده کنید.
        </div>
        <ul class="list-disc pr-4 space-y-0.5">
          <li>پرانتز و آب تبلور: <code dir="ltr" class="px-1 rounded bg-gray-100 dark:bg-gray-700">Ca(NO3)2·4H2O</code> (به‌جای «·» می‌توانید «.» بزنید)</li>
          <li>فرم اکسیدی برچسب: <code dir="ltr" class="px-1 rounded bg-gray-100 dark:bg-gray-700">K2O</code> و <code dir="ltr" class="px-1 rounded bg-gray-100 dark:bg-gray-700">P2O5</code> (برنامه به عنصر خالص تبدیل می‌کند)</li>
          <li>نماد عناصر با حرف بزرگ شروع شود: <code dir="ltr" class="px-1 rounded bg-gray-100 dark:bg-gray-700">KNO3</code> نه <code dir="ltr" class="px-1 rounded bg-gray-100 dark:bg-gray-700">kno3</code></li>
          <li>کلات‌ها فرمول عنصری ندارند؛ از دکمهٔ «کلات‌ها» استفاده کنید.</li>
        </ul>
        <div class="flex flex-wrap gap-1.5 pt-0.5">
          <span class="text-[11px] text-gray-500 py-1">نمونه‌های آماده:</span>
          <button v-for="ex in EXAMPLES" :key="ex.t" type="button" @click="loadExample(ex)"
            class="px-2.5 py-1 rounded-full text-[11px] font-medium bg-teal-50 dark:bg-teal-900/20 text-teal-700 dark:text-teal-300 border border-teal-200 dark:border-teal-800/60 hover:bg-teal-100 transition-colors">{{ ex.t }}</button>
        </div>
      </div>
    </Transition>

    <!-- ردیف‌ها -->
    <TransitionGroup name="ab" tag="div" class="space-y-2.5">
      <article v-for="(r, i) in rows" :key="r.id" class="rounded-2xl bg-white dark:bg-gray-800 border p-3 space-y-2 shadow-sm transition-colors"
        :class="states[i].error ? 'border-danger-300 dark:border-danger-700/70' : states[i].analysis ? 'border-teal-200 dark:border-teal-800/50' : 'border-gray-200 dark:border-gray-700'">
        <!-- خط ۱: شماره + فرمول + حذف -->
        <div class="flex items-center gap-2">
          <span class="w-7 h-7 rounded-lg bg-gray-100 dark:bg-gray-700 text-[11px] font-bold text-gray-500 dark:text-gray-300 flex items-center justify-center flex-shrink-0 tabular-nums">{{ (i + 1).toLocaleString('fa-IR') }}</span>
          <div class="relative flex-1 min-w-0">
            <input v-model="r.formula" dir="ltr" placeholder="Ca(NO3)2·4H2O" spellcheck="false" autocomplete="off" aria-label="فرمول شیمیایی"
              class="w-full h-11 pl-3 pr-9 text-[15px] rounded-xl border-2 bg-gray-50 dark:bg-gray-700/60 text-gray-900 dark:text-gray-100 font-mono outline-none transition-colors placeholder-gray-300 dark:placeholder-gray-500"
              :class="states[i].error ? 'border-danger-300 focus:border-danger-500' : states[i].analysis ? 'border-teal-300 dark:border-teal-700 focus:border-teal-500' : 'border-gray-200 dark:border-gray-600 focus:border-teal-400'" />
            <span class="absolute right-2.5 top-1/2 -translate-y-1/2">
              <svg v-if="states[i].analysis" class="w-5 h-5 text-teal-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd" /></svg>
              <svg v-else-if="states[i].error" class="w-5 h-5 text-danger-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-5a.75.75 0 01.75.75v4.5a.75.75 0 01-1.5 0v-4.5A.75.75 0 0110 5zm0 10a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" /></svg>
            </span>
          </div>
          <button type="button" @click="rows.splice(i, 1)" class="p-2 rounded-xl text-gray-400 hover:text-danger-600 hover:bg-danger-50 dark:hover:bg-danger-900/20 transition-colors" title="حذف ردیف" aria-label="حذف ردیف">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>

        <!-- خط ۲: سهم از محصول -->
        <div class="flex items-center gap-2 pr-9">
          <span class="text-[12px] text-gray-500 dark:text-gray-400 flex-shrink-0" title="چند درصد از وزن کل محصول، همین ماده است (۱۰۰ = کل محصول فقط همین ماده)">سهم این ماده از وزن محصول</span>
          <label class="flex items-center h-10 rounded-xl border-2 bg-white dark:bg-gray-700 overflow-hidden focus-within:border-teal-500 transition-colors"
            :class="Number(r.amount) > 0 ? 'border-teal-300 dark:border-teal-700' : 'border-gray-200 dark:border-gray-600'">
            <input v-model.number="r.amount" type="number" min="0" max="100" step="0.01" dir="ltr" placeholder="۰" aria-label="درصد از محصول"
              class="w-20 h-full px-2 text-center text-lg font-extrabold bg-transparent text-gray-900 dark:text-white outline-none tabular-nums" />
            <span class="h-full px-2.5 flex items-center text-xs font-bold bg-gray-50 dark:bg-gray-600/60 text-gray-500 dark:text-gray-300 border-r border-gray-200 dark:border-gray-600">٪</span>
          </label>
        </div>

        <!-- نتیجهٔ همین ردیف -->
        <p v-if="states[i].error" class="pr-9 text-[12px] text-danger-600 dark:text-danger-400 flex items-start gap-1.5">{{ states[i].error }}</p>
        <div v-else-if="states[i].analysis" class="pr-9 flex flex-wrap items-center gap-1.5">
          <span class="text-[11px] text-gray-400 ml-1">جرم مولی <b class="tabular-nums text-gray-600 dark:text-gray-300">{{ states[i].analysis.mass.toLocaleString('fa-IR', { maximumFractionDigits: 2 }) }}</b></span>
          <span v-for="(v, k) in states[i].analysis.elements" :key="k" class="inline-flex items-center gap-1 pl-2 pr-1 py-0.5 rounded-full text-[11px] font-medium tabular-nums" :class="chipCls(String(k))">
            <b class="px-1.5 rounded-full bg-white/70 dark:bg-black/20">{{ symbol(String(k)) }}</b><span dir="ltr">{{ (v * 100).toLocaleString('fa-IR', { maximumFractionDigits: 2 }) }}٪</span>
          </span>
          <span v-for="(v, k) in states[i].analysis.untracked" :key="'u' + k" class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400" title="این عنصر در محاسبات برنامه دنبال نمی‌شود">
            <span dir="ltr">{{ k }} {{ (v * 100).toLocaleString('fa-IR', { maximumFractionDigits: 1 }) }}٪</span> · ثبت نمی‌شود
          </span>
          <label v-if="states[i].analysis.genericN" class="flex items-center gap-1.5 text-[11px] text-gray-500 dark:text-gray-400 w-full pt-1">
            نیتروژن غیرنیترات/آمونیوم (مثل اوره) ثبت شود به‌عنوان
            <select v-model="r.genericN" class="h-7 px-1.5 text-[11px] rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100">
              <option value="N-NH4">آمونیومی</option><option value="N-NO3">نیتراتی</option>
            </select>
          </label>
          <div class="w-full pt-1">
            <button type="button" class="text-[11px] font-medium text-teal-700 dark:text-teal-300 hover:underline" @click="r.showCustom = !r.showCustom">{{ r.showCustom ? 'بستن تنظیم دقیق' : '✎ تنظیم دقیق مقدار عنصرها' }}</button>
            <span v-if="hasCustom(r)" class="mr-2 text-[10px] px-1.5 py-0.5 rounded-full bg-amber-100 text-amber-700">مقدار دستی فعال</span>
            <div v-if="r.showCustom" class="mt-1.5 rounded-xl bg-gray-50 dark:bg-gray-700/40 border border-gray-200 dark:border-gray-600 p-2.5 space-y-2">
              <p class="text-[11px] leading-5 text-gray-500 dark:text-gray-400">درصد هر عنصر را <b>در کل محصول</b> بنویسید تا جای مقدار محاسبه‌شده بنشیند (خالی = همان محاسبهٔ خودکار).</p>
              <div class="grid grid-cols-2 sm:grid-cols-3 gap-2">
                <label v-for="(v, k) in states[i].analysis.elements" :key="'c' + k" class="flex items-center gap-1.5 text-[11px] text-gray-600 dark:text-gray-300">
                  <span class="w-14 truncate font-semibold">{{ symbol(String(k)) }}</span>
                  <input v-model.number="r.custom[String(k)]" type="number" min="0" max="100" step="0.01" dir="ltr" :placeholder="(Number(r.amount) > 0 ? Number(r.amount) * v : v * 100).toLocaleString('fa-IR', { maximumFractionDigits: 3 })"
                    class="w-full h-8 px-2 text-center text-sm rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 tabular-nums" />
                </label>
              </div>
              <button v-if="hasCustom(r)" type="button" class="text-[11px] text-rose-600 hover:underline" @click="clearCustom(r)">پاک‌کردن مقدارهای دستی</button>
            </div>
          </div>
        </div>
      </article>
    </TransitionGroup>

    <!-- افزودن -->
    <div class="space-y-2">
      <div class="flex flex-wrap items-center gap-1.5">
        <button type="button" @click="addRow()" class="inline-flex items-center gap-1 h-8 px-3 rounded-full text-xs font-semibold bg-teal-600 text-white hover:bg-teal-700 shadow-sm transition-colors">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" /></svg>ردیف جدید
        </button>
        <span class="text-[11px] text-gray-400 mx-1">یا ترکیب رایج:</span>
        <button v-for="c in POPULAR" :key="c.f" type="button" @click="addRow(c.f)" :title="c.n"
          class="h-8 px-2.5 rounded-full text-[11px] font-mono border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 hover:border-teal-400 hover:text-teal-700 transition-colors" dir="ltr">{{ c.f }}</button>
        <select v-model="quick" @change="addQuick" aria-label="همهٔ ترکیب‌های رایج"
          class="h-8 px-2 text-[11px] rounded-full border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300">
          <option value="">همهٔ ترکیب‌ها…</option>
          <optgroup v-for="g in QUICK" :key="g.title" :label="g.title">
            <option v-for="c in g.items" :key="c.f" :value="c.f">{{ c.n }} — {{ c.f }}</option>
          </optgroup>
        </select>
      </div>
    </div>

    <!-- عنصر مستقیم -->
    <div class="rounded-2xl bg-white dark:bg-gray-800 border border-dashed border-teal-300 dark:border-teal-700 p-3 space-y-2">
      <p class="text-[12px] font-semibold text-teal-800 dark:text-teal-200">افزودن عنصر مستقیم <span class="font-normal text-gray-500">— اگر مقدار عنصری را از روی برچسب می‌دانید (مثلاً ۲٪ آهن)</span></p>
      <div v-for="x in extras" :key="x.id" class="flex items-center gap-2">
        <select v-model="x.key" class="h-9 px-2 text-sm rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 flex-1 min-w-0">
          <option v-for="d in ELEMENT_DEFS" :key="d.key" :value="d.key">{{ d.name }} ({{ symbol(d.key) }})</option>
        </select>
        <label class="flex items-center h-9 rounded-lg border border-gray-300 dark:border-gray-600 overflow-hidden bg-white dark:bg-gray-700"><input v-model.number="x.pct" type="number" min="0" max="100" step="0.01" dir="ltr" class="w-20 h-full px-2 text-center text-sm bg-transparent outline-none tabular-nums" placeholder="۰" /><span class="px-2 text-xs text-gray-500 bg-gray-50 dark:bg-gray-600/60 h-full flex items-center">٪ از محصول</span></label>
        <button type="button" class="p-1.5 text-gray-400 hover:text-danger-600" aria-label="حذف" @click="extras.splice(extras.indexOf(x), 1)">✕</button>
      </div>
      <button type="button" class="h-8 px-3 rounded-full text-xs font-semibold border border-teal-300 dark:border-teal-700 text-teal-700 dark:text-teal-300 hover:bg-teal-50 dark:hover:bg-teal-900/20" @click="extras.push({ id: ++seq, key: 'Fe', pct: null })">+ عنصر مستقیم</button>
    </div>

    <!-- نتیجه -->
    <Transition name="ab">
      <div v-if="hasResult" class="rounded-2xl bg-white dark:bg-gray-800 border border-emerald-200 dark:border-emerald-800/50 overflow-hidden shadow-sm">
        <div class="px-3.5 py-2.5 bg-gradient-to-l from-emerald-50 to-white dark:from-emerald-900/20 dark:to-gray-800 border-b border-emerald-100 dark:border-emerald-800/40 flex items-center justify-between gap-2">
          <p class="text-sm font-bold text-emerald-900 dark:text-emerald-200">عنصرهای استخراج‌شده</p>
          <span class="text-[11px] text-emerald-700/80 dark:text-emerald-300/80">درصد عنصر خالص در محصول</span>
        </div>

        <div class="p-3.5 space-y-3">
          <!-- ترازوی جرم: مجموع اجزا -->
          <div>
            <div class="flex items-center justify-between text-[11px] mb-1">
              <span class="text-gray-500 dark:text-gray-400">مجموع اجزا از محصول</span>
              <b class="tabular-nums" :class="amountSum > 100.0001 ? 'text-danger-600' : 'text-gray-800 dark:text-gray-100'">{{ amountSum.toLocaleString('fa-IR', { maximumFractionDigits: 2 }) }}٪</b>
            </div>
            <div class="h-2.5 rounded-full bg-gray-100 dark:bg-gray-700 overflow-hidden">
              <div class="h-full rounded-full transition-all duration-500" :class="amountSum > 100.0001 ? 'bg-danger-500' : 'bg-gradient-to-l from-teal-400 to-emerald-500'" :style="{ width: Math.min(amountSum, 100) + '%' }"></div>
            </div>
            <p class="text-[11px] mt-1" :class="amountSum > 100.0001 ? 'text-danger-600 dark:text-danger-400 font-medium' : 'text-gray-400'">
              <template v-if="amountSum > 100.0001">مجموع اجزا از ۱۰۰٪ بیشتر است؛ مقدارها را بررسی کنید.</template>
              <template v-else>باقی‌مانده (حامل/ناخالصی): {{ (100 - amountSum).toLocaleString('fa-IR', { maximumFractionDigits: 2 }) }}٪</template>
            </p>
          </div>

          <!-- کاشی‌های عنصر -->
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-2">
            <div v-for="e in resultList" :key="e.key" class="rounded-xl border p-2.5" :class="tileCls(e.key)">
              <div class="flex items-center justify-between gap-1">
                <span class="text-[11px] text-gray-600 dark:text-gray-300 truncate">{{ e.name }}</span>
                <span class="text-[10px] font-bold px-1.5 rounded-md bg-white/70 dark:bg-black/20" dir="ltr">{{ e.symbol }}</span>
              </div>
              <p class="mt-1 text-xl font-extrabold tabular-nums text-gray-900 dark:text-white" dir="ltr">{{ e.pct.toLocaleString('fa-IR', { maximumFractionDigits: 4 }) }}<span class="text-xs font-semibold text-gray-400 mr-0.5">٪</span></p>
              <div class="mt-1.5 h-1 rounded-full bg-black/5 dark:bg-white/10 overflow-hidden"><div class="h-full rounded-full bg-current opacity-60" :style="{ width: Math.min((e.pct / maxPct) * 100, 100) + '%' }"></div></div>
            </div>
          </div>

          <!-- غلظت در محلول (ابزارک مستقل) -->
          <div v-if="standalone" class="rounded-xl bg-sky-50/70 dark:bg-sky-900/15 border border-sky-200 dark:border-sky-800/50 p-3 space-y-2.5">
            <p class="text-[12px] font-semibold text-sky-900 dark:text-sky-200">این کود در محلول چقدر می‌شود؟</p>
            <div class="grid grid-cols-2 gap-2.5">
              <label class="text-[11px] text-gray-600 dark:text-gray-300">مقدار کود (گرم)<input v-model.number="dissolveG" type="number" min="0" dir="ltr" class="mt-1 w-full h-9 px-2 text-center text-sm rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 tabular-nums" /></label>
              <label class="text-[11px] text-gray-600 dark:text-gray-300">حجم آب (لیتر)<input v-model.number="dissolveL" type="number" min="0" dir="ltr" class="mt-1 w-full h-9 px-2 text-center text-sm rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 tabular-nums" /></label>
            </div>
            <div v-if="ppmList.length" class="grid grid-cols-2 sm:grid-cols-3 gap-2">
              <div v-for="e in ppmList" :key="e.key" class="rounded-lg bg-white dark:bg-gray-800 border border-sky-100 dark:border-sky-900/40 px-2.5 py-1.5 flex items-center justify-between gap-2">
                <span class="text-[11px] text-gray-600 dark:text-gray-300">{{ e.symbol }}</span>
                <b class="text-sm tabular-nums" dir="ltr">{{ e.ppm.toLocaleString('fa-IR', { maximumFractionDigits: 1 }) }} <span class="text-[10px] font-normal text-gray-400">ppm</span></b>
              </div>
            </div>
            <p v-else class="text-[11px] text-gray-400">مقدار کود و حجم آب را بنویسید تا غلظت هر عنصر (میلی‌گرم در لیتر) نمایش داده شود.</p>
          </div>

          <div v-if="!standalone" class="flex flex-wrap items-center gap-2 pt-0.5">
            <button type="button" :disabled="!canApply" @click="apply"
              class="flex-1 min-w-[12rem] h-11 rounded-xl text-sm font-bold text-white bg-gradient-to-l from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 shadow-md shadow-emerald-600/20 transition-all active:scale-[.99] disabled:opacity-40 disabled:cursor-not-allowed disabled:shadow-none flex items-center justify-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.4"><path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" /></svg>
              اعمال روی جدول عناصر
            </button>
            <button type="button" @click="rows.splice(0); extras.splice(0); addRow()" class="h-11 px-4 rounded-xl text-sm text-gray-600 dark:text-gray-300 border border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">پاک کردن</button>
          </div>
          <p class="text-[11px] text-gray-400 leading-5">با اعمال، مقدار فعلی جدول با این نتیجه جایگزین می‌شود و بعداً می‌توانید دستی ویرایش کنید.</p>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue';
import { analyse, FormulaError, parseFormula, type Analysis } from '@/utils/chemFormula';
import { ELEMENT_DEFS, getElementDef, prettyFormula } from '@/utils/labelForms';

const props = defineProps<{ entries?: Record<string, { form: string; value: number | null }>; standalone?: boolean }>();
const emit = defineEmits<{ (e: 'applied', info: { formula: string | null }): void }>();

interface Row { id: number; formula: string; amount: number | null; genericN: 'N-NH4' | 'N-NO3'; custom: Record<string, number | null | ''>; showCustom: boolean }
interface Extra { id: number; key: string; pct: number | null }
let seq = 0;
const rows = reactive<Row[]>([]);
const extras = reactive<Extra[]>([]);
const mkRow = (formula = '', amount: number | null = null): Row => ({ id: ++seq, formula, amount, genericN: 'N-NH4', custom: {}, showCustom: false });
const hasCustom = (r: Row) => Object.values(r.custom).some((v) => v !== null && v !== '' && Number.isFinite(Number(v)));
const clearCustom = (r: Row) => { r.custom = {}; };
const quick = ref('');
const showHelp = ref(false);
const POPULAR = [
  { f: 'KNO3', n: 'نیترات پتاسیم' }, { f: 'Ca(NO3)2·4H2O', n: 'نیترات کلسیم ۴آبه' }, { f: 'KH2PO4', n: 'مونوپتاسیم فسفات' },
  { f: 'MgSO4·7H2O', n: 'سولفات منیزیم' }, { f: 'K2SO4', n: 'سولفات پتاسیم' }, { f: 'H3BO3', n: 'اسید بوریک' }
];
const EXAMPLES = [
  { t: 'مخلوط دو نمک', rows: [['KNO3', 50], ['Ca(NO3)2·4H2O', 30]] },
  { t: 'فرم اکسیدی NPK', rows: [['P2O5', 20], ['K2O', 20]] },
  { t: 'کود ۱۰۰٪ خالص', rows: [['(NH4)2SO4', 100]] }
] as { t: string; rows: [string, number][] }[];
const loadExample = (ex: { rows: [string, number][] }) => {
  rows.splice(0);
  for (const [f, a] of ex.rows) { rows.push(mkRow(f, a)); }
  extras.splice(0);
};

const QUICK = [
  { title: 'نیتروژن', items: [
    { n: 'نیترات پتاسیم', f: 'KNO3' }, { n: 'نیترات کلسیم ۴آبه', f: 'Ca(NO3)2·4H2O' }, { n: 'نیترات منیزیم', f: 'Mg(NO3)2·6H2O' },
    { n: 'نیترات آمونیوم', f: 'NH4NO3' }, { n: 'سولفات آمونیوم', f: '(NH4)2SO4' }, { n: 'اوره', f: 'CO(NH2)2' }] },
  { title: 'فسفر و پتاسیم', items: [
    { n: 'مونوپتاسیم فسفات', f: 'KH2PO4' }, { n: 'مونوآمونیوم فسفات', f: 'NH4H2PO4' }, { n: 'اسید فسفریک', f: 'H3PO4' },
    { n: 'سولفات پتاسیم', f: 'K2SO4' }, { n: 'کلرید پتاسیم', f: 'KCl' }, { n: 'پنتااکسید فسفر (P₂O₅)', f: 'P2O5' }, { n: 'اکسید پتاسیم (K₂O)', f: 'K2O' }] },
  { title: 'کلسیم، منیزیم و گوگرد', items: [
    { n: 'سولفات منیزیم ۷آبه', f: 'MgSO4·7H2O' }, { n: 'گچ', f: 'CaSO4·2H2O' }, { n: 'اکسید منیزیم', f: 'MgO' }, { n: 'اکسید کلسیم', f: 'CaO' }, { n: 'اسید سولفوریک', f: 'H2SO4' }] },
  { title: 'ریزمغذی‌ها', items: [
    { n: 'سولفات آهن ۷آبه', f: 'FeSO4·7H2O' }, { n: 'سولفات منگنز یک‌آبه', f: 'MnSO4·H2O' }, { n: 'سولفات روی ۷آبه', f: 'ZnSO4·7H2O' },
    { n: 'سولفات مس ۵آبه', f: 'CuSO4·5H2O' }, { n: 'اسید بوریک', f: 'H3BO3' }, { n: 'سولوبور', f: 'Na2B8O13·4H2O' }, { n: 'مولیبدات سدیم ۲آبه', f: 'Na2MoO4·2H2O' }] },
];

const addRow = (formula = '') => { rows.push(mkRow(formula)); };
const addQuick = () => { if (quick.value) addRow(quick.value); quick.value = ''; };
addRow();

// تحلیل هر ردیف (واکنشی)
const states = computed(() =>
  rows.map((r) => {
    if (!r.formula.trim()) return { analysis: null as Analysis | null, error: '' };
    try { return { analysis: analyse(parseFormula(r.formula), r.genericN), error: '' }; }
    catch (e) { return { analysis: null, error: e instanceof FormulaError ? e.message : 'فرمول معتبر نیست' }; }
  })
);
const symbol = (k: string) => (k === 'N-NO3' ? 'N نیترات' : k === 'N-NH4' ? 'N آمونیوم' : getElementDef(k)?.symbol || k);
const amountSum = computed(() => rows.reduce((s, r, i) => s + (states.value[i].analysis ? Number(r.amount) || 0 : 0), 0));
const totals = computed<Record<string, number>>(() => {
  const t: Record<string, number> = {};
  rows.forEach((r, i) => {
    const a = states.value[i].analysis;
    const amt = Number(r.amount) || 0;
    if (!a) return;
    for (const [k, frac] of Object.entries(a.elements)) {
      const manual = r.custom[k];
      if (manual !== null && manual !== undefined && manual !== '' && Number.isFinite(Number(manual))) t[k] = (t[k] || 0) + Number(manual);   // مقدار دستی کاربر
      else if (amt > 0) t[k] = (t[k] || 0) + amt * frac;                                                                                       // محاسبهٔ خودکار
    }
  });
  for (const x of extras) if (Number(x.pct) > 0) t[x.key] = (t[x.key] || 0) + Number(x.pct);
  return t;
});
const resultList = computed(() =>
  ELEMENT_DEFS.filter((d) => (totals.value[d.key] || 0) > 0.00005)
    .map((d) => ({ key: d.key, name: d.name, symbol: symbol(d.key), pct: Math.round(totals.value[d.key] * 10000) / 10000 }))
);
const maxPct = computed(() => Math.max(0.0001, ...resultList.value.map((e) => e.pct)));
const isMicro = (k: string) => ['Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo', 'Si'].includes(k);
const chipCls = (k: string) => k.startsWith('N')
  ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-900/25 dark:text-emerald-300'
  : isMicro(k) ? 'bg-amber-50 text-amber-700 dark:bg-amber-900/25 dark:text-amber-300' : 'bg-blue-50 text-blue-700 dark:bg-blue-900/25 dark:text-blue-300';
const tileCls = (k: string) => k.startsWith('N')
  ? 'bg-emerald-50/70 dark:bg-emerald-900/15 border-emerald-200 dark:border-emerald-800/50 text-emerald-600'
  : isMicro(k) ? 'bg-amber-50/70 dark:bg-amber-900/15 border-amber-200 dark:border-amber-800/50 text-amber-600' : 'bg-blue-50/70 dark:bg-blue-900/15 border-blue-200 dark:border-blue-800/50 text-blue-600';
const dissolveG = ref<number | null>(null);
const dissolveL = ref<number | null>(null);
const ppmList = computed(() => {
  const g = Number(dissolveG.value), l = Number(dissolveL.value);
  if (!(g > 0 && l > 0)) return [];
  return resultList.value.map((e) => ({ key: e.key, symbol: e.symbol, ppm: (e.pct / 100) * (g * 1000) / l }));
});
const hasResult = computed(() => resultList.value.length > 0);
const canApply = computed(() => hasResult.value && amountSum.value <= 100.0001 && resultList.value.every((e) => e.pct <= 100));

const apply = () => {
  if (!props.entries) return;
  const entries = props.entries;
  const filled = ELEMENT_DEFS.some((d) => Number(entries[d.key]?.value) > 0);
  if (filled && !confirm('مقدار فعلی جدول عناصر با نتیجهٔ این ترکیب جایگزین شود؟')) return;
  for (const d of ELEMENT_DEFS) entries[d.key] = { form: d.key.startsWith('N-') ? 'N' : d.key, value: null };
  for (const e of resultList.value) {
    const d = getElementDef(e.key)!;
    entries[e.key] = { form: d.key.startsWith('N-') ? 'N' : d.key, value: e.pct };
  }
  // اگر فقط یک جزء با ۱۰۰٪ بود، فرمول همان جزء را برای فیلد «فرمول» پیشنهاد بده
  const used = rows.filter((r, i) => states.value[i].analysis && Number(r.amount) > 0);
  emit('applied', { formula: used.length === 1 ? prettyFormula(used[0].formula.replace(/[·.]/g, '·')) : null });
};

</script>

<style scoped>
input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
input[type=number] { -moz-appearance: textfield; appearance: textfield; }
input:focus, select:focus { outline: none; }
.ab-enter-active, .ab-leave-active { transition: all .2s ease; }
.ab-enter-from { opacity: 0; transform: translateY(-6px) scale(.985); }
.ab-leave-to { opacity: 0; transform: translateX(14px); }
</style>
