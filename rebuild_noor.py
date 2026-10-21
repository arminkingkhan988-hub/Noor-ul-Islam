import json
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(".")
ASSETS = ROOT / "app/src/main/assets"
DATA = ASSETS / "data"
HTML_FILE = ASSETS / "index.html"
QURAN_FILE = DATA / "quran.json"
ISLAMIC_FILE = DATA / "islamic.json"

if not QURAN_FILE.exists() or not ISLAMIC_FILE.exists():
    raise SystemExit("خطا: د قرآن یا اسلامي درسونو فایل ونه موندل شو.")

quran = json.loads(QURAN_FILE.read_text(encoding="utf-8"))
lessons = json.loads(ISLAMIC_FILE.read_text(encoding="utf-8"))

if len(quran) != 114:
    raise SystemExit("قرآن کې ۱۱۴ سورتونه ونه موندل شول؛ فایل نه بدلېږي.")

if len(lessons) > 100:
    raise SystemExit("له ۱۰۰ څخه زیات درسونه موجود دي؛ فایل نه بدلېږي.")

# د نوي ډیزاین له پیل مخکې بیک‌اپ
backup_dir = ROOT / "backups" / datetime.now().strftime("redesign_%Y%m%d_%H%M%S")
backup_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(HTML_FILE, backup_dir / "index.html")
shutil.copy2(QURAN_FILE, backup_dir / "quran.json")
shutil.copy2(ISLAMIC_FILE, backup_dir / "islamic.json")

# ۵۰ اضافي اسلامي موضوعات
extra_topics = [
    ("د اسلام پنځه بناوې", "د اسلام پنځه بنسټونه او د هر یوه اهمیت زده کړه."),
    ("د ایمان شپږ ارکان", "پر الله، ملایکو، کتابونو، رسولانو، آخرت او تقدیر ایمان."),
    ("د الله ښکلي نومونه", "د الله د ښکلو نومونو معناوې او د دعا په وخت کې یې کارول."),
    ("د توحید پېژندنه", "د الله یووالی او د عبادت د خالص کولو اهمیت."),
    ("اخلاص په عبادت کې", "عبادت یوازې د الله د رضا لپاره ترسره کول."),
    ("توبه او استغفار", "له ګناه څخه لاس اخیستل، پښېماني او د اصلاح هڅه."),
    ("د قرآن کریم آداب", "د قرآن تلاوت، اورېدو او درناوي آداب."),
    ("د قرآن د تلاوت فضیلت", "د قرآن د زده کړې، تلاوت او عمل ارزښت."),
    ("د تجوید پېژندنه", "د قرآن د تورو د سم ادا کولو بنسټیز اصول."),
    ("د لمانځه اهمیت", "په اسلام کې د لمانځه مقام او د وخت پابندي."),
    ("د جماعت لمونځ", "د جماعت د لمانځه اهمیت او د جماعت آداب."),
    ("د جمعې لمونځ", "د جمعې د ورځې فضیلت او د جمعې د لمانځه عمومي احکام."),
    ("د اختر لمونځ", "د کوچني او لوی اختر د لمانځه پېژندنه."),
    ("د جنازې لمونځ", "د جنازې د لمانځه اهمیت او عمومي طریقه."),
    ("د مسافر لمونځ", "د سفر د لمانځه په اړه عمومي معلومات."),
    ("د سجدې آداب", "په سجده کې عاجزي او د لمانځه د ارکانو درناوی."),
    ("د اذان او اقامت احکام", "د اذان او اقامت اهمیت او د اورېدو آداب."),
    ("د جمعې د ورځې آداب", "غسل، پاکوالی، وختي تګ او د خطبې اورېدل."),
    ("د روژې حکمتونه", "د روژې روحاني، اخلاقي او ټولنیز درسونه."),
    ("د روژې ماتولو آداب", "د افطار وخت، دعا او د نعمتونو شکر."),
    ("د سحري اهمیت", "د سحري فضیلت او د روژې لپاره مناسب چمتووالی."),
    ("د اعتکاف پېژندنه", "د اعتکاف معنا او د دې عبادت عمومي شرایط."),
    ("د زکات حکمتونه", "د مال پاکوالی، د اړمنو مرسته او ټولنیز مسؤلیت."),
    ("صدقه او خیرات", "د مرستې ډولونه او د صدقې اخلاق."),
    ("د حج موخې", "د حج روحاني پیغام او د مسلمانانو یووالی."),
    ("د عمرې پېژندنه", "د عمرې بنسټیز مناسک او د زده کړې اړتیا."),
    ("د مور او پلار حقونه", "له مور او پلار سره نېکي او ښه چلند."),
    ("د خپلوانو پالنه", "صله رحمي او د کورنۍ اړیکو ساتل."),
    ("د ګاونډي حقونه", "له ګاونډیانو سره مرسته او ښه ګاونډیتوب."),
    ("د یتیمانو پالنه", "د یتیمانو درناوی، مرسته او د هغوی حقونه."),
    ("د غریبانو مرسته", "له اړمنو سره مرسته او د ټولنې مسؤلیت."),
    ("رښتینولي", "په خبرو او کړنو کې رښتیا ویل."),
    ("امانتداري", "د خلکو د امانتونو ساتل او د ژمنو پوره کول."),
    ("عدالت او انصاف", "له ټولو خلکو سره عادلانه چلند."),
    ("بخښنه او زغم", "د نورو تېروتنې بښل او له غوسې ځان ساتل."),
    ("تواضع او عاجزي", "له تکبر څخه ځان ساتل او د خلکو درناوی."),
    ("د ژبې ساتنه", "له دروغو، غیبت او سپکو خبرو ځان ساتل."),
    ("غیبت او بهتان", "د غیبت او بهتان زیانونه او د ځان ساتنې لارې."),
    ("د حسد زیانونه", "له حسد څخه ځان ساتل او د نورو لپاره خیر غوښتل."),
    ("د وخت ارزښت", "د وخت تنظیم او د ګټورو کارونو عادت."),
    ("د علم فضیلت", "د ګټور علم زده کړه او پر علم عمل کول."),
    ("د استاد حقونه", "د ښوونکي درناوی او د زده کړې آداب."),
    ("د زده کوونکي آداب", "د علم په لټه کې صبر، نظم او درناوی."),
    ("د ماشومانو اسلامي روزنه", "له ماشومانو سره مینه او د ښو اخلاقو روزنه."),
    ("د مېلمه پالنې آداب", "د مېلمه درناوی او د کوربه مسؤلیتونه."),
    ("د خوراک آداب", "د خوراک مخکې او وروسته آداب او د نعمت شکر."),
    ("د څښاک آداب", "د څښاک مناسب آداب او د پاکوالي رعایت."),
    ("د خوب آداب", "د خوب لپاره پاکوالی، دعا او مناسب عادتونه."),
    ("د سفر آداب", "د سفر چمتووالی، د ملګرو حقونه او خوندیتوب."),
    ("د دعا آداب", "د دعا پر مهال اخلاص، عاجزي او د الله څخه غوښتنه."),
]

