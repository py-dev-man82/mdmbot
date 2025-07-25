from telegram import Update
from telegram.ext import ContextTypes
from handlers.basic import login, logout_cmd, start
from handlers.device import device_cmd
from handlers.adddevice import adddevice_cmd
from handlers.deldevice import deldevice_cmd
from config import logger

async def menu_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    logger.info(f"[MenuButton] User {user.id} pressed button: {text}")

    if text == "Device Info":
        return await device_cmd(update, context)
    elif text == "Add Device":
        return await adddevice_cmd(update, context)
    elif text == "Delete Device":
        return await deldevice_cmd(update, context)
    elif text == "Login":
        return await login(update, context)
    elif text == "Logout":
        return await logout_cmd(update, context)
    else:
        await update.message.reply_text("❓ Unknown menu option. Please use the buttons or commands.")
        return
