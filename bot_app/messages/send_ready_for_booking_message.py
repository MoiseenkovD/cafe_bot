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
            InlineKeyboardButton('📝 My bookings', callback_data='my_bookings'),
            InlineKeyboardButton('🏙 Change city', callback_data='change_city')
        ]
    ])

    bot.send_message(
        chat_id=chat_id,
        text=f'Я готов забронировать 🌖 \n'
             f'для тебя столик в ресторанах 🥗 и барах🍹города {user_city}\n\n'
             f'Для этого нажми👇 кнопку 🛎 <strong>Бронировать столик</strong> 🍽 и впиши '
             f'название заведения в поиске или воспользуйся 🆕 новой услугой\n🛍 '
             f'<strong>Заказ еды с собой</strong>',
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )