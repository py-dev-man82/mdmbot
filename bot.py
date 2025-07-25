from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)
from config import TELEGRAM_BOT_TOKEN, logger
from handlers.basic import start, login, logout_cmd
from handlers.device import device_cmd, device_conv
from handlers.adddevice import adddevice_cmd, adddevice_conv
from handlers.deldevice import deldevice_cmd, deldevice_conv

def main():
    logger.info("Starting MDM Bot...")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Basic commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("login", login))
    app.add_handler(CommandHandler("logout", logout_cmd))

    # --- Device Info ---
    # Button entry
    app.add_handler(MessageHandler(filters.Regex("^Device Info$"), device_cmd))
    # Slash command entry (conversation)
    app.add_handler(device_conv)

    # --- Add Device ---
    app.add_handler(MessageHandler(filters.Regex("^Add Device$"), adddevice_cmd))
    app.add_handler(adddevice_conv)

    # --- Delete Device ---
    app.add_handler(MessageHandler(filters.Regex("^Delete Device$"), deldevice_cmd))
    app.add_handler(deldevice_conv)

    # Optional: fallback for unknown commands or menu redisplay
    async def unknown(update, context):
        await update.message.reply_text("❓ Unknown command. Please use /start or select from the menu.")

    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    logger.info("Bot is running. Waiting for updates...")
    app.run_polling()

if __name__ == "__main__":
    main()
