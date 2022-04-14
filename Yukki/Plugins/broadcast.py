import asyncio

from pyrogram.types import Message
from pyrogram import filters, Client

from Yukki import app, OWNER
from ..YukkiUtilities.helpers.filters import command
from Yukki.YukkiUtilities.database.chats import get_served_chats


@app.on_message(command(["broadcast_pin"]) & filters.user(OWNER))
async def broadcast_message_pin(_, message):
    if message.reply_to_message:
        msg = await message.reply_text("🔄 Broadcasting message...")
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        pins = 0
        chats = []
        schats = await get_served_chats()
        chats.extend(int(chat["chat_id"]) for chat in schats)
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=False)
                    pins += 1
                except Exception:
                    pass
                await asyncio.sleep(.3)
                sent += 1
            except Exception:
                pass
        await msg.edit_text(f"✅ Broadcasted message in {sent} chats\n📌 Sent with {pins} chat pins.")
        return
    if len(message.command) < 2:
        await message.reply_text("**usage**:\n\n/broadcast_pin (message)")
        return
    msg = await message.reply_text("🔄 Broadcasting message...")
    text = message.text.split(None, 1)[1]
    sent = 0
    pins = 0
    chats = []
    schats = await get_served_chats()
    chats.extend(int(chat["chat_id"]) for chat in schats)
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            try:
                await m.pin(disable_notification=False)
                pins += 1
            except Exception:
                pass
            await asyncio.sleep(.3)
            sent += 1
        except Exception:
            pass
    await msg.edit_text(f"✅ Broadcasted message in {sent} chats\n📌 Sent with {pins} chat pins.")


@app.on_message(command(["broadcast"]) & filters.user(OWNER))
async def broadcast_message_nopin(_, message):
    if message.reply_to_message:
        msg = await message.reply_text("🔄 Broadcasting message...")
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        chats = []
        schats = await get_served_chats()
        chats.extend(int(chat["chat_id"]) for chat in schats)
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await msg.edit_text(f"✅ Broadcasted message in {sent} chats")
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**usage**:\n\n/broadcast (message)"
        )
        return
    msg = await message.reply_text("🔄 Broadcasting message...")
    text = message.text.split(None, 1)[1]
    sent = 0
    chats = []
    schats = await get_served_chats()
    chats.extend(int(chat["chat_id"]) for chat in schats)
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await msg.edit_text(f"✅ Broadcasted message in {sent} chats")
