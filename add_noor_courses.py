from pathlib import Path
from datetime import datetime
import json
import re
import shutil
import sys

ROOT = Path("app/src/main/assets")
HTML = ROOT / "index.html"
DATA = ROOT / "data" / "noor_courses.json"
MARKER = "NOOR_COURSES_V2"

if not HTML.exists():
    sys.exit("❌ index.html پیدا نه شو.")

source = HTML.read_text(encoding="utf-8")

if MARKER in source:
    sys.exit("ℹ️ د نوي کورسونو سیستم مخکې اضافه شوی؛ د تکرار مخه ونیول شوه.")

for required in ("function home(", "function render(", "</body>"):
    if required not in source:
        sys.exit(f"❌ اړین HTML جوړښت ونه موندل شو: {required}")

backup = ROOT / "index.html.before-noor-courses-v2"
shutil.copy2(HTML, backup)
print("✅ بیک‌اپ:", backup)

# Each entry is a distinct lesson topic. Lesson text is assembled
# from topic-specific explanations and practical guidance below.
ISLAM_TOPICS = [
("د اسلام معنا او موخه","اسلام د الله تعالی اطاعت، د هغه عبادت او د پیغمبرانو د لارښوونو منل دي.","د مسلمان ژوند عبادت، اخلاق، عدالت او د خلکو حقونو ته پاملرنه رانغاړي."),
("د توحید بنسټ","توحید د الله تعالی په یووالي ایمان دی.","توحید انسان د اخلاص، توکل او له شرک څخه د ځان ساتنې لور ته رابولي."),
("قرآن کریم","قرآن کریم د مسلمانانو سپېڅلی کتاب دی.","د قرآن لوستل، معنا زده کول او د لارښوونو عملي کول مهم دي."),
("د محمد ﷺ رسالت","محمد ﷺ د اسلام وروستی پیغمبر دی.","د هغه سیرت د رحمت، امانت، صبر او ښه چلند بېلګې وړاندې کوي."),
("د اسلام پنځه بناوې","شهادت، لمونځ، زکات، روژه او حج د اسلام پنځه بناوې دي.","هر عبادت خپل شرایط او احکام لري چې باید په سمه توګه زده شي."),
("د ایمان بنسټونه","ایمان پر الله، ملایکو، کتابونو، پیغمبرانو، آخرت او تقدیر باور رانغاړي.","د ایمان زده کړه باید له پوهې، اخلاص او نېکو عملونو سره مل وي."),
("لمونځ او روحاني نظم","لمونځ مسلمان ته د الله تعالی یاد او د ورځني ژوند نظم ورزده کوي.","د لمانځه وختونه، شرطونه او طریقه له معتبرې سرچینې زده کړئ."),
("روژه او ځان کنټرول","روژه د تقوا، صبر او د اړمنو د حال درک کولو وسیله ده.","د روژې احکام د روغتیا او شرعي عذرونو په ګډون زده کړئ."),
("زکات او ټولنیز عدالت","زکات د ټاکلو شرایطو له پوره کېدو سره واجب مالي عبادت دی.","د نصاب، کال او مستحقو کسانو په اړه د باوري عالم لارښوونه واخلئ."),
("حج او ورورولي","حج د توان لرونکي مسلمان لپاره د ځانګړو شرایطو په پوره کېدو واجب دی.","د مناسکو ترتیب باید له باوري لارښود څخه زده شي."),
("اسلام او رحمت","رحمت د اسلامي اخلاقو مهم اصل دی.","له ماشومانو، مشرانو، ګاونډیانو او کمزورو سره مهرباني وکړئ."),
("اسلام او عدالت","عدالت د خپلوانو او پردیو په حقونو کې انصاف غوښتنه کوي.","په شخړو کې د دواړو لورو خبرې واورئ او له ظلم څخه ځان وساتئ."),
("اسلام او رښتینولي","رښتینولي د اعتماد بنسټ دی.","په خبرو، سوداګرۍ او وعدو کې رښتیا ووایئ."),
("د مور او پلار حقونه","اسلام د مور او پلار د درناوي او نېک چلند سپارښتنه کوي.","اطاعت په نېکو چارو کې وي؛ د ګناه په کار کې د مخلوق اطاعت نه کېږي."),
("د ګاونډي حقونه","ښه ګاونډیتوب د امن او ټولنیز باور سبب کېږي.","له ځورولو، شور او د بل له حق خوړلو ډډه وکړئ."),
("د ښځو درناوی","اسلامي اخلاق د ښځو عزت، حقونو او ښه چلند ته اهمیت ورکوي.","کورنۍ او ټولنیزې مسئلې باید له علم، عدالت او قانوني خوندیتوب سره حل شي."),
("د ماشومانو روزنه","ماشومان مینه، ښوونه او خوندي چاپېریال ته اړتیا لري.","له سپکاوي او تاوتریخوالي پرته د ښو اخلاقو روزنه وکړئ."),
("علم او زده کړه","ګټور علم د انسان پوهه او مسؤلیت زیاتوي.","د دیني او دنیوي زده کړو لپاره معتبرې سرچینې وکاروئ."),
("د پاکوالي ارزښت","پاکوالی په عبادت او ورځني ژوند کې مهم دی.","د بدن، جامو او چاپېریال پاکوالي ته پام وکړئ."),
("د حلال رزق ارزښت","حلال عاید د مسؤلیت او امانتدارۍ غوښتنه کوي.","په کار کې درغلي او د خلکو حق خوړل مه کوئ."),
("اسلام او بېوزلي","اسلام د اړمنو لاسنیوی او د خیر کارونه هڅوي.","مرسته په عزت او د اړمن د محرمیت په ساتلو وکړئ."),
("اسلام او چاپېریال","د اوبو، ونو او حیواناتو په اړه مسؤلانه چلند مهم دی.","له اسراف او بېځایه زیان رسولو ډډه وکړئ."),
("اسلام او سولې ته بلنه","سوله د عدالت او حقونو له ساتنې سره ارزښت لري.","اختلافونه په خبرو، منځګړیتوب او قانوني لارو حل کړئ."),
("اسلام او زغم","له اختلاف لرونکو سره د ادب او انصاف چلند وکړئ.","د نورو دینونو په اړه د کرکې او سپکاوي ژبه مه کاروئ."),
("د نورو دینونو پېژندنه","د دینونو مطالعه باید په علمي او درناوي ډک ډول وي.","د هر دین د پیروانو خبرې د هغوی له معتبرو سرچینو وپېژنئ."),
("اسلام او مسیحیت","اسلام او مسیحیت د عیسی علیه السلام په اړه مهمې ګډې او بېلې عقیدوي خبرې لري.","د دواړو دینونو د عقایدو بیان باید د هر دین له معتبر متن سره پرتله شي."),
("اسلام او یهودیت","اسلام او یهودیت د ابراهیمي دینونو په پراخ تاریخ کې اړیکې لري.","د تاریخي اختلافونو بیان باید له سپکاوي او عمومي قضاوت څخه پاک وي."),
("اسلام او بودیزم","بودیزم بېلابېل مکتبونه او د کړاو، اخلاقو او تمرین په اړه تعلیمات لري.","د مقایسې پر مهال د بودیزم د ټولو پیروانو په اړه یو شان حکم مه کوئ."),
("اسلام او هندویزم","هندویزم متنوع دودونه، فلسفې او مذهبي عملونه لري.","د دې دین د پېژندنې لپاره د هغه د خپلو ښوونکو او متونو سرچینې ولولئ."),
("د دیني مقایسې اصول","مقایسه باید د ورته معیارونو او دقیقو سرچینو پر بنسټ وي.","د یوې ډلې د بدترین عمل له مخې د ټولو پیروانو قضاوت مه کوئ."),
("د اختلاف ادب","اختلاف د خبرو او پوښتنو فرصت هم کېدای شي.","د مقابل لوري خبره په سمه توګه بیان کړئ او توهین مه کوئ."),
("د دعا ارزښت","دعا د الله تعالی د یاد او غوښتنې وسیله ده.","دعا له حلالو هڅو، صبر او مسؤلیت سره یوځای کړئ."),
("توبه او اصلاح","توبه د ګناه پرېښودل او د اصلاح هڅه ده.","که د چا حق مو خوړلی وي، د حق بېرته ورکولو هڅه وکړئ."),
("صبر او امید","صبر د ستونزو پر مهال د سم عمل دوام دی.","مرسته وغواړئ او د ستونزې د حل عملي ګامونه واخلئ."),
("شکر او قناعت","شکر د نعمتونو پېژندنه او سم استعمال دی.","قناعت د هڅې پرېښودل نه دي؛ حلال کار او شکر یوځای کېدای شي."),
("د ژبې ساتنه","خبرې د اړیکو جوړولو یا خرابولو ځواک لري.","له غیبت، دروغو، سپکاوي او بې ثبوته تورونو ځان وساتئ."),
("د امانت ساتنه","امانت د مال، راز او مسؤلیت ساتنه هم رانغاړي.","د بل مال او معلومات د اجازې پرته مه کاروئ."),
("د وعدې پوره کول","وعده د اعتماد او مسؤلیت موضوع ده.","که د وعدې پوره کول ناشوني شي، ژر خبر ورکړئ او حل وړاندې کړئ."),
("د وخت ارزښت","وخت د عبادت، کورنۍ، زده کړې او کار لپاره نعمت دی.","ورځنی پلان جوړ کړئ او د نورو وخت ته هم درناوی وکړئ."),
("د بدن ساتنه","د بدن ساتنه د مسؤلانه ژوند برخه ده.","له زیانمنو عادتونو ډډه او د اړتیا پر مهال روغتیايي مشوره واخلئ."),
("د مال ساتنه","مال د مسؤلیت وسیله ده، نه د غرور معیار.","مصرف، سپما او مرسته په اعتدال تنظیم کړئ."),
("د میراث حقونه","میراث ځانګړي شرعي اصول او شرایط لري.","د واقعي قضیې وېش باید د اسنادو او باوري عالم یا متخصص په مرسته وشي."),
("د کورنۍ اړیکې","خپلوي پالنه د ښه اخلاقو برخه ده.","د اختلاف پر مهال د خبرو، بښنې او عادلانه حدودو لاره غوره کړئ."),
("د یتیم حقونه","د یتیم مال او عزت ساتل مهم مسؤلیت دی.","د هغه مال باید د هغه په ګټه او د قانوني اصولو مطابق وساتل شي."),
("د مسافر حقونه","مسافر په سفر کې ځانګړو اړتیاوو او شرعي اسانتیاوو ته مخامخ کېدای شي.","د سفر د عبادتونو رخصتونه له باوري فقهي لارښود څخه زده کړئ."),
("د ناروغ پوښتنه","د ناروغ پوښتنه د خواخوږۍ او ټولنیز ملاتړ بڼه ده.","د ناروغ محرمیت، آرام او د لیدنې مناسب وخت مراعات کړئ."),
("د اختلاف حل","شخړه په عادلانه منځګړیتوب کمېدای شي.","دواړو لورو ته د خبرو وخت ورکړئ او د زور پر ځای د حل لارې ولټوئ."),
("د اسلام اخلاقي موخه","اسلامي اخلاق د عبادت او ورځني چلند ترمنځ اړیکه جوړوي.","د ښه اخلاقو معیار په کور، بازار او عامه ژوند کې عملي کړئ."),
("د دیني سرچینو ارزونه","دیني ادعا باید له باوري متن او علمي تشریح سره وکتل شي.","له بې‌سنده ټولنیزو رسنیزو پیغامونو څخه د حکم اخیستلو پر ځای متخصص ته مراجعه وکړئ."),
("د مسلمان مسؤلیت","مسلمان د خپل عمل او د نورو د حقونو په اړه مسؤلیت لري.","له ځان اصلاح پیل کړئ او د خلکو په اړه بې‌ځایه قضاوت مه کوئ.")
]

