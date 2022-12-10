import random

class BullsAndCows:

    def __init__(self) -> None:
        self.number_lenght = 4
        self.number = self._number_generator()
    
    def check(self, candidate) -> tuple:
        result = {
            "bulls" : 0,
            "cows" : 0
            }
        _candidate = self._number_validator(candidate)
        for i, elem in enumerate(_candidate):
            if elem == self.number[i]:
                result["bulls"] += 1
            elif elem in self.number:
                result["cows"] += 1
        win_status = True if result["bulls"] == self.number_lenght else False            
        return (result, win_status)

    def _number_generator(self) -> tuple:
        seq = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        return tuple(random.choices(seq, k=self.number_lenght))

class GameSession:

    def __init__(self, player_1: str, player_2: str) -> None:
        self.games = {
            player_1 : (game_1 := BullsAndCows()),
            player_2 : (game_2 := BullsAndCows())
        }

    def check(self, player, number) -> tuple:
        return self.games[player].check(number)

if __name__ == "__main__":

    number = '1246'
    bac = BullsAndCows(number=number)
    #print(bac._number_validator(number))
    #print(bac._number_generator())
    print(bac.check('1111'))
