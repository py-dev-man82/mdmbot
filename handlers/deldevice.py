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
from mdm_api import delete_device

# Conversation states
ASK_DEVICE_ID, CONFIRM = range(2)

async def deldevice_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Delete Device started by {update.effective_user.id} ({update.effective_user.username})")
    await update.message.reply_text(
        "⚠️ Enter the device ID to delete and wipe:",
        reply_markup=ForceReply(selective=True)
    )
    return ASK_DEVICE_ID

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    device_id = update.message.text.strip()
    context.user_data["deldevice_id"] = device_id
    logger.info(f"Device ID to delete: {device_id}")

    review_msg = (
        f"⚠️ <b>Confirm Delete & Wipe</b>\n"
        f"Device ID: <code>{device_id}</code>\n\n"
        f"Are you sure you want to delete and wipe this device?"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Yes, Delete & Wipe", callback_data="deldevice_yes"),
         InlineKeyboardButton("❌ Cancel", callback_data="deldevice_cancel")]
    ])
    await update.message.reply_text(review_msg, parse_mode="HTML", reply_markup=buttons)
    return CONFIRM

async def do_del_device(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data
    user = query.from_user

    if action == "deldevice_yes":
        device_id = context.user_data.get("deldevice_id")
        logger.info(f"Attempting delete & wipe for device: {device_id}")

        try:
            # The delete_device function should send the correct payload for wipe+delete (API must support this!)
            result = delete_device(device_id)
            await query.edit_message_text(
                f"✅ Device deleted and wipe command sent!\n"
                f"Device ID: <code>{device_id}</code>",
                parse_mode="HTML"
            )
            logger.info(f"Device deleted successfully: {result}")
        except Exception as e:
            logger.exception("Device delete failed.")
            await query.edit_message_text(f"❌ Failed to delete device: {e}")
    else:
        await query.edit_message_text("❌ Delete device cancelled.")
        logger.info(f"Device delete cancelled by {user.id}")
    return ConversationHandler.END

deldevice_conv = ConversationHandler(
    entry_points=[
        CommandHandler("deldevice", deldevice_cmd),
        MessageHandler(filters.Regex("^Delete Device$"), deldevice_cmd)
    ],
    states={
        ASK_DEVICE_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm)],
        CONFIRM: [CallbackQueryHandler(do_del_device)],
    },
    fallbacks=[],
)
