from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cafe_bot.settings")
django.setup()

from datetime import datetime, timedelta


def reserve_table(update: Update, context: CallbackContext, payload):
    query = update.callback_query

    buttons = list(map(
        lambda i: [KeyboardButton((datetime.now() + timedelta(days=+i)).strftime('%d %B (%A)'))],
        range(14)
    ))

    keyboard = ReplyKeyboardMarkup(buttons)

    context.bot.send_message(
        chat_id=query.message.chat_id,
        text="🗓 Please choose a date:",
        reply_markup=keyboard
    )

