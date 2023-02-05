from telebot.types import Message
from config_data.my_config import DEFAULT_COMMANDS
from loader import bot
from logs.loggers import func_logger


@bot.message_handler(commands=['help'])
@func_logger
def bot_help(message: Message) -> None:
    bot.delete_state(message.from_user.id, message.chat.id)
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, 'Бот фирмы Too Easy Travel может помочь Вам с выбором отеля\n'
                          'В начале работы будет произведен опрос в каком городе будет произведен поиск\n'
                          'Затем нужно ввести критерии поиска и бот предложит сортировку результатов\n'
                          'Бюджетные отели, сортировка по убываю цены и лучшие предложения\n'
                          'Удачи Вам при работе с нашим ботом!')
    bot.reply_to(message, '\n'.join(text))
