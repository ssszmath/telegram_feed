import requests
import os
from datetime import datetime

GIST_ID = "gist_id_اینجا"  # مثلاً "abc123def456"
GITHUB_TOKEN = os.environ["GIST_TOKEN"]   # توکنی که توی secrets میذاری
GIST_FILENAME = "scraped_content.json"    # اسم فایل داخل gist

def fetch_urls(url_list_file="urls.txt"):
    with open(url_list_file, "r") as f:
        urls = [line.strip() for line in f if line.strip()]
    return urls

def scrape_all(urls):
    results = {}
    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            results[url] = r.text[:5000]   # محدود کردم به ۵۰۰۰ کاراکتر
        except Exception as e:
            results[url] = f"Error: {str(e)}"
    return results

def save_to_gist(content):
    gist_api_url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "files": {
            GIST_FILENAME: {
                "content": content
            }
        }
    }
    response = requests.patch(gist_api_url, headers=headers, json=payload)
    response.raise_for_status()
    print("✅ Gist updated successfully")

if __name__ == "__main__":
    urls = fetch_urls()
    scraped_data = scrape_all(urls)
    
    # اضافه کردن timestamp
    output = {
        "last_run": datetime.utcnow().isoformat(),
        "data": scraped_data
    }
    
    import json
    content_json = json.dumps(output, indent=2, ensure_ascii=False)
    save_to_gist(content_json)
