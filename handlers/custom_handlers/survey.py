from states.contact_information import UserInfoState
from loader import bot, db_user
from utils.logger import logger

from telebot.types import Message


@bot.message_handler(commands=['survey'])
def start_ex(message: Message) -> None:
    """
    Команда старт. Присваивается этап 'name'
    :param: Message
    :return: None
    """
    logger.info(f'user_id: {message.from_user.id}')
    if not db_user.check_user(message.from_user.id):
        db_user.add_user(message.from_user.id)
        logger.error(f'user_id: {message.from_user.id}')
    bot.set_state(message.from_user.id, UserInfoState.name, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['id'] = message.from_user.id
    bot.send_message(message.chat.id, 'Привет! Напиши свое имя.')


@bot.message_handler(state=UserInfoState.name)
def name_get(message: Message) -> None:
    """
    У пользователя запрашивается имя
    :param: Message
    :return: None
    """
    logger.info(f'user_id: {message.from_user.id}')
    bot.send_message(message.chat.id, f'"Спасибо! Запомню:) А Теперь введи, пожалуйста, страну проживания"')
    bot.set_state(message.from_user.id, UserInfoState.country, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text


@bot.message_handler(state=UserInfoState.country)
def ask_age(message: Message) -> None:
    """
    У пользователя запрашивается город и записывается страна проживания
    :param: Message
    :return: None
    """
    logger.info(f'user_id: {message.from_user.id}')
    bot.send_message(message.chat.id, "Спасибо! Запомню:) А Теперь напиши из какого ты города?")
    bot.set_state(message.from_user.id, UserInfoState.city, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['country'] = message.text


@bot.message_handler(state=UserInfoState.city)
def ask_age(message: Message) -> None:
    """
    У пользователя запрашивается возраст и записывается город проживания
    :param: Message
    :return: None
    """
    logger.info(f'user_id: {message.from_user.id}')
    bot.send_message(message.chat.id, "Сколько тебе лет?")
    bot.set_state(message.from_user.id, UserInfoState.age, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text


@bot.message_handler(state=UserInfoState.age, is_digit=True)
def ready_for_answer(message: Message) -> None:
    """
    Идет проверка на ввод возраста числом
    :param: Message
    :return: None
    """
    logger.info(f'user_id: {message.from_user.id}')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = int(message.text)
        bot.set_state(message.from_user.id, UserInfoState.phone_number, message.chat.id)
        bot.send_message(message.chat.id, "А теперь отправь свой номер телефона, нажав на кнопку!")
        db_user.filling_db(data)


@bot.message_handler(state=UserInfoState.age, is_digit=False)
def age_incorrect(message: Message) -> None:
    """
    Если при вводе возраста ввели не число
    """
    logger.error(f'user_id: {message.from_user.id}')
    bot.send_message(message.chat.id, 'Ты ввел не цифру, а строку! Пожалуйста, введи свой возраст в цифрах!')


@bot.message_handler(content_types=['contact', 'text'], state=UserInfoState.phone_number)
def get_contact(message: Message) -> None:
    """
    У пользователя запрашивается номер телефона
    :param: Message
    :return: None
    """
    if message.content_type == 'contact':
        bot.send_message(message.from_user.id, "Спасибо за предоставленную информацию! Всё записал:)")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['phone_number'] = message.contact.phone_number
            db_user.filling_db(data)
        bot.send_message(message.from_user.id, f"Ваши данные:\nИмя - {data['name']}\nВозраст - {data['age']}\n"
                                               f"Страна - {data['country']}\nГород - {data['city']}\n"
                                               f"Номер телефона - {data['phone_number']}")
    else:
        bot.send_message(message.from_user.id, "Нужно нажать на кнопку, чтобы отправить контактную информацию!")
    bot.delete_state(message.from_user.id, message.chat.id)
