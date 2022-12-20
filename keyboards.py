from aiogram.types import ReplyKeyboardMarkup, KeyboardButton #, ReplyKeyboardRemove

button_1 = KeyboardButton("/PvP_game")
button_2 = KeyboardButton("/Single_game")
button_3 = KeyboardButton("/Rules")
button_4 = KeyboardButton("/Cancel_game")

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
start_keyboard.add(button_1).add(button_2).add(button_3)

cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
cancel_keyboard.add(button_4).add(button_3)

rules_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
rules_keyboard.add(button_3)
