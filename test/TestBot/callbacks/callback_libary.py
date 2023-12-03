from loader import dp

from keyboards import inline

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types

from utils.database import load_books, save_books

# callback для добавления книги
class AddBook(StatesGroup):
    adding_title = State()
    adding_author = State()
    adding_description = State()
    adding_genre = State()

# Обработчик ввода названия книги
@dp.message_handler(state=AddBook.adding_title)
async def process_title(message: types.Message, state: FSMContext):
    title = message.text
    libary = load_books()

    if any(book['title'].lower() == title.lower() for book in libary):
        await message.answer("Данная книга уже есть у нас в библиотеке. \nОзнакомиться со списком книг вы можете здесь - /listbooks")
        await state.finish()
        return
    
    async with state.proxy() as data:
        data['title'] = title

    await AddBook.next()
    await message.answer("Введите автора книги:")

# Обработчик ввода автора книги
@dp.message_handler(state=AddBook.adding_author)
async def process_author(message: types.Message, state: FSMContext):
    author = message.text
    async with state.proxy() as data:
        data['author'] = author

    await AddBook.next()
    await message.answer("Введите описание книги:")

# Обработчик ввода описания книги
@dp.message_handler(state=AddBook.adding_description)
async def process_description(message: types.Message, state: FSMContext):
    description = message.text
    async with state.proxy() as data:
        data['description'] = description

        keyboard = inline.genres_keyboard()

    await message.answer("Выберите жанр книги или введите свой:", reply_markup=keyboard)
    await AddBook.adding_genre.set()

# callback для выбора жанра по кнопке
@dp.callback_query_handler(text_startswith='genre', state=AddBook.adding_genre)
async def process_genre_callback(query: types.CallbackQuery, state: FSMContext):
    genre = query.data.split(':')[1]
    data = await state.get_data()

    books = load_books()
    new_book = {
        'title': data['title'],
        'author': data['author'],
        'description': data['description'],
        'genre': genre
    }
    books.append(new_book)
    save_books(books)

    await dp.bot.send_message(query.from_user.id, "Книга успешно добавлена в библиотеку!")

    await state.finish()

# Обработчик ввода жанра книги
@dp.message_handler(state=AddBook.adding_genre)
async def process_genre(message: types.Message, state: FSMContext):
    genre = message.text
    async with state.proxy() as data:
        data['genre'] = genre

    books = load_books()
    new_book = {
        'title': data['title'],
        'author': data['author'],
        'description': data['description'],
        'genre': data['genre']
    }
    books.append(new_book)
    save_books(books)

    await message.answer("Книга успешно добавлена в библиотеку!")

    await state.finish()

# callback для поиска книг
class SearchBook(StatesGroup):
    searching = State()

@dp.message_handler(state=SearchBook.searching)
async def process_search(message: types.Message, state: FSMContext):
    keyword = message.text
    books = load_books()
    found_books = [book for book in books if keyword.lower() in book['title'].lower() or keyword.lower() in book['author'].lower()]
    
    if not found_books:
        await message.answer("По вашему запросу ничего не найдено.")
        return
    
    content = ''
    for book in found_books:
        content += f"Название - <b>{book['title']}</b>\nАвтор - <b>{book['author']}</b>\nЖанр - <b>{book['genre']}</b>\nОписание - <b>{book['description']}</b>\n\n"
    await message.answer(content)
    await state.finish()

# callback для удаления книги
class DelBook(StatesGroup):
    deleting = State()

@dp.message_handler(state=DelBook.deleting)
async def process_delete(message: types.Message, state: FSMContext):
    title_to_delete = message.text
    books = load_books()
    new_books = [book for book in books if book['title'].lower() != title_to_delete.lower()]

    if len(new_books) == len(books):
        await message.answer(f"Книга с названием <b>'{title_to_delete}'</b> не найдена.")
    else:
        save_books(new_books)
        await message.answer(f"Книга с названием <b>'{title_to_delete}'</b> успешно удалена.")

    await state.finish()
    
