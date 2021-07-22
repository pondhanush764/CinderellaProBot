import random
from telegram.ext import run_async, Filters
from telegram import Message, Chat, Update, Bot, MessageEntity
from cinderella import dispatcher
from cinderella.modules.disable import DisableAbleCommandHandler

ABUSE_STRINGS = (
    "Palla odachi kaila kuduthuruven🥱",
    "Hair ah pudungu🤭",
    "Po di dog🤣",
    "Railway station la suthuravan ella inga vandhurukane🤢",
    "Vaaya moodu da korangu🤫",
    "Nandri ketta naaye😡",
    "Manda bathiram",
    "Ennada ithu mooji🤣 Sethula mukkuna mathiri iruku🤣",
    "Vayila nalla varuthu🤬 Ean thalaivan @THE_BOSS_OF_TELEGRAM kaga tha amaithiya iruke🥱",
    "Nenga moodetu irukalam nu computer solluthu sir😑",
    "Po da 8+1 🤣 8 ah yu 1 ah yu setha 81 pa 🤣",
    "Yar da avan /abuse /abuse nu pottu uyira vanguran😒",
    "Dai unaya na kutralathula pathene🤔 ovvoru trees ka thavi thavi pova🤭 unaku inga enna vela 🤣",
    "Na unaya eppudi thitunalu unayala hair ah kooda pudunga mudiyathu🤣🤣🤣",
    "Moonja odaichi kaila koduthuruve pathuko🤫",
    "Enga team no way kitta mothi par da mudinja🤣, unayala hair ah kooda pudunga mudiyathu🤭,only for haters😒",
    "Ivan evan da mutta paiyan🤢",
    "yenaya ethavathu un grp la add panni admin podu na soldre😒",
    "Yar da ivan loosu mathiri olaruran",
    "My thambi veluma🤣, Apd illa pa 😳 my thambi football player atha coaching ku veluma nu kete 🤣",
    "Ivan yarrda pombala poruki ah irukan🥱",
    "Po di anguttu🤬",
    "Summa summa kadup hair ah eatha koodathu🤬",
    "Ena sound vidura 🥱 Vaya odachiruve😡",
    "Enaku /abuse nu command pottavar periya mannar parambora🤢 Ivar yarayachu thitta sonan na thitaluma 🤣🥱",
    "Dai ne ena avalo periya kinguh ah😡,Iru nalaki unaku sangu tha 🥱",
    "Ean area la nan than da raaja .👿",
    "Ippa ean da kadharura🤣",
    "Ithu 18+ Pa🚫 . ellaru nalla potengala🤣 ,Eppa Eppa nenga high level thinking ku ella pogathenga😳, Na vote ah sone🤣",
    "Moonjum aalum mandayayum paaru🤣",
    "Na enna unaku velakarana ne /abuse nu potta na soldrathuku😡",
    "Po da baadu🥱",
    "Thambi enna pa unaku ippa prechana🙄",
    "Enna da landha🥱",
    "Sanda na sollu sirappa senjiruvom🥱",
    "Tharai la ooduthu paambu ne apparama poi ****🤭 paaru nu solla vandhen athu kulla antha symbol came 🤣🤣",
    "Kuttralathula iruka vendiyavangala inga vandhu namma uyira vanguranga",
    "Po da kundu papa🤣🤭",
    "Yar da enaya koopitathu🙄",
    "Po da uncle ooda wife🤣",
    "I am tired , ipa na yarayu thittura nalamai la illa pa 🥱",
    "Kanna nondi eduthuruve 👀",
    "Seruppu keela iruku , innum oru sec la ne mela irupa🤣",
    "Vanga grandma👵",
    "Po da panni.... Next rhyming ah na pesuna avan odeeruvan🤣",
    "Pongada nengalu unga /abuse um😒"
  )

