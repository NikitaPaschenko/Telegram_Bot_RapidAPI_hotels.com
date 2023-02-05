import os
from telebot.custom_filters import StateFilter
from loguru import logger
from loader import bot
import handlers
from utils.set_bot_commands import set_default_commands
from database.database import create_tables

if __name__ == '__main__':
    logger.add(os.path.join('logs', 'logs.log'),
               format='{time} {level} {message}',
               retention='2 days')
    logger.debug('Запущен новый сеанс')

    create_tables()

    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()
