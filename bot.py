import logging
from data_base import sqlite_db
from aiogram.utils import executor
from create_bot import dp
from handlers import user, suggest, common


logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    print('Бот вышел в онлайн')
    sqlite_db.init_db()

user.register_handlers_user(dp)
suggest.register_handlers_suggest(dp)
common.register_handlers_common(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
