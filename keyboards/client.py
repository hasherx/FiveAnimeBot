from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

client_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
b_menu1 = KeyboardButton('📖 Каталог аниме 📖')
b_menu2 = KeyboardButton('🔎 О боте')
b_menu3 = KeyboardButton('❓ Помощь')
client_keyboard.add(b_menu1).add(b_menu2).insert(b_menu3)


catalogue_keyboard = InlineKeyboardMarkup(row_width=2)
b_catalogue1 = InlineKeyboardButton('🎲 Рандом', callback_data='random')
b_catalogue2 = InlineKeyboardButton('🎯 Жанры', callback_data='genres')
b_catalogue3 = InlineKeyboardButton('📆 Онгоинги', callback_data='new_title')
b_catalogue4 = InlineKeyboardButton('🎬 Фильмы', callback_data='films')
b_catalogue5 = InlineKeyboardButton('❌ Закрыть', callback_data='close_menu')
catalogue_keyboard.add(b_catalogue1).insert(b_catalogue2).add(b_catalogue3).\
    insert(b_catalogue4).add(b_catalogue5)


def get_cats_markup(data):
    markup = InlineKeyboardMarkup(row_width=2)  # создаём клавиатуру
    for cat in data:
        markup.insert(InlineKeyboardButton(cat[0], callback_data=f'getcat_{cat[0]}'))  # Создаём кнопки, i[1] - название, i[2] - каллбек дата
    markup.add(InlineKeyboardButton(text='Назад', callback_data='step_back'))
    return markup  # возвращаем клавиатуру