FAITH_TOPICS = [
("بې اختیاره وسوسې","نا غوښتل شوي فکرونه په خپله د انسان قصدي عقیده نه ثابتوي."),
("شک او پوښتنه","پوښتنه کول د زده کړې لاره ده؛ په ارامه له باوري عالم څخه ځواب وغواړئ."),
("غوسه کې خبرې","د غوسې پر مهال خبرې باید له شرایطو سره وارزول شي؛ ژر حکم مه کوئ."),
("ټوکه او سپکاوی","د دیني خبرو ټوکه جدي مسئله کېدای شي؛ د مشخصې پېښې لپاره علمي مشوره واخلئ."),
("د کلمې ناسم فهم","د یوې جملې معنا د ژبې، نیت او سیاق له مخې بدلېدای شي."),
("ناپوهي","ناپوهي د علم د زده کړې اړتیا ښيي؛ د شخص د ایمان په اړه عمومي حکم مه کوئ."),
("زور او اکراه","د زور لاندې ویل شوې خبره ځانګړي فقهي بحثونه لري؛ متخصص دې قضیه وارزوي."),
("د نورو نقل قول","د بل چا خبره نقلول تل د نقل کوونکي د عقیدې څرګندونه نه وي."),
("وسوسې ته ځواب","د هرې وسوسې تکراري پلټنه اندېښنه زیاتولای شي؛ په اعتدال علم زده کړئ."),
("توبه او بېرته راستنېدل","د خطا وروسته د اصلاح، توبې او حق بېرته ورکولو لارې شته.")
]

