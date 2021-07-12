import time
import datetime
from datetime import datetime, timedelta
from io import BytesIO
from urllib.request import urlopen

import praw
import pytz
import requests
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
bot_token = ""  # BOT Token
app = Client("meme", bot_token=bot_token)

# Credenziali
client_id = ""
client_secret = ""
user_agent = ""
username = ""
password = ""

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent, username=username, password=password)

subreddit = ""  # Da dove prendere i meme
# scritto in 30 mins btw
admins = []  # Lista Admins
channelid =   # ID del canale automatico
imagepath = ""
activated = False

delay = 300 # Intervallo tra i post (secondi)


@app.on_message(filters.command("start", "/") & filters.user(admins))
def start(Client, message):
    global activated
    text = "<b>🦈 SharkMemes Panel</b>\n\n" \
           f"<b>🔄 Activated:</b> <code>"

    if activated:
        app.send_message(message.chat.id, f"{text}{activated}</code>\n\n<b>⏹ To deactivate digit /deactivate</b>", reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🦈 SharkMemes", url="t.me/SharkMemes")]]))
    else:
        app.send_message(message.chat.id, f"{text}{activated}</code>\n\n<b>▶️ To activate digit /activate</b>", reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🦈 SharkMemes", url="t.me/SharkMemes")]]))


@app.on_message(filters.command("activate", "/") & filters.user(admins))
def activate(Client, message):
    global subreddit, activated
    if activated:
        text = "<b>❌ BOT Activated</b>\n\n" \
               "<b>▶️ The BOT is already activated</b>\n\n" \
               "<b>⏹ To deactivate digit /deactivate</b>\n\n" \
               "<b>🏠 Digit /start to return to the panel</b>"

        app.send_message(message.chat.id, text, reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🦈 SharkMemes", url="t.me/SharkMemes")]]))
    else:
        activated = True
        timenow = datetime.now(pytz.timezone("Europe/Rome"))
        stimatetime = datetime.now(pytz.timezone("Europe/Rome"))
        stimatetime += timedelta(seconds=delay)
        text = "<b>▶️ BOT Activated</b>\n\n" \
               "<b>🕰 Estimated start time:</b> <code>" + str(stimatetime.strftime("%X")) + "</code>\n\n" \
               "<b>⏹ To deactivate digit /deactivate</b>\n\n" \
               "<b>🏠 Digit /start to return to the panel</b>"

        app.send_message(message.chat.id, text, reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🦈 SharkMemes", url="t.me/SharkMemes")]]))

        while True:
            if activated:
                try:
                    sr = reddit.subreddit(subreddit)
                    init_time = datetime.now()
                    # Cerca nuovi post nel subreddit
                    for submission in sr.stream.submissions():
                        if activated:
                            link = submission.url
                            post_time = datetime.fromtimestamp(submission.created_utc)

                            image_formats = ("image/png", "image/jpeg", "image/jpg")
                            site = urlopen(link)
                            meta = site.info()

                            # Controlla se è un immagine e se il post è nuovo
                            if meta["content-type"] in image_formats and post_time > init_time:

                                # Opacità
                                opacity = 65

                                response = requests.get(link)
                                memeimg = Image.open(BytesIO(response.content))
                                watermark = Image.open(imagepath + "watermark.png")

                                # Grandezza
                                size = (memeimg.width // 4, memeimg.height // 4)

                                watermark.thumbnail(size)

                                # Posizione Watermark
                                area = memeimg.width - watermark.width, memeimg.height - watermark.width

                                if watermark.mode != 'RGBA':
                                    alpha = Image.new('L', size, 255)
                                    watermark.putalpha(alpha)

                                paste_mask = watermark.split()[3].point(lambda i: i * opacity / 100.)
                                memeimg.paste(watermark, area, mask=paste_mask)
                                memeimg.save(imagepath + "meme.png")

                                time.sleep(delay)  # Aspetta prima di postare
                                app.send_photo(channelid, imagepath + "meme.png", caption="@SharkMemes 🦈", disable_notification=True)
                        else:
                            break
                except:
                    pass
            else:
                break


@app.on_message(filters.command("deactivate", "/") & filters.user(admins))
def deactivate(Client, message):
    global activated
    if activated:
        activated = False
        text = "<b>⏹ BOT Deactivated</b>\n\n" \
               "<b>▶️ To activate digit /activate</b>\n\n" \
               "<b>🏠 Digit /start to return to the panel</b>"

        app.send_message(message.chat.id, text, reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🦈 SharkMemes", url="t.me/SharkMemes")]]))
    else:
        text = "<b>❌ BOT Deactivated</b>\n\n" \
               "<b>⏹ The BOT is already deactivated</b>\n\n" \
               "<b>▶️ To activate digit /activate</b>\n\n" \
               "<b>🏠 Digit /start to return to the panel</b>"

        app.send_message(message.chat.id, text, reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🦈 SharkMemes", url="t.me/SharkMemes")]]))


app.run()
