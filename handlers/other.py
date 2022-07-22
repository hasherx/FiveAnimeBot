import json
import string

from create_bot import bot, dp
from aiogram import types, Dispatcher


async def mat_control(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
            .intersection(set(json.load(open('mat.json')))) != set():
        await message.answer('Маты запрещены')
        await message.delete()


def register_handler_other(dp: Dispatcher):
    dp.register_message_handler(mat_control)
