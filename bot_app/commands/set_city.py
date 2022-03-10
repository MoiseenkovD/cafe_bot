from telegram import Update
from telegram.ext import CallbackContext

from bot_app import messages


def set_city(update: Update, context: CallbackContext, payload):
    query = update.callback_query

    query.delete_message()

    messages.send_ready_for_booking_message(
        context.bot,
        update.callback_query.message.chat_id,
        payload[0]
    )
