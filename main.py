
from pyrogram import Client, filters
from pyrogram.types import Message
import os, json, datetime, re
from vars import API_ID, API_HASH, BOT_TOKEN, ADMIN_ID, PRICE, DAYS, WATERMARK_TAG
import yt_dlp
from pyrogram import Client
from flask import Flask
app = Flask(__name__)

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

def load_users():
    try:
        with open("user_db.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open("user_db.json", "w") as f:
        json.dump(data, f, indent=2)

def is_valid_url(text):
    return text.startswith("http://") or text.startswith("https://")

@bot.on_message(filters.command("start"))
async def start(_, m: Message):
    await m.reply("""🔥 Warrior Uploader Bot

Send a .txt file with Classplus video links.
Bot will auto-download and send you the videos (Premium only).""")

@bot.on_message(filters.command("profile"))
async def profile(_, m: Message):
    users = load_users()
    uid = str(m.from_user.id)
    if uid in users:
        exp = users[uid]["expires"]
        await m.reply(f"""👤 Your Profile:

🆔 User ID: {uid}
💼 Status: Premium
⏳ Expires: {exp}""")
    else:
        await m.reply("""🆔 User ID: {}
💼 Status: Free User
⛔ No active premium plan.""".format(uid))

@bot.on_message(filters.command("redeem"))
async def redeem(_, m: Message):
    try:
        code = m.text.split()[1]
    except:
        return await m.reply("❌ Use: /redeem <code>")
    users = load_users()
    uid = str(m.from_user.id)
    with open("redeem_codes.json", "r") as f:
        codes = json.load(f)
    if code in codes and not codes[code]["used"]:
        exp = (datetime.datetime.now() + datetime.timedelta(days=DAYS)).strftime("%d %b %Y")
        users[uid] = {"expires": exp}
        codes[code]["used"] = True
        with open("user_db.json", "w") as f1:
            json.dump(users, f1, indent=2)
        with open("redeem_codes.json", "w") as f2:
            json.dump(codes, f2, indent=2)
        await m.reply(f"""✅ Code Applied: {code}
🎉 Premium Unlocked till {exp}""")
    else:
        await m.reply("❌ Invalid or already used redeem code.")

@bot.on_message(filters.document)
async def handle_txt(_, m: Message):
    users = load_users()
    uid = str(m.from_user.id)
    if uid not in users:
        return await m.reply("""⛔ You need Premium to use this feature.
Use /redeem <code>""")

    doc = m.document
    if not doc.file_name.endswith(".txt"):
        return

    downloaded = await m.download()
    with open(downloaded, "r") as f:
        links = [line.strip() for line in f if is_valid_url(line.strip())]

    if not links:
        return await m.reply("❌ No valid links found in the .txt file.")

    os.makedirs("downloads", exist_ok=True)

    for i, link in enumerate(links[:3]):  # Limit to 3 for speed
        try:
            ydl_opts = {
                "outtmpl": f"downloads/video_{i}{WATERMARK_TAG}.mp4",
                "quiet": True,
                "merge_output_format": "mp4",
                }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            await m.reply_video(f"downloads/video_{i}{WATERMARK_TAG}.mp4", caption="✅ Downloaded with Warrior Watermark")
        except Exception as e:
            await m.reply(f"❌ Failed to download link {i+1}: {e}")
            
from flask import Flask
import threading

app = Flask(__name__)

# 1. Yahan root endpoint paste karein
@app.route("/", methods=["GET", "HEAD"])
def index():
    return "Bot Service Running!", 200

# ... aapke dusre Flask ya bot ke functions ...

def run_flask():
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def run_bot():
    # Yahan aapka bot start hone wala code
    pass  # Replace with your actual bot start code

# 2. Program ke end/main par ye paste karein
if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start() 
    bot.run()
