#!/usr/bin/env python3
"""auto_fetch.py - جمع تلقائي للفرص"""
import re
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from database import get_db, init_db

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36"
}

RSS_FEEDS = [
    ("https://www.jobs4dz.com/feed/", "travail", "emploi"),
    ("https://www.jobs4dz.com/التوظيف-حسب-الولايات/الجزائر/feed/", "travail", "emploi"),
    ("https://elikaaonline.com/tag/التوظيف-في-الجزائر/feed/", "travail", "emploi"),
    ("https://www.education.gov.dz/rss", "education", "concours"),
]

JOB_KEYWORDS = [
    "توظيف", "مسابقة", "منصب", "مناصب", "استدعاء", "مترشح",
    "ترشح", "ترشيح", "المسابقة", "مسابقات",
    "recrutement", "concours", "emploi", "poste",
    "مفتش", "مهندس", "أستاذ", "عون", "ملحق", "متصرف",
    "محاسب", "تقني", "إداري", "سائق", "حارس", "طبيب",
    "ممرض", "قاضي", "ضابط", "شرطي", "دركي", "أعوان",
]

NEWS_KEYWORDS = [
    "ندوة", "زيارة", "افتتاح", "تكريم", "حفل",
    "تصريح", "اجتماع", "ملتقى", "مؤتمر", "احتفال",
    "اقتناء", "مناقصة", "شراء", "توريد", "صفقة",
    "صيانة", "إصلاح", "بناء", "ترميم",
    "مباراة رياضية", "المنتخب", "كأس", "الترتيب",
    "مؤشر", "اليونسكو", "دورة عالمية",
]


def is_job_opportunity(title, description):
    text = (title + " " + description).lower()
    for news in NEWS_KEYWORDS:
        if news.lower() in text:
            return False
    for job in JOB_KEYWORDS:
        if job.lower() in text:
            return True
    return False


def parse_rss(url, sector_code, opp_type):
    items = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(f"❌ {url[:50]}: {str(e)[:40]}")
        return items

    content = r.content
    xml_start = content.find(b'<?xml')
    if xml_start > 0:
        content = content[xml_start:]

    try:
        root = ET.fromstring(content.strip())
    except ET.ParseError as e:
        print(f"❌ XML error: {str(e)[:50]}")
        return items

    for item in root.iter("item"):
        title_el = item.find("title")
        link_el = item.find("link")
        desc_el = item.find("description")

        if title_el is None or title_el.text is None:
            continue

        title = title_el.text.strip()
        if len(title) < 5:
            continue

        desc = ""
        if desc_el is not None and desc_el.text:
            desc = re.sub(r"<[^>]+>", " ", desc_el.text)
            desc = re.sub(r"\s+", " ", desc).strip()[:500]

        if not is_job_opportunity(title, desc):
            continue

        link = link_el.text.strip() if link_el is not None and link_el.text else "#"

        items.append({
            "title": title[:200],
            "description": desc,
            "url": link,
            "type": opp_type,
            "sector_code": sector_code,
        })

    return items


def save_opportunities(items):
    conn = get_db()
    c = conn.cursor()
    added = 0
    skipped = 0

    for item in items:
        c.execute("SELECT id FROM opportunities WHERE url = ?", (item["url"],))
        if c.fetchone():
            skipped += 1
            continue

        c.execute("SELECT id FROM sectors WHERE code = ?", (item["sector_code"],))
        row = c.fetchone()
        sector_id = row["id"] if row else None

        c.execute("SELECT id FROM sources LIMIT 1")
        row = c.fetchone()
        source_id = row["id"] if row else None

        try:
            c.execute("""
                INSERT INTO opportunities
                (title, description, type, sector_id, source_id,
                 organization, url, added_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item["title"], item["description"], item["type"],
                sector_id, source_id,
                "مصدر رسمي",
                item["url"],
                datetime.now().isoformat()
            ))
            added += 1
            print(f"  ✅ {item['title'][:65]}")
        except Exception as e:
            print(f"  ⚠️ {item['title'][:40]}: {e}")

    conn.commit()
    conn.close()
    return added, skipped


def main():
    print("═" * 60)
    print("🤖 جمع تلقائي للفرص — مصادر متعددة")
    print("═" * 60)

    init_db()
    total_added = 0
    total_skipped = 0

    for feed_url, sector, otype in RSS_FEEDS:
        print(f"\n📡 {feed_url[:60]}")
        items = parse_rss(feed_url, sector, otype)
        print(f"   📊 مقبول: {len(items)}")

        if items:
            added, skipped = save_opportunities(items)
            total_added += added
            total_skipped += skipped

    print()
    print("═" * 60)
    print(f"✅ أضيف:   {total_added}")
    print(f"⏭️ مكرر:   {total_skipped}")
    print("═" * 60)


if __name__ == "__main__":
    main()
