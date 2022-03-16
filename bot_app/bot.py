from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, \
    InlineKeyboardButton, ParseMode, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, InlineQueryHandler, \
    MessageHandler, Filters

import utils

import os, django

from bot_app.configs import configs
import bot_app.commands as commands

import bot_app.model_choices as mch

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cafe_bot.settings")
django.setup()

from bot_app.models import Restaurants, Users, Reservations

bot = Updater(token=configs['TOKEN'], use_context=True)

import datetime as dt


def button(update: Update, context: CallbackContext):
    query = update.callback_query

    query.answer()

    command, *payload = query.data.split(':')

    if command == 'set_city':
        commands.set_city(update, context, payload)
    elif command == 'change_city':
        commands.change_city(update, context, payload)
    elif command == 'my_bookings':
        commands.my_bookings(update, context, payload)
    elif command == 'get_location':
        commands.get_location(update, context, payload)
    elif command == 'get_contacts':
        commands.get_contacts(update, context, payload)
    elif command == 'get_menu':
        commands.get_menu(update, context, payload)
    elif command == 'reserve_table':
        commands.reserve_table(update, context, payload)


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


def on_select_restaurant(update: Update, context: CallbackContext) -> None:
    restaurant = Restaurants.objects.get(
        name=update.message.text
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                '🛎 Бронировать столик 🍽',
                callback_data=f'reserve_table:{restaurant.id}'
            )
        ],
        [
            InlineKeyboardButton(
                '🛍 Заказ еды с собой',
                callback_data='1'
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


def on_reservation(update: Update, context: CallbackContext) -> None:
    user = None
    reservation = None

    try:
        user = Users.objects.get(
            chat_id=update.message.chat_id
        )
    except Users.DoesNotExist:
        return

    try:
        reservation = Reservations.objects.get(
            user=user,
            status=mch.DRAFT,
        )
    except Reservations.DoesNotExist:
        return

    if reservation.date is None:
        open_at_str = reservation.restaurant.open_at
        close_at_str = reservation.restaurant.close_at

        time = dt.datetime.strptime(open_at_str, '%H:%M')
        close_at = dt.datetime.strptime(close_at_str, '%H:%M')

        time_buttons = []

        while time <= close_at:
            time_buttons.append(KeyboardButton(time.strftime('%H:%M')))
            time = time + dt.timedelta(minutes=15)

        keyboard = ReplyKeyboardMarkup(utils.chunks(time_buttons, 4))

        date_str = update.message.text
        date_obj = dt.datetime.strptime(date_str, '%d %B (%A)').replace(year=dt.datetime.now().year)

        reservation.date = date_obj
        reservation.save()
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text='Select time',
            reply_markup=keyboard
        )
    elif reservation.time is None:

        keyboard = ReplyKeyboardMarkup([
            [KeyboardButton('Не имеет значение')],
            [KeyboardButton('Терасса')],
            [KeyboardButton('Основной зал')],
            [KeyboardButton('Балкон')],
        ])

        reservation.time = update.message.text
        reservation.save()
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text='🖼 Please choose hall type',
            reply_markup=keyboard
        )

    elif reservation.place is None:
        count_people = (list(map(
            lambda i: KeyboardButton(str(i) if i != 15 else '15+'),
            range(16)
        )))

        keyboard = ReplyKeyboardMarkup(utils.chunks(count_people, 3))

        reservation.place = update.message.text
        reservation.save()
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text='🔢 Please choose people number or write it down',
            reply_markup=keyboard
        )
    elif reservation.number_of_people is None:
        reservation.number_of_people = update.message.text
        reservation.save()

        username = update.effective_user.full_name

        keyboard = ReplyKeyboardMarkup([[KeyboardButton(username)]])

        context.bot.send_message(
            chat_id=update.message.chat_id,
            text='📝 Please choose customer name or write down',
            reply_markup=keyboard
        )
    elif reservation.contact_name is None:
        reservation.contact_name = update.message.text
        reservation.save()

        keyboard = ReplyKeyboardMarkup([[KeyboardButton('Send contact', request_contact=True)]])

        context.bot.send_message(
            chat_id=update.message.chat_id,
            text='📱 Please send customer contact phone number',
            reply_markup=keyboard
        )
    elif reservation.contact_phone_number is None:
        reservation.contact_phone_number = update.message.contact.phone_number
        reservation.status = mch.ON_REVIEW
        reservation.save()

        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f'Your booking sent to {reservation.restaurant.name}💪🏽\n'
                 f'we are waiting while manager🤵🏽 will approve booking.'
                 f'I will notify 💬 you when get answer from {reservation.restaurant.name}.',
            reply_markup=ReplyKeyboardRemove()
        )


def main():
    start_handler = CommandHandler('start', commands.start)
    help_handler = CommandHandler('help', commands.help)
    inline_handler = InlineQueryHandler(inline)
    button_handler = CallbackQueryHandler(button)
    on_restaurant_select_handler = MessageHandler(Filters.via_bot(bot_id=bot.bot.id), on_select_restaurant)
    on_reservation_handler = MessageHandler((Filters.text | Filters.contact) & ~Filters.command, on_reservation)

    bot.dispatcher.add_handler(on_restaurant_select_handler)
    bot.dispatcher.add_handler(on_reservation_handler)
    bot.dispatcher.add_handler(inline_handler)
    bot.dispatcher.add_handler(button_handler)
    bot.dispatcher.add_handler(start_handler)
    bot.dispatcher.add_handler(help_handler)

    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
