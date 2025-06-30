# Copyright @ISmartDevs
# Channel t.me/TheSmartDev
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode
from config import UPDATE_CHANNEL_URL, COMMAND_PREFIX

def setup_start_handler(app: Client):
    @app.on_message(filters.command(["start"], prefixes=COMMAND_PREFIX) & filters.private)
    async def start_command(client: Client, message: Message):
        user = message.from_user
        full_name = f"{user.first_name} {user.last_name}" if user and user.last_name else user.first_name if user else "User"

        welcome_message = (
            f"<b>Hi {full_name}! Welcome to this bot</b>\n"
            f"<b>━━━━━━━━━━━━━━━━━━━━━━</b>\n"
            f" <b>SmartCC-Gen</b> is your ultimate toolkit on Telegram, packed with CC generators, educational resources, downloaders, temp mail, crypto utilities, and more. Simplify your tasks with cardin ease!\n"
            f"<b>━━━━━━━━━━━━━━━━━━━━━━</b>\n"
            f"<b>Don't forget to <a href=\"{UPDATE_CHANNEL_URL}\">JoinNow</a> for updates!</b>"
        )

        await client.send_message(
            chat_id=message.chat.id,
            text=welcome_message,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Updates Channel", url=UPDATE_CHANNEL_URL)]
            ])
        )