import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from bulls_and_cows import GameSession
from bot_config import TELEGRAM_BOT_TOKEN as BOT_TOKEN

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

async def start_handler(player: types.Message):
    await player.answer(
        f"Hello, {player.from_user.get_mention(as_html=True)} 👋!",
        parse_mode=types.ParseMode.HTML,
    )

async def search_handler(player: types.Message, state: FSMContext):
    await player.answer(
        f"Searching opponent..."
        )
    # ищем оппонента, и когда он найден, меняем состояние игрока и оппонента
    opponent = await get_opponent(player)
    if opponent is not None:
        await GamerState.game.set()
        ##await state.storage.set_state(chat=opponent.chat.id, user=opponent.from_user.id, state=GamerState.game)
        # создаём игровую сессию и записываем её в состояния игроков
        game_session = GameSession(player.chat.id, opponent.chat.id)
        sesion_index = await storage.get_shared_data("session_index")
        sesion_index += 1
        await storage.update_shared_data({"session_index" : sesion_index, str(sesion_index) : game_session})
        await state.update_data(session_index=sesion_index)
        ##await state.storage.update_data(chat=opponent.chat.id, user=opponent.from_user.id, data={"session_index" : session_index})
        # отправляем сообщения о начале игры
        ##await player.answer(
        ##f"Your opponent is {opponent.from_user.get_mention(as_html=False)}! Enter your number:"
        ##)
        ##await opponent.answer(
        ##f"Your opponent is {player.from_user.get_mention(as_html=False)}! Enter your number:"
        ##)

async def game_handler(player: types.Message, state: FSMContext):
    number = player.text
    print(number)
    data =await state.get_data()
    session_index = data["session_index"]
    session = await storage.get_shared_data(str(session_index))
    result, win_status = session.check(player, number)
    if win_status:
        await result["winner"].answer(f"You win!")
        await result["looser"].answer(f"You loose!")
        await state.reset_state()
        await state.storage.reset_state(chat=result["looser"].chat.id, user=result["looser"].from_user.id)
    else:
        await player.answer(f"""Bulls: {result["bulls"]}
                                 Cows: {result["cows"]}""")

from tests import FakePlayer
opponent_queue = set([FakePlayer()])
async def get_opponent(player: types.Message) -> types.Message | None:
    opponent_queue.add(player)
    if len(opponent_queue) > 1:
        for elem in opponent_queue:
            if elem.chat.id != player.chat.id:
                opponent_queue.remove(player)
                opponent_queue.remove(elem)
                return elem
    return None

async def main():
    bot = Bot(token=BOT_TOKEN)
    try:
        disp = Dispatcher(bot=bot, storage=storage)
        disp.register_message_handler(start_handler, commands={"start", "restart"})
        disp.register_message_handler(search_handler, commands={"search"})
        disp.register_message_handler(game_handler, state=GamerState.game)
        await disp.start_polling()
    finally:
        await bot.close()

asyncio.run(main())