from pathlib import Path
from datetime import datetime
import shutil
import json

html = Path("app/src/main/assets/index.html")
data = Path("app/src/main/assets/data/prayer_guides.json")

if not html.exists() or not data.exists():
    raise SystemExit("ERROR: اړین فایلونه ونه موندل شول.")

source = html.read_text(encoding="utf-8")
guides = json.loads(data.read_text(encoding="utf-8"))

if 'data-action="prayer-guides"' in source:
    raise SystemExit("لارښود لا مخکې اضافه شوی؛ د تکرار مخنیوی وشو.")

required = [
    "function home(){",
    "function render(){",
    'app.addEventListener("click"',
    "function card("
]
for marker in required:
    if marker not in source:
        raise SystemExit("ERROR: د HTML جوړښت بدل دی: " + marker)

backup_dir = Path("backups")
backup_dir.mkdir(exist_ok=True)
stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = backup_dir / f"index-before-prayer-{stamp}.html"
shutil.copy2(html, backup)

# د لارښودونو JSON د JavaScript لپاره خوندي بڼه
guides_json = json.dumps(guides, ensure_ascii=False).replace("</", "<\\/")

# د لارښود کارتونه او تشریحات
addition = r'''
/* Noor-ul-Islam: Prayer and purification guide */
const PRAYER_GUIDES = __PRAYER_GUIDES_JSON__;

function renderPrayerGuides() {
  app.innerHTML =
    `<button class="back" data-action="home">← بېرته کورپاڼې ته</button>` +
    header("د لمانځه او پاکوالي لارښود", "د حنفي طریقې له مخې د زده کړې کارتونه") +
    `<div class="grid">` +
    PRAYER_GUIDES.map(g =>
      card(g.icon, g.title, (g.steps || []).length + " ګامونه · د لوستلو لپاره کلیک وکړئ", "prayer-topic:" + g.id)
    ).join("") +
    `</div>`;
}

function renderPrayerTopic(id) {
  const g = PRAYER_GUIDES.find(x => x.id === id);
  if (!g) { renderPrayerGuides(); return; }

  let html = `<button class="back" data-action="prayer-guides">← بېرته لارښودونو ته</button>`;
  html += header(g.icon + " " + g.title, "هر ګام په غور ولولئ");

  html += `<div class="grid">` + (g.steps || []).map((s, i) =>
    `<article class="panel" style="border-radius:18px;padding:18px;margin:8px 0">
      <div style="font-size:28px;margin-bottom:8px">${["🟢","💧","📖","🤲","🕌","✨"][i % 6]}</div>
      <h3>${esc(s.title || "")}</h3>
      <p style="line-height:1.9">${esc(s.description || "")}</p>
    </article>`
  ).join("") + `</div>`;

  if (Array.isArray(g.hanafi_fard) && g.hanafi_fard.length) {
    html += header("د حنفي طریقې فرضونه", "د زده کړې لپاره");
    html += `<div class="panel"><ol>` +
      g.hanafi_fard.map(x => `<li style="margin:10px 0;line-height:1.8">${esc(x)}</li>`).join("") +
      `</ol></div>`;
  }

  app.innerHTML = html;
}
'''.replace("__PRAYER_GUIDES_JSON__", guides_json)

# د JavaScript د اصلي پای برخې څخه مخکې فنکشنونه ورزیاتول
script_end = "</script>"
pos = source.rfind(script_end)
if pos < 0:
    raise SystemExit("ERROR: د script پای ونه موندل شو؛ اصلي فایل نه دی بدل شوی.")

source = source[:pos] + addition + "\n" + source[pos:]

# د کورپاڼې کارت ورزیاتول
home_marker = '${card("💬","۵۰۰ اسلامي ویناوې"'
if home_marker not in source:
    raise SystemExit("ERROR: د کورپاڼې د کارت ځای ونه موندل شو؛ اصلي فایل نه دی بدل شوی.")

source = source.replace(
    home_marker,
    '${card("🕌","د لمانځه او پاکوالي لارښود","لمونځ، اوداسه، غسل او تیمم","prayer-guides")}' + home_marker,
    1
)

# د render() دننه د نوو پاڼو ملاتړ
render_marker = 'if (page === "quotes" || page.startsWith("quotes:")'
if render_marker not in source:
    raise SystemExit("ERROR: د render() ځای ونه موندل شو؛ اصلي فایل نه دی بدل شوی.")

source = source.replace(
    render_marker,
    'if (page === "prayer-guides") { renderPrayerGuides(); return; }\n'
    '  if (page.startsWith("prayer-topic:")) { renderPrayerTopic(page.slice(13)); return; }\n'
    + render_marker,
    1
)

# د کلیک سیستم
click_marker = 'const action=b.dataset.action;'
if click_marker not in source:
    raise SystemExit("ERROR: د کلیک سیستم ونه موندل شو؛ اصلي فایل نه دی بدل شوی.")

source = source.replace(
    click_marker,
    click_marker + '''
    if(action==="prayer-guides"){
      page="prayer-guides";selectedSurah=null;selectedLesson=null;
      search.value="";query="";render();window.scrollTo(0,0);return;
    }
    if(action.startsWith("prayer-topic:")){
      page=action;search.value="";query="";render();window.scrollTo(0,0);return;
    }
    ''',
    1
)

# وروستۍ خوندي لیکنه
html.write_text(source, encoding="utf-8")

# د JavaScript نښو تایید
check = html.read_text(encoding="utf-8")
assert 'data-action="prayer-guides"' in check
assert "function renderPrayerGuides()" in check
assert "function renderPrayerTopic(id)" in check
assert "const PRAYER_GUIDES" in check

print("بریالی شو! د لمانځه لارښود اضافه شو.")
print("د لارښودونو شمېر:", len(guides))
print("بیک‌اپ:", backup)
print("اوس د اپلیکیشن build او ازموینه وکړئ.")