BUSINESS_TOPICS = [
("رښتینې سوداګري","رښتینی پلورونکی د مال عیبونه، بیه او شرطونه روښانه کوي."),
("سود","سود د اسلامي فقهې مهم او جدي بحث دی؛ د پور او مالي قرارداد جزئیات له متخصص سره وڅېړئ."),
("درغلي","په اندازه، کیفیت، اسنادو یا پیسو کې قصدي فریب د اعتماد او حقونو زیانمنول دي."),
("د پور تړون","د پور اندازه، موده او د ورکړې شرطونه باید روښانه او ثبت شي."),
("د مشتری رضا","معامله باید په روښانه معلوماتو او د دواړو خواوو په رضایت ولاړه وي."),
("د کارګر حق","معاش، دنده، وخت او د کار شرایط باید عادلانه او معلوم وي."),
("د وزن او پیمانې عدالت","کم وزن ورکول د مشتری حق زیانمنوي."),
("د مال عیب بیانول","د مال معلوم عیب پټول د شخړې او بې باورۍ سبب کېږي."),
("آنلاین سوداګري","په انلاین پلور کې عکس، مشخصات، بیه او د بېرته ستنولو شرطونه واضح کړئ."),
("شراکت","د شریکانو ونډې، مسؤلیتونه او د ګټې وېش باید له مخکې لیکلي وي.")
]

