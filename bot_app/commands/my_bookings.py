from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from telegram.utils.helpers import escape_markdown

from bot_app import messages

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cafe_bot.settings")
django.setup()

from bot_app.models import Users, Reservations

from bot_app import model_choices as mch


def my_bookings(update: Update, context: CallbackContext, payload):
    query = update.callback_query

    user = Users.objects.get(
        chat_id=query.message.chat_id
    )

    reservations = Reservations.objects.filter(
        user=user,
        status__in=[mch.ON_REVIEW, mch.APPROVED],
    )

    if len(reservations) == 0:
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text='maybe u do not have a reservations :( or u should to finish reservation'
        )
    else:
        for reservation in reservations:
            reservations_name = reservation.restaurant.name
            reservations_date = reservation.date
            reservations_time = reservation.time
            reservations_place = reservation.place
            reservations_number_of_people = reservation.number_of_people
            reservations_contact_name = reservation.contact_name
            reservations_contact_phone_number = reservation.contact_phone_number
            reservations_status = reservation.status

            context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f'📜Your reservation:\n'
                     f'<strong>⭐️Restaurant:</strong> {reservations_name}\n'
                     f'<strong>🗓Date:</strong> {reservations_date}\n'
                     f'<strong>🕰Time:</strong> {reservations_time}\n'
                     f'<strong>📍Place in the restaurant:</strong> {reservations_place}\n'
                     f'<strong>👫Number of people:</strong> {reservations_number_of_people}\n'
                     f'<strong>📎Contact name:</strong> {reservations_contact_name}\n'
                     f'<strong>📱Phone Number:</strong> {reservations_contact_phone_number}\n'
                     f'<strong>♻️Status:</strong> {reservations_status}',
                parse_mode=ParseMode.HTML
            )
