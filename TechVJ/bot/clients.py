import sys
import glob
import importlib
from pathlib import Path
from pyrogram import idle
import logging
import logging.config
import asyncio
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import LOG_CHANNEL, ON_HEROKU, CLONE_MODE, PORT, FORCE_SUB_CHANNEL1, FORCE_SUB_CHANNEL2, FORCE_SUB_CHANNEL3, FORCE_SUB_CHANNEL4
from typing import Union, Optional, AsyncGenerator
from pyrogram import types
from Script import script 
from datetime import date, datetime 
import pytz
from aiohttp import web
from TechVJ.server import web_server
from plugins.clone import restart_bots
from TechVJ.bot import StreamBot
from TechVJ.utils.keepalive import ping_server
from TechVJ.bot.clients import initialize_clients

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

ppath = "plugins/*.py"
files = glob.glob(ppath)
StreamBot.start()
loop = asyncio.get_event_loop()

async def start():
    print('\n')
    print('Initalizing Tech VJ Bot')
    bot_info = await StreamBot.get_me()
    StreamBot.username = bot_info.username
    await initialize_clients()
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"plugins/{plugin_name}.py")
            import_path = "plugins.{}".format(plugin_name)
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules["plugins." + plugin_name] = load
            print("Tech VJ Imported => " + plugin_name)
    if ON_HEROKU:
        asyncio.create_task(ping_server())
    me = await StreamBot.get_me()
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time = now.strftime("%H:%M:%S %p")
    app = web.AppRunner(await web_server())
    await StreamBot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()
    if CLONE_MODE == True:
        await restart_bots()
    print("Bot Started Powered By @VJ_Botz")
    await idle()

    if FORCE_SUB_CHANNEL1:
        try:
            link = (await StreamBot.get_chat(FORCE_SUB_CHANNEL1)).invite_link
            if not link:
                await StreamBot.export_chat_invite_link(FORCE_SUB_CHANNEL1)
                link = (await StreamBot.get_chat(FORCE_SUB_CHANNEL1)).invite_link
            StreamBot.invitelink1 = link
        except Exception as a:
            logging.warning(a)
            logging.warning("Bot can't Export Invite link from Force Sub Channel!")
            logging.warning(f"Please Double check the FORCE_SUB_CHANNEL1 value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL1}")
            logging.info("\nBot Stopped. https://t.me/weebs_support for support")
            sys.exit()
    if FORCE_SUB_CHANNEL2:
        try:
            link = (await StreamBot.get_chat(FORCE_SUB_CHANNEL2)).invite_link
            if not link:
                await StreamBot.export_chat_invite_link(FORCE_SUB_CHANNEL2)
                link = (await StreamBot.get_chat(FORCE_SUB_CHANNEL2)).invite_link
            StreamBot.invitelink2 = link
        except Exception as a:
            logging.warning(a)
            logging.warning("Bot can't Export Invite link from Force Sub Channel!")
            logging.warning(f"Please Double check the FORCE_SUB_CHANNEL2 value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL2}")
            logging.info("\nBot Stopped. https://t.me/weebs_support for support")
            sys.exit()
    if FORCE_SUB_CHANNEL3:
        try:
            link = (await StreamBot.get_chat(FORCE_SUB_CHANNEL3)).invite_link
            if not link:
                await StreamBot.export_chat_invite_link(FORCE_SUB_CHANNEL3)
                link = (await StreamBot.get_chat(FORCE_SUB_CHANNEL3)).invite_link
            StreamBot.invitelink3 = link
        except Exception as a:
            logging.warning(a)
            logging.warning("Bot can't Export Invite link from Force Sub Channel!")
            logging.warning(f"Please Double check the FORCE_SUB_CHANNEL3 value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL3}")
            logging.info("\nBot Stopped. https://t.me/weebs_support for support")
            sys.exit()
    if FORCE_SUB_CHANNEL4:
        try:
            link = (await StreamBot.get_chat(FORCE_SUB_CHANNEL4)).invite_link
            if not link:
                await StreamBot.export_chat_invite_link(FORCE_SUB_CHANNEL4)
                link = (await StreamBot.get_chat(FORCE_SUB_CHANNEL4)).invite_link
            StreamBot.invitelink4 = link
        except Exception as a:
            logging.warning(a)
            logging.warning("Bot can't Export Invite link from Force Sub Channel!")
            logging.warning(f"Please Double check the FORCE_SUB_CHANNEL4 value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL4}")

if __name__ == '__main__':
    try:
        loop.run_until_complete(start())
    except KeyboardInterrupt:
        logging.info('Service Stopped Bye 👋')
