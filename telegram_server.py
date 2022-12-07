import asyncio
from aiogram import Bot, Dispatcher, types

from bulls_and_cows import BullsAndCows
from bot_config import TELEGRAM_BOT_TOKEN as BOT_TOKEN
from collections import deque
import time

async def start_handler(event: types.Message):
    await event.answer(
        f"Hello, {event.from_user.get_mention(as_html=True)} 👋!",
        parse_mode=types.ParseMode.HTML,
    )

async def search_handler(event: types.Message):
    await event.answer(
        f"Searching opponent..."
        )
    print(event.from_user.first_name)
    opponent = None
    while opponent is None:
        opponent = await get_opponent(event)
        await asyncio.sleep(1)
    print(opponent)
    await create_game_session(event, opponent)

opponent_queue = set()
async def get_opponent(event: types.Message):
    opponent_queue.add(event)
    if len(opponent_queue) > 1:
        for elem in opponent_queue:
            if elem.chat.id != event.chat.id:
                opponent_queue.remove(event)
                opponent_queue.remove(elem)
                return elem

async def create_game_session(player_1: types.Message, player_2: types.Message):
    await player_1.answer(
        f"Your opponent {player_2.from_user.get_mention(as_html=True)}👋 Get ready to the battle!",
        parse_mode=types.ParseMode.HTML,
    )
    await player_2.answer(
        f"Your opponent {player_1.from_user.get_mention(as_html=True)}👋 Get ready to the battle!",
        parse_mode=types.ParseMode.HTML,
    )
    winner = None
    game_1 = game_2 = BullsAndCows()
    while winner is None:
        winner = await play_game(player_1, game_1)
        winner = await play_game(player_2, game_2)
    # объявить победителя и закончить сессию

async def play_game(player: types.Message, game: BullsAndCows):
    await player.answer(
        f"Put the number:",
        parse_mode=types.ParseMode.HTML,
    )
    # здесь читать число из чата, проверить и выдать результат в чат

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