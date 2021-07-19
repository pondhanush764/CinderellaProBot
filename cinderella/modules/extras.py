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
    "🎶 മിഴിയറിയാതെ വന്നു നീ മിഴിയൂഞ്ഞാലിൽ... കനവറിയാതെയേതോ കിനാവു പോലെ... 🎶.",
    "🎶 നിലാവിന്റെ നീലഭസ്മ കുറിയണിഞ്ഞവളേ... കാതിലോലക്കമ്മലിട്ടു കുണുങ്ങി നിന്നവളേ... 🎶",
    "🎶 എന്തിനു വേറൊരു സൂര്യോദയം... നീയെൻ പൊന്നുഷസ്സന്ധ്യയല്ലേ... 🎶", 
    "🎶 ശ്രീരാഗമോ തേടുന്നിതെൻ വീണതൻ പൊൻ തന്ത്രിയിൽ... 🎶", 
    "🎶 മഴത്തുള്ളികൾ പൊഴിഞ്ഞീടുമീ നാടൻ വഴി... നനഞ്ഞോടിയെൻ കുടക്കീഴിൽ നീ വന്ന നാൾ... 🎶", 
    "🎶 നീയൊരു പുഴയായ് തഴുകുമ്പോൾ ഞാൻ പ്രണയം വിടരും കരയാവും... 🎶", 
    "🎶 അല്ലിമലർ കാവിൽ പൂരം കാണാൻ... അന്നു നമ്മൾ പോയി രാവിൽ നിലാവിൽ... 🎶", 
    "🎶 നിലാവിന്റെ നീലഭസ്മ കുറിയണിഞ്ഞവളേ... കാതിലോലക്കമ്മലിട്ടു കുണുങ്ങി നിന്നവളേ... 🎶", 
    "🎶 ചന്ദനച്ചോലയിൽ മുങ്ങിനീരാടിയെൻ ഇളമാൻ കിടാവേ ഉറക്കമായോ... 🎶", 
    "🎶 അന്തിപ്പൊൻവെട്ടം കടലിൽ മെല്ലെത്താഴുമ്പോൾ... മാനത്തെ മുല്ലത്തറയില് മാണിക്യച്ചെപ്പ്... 🎶", 
    "🎶 താമരപ്പൂവിൽ വാഴും ദേവിയല്ലോ നീ... പൂനിലാക്കടവിൽ പൂക്കും പുണ്യമല്ലോ നീ... 🎶", 
    "🎶 കുന്നിമണിച്ചെപ്പു തുറന്നെണ്ണി നോക്കും നേരം, പിന്നിൽവന്നു കണ്ണു പൊത്തും കള്ളനെങ്ങു പോയി... 🎶", 
    "🎶 ശ്യാമാംബരം പുൽകുന്നൊരാ വെൺചന്ദ്രനായ് നിൻ പൂമുഖം... 🎶", 
    "🎶 പാടം പൂത്തകാലം പാടാൻ വന്നു നീയും... 🎶", 
    "🎶 കറുകവയൽ കുരുവീ... മുറിവാലൻ കുരുവീ... തളിർ വെറ്റിലയുണ്ടോ... വരദക്ഷിണ വെക്കാൻ... 🎶", 
    "🎶 പത്തുവെളുപ്പിന് മുറ്റത്തു നിക്കണ കസ്തൂരി മുല്ലയ്ക്ക് കാത്തുകുത്ത്... എന്റെ കസ്തൂരി മുല്ലയ്ക്ക് കാതു കുത്ത്.. 🎶", 
    "🎶 മഞ്ഞൾ പ്രസാദവും നെറ്റിയിൽ ചാർത്തി... മഞ്ഞക്കുറിമുണ്ടു ചുറ്റി... 🎶", 
    "🎶 കറുത്തപെണ്ണേ നിന്നെ കാണാഞ്ഞിട്ടൊരു നാളുണ്ടേ... 🎶"
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

__mod_name__ = "fun"

ABUSE_HANDLER = DisableAbleCommandHandler("abuse", abuse)
SING_HANDLER = DisableAbleCommandHandler("sing", sing)

dispatcher.add_handler(ABUSE_HANDLER)
dispatcher.add_handler(SING_HANDLER)
