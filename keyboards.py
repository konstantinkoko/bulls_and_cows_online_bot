from aiogram.types import ReplyKeyboardMarkup, KeyboardButton #, ReplyKeyboardRemove

pvp_button = KeyboardButton("/PvP_game")
single_game_button = KeyboardButton("/Single_game")
rules_button = KeyboardButton("/Rules")
cansel_button = KeyboardButton("/Cancel_game")

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
start_keyboard.add(pvp_button).add(single_game_button).add(rules_button)

cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
cancel_keyboard.add(cansel_button).add(rules_button)

rules_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
rules_keyboard.add(rules_button)
