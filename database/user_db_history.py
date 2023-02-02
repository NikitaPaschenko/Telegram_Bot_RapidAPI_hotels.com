import sqlite3
import json
from typing import Any, Optional
from utils.logger import logger


class HistoryUserDb:
    """
    Пользовательский класс базы данных для работы с историей поиска пользователя
    """

    def __init__(self, db_file: Any) -> None:
        """
        Конструктор класса базы данных, в которой собрана история поиска пользователей
        """
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.set_up_table()

    def set_up_table(self) -> Any:
        """
        Создает таблицу в БД если ее нет для пользователя
        :return: Создание базы данных
        """
        logger.info(' ')
        with self.connection:
            return self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS UserHistory(
            userID INT,
            search_date datetime DEFAULT CURRENT_DATE,
            command TEXT,
            data json)
            ''')

    def set_data(self, user_id: int, command: str, data: dict[str:Optional]) -> Any:
        """
        Запись в БД пользователя, введенной команды и словаря отелей
        :param user_id: Идентификатор пользователя
        :param command: Команда поиска отелей
        :param data: Словарь отелей
        :return: Заполнение базы данных
        """
        logger.info(' ')
        with self.connection:
            return self.cursor.execute('''
            INSERT INTO UserHistory(`userID`,`command`,`data`)
            VALUES (?,?,?)''', (user_id, command, json.dumps(data)))

    def get_data(self, user_id: int, count: int) -> Any:
        """
        Получение из базы данных истории поиска пользователя
        :param user_id: Идентификатор пользователя
        :param count: Количество отелей
        :return: История поиска пользователя
        """
        logger.info(' ')
        with self.connection:
            return self.cursor.execute('''
            SELECT `search_date`,`command`,`data` FROM UserHistory
            WHERE `userID` = ? LIMIT ?''', (user_id, count))

    def del_data(self, user_id: int) -> Any:
        """
        Стереть историю поиска пользователя
        :param user_id: Идентификатор пользователя
        :return: Удаление истории поиска пользователя
        """
        logger.info(' ')
        with self.connection:
            return self.cursor.execute('''
            DELETE FROM UserHistory WHERE `userID` = ? ''', (user_id,))
