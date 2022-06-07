import yt_dlp

from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)
from youtubesearchpython import VideosSearch

from ..YukkiUtilities.helpers.ytdl import ytdl_opts 
from ..YukkiUtilities.helpers.filters import command
from ..YukkiUtilities.helpers.thumbnails import down_thumb
from Yukki.YukkiUtilities.database.queue import remove_active_chat
from Yukki.YukkiUtilities.database.sudo import get_sudoers, remove_sudo
from ..YukkiUtilities.helpers.inline import start_keyboard, personal_markup
from Yukki import app, BOT_USERNAME, BOT_ID, ASSID, ASSNAME, ASSUSERNAME, OWNER, SUDOERS
from Yukki.YukkiUtilities.database.chats import get_served_chats, is_served_chat, add_served_chat

welcome_captcha_group = 2

@app.on_message(filters.new_chat_members, group=welcome_captcha_group)
async def welcome(_, message: Message):
    chat_id = message.chat.id
    for member in message.new_chat_members:
        try:
            if member.id in OWNER:
                return await app.send_message(
                    chat_id,
                    f"🧙🏻‍♂️ • {member.mention} •\n\n• **Owner** of {BOT_NAME} has joined this Group.",
                )
            if member.id in SUDOERS:
                return await app.send_message(
                    chat_id,
                    f"🧙🏻‍♂️ • {member.mention} •\n\n• **Staff** of {BOT_NAME} has joined this Group.",
                )
            if member.id == ASSID:
                await remove_active_chat(chat_id)
            if member.id == BOT_ID:
                out = start_pannel()
                await app.send_message(
                    chat_id,
                    f"❤️ **Thanks for adding me to the group !**\n\n**Promote me as administrator of the group, otherwise I will not be able to work properly.\nOnce done, type `/reload`",
                    reply_markup=InlineKeyboardMarkup(out[1]),
                )
                return
        except:
            return


@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def play(_, message: Message):
    if len(message.command) == 2:
        chat_id = message.chat.id                                                       
        query = message.text.split(None, 1)[1]
        f1 = (query[0])
        f2 = (query[1])
        f3 = (query[2])
        finxx = (f"{f1}{f2}{f3}")
        if str(finxx) == "inf":
            boom = await app.send_message(chat_id, "🔍 Getting info...")
            query = ((str(query)).replace("info_","", 1))
            query = (f"https://www.youtube.com/watch?v={query}")
            results = VideosSearch(query, limit=1)
            for result in results.result()["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channel = result["channel"]["name"]
                link = result["link"]
            searched_text = f"""
💡 **Track Informations**

🏷 **Name:** {title}
⏱ **Duration:** {duration}
👀 **Views:** {views}
📣 **Channel:** {channel}
🔗 **Link:** {link}

⚡️ __Powered by Veez Music AI__"""
            buttons = personal_markup(link)
            userid = message.from_user.id
            thumb = await down_thumb(thumbnail, userid)
            await boom.delete()
            await app.send_photo(message.chat.id,
                photo=thumb,                 
                caption=searched_text,
                parse_mode="markdown",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        if str(finxx) == "sud":
            sudoers = await get_sudoers()
            text = "🧙🏻‍♂️ **List of sudo users:**\n\n"
            for count, user_id in enumerate(sudoers, 1):
                try:                     
                    user = await app.get_users(user_id)
                    user = user.first_name if not user.mention else user.mention
                except Exception:
                    continue                     
                text += f"➤ {user}\n"
            if not text:
                await message.reply_text("❌ no sudo users found")  
            else:
                await message.reply_text(text)
