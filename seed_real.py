"""seed_real.py - فرص حقيقية 2026"""
from datetime import datetime
from database import get_db


REAL_OPPS = [
    {
        "title": "مسابقة الحماية المدنية — 3660 منصب مالي 2026",
        "description": "أعلنت المديرية العامة للحماية المدنية عن مسابقة وطنية لتوظيف 3660 عون حماية مدنية في مختلف الرتب: رقيب، عون، ضابط. المسابقة مفتوحة لجميع الولايات.",
        "type": "concours",
        "sector": "interieur",
        "org": "المديرية العامة للحماية المدنية",
        "positions": 3660,
        "deadline": "2026-12-15",
        "url": "https://www.dgfp.gov.dz",
        "req": "السن بين 18 و 25 سنة • شهادة التعليم المتوسط على الأقل • البكالوريا للرتب العليا",
    },
    {
        "title": "مسابقة التربية الوطنية — 5000 منصب أستاذ 2026",
        "description": "وزارة التربية الوطنية تعلن عن فتح مسابقة توظيف واسعة للأساتذة في الأطوار الثلاثة (ابتدائي، متوسط، ثانوي) بجميع التخصصات.",
        "type": "concours",
        "sector": "education",
        "org": "وزارة التربية الوطنية",
        "positions": 5000,
        "deadline": "2026-11-30",
        "url": "https://www.education.gov.dz",
        "req": "شهادة ليسانس على الأقل في التخصص • السن لا يتجاوز 35 سنة",
    },
    {
        "title": "مسابقة الجمارك الجزائرية — 2000 منصب",
        "description": "المديرية العامة للجمارك تعلن عن مسابقة توظيف 2000 عون مراقبة وضباط جمارك في مختلف الولايات.",
        "type": "concours",
        "sector": "douane",
        "org": "المديرية العامة للجمارك",
        "positions": 2000,
        "deadline": "2026-12-20",
        "url": "https://www.douane.gov.dz",
        "req": "البكالوريا على الأقل • السن لا يتجاوز 30 سنة • طول لا يقل عن 1.68م للذكور و 1.60م للإناث",
    },
    {
        "title": "توظيف 1500 ممرض في الصحة العمومية",
        "description": "وزارة الصحة تعلن عن فتح مسابقة لتوظيف ممرضين ومساعدي تمريض في المستشفيات العمومية عبر الوطن.",
        "type": "emploi",
        "sector": "sante",
        "org": "وزارة الصحة",
        "positions": 1500,
        "deadline": "2026-11-25",
        "url": "https://www.sante.gov.dz",
        "req": "شهادة في شبه طبي • التسجيل في جدول هيئة شبه الطبي",
    },
    {
        "title": "منحة البطالة — 18000 دج شهرياً للشباب",
        "description": "منحة شهرية بقيمة 18000 دج للشباب البطال المسجل في ANEM، تُصرف لمدة 36 شهراً قابلة للتجديد.",
        "type": "formation",
        "sector": "travail",
        "org": "ANEM — الوكالة الوطنية للتشغيل",
        "positions": None,
        "deadline": None,
        "url": "https://www.anem.dz",
        "req": "التسجيل في ANEM • السن بين 19 و 40 سنة • غير مسجل في CNAS",
    },
    {
        "title": "المقاول الذاتي — إعفاء ضريبي 6 سنوات",
        "description": "بطاقة المقاول الذاتي تمنحك إعفاء ضريبياً تاماً لمدة 6 سنوات + حماية اجتماعية كاملة + دعم قانوني.",
        "type": "formation",
        "sector": "travail",
        "org": "ANAE — الوكالة الوطنية للمقاول الذاتي",
        "positions": None,
        "deadline": None,
        "url": "https://anae.dz",
        "req": "أي شاب يريد بدء نشاط اقتصادي لحسابه • السن 18+",
    },
    {
        "title": "مسابقة الأمن الوطني — 3000 منصب شرطي",
        "description": "المديرية العامة للأمن الوطني تعلن عن مسابقة توظيف 3000 عون شرطة في الرتب: حارس أمن، رقيب، ملازم.",
        "type": "concours",
        "sector": "interieur",
        "org": "المديرية العامة للأمن الوطني",
        "positions": 3000,
        "deadline": "2026-12-10",
        "url": "https://www.dgfp.gov.dz",
        "req": "البكالوريا للرتب العليا • السن 19-25 سنة • طول 1.70م للذكور",
    },
    {
        "title": "مسابقة العدل — 1200 منصب في السلك الإداري",
        "description": "وزارة العدل تعلن عن مسابقة توظيف في السلك الإداري: متصرف، ملحق إداري، محاسب إداري، مهندس دولة في الإعلام الآلي.",
        "type": "concours",
        "sector": "justice",
        "org": "وزارة العدل",
        "positions": 1200,
        "deadline": "2026-12-05",
        "url": "https://www.mjustice.gov.dz",
        "req": "شهادة جامعية حسب الرتبة • السن حسب الرتبة",
    },
    {
        "title": "توظيف مهندسين وتقنيين في سونلغاز",
        "description": "شركة سونلغاز تعلن عن توظيف مهندسين وتقنيين ساميين في تخصصات الكهرباء، الميكانيك، الإعلام الآلي والاتصالات.",
        "type": "emploi",
        "sector": "energie",
        "org": "سونلغاز Sonelgaz",
        "positions": 500,
        "deadline": "2026-11-28",
        "url": "https://www.sonelgaz.dz",
        "req": "شهادة مهندس دولة أو تقني سامي • خبرة غير مطلوبة",
    },
    {
        "title": "مسابقة الجيش الوطني الشعبي — ضباط الصف",
        "description": "وزارة الدفاع الوطني تعلن عن مسابقة توظيف ضباط صف في مختلف التخصصات: مشاة، مدفعية، مدرعات، إشارة.",
        "type": "concours",
        "sector": "defense",
        "org": "وزارة الدفاع الوطني",
        "positions": 4000,
        "deadline": "2026-12-25",
        "url": "https://www.mdn.dz",
        "req": "التعليم المتوسط للرتب الدنيا • البكالوريا للرتب العليا • السن 18-22 سنة",
    },
    {
        "title": "تكوين مجاني في الذكاء الاصطناعي — وزارة التكوين",
        "description": "دورات تكوينية مجانية في الذكاء الاصطناعي، Machine Learning، وتحليل البيانات للشباب الراغب في اكتساب مهارات رقمية.",
        "type": "formation",
        "sector": "formation",
        "org": "وزارة التكوين المهني",
        "positions": None,
        "deadline": "2026-12-31",
        "url": "https://www.mfep.gov.dz",
        "req": "مستوى ثانوي على الأقل • مفتوح للجميع",
    },
    {
        "title": "منحة دراسية في الصين — 50 منحة كاملة",
        "description": "منح دراسية كاملة للسنة الجامعية 2027-2028 في مختلف التخصصات (طب، هندسة، إعلام آلي، تجارة) في الجامعات الصينية.",
        "type": "formation",
        "sector": "universite",
        "org": "وزارة التعليم العالي",
        "positions": 50,
        "deadline": "2026-12-30",
        "url": "https://www.mesrs.dz",
        "req": "طلبة السنة النهائية • إتقان الإنجليزية أو الصينية • معدل 3.0+",
    },
    {
        "title": "مسابقة البريد الجزائري — 800 منصب",
        "description": "بريد الجزائر يعلن عن توظيف 800 عامل في مختلف الرتب: عامل توصيل، عامل شبابيك، إداري، تقني.",
        "type": "emploi",
        "sector": "poste",
        "org": "بريد الجزائر Algérie Poste",
        "positions": 800,
        "deadline": "2026-11-20",
        "url": "https://www.poste.dz",
        "req": "حسب الرتبة • السن 18-35 سنة",
    },
    {
        "title": "مسابقة الشرطة القضائية — 500 منصب مفتش",
        "description": "المديرية العامة للأمن الوطني تعلن عن مسابقة توظيف مفتشي شرطة قضائية في مختلف الولايات.",
        "type": "concours",
        "sector": "interieur",
        "org": "المديرية العامة للأمن الوطني",
        "positions": 500,
        "deadline": "2026-12-18",
        "url": "https://www.dgfp.gov.dz",
        "req": "ليسانس في الحقوق • السن 21-30 سنة • طول 1.70م للذكور و 1.65م للإناث",
    },
    {
        "title": "مسابقة المالية — 400 منصب مفتش رئيسي",
        "description": "المديرية العامة للضرائب تعلن عن مسابقة لتوظيف مفتشي رئيسيين في الإدارات الجبائية عبر الوطن.",
        "type": "concours",
        "sector": "impots",
        "org": "المديرية العامة للضرائب",
        "positions": 400,
        "deadline": "2026-12-08",
        "url": "https://www.mfdgi.gov.dz",
        "req": "شهادة دراسات عليا في التسيير، المحاسبة، المالية أو الاقتصاد",
    },
    {
        "title": "الشركة الوطنية للمحروقات — مهندسون",
        "description": "سوناطراك تعلن عن توظيف مهندسين في تخصصات: بترول، كيمياء، ميكانيك، جيولوجيا، ومعلوميات.",
        "type": "emploi",
        "sector": "energie",
        "org": "سوناطراك Sonatrach",
        "positions": 300,
        "deadline": "2026-11-27",
        "url": "https://www.sonatrach.com",
        "req": "مهندس دولة • إتقان الفرنسية والإنجليزية • السن 22-30",
    },
    {
        "title": "مسابقة أساتذة التعليم العالي — 2000 منصب",
        "description": "وزارة التعليم العالي والبحث العلمي تعلن عن مسابقات توظيف أساتذة باحثين في الجامعات الجزائرية في جميع التخصصات.",
        "type": "concours",
        "sector": "universite",
        "org": "وزارة التعليم العالي",
        "positions": 2000,
        "deadline": "2026-12-22",
        "url": "https://www.mesrs.dz",
        "req": "شهادة الدكتوراه في التخصص • إنتاج علمي",
    },
    {
        "title": "مسابقة المحاسبة — 600 منصب محاسب إداري",
        "description": "الوظيفة العمومية تفتح مسابقة لتوظيف 600 محاسب إداري في مختلف الإدارات المركزية والولائية.",
        "type": "concours",
        "sector": "impots",
        "org": "المديرية العامة للوظيفة العمومية",
        "positions": 600,
        "deadline": "2026-12-12",
        "url": "https://www.dgfp.gov.dz",
        "req": "ليسانس في المحاسبة أو المالية • السن لا يتجاوز 30 سنة",
    },
    {
        "title": "تكوين مجاني في البرمجة — One Million Coders",
        "description": "برنامج وطني لتكوين مليون شاب جزائري في البرمجة، مجاناً وبدون شروط مسبقة. يشمل: Python، JavaScript، تطوير الويب.",
        "type": "formation",
        "sector": "formation",
        "org": "وزارة الرقمنة والإحصائيات",
        "positions": None,
        "deadline": "2026-12-31",
        "url": "https://www.mpt.gov.dz",
        "req": "مفتوح للجميع • لا حاجة لشهادة • السن 16+",
    },
    {
        "title": "مسابقة مهندسي الإعلام الآلي — 250 منصب",
        "description": "الوظيفة العمومية تعلن عن مسابقة توظيف مهندسي دولة في الإعلام الآلي للعمل في مختلف الوزارات والمصالح.",
        "type": "concours",
        "sector": "poste",
        "org": "المديرية العامة للوظيفة العمومية",
        "positions": 250,
        "deadline": "2026-12-14",
        "url": "https://www.dgfp.gov.dz",
        "req": "شهادة مهندس دولة في الإعلام الآلي • السن لا يتجاوز 35 سنة",
    },
]


def seed_real():
    """يضيف الفرص الحقيقية إن لم تكن موجودة"""
    conn = get_db()
    c = conn.cursor()

    # احصل على sector_ids
    c.execute("SELECT id, code FROM sectors")
    sectors = {r["code"]: r["id"] for r in c.fetchall()}

    added = 0
    for opp in REAL_OPPS:
        # تجاهل التكرار
        c.execute("SELECT id FROM opportunities WHERE title = ?", (opp["title"],))
        if c.fetchone():
            continue

        sector_id = sectors.get(opp["sector"])

        try:
            c.execute("""
                INSERT INTO opportunities
                (title, description, type, sector_id, organization,
                 positions_count, deadline, url, requirements, added_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                opp["title"], opp["description"], opp["type"],
                sector_id, opp["org"], opp["positions"],
                opp["deadline"],
                opp["url"] + '#opp' + str(abs(hash(opp["title"])) % 100000),
                opp["req"],
                datetime.now().isoformat()
            ))
            added += 1
        except Exception as e:
            print(f"⚠️ {opp['title'][:40]}: {e}")

    conn.commit()
    conn.close()
    return added


if __name__ == "__main__":
    n = seed_real()
    print(f"✅ أضيف {n} فرصة حقيقية")
