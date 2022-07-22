from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from create_bot import bot, dp
from data_base.postgre_db import *
from keyboards.admin import *

ID = None


async def moderate(message: types.Message):
    await message.delete()
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Что нужно, хозяин?', reply_markup=admin_menu)


# Добавление тайтла
class OrderAnime(StatesGroup):
    name = State()
    year = State()
    genres = State()
    description = State()
    image = State()
    cats = State()


async def add_title(message: types.Message):
    await message.delete()
    if message.from_user.id == ID:
        await OrderAnime.name.set()
        await message.answer('Введи имя:')
    else:
        await message.answer('У вас недостаточно прав!')


async def cansel_form(message: types.Message, state: FSMContext):
    await message.delete()
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('OK', reply_markup=ReplyKeyboardRemove())
        return
    await state.finish()
    await message.answer('OK', reply_markup=ReplyKeyboardRemove())


async def add_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Введи год:')
    await OrderAnime.next()


async def add_year(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['year'] = message.text
    await message.answer('Введи жанры:')
    await OrderAnime.next()


async def add_genres(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['genres'] = message.text
    await message.answer('Введи описание:')
    await OrderAnime.next()


async def add_description(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await message.answer('Загрузи фото:')
    await OrderAnime.next()


async def add_image(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['image'] = message.photo[0].file_id
    await sql_add_title(state)
    async with state.proxy() as data:
        data['cats'] = set()
    categories = await sql_get_cats()
    await bot.send_message(message.from_user.id, 'Выбери категорию:', reply_markup=get_cats_markup(categories, state))
    await OrderAnime.next()


async def add_cat(callback_query: types.CallbackQuery, state=FSMContext):
    category = callback_query.data.replace('addcat_', '')
    async with state.proxy() as data:
        data['cats'].add(category)
    await callback_query.answer('Категория ' + f'{category}'.lower() + ' добавлена')


async def end_adding(callback_query: types.CallbackQuery, state=FSMContext):
    async with state.proxy() as data:
        cats = data['cats']
        for cat in cats:
            await sql_add_connection(data['name'], cat)
    await callback_query.message.answer('Тайтл успешно добавлен!')
    await callback_query.answer('Добавить')
    await state.finish()


# Добавить категорию
class OrderCat(StatesGroup):
    name = State()


async def add_category(message: types.Message):
    await message.delete()
    if message.from_user.id == ID:
        await OrderCat.name.set()
        await message.answer('Введи название категории:')
    else:
        await message.answer('У вас недостаточно прав!')


async def cat_name(message: types.Message, state=FSMContext):
    name = [message.text.strip()]
    await sql_add_cat(name)
    await message.answer('Категория успешно добавлена!')
    await state.finish()


# Удалить тайтл
class OrderTitleDelete(StatesGroup):
    category = State()
    title = State()


async def delete_title_start(message: types.Message, state: FSMContext):
    await message.delete()
    if message.from_user.id == ID:
        categories = await sql_get_cats()
        await OrderTitleDelete.category.set()
        await message.answer('Выберите категорию:', reply_markup=get_cats_markup(categories, await state.get_state()))
    else:
        await message.answer('У вас недостаточно прав!')


async def delete_chose_cat(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.answer('Категория выбрана')
    post_list = await sql_get_title_by_cat(callback_query.data.replace('deletecat_', ''))
    for post in post_list:
        await callback_query.message.answer(f'Название: {post[0]}\nГод выпуска: {post[1]}\nЖанры: {post[2]}',
                                            reply_markup=delete_buttons(f'{post[0]}'))
    await OrderTitleDelete.next()


async def delete_title_click(callback_queryset: types.CallbackQuery, state: FSMContext):
    await callback_queryset.answer('Тайтл ' + callback_queryset.data.replace('titledelete_', '') + ' удален')
    await sql_delete_title(callback_queryset.data.replace('titledelete_', ''))


async def delete_title_finish(callback_queryset: types.CallbackQuery, state: FSMContext):
    await callback_queryset.answer('Тайтлы удалены')
    await state.finish()
    await callback_queryset.message.answer('Чем теперь займёмся?', reply_markup=admin_menu)


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(moderate, commands=['admin'], is_chat_admin=True)
    dp.register_message_handler(add_title, Text(equals='Добавить тайтл'), state=None)
    dp.register_message_handler(cansel_form, state="*", commands=['отмена'])
    dp.register_message_handler(cansel_form, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(add_name, state=OrderAnime.name)
    dp.register_message_handler(add_year, state=OrderAnime.year)
    dp.register_message_handler(add_genres, state=OrderAnime.genres)
    dp.register_message_handler(add_description, state=OrderAnime.description)
    dp.register_message_handler(add_image, state=OrderAnime.image, content_types=['photo'])
    dp.register_callback_query_handler(add_cat, lambda x: x.data and x.data.startswith('addcat_'),
                                       state=OrderAnime.cats)
    dp.register_callback_query_handler(end_adding, text='end_adding', state=OrderAnime.cats)
    dp.register_message_handler(add_category, Text(equals='Добавить категорию'), state=None)
    dp.register_message_handler(cat_name, state=OrderCat.name)
    dp.register_message_handler(delete_title_start, Text(equals='Удалить тайтл'), state=None)
    dp.register_callback_query_handler(delete_chose_cat, lambda x: x.data and x.data.startswith('deletecat_'),
                                       state=OrderTitleDelete.category)
    dp.register_callback_query_handler(delete_title_click, lambda x: x.data and x.data.startswith('titledelete_'),
                                       state=OrderTitleDelete.title)
    dp.register_callback_query_handler(delete_title_finish, Text(equals='delete_title_finish'),
                                       state=OrderTitleDelete.title)
