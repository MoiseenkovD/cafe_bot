from telegram import Update, InputMediaPhoto
from telegram.ext import CallbackContext

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cafe_bot.settings")
django.setup()

from bot_app.models import RestaurantsMenu


def get_menu(update: Update, context: CallbackContext, payload):
    query = update.callback_query

    restaurant_menu_items = RestaurantsMenu.objects.filter(
        restaurant=payload[0],
        type='MENU'
    )

    context.bot.send_media_group(
        chat_id=query.message.chat_id,
        media=list(map(lambda menu_item: InputMediaPhoto(media=menu_item.image), restaurant_menu_items))
    )
