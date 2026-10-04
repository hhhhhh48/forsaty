"""add_sample.py - إضافة فرص تجريبية"""
from database import get_db

SAMPLES = [
    {
        "title": "مسابقة توظيف 5000 منصب في التربية الوطنية",
        "description": "أعلنت وزارة التربية الوطنية عن فتح مسابقة توظيف لأساتذة التعليم الابتدائي والمتوسط والثانوي في جميع الولايات.",
        "type": "concours",
        "sector_code": "education",
        "organization": "وزارة التربية الوطنية",
        "positions": 5000,
        "deadline": "2026-11-15",
        "url": "https://www.education.gov.dz",
        "requirements": "شهادة جامعية في التخصص + السن لا يتجاوز 35 سنة",
    },
    {
        "title": "مسابقة الحماية المدنية — 3660 منصب",
        "description": "أعلنت المديرية العامة للحماية المدنية عن مسابقة وطنية لتوظيف 3660 عون حماية مدنية في مختلف الرتب.",
        "type": "concours",
        "sector_code": "interieur",
        "organization": "المديرية العامة للحماية المدنية",
        "positions": 3660,
        "deadline": "2026-12-01",
        "url": "https://www.dgfp.gov.dz",
        "requirements": "السن بين 18 و 25 سنة + شهادة التعليم المتوسط على الأقل",
    },
    {
        "title": "منحة البطالة — 18000 دج شهرياً",
        "description": "منحة شهرية للشباب البطال المسجل في ANEM. تُصرف شهرياً لمدة 36 شهراً.",
        "type": "formation",
        "sector_code": "travail",
        "organization": "ANEM + CNAS",
        "positions": None,
        "deadline": None,
        "url": "https://www.anem.dz",
        "requirements": "التسجيل في ANEM + السن بين 19 و 40 سنة",
    },
    {
        "title": "توظيف 1500 ممرض في الصحة العمومية",
        "description": "وزارة الصحة تعلن عن فتح مسابقة لتوظيف ممرضين في المستشفيات العمومية.",
        "type": "emploi",
        "sector_code": "sante",
        "organization": "وزارة الصحة",
        "positions": 1500,
        "deadline": "2026-11-30",
        "url": "https://www.sante.gov.dz",
        "requirements": "شهادة في شبه طبي + التسجيل في جدول هيئة شبه الطبي",
    },
    {
        "title": "مسابقة الجمارك الجزائرية — 2000 منصب",
        "description": "المديرية العامة للجمارك تعلن عن مسابقة لتوظيف 2000 عون مراقبة وضباط جمارك.",
        "type": "concours",
        "sector_code": "douane",
        "organization": "المديرية العامة للجمارك",
        "positions": 2000,
        "deadline": "2026-12-15",
        "url": "https://www.douane.gov.dz",
        "requirements": "شهادة البكالوريا على الأقل + السن لا يتجاوز 30 سنة",
    },
    {
        "title": "المقاول الذاتي — إعفاء ضريبي 6 سنوات",
        "description": "بطاقة المقاول الذاتي تمنحك إعفاء ضريبياً تاماً لمدة 6 سنوات + حماية اجتماعية.",
        "type": "formation",
        "sector_code": "travail",
        "organization": "ANAE — الوكالة الوطنية للمقاول الذاتي",
        "positions": None,
        "deadline": None,
        "url": "https://anae.dz",
        "requirements": "أي شاب يريد بدء نشاط اقتصادي لحسابه",
    },
    {
        "title": "توظيف مهندسين في سونلغاز",
        "description": "سونلغاز تعلن عن توظيف مهندسين في تخصصات كهرباء، ميكانيك، إعلام آلي.",
        "type": "emploi",
        "sector_code": "energie",
        "organization": "سونلغاز",
        "positions": 500,
        "deadline": "2026-11-20",
        "url": "https://www.sonelgaz.dz",
        "requirements": "شهادة مهندس دولة في التخصص",
    },
    {
        "title": "منحة دراسية في الصين — 50 منحة",
        "description": "منح دراسية كاملة للسنة الجامعية 2026-2027 في مختلف التخصصات.",
        "type": "formation",
        "sector_code": "universite",
        "organization": "وزارة التعليم العالي",
        "positions": 50,
        "deadline": "2026-12-20",
        "url": "https://www.mesrs.dz",
        "requirements": "طلبة السنة النهائية + إتقان الإنجليزية أو الصينية",
    },
    {
        "title": "توظيف 800 مساعد إداري",
        "description": "الوظيفة العمومية — مسابقة لتوظيف مساعدين إداريين في الإدارات المركزية.",
        "type": "concours",
        "sector_code": "interieur",
        "organization": "المديرية العامة للوظيفة العمومية",
        "positions": 800,
        "deadline": "2026-11-25",
        "url": "https://www.dgfp.gov.dz",
        "requirements": "شهادة البكالوريا + السن لا يتجاوز 30 سنة",
    },
    {
        "title": "تكوين مجاني في الذكاء الاصطناعي",
        "description": "دورات تكوينية مجانية في AI، Machine Learning، وData Science للمبتدئين.",
        "type": "formation",
        "sector_code": "formation",
        "organization": "وزارة التكوين المهني",
        "positions": None,
        "deadline": "2026-11-30",
        "url": "https://www.mfep.gov.dz",
        "requirements": "مفتوح للجميع — مستوى ثانوي على الأقل",
    },
]


def add_samples():
    conn = get_db()
    c = conn.cursor()

    added = 0
    for s in SAMPLES:
        # احضر sector_id
        c.execute("SELECT id FROM sectors WHERE code = ?", (s["sector_code"],))
        row = c.fetchone()
        sector_id = row["id"] if row else None

        # احضر source_id (اختياري)
        c.execute("SELECT id FROM sources LIMIT 1")
        row = c.fetchone()
        source_id = row["id"] if row else None

        try:
            c.execute("""
                INSERT INTO opportunities
                (title, description, type, sector_id, source_id,
                 organization, positions_count, deadline, url, requirements)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                s["title"], s["description"], s["type"],
                sector_id, source_id, s["organization"],
                s["positions"], s["deadline"], s["url"], s["requirements"]
            ))
            added += 1
            print(f"✅ {s['title'][:50]}")
        except Exception as e:
            print(f"⚠️ {s['title'][:30]}: {e}")

    conn.commit()
    c.execute("SELECT COUNT(*) FROM opportunities")
    total = c.fetchone()[0]
    conn.close()

    print()
    print(f"══════════════════════════════")
    print(f"✅ تمت الإضافة: {added}")
    print(f"📊 المجموع في DB: {total}")
    print(f"══════════════════════════════")


if __name__ == "__main__":
    add_samples()
