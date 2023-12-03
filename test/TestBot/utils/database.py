import json

# Загрузить список книг
def load_books():
    try:
        with open('data/libary.json', 'r') as file:
            books = json.load(file)
    except FileNotFoundError:
        books = []
    return books

# Сохранить список книг
def save_books(books):
    with open('data/libary.json', 'w') as file:
        json.dump(books, file, indent=2)