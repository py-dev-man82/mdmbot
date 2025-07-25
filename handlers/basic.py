from telegram import Update
from telegram.ext import ContextTypes
from config import logger
from mdm_api import api_login, logout

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"/start by {update.effective_user.id} ({update.effective_user.username})")
    await update.message.reply_text(
        "👋 Welcome to the MDM Bot.\n\n"
        "Commands:\n"
        "• /login – Log in to MDM\n"
        "• /device – Get device info\n"
        "• /adddevice – Register new device\n"
        "• /deldevice – Wipe & delete device\n"
        "• /logout – Log out"
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
