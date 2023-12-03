from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config
import logging

mainbot = Bot((config.API_BOT), parse_mode="HTML")
dp = Dispatcher(mainbot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)