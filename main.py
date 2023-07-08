from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import ChatPermissions
import time
from time import sleep
import random
import datetime
import asyncio
import spotipy
import spotipy.util as util

# Spotify Settings
CLIENT_ID = 'YOUR_SPOT_CLIENT_ID'

CLIENT_SECRET = 'YOUR_SPOT_CLIENT_SECRET'

username = "YourUsername"
scope = "user-read-currently-playing"
redirect_uri = "http://localhost:8888/callback"

token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, redirect_uri)
sp = spotipy.Spotify(auth=token)

# Telegram Settings
api_id = 'TG_API_ID'
api_hash = 'TG_API_HASH'

app = Client("my_account", api_id=api_id, api_hash=api_hash)

track = sp.current_user_playing_track()

upd_spot = False
user_bio = "Задай био командой .setbio"

@app.on_message(filters.command("setbio", prefixes=".") & filters.me)
async def set_bio(client, message):
    global upd_spot, user_bio
    user_bio = f"{message.text[8:]}"
    await message.edit(f"✅Задал био: {message.text[8:]}. Он появится после остановки трекинга Spotify или когда ничего не будет играть.")
    

@app.on_message(filters.command("stop_spotify", prefixes=".") & filters.me)
async def stop_spot(client, message):
    global upd_spot, user_bio
    if upd_spot:
        await message.edit("✅Закончил трекинг Spotify!")
        await app.update_profile(bio=user_bio)
        upd_spot = False
    else:
        await message.edit("Сейчас трекинг Spotify выключен")

@app.on_message(filters.command("spotify", prefixes=".") & filters.me)
async def set_name(client, message):
    global upd_spot, user_bio
    if upd_spot:
        await message.edit("Сейчас трекинг Spotify включен")
    else:
        await message.edit("✅Начал трекинг Spotify!")
        upd_spot = True
        t = sp.current_user_playing_track()
        if t == None:
            await app.update_profile(bio=user_bio)
        else:
            tname = t['item']['name']
            tartist = t['item']['artists'][0]['name']
            sname = tname
            await app.update_profile(bio=f"🎧 Spotify | {tartist} - {tname}")
        while upd_spot:
            t = sp.current_user_playing_track()
            if t == None:
                await asyncio.sleep(0.5)
                await app.update_profile(bio=user_bio)
            else:
                tname = t['item']['name']
                tartist = t['item']['artists'][0]['name']
                if sname != tname:
                    await app.update_profile(bio=f"🎧 Spotify | {tartist} - {tname}")
                    sname = tname
                else:
                    await asyncio.sleep(0.5)


app.run()
