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
            f"📊 𝑻𝒐𝒕𝒂𝒍 𝑹𝒆𝒒𝓾𝓮𝓼𝓽𝒔: #{req_number}\n"
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

# First Post (Join Request ke liye - Bold Serif Fonts)
async def send_first_post(chat_id, user, context):
    try:
        user_first_name = user.first_name or "Dear"
        caption_text_1 = (
            f"✨ 𝑾𝑬𝑳𝑪𝑶𝑴𝑬 𝑻𝑶 𝑨𝑰𝒁𝑨 𝑸𝑼𝑶𝑻𝑬𝗫 𝗧𝗥𝗔𝗗𝗘𝗥 (𝗔𝗤𝗧) ♥️ ✨\n\n"
            f"🎀 𝑯𝒆𝒍𝒍𝒐, {user_first_name}! 🌸 𝐀𝐚𝐩𝐤𝐢 𝐣𝐨𝐢𝐧 𝐫𝐞𝐪𝐮𝐞𝐬𝐭 𝐬𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐦𝐢𝐥 𝐜𝐡𝐮𝐤𝐢 𝐡𝐚𝐢. 𝐀𝐚𝐩𝐤𝐚 𝐲𝐚𝐡𝐚𝐧 𝐬𝐰𝐚𝐠𝐚𝐭 𝐡𝐚𝐢 𝐞𝐤 𝐦𝐨𝐬𝐭 𝐩𝐫𝐨𝐟𝐢𝐭𝐚𝐛𝐥𝐞 𝐚𝐮𝐫 𝐬𝐚𝐟𝐞 𝐭𝐫𝐚𝐝𝐢𝐧𝐠 𝐬𝐚𝐟𝐚𝐫 𝐦𝐞𝐢𝐧!\n\n"
            f"💫 𝑾𝑯𝑨𝑻 𝒀𝑶𝑼 𝑾𝑰𝑳𝑳 𝑮𝑬𝑻 𝑯𝑬𝑹𝑬:\n"
            f"🌸 100% 𝐇𝐢𝐠𝐡 𝐀𝐜𝐜𝐮𝐫𝐚𝐜𝐲 𝐒𝐮𝐫𝐞-𝐒𝐡𝐨𝐭 𝐒𝐢𝐠𝐧𝐚𝐥𝐬 📊\n"
            f"🌸 𝐒𝐦𝐚𝐫𝐭 𝐌𝐚𝐫𝐤𝐞𝐭 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬 & 𝐒𝐚𝐟𝐞 𝐒𝐞𝐭𝐮𝐩𝐬 🎯\n"
            f"🌸 𝐅𝐫𝐢𝐞𝐧𝐝𝐥𝐲 𝐆𝐮𝐢𝐝𝐚𝐧𝐜𝐞 & 𝐒𝐩𝐞𝐜𝐢𝐚𝐥 𝐂𝐚𝐫𝐞 💕\n\n"
            f"👇 𝑵𝒆𝒆𝒄𝒉𝒆 𝒅𝒊𝒚𝒆 𝒈𝒂𝒚𝒆 𝒃𝒖𝒕𝒕𝒐𝒏 𝒑𝒂𝒓 𝒄𝒍𝒊𝒄𝒌 𝒌𝒂𝒓𝒌𝒆 𝒇𝒐𝒓𝒂𝒏 𝒉𝒂𝒎𝒂𝒓𝒂 𝒐𝒇𝒇𝒊𝒄𝒊𝒂𝒍 𝒄𝒉𝒂𝒏𝒏𝒆𝒍 𝒋𝒐𝒊𝒏 𝒌𝒂𝒓𝒆𝒊𝚗:\n\n"
            f"🔗 {CHANNEL_LINK}\n"
            f"🔗 {CHANNEL_LINK}\n"
            f"🔗 {CHANNEL_LINK}\n\n"
            f"✨ 𝑨𝒊𝒛𝒂 𝗤𝘂𝗼𝘁𝗲𝗫 𝗧𝗿𝗮𝗱𝗲𝗿 — 𝑾𝒉𝒆𝒓𝒆 𝑷𝒓𝒐𝒇𝒊𝖙 𝒎𝒆𝒆𝒕𝖘 𝗘𝗹𝗲𝗴𝗮𝗻𝗰𝗲 💖"
        )
        
        keyboard_1 = [
            [InlineKeyboardButton("🌸 𝙹𝙾𝙸𝙽 𝙰𝙸𝚉𝙰 𝙾𝙵𝙵𝙸𝙲𝙸𝙰𝙻 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 🌸", url=CHANNEL_LINK)]
        ]
        
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=PHOTO_URL,
            caption=caption_text_1,
            reply_markup=InlineKeyboardMarkup(keyboard_1)
        )
    except Exception as e:
        print(f"First post error: {e}")

