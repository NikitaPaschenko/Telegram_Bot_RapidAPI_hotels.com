from loader import bot
import handlers
from keyboards.inline.filter import bind_filters
from utils.set_bot_commands import set_default_commands
from telebot.custom_filters import StateFilter
from utils.logger import logger

if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bind_filters(bot)
    try:
        bot.delete_webhook()
    except Exception as exc:
        logger.exception(exc)
    bot.infinity_polling()
