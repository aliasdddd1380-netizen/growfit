# طرح ساختار منبع‌دهی مستقل برای هر ریزمغذی

تاریخ: 2026-11-14  
وضعیت: نمونه اولیه و آزمون‌های سازگاری پیاده‌سازی شده؛ انتشار داده همچنان غیرفعال  
محدوده: فقط محیط آزمایشگاهی GrowFit

## هدف

ساختار فعلی بانک غذایی برای هر ماده یک شیء micronutrientsPer100g و یک منبع کلی fdcMatch دارد. این مدل زمانی مناسب است که همه مقادیر از یک رکورد USDA آمده باشند؛ اما برای ترکیب کنترل‌شده منابع علمی مختلف کافی نیست.

طرح حاضر به هر مقدار ریزمغذی provenance مستقل می‌دهد: منبع، نوع داده، واحد، مبنای اندازه‌گیری، روش آزمایش و وضعیت بازبینی.

این ساختار به‌عنوان بسته‌ای مستقل در پوشه tools پیاده‌سازی شده است. اسکریپت enrichment فقط تضمین می‌کند شواهد مستقل را هنگام به‌روزرسانی فیلدهای USDA حفظ کند؛ صفحه تغذیه و محاسبات وعده همچنان فقط ساختار قدیمی micronutrientsPer100g را می‌خوانند. هیچ فایل بانک غذایی یا صفحه کاربر برای فعال‌سازی این شواهد تغییر نکرده است.

## اصول طراحی

1. منبع در سطح هر nutrient value ذخیره شود، نه فقط در سطح ماده غذایی.
2. مقدار خام منبع بدون دستکاری حفظ شود؛ مقدار استانداردشده جداگانه ثبت شود.
3. واحد و مخرج همیشه صریح باشند؛ مثلاً mg/kg dry matter با mg/100g edible portion یکی نیست.
4. وضعیت خام/پخته و روش پخت ثبت شود.
5. نوع داده مشخص شود: آزمایشگاهی، محاسبه‌شده از دستور، اقتباس‌شده از جدول دیگر یا برآوردشده.
6. مقادیر نامعلوم null بمانند؛ نبود داده هرگز صفر نیست.
7. مقدار تبدیل‌شده فقط وقتی قابل انتشار باشد که فرمول، ضریب تبدیل و داده ورودی لازم مستند باشند.
8. آلاینده‌ها و فلزات سمی در فیلدهای مواد معدنی تغذیه‌ای قرار نگیرند.
9. یک nutrient می‌تواند چند شاهد داشته باشد، اما فقط یک مقدار منتخب و تأییدشده وارد نمای تغذیه‌ای شود.
10. رکوردهای USDA همچنان با شناسه FDC خود نگهداری شوند؛ منابع غیر USDA نباید به‌زور در fdcMatch جا داده شوند.

## ساختار پیشنهادی در سطح ماده غذایی

نمونه مفهومی برای آهن سنگک:

{
  "id": 27,
  "name": "نان سنگک",
  "nutrientEvidence": {
    "iron": [
      {
        "evidenceId": "SANGAK-IRON-2012-A",
        "sourceId": "SANGAK-BARBARI-MINERALS-2012",
        "rawValue": 37.6,
        "rawUnit": "µg/g",
        "rawBasis": "as-reported; moisture basis not confirmed",
        "standardValue": null,
        "standardUnit": "mg/100g edible portion",
        "standardBasis": "edible portion",
        "conversion": null,
        "foodState": "baked",
        "sampleCountry": "Iran",
        "sampleRegion": null,
        "sampleYear": 2012,
        "sampleCount": null,
        "method": null,
        "dataType": "analytical",
        "reviewStatus": "research-only",
        "reviewNote": "Basis is not sufficient for safe conversion to edible-weight value."
      }
    ]
  },
  "micronutrientsPer100g": {
    "iron": null
  }
}

در مثال بالا مقدار خام مقاله حفظ می‌شود، اما مقدار استانداردشده عمداً null است؛ بنابراین رابط کاربری فعلی نباید آن را به‌عنوان آهن در هر ۱۰۰ گرم نمایش دهد.

## قرارداد فیلدها

