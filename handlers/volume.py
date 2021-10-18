import re
import subprocess
from pyrogram import Client, filters
from helpers.filters import command
from pyrogram.handlers import CallbackQueryHandler
from helpers.decorators import authorized_users_only
from pyrogram.types import MessageHandler, InlineKeyboardMarkup, InlineKeyboardButton
from config import SUDO_USERS


@Client.on_message(command(["volume", f"volume@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
def volume(client, message):
    if len(message.text.split()) == 2 and message.from_user.id in SUDO_USERS:
        try:
            volume = int(message.text.split()[1])
            if volume in range(1, 101):
                volume = f"{volume}%"
                subprocess.Popen(
                    [
                        "pactl",
                        "set-sink-volume",
                        "MySink",
                        volume
                    ]
                ).wait()
                message.reply_text(
                    f"Volume set to {0}".format(volume)
                )
                return
        except:
            pass

    current_volume = "".join(re.search(r"Volume\:(.+)\n", subprocess.check_output(
        ["pactl", "list", "sinks"]).decode()).group(0).split()).split("/")[1]

    if message.from_user.id in SUDO_USERS:
        message.reply_text(
            f"Current volume is {0}".format(current_volume),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "➖",
                            callback_data="decrease_volume"
                        ),
                        InlineKeyboardButton(
                            "➕",
                            callback_data="increase_volume"
                        )
                    ]
                ]
            ),
            quote=True
        )
    else:
        message.reply_text(
            f"Current volume is {0}".format(current_volume),
        )


@Client.on_callback_query(filters.regex("volume"))
def callback(client, query):
    current_volume = int(query.message.text.split()[-1].replace("%", ""))

    if query.data == "decrease_volume":
        volume = current_volume - 1

        if volume < 0:
            volume = 0

        volume = f"{volume}%"

        subprocess.Popen(["pactl", "set-sink-volume", "MySink", volume]).wait()

        query.message.reply_text(
            f"Current volume is {0}".format(volume),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("➖", callback_data="decrease_volume"),
                        InlineKeyboardButton("➕", callback_data="increase_volume"),
                    ]
                ]
            ),
            quote=False,
        )
        query.message.delete()
        query.answer()
    elif query.data == "increase_volume":
        volume = current_volume + 1

        if volume > 100:
            volume = 100

        volume = f"{volume}%"

        subprocess.Popen(["pactl", "set-sink-volume", "MySink", volume]).wait()

        query.message.reply_text(
            f"Current volume is {0}".format(volume),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("➖", callback_data="decrease_volume"),
                        InlineKeyboardButton("➕", callback_data="increase_volume"),
                    ]
                ]
            ),
            quote=False,
        )
        query.message.delete()
        query.answer()
