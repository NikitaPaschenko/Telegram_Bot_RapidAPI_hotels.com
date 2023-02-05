from telebot.types import Message
from loader import bot
from logs.loggers import func_logger


@bot.message_handler(state=None)
@func_logger
def bot_echo(message: Message) -> None:
    bot.reply_to(message, "Эхо без состояния или фильтра.\nСообщение:"
                          f"{message.text}")