| فیلد | کاربرد |
|---|---|
| evidenceId | شناسه یکتای مشاهده/مقدار |
| sourceId | ارجاع به رکورد منبع در فهرست منابع |
| rawValue, rawUnit, rawBasis | مقدار دقیقاً مطابق منبع |
| standardValue, standardUnit, standardBasis | مقدار تبدیل‌شده فقط در صورت تبدیل معتبر |
| conversion | فرمول، ضرایب، ورودی‌ها و توضیح تبدیل |
| foodState | خام، پخته، خشک، پخته‌شده با روش مشخص و مانند آن |
| sampleCountry, sampleRegion, sampleYear | محل و زمان نمونه‌برداری |
| sampleCount | تعداد نمونه‌ها، در صورت گزارش |
| method | روش آزمایشگاهی یا محاسباتی |
| dataType | analytical، calculated، borrowed یا estimated |
| reviewStatus | وضعیت ارزیابی و اجازه استفاده |
| reviewNote | محدودیت‌ها و توضیح بازبین |

## وضعیت‌های مجاز

- research-only: شاهد علمی ثبت شده، اما قابل استفاده در محاسبات برنامه نیست.
- needs-review: اطلاعات برای تصمیم‌گیری کافی نیست.
- approved: مقدار و مبنای آن بررسی و برای استفاده تأیید شده است.
- rejected: این شاهد برای این ماده/مغذی قابل استفاده نیست.

## فهرست منابع مستقل

نمونه:

{
  "sources": [
    {
      "sourceId": "SANGAK-BARBARI-MINERALS-2012",
      "title": "Dephytinisation of Sangak and Barbari bread made from different extraction rate flours increases iron and zinc bioaccessibility in Caco-2 cells",
      "year": 2012,
      "url": "https://academic.oup.com/ijfst/article/47/11/2252/7865861",
      "sourceType": "peer-reviewed-article",
      "country": "Iran",
      "bibliographicNote": "Record source metadata once; link individual nutrient observations to this source."
    }
  ]
}

## سازگاری با نسخه فعلی GrowFit

برای جلوگیری از شکستن داشبورد یا pipeline، مهاجرت باید دو مرحله‌ای باشد.

### مرحله A — فقط ذخیره شواهد

- افزودن nutrientEvidence به‌صورت ساختار افزوده و غیرفعال.
- نگه داشتن micronutrientsPer100g و fdcMatch بدون تغییر.
- اسکریپت enrichment با تابع apply_usda_fields فیلدهای USDA را به‌روزرسانی می‌کند و برابری nutrientEvidence قبل و بعد از تغییر را کنترل می‌کند؛ تست رگرسیون این حفاظت را بررسی می‌کند.
- صفحه تغذیه همچنان فقط مقدارهای قدیمی را نمایش دهد.
- شواهد ناقص و dry-weight فقط در گزارش پژوهشی بمانند.

### مرحله B — انتشار مقدارهای تأییدشده، پس از تأیید جداگانه

- یک مرحله اعتبارسنجی، فقط مقادیر approved با واحد و مبنای سازگار را به نمای استاندارد micronutrientsPer100g منتقل کند.
- هر مقدار منتشرشده باید منبع قابل نمایش داشته باشد.
- اگر یک ماده برای یک nutrient چند مقدار معتبر دارد، سیاست انتخاب/میانگین‌گیری باید مستند و قابل ممیزی باشد.
- مجموع ریزمغذی وعده فقط از مقادیر استانداردشده و تأییدشده محاسبه شود.
- مقدار نامعلوم در هر ماده اولیه باعث نامعلوم ماندن مجموع همان nutrient در وعده شود.

## قواعد ویژه تبدیل

- mg/kg به mg/100g از نظر ریاضی ضریب 0.1 دارد، اما این تبدیل به‌تنهایی مشکل تفاوت dry matter و edible portion را حل نمی‌کند.
- µg/g به mg/100g از نظر ریاضی ضریب 0.1 دارد؛ اما تنها در صورتی می‌توان آن را استفاده کرد که مخرج و مبنای رطوبت با هدف سازگار باشد.
- per 100 mL برای نوشیدنی‌هایی مانند دوغ، بدون چگالی معتبر نباید به per 100 g تبدیل شود.
- نمک معادل سدیم نیست؛ تبدیل فقط با تعریف و روش مشخص مجاز است.
- انرژی از یک منبع جایگزین نباید کورکورانه کپی شود؛ در صورت نیاز باید با تعریف اجزا و عوامل تبدیل سازگار محاسبه و مستند شود.
- تعریف اجزای غذایی نیز مهم است؛ برای مثال روش سنجش فیبر و تعریف معادل ویتامین A می‌تواند مقدار گزارش‌شده را تغییر دهد.