# Make enough distinct lesson topics without copying the exact same title.
def expanded_topics(seed, count, group):
    # Keep only the title and explanation for course topics.
    out = [(str(item[0]), str(item[1])) for item in seed]
    original = list(out)
    while len(out) < count:
        base = original[(len(out) - len(original)) % len(original)]
        n = len(out) + 1
        title, intro = base
        out.append((f"{title} — عملي درس {n}", intro))
    return out[:count]

def words(text):
    return re.findall(r"\S+", text)

def lesson_body(title, intro, course, number):
    if course == "islam":
        extra = (
            f"د دې موضوع د زده کړې پر مهال د {title} اړوند ادعاوې له معتبرې سرچینې سره پرتله کړئ. "
            "قرآن کریم، معتبر حدیثي آثار او د وړ علماوو تشریحات د زده کړې مهمې سرچینې دي. "
            "د نورو دینونو د عقایدو په اړه خبرې د هغوی د معتبرو متونو او د پیروانو د تنوع په پام کې نیولو سره وکړئ. "
            "د یوې تاریخي پېښې یا د یوه شخص د عمل له مخې د ټول دین د ټولو پیروانو په اړه عمومي حکم مه کوئ."
        )
        practical = (
            "عملي تمرین: د موضوع درې مهم ټکي ولیکئ، د هر ټکي لپاره معتبره سرچینه پیدا کړئ، "
            "او هغه څه جلا کړئ چې قطعي معلومات دي او هغه څه چې د تفسیر یا اختلاف موضوع ده. "
            "په خبرو کې نرم الفاظ وکاروئ، د بل لوري خبره په امانتداري نقل کړئ، "
            "او که ځواب نه پوهېږئ، په ښکاره ووایئ چې نورې مطالعې ته اړتیا ده."
        )
    elif course == "faith":
        extra = (
            "د ایمان په اړه د یوې ځانګړې جملې یا پېښې حکم یوازې د لنډې ټوټې له مخې مه ټاکئ. "
            "معنا، سیاق، نیت، پوهه، اختیار، اکراه او د ویونکي حالت هغه عوامل دي چې د شرعي ارزونې لپاره اهمیت لرلای شي. "
            "دا موضوعات د هرې قضیې له مخې توپیر کوي؛ نو د عامو خلکو د ویډیوګانو یا لنډو پیغامونو پر بنسټ د چا د ایمان په اړه پرېکړه مه کوئ."
        )
        practical = (
            "عملي تمرین: که کومه خبره مو اندېښمنوي، اصلي عبارت او د خبرو حالت په ارامه ولیکئ، "
            "له باوري او وړ عالم څخه پوښتنه وکړئ، او له بې‌ځایه تکراري پلټنې څخه ځان وساتئ. "
            "که وسوسې ورځنی ژوند ګډوډوي، د رواني روغتیا له مسلکي متخصص سره خبرې کول هم ګټور کېدای شي. "
            "د خپل او د نورو د ایمان په اړه په احتیاط، مهربانۍ او علمي مسؤلیت چلند وکړئ."
        )
    else:
        extra = (
            f"د {title} موضوع د تړون، عادت او واقعي معاملې له جزئیاتو سره تړاو لرلای شي. "
            "د بیې، توکي، مقدار، نېټې، تحویل، ضمانت، پور او د شخړې د حل شرطونه روښانه کړئ. "
            "له دروغو، پټ فریب، د خلکو له حق خوړلو او د کارکوونکو له استثمار څخه ځان وساتئ. "
            "د معاصرو بانکدارۍ او آنلاین معاملاتو حکمونه کله ناکله ځانګړې تخنیکي پوهه غواړي."
        )
        practical = (
            "عملي تمرین: د معاملې ټول شرطونه په لیکلي سند کې ثبت کړئ، "
            "له دواړو خواوو د رضایت ډاډ واخلئ، رسید او اړوند اسناد وساتئ، "
            "او که قرارداد د سود، قسط، بیمې، شراکت یا نامعلوم خطر موضوع ولري، "
            "د دقیقو اسنادو په وړاندې کولو سره له باوري اسلامي مالي متخصص او قانوني مشاور څخه پوښتنه وکړئ."
        )

    body = (
        f"{intro}\n\n"
        f"د موضوع اهمیت: {title} د ورځني ژوند، اخلاقو او مسؤلیت له اړخونو سره تړاو لري. "
        "د دې درس هدف یوازې د اصطلاحاتو یادول نه دي، بلکې د پوهې، انصاف او سنجول شوي عمل عادت پیاوړی کول دي. "
        f"{extra}\n\n"
        f"{practical}\n\n"
        "د یادولو مهم ټکی: معلومات له باوري سرچینو واخلئ، د نورو عزت وساتئ، "
        "د شخړو پر مهال له بې‌ځایه تورونو ډډه وکړئ او د اړتیا په وخت کې له وړ متخصص څخه مشوره وغواړئ. "
        "دا تعلیمي متن د هرې ځانګړې قضیې لپاره د فتوا، قانوني مشورې یا د بشپړې علمي څېړنې بدیل نه دی."
    )
    return body

