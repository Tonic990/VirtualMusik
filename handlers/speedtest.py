import os
import wget
import speedtest
from pyrogram.types import Message
from pyrogram import filters, Client
from helpers.gets import bytes
from helpers.onoff import (is_on_off, add_on, add_off)
from config import SUDO_USERS


@Client.on_message(filters.command("speedtest") & ~filters.edited)
async def gstats(_, message: Message):
    userid = message.from_user.id
    if await is_on_off(2):
        if userid in SUDO_USERS:
            pass
        else:
            return
    m = await message.reply_text("running server speed test")
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = await m.edit("running download speedtest...")
        test.download()
        m = await m.edit("running upload speedtest...")
        test.upload()
        test.results.share()
        result = test.results.dict()
    except Exception as e:
        await message.err(text=e)
        return 
    m = await m.edit("sharing speedtest results...")
    path = wget.download(result["share"])
    output = f"""**SpeedTest Results**
    
<u>**Client:**</u>
**__ISP:__** {result['client']['isp']}
**__Country:__** {result['client']['country']}
  
<u>**Server:**</u>
**__Name:__** {result['server']['name']}
**__Country:__** {result['server']['country']}, {result['server']['cc']}
**__Sponsor:__** {result['server']['sponsor']}
**__Latency:__** {result['server']['latency']}  
**__Ping:__** {result['ping']}"""
    msg = await Client.send_photo(
        chat_id=message.chat.id, photo=path, caption=output
    )
    os.remove(path)
    await m.delete()
