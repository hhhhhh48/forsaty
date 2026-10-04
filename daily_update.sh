#!/data/data/com.termux/files/usr/bin/bash
# daily_update.sh - تحديث تلقائي يومياً

cd ~/forsaty

echo "════════════════════════════════════"
echo "🕐 $(date '+%Y-%m-%d %H:%M:%S')"
echo "🚀 بدء التحديث اليومي"
echo "════════════════════════════════════"

# 1. جلب الفرص الجديدة
echo ""
echo "📡 المرحلة 1: جلب الفرص..."
python auto_fetch.py 2>&1 | tail -20

# 2. إحصائيات
echo ""
echo "📊 المرحلة 2: إحصائيات قاعدة البيانات..."
python -c "
import sqlite3
conn = sqlite3.connect('data/forsaty.db')
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM opportunities')
total = c.fetchone()[0]
c.execute('SELECT COUNT(*) FROM opportunities WHERE type=\"emploi\"')
emplois = c.fetchone()[0]
c.execute('SELECT COUNT(*) FROM opportunities WHERE type=\"concours\"')
concours = c.fetchone()[0]
conn.close()
print(f'  📋 المجموع: {total}')
print(f'  💼 وظائف:  {emplois}')
print(f'  📝 مسابقات: {concours}')
"

echo ""
echo "✅ انتهى التحديث — $(date '+%H:%M:%S')"
echo "════════════════════════════════════"