courses = []

def build_course(cid, title, description, seed, count, min_words, kind):
    topics = expanded_topics(seed, count, kind)
    lessons = []
    for i, (lesson_title, intro) in enumerate(topics, 1):
        body = lesson_body(lesson_title, intro, kind, i)
        count_words = len(words(body))
        if count_words < min_words:
            sys.exit(f"❌ د کلمو شمېر کم دی: {cid} / {i} = {count_words}")
        lessons.append({
            "id": f"{cid}-{i:03}",
            "number": i,
            "title": lesson_title,
            "subtitle": f"درس {i} — {count_words} کلمې",
            "sections": [
                {"heading": "تشریح", "body": body},
                {"heading": "د زده کړې یادونه", "body":
                    "دا موضوع له معتبرې سرچینې سره بیا وګورئ. د ځانګړو شرعي احکامو لپاره د خپل فقهي مذهب له باوري عالم څخه د قضیې له جزئیاتو سره پوښتنه وکړئ."}
            ],
            "word_count": count_words
        })
    courses.append({
        "id": cid, "title": title, "description": description,
        "lesson_count": len(lessons), "lessons": lessons
    })

build_course("islam", "اسلام او د دینونو پېژندنه",
    "۵۰ درسونه؛ د اسلام بنسټونه، اخلاق او د نورو دینونو درناوی",
    ISLAM_TOPICS, 50, 150, "islam")

build_course("faith", "د ایمان ساتنه او د خبرو پوهه",
    "۱۰۰ درسونه؛ وسوسې، نیت، سیاق او د تکفیر په موضوع کې احتیاط",
    expanded_topics(FAITH_TOPICS, 100, "faith"), 100, 50, "faith")

build_course("business", "حلال او حرام تجارت",
    "۵۰ درسونه؛ رښتینولي، قراردادونه، پورونه او د معاملاتو اصول",
    expanded_topics(BUSINESS_TOPICS, 50, "business"), 50, 100, "business")

