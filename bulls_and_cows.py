import random
from bot_config import NUMBER_LENGHT

class BullsAndCows:

    def __init__(self) -> None:
        self.number_lenght = NUMBER_LENGHT
        self.number = self._number_generator()
        self.game_steps = {}
    
    def check(self, candidate: str) -> tuple:
        _candidate, status = self._number_validator(candidate)
        if status == "incorrect":
            return (candidate, status)
        result = {
            "bulls" : 0,
            "cows" : 0,
            }
        print(_candidate, self.number) # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        for i, elem in enumerate(_candidate):
            if elem == self.number[i]:
                result["bulls"] += 1
            elif elem in self.number:
                result["cows"] += 1
        self.game_steps[candidate] = result
        status = "win" if result["bulls"] == self.number_lenght else "game"
        return (self.game_steps, status)

    def _number_generator(self) -> tuple:
        seq = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        number = []
        for _ in range(self.number_lenght):
            elem = random.choice(seq)
            seq.remove(elem)
            number.append(elem)
        return tuple(number)
    
    def _number_validator(self, text: str) -> tuple:
        if len(_text := text.strip()) == self.number_lenght and _text.isdigit():
            status = "correct"
        else:
            status = "incorrect"
            _text = text
        return (_text, status)

class GameSession:

    def __init__(self, player, opponent) -> None:
        self.mode = "single" if opponent is None else "pvp"
        if self.mode == "single":
            self.player = player
            self.game = BullsAndCows()
        else:
            self.player_1 = player
            self.player_2 = opponent
            self.games = {
                self.player_1.chat_id : (game_1 := BullsAndCows()),
                self.player_2.chat_id : (game_2 := BullsAndCows())
            }            

    def check(self, number, chat_id) -> tuple:
        if self.mode == "single":
            result, status = self.game.check(number)
        else:
            result, status = self.games[chat_id].check(number)
        steps = len(result)
        if status == "win":
            if self.mode == "single":
                winner = self.player
                looser = None
            else:
                players_chat_id = self.games.keys()
                if list(players_chat_id)[0] == chat_id:
                    winner = self.player_1
                    looser = self.player_2
                else:
                    winner = self.player_2
                    looser = self.player_1
            result = {
                "winner" : winner,
                "looser" : looser
            }
        return (result, status, steps)
