from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

but1 = KeyboardButton('/start')
but2 = KeyboardButton('/help')
but3 = KeyboardButton('/dice')

kb_user = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_user.add(but1).add(but2).add(but3)
