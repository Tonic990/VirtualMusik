import os
import aiohttp
import asyncio
import json
import sys
import time
from config import OWNER_NAME as bn
from youtubesearchpython import SearchVideos
from pyrogram import filters, Client
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

@Client.on_message(filters.command("song") & ~filters.edited)
async def song(client, message):
    cap = f"🎶 Uploader @{bn}"
    url = message.text.split(None, 1)[1]
    veez = await message.reply("🔁 processing...")
    if not url:
        await veez.edit("**❗ give a valid song name.**")
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get("search_result")
    try:
        url = q[0]["link"]
    except BaseException:
        return await veez.edit("❗ song not found.")
    type = "audio"
    if type == "audio":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        song = True
    try:
        await veez.edit("📥 downloading...")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await veez.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await veez.edit("`the download content was too short.`")
        return
    except GeoRestrictedError:
        await veez.edit(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await veez.edit("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await veez.edit("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await veez.edit("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await veez.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await veez.edit("`There was an error during info extraction.`")
        return
    except Exception as e:
        await veez.edit(f"{str(type(e)): {str(e)}}")
        return
    time.time()
    if song:
        await veez.edit("📤 uploading...") #veez
        lol = "./etc/thumb.jpg"
        lel = await message.reply_audio(
                 f"{rip_data['id']}.mp3",
                 duration=int(rip_data["duration"]),
                 title=str(rip_data["title"]),
                 performer=str(rip_data["uploader"]),
                 thumb=lol,
                 caption=cap)  #music
        await veez.delete()
