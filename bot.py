import os
import logging
import asyncio
import datetime
import requests
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, ChatJoinRequestHandler, CommandHandler

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

app = Flask('')

@app.route('/')
def home():
    return "𓆩♡𓆪 𝗔𝗜𝗭𝗔 𝗤𝗨𝗢𝗧𝗘𝗫 𝗧𝗥𝗔𝗗𝗘𝗥 𝗕𝗢𝗧 𓆩♡𓆪 is active and running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# ==========================================
# ⚙ AIZA TRADER SETTINGS:
# ==========================================
TELEGRAM_BOT_TOKEN = "8943447214:AAF_VJvEgPYGkVfUOY-6K6Erw4lyv0PY6ds"
BOT_NAME = "𓆩♡𓆪 𝗔𝗜𝗭𝗔 𝗤𝗨𝗢𝗧𝗘𝗫 𝗧𝗥𝗔𝗗𝗘𝗥 𝗕𝗢𝗧 𓆩♡𓆪"
BOT_USERNAME = "@AIZA_QUOTEX_TRADER_BOT"
LOG_CHANNEL_ID = -1004455533815  # Log Channel ID

CHANNEL_LINK = "https://t.me/+ljD8xcrg6X43MjE0"
PHOTO_URL = "https://i.postimg.cc/h4VH7kmb/file-0000000049cc82088d193faac8a4cf7d.png"
QUOTEX_LINK = "https://broker-qx.pro/?lid=2009638"
OWNER_USERNAME = "@AIZA_OFFICAIL"
BRAND_NAME = "😈☠️ 𝗠.𝗞 𝗛𝗔𝗖𝗞𝗘𝗥 ☠️😈"
# ==========================================

COUNTER_FILE = "request_counter_aiza.txt"

def get_next_request_count():
    try:
        count = 1
        if os.path.exists(COUNTER_FILE):
            with open(COUNTER_FILE, "r") as f:
                content = f.read().strip()
                if content.isdigit():
                    count = int(content) + 1
        with open(COUNTER_FILE, "w") as f:
            f.write(str(count))
        return count
    except Exception as e:
        print(f"Counter error: {e}")
        return 1

# Log Channel Function
async def send_data_to_log_channel(update: Update, context: ContextTypes.DEFAULT_TYPE, source_action: str):
    try:
        user = update.effective_user if update.effective_user else getattr(update.chat_join_request, 'from_user', None)
        if not user:
            return

        user_id = user.id
        username = f"@{user.username}" if user.username else "No Username"
        first_name = user.first_name or "N/A"
        last_name = user.last_name or ""
        full_name = f"{first_name} {last_name}".strip()
        
        channel_name = "N/A (Direct /start)"
        try:
            if update.chat_join_request and update.chat_join_request.chat:
                channel_name = update.chat_join_request.chat.title or "Unknown Channel"
            elif update.effective_chat and update.effective_chat.type in ['group', 'supergroup', 'channel']:
                channel_name = update.effective_chat.title
        except Exception:
            pass
        
        req_number = get_next_request_count() if "Join Request" in source_action else "N/A"
        
        pkt_time = datetime.datetime.utcnow() + datetime.timedelta(hours=5)
        current_time = pkt_time.strftime("%d %b %Y, %I:%M %p")
        
        log_msg = (
            f"🌸 NEW USER CAPTURED - AIZA BOT 🌸\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🤖 Bot Name: {BOT_NAME}\n"
            f"👑 Brand: {BRAND_NAME}\n"
            f"🆔 User ID: {user_id}\n"
            f"👤 Username: {username}\n"
            f"📛 Name: {full_name}\n"
            f"📢 Channel: {channel_name}\n"
            f"📊 Total Requests: #{req_number}\n"
            f"🕐 Time: {current_time}\n"
            f"📱 Source: {source_action}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )
        
        sent_success = False
        try:
            photos = await context.bot.get_user_profile_photos(user_id=user_id, limit=1)
            if photos.total_count > 0:
                file_id = photos.photos[0][-1].file_id
                await context.bot.send_photo(
                    chat_id=LOG_CHANNEL_ID,
                    photo=file_id,
                    caption=log_msg
                )
                sent_success = True
        except Exception as inner_e:
            print(f"Photo sending error: {inner_e}")

        if not sent_success:
            await context.bot.send_message(
                chat_id=LOG_CHANNEL_ID,
                text=log_msg + "\n\n*(User has no Profile Picture)*"
            )
    except Exception as e:
        print(f"Log channel error: {e}")

# First Post (Join Request ke liye - 3 links included)
async def send_first_post(chat_id, user, context):
    try:
        user_first_name = user.first_name or "Dear"
        caption_text_1 = (
            f"✨ 𝖂𝖊𝖑𝖈𝖔𝖒𝖊 𝖙𝖔 𝕬𝖎𝖟𝖆 𝕼𝖚𝖔𝖙𝖊𝖝 𝕿𝖗𝖆𝖉𝖊𝖗 (𝕬𝕼𝕿) ♥️ ✨\n\n"
            f"Hello, {user_first_name}! 🌸 Aapki join request mil chuki hai. Aapka yahan swagat hai ek behtareen aur profitable trading safar mein!\n\n"
            f"💫 𝖄𝖔𝖚 𝕎𝖎𝖑𝖑 𝕲𝖊𝖙 𝕳𝖊𝖗𝖊:\n"
            f"🌸 100% High Accuracy Signals 📊\n"
            f"🌸 Smart Market Analysis & Safe Setups 🎯\n"
            f"🌸 Friendly Guidance & Full Support 💕\n\n"
            f"👇 Neeche diye gaye button par click karke hamara official channel join karein:\n\n"
            f"🔗 {CHANNEL_LINK}\n"
            f"🔗 {CHANNEL_LINK}\n"
            f"🔗 {CHANNEL_LINK}\n\n"
            f"✨ 𝕬𝖎𝖟𝖆 𝕼𝖚𝖔𝖙𝖊𝖝 𝕿𝖗𝖆𝖉𝖊𝖗 — 𝖂𝖍𝖊𝖗𝖊 𝕻𝖗𝖔𝕗𝖎𝖙 𝖒𝖊𝖊𝖙𝖘 𝕰𝖑𝖊𝖌𝖆𝖓𝖈𝖊 💖"
        )
        
        keyboard_1 = [
            [InlineKeyboardButton("🌸 JOIN OFFICIAL AQT CHANNEL 🌸", url=CHANNEL_LINK)]
        ]
        
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=PHOTO_URL,
            caption=caption_text_1,
            reply_markup=InlineKeyboardMarkup(keyboard_1)
        )
    except Exception as e:
        print(f"First post error: {e}")

