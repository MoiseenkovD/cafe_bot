from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

import os, django

import bot_app.model_choices as mch

from bot_app.models import Users, Reservations, Restaurants

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cafe_bot.settings")
django.setup()


from datetime import datetime, timedelta


def reserve_table(update: Update, context: CallbackContext, payload):
    query = update.callback_query

    user = Users.objects.get(
        chat_id=query.message.chat_id
    )

    reservation = Reservations.objects.get_or_create(
        user=user,
        status=mch.DRAFT,
    )[0]

    restaurant = Restaurants.objects.get(
        id=payload[0]
    )

    reservation.restaurant = restaurant
    reservation.date = None
    reservation.time = None
    reservation.place = None
    reservation.number_of_people = None
    reservation.contact_name = None
    reservation.contact_phone_number = None
    reservation.save()

    keyboard = ReplyKeyboardMarkup(list(map(
        lambda i: [KeyboardButton((datetime.now() + timedelta(days=+i)).strftime('%d %B (%A)'))],
        range(14)
    )))

    context.bot.send_message(
        chat_id=query.message.chat_id,
        text="🗓 Please choose a date:",
        reply_markup=keyboard
    )
