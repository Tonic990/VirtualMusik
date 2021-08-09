from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
import asyncio
from helpers.decorators import authorized_users_only, errors
from callsmusic.callsmusic import client as USER
from config import SUDO_USERS

@Client.on_message(filters.command(["veezjoin"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>make me as admin first</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "music player"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "🤖: i'm joined here to play music on voice chat.")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>assistant music already in your chat</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Flood Wait Error 🛑 \n The {user.first_name} can't join to your group, the assistant has been banned by admin in this group."
            "\n\nplease unbanned the assistant or add manually.</b>",
        )
        return
    await message.reply_text(
        "<b>assistant music joined your chat.</b>",
    )


@USER.on_message(filters.group & filters.command(["vleave"]))
@authorized_users_only
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            f"<b>assistant can't leave chats because waiting for floodwait."
            "\n\nor kick assistant manually</b>",
        )
        return
    
@Client.on_message(filters.command(["vleaveall"]))
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left=0
        failed=0
        await message.reply("assistant leaving all chats !")
        for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left+1
                await lol.edit(f"Assistant leaving... Left: {left} chats. Failed: {failed} chats.")
            except:
                failed=failed+1
                await lol.edit(f"Assistant leaving... Left: {left} chats. Failed: {failed} chats.")
            await asyncio.sleep(0.7)
        await client.send_message(message.chat.id, f"Left {left} chats. Failed {failed} chats.")
