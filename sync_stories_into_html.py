import json
import re
import shutil
from pathlib import Path
from datetime import datetime

html_path = Path("app/src/main/assets/index.html")
json_path = Path("app/src/main/assets/data/stories.json")

if not html_path.exists() or not json_path.exists():
    raise SystemExit("خطا: اړین فایلونه پیدا نه شول.")

html = html_path.read_text(encoding="utf-8")
stories = json.loads(json_path.read_text(encoding="utf-8"))

if len(stories) != 100:
    raise SystemExit(f"تم شو: ۱۰۰ کیسې تمه کېدې، خو {len(stories)} پیدا شوې.")

for i, story in enumerate(stories, 1):
    if not story.get("title") or len(story.get("text", "").split()) < 500:
        raise SystemExit(
            f"تم شو: د {i}مې کیسې سرلیک یا اوږد متن سم نه دی."
        )

pattern = re.compile(
    r'(<script\b[^>]*\bid=["\']stories-data["\'][^>]*>).*?(</script>)',
    re.S | re.I
)

if not pattern.search(html):
    raise SystemExit(
        "خطا: په HTML کې stories-data برخه پیدا نه شوه؛ "
        "فایل مو نه دی بدل کړی."
    )

backup = html_path.with_name(
    "index.html.before-full-stories-" +
    datetime.now().strftime("%Y%m%d_%H%M%S") + ".bak"
)
shutil.copy2(html_path, backup)

embedded_json = json.dumps(
    stories, ensure_ascii=False, separators=(",", ":")
)

updated_html = pattern.sub(
    lambda m: m.group(1) + embedded_json + m.group(2),
    html,
    count=1
)

if updated_html == html:
    raise SystemExit("بدلون ونه شو؛ اصلي فایل مو نه دی بدل کړی.")

html_path.write_text(updated_html, encoding="utf-8")

# د HTML دننه د کیسو معلومات بېرته ولوله او تایید یې کړه.
check = pattern.search(updated_html)
embedded_stories = json.loads(check.group(0).split(">", 1)[1].rsplit("</script>", 1)[0])

if len(embedded_stories) != 100:
    shutil.copy2(backup, html_path)
    raise SystemExit("تایید ناکام شو؛ بیک‌اپ بېرته راوګرځول شو.")

short = [
    s.get("title", "?")
    for s in embedded_stories
    if len(s.get("text", "").split()) < 500
]

if short:
    shutil.copy2(backup, html_path)
    raise SystemExit(f"تایید ناکام شو؛ لنډې کیسې: {short}")

print("بریالیتوب! ✅")
print("په HTML کې د کیسو شمېر:", len(embedded_stories))
print("له ۵۰۰ کلمو کمې کیسې:", len(short))
print("د لومړۍ کیسې کلمې:", len(embedded_stories[0]["text"].split()))
print("د وروستۍ کیسې کلمې:", len(embedded_stories[-1]["text"].split()))
print("بیک‌اپ:", backup)
print("اوس د index.html نوې نسخه د بشپړو کیسو متنونه لري.")
