import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from bulls_and_cows import GameSession
from bot_config import TELEGRAM_BOT_TOKEN as BOT_TOKEN

storage = MemoryStorage()

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
        await state.storage.set_state(chat=opponent.chat.id, user=opponent.from_user.id, state=GamerState.game)
        # создаём игровую сессию и записываем её в состояния игроков
        game_session = GameSession(player.chat.id, opponent.chat.id)
        await state.update_data(session=game_session)
        await state.storage.update_data(chat=opponent.chat.id, user=opponent.from_user.id, data={'session' : game_session})
        # отправляем сообщения о начале игры
        await player.answer(
        f"Your opponent is {opponent.from_user.get_mention(as_html=False)}! Enter your number:"
        )
        await opponent.answer(
        f"Your opponent is {player.from_user.get_mention(as_html=False)}! Enter your number:"
        )

async def game_handler(player: types.Message, state: FSMContext):
    await player.answer(
        f"GAME!!!!"
        )

opponent_queue = set()
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