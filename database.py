"""database.py - قاعدة بيانات منصة فرصتي"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "forsaty.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    # المصادر (DGFP, ANEM, Emploitic...)
    c.execute("""
        CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            type TEXT,
            active INTEGER DEFAULT 1
        )
    """)

    # الولايات (58 ولاية)
    c.execute("""
        CREATE TABLE IF NOT EXISTS wilayas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code INTEGER UNIQUE NOT NULL,
            name TEXT NOT NULL
        )
    """)

    # القطاعات (تعليم، صحة، عدل، جمارك...)
    c.execute("""
        CREATE TABLE IF NOT EXISTS sectors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            icon TEXT
        )
    """)

    # الفرص (وظائف + مسابقات + منح)
    c.execute("""
        CREATE TABLE IF NOT EXISTS opportunities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            type TEXT NOT NULL,
            source_id INTEGER,
            sector_id INTEGER,
            wilaya_id INTEGER,
            organization TEXT,
            positions_count INTEGER,
            deadline TEXT,
            start_date TEXT,
            url TEXT UNIQUE NOT NULL,
            requirements TEXT,
            added_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (source_id) REFERENCES sources(id),
            FOREIGN KEY (sector_id) REFERENCES sectors(id),
            FOREIGN KEY (wilaya_id) REFERENCES wilayas(id)
        )
    """)

    # فهرس للبحث السريع
    c.execute("CREATE INDEX IF NOT EXISTS idx_opp_type ON opportunities(type)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_opp_deadline ON opportunities(deadline)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_opp_wilaya ON opportunities(wilaya_id)")

    conn.commit()
    conn.close()
    print("✅ قاعدة البيانات جاهزة")


if __name__ == "__main__":
    os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)
    init_db()
    print("🎯 forsaty.db جاهز")