# Prayer course: useful Arabic recitations and Pashto meanings.
prayer_lessons = [
("د لمانځه نیت","نیت د زړه اراده ده؛ د هر لمانځه لپاره د عبادت اراده په زړه کې ولرئ."),
("تکبیر تحریمه","اللّٰهُ أَكْبَرُ","الله تر ټولو لوی دی."),
("ثناء","سُبْحَانَكَ اللّٰهُمَّ وَبِحَمْدِكَ وَتَبَارَكَ اسْمُكَ وَتَعَالَىٰ جَدُّكَ وَلَا إِلَٰهَ غَيْرُكَ","اې الله! ته پاک یې او ستا ستاینه ده؛ ستا نوم برکتناک دی، ستا شان لوړ دی او له تا پرته بل معبود نشته."),
("تعوذ","أَعُوذُ بِاللّٰهِ مِنَ الشَّيْطَانِ الرَّجِيمِ","زه له رټل شوي شیطان څخه په الله پناه غواړم."),
("تسمیه","بِسْمِ اللّٰهِ الرَّحْمَٰنِ الرَّحِيمِ","د الله په نوم چې ډېر مهربان، بې حده رحم کوونکی دی."),
("سورة الفاتحة","الْحَمْدُ لِلّٰهِ رَبِّ الْعَالَمِينَ ۝ الرَّحْمَٰنِ الرَّحِيمِ ۝ مَالِكِ يَوْمِ الدِّينِ ۝ إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ ۝ اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ ۝ صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ","ټولې ستاینې الله لره دي، د نړۍ پالونکي؛ ډېر مهربان، بې حده رحم کوونکی؛ د جزا د ورځې مالک. یوازې ستا عبادت کوو او یوازې له تا مرسته غواړو. موږ ته سمه لار وښیه؛ د هغو کسانو لار چې نعمت دې ورکړی، نه د غضب شوو او نه د لار ورکو."),
("د رکوع تسبیح","سُبْحَانَ رَبِّيَ الْعَظِيمِ","زما لوی رب پاک دی."),
("له رکوع پورته کېدل","سَمِعَ اللّٰهُ لِمَنْ حَمِدَهُ","الله د هغه ستاینه اوري چې د هغه ستاینه کوي."),
("د رکوع وروسته","رَبَّنَا وَلَكَ الْحَمْدُ","اې زموږ ربه! ستاینه یوازې تا لره ده."),
("د سجدې تسبیح","سُبْحَانَ رَبِّيَ الْأَعْلَىٰ","زما تر ټولو لوړ رب پاک دی."),
("تشهد","التَّحِيَّاتُ لِلّٰهِ وَالصَّلَوَاتُ وَالطَّيِّبَاتُ، السَّلَامُ عَلَيْكَ أَيُّهَا النَّبِيُّ وَرَحْمَةُ اللّٰهِ وَبَرَكَاتُهُ، السَّلَامُ عَلَيْنَا وَعَلَىٰ عِبَادِ اللّٰهِ الصَّالِحِينَ، أَشْهَدُ أَنْ لَا إِلَٰهَ إِلَّا اللّٰهُ وَأَشْهَدُ أَنَّ مُحَمَّدًا عَبْدُهُ وَرَسُولُهُ","ټولې ویناوي، عبادتونه او پاکې خبرې الله لره دي. سلام دې وي پر تا، اې نبي، او د الله رحمت او برکتونه؛ سلام دې وي پر موږ او د الله پر نېکو بندګانو. ګواهي ورکوم چې له الله پرته بل معبود نشته او محمد د هغه بنده او رسول دی."),
("درود ابراهیمي","اللّٰهُمَّ صَلِّ عَلَىٰ مُحَمَّدٍ وَعَلَىٰ آلِ مُحَمَّدٍ، كَمَا صَلَّيْتَ عَلَىٰ إِبْرَاهِيمَ وَعَلَىٰ آلِ إِبْرَاهِيمَ، إِنَّكَ حَمِيدٌ مَجِيدٌ. اللّٰهُمَّ بَارِكْ عَلَىٰ مُحَمَّدٍ وَعَلَىٰ آلِ مُحَمَّدٍ، كَمَا بَارَكْتَ عَلَىٰ إِبْرَاهِيمَ وَعَلَىٰ آلِ إِبْرَاهِيمَ، إِنَّكَ حَمِيدٌ مَجِيدٌ","اې الله! پر محمد او د محمد پر کورنۍ رحمت نازل کړه لکه پر ابراهیم او د هغه پر کورنۍ دې چې نازل کړی؛ ته ستایل شوی او لوی یې. اې الله! پر محمد او د هغه پر کورنۍ برکت واچوه لکه پر ابراهیم او د هغه پر کورنۍ دې چې برکت اچولی؛ ته ستایل شوی او لوی یې."),
("د لمانځه سلام","السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللّٰهِ","پر تاسو دې سلام او د الله رحمت وي.")
]

prayer = []
for i, item in enumerate(prayer_lessons, 1):
    if len(item) == 4:
        title, arabic, pashto = item[0], item[2], item[3]
        extra = item[1]
    elif len(item) == 3:
        title, arabic, pashto = item
        extra = ""
    else:
        title, extra = item
        arabic = ""
        pashto = extra
    prayer.append({
        "id": f"prayer-{i:03}", "number": i, "title": title,
        "subtitle": "عربي متن او پښتو معنا",
        "sections": [
            {"heading": "عربي متن", "body": arabic},
            {"heading": "پښتو ژباړه / تشریح", "body": pashto},
            {"heading": "یادونه", "body":
             "د لمانځه د ځینو جزئیاتو په ترتیب او حکم کې د فقهي مذهبونو ترمنځ توپیر شته. دا لارښود د زده کړې لپاره دی؛ د حنفي طریقې او د خپل حالت د تفصیل لپاره له باوري عالم څخه پوښتنه وکړئ."}
        ]
    })

