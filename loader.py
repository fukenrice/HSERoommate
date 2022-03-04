from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.mongo import MongoStorage

from utils.db_api import DataBase
from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
# storage = MongoStorage(host='localhost', port=27017, db_name='aiogram_fsm')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = DataBase(config.DB_PATH)
