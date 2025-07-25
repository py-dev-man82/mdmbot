from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from config import logger
from mdm_api import get_device_info

# States for conversation
ASK_DEVICE_ID, SHOW_RESULT = range(2)

async def device_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Device info requested by {update.effective_user.id} ({update.effective_user.username})")
    await update.message.reply_text(
        "🔍 Enter the Device ID or IMEI:",
        reply_markup=ForceReply(selective=True)
    )
    return ASK_DEVICE_ID

async def fetch_and_show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    device_id = update.message.text.strip()
    logger.info(f"Device info lookup for: {device_id}")

    try:
        device = get_device_info(device_id)
        if not device:
            await update.message.reply_text("❌ Device not found.")
            return ConversationHandler.END

        text = (
            f"<b>Device Info</b>\n"
            f"Name: <b>{device.get('name','-')}</b>\n"
            f"ID: <code>{device.get('id','-')}</code>\n"
            f"IMEI: <code>{device.get('imei','-')}</code>\n"
            f"Model: <code>{device.get('model','-')}</code>\n"
            f"Last Seen: <code>{device.get('lastUpdateTime','-')}</code>\n"
            f"Status: <code>{device.get('status','-')}</code>\n"
        )

        await update.message.reply_text(
            text, parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Lookup Another", callback_data="device_again")]
            ])
        )
        return SHOW_RESULT
    except Exception as e:
        logger.exception("Device info fetch failed.")
        await update.message.reply_text(f"❌ Error fetching device info: {e}")
        return ConversationHandler.END

async def device_again_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🔍 Enter the Device ID or IMEI:",
        reply_markup=ForceReply(selective=True)
    )
    return ASK_DEVICE_ID

device_conv = ConversationHandler(
    entry_points=[
        CommandHandler("device", device_cmd),
        MessageHandler(filters.Regex("^Device Info$"), device_cmd)
    ],
    states={
        ASK_DEVICE_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, fetch_and_show)],
        SHOW_RESULT: [CallbackQueryHandler(device_again_cb, pattern="device_again")],
    },
    fallbacks=[],
)
