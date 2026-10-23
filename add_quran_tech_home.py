from pathlib import Path
from datetime import datetime
import re
import sys

p = Path("app/src/main/assets/index.html")
html = p.read_text(encoding="utf-8")

backup = p.with_name(
    "index.html.before-home-card-" +
    datetime.now().strftime("%Y%m%d-%H%M%S") + ".bak"
)
backup.write_text(html, encoding="utf-8")

marker = '${card("🕌","د لمانځه او پاکوالي لارښود"'
card = '${card("🔬","قرآن کریم او ټکنالوژي","۱۰۰ درسونه · قرآني کیسې، علمي الهامونه او مصنوعي ځیرکتیا","quran-inspiration","۱۰۰ درسونه")}'

if "قرآن کریم او ټکنالوژي" in html:
    print("د قرآن کریم او ټکنالوژۍ کارت له مخکې موجود دی.")
elif marker in html:
    html = html.replace(marker, card + "\n      " + marker, 1)
    p.write_text(html, encoding="utf-8")
    print("بریالیتوب: کارت د کور پاڼې ته اضافه شو.")
else:
    print("خطا: د کور پاڼې د کارت ځای ونه موندل شو.")
    print("بیک‌اپ:", backup)
    sys.exit(1)

print("د کارت شمېر:", html.count("قرآن کریم او ټکنالوژي"))
print("بیک‌اپ:", backup)
