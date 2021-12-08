from aiogram import types, Dispatcher
from create_bot import dp


@dp.message_handler()
async def echo_message(message: types.Message):
    if message.text.lower() == 'перерыв':
        await message.answer('Внимание, объявляется перекур 🚬')
    else:
        await message.answer(message.text)


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(echo_message)