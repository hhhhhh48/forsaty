"""seed.py - ملء البيانات الأولية"""
from database import get_db, init_db


WILAYAS = [
    (1, "أدرار"), (2, "الشلف"), (3, "الأغواط"), (4, "أم البواقي"),
    (5, "باتنة"), (6, "بجاية"), (7, "بسكرة"), (8, "بشار"),
    (9, "البليدة"), (10, "البويرة"), (11, "تمنراست"), (12, "تبسة"),
    (13, "تلمسان"), (14, "تيارت"), (15, "تيزي وزو"), (16, "الجزائر"),
    (17, "الجلفة"), (18, "جيجل"), (19, "سطيف"), (20, "سعيدة"),
    (21, "سكيكدة"), (22, "سيدي بلعباس"), (23, "عنابة"), (24, "قالمة"),
    (25, "قسنطينة"), (26, "المدية"), (27, "مستغانم"), (28, "المسيلة"),
    (29, "معسكر"), (30, "ورقلة"), (31, "وهران"), (32, "البيض"),
    (33, "إليزي"), (34, "برج بوعريريج"), (35, "بومرداس"), (36, "الطارف"),
    (37, "تندوف"), (38, "تيسمسيلت"), (39, "الوادي"), (40, "خنشلة"),
    (41, "سوق أهراس"), (42, "تيبازة"), (43, "ميلة"), (44, "عين الدفلى"),
    (45, "النعامة"), (46, "عين تموشنت"), (47, "غرداية"), (48, "غليزان"),
    (49, "تيميمون"), (50, "برج باجي مختار"), (51, "أولاد جلال"),
    (52, "بني عباس"), (53, "عين صالح"), (54, "عين قزام"),
    (55, "تقرت"), (56, "جانت"), (57, "المغير"), (58, "المنيعة"),
]


SECTORS = [
    ("education", "التربية الوطنية", "📚"),
    ("sante", "الصحة", "🏥"),
    ("justice", "العدل", "⚖️"),
    ("interieur", "الداخلية والجماعات المحلية", "🏛️"),
    ("defense", "الدفاع الوطني", "🎖️"),
    ("douane", "الجمارك", "🛃"),
    ("impots", "الضرائب", "💰"),
    ("travail", "العمل والتشغيل", "👷"),
    ("poste", "البريد والاتصالات", "📮"),
    ("transport", "النقل", "🚌"),
    ("eau", "الموارد المائية", "💧"),
    ("agriculture", "الفلاحة", "🌾"),
    ("jeunesse", "الشباب والرياضة", "⚽"),
    ("culture", "الثقافة", "🎭"),
    ("tourisme", "السياحة", "🏖️"),
    ("habitat", "السكن والعمران", "🏗️"),
    ("energie", "الطاقة والمناجم", "⚡"),
    ("industrie", "الصناعة", "🏭"),
    ("commerce", "التجارة", "🛒"),
    ("telecom", "الاتصالات", "📡"),
    ("banque", "البنوك والمالية", "🏦"),
    ("cnas", "الضمان الاجتماعي", "🛡️"),
    ("universite", "التعليم العالي", "🎓"),
    ("formation", "التكوين المهني", "🔧"),
    ("environnement", "البيئة", "🌳"),
]


SOURCES = [
    ("DGFP - الوظيفة العمومية", "https://www.dgfp.gov.dz", "concours"),
    ("ANEM - التشغيل", "https://www.anem.dz", "emploi"),
    ("Emploitic", "https://www.emploitic.com", "emploi"),
    ("وظيفتي", "https://wathifati.dz", "emploi"),
    ("وزارة التربية", "https://www.education.gov.dz", "concours"),
    ("وزارة الصحة", "https://www.sante.gov.dz", "concours"),
]


def seed_all():
    init_db()
    conn = get_db()
    c = conn.cursor()

    print("📍 إضافة الولايات...")
    for code, name in WILAYAS:
        c.execute(
            "INSERT OR IGNORE INTO wilayas (code, name) VALUES (?, ?)",
            (code, name)
        )

    print("🏢 إضافة القطاعات...")
    for code, name, icon in SECTORS:
        c.execute(
            "INSERT OR IGNORE INTO sectors (code, name, icon) VALUES (?, ?, ?)",
            (code, name, icon)
        )

    print("🌐 إضافة المصادر...")
    for name, url, typ in SOURCES:
        c.execute(
            "INSERT OR IGNORE INTO sources (name, url, type) VALUES (?, ?, ?)",
            (name, url, typ)
        )

    conn.commit()

    # إحصائيات
    c.execute("SELECT COUNT(*) FROM wilayas")
    w = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM sectors")
    s = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM sources")
    src = c.fetchone()[0]

    conn.close()

    print()
    print("═" * 40)
    print(f"✅ الولايات:  {w}")
    print(f"✅ القطاعات:  {s}")
    print(f"✅ المصادر:   {src}")
    print("═" * 40)


if __name__ == "__main__":
    seed_all()