def make_section(title, body):
    return {
        "heading": title,
        "body": body
    }

existing_ids = {str(x.get("id", "")) for x in lessons}

for i, (title, description) in enumerate(extra_topics, start=1):
    lesson_id = f"additional_{i:02d}"
    if lesson_id in existing_ids:
        continue

    lessons.append({
        "id": lesson_id,
        "title": title,
        "sections": [
            make_section("د موضوع پېژندنه", description),
            make_section(
                "د زده کړې موخه",
                "دا درس د موضوع د بنسټیزو مفاهیمو د زده کړې لپاره دی. "
                "موضوع په غور ولولئ، مهم ټکي یاد کړئ او په ورځني ژوند کې "
                "د ښو اخلاقو او ګټور عمل هڅه وکړئ."
            ),
            make_section(
                "مهمه یادونه",
                "د ځانګړو شرعي احکامو، اختلاف لرونکو مسئلو او عملي فتواوو "
                "لپاره له باوري علماوو او معتبره اسلامي سرچینو څخه پوښتنه وکړئ."
            )
        ]
    })

if len(lessons) < 100:
    raise SystemExit(
        f"د درسونو شمېر {len(lessons)} شو، ۱۰۰ ته ونه رسېد؛ "
        "اصلي فایلونه خوندي دي."
    )

lessons = lessons[:100]

