from aiogram import types, Dispatcher
from aiogram.utils.markdown import text, bold
from aiogram.types import ParseMode
from create_bot import dp
from keyboards.user_kb import kb_user


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nЭто бот-предложка, пропиши команду /help, чтобы узнать, что я могу",
                        reply_markup=kb_user)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    msg = text(bold('Я могу передать твое фото на рассмотрение в чат модераторов, чтобы сделать это, пропиши команду '
                    '/suggest'))
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['dice'])
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")


def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(process_start_command, commands=['start'])
    dp.register_message_handler(process_help_command, commands=['help'])
    dp.register_message_handler(cmd_dice, commands=['dice'])
