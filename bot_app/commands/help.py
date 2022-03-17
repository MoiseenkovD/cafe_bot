from telegram import Update
from telegram.ext import CallbackContext


def help(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Список доступных команд \n/start \n/help',
    )
