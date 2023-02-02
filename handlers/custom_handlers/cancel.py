from loader import bot
from utils.logger import logger


@bot.message_handler(state="*", commands=['отмена', 'Отмена', 'ОТМЕНА'])
def any_state(message) -> None:
    """
    Отмена этапов поиска и выбора критериев
    """
    logger.info(f'user_id: {message.from_user.id}')
    bot.send_message(message.chat.id, "Твои этапы отменены.")
    bot.delete_state(message.from_user.id, message.chat.id)
