from bulls_and_cows import NUMBER_LENGHT
from bot_config import LANGUAGE

HELLO_MESSAGE_TEXT = {
    "en" : "Play with me, {} 👋!",
    "ru" : "Сыграй со мной, {} 👋!"
}
RULES_TEXT = {
    "en" : """Maked a 4-digit secret number. The digits must be all different. Then the player tries to guess number using
the number of matches. The digits of the number guessed also must all be different. It is possible that zero is on the first position.
If the matching digits are in their right positions, they are "bulls", if in different positions, they are "cows".

Example:
Secret number: 4271
Player's try: 1234
Answer: 1 bull and 2 cows. (The bull is "2", the cows are "4" and "1".)""",
    "ru" : """Maked a 4-digit secret number. The digits must be all different. Then the player tries to guess number using
the number of matches. The digits of the number guessed also must all be different. It is possible that zero is on the first position.
If the matching digits are in their right positions, they are "bulls", if in different positions, they are "cows".

Example:
Secret number: 4271
Player's try: 1234
Answer: 1 bull and 2 cows. (The bull is "2", the cows are "4" and "1".)"""
}
PUT_THE_NUMBER_TEXT = {
    "en" : f"Put a {NUMBER_LENGHT}-digit number:",
    "ru" : f"Введите {NUMBER_LENGHT}-значное число"
}
WRONG_INPUT_TEXT = {
    "en" : "Wrong input! " + PUT_THE_NUMBER_TEXT[LANGUAGE],
    "ru" : "Неверный ввод! " + PUT_THE_NUMBER_TEXT[LANGUAGE]
}
GAME_STEP_TEXT = "{} : 🐂 {}    🐮 {}\n---------------\n"

SEARCHING_OPPONENT_TEXT = {
    "en" : "Searching opponent...",
    "ru" : "Поиск оппонента..."
}

BEGIN_PVP_GAME_TEXT = {
    "en" : "Your opponent is {} 👋! " + PUT_THE_NUMBER_TEXT[LANGUAGE],
    "ru" : "Ваш оппонент {} 👋! " + PUT_THE_NUMBER_TEXT[LANGUAGE]
}
BEGIN_SINGLE_GAME_TEXT = {
    "en" : "Let's go! " + PUT_THE_NUMBER_TEXT[LANGUAGE],
    "ru" : "Поехали! " + PUT_THE_NUMBER_TEXT[LANGUAGE]
}

WIN_TEXT = {
    "en" : "You win 👋!    Steps: {}",
    "ru" : "Ваша победа 👋!    Шагов: {}"
}
LOSE_TEXT = {
    "en" : "You lose 😢!",
    "ru" : "Вы проиграли 😢!"
}
