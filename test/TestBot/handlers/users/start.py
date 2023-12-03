from loader import dp
from aiogram import types

# Начало работы
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот для управления библиотекой.\n"
                        "Вот список моих команд:\n"
                        "/addbook - <b>Добавить книгу</b>\n"
                        "/search - <b>Найти книгу по ключевым словам</b>\n"
                        "/listbooks - <b>Список всех книг</b>\n"
                        "/deletebook - <b>Удалить книгу</b>")