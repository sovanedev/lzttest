from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def genres_keyboard():
    keyboard = InlineKeyboardMarkup()

    genres = ["Фантастика", "Детектив", "Роман", "Поэзия", "Другое"]

    for genre in genres:
        keyboard.add(InlineKeyboardButton(text=genre, callback_data=f"genre:{genre}"))

    return keyboard