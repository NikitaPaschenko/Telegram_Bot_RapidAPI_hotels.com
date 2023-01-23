from keyboards.reply.contact import request_contact
from loader import bot
from states.contact_information import UserInfoState
from telebot.types import Message


@bot.message_handler(commands=['survey'])
def survey(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.name, message.chat.id)
    bot.send_message(message.from_user.id, f"Доброго времени суток, {message.from_user.username}, введи своё имя")


@bot.message_handler(state=UserInfoState.name)
def get_name(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, "Спасибо! Запомню:) А Теперь напиши сколько тебе лет?")
        bot.set_state(message.from_user.id, UserInfoState.age, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['name'] = message.text
    else:
        bot.send_message(message.from_user.id, "Имя может содержать только буквы!")


@bot.message_handler(state=UserInfoState.age)
def get_age(message: Message) -> None:
    if message.text.isdigit():
        if 0 < int(message.text) < 150:
            bot.send_message(message.from_user.id, "Спасибо! Запомню:) А Теперь введи, пожалуйста, страну проживания")
            bot.set_state(message.from_user.id, UserInfoState.country, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['age'] = message.text
        else:
            bot.send_message(message.from_user.id, "Вряд ли это твой настоящий возраст!")
    else:
        bot.send_message(message.from_user.id, "Возраст может быть только числом!")


@bot.message_handler(state=UserInfoState.country)
def get_country(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, "Спасибо! Запомню:) А Теперь напиши из какого ты города?")
        bot.set_state(message.from_user.id, UserInfoState.city, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['country'] = message.text
    else:
        bot.send_message(message.from_user.id, "Название страны может содержать только буквы!")


@bot.message_handler(state=UserInfoState.country)
def get_country(message: Message) -> None:
    bot.send_message(message.from_user.id, "Спасибо! Запомню:) А Теперь напиши из какого ты города?")
    bot.set_state(message.from_user.id, UserInfoState.city, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['country'] = message.text


@bot.message_handler(state=UserInfoState.city)
def get_city(message: Message) -> None:
    bot.send_message(message.from_user.id, "Спасибо! Запомню:) А Теперь отправь свой номер, нажав на кнопку!",
                     reply_markup=request_contact())
    bot.set_state(message.from_user.id, UserInfoState.phone_number, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text


@bot.message_handler(content_types=['contact', 'text'], state=UserInfoState.phone_number)
def get_contact(message: Message) -> None:
    if message.content_type == 'contact':
        bot.send_message(message.from_user.id, "Спасибо за предоставленную информацию! Всё записал:)")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['phone_number'] = message.contact.phone_number
        bot.send_message(message.from_user.id, f"Ваши данные:\nИмя - {data['name']}\nВозраст - {data['age']}\n"
                                               f"Страна - {data['country']}\nГород - {data['city']}\n"
                                               f"Номер телефона - {data['phone_number']}")
    else:
        bot.send_message(message.from_user.id, "Нужно нажать на кнопку, чтобы отправить контактную информацию!")
