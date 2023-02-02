import sqlite3
from typing import Any, Dict

from utils.logger import logger


class UserDb:
    """
    Конструктор класса базы данных пользователей
    """
    def __init__(self, db_file: Any) -> None:
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.set_up_db()

    def set_up_db(self) -> Any:
        """
        :return: Создание базы данных
        """
        logger.info(' ')
        with self.connection:
            return self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS User(
            userId INT PRIMARY KEY ,
            first_name TEXT,
            AGE INT NOT NULL DEFAULT 1,
            country TEXT,
            city TEXT)
            ''')

    def check_user(self, user_id: int) -> bool:
        """
        :param user_id: Идентификатор пользователя
        :return: Наличие/отсутствие пользователя
        :rtype: bool
        """
        logger.info(' ')
        with self.connection:
            result = self.cursor.execute('SELECT `userId` FROM User WHERE `userId` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id: int) -> Any:
        """
        :param user_id: Идентификатор пользователя
        :return: Добавить пользователя  БД
        """
        logger.info(' ')
        with self.connection:
            return self.cursor.execute('INSERT INTO User(UserId) VALUES (?)', (user_id,))

    def filling_db(self, data: Dict) -> None:
        """
        Функция записи информации о пользователе из custom_handlers.
        :param data: State telebot
        :return: None
        """
        logger.info(' ')
        with self.connection:
            self.cursor.execute('UPDATE User SET first_name=?, AGE=?, country=?, city=? WHERE userID=?',
                                (data['name'], data['age'], data['country'], data['city'], data['id']))
