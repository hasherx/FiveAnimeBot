from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_cats_markup(data, state_name):
    markup = InlineKeyboardMarkup(row_width=2)  # создаём клавиатуру
    if state_name == 'OrderTitleDelete:category':
        for cat in data:  # цикл для создания кнопок
            markup.insert(InlineKeyboardButton(cat[0], callback_data=f'deletecat_{cat[0]}'))
    else:
        for cat in data:
            markup.insert(InlineKeyboardButton(cat[0], callback_data=f'addcat_{cat[0]}'))  # Создаём кнопки, i[1] - название, i[2] - каллбек дата
        markup.add(InlineKeyboardButton(text='Выбрать', callback_data='end_adding'))
    return markup  # возвращаем клавиатуру


admin_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
menu_b1 = KeyboardButton('Добавить тайтл')
menu_b2 = KeyboardButton('Добавить категорию')
menu_b3 = KeyboardButton('Удалить тайтл')
menu_b4 = KeyboardButton('Отмена')
admin_menu.add(menu_b1).insert(menu_b2).insert(menu_b3).add(menu_b4)


def delete_buttons(name):
    delete_button_board = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton(text=f'Удалить {name}', callback_data=f'titledelete_{name}')
    b_end = InlineKeyboardButton(text='Закончить', callback_data='delete_title_finish')
    delete_button_board.add(b1).insert(b_end)
    return delete_button_board
