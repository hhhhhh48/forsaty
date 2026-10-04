#!/usr/bin/env python3
"""اختبار مصادر RSS جديدة"""
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36"
}

FEEDS = [
    ("jobs4dz-main",     "https://www.jobs4dz.com/feed/"),
    ("jobs4dz-jobs",     "https://www.jobs4dz.com/category/عروض-التوظيف/feed/"),
    ("jobs4dz-concours", "https://www.jobs4dz.com/category/مسابقات-التوظيف/feed/"),
    ("ouedkniss-fr",     "http://ouedkniss.fr/feed/"),
    ("emploitic",        "https://www.emploitic.com/feed/"),
    ("tawthif",          "https://www.tawthifdz.com/feed/"),
    ("algem",            "https://www.algem.com/feed/"),
]

print("═" * 60)
print("🔍 اختبار مصادر جديدة")
print("═" * 60)

for name, url in FEEDS:
    try:
        r = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
        ct = r.headers.get("content-type", "")
        is_xml = "xml" in ct or r.text.strip().startswith("<?xml")
        icon = "✅" if (r.status_code == 200 and is_xml) else "❌"
        print(f"{icon} [{name:18}] {r.status_code} | {len(r.text):>7} | {url[:50]}")
    except Exception as e:
        print(f"❌ [{name:18}] ERR | {str(e)[:40]}")
