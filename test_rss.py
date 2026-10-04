#!/usr/bin/env python3
"""اختبار RSS feeds للمواقع الجزائرية"""
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36"
}

FEEDS = [
    "https://www.anem.dz/rss",
    "https://www.anem.dz/feed",
    "https://www.dgfp.gov.dz/rss",
    "https://www.dgfp.gov.dz/feed",
    "https://www.emploitic.com/rss",
    "https://www.emploitic.com/feed",
    "https://www.education.gov.dz/rss",
    "https://www.education.gov.dz/feed",
    "https://www.sante.gov.dz/rss",
    "https://www.sante.gov.dz/feed",
    "https://www.mtess.gov.dz/rss",
    "https://www.mtess.gov.dz/feed",
]

print("═" * 60)
print("🔍 اختبار RSS Feeds")
print("═" * 60)

for url in FEEDS:
    try:
        r = requests.get(url, headers=headers, timeout=8, allow_redirects=True)
        ct = r.headers.get("content-type", "")
        is_xml = "xml" in ct or "rss" in ct or r.text.strip().startswith("<?xml")
        icon = "✅" if (r.status_code == 200 and is_xml) else "❌"
        print(f"{icon} {r.status_code} | {len(r.text):>7} | {url}")
        if r.status_code == 200 and is_xml:
            # اعرض أول سطر
            print(f"     {r.text[:100]}")
    except Exception as e:
        print(f"❌ ERR | {url} → {str(e)[:50]}")
