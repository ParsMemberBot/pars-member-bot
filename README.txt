📦 راه‌اندازی ربات فروش خدمات + مدیریت گروه (مخصوص بله)

ساختار فایل‌ها:
- main.py: فایل اصلی اجرا
- bot/: شامل فایل‌های store.py, admin.py, utils.py, group.py, fun.py
- data/: شامل فایل‌های users.json, orders.json, settings.json

برای اجرای ربات:
1. مطمئن شوید پکیج requests نصب است (در Pydroid یا Termux):
   pip install requests
2. مقدار API_URL در main.py را با توکن و آیدی عددی خود تنظیم کنید
3. فایل‌ها را در مسیر درست قرار دهید و اجرا کنید:
   python main.py