"""app.py - منصة فرصتي الكاملة"""
import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
from datetime import datetime
from database import get_db, init_db

# محاولة استيراد seed_all
try:
    from seed import seed_all
except ImportError:
    seed_all = None

# محاولة استيراد seed_real
try:
    from seed_real import seed_real
except ImportError:
    seed_real = None

# ═══════ تهيئة قاعدة البيانات عند بدء التطبيق ═══════
os.makedirs("data", exist_ok=True)

try:
    init_db()
    if seed_all:
        seed_all()
    if seed_real:
        n = seed_real()
        print(f"✅ Seed real: {n} فرصة أضيفت")
except Exception as e:
    print(f"Init error: {e}")

# إنشاء جداول الزوار والإحصائيات
try:
    _conn = get_db()
    _c = _conn.cursor()
    _c.execute("""CREATE TABLE IF NOT EXISTS visits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT, page TEXT,
        visited_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
    _c.execute("""CREATE TABLE IF NOT EXISTS stats (
        key TEXT PRIMARY KEY, value INTEGER DEFAULT 0)""")
    _c.execute("INSERT OR IGNORE INTO stats (key, value) VALUES ('total_visits', 0)")
    _c.execute("INSERT OR IGNORE INTO stats (key, value) VALUES ('unique_visitors', 0)")
    _conn.commit()
    _conn.close()
except Exception as e:
    print(f"Tables error: {e}")


# ═══════ تهيئة Flask ═══════
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "forsaty-secret-2026-change-me")
ADMIN_PASSWORD = "Forsaty@Dz2026"


# ═══════ أدوات مساعدة ═══════
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


def track_visit(page="home"):
    try:
        conn = get_db()
        c = conn.cursor()
        ip = request.remote_addr or "unknown"
        c.execute(
            "INSERT INTO visits (ip, page, visited_at) VALUES (?, ?, ?)",
            (ip, page, datetime.now().isoformat())
        )
        c.execute("UPDATE stats SET value = value + 1 WHERE key = 'total_visits'")
        today = datetime.now().strftime("%Y-%m-%d")
        c.execute(
            "SELECT COUNT(*) FROM visits WHERE ip = ? AND DATE(visited_at) = ?",
            (ip, today)
        )
        if c.fetchone()[0] == 1:
            c.execute("UPDATE stats SET value = value + 1 WHERE key = 'unique_visitors'")
        conn.commit()
        conn.close()
    except Exception:
        pass


def get_visits():
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT value FROM stats WHERE key = 'total_visits'")
        r = c.fetchone()
        total = r[0] if r else 0
        c.execute("SELECT value FROM stats WHERE key = 'unique_visitors'")
        r = c.fetchone()
        unique = r[0] if r else 0
        conn.close()
        return {"total": total, "unique": unique}
    except Exception:
        return {"total": 0, "unique": 0}


# ═══════ الرئيسية ═══════
@app.route("/")
def home():
    track_visit("home")
    visits = get_visits()
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM opportunities")
    total_opps = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM opportunities WHERE type = 'concours'")
    total_concours = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM opportunities WHERE type = 'emploi'")
    total_emploi = c.fetchone()[0]

    c.execute("""
        SELECT o.*, s.name as sector_name, s.icon as sector_icon,
               w.name as wilaya_name, src.name as source_name,
               CASE WHEN julianday('now') - julianday(o.added_at) <= 3
                    THEN 1 ELSE 0 END as is_new
        FROM opportunities o
        LEFT JOIN sectors s ON o.sector_id = s.id
        LEFT JOIN wilayas w ON o.wilaya_id = w.id
        LEFT JOIN sources src ON o.source_id = src.id
        ORDER BY o.added_at DESC
        LIMIT 12
    """)
    opportunities = c.fetchall()

    c.execute("""
        SELECT s.*, COUNT(o.id) as count
        FROM sectors s
        LEFT JOIN opportunities o ON s.id = o.sector_id
        GROUP BY s.id
        HAVING count > 0
        ORDER BY count DESC, s.name
        LIMIT 15
    """)
    sectors = c.fetchall()

    conn.close()
    return render_template("index.html",
                          total_opps=total_opps,
                          total_concours=total_concours,
                          total_emploi=total_emploi,
                          opportunities=opportunities,
                          sectors=sectors,
                          visits=visits)


# ═══════ الفرص ═══════
@app.route("/opportunities")
def opportunities_page():
    track_visit("opportunities")
    conn = get_db()
    c = conn.cursor()
    q = request.args.get("q", "").strip()
    sector_code = request.args.get("sector", "").strip()
    wilaya_code = request.args.get("wilaya", "").strip()
    otype = request.args.get("type", "").strip()

    sql = """
        SELECT o.*, s.name as sector_name, s.icon as sector_icon,
               w.name as wilaya_name, src.name as source_name
        FROM opportunities o
        LEFT JOIN sectors s ON o.sector_id = s.id
        LEFT JOIN wilayas w ON o.wilaya_id = w.id
        LEFT JOIN sources src ON o.source_id = src.id
        WHERE 1=1
    """
    params = []

    if q:
        sql += " AND (o.title LIKE ? OR o.organization LIKE ? OR o.description LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%", f"%{q}%"])
    if sector_code:
        sql += " AND s.code = ?"
        params.append(sector_code)
    if wilaya_code:
        sql += " AND w.code = ?"
        params.append(wilaya_code)
    if otype:
        sql += " AND o.type = ?"
        params.append(otype)

    sql += " ORDER BY o.added_at DESC LIMIT 200"

    c.execute(sql, params)
    opportunities = c.fetchall()

    c.execute("SELECT * FROM sectors ORDER BY name")
    sectors = c.fetchall()
    c.execute("SELECT * FROM wilayas ORDER BY code")
    wilayas = c.fetchall()

    conn.close()
    return render_template("opportunities.html",
                          opportunities=opportunities,
                          sectors=sectors,
                          wilayas=wilayas,
                          q=q,
                          selected_sector=sector_code,
                          selected_wilaya=wilaya_code,
                          selected_type=otype)


# ═══════ التفاصيل ═══════
@app.route("/opportunity/<int:oid>")
def opportunity_detail(oid):
    track_visit("detail")
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT o.*, s.name as sector_name, s.icon as sector_icon,
               w.name as wilaya_name, src.name as source_name
        FROM opportunities o
        LEFT JOIN sectors s ON o.sector_id = s.id
        LEFT JOIN wilayas w ON o.wilaya_id = w.id
        LEFT JOIN sources src ON o.source_id = src.id
        WHERE o.id = ?
    """, (oid,))
    opp = c.fetchone()
    conn.close()
    if not opp:
        return "الفرصة غير موجودة", 404
    return render_template("detail.html", opp=opp)


