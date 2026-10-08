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
            f"🌸 𝐍𝐄𝐖 𝐔𝐒𝐄𝐑 𝐂𝐀𝐏𝐓𝐔𝐑𝐄𝐃 - 𝐀𝐈𝐙𝐀 𝐁𝐎𝐓 🌸\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🤖 𝑩𝒐𝒕 𝑵𝒂𝒎𝒆: {BOT_NAME}\n"
            f"👑 𝑩𝒓𝒂𝒏𝒅: {BRAND_NAME}\n"
            f"🆔 𝑼𝒔𝒆𝒓 𝑰𝑫: {user_id}\n"
            f"👤 𝑼𝒔𝒆𝒓𝒏𝒂𝓶𝓮: {username}\n"
            f"📛 𝑵𝒂𝓶𝒆: {full_name}\n"
            f"📢 𝑪𝒉𝒂𝒏𝒏𝓮𝓵: {channel_name}\n"
            f"📊 𝑻𝒐𝒕𝒂𝒍 𝑹𝒆𝒒𝒖𝒆𝒔𝒕𝒔: #{req_number}\n"
            f"🕐 𝑻𝒊𝓶𝒆: {current_time}\n"
            f"📱 𝑺𝒐𝒖𝒓𝒄𝒆: {source_action}\n"
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

# First Post (Join Request ke liye - Stylish Text)
async def send_first_post(chat_id, user, context):
    try:
        user_first_name = user.first_name or "Dear"
        caption_text_1 = (
            f"✨ 𝖂𝑬𝑳𝑪𝑶𝑴𝑬 𝑻𝑶 𝑨𝑰𝒁𝑨 𝑸𝑼𝑶𝑻𝑬𝑿 𝗧𝗥𝗔𝗗𝗘𝗥 (𝗔𝗤𝗧) ♥️ ✨\n\n"
            f"🎀 𝙷𝚎𝚕𝚕𝚘, {user_first_name}! 🌸 𝓐𝓪𝓹𝓴𝓲 𝓳𝓸𝓲𝓷 𝓻𝓮𝓺𝓾𝓮𝓼𝓽 𝓼𝓾𝓬𝓬𝓮𝓼𝓼𝓯𝓾𝓵𝓵𝔂 𝓶𝓲𝓵 𝓬𝓱𝓾𝓴𝓲 𝓱𝓪𝓲. 𝓐𝓪𝓹𝓴𝓪 𝔂𝓪𝓱𝓪𝓷 𝓼𝔀𝓪𝓰𝓪𝓽 𝓱𝓪𝓲 𝓮𝓴 𝓶𝓸𝓼𝓽 𝓹𝓻𝓸𝓯𝓲𝓽𝓪𝓫𝓵𝓮 𝓪𝓾𝓻 𝓼𝓪𝓯𝓮 𝓽𝓻𝓪𝓭𝓲𝓷𝓰 𝓼𝓪𝓯𝓪𝓻 𝓶𝓮𝓲𝓷!\n\n"
            f"💫 𝑾𝑯𝑨𝑻 𝒀𝑶𝑼 𝑾𝑰𝑳𝑳 𝑮𝑬𝑻 𝑯𝑬𝑹𝑬:\n"
            f"🌸 100% High Accuracy Sure-Shot Signals 📊\n"
            f"🌸 Smart Market Analysis & Safe Setups 🎯\n"
            f"🌸 Friendly Guidance & Special Care 💕\n\n"
            f"👇 𝓝𝓮𝓮𝓬𝓱𝓮 𝓭𝓲𝔂𝓮 𝓰𝓪𝔂𝓮 𝓫𝓾𝓽𝓽𝓸𝓷 𝓹𝓪𝓻 𝓬𝓵𝓲𝓬𝓴 𝓴𝓪𝓻𝓴𝓮 𝓯𝓸𝓻𝓪𝓷 𝓱𝓪𝓶𝓪𝓻𝓪 𝓸𝓯𝓯𝓲𝓬𝓲𝓪𝓵 𝓬𝓱𝓪𝓷𝓷𝓮𝓵 𝓳𝓸𝓲𝓷 𝓴𝓪𝓻𝓮𝓲𝓷:\n\n"
            f"🔗 {CHANNEL_LINK}\n"
            f"🔗 {CHANNEL_LINK}\n"
            f"🔗 {CHANNEL_LINK}\n\n"
            f"✨ 𝑨𝒊𝒛𝒂 𝗤𝘂𝗼𝘁𝗲𝗫 𝗧𝗿𝗮𝗱𝗲𝗿 — 𝑾𝒉𝒆𝒓𝒆 𝑷𝒓𝒐𝒇𝒊𝖙 𝒎𝒆𝒆𝒕𝖘 𝗘𝗹𝗲𝗴𝗮𝗻𝗰𝗲 💖"
        )
        
        keyboard_1 = [
            [InlineKeyboardButton("🌸 𝙹𝙾𝙸𝙽 𝙾𝙵𝙵𝙸𝙲𝙸𝙰𝙻 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 🌸", url=CHANNEL_LINK)]
        ]
        
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=PHOTO_URL,
            caption=caption_text_1,
            reply_markup=InlineKeyboardMarkup(keyboard_1)
        )
    except Exception as e:
        print(f"First post error: {e}")

