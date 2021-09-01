# function to remove the downloaded files

import os

from pyrogram import Client, filters
from pyrogram.types import Message
from helpers.filters import command
from helpers.decorators import sudo_users_only, errors

downloads = os.path.realpath("downloads")


@Client.on_message(command(["rmd", "rmdownloads", "cleardownloads"]) & ~filters.edited)
@sudo_users_only
@errors
asycn def clear_downloads(_, message: Message):
    ls_dir = os.listdir(downloads)
    if ls_dir:
        for file in os.listdir(downloads):
            os.remove(os.path.join(downloads, file))
        await message.reply_text("<b>✅ deleted all downloaded files</b>", quote=False)
    else:
        await message.reply_text("<b>❌ no files downloaded</b>", quote=False)