# ═══════ من نحن / الخصوصية ═══════
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ═══════ تسجيل الدخول ═══════
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["is_admin"] = True
            session.permanent = True
            return redirect(url_for("admin"))
        error = "كلمة السر خاطئة"
    return render_template("admin_login.html", error=error)


@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("admin_login"))


# ═══════ لوحة الإدارة ═══════
@app.route("/admin")
@login_required
def admin():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM sectors ORDER BY name")
    sectors = c.fetchall()
    c.execute("SELECT * FROM wilayas ORDER BY code")
    wilayas = c.fetchall()
    c.execute("""
        SELECT o.*, s.name as sector_name, s.icon as sector_icon
        FROM opportunities o
        LEFT JOIN sectors s ON o.sector_id = s.id
        ORDER BY o.added_at DESC LIMIT 50
    """)
    opps = c.fetchall()
    visits = get_visits()
    conn.close()
    return render_template("admin.html",
                          sectors=sectors, wilayas=wilayas,
                          opportunities=opps, visits=visits)


# ═══════ جلب الفرص تلقائياً ═══════
@app.route("/admin/refetch")
@login_required
def admin_refetch():
    try:
        result = subprocess.run(
            ["python", "auto_fetch.py"],
            capture_output=True, text=True, timeout=120
        )
        output = result.stdout[-1500:] if result.stdout else "لا مخرجات"
        if result.stderr:
            output += "\n\n⚠️ stderr:\n" + result.stderr[-500:]
    except Exception as e:
        output = f"خطأ: {str(e)[:200]}"

    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>جلب الفرص</title>
<style>
body{{font-family:monospace;background:#0a0a0f;color:#10b981;padding:20px;direction:rtl}}
pre{{background:#000;padding:20px;border-radius:10px;border:1px solid #10b981;white-space:pre-wrap;word-break:break-all}}
a{{color:#06b6d4;text-decoration:none;display:inline-block;margin-top:20px;padding:10px 20px;background:#10b981;color:#000;border-radius:8px;font-weight:bold}}
</style></head><body>
<h1 style="color:#fff">🔄 جلب الفرص</h1>
<pre>{output}</pre>
<a href="/admin">← عودة للإدارة</a>
</body></html>"""


# ═══════ إضافة فرصة يدوياً ═══════
@app.route("/admin/add", methods=["POST"])
@login_required
def admin_add():
    conn = get_db()
    c = conn.cursor()
    try:
        title = request.form["title"].strip()
        if not title:
            return "العنوان مطلوب", 400

        sector_code = request.form.get("sector", "").strip()
        wilaya_code = request.form.get("wilaya", "").strip()
        sector_id = None
        wilaya_id = None

        if sector_code:
            c.execute("SELECT id FROM sectors WHERE code = ?", (sector_code,))
            r = c.fetchone()
            if r:
                sector_id = r["id"]
        if wilaya_code:
            c.execute("SELECT id FROM wilayas WHERE code = ?", (wilaya_code,))
            r = c.fetchone()
            if r:
                wilaya_id = r["id"]

        positions = request.form.get("positions", "").strip()
        positions_val = int(positions) if positions.isdigit() else None

        import random
        unique_url = (request.form.get("url", "").strip() or "#") + "#" + str(random.randint(10000, 99999))

        c.execute("""
            INSERT INTO opportunities
            (title, description, type, sector_id, wilaya_id, organization,
             positions_count, deadline, url, requirements)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            title,
            request.form.get("description", "").strip(),
            request.form.get("type", "emploi"),
            sector_id, wilaya_id,
            request.form.get("organization", "").strip(),
            positions_val,
            request.form.get("deadline", "").strip() or None,
            unique_url,
            request.form.get("requirements", "").strip(),
        ))
        conn.commit()
    finally:
        conn.close()
    return redirect(url_for("admin"))


@app.route("/admin/delete/<int:oid>")
@login_required
def admin_delete(oid):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM opportunities WHERE id = ?", (oid,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin"))


# ═══════ APIs ═══════
@app.route("/api/stats")
def api_stats():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM opportunities")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM opportunities WHERE type = 'emploi'")
    emplois = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM opportunities WHERE type = 'concours'")
    concours = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM opportunities WHERE type = 'formation'")
    formation = c.fetchone()[0]
    conn.close()
    return jsonify({
        "total": total,
        "emploi": emplois,
        "concours": concours,
        "formation": formation,
        "visits": get_visits(),
    })


# ═══════ التشغيل ═══════
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
