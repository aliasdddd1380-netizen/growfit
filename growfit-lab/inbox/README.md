# فایل‌های ارسالی برای بررسی

فایل‌هایی که می‌خواهی من بررسی کنم یا نسخه‌های طراحی‌شدهٔ جدید را اینجا بارگذاری کن.

## روش ارسال
1. وارد پوشهٔ `growfit-lab/inbox` شو.
2. گزینهٔ **Add file → Upload files** را بزن.
3. فایل‌ها یا پوشهٔ فایل‌هایت را انتخاب و بارگذاری کن.
4. تغییرات را با **Commit changes** ذخیره کن.
5. همین‌جا در گفت‌وگو بگو «فایل‌ها رو گذاشتم».

## نکات
- فایل‌های اصلی پروژه را اینجا جایگزین نکن.
- اگر چند فایل به هم وابسته‌اند، همه را با ساختار پوشه‌ای اصلی‌شان بارگذاری کن.
- اگر فایل HTML به CSS، JS، تصویر یا فونت نیاز دارد، همهٔ وابستگی‌هایش را هم بفرست.
- بعد از بارگذاری، من فایل‌ها را از همین مسیر می‌خوانم و بررسی می‌کنم.

## USDA nutrition enrichment

The preview workflow also runs the USDA FoodData Central enrichment script when `USDA_API_KEY` is configured as a GitHub Actions repository secret. Matched food records are added only when confidence checks pass; ambiguous or missing matches are kept for review rather than guessed.
