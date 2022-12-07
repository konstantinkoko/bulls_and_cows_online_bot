import random

class BullsAndCows:

    def __init__(self) -> None:
        self.number_lenght = 4
        self.number = self._number_generator()
    
    def check(self, candidate) -> dict:
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
        return result

    def _number_generator(self) -> tuple:
        seq = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        return tuple(random.choices(seq, k=self.number_lenght))

class Player:

    def __init__(self, player_id : str, number_for_opponent=None) -> None:
        
        self.player_id = player_id
        self.number_for_opponent = number_for_opponent
    
    #нужна валидация (на верхнем уровне)
    def set_number_for_opponent(self, number):

        self.number_for_opponent = number

class PvPSession:

    def __init__(self, player_1 : Player, player_2 : Player) -> None:
        
        self.game_1 = BullsAndCows(number=player_2.number_for_opponent)
        self.game_2 = BullsAndCows(number=player_1.number_for_opponent)
    

    def start(self) -> bool:
        pass

if __name__ == "__main__":

    number = '1246'
    bac = BullsAndCows(number=number)
    #print(bac._number_validator(number))
    #print(bac._number_generator())
    print(bac.check('1111'))
    