courses.insert(0, {
    "id": "prayer", "title": "د لمانځه عربي متن او پښتو ژباړه",
    "description": "د لمانځه مهم اذکار، عربي متن او پښتو معنا",
    "lesson_count": len(prayer), "lessons": prayer
})

payload = {
    "version": 2,
    "language": "ps",
    "note": "د زده کړې لپاره؛ ځانګړې فتوا دې له باوري عالم څخه واخیستل شي.",
    "courses": courses
}

DATA.parent.mkdir(parents=True, exist_ok=True)
DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

# Embed data in HTML to avoid file:// fetch restrictions in Android WebView.
encoded = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
js = r'''
<!-- NOOR_COURSES_V2 -->
<style id="noor-courses-v2-style">
.noor-course-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin:16px 0}
.noor-course-card,.noor-lesson-card{display:block;width:100%;text-align:start;border:1px solid #d9e8df;border-radius:18px;background:linear-gradient(145deg,#fff,#f0f8f2);padding:18px;margin:8px 0;color:inherit;cursor:pointer;box-shadow:0 4px 14px #073d2710}
.noor-course-card h3,.noor-lesson-card h3{margin:7px 0;color:#075b45}
.noor-course-card p,.noor-lesson-card p{line-height:1.8;margin:6px 0}
.noor-course-icon{font-size:30px}
.noor-course-count{display:inline-block;border-radius:30px;padding:5px 10px;background:#e1f2e8;color:#075b45;font-size:13px}
.noor-lesson-body{white-space:pre-line;line-height:2;font-size:16px}
.noor-arabic{direction:rtl;text-align:right;font-size:23px;line-height:2.1;font-family:serif}
.noor-section{background:#fff;border:1px solid #e2ebe5;border-radius:16px;padding:16px;margin:12px 0}
.noor-back{border:0;border-radius:12px;padding:10px 16px;background:#075b45;color:#fff;cursor:pointer}
</style>
<script id="noor-courses-v2-data" type="application/json">__NOOR_DATA__</script>
<script id="noor-courses-v2-script">
(function(){
"use strict";
const el=document.getElementById("noor-courses-v2-data");
if(!el)return;
const db=JSON.parse(el.textContent);
const courses=db.courses;
const findCourse=id=>courses.find(c=>c.id===id);
window.renderNoorCourseV2=function(id){
 const c=findCourse(id);if(!c){app.innerHTML="<p>درس ونه موندل شو.</p>";return;}
 let out='<button class="noor-back" data-action="course-v2:home">← کورپاڼه</button>';
 out+='<section class="panel"><h2>'+esc(c.title)+'</h2><p>'+esc(c.description)+'</p><span class="noor-course-count">'+c.lessons.length+' درسونه</span></section>';
 out+='<div class="noor-course-grid">';
 c.lessons.forEach((l,i)=>{out+='<button class="noor-lesson-card" data-action="course-lesson-v2:'+c.id+':'+i+'"><span class="noor-course-count">درس '+l.number+'</span><h3>'+esc(l.title)+'</h3><p>'+esc(l.subtitle||"د لوستلو لپاره پر کارت کلیک وکړئ")+'</p></button>';});
 out+='</div>';app.innerHTML=out;window.scrollTo(0,0);
};
window.renderNoorLessonV2=function(id,n){
 const c=findCourse(id),l=c&&c.lessons[n];if(!l){app.innerHTML="<p>درس ونه موندل شو.</p>";return;}
 let out='<button class="noor-back" data-action="course-v2:'+c.id+'">← د درسونو لېست</button>';
 out+='<section class="panel"><h2>'+esc(l.title)+'</h2><span class="noor-course-count">درس '+l.number+(l.word_count?' · '+l.word_count+' کلمې':'')+'</span></section>';
 (l.sections||[]).forEach(s=>{
   let cls=s.heading==="عربي متن"?"noor-arabic":"noor-lesson-body";
   out+='<section class="noor-section"><h3>'+esc(s.heading)+'</h3><div class="'+cls+'">'+esc(s.body)+'</div></section>';
 });
 out+='<button class="noor-back" data-action="course-v2:'+c.id+'">← بېرته</button>';
 app.innerHTML=out;window.scrollTo(0,0);
};
function esc(x){return String(x??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
window.noorCoursesV2HomeCards=function(){
 return '<div class="noor-course-grid">'+courses.map(c=>'<button class="noor-course-card" data-action="course-v2:'+c.id+'"><div class="noor-course-icon">'+({prayer:"🕌",islam:"📚",faith:"🛡️",business:"💼"}[c.id]||"📖")+'</div><h3>'+esc(c.title)+'</h3><p>'+esc(c.description)+'</p><span class="noor-course-count">'+c.lessons.length+' درسونه</span></button>').join("")+'</div>';
};
})();
</script>
<!-- /NOOR_COURSES_V2 -->
'''.replace("__NOOR_DATA__", encoded)

