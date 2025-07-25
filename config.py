import logging

# MDM API credentials
MDM_API_URL = "https://your-mdm.com/rest"
MDM_USER = "admin"
MDM_PASS = "admin"

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# Debug/logging mode
DEBUG_MODE = True

# Logging config
LOG_LEVEL = logging.DEBUG if DEBUG_MODE else logging.INFO

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("mdm_bot.log", encoding="utf-8")
    ]
)
logger = logging.getLogger("mdm_bot")