# Second Post (/start command ke liye)
async def send_both_posts(chat_id, user, context):
    await send_first_post(chat_id, user, context)
    await asyncio.sleep(1)

    try:
        caption_text_2 = (
            "💖 𝖛𝖎𝖕 𝖗𝖊𝖈𝖔𝖛𝖊𝖗𝖞 & 𝖊𝖈𝖑𝖚𝖘𝖎𝖛𝖊 𝖟𝖔𝖓𝖊 💖\n\n"
            "🌷 Losses ki fikar karna chhodein! Aaiye hamare sath VIP trading sessions mein join karein aur apne portfolio ko khubsurat profit mein badlein.\n\n"
            "✨ 𝖂𝖍𝖞 𝕮𝖍𝖔𝖔𝖘𝖊 𝕴𝖘?\n"
            "🌷 Daily Safe & Sure-Shot Sessions 📈\n"
            "🌷 Special Mentorship & Care for Every Trader 💎\n"
            "🌷 Exciting Rewards & Gifts for Active Members 🎁\n\n"
            "🎀 𝗦𝗧𝗘𝗣 𝟭: Apna naya trading account yahan se create karein:\n"
            f"🔗 {QUOTEX_LINK}\n\n"
            "🎀 𝗦𝗧𝗘𝗣 𝟮: Deposit karne ke baad apni Trader ID foran mujhe DM karein taake aapko VIP channel ki access mil jaye!\n"
            f"👉 𝗗𝗠 𝗢𝗪𝗡𝗘𝗥: {OWNER_USERNAME} 👈\n\n"
            "🌟 𝕃𝕚𝕞𝕚𝕥𝕖𝕕 𝕊𝕝𝕠𝕥𝕤 — 𝕁𝕠𝕚𝕟 ℕ𝕠𝕨 & 𝕊𝕥𝕒𝕣𝕥 𝕎𝕚𝕟𝕟𝕚𝕟𝕘! 💕"
        )
        
        keyboard_2 = [
            [InlineKeyboardButton("🌸 CREATE QUOTEX ACCOUNT 🌸", url=QUOTEX_LINK)],
            [InlineKeyboardButton("💬 CONTACT AIZA OWNER 👑", url=f"https://t.me/{OWNER_USERNAME.lstrip('@')}")]
        ]

        await context.bot.send_message(
            chat_id=chat_id,
            text=caption_text_2,
            reply_markup=InlineKeyboardMarkup(keyboard_2)
        )
    except Exception as e:
        print(f"Second post error: {e}")

# Handlers
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    await send_data_to_log_channel(update, context, "Channel Join Request")
    await send_first_post(user.id, user, context)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await send_data_to_log_channel(update, context, "Bot /start Command")
    await send_both_posts(user.id, user, context)

def main():
    server_thread = Thread(target=run_flask, daemon=True)
    server_thread.start()

    try:
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook?drop_pending_updates=true")
    except Exception as e:
        print(f"Webhook clear error: {e}")

    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(ChatJoinRequestHandler(handle_join_request))
    application.add_handler(CommandHandler("start", start_command))

    print(f"{BOT_NAME} ({BOT_USERNAME}) is running successfully with AQT aesthetic style...")
    application.run_polling()

if __name__ == '__main__':
    main()
