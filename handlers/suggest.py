import PIL
import imagehash
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp
from data_base import sqlite_db
from PIL import Image
import os


class FSMSuggest(StatesGroup):
    photo = State()


# начало диалога о публикации записи
@dp.message_handler(commands='suggest', state=None)
async def photo_suggest(message: types.Message):
    await FSMSuggest.photo.set()
    await message.reply('Пришлите фото')


# ловим фото от пользователя
@dp.message_handler(content_types=['photo', 'document'], state=FSMSuggest.photo)
async def load_pic(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        error = False
        file_name = 'user_photo.jpg'
        file_path = '/home/phil/PycharmProjects/TelegramBot/handlers/'+file_name
        try:
            await message.photo[-1].download(destination_file=file_path)
            image = Image.open(file_path)
            data['photo'] = message.photo[-1].file_id
            data['d_hash'] = str(imagehash.dhash(image, hash_size=11))
            data['p_hash'] = str(imagehash.phash(image, hash_size=11))
        except IndexError:
            await message.document.download(destination_file=file_path)
            try:
                image = Image.open(file_path)
                data['photo'] = message.document.file_id
                data['d_hash'] = str(imagehash.dhash(image, hash_size=11))
                data['p_hash'] = str(imagehash.phash(image, hash_size=11))
            except PIL.UnidentifiedImageError:
                error = True
                await message.reply('Данный тип файла не может быть обработан, пришлите фото формата JPEG или PNG')
                await state.finish()
    os.remove(file_path)
    if not error:
        if not (await sqlite_db.duplicate_check(state))[0]:
            await message.answer('Фото было проверено и уже направилось на одобрение к модераторам!')
        #/.../
        await state.finish()


# выход из машины состяний
@dp.message_handler(commands='stop', state='*')
@dp.message_handler(Text(equals='stop', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Процесс публикации отменен')


# регистрируем хэндлер
def register_handlers_suggest(dp: Dispatcher):
    dp.register_message_handler(photo_suggest, commands=['suggest'], state=None)
    dp.register_message_handler(load_pic, content_types=['photo'], state=FSMSuggest.photo)
    dp.register_message_handler(cancel_handler, commands='stop', state='*')
    dp.register_message_handler(cancel_handler, Text(equals='stop', ignore_case=True), state='*')
