from telegram import Update
from telegram.ext import CallbackContext


async def handle_inline(update: Update, _: CallbackContext):
    await update.message.reply_text(update.inline_query.query)
