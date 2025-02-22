from Models.battleship import Battleship


class Player:
    def __init__(self, player_id, name):
        self.id = player_id
        self.name = name
        self.battleships = []
        self.activeBattleships = set()

    def add_battleship(self, battleship: Battleship):
        self.battleships.append(battleship)
        self.activeBattleships.add(battleship.id)

    def __repr__(self):
        return "Player{}, activeBattleships: {}".format(self.id, self.activeBattleships)