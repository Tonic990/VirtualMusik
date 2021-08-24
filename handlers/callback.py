# (C) supun-maduraga my best friend for his project on call-music-plus

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from config import BOT_NAME


# close calllback

@Client.on_callback_query(filters.regex("close"))
async def close(_, query: CallbackQuery):
    await query.message.delete()

# Player Control Callbacks

@Client.on_callback_query(filters.regex("cbback"))
async def cbback(_, query: CallbackQuery):
    await query.edit_message_text(
        "**💡 here is the control menu of bot:**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⏸ pause music", callback_data="cbpause"
                    ),
                    InlineKeyboardButton(
                        "▶️ resume music", callback_data="cbresume"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⏩ skip music", callback_data="cbskip"
                    ),
                    InlineKeyboardButton(
                        "⏹ end music", callback_data="cbend"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔇 mute player", callback_data="cbmute"
                    ),
                    InlineKeyboardButton(
                        "🔊 unmute player", callback_data="cbunmute"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🗑 del cmd", callback_data="cbdelcmds"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbdelcmds"))
async def cbdelcmds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>this is the feature information:</b>
        
**💡 Feature:** delete every commands sent by users to avoid spam !

**❔ usage:**

   1️⃣ to turn on feature:
      - type /delcmd on
    
   2️⃣ to turn off feature:
      - type /delcmd off
      
⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏡 BACK", callback_data="cbback"
                    )
                ]
            ]
        )
    )
