// frontend/src/composables/usePrint.ts
import { ref } from 'vue';

export function usePrint() {
  const isPrinting = ref(false);

  // ============================================================
  // چاپ گزارش
  // ============================================================

  function printReport(elementId: string = 'print-area', title: string = 'گزارش تغذیه سبز') {
    isPrinting.value = true;

    try {
      const printElement = document.getElementById(elementId);
      if (!printElement) {
        console.error('عنصر مورد نظر برای چاپ یافت نشد');
        return;
      }

      // ایجاد محتوای چاپ
      const printContent = `
        <!DOCTYPE html>
        <html>
          <head>
            <meta charset="UTF-8">
            <title>${title}</title>
            <style>
              body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                padding: 20px;
                direction: rtl;
              }
              .print-header {
                text-align: center;
                border-bottom: 2px solid #333;
                padding-bottom: 10px;
                margin-bottom: 20px;
              }
              .print-header h1 {
                margin: 0;
                color: #0d6efd;
              }
              .print-header p {
                margin: 5px 0;
                color: #666;
              }
              table {
                width: 100%;
                border-collapse: collapse;
                margin: 10px 0;
                font-size: 12px;
              }
              table th {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                padding: 8px;
                text-align: center;
              }
              table td {
                border: 1px solid #dee2e6;
                padding: 6px;
                text-align: center;
              }
              .print-footer {
                margin-top: 30px;
                text-align: center;
                font-size: 12px;
                color: #666;
                border-top: 1px solid #ddd;
                padding-top: 15px;
              }
              .print-date {
                text-align: left;
                font-size: 12px;
                color: #666;
              }
              @page {
                size: A4;
                margin: 15mm;
              }
              @media print {
                .no-print { display: none; }
                body { margin: 0; }
              }
            </style>
          </head>
          <body>
            <div class="print-header">
              <h1>${title}</h1>
              <p>تاریخ چاپ: ${new Date().toLocaleDateString('fa-IR')}</p>
              <p>زمان: ${new Date().toLocaleTimeString('fa-IR')}</p>
            </div>
            ${printElement.innerHTML}
            <div class="print-footer">
              <p>گزارش تولید شده توسط FarmTech - ProFertilizer</p>
              <p>تمامی حقوق محفوظ است © ${new Date().getFullYear()}</p>
            </div>
          </body>
        </html>
      `;

      // باز کردن پنجره جدید برای چاپ
      const printWindow = window.open('', '_blank', 'width=800,height=600');
      if (!printWindow) {
        console.error('پنجره چاپ باز نشد');
        return;
      }

      printWindow.document.write(printContent);
      printWindow.document.close();

      // چاپ بعد از بارگذاری کامل
      printWindow.onload = function() {
        printWindow.print();
        printWindow.onafterprint = function() {
          printWindow.close();
        };
      };

    } catch (error) {
      console.error('خطا در چاپ:', error);
    } finally {
      isPrinting.value = false;
    }
  }

  // ============================================================
  // چاپ بخشی از صفحه
  // ============================================================

  function printSection(sectionId: string, title?: string) {
    printReport(sectionId, title);
  }

  // ============================================================
  // چاپ کل صفحه
  // ============================================================

  function printFullPage() {
    window.print();
  }

  return {
    isPrinting,
    printReport,
    printSection,
    printFullPage
  };
}