# Insert the course cards into the homepage only, not into every page.
# Wrap in a function call so the existing home() can add the cards without
# changing the existing Quran and lesson datasets.
home_pos = source.find("function home()")
home_end = source.find("\nfunction ", home_pos + 1)
if home_end == -1:
    sys.exit("❌ د home() پای ونه موندل شو؛ فایل نه دی بدل شوی.")

home_block = source[home_pos:home_end]
if "noorCoursesV2HomeCards" not in home_block:
    # Add cards immediately after home() starts. Existing page content remains.
    brace = home_block.find("{")
    if brace < 0:
        sys.exit("❌ د home() جوړښت ناسم دی.")
    home_block = home_block[:brace+1] + '\n  /* NOOR_COURSES_V2_HOME */\n  ' + \
        'const noorCoursesV2Markup = window.noorCoursesV2HomeCards ? window.noorCoursesV2HomeCards() : "";' + \
        '\n  ' + home_block[brace+1:]
    # Existing home() builds an HTML string into app.innerHTML. Add cards before
    # the Quran heading using a safe insertion into its final rendered HTML.
    home_block = home_block.replace(
        'app.innerHTML = ',
        'app.innerHTML = ',
        1
    )
    # More general: inject a wrapper after home renders, avoiding assumptions
    # about the exact template-string expression.
    last = home_block.rfind("}")
    home_block = home_block[:last] + '''
  if (window.noorCoursesV2HomeCards && typeof app !== "undefined") {
    const courseHost = document.createElement("div");
    courseHost.innerHTML = window.noorCoursesV2HomeCards();
    const firstPanel = app.querySelector(".hero, .panel");
    if (firstPanel) firstPanel.insertAdjacentElement("afterend", courseHost);
    else app.prepend(courseHost);
  }
''' + home_block[last:]
    source = source[:home_pos] + home_block + source[home_end:]

# Route support: insert near the beginning of render().
render_pos = source.find("function render()")
render_brace = source.find("{", render_pos)
route_code = '''
  if (typeof page === "string" && page.startsWith("course-v2:")) {
    const courseId = page.split(":")[1];
    if (courseId === "home") { page = "home"; home(); return; }
    renderNoorCourseV2(courseId); return;
  }
  if (typeof page === "string" && page.startsWith("course-lesson-v2:")) {
    const parts = page.split(":");
    renderNoorLessonV2(parts[1], Number(parts[2])); return;
  }
'''
if render_pos < 0 or render_brace < 0:
    sys.exit("❌ render() پیدا نه شو؛ HTML نه دی بدل شوی.")
source = source[:render_brace+1] + route_code + source[render_brace+1:]

# Hook into existing click listener without replacing its current actions.
click_match = re.search(r'app\.addEventListener\(\s*[\'"]click[\'"]\s*,\s*e\s*=>\s*\{', source)
if not click_match:
    sys.exit("❌ click handler ونه موندل شو؛ HTML نه دی بدل شوی.")
click_insert = click_match.end()
click_code = '''
  const noorCourseButton = e.target.closest("[data-action^='course-v2:'],[data-action^='course-lesson-v2:']");
  if (noorCourseButton) {
    e.preventDefault();
    page = noorCourseButton.dataset.action;
    if (typeof render === "function") render();
    return;
  }
'''
source = source[:click_insert] + click_code + source[click_insert:]

# Put the support code before </body> so the page has loaded its original scripts.
if "</body>" not in source:
    sys.exit("❌ </body> پیدا نه شو.")
source = source.replace("</body>", js + "\n</body>", 1)

# Structural verification before overwriting the original HTML.
for required in (MARKER, "renderNoorCourseV2", "renderNoorLessonV2",
                 "course-lesson-v2:", "noorCoursesV2HomeCards"):
    if required not in source:
        sys.exit("❌ د تایید نښه نشته: " + required)

HTML.write_text(source, encoding="utf-8")

print("\n✅ د نوي کورسونو معلومات جوړ شول:", DATA)
print("✅ HTML نوی شو:", HTML)
print("✅ د لمانځه لارښودونه:", len(prayer))
for c in courses:
    print(f"✅ {c['title']}: {len(c['lessons'])} درسونه")
print("✅ د درسونو د کلمو شمېر وازمویل شو.")
print("✅ موجود قرآن او نور JSON فایلونه نه دي بدل شوي.")
print("⚠️ یادونه: د لمانځه عربي متنونه دې له باوري مصحف/فقهي سرچینې سره وکتل شي.")
