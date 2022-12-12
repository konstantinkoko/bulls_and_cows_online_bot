import random

class BullsAndCows:

    def __init__(self) -> None:
        self.number_lenght = 4
        self.number = self._number_generator()
    
    def check(self, candidate: str) -> tuple:
        _candidate, status = self._number_validator(candidate)
        if status == "incorrect":
            return (candidate, status)
        result = {
            "bulls" : 0,
            "cows" : 0
            }
        print(_candidate, self.number) # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        for i, elem in enumerate(_candidate):
            if elem == self.number[i]:
                result["bulls"] += 1
            elif elem in self.number:
                result["cows"] += 1
        status = "win" if result["bulls"] == self.number_lenght else "game"
        return (result, status)

    def _number_generator(self) -> tuple:
        seq = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        return tuple(random.choices(seq, k=self.number_lenght))
    
    def _number_validator(self, text: str) -> tuple:
        if len(_text := text.strip()) == self.number_lenght and _text.isdigit():
            status = "correct"
        else:
            status = "incorrect"
            _text = text
        return (_text, status)

class GameSession:

    def __init__(self, player_1, player_2) -> None:
        self.player_1 = player_1
        self.player_2 = player_2
        self.games = {
            player_1.chat_id : (game_1 := BullsAndCows()),
            player_2.chat_id : (game_2 := BullsAndCows())
        }

    def check(self, chat_id, number) -> tuple:
        result, status = self.games[chat_id].check(number)
        if status == "win":
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
        return (result, status)

