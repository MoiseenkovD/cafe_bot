from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from bot_app import messages

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cafe_bot.settings")
django.setup()

from bot_app.models import Users, Cities


def change_city(update: Update, context: CallbackContext, payload):
    query = update.callback_query

    query.delete_message()

    city_buttons = []

    for city in Cities.objects.all():
        city_buttons.append([InlineKeyboardButton(str(city.name), callback_data=f'set_city:{city.id}')])

    city_keyboard = InlineKeyboardMarkup(city_buttons)

    context.bot.send_message(
        chat_id=query.message.chat_id,
        text="In which city are we looking for venue?",
        reply_markup=city_keyboard
    )
