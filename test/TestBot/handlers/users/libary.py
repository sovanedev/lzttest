from loader import dp
from aiogram import types

from callbacks.callback_libary import AddBook, SearchBook, DelBook

from utils.database import load_books

# Добавить книгу
@dp.message_handler(commands=['addbook'])
async def add_book(message: types.Message):
    await message.answer("Введите название книги:")
    await AddBook.adding_title.set()

# Список книг
@dp.message_handler(commands=['listbooks'])
async def list_books(message: types.Message):
    books = load_books()
    if not books:
        await message.answer("Библиотека пуста.")
        return
    content = '------------== Список книг ==------------\n'
    for book in books:
        content += f"Название - <b>{book['title']}</b>\nАвтор - <b>{book['author']}</b>\nЖанр - <b>{book['genre']}</b>\nОписание - <b>{book['description']}</b>"
        content += "\n---------------------=====-------------------\n"

    await message.answer(content)

# Найти книгу
@dp.message_handler(commands=['search'])
async def search_books(message: types.Message):
    await message.answer("Введите ключевое слово для поиска:")
    await SearchBook.searching.set()

# Удалить книгу
@dp.message_handler(commands=['deletebook'])
async def delete_book(message: types.Message):
    await message.answer("Введите название книги, которую вы хотите удалить:")
    await DelBook.deleting.set()