SONG_STRINGS = (
    "🎶 ஹே ரக்கிட் ரக்கிட் ரக்கிட்ட... 🎶",
    "🎶 என் கண்ணுகுள்ள ஒரு சிருக்கி கட்டிபுட்டாளே என்ன இருக்கி மனசகட்டி போட மறுத்தாளே ஹய்யோ, ஹய்யையோ... 🎶",
    "🎶 உன் பேரே தெரியாது உன்னை கூப்பிட முடியாது நான் உனக்கோர் பேர் வைத்தேன் உனக்கே தெரியாது... 🎶", 
    "🎶 உனக்கென்ன வேணும் சொல்லு உலகத்தை காட்டச் சொல்லு புது இடம் புது மேகம் தேடி போவோமே... 🎶", 
    "🎶 காதல மறக்க நினைச்சு சிரிக்கிறேன் என் காதலி முகத்த நினைச்சு சிரிக்கிறேன் சோகத்தில் லைப்ப நினைச்சு சிரிக்கிறேன் நான் கோவத்த அடக்க முடியல சிரிக்கிறேன்... 🎶", 
    "🎶 உன்ன நெனச்சு நெனச்சு உருகி போனேன் மெழுகா நெஞ்ச ஒதைச்சு ஒதைச்சு பறந்து போனா அழகா... 🎶", 
    "🎶 ஏதோ ஒன்று என்னை தாக்க யாரோ போல உன்னை பார்க்க... 🎶", 
    "🎶 எதிர் வீட்டு ஹீரோயினி நீ லெமன் மின்ட்டு கூலர்மா நீ ஏதோ கொஞ்சம் கிளாமருதான் நீ அதுகின்னமா... 🎶", 
    "🎶எதுக்காக கிட்ட வந்தாளோ? எத தேடி விட்டு போனாளோ விழுந்தாலும் நா ஒடஞ்சே போயிருந்தாலும் உன் நினைவிருந்தாலே போதும் நிமிர்ந்திடுவேனே நானும்🎶", 
    "🎶இங்கே இங்கே ஒரு மர்லின் மன்றோ நான்தான் உன்கையின் காம்பில் பூ நான் நம் காதல் யாவும் தேன்தான்\nபூவே பூவே நீ போதை கொள்ளும் பாடம் மனம் காற்றைப்போல ஓடும் உன்னை காதல் கண்கள் தேடும்🎶", 
    "ஆண்: 🥰ஓ... மஞ்சள் குங்குமம் தாலியின் சிறப்பு பெண்களுக்கெல்லாம் இன்னொரு பொறப்பு🥰🥰\nபெண்: டும் டும் டும் டும்☺\nஆண்: டும் டும் டும் டுடும் டுடும் டும் டும் டும் டும்😁", 
    "🎶மனசுல பூங்காத்து நீ பாக்கும் திசையில் வீசும் போது நமக்குன்னு ஒரு தேசம் அதில் இருவரும் சேர்ந்து ஒன்னா வாழ்வோம்🎶", 
    "🎶சார பாம்பு சடை சலவை செஞ்ச இடை சாட்டா வீசும் நடை உனக்குதான்\nமார்பில் மச்சபடை மனசில் ரெட்டை கொட தோதா தூக்கும் இடம் உனக்குதான்\nஎன் கூச்சம் எல்லாம் குத்தகைக்கு உனக்குதான்\nஎன் கொழுகொழுப்பு இலவசம் உனக்குதான்🎶", 
    "🎶hand la glass..glass la scotch eyes-u full-aa tear-u\nempty life-u.. girl-u come-u life reverse gear-u\nlovvu lovvu ..oh my lovvu you showed me bouv-u cow-u cow-u holi cow-u i want u hear now-u🎶", 
    "🎶சின்னச் சின்ன ஆச, உள்ள திக்கித் திக்கிப் பேச! மல்லிகப்பூ வாசம், கொஞ்சம் காத்தோட வீச! உத்து உத்துப் பார்க்க,நெஞ்சில் முத்து முத்தா வேர்க்க! புத்தம் புது வாழ்க்க, என்ன உன்னோட சேர்க்க!🎶", 
    "🎶Insta கிராமத்துல வாடி வாழலாம் நாம வாழும் நிமிஷத்தெல்லாம் சுட்டு தள்ளலாம்\nநானும் நீயும் சேரும் பொது தாறுமாறு தான் அந்த FaceBook-இல் பிச்சிக்கிடும் Like-உ Share-உ தான்🎶", 
    "🎶ஏ மைக்ரோ மிடி போடட்டா பூனை நட நடக்கட்டா ஜோலிக்கே பீஜேன்னு சோக்கா பாடட்டா\nஏ இங்கிலீபீசு வேணான்டி இந்தி பீசு வேணான்டி கரகாட்டம் ஆடிக்கிட்டே தமிழில் பாடேன்டி🎶", 
    "🎶என் நாடியை சிலிர்க்க வைத்தாய் என் இரவெல்லாம் வெளிச்சம் தந்தாய்\nஎன் ஆண் கர்வம் மறந்தின்று உன் முன்னே பணிய வைத்தாய்🎶"
 )

@run_async
def abuse(bot: Bot, update: Update):
    bot.sendChatAction(update.effective_chat.id, "typing") # Bot typing before send messages
    message = update.effective_message
    if message.reply_to_message:
      message.reply_to_message.reply_text(random.choice(ABUSE_STRINGS))
    else:
      message.reply_text(random.choice(ABUSE_STRINGS))

@run_async
def sing(bot: Bot, update: Update):
    bot.sendChatAction(update.effective_chat.id, "typing") # Bot typing before send messages
    message = update.effective_message
    if message.reply_to_message:
      message.reply_to_message.reply_text(random.choice(SONG_STRINGS))
    else:
      message.reply_text(random.choice(SONG_STRINGS))

__help__ = """
- /abuse : Abuse someone in malayalam.
- /sing : First lines of some random malayalam Songs.
"""

__mod_name__ = "Tamil💥"

ABUSE_HANDLER = DisableAbleCommandHandler("abuse", abuse)
SING_HANDLER = DisableAbleCommandHandler("sing", sing)

dispatcher.add_handler(ABUSE_HANDLER)
dispatcher.add_handler(SING_HANDLER)