## تست‌های لازم پیش از فعال‌سازی

- مقدار null به صفر تبدیل نشود.
- داده dry-weight به‌عنوان edible-portion پذیرفته نشود.
- رکورد خام و پخته به‌جای یکدیگر انتخاب نشوند.
- مقدار بدون منبع یا بدون واحد رد شود.
- مقدار research-only و needs-review وارد مجموع وعده نشود.
- اجرای مجدد enrichment، شواهد دستی و منبع‌های غیر USDA را حذف نکند.
- اگر یک ماده اولیه مقدار یک nutrient را ندارد، مجموع آن nutrient برای وعده null شود.
- صفحه تغذیه منبع و وضعیت پوشش را دقیقاً مطابق داده واقعی نمایش دهد.

## منابع راهنما

- FAO/INFOODS, Guidelines for Food Matching, Version 1.2 (2012): https://www.fao.org/fileadmin/templates/food_composition/documents/upload/INFOODSGuidelinesforFoodMatching_version_1_2.pdf
- FAO/INFOODS, Guidelines for Checking Food Composition Data: https://www.fao.org/fileadmin/templates/food_composition/documents/pdf/Guidelines_data_checking2012.pdf
- FAO, Food Composition Data — conventions and modes of expression: https://www.fao.org/4/y4705e/y4705E14.htm
- FAO/INFOODS Standards & Guidelines: https://www.fao.org/infoods/infoods/standards-guidelines/en/

این راهنماها بر تطبیق دقیق هویت غذا، تعریف nutrient، روش، واحد و مخرج و نیز مستندسازی منبع در سطح مقدار تأکید دارند.

## وضعیت اجرای پیاده‌سازی و کنترل‌ها

نمونه اولیهٔ مرحله A در پوشه tools ایجاد شده است:

- `nutrient-evidence.schema.json`: قرارداد JSON Schema نسخه Draft 2020-12.
- `nutrient-evidence.sample.json`: شاهد آهن سنگک با مقدار خام 37.6 µg/g و وضعیت research-only؛ مقدار استانداردشده عمداً null است.
- `validate-nutrient-evidence.py` و `test-nutrient-evidence-validator.py`: اعتبارسنج و تست‌های مثبت/منفی.
- `apply_usda_fields` در `enrich-food-bank.py`: به‌روزرسانی فیلدهای تحت مالکیت USDA بدون دست‌کاری شواهد مستقل، همراه با کنترل برابری شواهد قبل و بعد.
- `test-enrichment-evidence-preservation.py`: تست حفظ شواهد در به‌روزرسانی تکی و تکراری، نبود شواهد برای رکوردهای قدیمی، و عدم ورود داده research-only به مجموع وعده.
- workflow صفحات آزمایشگاهی، این تست‌ها را اجرا می‌کند و enrichment را فقط وقتی اجرا می‌کند که ورودی‌های پوشه inbox تغییر کرده باشند یا workflow به‌صورت دستی اجرا شود؛ تغییرات tools به‌تنهایی نباید بانک را بازنویسی کند.

### مرز فعال‌سازی

این پیاده‌سازی فقط ذخیره‌سازی/اعتبارسنجی و حفاظت از داده است. هیچ شاهد research-only یا needs-review وارد `micronutrientsPer100g` نشده و هیچ مقداری از `nutrientEvidence` در محاسبات وعده استفاده نمی‌شود. انتشار مقادیر approved، انتخاب منبع برتر در صورت چند شاهد، نمایش منبع در رابط کاربری و مهاجرت بانک غذایی همگی خارج از این مرحله‌اند و به تأیید جداگانه نیاز دارند.

## وضعیت این طرح

- سند طراحی، JSON Schema، نمونه، اعتبارسنج و تست‌های رگرسیون در پوشه tools قرار دارند.
- بانک غذایی تغییر نکرده است.
- enrichment script فقط برای حفظ nutrientEvidence در زمان نوشتن فیلدهای USDA به‌روزرسانی شده است.
- صفحه تغذیه تغییر نکرده است.
- هیچ مقدار پژوهشی به محاسبات وعده‌ها وارد نشده است.
