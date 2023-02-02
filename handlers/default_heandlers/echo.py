from telebot.types import Message
from loader import bot
from utils.logger import logger


@bot.message_handler(state=None)
def bot_echo(message: Message):
    logger.info(f'user_id: {message.from_user.id}')
    bot.reply_to(message, "Эхо без состояния или фильтра.\nСообщение:"
                          f"{message.text}")
