from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from config import logger

main_menu_keyboard = [
    [KeyboardButton("Device Info"), KeyboardButton("Add Device")],
    [KeyboardButton("Delete Device")],
    [KeyboardButton("Login"), KeyboardButton("Logout")]
]
main_menu_markup = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"/start by {update.effective_user.id} ({update.effective_user.username})")
    await update.message.reply_text(
        "👋 Welcome to the MDM Bot.\n\n"
        "Choose an action below, or use a command.",
        reply_markup=main_menu_markup
    )


async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"/login by {update.effective_user.id} ({update.effective_user.username})")
    try:
        api_login()
        await update.message.reply_text("✅ Logged in to MDM panel successfully.")
        logger.info("MDM login successful.")
    except Exception as e:
        logger.exception("MDM login failed.")
        await update.message.reply_text(f"❌ Login failed: {e}")

async def logout_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"/logout by {update.effective_user.id} ({update.effective_user.username})")
    logout()
    await update.message.reply_text("🔒 Logged out and cleared session.")
