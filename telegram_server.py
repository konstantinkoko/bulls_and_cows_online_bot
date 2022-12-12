import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from bulls_and_cows import GameSession
from bot_config import TELEGRAM_BOT_TOKEN as BOT_TOKEN

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
    game = State()

class Player:
    def __init__(self, chat_id: str, id: str) -> None:
        self.chat_id = chat_id
        self.id = id

async def start_handler(message: types.Message):
    await message.answer(
        f"Hello, {message.from_user.get_mention(as_html=True)} 👋!",
        parse_mode=types.ParseMode.HTML,
    )

async def search_handler(message: types.Message, state: FSMContext):
    await message.answer(
        f"Searching opponent..."
        )
    # ищем оппонента, и когда он найден, меняем состояние игрока и оппонента
    player = Player(message.chat.id, message.from_user.id)
    opponent = await get_opponent(player)
    if opponent is not None:
        await GamerState.game.set()
        await state.storage.set_state(chat=opponent.chat_id, user=opponent.id, state=GamerState.game)
        # создаём игровую сессию и записываем её в состояния игроков
        game_session = GameSession(player, opponent)
        session_index = await storage.get_shared_data("session_index")
        session_index += 1
        await storage.update_shared_data({"session_index" : session_index, str(session_index) : game_session})
        # меняем состояние игроков
        await state.update_data(session_index=session_index)
        await state.storage.update_data(chat=opponent.chat_id, user=opponent.id, data={"session_index" : session_index})
        # отправляем сообщения о начале игры
        opponent_info = await bot.get_chat_member(chat_id=opponent.chat_id, user_id=opponent.id)
        await bot.send_message(
            player.chat_id, f"Your opponent is {opponent_info.user.get_mention(as_html=True)} 👋! Put the number:",
            parse_mode=types.ParseMode.HTML,
        )
        await bot.send_message(
            opponent.chat_id, f"Your opponent is {message.from_user.get_mention(as_html=True)} 👋!  Put the number:",
            parse_mode=types.ParseMode.HTML,
        )

async def game_handler(message: types.Message, state: FSMContext):
    number = message.text
    print(number) #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    data = await state.get_data()
    session_index = data["session_index"]
    session = await storage.get_shared_data(str(session_index))
    result, status = session.check(message.chat.id, number)
    if status == "incorrect":
        await message.answer(f"Wrong input!")
    elif status == "win":
        await bot.send_message(
            result["winner"].chat_id, f"You win 👋!",
            parse_mode=types.ParseMode.HTML,
        )
        await bot.send_message(
            result["looser"].chat_id, f"You loose 👋!",
            parse_mode=types.ParseMode.HTML,
        )
        await state.reset_state()
        await state.storage.reset_state(chat=result["looser"].chat_id, user=result["looser"].id)
    else:
        await message.answer(f"""Bulls: {result["bulls"]}\nCows: {result["cows"]}""")

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
        disp.register_message_handler(search_handler, commands={"search"})
        disp.register_message_handler(game_handler, state=GamerState.game)
        await disp.start_polling()
    finally:
        await bot.close()

asyncio.run(main())