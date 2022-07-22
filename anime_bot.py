from aiogram.utils import executor
from create_bot import dp
from data_base.postgre_db import sql_start
from handlers import client, admin, other


async def bot_onstartup(_):
    sql_start()
    print('Бот вышел в онлайн')


admin.register_handler_admin(dp)
client.register_handler_client(dp)
other.register_handler_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=bot_onstartup)
