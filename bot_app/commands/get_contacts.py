from telegram import Update
from telegram.ext import CallbackContext

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cafe_bot.settings")
django.setup()

from bot_app.models import Restaurants


def get_contacts(update: Update, context: CallbackContext, payload):
    query = update.callback_query

    restaurant = Restaurants.objects.get(
        id=payload[0]
    )

    context.bot.send_contact(
        chat_id=query.message.chat_id,
        first_name=restaurant.name,
        phone_number=restaurant.phone_number
    )

