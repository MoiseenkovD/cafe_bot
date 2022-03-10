from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, InlineQueryHandler

import os, django

from bot_app.configs import configs
import bot_app.commands as commands

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cafe_bot.settings")
django.setup()

from bot_app.models import Restaurants

bot = Updater(token=configs['TOKEN'], use_context=True)


def button(update: Update, context: CallbackContext):
    query = update.callback_query

    query.answer()

    command, *payload = query.data.split(':')

    if command == 'set_city':
        commands.set_city(update, context, payload)


def inline(update: Update, context: CallbackContext):
    query = update.inline_query.query

    restaurants = Restaurants.objects.all()

    restaurant_inline = []

    for restaurant in restaurants:
        restaurant_inline.append(InlineQueryResultArticle(
            id=restaurant.id,
            title=f'{restaurant.name} {"🛍" if restaurant.is_delivery else ""}(⭐️️{restaurant.rating})\n',
            description=f'{restaurant.open_at}-{restaurant.close_at}\n'
                        f'{restaurant.address}',
            # TODO
            thumb_url=f'https://via.placeholder.com/150/771796',
            input_message_content=InputTextMessageContent(f'{restaurant.name}')))

    update.inline_query.answer(restaurant_inline, cache_time=0)


def main():
    start_handler = CommandHandler('start', commands.start)
    help_handler = CommandHandler('help', commands.help)
    inline_handler = InlineQueryHandler(inline)
    button_handler = CallbackQueryHandler(button)

    bot.dispatcher.add_handler(inline_handler)
    bot.dispatcher.add_handler(button_handler)
    bot.dispatcher.add_handler(start_handler)
    bot.dispatcher.add_handler(help_handler)

    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