# درسونه په JSON کې خوندي کول
ISLAMIC_FILE.write_text(
    json.dumps(lessons, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

quran_json = json.dumps(quran, ensure_ascii=False, separators=(",", ":"))
lessons_json = json.dumps(lessons, ensure_ascii=False, separators=(",", ":"))

html = r'''<!doctype html>
<html lang="ps" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<meta name="theme-color" content="#075b45">
<title>نورالاسلام | Noor-ul-Islam</title>
<style>
:root{
 --green:#075b45;--green2:#0d7658;--gold:#d9b45b;
 --bg:#f3f7f3;--card:#fff;--ink:#18372c;--muted:#6b7d73;
 --line:#e2ebe4;--shadow:0 5px 20px #123b2510
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
 font-family:Arial,"Noto Naskh Arabic",sans-serif;line-height:1.8}
button,input{font:inherit}
button{cursor:pointer}
.hero{background:linear-gradient(135deg,#043d30,#0d7658);
 color:white;padding:25px 18px 30px;border-radius:0 0 28px 28px;
 position:relative;overflow:hidden}
.hero:after{content:"☪";position:absolute;left:12px;top:-25px;
 font-size:120px;color:#ffffff12}
.topline{display:flex;justify-content:space-between;align-items:center;gap:12px}
.brand{font-size:23px;font-weight:900}
.badge{font-size:12px;background:#ffffff1a;border:1px solid #ffffff40;
 padding:4px 10px;border-radius:20px}
.hero h1{font-size:25px;margin:20px 0 3px}
.hero p{margin:0;color:#e2f3e9;font-size:14px}
.search-wrap{padding:0 16px;margin-top:-19px;position:relative}
.search{width:100%;padding:14px 17px;border:1px solid var(--line);
 border-radius:15px;background:white;outline:none;box-shadow:var(--shadow)}
.tabs{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;
 padding:15px 12px 5px}
.tab{border:1px solid var(--line);border-radius:12px;background:white;
 color:var(--green);padding:9px 3px;font-size:13px;font-weight:bold}
.tab.active{background:var(--green);color:white;border-color:var(--green)}
main{padding:12px 14px 90px;max-width:900px;margin:auto}
.section-head{display:flex;align-items:center;justify-content:space-between;
 gap:8px;margin:14px 2px 10px}
.section-head h2{font-size:20px;margin:0}
.small{font-size:12px;color:var(--muted)}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:11px}
.card{background:var(--card);border:1px solid var(--line);border-radius:17px;
 padding:15px;text-align:right;box-shadow:var(--shadow);min-width:0}
.card:active{transform:scale(.99)}
.icon{width:43px;height:43px;display:grid;place-items:center;
 border-radius:14px;background:#eaf5ee;font-size:23px;margin-bottom:8px}
.card h3{font-size:15px;margin:3px 0 5px;line-height:1.6}
.card p{font-size:12px;color:var(--muted);margin:0}
.pill{display:inline-block;font-size:11px;padding:2px 8px;border-radius:20px;
 background:#f4ecd5;color:#76591d;margin-top:8px}
.panel{background:white;border:1px solid var(--line);border-radius:18px;
 padding:16px;margin:12px 0;box-shadow:var(--shadow)}
.back{border:0;background:#e5f1e9;color:var(--green);padding:8px 14px;
 border-radius:10px;font-weight:bold;margin-bottom:12px}
.verse{padding:18px 5px;border-bottom:1px solid var(--line)}
.verse:last-child{border:0}
.arabic{font-size:25px;line-height:2.2;text-align:justify;color:#173f30}
.pashto{font-size:15px;color:#53675b;margin-top:8px}
.verse-tools{display:flex;align-items:center;justify-content:space-between;
 margin-top:9px;gap:8px}
.verse-number{color:var(--green);font-weight:bold;font-size:12px}
.mini{border:1px solid var(--line);background:#f8fbf8;
 border-radius:9px;padding:5px 9px;color:var(--green);font-size:12px}
.lesson-section{padding:10px 0;border-bottom:1px solid var(--line)}
.lesson-section:last-child{border:0}
.lesson-section h3{color:var(--green);font-size:16px}
.empty{text-align:center;color:var(--muted);padding:30px 10px}
footer{text-align:center;padding:20px;color:var(--muted);font-size:12px}
.bottom{position:fixed;bottom:0;left:0;right:0;background:#ffffffed;
 border-top:1px solid var(--line);padding:9px 16px;
 text-align:center;font-size:12px;color:var(--muted);backdrop-filter:blur(8px)}
.hidden{display:none!important}
@media(min-width:600px){.grid{grid-template-columns:repeat(3,minmax(0,1fr))}
 .hero{padding-left:max(22px,calc((100% - 860px)/2));padding-right:max(22px,calc((100% - 860px)/2))}}
</style>
</head>
<body>
<header class="hero">
 <div class="topline"><div class="brand">☪ نورالاسلام</div>
 <span class="badge">وړیا · بې اعلاناتو · آفلاین</span></div>
 <h1 id="heroTitle">د اسلام د زده کړې ښکلی سفر</h1>
 <p id="heroSub">قرآن کریم، اسلامي درسونه او ګټور معلومات</p>
</header>
<div class="search-wrap">
 <input id="search" class="search" placeholder="🔎 قرآن، سورت یا اسلامي درس ولټوئ..." autocomplete="off">
</div>
<nav class="tabs">
 <button class="tab active" data-page="home">کورپاڼه</button>
 <button class="tab" data-page="quran">قرآن کریم</button>
 <button class="tab" data-page="lessons">درسونه</button>
 <button class="tab" data-page="saved">خوندي شوي</button>
</nav>
<main id="app"></main>
<div class="bottom">نورالاسلام · د زده کړې لپاره · وړیا او بې اعلاناتو</div>

<script id="quran-data" type="application/json">__QURAN_DATA__</script>
<script id="lesson-data" type="application/json">__LESSON_DATA__</script>
<script>
"use strict";
const QURAN=JSON.parse(document.getElementById("quran-data").textContent);
const LESSONS=JSON.parse(document.getElementById("lesson-data").textContent);
const app=document.getElementById("app");
const search=document.getElementById("search");
let page="home", query="", selectedSurah=null, selectedLesson=null;
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function readSaved(){try{return JSON.parse(localStorage.getItem("noorSavedV2")||"[]")}catch(e){return []}}
function saveSaved(a){localStorage.setItem("noorSavedV2",JSON.stringify(a))}
function isSaved(id){return readSaved().includes(String(id))}
function toggleSaved(id){
 id=String(id);let a=readSaved();
 a=a.includes(id)?a.filter(x=>x!==id):[...a,id];
 saveSaved(a);render();
}
function surahName(s){return s.name||s.englishName||("سورت "+s.sura)}
function surahNumber(s,i){return Number(s.sura||s.number||i+1)}
function versesOf(s){return s.verses||s.ayahs||[]}
function lessonTitle(l){return l.title||l.ps||l.name||l.id||"اسلامي درس"}
function lessonSections(l){
 if(Array.isArray(l.sections)) return l.sections;
 if(Array.isArray(l.body)) return l.body;
 if(typeof l.body==="string") return [{heading:"تشریح",body:l.body}];
 return [];
}
function sectionHeading(s){return s.heading||s.title||s.name||"تشریح"}
function sectionBody(s){return s.body||s.text||s.content||""}
function totalVerses(){return QURAN.reduce((n,s)=>n+versesOf(s).length,0)}
function header(title,sub=""){
 return `<div class="section-head"><div><h2>${esc(title)}</h2><div class="small">${esc(sub)}</div></div></div>`;
}
function card(icon,title,desc,action,tag=""){
 return `<button class="card" data-action="${esc(action)}"><div class="icon">${icon}</div>
 <h3>${esc(title)}</h3><p>${esc(desc)}</p>${tag?`<span class="pill">${esc(tag)}</span>`:""}</button>`;
}
function home(){
 const q=totalVerses();
 app.innerHTML=`
 ${header("السلام علیکم","د علم او نېکو عملونو سفر پیل کړئ")}
 <div class="grid">
 ${card("📖","قرآن کریم","۱۱۴ سورتونه · ${q} آیتونه","quran")}
 ${card("🕌","اسلامي درسونه","۱۰۰ موضوعات د زده کړې لپاره","lessons")}
 ${card("🔖","خوندي شوي","خپل خوښ آیتونه او درسونه وګورئ","saved")}
 ${card("🌿","د اپ په اړه","وړیا، بې اعلاناتو او آفلاین","about")}
 </div>
 ${header("د قرآن کریم سورتونه","د لوستلو لپاره سورت وټاکئ")}
 <div class="grid">${QURAN.slice(0,6).map((s,i)=>card("📜",surahName(s),
 "سورت "+surahNumber(s,i)+" · "+versesOf(s).length+" آیتونه","surah:"+surahNumber(s,i))).join("")}</div>
 ${header("د اسلامي درسونو بېلګې","د موضوع د لوستلو لپاره کارت وټاکئ")}
 <div class="grid">${LESSONS.slice(0,6).map((l,i)=>card("🕌",lessonTitle(l),"اسلامي زده کړه","lesson:"+i)).join("")}</div>`;
}
function renderQuran(){
 let list=QURAN.map((s,i)=>({s,i})).filter(({s,i})=>{
  if(!query)return true;
  const q=query.toLowerCase();
  return surahName(s).toLowerCase().includes(q)||
   ("سورت "+surahNumber(s,i)).includes(q)||
   versesOf(s).some(v=>(v.arabic||"").includes(query)||(v.pashto||"").includes(query));
 });
 app.innerHTML=header("قرآن کریم","عربي متن او پښتو ژباړه · آفلاین")+
 `<div class="grid">${list.map(({s,i})=>card("📖",surahName(s),
 "سورت "+surahNumber(s,i)+" · "+versesOf(s).length+" آیتونه","surah:"+surahNumber(s,i))).join("")}</div>`+
 (list.length?"":'<div class="empty">پایله ونه موندل شوه.</div>');
}
function renderSurah(num){
 const idx=QURAN.findIndex((s,i)=>surahNumber(s,i)===Number(num));
 if(idx<0){renderQuran();return}
 const s=QURAN[idx], verses=versesOf(s);
 let filtered=verses.map((v,i)=>({v,i})).filter(({v})=>
  !query||(v.arabic||"").includes(query)||(v.pashto||"").includes(query));
 app.innerHTML=`<button class="back" data-action="quran">← د سورتونو لېست</button>
 <div class="panel"><h2>${esc(surahName(s))}</h2>
 <p class="small">سورت ${surahNumber(s,idx)} · ${verses.length} آیتونه</p>
 <p>د قرآن کریم تلاوت په غور ولولئ او د ژباړې معنا ته پام وکړئ.</p></div>
 <div class="panel">${filtered.map(({v,i})=>{
  const id="v:"+surahNumber(s,idx)+":"+String(v.aya??i+1);
  return `<div class="verse"><div class="arabic">${esc(v.arabic||"")}</div>
  <div class="pashto">${esc(v.pashto||"ژباړه نشته")}</div>
  <div class="verse-tools"><span class="verse-number">آیت ${esc(v.aya??i+1)}</span>
  <button class="mini" data-action="save:${esc(id)}">${isSaved(id)?"★ خوندي دی":"☆ خوندي کول"}</button></div></div>`;
 }).join("")}</div>`+(filtered.length?"":'<div class="empty">آیت ونه موندل شو.</div>');
}
function renderLessons(){
 const list=LESSONS.map((l,i)=>({l,i})).filter(({l})=>{
  if(!query)return true;
  const q=query.toLowerCase();
  return lessonTitle(l).toLowerCase().includes(q)||
   lessonSections(l).some(s=>(sectionHeading(s)+" "+sectionBody(s)).toLowerCase().includes(q));
 });
 app.innerHTML=header("۱۰۰ اسلامي درسونه","هر کارت د یوې موضوع د زده کړې لپاره")+
 `<div class="grid">${list.map(({l,i})=>card("🕌",lessonTitle(l),
 lessonSections(l).length+" برخې · د لوستلو لپاره کلیک وکړئ","lesson:"+i,
 "درس "+(i+1))).join("")}</div>`+
 (list.length?"":'<div class="empty">درس ونه موندل شو.</div>');
}
function renderLesson(i){
 const l=LESSONS[Number(i)];if(!l){renderLessons();return}
 const id="l:"+String(l.id??i);
 app.innerHTML=`<button class="back" data-action="lessons">← د درسونو لېست</button>
 <div class="panel"><div class="icon">🕌</div><h2>${esc(lessonTitle(l))}</h2>
 <p class="small">اسلامي درس · ${Number(i)+1} له ${LESSONS.length}</p>
 <button class="mini" data-action="save:${esc(id)}">${isSaved(id)?"★ خوندي دی":"☆ درس خوندي کول"}</button></div>
 <div class="panel">${lessonSections(l).map(s=>`<section class="lesson-section">
 <h3>${esc(sectionHeading(s))}</h3><div>${esc(sectionBody(s))}</div></section>`).join("")}
 ${lessonSections(l).length?"":'<p>د دې درس تفصیلي معلومات لا نه دي داخل شوي.</p>'}</div>`;
}
function renderSaved(){
 const saved=readSaved();
 const verses=[], lessons=[];
 saved.forEach(id=>{
  if(id.startsWith("v:")) verses.push(id);
  else if(id.startsWith("l:")) lessons.push(id);
 });
 app.innerHTML=header("خوندي شوي","ستاسې خوښې آیتونه او درسونه")+
 `<div class="panel"><h3>📖 خوندي شوي آیتونه</h3>
 ${verses.length?verses.map(id=>{
  const [,sn,an]=id.split(":");
  const s=QURAN.find((x,i)=>surahNumber(x,i)===Number(sn));
  const v=s&&versesOf(s).find((x,i)=>String(x.aya??i+1)===an);
  return v?`<div class="verse"><div class="arabic">${esc(v.arabic)}</div>
  <div class="pashto">${esc(v.pashto)}</div>
  <div class="verse-tools"><span>${esc(surahName(s))} · آیت ${esc(an)}</span>
  <button class="mini" data-action="save:${esc(id)}">لرې کول</button></div></div>`:"";
 }).join(""):'<p class="small">تر اوسه آیت نه دی خوندي شوی.</p>'}</div>
 <div class="panel"><h3>🕌 خوندي شوي درسونه</h3>
 ${lessons.length?lessons.map(id=>{
  const l=LESSONS.find((x,i)=>"l:"+String(x.id??i)===id);
  return l?`<div class="verse"><b>${esc(lessonTitle(l))}</b>
  <button class="mini" data-action="save:${esc(id)}">لرې کول</button></div>`:"";
 }).join(""):'<p class="small">تر اوسه درس نه دی خوندي شوی.</p>'}</div>`;
}
function about(){
 app.innerHTML=`<div class="panel"><div class="icon">☪</div><h2>نورالاسلام</h2>
 <p>د قرآن کریم او اسلامي زده کړو لپاره وړیا اپلیکیشن.</p>
 <p>قرآن: ${QURAN.length} سورتونه، ${totalVerses()} آیتونه.</p>
 <p>اسلامي درسونه: ${LESSONS.length}.</p>
 <p>قرآن او درسونه په اپ کې ځای پر ځای شوي؛ د لوستلو لپاره انټرنېټ ته اړتیا نشته.</p>
 <p class="small">د شرعي مسئلو لپاره له باوري علماوو سره مشوره وکړئ.</p></div>`;
}
function render(){
 document.querySelectorAll(".tab").forEach(b=>b.classList.toggle("active",b.dataset.page===page));
 if(page==="home")home();
 else if(page==="quran"){if(selectedSurah)renderSurah(selectedSurah);else renderQuran()}
 else if(page==="lessons"){if(selectedLesson!==null)renderLesson(selectedLesson);else renderLessons()}
 else if(page==="saved")renderSaved();
 else if(page==="about")about();
}
document.querySelectorAll(".tab").forEach(b=>b.addEventListener("click",()=>{
 page=b.dataset.page;selectedSurah=null;selectedLesson=null;query="";search.value="";render();
}));
search.addEventListener("input",()=>{
 query=search.value.trim();
 if(page==="home"){page="lessons";selectedLesson=null;selectedSurah=null}
 render();
});
app.addEventListener("click",e=>{
 const b=e.target.closest("[data-action]");if(!b)return;
 const action=b.dataset.action;
 if(action==="quran"){page="quran";selectedSurah=null;selectedLesson=null}
 else if(action==="lessons"){page="lessons";selectedLesson=null;selectedSurah=null}
 else if(action==="saved"){page="saved";selectedLesson=null;selectedSurah=null}
 else if(action==="about"){page="about";selectedLesson=null;selectedSurah=null}
 else if(action.startsWith("surah:")){page="quran";selectedSurah=action.split(":")[1];selectedLesson=null}
 else if(action.startsWith("lesson:")){page="lessons";selectedLesson=action.split(":")[1];selectedSurah=null}
 else if(action.startsWith("save:")){toggleSaved(action.slice(5));return}
 search.value="";query="";render();window.scrollTo(0,0);
});
render();
</script>
</body>
</html>'''

html = html.replace("__QURAN_DATA__", quran_json)
html = html.replace("__LESSON_DATA__", lessons_json)
HTML_FILE.write_text(html, encoding="utf-8")

print("\n" + "="*48)
print("✅ د Noor-ul-Islam نوی ډیزاین جوړ شو!")
print("قرآن کریم:", len(quran), "سورتونه")
print("د قرآن آیتونه:", sum(len(s.get("verses", [])) for s in quran))
print("اسلامي درسونه:", len(lessons))
print("HTML اندازه: %.2f MB" % (HTML_FILE.stat().st_size / 1048576))
print("بیک‌اپ:", backup_dir)
print("="*48)
print("یادونه: د Android APK د جوړولو لپاره GitHub Actions وکاروه.")