# Second Post (/start command ke liye - Stylish Text)
async def send_both_posts(chat_id, user, context):
    await send_first_post(chat_id, user, context)
    await asyncio.sleep(1)

    try:
        caption_text_2 = (
            "💖 𝑽𝑰𝑷 𝑹𝑬𝑪𝑶𝑽𝑬𝑹𝒀 & 𝑬𝗫𝗖𝗟𝗨𝗦𝗜𝗩𝗘 𝗭𝗢𝗡𝗘 💖\n\n"
            "🌷 𝓟𝓾𝓻𝓪𝓷𝓮 𝓵𝓸𝓼𝓼𝓮𝓼 𝓴𝓲 𝓯𝓲𝓴𝓪𝓻 𝓴𝓪𝓻𝓷𝓪 𝓫𝓲𝓵𝓴𝓾𝓵 𝓬𝓱𝓱𝓸𝓭𝓮𝓲𝓷! 𝓐𝓪𝓲𝔂𝓮 𝓱𝓪𝓶𝓪𝓻𝓮 𝓼𝓪𝓽𝓱 𝓮𝔁𝓬𝓵𝓾𝓼𝓲𝓿𝓮 𝖁𝕴𝕻 𝓽𝓻𝓪𝓭𝓲𝓷𝓰 𝓼𝓮𝓼𝓼𝓲𝓸𝓷𝓼 𝓶𝓮𝓲𝓷 𝓳𝓸𝓲𝓷 𝓴𝓪𝓻𝓮𝓲𝓷 𝓪𝓾𝓻 𝓪𝓹𝓷𝓮 𝓹𝓸𝓻𝓽𝓯𝓸𝓵𝓲𝓸 𝓴𝓸 𝓮𝓴 𝓴𝓱𝓾𝓫𝓼𝓾𝓻𝓪𝓽 𝓹𝓻𝓸𝓯𝓲𝓽 𝓶𝓮𝓲𝓷 𝓫𝓪𝓭𝓵𝓮𝓲𝓷.\n\n"
            "✨ 𝑾𝑯𝒀 𝗖𝗛𝗢𝗢𝗦𝗘 𝗨𝗦?\n"
            "🌷 Daily Safe & High-Profit Sessions 📈\n"
            "🌷 Special Mentorship & Personal Guidance 💎\n"
            "🌷 Exciting Gifts & Rewards for Active Members 🎁\n\n"
            "🎀 𝗦𝗧𝗘𝗣 𝟭: 𝓐𝓹𝓷𝓪 𝓷𝓪𝔂𝓪 𝓽𝓻𝓪𝓭𝓲𝓷𝓰 𝓪𝓬𝓬𝓸𝓾𝓷𝓽 𝔂𝓪𝓱𝓪𝓷 𝓼𝓮 𝓬𝓻𝓮𝓪𝓽𝓮 𝓴𝓪𝓻𝓮𝓲𝓷:\n"
            f"🔗 {QUOTEX_LINK}\n\n"
            "🎀 𝗦𝗧𝗘𝗣 𝟮: 𝓓𝓮𝓹𝓸𝓼𝓲𝓽 𝓴𝓪𝓻𝓷𝓮 𝓴𝓮 𝓫𝓪𝓪𝓭 𝓪𝓹𝓷𝓲 𝓣𝓻𝓪𝓭𝓮𝓻 𝓘𝓓 𝓯𝓸𝓻𝓪𝓷 𝓶𝓾𝓳𝓱𝓮 𝓓𝓜 𝓴𝓪𝓻𝓮𝓲𝓷 𝓽𝓪𝓪𝓴𝓮 𝓪𝓪𝓹𝓴𝓸 𝖁𝕴𝕻 𝓬𝓱𝓪𝓷𝓷𝓮𝓵 𝓴𝓲 𝓪𝓬𝓬𝓮𝓼𝓼 𝓶𝓲𝓵 𝓳𝓪𝔂𝓮!\n"
            f"👉 𝗗𝗠 𝗢𝗪𝗡𝗘𝗥: {OWNER_USERNAME} 👈\n\n"
            "🌟 𝑳𝒊𝒎𝒊𝒕𝒆𝒅 𝑺𝒍𝒐𝒕𝒔 — 𝑱𝒐𝒊𝒏 𝗡𝗼𝘄 & 𝗦𝘁𝗮𝗿𝘁 𝑾𝒊𝒏𝒏𝒊𝒏𝒈! 💕"
        )
        
        keyboard_2 = [
            [InlineKeyboardButton("🌸 𝗖𝗥𝗘𝗔𝗧𝗘 𝗤𝗨𝗢𝗧𝗘𝗫 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 🌸", url=QUOTEX_LINK)],
            [InlineKeyboardButton("👑 𝗖𝗢𝗡𝗧𝗔𝗖𝗧 𝗔𝗜𝗭𝗔 𝗢𝗪𝗡𝗘𝗥 👑", url=f"https://t.me/{OWNER_USERNAME.lstrip('@')}")]
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

    print(f"{BOT_NAME} ({BOT_USERNAME}) is running successfully...")
    application.run_polling()

if __name__ == '__main__':
    main()
