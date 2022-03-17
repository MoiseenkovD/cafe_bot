from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from bot_app import messages

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cafe_bot.settings")
django.setup()

from bot_app.models import Restaurants


def get_location(update: Update, context: CallbackContext, payload):
    query = update.callback_query

    restaurant = Restaurants.objects.get(
        id=payload[0]
    )

    context.bot.send_venue(
        chat_id=query.message.chat_id,
        latitude=restaurant.lat,
        longitude=restaurant.lng,
        title=restaurant.name,
        address=restaurant.address,
    )

