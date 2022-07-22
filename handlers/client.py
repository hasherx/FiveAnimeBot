from aiogram.types import ReplyKeyboardRemove

from create_bot import bot, dp
from aiogram.utils.exceptions import CantInitiateConversation
from aiogram import types, Dispatcher

from data_base.postgre_db import *
from keyboards.client import *


async def start_command(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Давай пообщаемся тут', reply_markup=client_keyboard)
        await message.delete()
    except CantInitiateConversation:
        await message.reply('Напиши мне в лс, пожалуйста')


async def bot_description(message: types.Message):
    await message.delete()
    await message.answer('''Five_Anime - помощник для поиска аниме сериалов и фильмов!''',
                         reply_markup=client_keyboard)


async def bot_helper(message: types.Message):
    await message.delete()
    await message.answer('''
    ✅ Доступные команды:
    📌 /menu
    📌 /start
    Для администратора:
    📌 /admin - писать в группе
    ''', reply_markup=client_keyboard)


async def bot_catalogue(message: types.Message):
    await message.delete()
    await message.answer('Выберите категорию!', reply_markup=catalogue_keyboard)


async def close_client_menu(callback_query: types.CallbackQuery):
    await callback_query.answer('Меню закрыто')
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    # await callback_query.message.edit_reply_markup(reply_markup=client_keyboard)


async def random_titles(callback_query: types.CallbackQuery):
    await callback_query.answer('Случайные тайтлы')
    rand_titles = await sql_get_random_titles()
    for title in rand_titles:
        await callback_query.message.answer_photo(title[5], f'{title[1]}\nГод выхода: {title[2]}\nЖанры: {title[3]}\nОписание: {title[4]}\n')

async def ongoing_titles(callback_query: types.CallbackQuery):
    await callback_query.answer('Онгоинги')
    ongoing_titles_list = await sql_get_ongoing()
    for title in ongoing_titles_list:
        await callback_query.message.answer_photo(title[4], f'{title[0]}\nГод выхода: {title[1]}\nЖанры: {title[2]}\nОписание: {title[3]}\n')


async def film_titles(callback_query: types.CallbackQuery):
    await callback_query.answer('Фильмы')
    film_titles_list = await sql_get_films()
    for title in film_titles_list:
        await callback_query.message.answer_photo(title[4], f'{title[0]}\nГод выхода: {title[1]}\nЖанры: {title[2]}\nОписание: {title[3]}\n')


async def get_cats_for_titles(callback_query: types.CallbackQuery):
    await callback_query.answer('Выбери категорию')
    categories = await sql_get_cats_noFilms()
    await callback_query.message.edit_reply_markup(reply_markup=get_cats_markup(categories))


async def titles_by_cats(callback_query: types.CallbackQuery):
    await callback_query.answer('Выбери категорию')
    name = callback_query.data.replace('getcat_', '')
    titles_list = await sql_get_title_by_cat(name)
    for title in titles_list:
        await callback_query.message.answer_photo(title[4], f'{title[0]}\nГод выхода: {title[1]}\nЖанры: {title[2]}\nОписание: {title[3]}\n')


async def step_back(callback_query: types.CallbackQuery):
    await callback_query.answer('Назад')
    await callback_query.message.edit_reply_markup(reply_markup=catalogue_keyboard)


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'menu'])
    dp.register_message_handler(bot_description, lambda message: message.text == "🔎 О боте")
    dp.register_message_handler(bot_helper, lambda message: message.text == "❓ Помощь")
    dp.register_message_handler(bot_catalogue, lambda message: message.text == "📖 Каталог аниме 📖")
    dp.register_callback_query_handler(close_client_menu, lambda message: message.data.startswith("close_menu"))
    dp.register_callback_query_handler(random_titles, lambda message: message.data.startswith("random"))
    dp.register_callback_query_handler(ongoing_titles, lambda message: message.data.startswith("new_title"))
    dp.register_callback_query_handler(film_titles, lambda message: message.data.startswith("films"))
    dp.register_callback_query_handler(get_cats_for_titles, lambda message: message.data.startswith("genres"))
    dp.register_callback_query_handler(step_back, lambda message: message.data.startswith("step_back"))
    dp.register_callback_query_handler(titles_by_cats, lambda message: message.data and message.data.startswith("getcat_"))
