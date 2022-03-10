from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cafe_bot.settings")
django.setup()


from bot_app import messages
from bot_app.models import Users, Cities


def start(update: Update, context: CallbackContext):
    user = Users.objects.get_or_create(
        chat_id=update.message.chat_id,
    )[0]

    user.first_name = update.message.chat.first_name
    user.last_name = update.message.chat.last_name
    user.username = update.message.chat.username

    user.save()

    with open('../stickers/logo.webp', 'rb') as stickerFile:
        context.bot.send_sticker(
            chat_id=update.message.chat_id,
            sticker=stickerFile
        )

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="👋🏻 Hi! Welcome to NigeriaEatBot😎,"
             " I'm here to help you find and make reservations at any restaurant.",
    )

    cities = list(map(lambda city: city.name, Cities.objects.all()))

    city_buttons = []

    for city in cities:
        city_buttons.append([InlineKeyboardButton(str(city), callback_data=f'set_city:{city}')])

    city_keyboard = InlineKeyboardMarkup(city_buttons)

    if user.city_id is None:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="In which city are we looking for venue?",
            reply_markup=city_keyboard
        )
    else:
        messages.send_ready_for_booking_message(context.bot, update.message.chat_id, user.city_id.name)