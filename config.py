import os
from dotenv import load_dotenv
import logging

load_dotenv(dotenv_path=".env")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MDM_API_URL = os.getenv("MDM_API_URL")
MDM_USER = os.getenv("MDM_USER")
MDM_PASS = os.getenv("MDM_PASS")

logger = logging.getLogger("mdm_bot")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
