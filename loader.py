from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import my_config

storage = StateMemoryStorage()
bot = TeleBot(token=my_config.BOT_TOKEN, state_storage=storage)
