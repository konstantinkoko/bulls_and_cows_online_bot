from bulls_and_cows import NUMBER_LENGHT

HELLO_MESSAGE_TEXT = "Play with me, {} 👋!"
RULS_MESSAGE_TEXT = "ПРАВИЛА"

WRONG_INPUT_TEXT = "Wrong input!"
PUT_THE_NUMBER_TEXT = f"Put a {NUMBER_LENGHT}-digit number:"
GAME_STEP_TEXT = "{} : 🐂 {}    🐮 {}\n---------------\n"

SEARCHING_OPPONENT_TEXT = "Searching opponent..."

BEGIN_PVP_GAME_TEXT = "Your opponent is {} 👋!  Put the number:"
BEGIN_SINGLE_GAME_TEXT = "Let's go! " + PUT_THE_NUMBER_TEXT

WIN_TEXT = "You win 👋!    Steps: {}"
LOSE_TEXT = "You lose 😢!"

RULLS_TEXT = """Maked a 4-digit secret number. The digits must be all different. Then the player try to guess number who gives
the number of matches. The digits of the number guessed also must all be different.
If the matching digits are in their right positions, they are "bulls", if in different positions, they are "cows".

Example:
Secret number: 4271
Player's try: 1234
Answer: 1 bull and 2 cows. (The bull is "2", the cows are "4" and "1".)"""