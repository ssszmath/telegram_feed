import os
import requests
from urllib.parse import urlparse
from datetime import datetime
import hashlib

def read_urls(file_path="urls.txt"):
    """خواندن لیست آدرس‌ها از فایل"""
    if not os.path.exists(file_path):
        print(f"فایل {file_path} یافت نشد.")
        return []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]
    return urls

def generate_filename(url):
    """ساخت نام فایل یکتا از روی آدرس صفحه"""
    parsed = urlparse(url)
    # ترکیب دامنه و مسیر و تبدیل به اسم فایل معتبر
    raw_name = f"{parsed.netloc}{parsed.path}".replace("/", "_").replace(":", "_")
    if not raw_name:
        raw_name = "index"
    
    # اضافه کردن هش کوتاه برای اطمینان از یکتایی
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # فرمت: domain_path_timestamp_hash.txt
    safe_name = f"{raw_name}_{timestamp}_{url_hash}.txt"
    # حذف کاراکترهای غیرمجاز در نام فایل
    safe_name = "".join(c if c.isalnum() or c in "._-" else "_" for c in safe_name)
    return safe_name

def fetch_and_save(url, output_dir="fetched_contents"):
    """دریافت محتوای صفحه و ذخیره در فایل txt"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=30, headers=headers)
        response.raise_for_status()
        
        # ایجاد دایرکتوری خروجی اگر وجود نداشته باشد
        os.makedirs(output_dir, exist_ok=True)
        
        # نام فایل یکتا
        filename = generate_filename(url)
        filepath = os.path.join(output_dir, filename)
        
        # ذخیره محتوا به همراه متادیتا
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"URL: {url}\n")
            f.write(f"Fetch Time: {datetime.now().isoformat()}\n")
            f.write(f"Status Code: {response.status_code}\n")
            f.write(f"Content-Type: {response.headers.get('content-type', 'unknown')}\n")
            f.write("="*80 + "\n\n")
            f.write(response.text)
        
        print(f"✓ ذخیره شد: {filepath}")
        return True
    
    except Exception as e:
        print(f"✗ خطا برای {url}: {str(e)}")
        return False

def main():
    urls = read_urls()
    if not urls:
        print("هیچ آدرسی برای پردازش وجود ندارد.")
        return
    
    print(f"شروع پردازش {len(urls)} آدرس...")
    for url in urls:
        fetch_and_save(url)
    print("پردازش کامل شد.")

if __name__ == "__main__":
    main()
