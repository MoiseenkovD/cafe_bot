from telegram import Bot, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton


def send_ready_for_booking_message(bot: Bot, chat_id: int, user_city: str):
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

    bot.send_message(
        chat_id=chat_id,
        text=f'Я готов забронировать 🌖 '
             f'для тебя столик в ресторанах 🥗 и барах🍹города {user_city}'
    )

    bot.send_message(
        chat_id=chat_id,
        text='Для этого нажми👇 кнопку 🛎\n <strong>Бронировать столик</strong> 🍽 и впиши '
             'название заведения в поиске или воспользуйся 🆕 новой услугой\n🛍 '
             '<strong>Заказ еды с собой</strong>',
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )