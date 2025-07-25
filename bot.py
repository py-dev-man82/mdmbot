from telegram.ext import ApplicationBuilder, CommandHandler
from config import TELEGRAM_BOT_TOKEN, logger
from handlers.basic import start, login, logout_cmd

def main():
    logger.info("Starting MDM Bot...")
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("login", login))
    app.add_handler(CommandHandler("logout", logout_cmd))
    # Other handlers will be added here as you build

    app.run_polling()

if __name__ == "__main__":
    main()
