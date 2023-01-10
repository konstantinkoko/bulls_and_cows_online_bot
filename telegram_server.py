import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from typing import Any

from bulls_and_cows import GameSession
from bot_config import LANGUAGE, TELEGRAM_BOT_TOKEN as BOT_TOKEN
import bot_messages
from keyboards import start_keyboard, cancel_keyboard, rules_keyboard

# инициализация бота
bot = Bot(token=BOT_TOKEN)

# добавление общего хранилища к MemoryStorage
class MyMemoryStorage(MemoryStorage):
    def __init__(self) -> None:
        super().__init__()
        self.shared_data = {"session_index" : 0}
    
    async def get_shared_data(self, key: str) -> Any:
        return self.shared_data[key]
    
    async def update_shared_data(self, data: dict) -> None:
        for key in data:
            self.shared_data[key] = data[key]

# инициализация хранилища
storage = MyMemoryStorage()

# описание состояний пользователя
class GamerState(StatesGroup):
    pvp_game = State()
    single_game = State()

class Player:
    def __init__(self, chat_id: str, id: str) -> None:
        self.chat_id = chat_id
        self.id = id

# хэндлеры
async def start_handler(message: types.Message, state: FSMContext) -> None:
    await state.reset_state()
    await message.answer(
        bot_messages.HELLO_MESSAGE_TEXT[LANGUAGE].format(message.from_user.get_mention(as_html=True)),
        reply_markup=start_keyboard,
        parse_mode=types.ParseMode.HTML
    )

async def rules_handler(message: types.Message, state: FSMContext) -> None:
    await message.answer(bot_messages.RULES_TEXT[LANGUAGE])
    if await state.get_state() is not None:
        await message.answer(bot_messages.PUT_THE_NUMBER_TEXT[LANGUAGE])

async def begin_game_handler(message: types.Message, state: FSMContext) -> None:
    player = Player(message.chat.id, message.from_user.id)
    if message.text.strip() == "/PvP_game":
        await message.answer(bot_messages.SEARCHING_OPPONENT_TEXT[LANGUAGE], reply_markup=rules_keyboard)
        opponent = await get_opponent(player)
        if opponent is not None:
            await GamerState.pvp_game.set()
            await state.storage.set_state(chat=opponent.chat_id, user=opponent.id, state=GamerState.pvp_game)
            await create_game_session(player, opponent, state)
            player_info = await bot.get_chat_member(chat_id=player.chat_id, user_id=player.id)
            opponent_info = await bot.get_chat_member(chat_id=opponent.chat_id, user_id=opponent.id)
            await bot.send_message(
                player.chat_id,
                bot_messages.BEGIN_PVP_GAME_TEXT[LANGUAGE].format(opponent_info.user.get_mention(as_html=True)),
                parse_mode=types.ParseMode.HTML,
            )
            await bot.send_message(
                opponent.chat_id,
                bot_messages.BEGIN_PVP_GAME_TEXT[LANGUAGE].format(player_info.user.get_mention(as_html=True)),
                parse_mode=types.ParseMode.HTML,
            )
    else:
        opponent = None
        await create_game_session(player, opponent, state)
        await bot.send_message(player.chat_id, bot_messages.BEGIN_SINGLE_GAME_TEXT[LANGUAGE], reply_markup=cancel_keyboard)

async def game_handler(message: types.Message, state: FSMContext) -> None:
    number = message.text
    data = await state.get_data()
    session_index = data["session_index"]
    session = await storage.get_shared_data(str(session_index))
    result, status, steps = session.check(number, message.chat.id)
    if status == "incorrect":
        await message.answer(bot_messages.WRONG_INPUT_TEXT[LANGUAGE])
    elif status == "win":
        await state.storage.reset_state(chat=result["winner"].chat_id, user=result["winner"].id)
        await bot.send_message(result["winner"].chat_id, bot_messages.WIN_TEXT[LANGUAGE].format(steps), reply_markup=start_keyboard)
        if result["looser"] is not None:
            await state.storage.reset_state(chat=result["looser"].chat_id, user=result["looser"].id)
            await bot.send_message(result["looser"].chat_id, bot_messages.LOSE_TEXT[LANGUAGE].format(steps), reply_markup=start_keyboard)
    else:
        text = ""
        for key in result:
            text += bot_messages.GAME_STEP_TEXT.format(key, result[key]["bulls"], result[key]["cows"])
        await message.answer(text)

# создание и запись в хранилище игровой сессии (если opponent is None - single game), и установка соответствующих состояний игрокам
async def create_game_session(player: Player, opponent: Player | None, state: FSMContext) -> None:
    game_session = GameSession(player, opponent)
    session_index = await storage.get_shared_data("session_index")
    session_index += 1
    await storage.update_shared_data({"session_index" : session_index, str(session_index) : game_session})
    await state.storage.update_data(chat=player.chat_id, user=player.id, data={"session_index" : session_index})
    if opponent is not None:
        await state.storage.set_state(chat=opponent.chat_id, user=opponent.id, state=GamerState.pvp_game)
        await state.storage.update_data(chat=opponent.chat_id, user=opponent.id, data={"session_index" : session_index})
        await state.storage.set_state(chat=player.chat_id, user=player.id, state=GamerState.pvp_game)
    else:
        await state.storage.set_state(chat=player.chat_id, user=player.id, state=GamerState.single_game)

# поиск оппонента
opponent_queue = set()
async def get_opponent(player: Player) -> Player | None:
    opponent_queue.add(player)
    if len(opponent_queue) > 1:
        for elem in opponent_queue:
            if elem.chat_id != player.chat_id:
                opponent_queue.remove(player)
                opponent_queue.remove(elem)
                return elem
    return None

async def main() -> None:
    try:
        disp = Dispatcher(bot=bot, storage=storage)
        disp.register_message_handler(start_handler, commands={"start", "restart", "Cancel_game"}, state='*')
        disp.register_message_handler(rules_handler, commands={"Rules"}, state='*')
        disp.register_message_handler(begin_game_handler, commands={"PvP_game", "Single_game"})
        disp.register_message_handler(game_handler, state={GamerState.single_game, GamerState.pvp_game})
        await disp.start_polling()
    finally:
        await bot.close()

asyncio.run(main())
