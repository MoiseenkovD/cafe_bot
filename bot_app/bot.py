from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, InlineQueryResultArticle, \
    InputTextMessageContent
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, InlineQueryHandler

import os, django

from bot_app.configs import configs

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cafe_bot.settings")
django.setup()

from bot_app.models import Cities, Restaurants, Users

bot = Updater(token=configs['TOKEN'], use_context=True)


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

    cities = list(map(lambda city: city.name, Cities.objects.all()))

    city_buttons = []

    for city in cities:
        city_buttons.append([InlineKeyboardButton(str(city), callback_data=f'set_city:{city}')])

    city_keyboard = InlineKeyboardMarkup(city_buttons)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="👋🏻 Hi! Welcome to NigeriaEatBot😎,"
             " I'm here to help you find and make reservations at any restaurant.",
    )

    if user.city_id is None:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="In which city are we looking for venue?",
            reply_markup=city_keyboard
        )
    else:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f'Я готов забронировать 🌖 '
                 f'для тебя столик в ресторанах 🥗 и барах🍹города {user.city_id.name}'
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    '🛎 Бронировать столик 🍽',
                    switch_inline_query_current_chat=''
                )
            ],
            [
                InlineKeyboardButton(
                    '🛍 Заказ еды с собой • Доставка 🚚',
                    callback_data='🛍 Заказ еды с собой • Доставка 🚚'
                )
            ],
            [
                InlineKeyboardButton('📝 My bookings', callback_data='📝 My bookings'),
                InlineKeyboardButton('🏙 Change city', callback_data='🏙 Change city')
            ]
        ])

        context.bot.send_message(
            chat_id=update.message.chat_id,
            text='Для этого нажми👇 кнопку 🛎\n <strong>Бронировать столик</strong> 🍽 и впиши '
                 'название заведения в поиске или воспользуйся 🆕 новой услугой\n🛍 '
                 '<strong>Заказ еды с собой</strong>',
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )


def button(update: Update, context: CallbackContext):
    query = update.callback_query

    query.answer()

    command, *payload = query.data.split(':')

    if command == 'set_city':

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    '🛎 Бронировать столик 🍽',
                    switch_inline_query_current_chat=''
                )
            ],
            [
                InlineKeyboardButton(
                    '🛍 Заказ еды с собой • Доставка 🚚',
                    callback_data='🛍 Заказ еды с собой • Доставка 🚚'
                )
            ],
            [
                InlineKeyboardButton('📝 My bookings', callback_data='📝 My bookings'),
                InlineKeyboardButton('🏙 Change city', callback_data='🏙 Change city')
            ]
        ])

        query.edit_message_text(
            text=f'Я готов забронировать 🌖 '
                 f'для тебя столик в ресторанах 🥗 и барах🍹города {payload[0]}'
        )

        context.bot.send_message(
            chat_id=update.callback_query.message.chat_id,
            text='Для этого нажми👇 кнопку 🛎\n <strong>Бронировать столик</strong> 🍽 и впиши '
                 'название заведения в поиске или воспользуйся 🆕 новой услугой\n🛍 '
                 '<strong>Заказ еды с собой</strong>',
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )


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


def help(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Список доступных команд \n/start \n/help',
    )


def main():
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
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
