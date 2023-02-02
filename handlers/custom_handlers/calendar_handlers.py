from loader import bot
from utils.logger import logger
from datetime import date
from keyboards.inline.calendar_inline.inline_calendar import bot_get_keyboard_inline
from keyboards.inline.filter import my_date
from telebot.types import Message, CallbackQuery


@bot.message_handler(commands=['calendar'])
def bot_get_keyboard(message: Message) -> None:
    """
    Ответ на команду выдать календарь
    """
    logger.info(f'user_id: {message.from_user.id}')
    bot.send_message(message.chat.id, 'Ваш календарь', reply_markup=bot_get_keyboard_inline())


@bot.callback_query_handler(func=None, my_date_config=my_date.filter())
def callback_inline(call: CallbackQuery) -> None:
    """
    Ловит выбор пользователя с календаря. Выводит дату или изменяет месяц
    :param call: Выбор пользователя
    """
    logger.info(f'user_id: {call.from_user.id}')
    data = my_date.parse(callback_data=call.data)
    my_exit_date = date(year=int(data['year']), month=int(data['month']), day=int(data['day']))
    bot.edit_message_text(my_exit_date, call.message.chat.id, call.message.id)
