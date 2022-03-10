from telegram import Update
from telegram.ext import CallbackContext

from bot_app import messages

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cafe_bot.settings")
django.setup()

from bot_app.models import Users, Cities


def set_city(update: Update, context: CallbackContext, payload):
    query = update.callback_query

    user = Users.objects.get(chat_id=query.message.chat_id)

    city = Cities.objects.get(name=payload[0])

    user.city = city

    user.save()

    query.delete_message()

    messages.send_ready_for_booking_message(
        context.bot,
        update.callback_query.message.chat_id,
        payload[0]
    )
