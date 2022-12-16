from aiogram.types import ReplyKeyboardMarkup, KeyboardButton #, ReplyKeyboardRemove

button_1 = KeyboardButton("/PvP_game")
button_2 = KeyboardButton("/Single_game")
button_3 = KeyboardButton("/Cancel_game")

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_keyboard.add(button_1).add(button_2)

cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cancel_keyboard.add(button_3)

    

