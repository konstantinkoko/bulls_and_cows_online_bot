import asyncio
from aiogram import Bot, Dispatcher, types

from bulls_and_cows import GameSession
from bot_config import TELEGRAM_BOT_TOKEN as BOT_TOKEN

async def start_handler(player: types.Message):
    await player.answer(
        f"Hello, {player.from_user.get_mention(as_html=True)} 👋!",
        parse_mode=types.ParseMode.HTML,
    )

async def search_handler(player: types.Message):
    await player.answer(
        f"Searching opponent..."
        )
    opponent = None
    while opponent is None:
        opponent = await get_opponent(player)
        await asyncio.sleep(1)
    game_session = GameSession(player.chat.id, opponent.chat.id)
    # изменить состояние игроков
    # записать game_session в кэш

opponent_queue = set()
async def get_opponent(player: types.Message):
    opponent_queue.add(player)
    if len(opponent_queue) > 1:
        for elem in opponent_queue:
            if elem.chat.id != player.chat.id:
                opponent_queue.remove(player)
                opponent_queue.remove(elem)
                return elem

async def main():
    bot = Bot(token=BOT_TOKEN)
    try:
        disp = Dispatcher(bot=bot)
        disp.register_message_handler(start_handler, commands={"start", "restart"})
        disp.register_message_handler(search_handler, commands={"search"})
        await disp.start_polling()
    finally:
        await bot.close()

asyncio.run(main())