import asyncio
from telethon.tl.types import ChannelParticipantsAdmins
from telegram.ext import run_async
from telegram import Message, Chat, Update, Bot, ParseMode
import telethon
from telethon import events


@run_async
def all(bot: Bot, update: Update):
async def _(event):
    if event.fwd_from:
        return 
    mentions = event.pattern_match.group(1)
    chat = await event.get_input_chat()
    async for x in bot.iter_participants(chat, 500):
        mentions += f" \n [{x.first_name}](tg://user?id={x.id})"
    await event.reply(mentions)
    await event.delete()





__mod_name__ = "Tagall"
__help__ = """
- /tagall : Tag everyone in a chat
"""

TAGALL_HANDLER = DisableAbleCommandHandler("@all", all)
dispatcher.add_handler(TAGALL_HANDLER)
