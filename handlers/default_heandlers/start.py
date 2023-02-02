from telebot.types import Message
from loader import bot
from utils.logger import logger
from keyboards.inline.start_button import create_buttons_start


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    logger.info(f'user_id: {message.from_user.id}')
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, 'Выберите действие',
                     reply_markup=create_buttons_start())
