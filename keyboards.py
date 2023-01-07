from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

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

symbols = ["йцукенгш", "щзхъфыва", "пролджэя", "чсмитьбю"]
symbol_keyboard = InlineKeyboardMarkup(row_width=1)
for symbol_line in symbols:
    buttons = []
    for symbol in symbol_line:
        buttons.append(InlineKeyboardButton(symbol, callback_data=symbol))
    symbol_keyboard.row(*buttons)


class SymbolKeyboard:

    def __init__(self, secret_word) -> None:
        self.symbols = list("йцукенгшщзхъфывапролджэячсмитьбю")
        self.secret_word = tuple(secret_word)
        self.bulls = []
        self.cows = []

    def _rebalance_symbols(self, word):
        for i, symbol in enumerate(list(word)):
            if word[i] == self.secret_word[i]:
                self.bulls.append(symbol)
                self.symbols.remove(symbol)
            elif symbol in self.secret_word:
                self.cows.append(symbol)
                self.symbols.remove(symbol)
    
    def _get_keyboard(self) -> InlineKeyboardMarkup:
        pass
        

