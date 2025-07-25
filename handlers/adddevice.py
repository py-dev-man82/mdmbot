from telegram import Update, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from config import logger
from mdm_api import add_device

# Conversation state
ASK_NAME, CONFIRM = range(2)

async def adddevice_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Add Device started by {update.effective_user.id} ({update.effective_user.username})")
    await update.message.reply_text(
        "📝 Enter device name (this will also be used as IMEI):",
        reply_markup=ForceReply(selective=True)
    )
    return ASK_NAME

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name_imei = update.message.text.strip()
    context.user_data["adddevice_value"] = name_imei
    logger.info(f"Device name/IMEI entered: {name_imei}")

    review_msg = (
        f"📝 <b>Review New Device</b>\n"
        f"Name: <code>{name_imei}</code>\n"
        f"IMEI: <code>{name_imei}</code>\n\n"
        f"Add this device?"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Yes, Add", callback_data="adddevice_yes"),
         InlineKeyboardButton("❌ Cancel", callback_data="adddevice_cancel")]
    ])
    await update.message.reply_text(review_msg, parse_mode="HTML", reply_markup=buttons)
    return CONFIRM

async def do_add_device(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data
    user = query.from_user

    if action == "adddevice_yes":
        name_imei = context.user_data.get("adddevice_value")
        logger.info(f"Creating device with Name/IMEI={name_imei}")

        try:
            payload = {
                "deviceName": name_imei,
                "imei": name_imei
            }
            result = add_device(payload)
            await query.edit_message_text(f"✅ Device added successfully! Device ID: <code>{result.get('id','-')}</code>", parse_mode="HTML")
            logger.info(f"Device added successfully: {result}")
        except Exception as e:
            logger.exception("Device add failed.")
            await query.edit_message_text(f"❌ Failed to add device: {e}")
    else:
        await query.edit_message_text("❌ Add device cancelled.")
        logger.info(f"Device add cancelled by {user.id}")
    return ConversationHandler.END

adddevice_conv = ConversationHandler(
    entry_points=[
        CommandHandler("adddevice", adddevice_cmd),
        MessageHandler(filters.Regex("^Add Device$"), adddevice_cmd)
    ],
    states={
        ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm)],
        CONFIRM: [CallbackQueryHandler(do_add_device)],
    },
    fallbacks=[],
)
