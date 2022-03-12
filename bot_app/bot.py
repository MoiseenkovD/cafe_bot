from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, \
    InlineKeyboardButton, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, InlineQueryHandler, \
    MessageHandler, Filters

import os, django

from bot_app.configs import configs
import bot_app.commands as commands

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cafe_bot.settings")
django.setup()

from bot_app.models import Restaurants, Users

bot = Updater(token=configs['TOKEN'], use_context=True)


def button(update: Update, context: CallbackContext):
    query = update.callback_query

    query.answer()

    command, *payload = query.data.split(':')

    if command == 'set_city':
        commands.set_city(update, context, payload)
    elif command == 'change_city':
        commands.change_city(update, context, payload)
    elif command == 'get_location':
        commands.get_location(update, context, payload)
    elif command == 'get_contacts':
        commands.get_contacts(update, context, payload)
    elif command == 'get_menu':
        commands.get_menu(update, context, payload)


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


def on_select_cafe(update: Update, context: CallbackContext) -> None:
    restaurant = Restaurants.objects.get(
        name=update.message.text
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                '🛎 Бронировать столик 🍽',
                callback_data='🛎 Бронировать столик 🍽'
            )
        ],
        [
            InlineKeyboardButton(
                '🛍 Заказ еды с собой',
                callback_data='🛍 Заказ еды с собой'
            )
        ],
        [
            InlineKeyboardButton('🍽 Меню', callback_data=f'get_menu:{restaurant.id}:MENU'),
            InlineKeyboardButton('🍹 Бар', callback_data=f'get_menu:{restaurant.id}:BAR')
        ],
        [
            InlineKeyboardButton('📍 Геопозиция', callback_data=f'get_location:{restaurant.id}'),
            InlineKeyboardButton('📞 Контакты', callback_data=f'get_contacts:{restaurant.id}')
        ]
    ])

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f'<strong>{restaurant.name} ⭐️{restaurant.rating}</strong>\n\n'
             f'{restaurant.open_at}-{restaurant.close_at}\n'
             f'{restaurant.address}\n\n'
             f'🛍<strong>Delivering:</strong> {"YES" if restaurant.is_delivery else "NO"}',
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )


def main():
    start_handler = CommandHandler('start', commands.start)
    help_handler = CommandHandler('help', commands.help)
    inline_handler = InlineQueryHandler(inline)
    button_handler = CallbackQueryHandler(button)
    message_handle = MessageHandler(Filters.via_bot(bot_id=bot.bot.id), on_select_cafe)

    bot.dispatcher.add_handler(message_handle)
    bot.dispatcher.add_handler(inline_handler)
    bot.dispatcher.add_handler(button_handler)
    bot.dispatcher.add_handler(start_handler)
    bot.dispatcher.add_handler(help_handler)

    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
