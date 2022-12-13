import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from bulls_and_cows import GameSession
from bot_config import TELEGRAM_BOT_TOKEN as BOT_TOKEN
import bot_messages

bot = Bot(token=BOT_TOKEN)

class MyMemoryStorage(MemoryStorage):
    def __init__(self):
        super().__init__()
        self.shared_data = {"session_index" : 0}
    
    async def get_shared_data(self, key):
        return self.shared_data[key]
    
    async def update_shared_data(self, data: dict):
        for key in data:
            self.shared_data[key] = data[key]

storage = MyMemoryStorage()

class GamerState(StatesGroup):
    pvp_game = State()
    single_game = State()

class Player:
    def __init__(self, chat_id: str, id: str) -> None:
        self.chat_id = chat_id
        self.id = id

async def start_handler(message: types.Message):
    await message.answer(
        bot_messages.HELLO_MESSAGE_TEXT.format(message.from_user.get_mention(as_html=True)),
        parse_mode=types.ParseMode.HTML,
    )

async def begin_game_handler(message: types.Message, state: FSMContext):
    player = Player(message.chat.id, message.from_user.id)
    if message.text.strip() == "/search":
        await message.answer(bot_messages.SEARCHING_OPPONENT_TEXT)
        opponent = await get_opponent(player)
        if opponent is not None:
            await GamerState.pvp_game.set()
            await state.storage.set_state(chat=opponent.chat_id, user=opponent.id, state=GamerState.pvp_game)
            await create_game_session(player, opponent, state)
    else:
        opponent = None
        await create_game_session(player, opponent, state)

async def game_handler(message: types.Message, state: FSMContext):
    number = message.text
    data = await state.get_data()
    session_index = data["session_index"]
    session = await storage.get_shared_data(str(session_index))
    result, status, steps = session.check(number, message.chat.id)
    if status == "incorrect":
        await message.answer(bot_messages.WRONG_INPUT_TEXT)
    elif status == "win":
        await state.storage.reset_state(chat=result["winner"].chat_id, user=result["winner"].id)
        await bot.send_message(result["winner"].chat_id, bot_messages.WIN_TEXT.format(steps))
        if result["looser"] is not None:
            await state.storage.reset_state(chat=result["looser"].chat_id, user=result["looser"].id)
            await bot.send_message(result["looser"].chat_id, bot_messages.LOSE_TEXT.format(steps))
    else:
        text = ""
        for key in result:
            text += bot_messages.GAME_STEP_TEXT.format(key, result[key]["bulls"], result[key]["cows"])
        await message.answer(text)

async def create_game_session(player: Player, opponent: Player | None, state: FSMContext):
    game_session = GameSession(player, opponent)
    session_index = await storage.get_shared_data("session_index")
    session_index += 1
    await storage.update_shared_data({"session_index" : session_index, str(session_index) : game_session})
    await state.storage.update_data(chat=player.chat_id, user=player.id, data={"session_index" : session_index})
    if opponent is not None:
        await state.storage.set_state(chat=opponent.chat_id, user=opponent.id, state=GamerState.pvp_game)
        await state.storage.update_data(chat=opponent.chat_id, user=opponent.id, data={"session_index" : session_index})
        await state.storage.set_state(chat=player.chat_id, user=player.id, state=GamerState.pvp_game)
        player_info = await bot.get_chat_member(chat_id=player.chat_id, user_id=player.id)
        opponent_info = await bot.get_chat_member(chat_id=opponent.chat_id, user_id=opponent.id)
        await bot.send_message(
            player.chat_id,
            bot_messages.BEGIN_PVP_GAME_TEXT.format(opponent_info.user.get_mention(as_html=True)),
            parse_mode=types.ParseMode.HTML,
        )
        await bot.send_message(
            opponent.chat_id,
            bot_messages.BEGIN_PVP_GAME_TEXT.format(player_info.user.get_mention(as_html=True)),
            parse_mode=types.ParseMode.HTML,
        )
    else:
        await state.storage.set_state(chat=player.chat_id, user=player.id, state=GamerState.single_game)
        await bot.send_message(player.chat_id, bot_messages.BEGIN_SINGLE_GAME_TEXT)

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

async def main():
    try:
        disp = Dispatcher(bot=bot, storage=storage)
        disp.register_message_handler(start_handler, commands={"start", "restart"})
        disp.register_message_handler(begin_game_handler, commands={"search", "single"})
        disp.register_message_handler(game_handler, state={GamerState.single_game, GamerState.pvp_game})
        await disp.start_polling()
    finally:
        await bot.close()

asyncio.run(main())