# Second Post (/start command ke liye - Bold Serif Fonts)
async def send_both_posts(chat_id, user, context):
    await send_first_post(chat_id, user, context)
    await asyncio.sleep(1)

    try:
        caption_text_2 = (
            "💖 𝑽𝑰𝑷 𝑹𝑬𝑪𝑶𝑽𝑬𝑹𝒀 & 𝑬𝗫𝗖𝗟𝗨𝗦𝗜𝗩𝗘 𝗭𝗢𝗡𝗘 💖\n\n"
            "🌷 𝑷𝒖𝒓𝒂𝒏𝒆 𝒍𝒐𝒔𝒔𝒆𝒔 𝒌𝒊 𝒇𝒊𝒌𝒂𝒓 𝒌𝒂𝒓𝒏𝒂 𝒃𝒊𝒍𝒌𝒖𝒍 𝒄𝒉𝒉𝒐𝒅𝒆𝒊𝒏! 𝑨𝒂𝒊𝒚𝒆 𝒉𝒂𝒎𝒂𝒓𝒆 𝒔𝒂𝒕𝒉 𝒆𝒙𝒄𝒍𝒖𝒔𝒊𝒗𝒆 𝑽𝑰𝑷 𝒕𝒓𝒂𝒅𝒊𝒏𝒈 𝒔𝒆𝒔𝒔𝒊𝒐𝒏𝒔 𝒎𝒆𝒊𝒏 𝒋𝒐𝒊𝒏 𝒌𝒂𝒓𝒆𝒊𝒏 𝒂𝒖𝒓 𝒂𝒑𝒏𝒆 𝒑𝒐𝒓𝒕𝒇𝒐𝒍𝒊𝒐 𝒌𝒐 𝒆𝒌 𝒌𝒉𝒖𝒃𝒔𝒖𝒓𝒂𝒕 𝒑𝒓𝒐𝒇𝒊𝒕 𝒎𝒆𝒊𝒏 𝒃𝒂𝒅𝒍𝒆𝒊𝒏.\n\n"
            "✨ 𝑾𝑯𝒀 𝗖𝗛𝗢𝗢𝗦𝗘 𝗨𝗦?\n"
            "🌷 𝐃𝐚𝐢𝐥𝐲 𝐒𝐚𝐟𝐞 & 𝐇𝐢𝐠𝐡-𝐏𝐫𝐨𝐟𝐢𝐭 𝐒𝐞𝐬𝐬𝐢𝐨𝐧𝐬 📈\n"
            "🌷 𝐒𝐩𝐞𝐜𝐢𝐚𝐥 𝐌𝐞𝐧𝐭𝐨𝐫𝐬𝐡𝐢𝐩 & 𝐏𝐞𝐫𝐬𝐨𝐧𝐚𝐥 𝐆𝐮𝐢𝐝𝐚𝐧𝐜𝐞 💎\n"
            "🌷 𝐄𝐱𝐜𝐢𝐭𝐢𝐧𝐠 𝐆𝐢𝐟𝐭𝐬 & 𝐑𝐞𝐰𝐚𝐫𝐝𝐬 𝐟𝐨𝐫 𝐀𝐜𝐭𝐢𝐯𝐞 𝐌𝐞𝐦𝐛𝐞𝐫𝐬 🎁\n\n"
            "🎀 𝗦𝗧𝗘𝗣 𝟭: 𝑨𝒑𝒏𝒂 𝒏𝒂𝒚𝒂 𝒕𝒓𝒂𝒅𝒊𝒏𝒈 𝒂𝒄𝒄𝒐𝒖𝒏𝒕 𝒚𝒂𝒉𝒂𝒏 𝒔𝒆 𝒄𝒓𝒆𝒂𝒕𝒆 𝒌𝒂𝒓𝒆𝒊𝚗:\n"
            f"🔗 {QUOTEX_LINK}\n\n"
            "🎀 𝗦𝗧𝗘𝗣 𝟮: 𝑫𝒆𝒑𝒐𝒔𝒊𝒕 𝒌𝒂𝒓𝒏𝒆 𝒌𝒆 𝒃𝒂𝒂𝚍 𝒂𝒑𝒏𝒊 𝑻𝒓𝒂𝒅𝒆𝒓 𝑰𝑫 𝒇𝒐𝒓𝒂𝒏 𝒎𝒖𝒋𝒉𝒆 𝑫𝑴 𝒌𝒂𝒓𝒆𝒊𝒏 𝒕𝒂𝒂𝒌𝒆 𝒂𝒂𝒑𝒌𝒐 𝑽𝑰𝑷 𝒄𝒉𝒂𝒏𝒏𝒆𝒍 𝒌𝒊 𝒂𝒄𝒄𝒆𝒔𝒔 𝒎𝒊𝒍 𝒋𝒂𝒚𝚎!\n"
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
