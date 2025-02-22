from Models.battlefield import Battlefield
from Models.battleship import Battleship
from Models.player import Player
import json
from collections import deque
from strategy.firingStrategy import RandomFiringStrategy
from enums.firingStrategy import FiringStrategyEnum


class GameService:
    def __init__(self):
        self.battlefield = None
        self.players = deque()
        self.playersMap = {}
        self.firingStrategy = None

    def read_input(self, input_path):
        with open(input_path) as file:
            json_input = json.load(file)
        return json_input

    def initialize_strategy(self, json_input):
        all_points = []
        for i in range(self.battlefield.n):
            for j in range(self.battlefield.n):
                all_points.append([i,j])

        if json_input['firingStrategy'] == FiringStrategyEnum.RANDOM_FIRE_STRATEGY.value:
            self.firingStrategy = RandomFiringStrategy(all_points)
        else:
            raise Exception("Incorrect firing strategy")

    def init_game(self, path):
        json_input = self.read_input(path)

        n = json_input['n']
        self.battlefield = Battlefield(n)

        players_count = json_input['players']
        for i in range(players_count):
            p = Player(i+1, "Player{}".format(i+1))
            self.players.append(p)
            self.playersMap[i+1] = p

        player_ships = json_input['playersToShips']
        for player_id, ships in player_ships.items():
            for ship_id, ship in enumerate(ships):
                if Battleship.validate_battleship(n, ship['size'], ship['top_left_edge']):
                    bs = Battleship(ship_id+1, ship['size'], ship['top_left_edge'])
                    player = self.players[int(player_id)-1]
                    player.add_battleship(bs)
                    self.add_battleship_in_grid(bs)
                else:
                    raise Exception("Ship input invalid")

        self.divide_grid_among_players(n)
        self.initialize_strategy(json_input)
        self.battlefield.print_battlefield()
        self.play_game()

    def add_battleship_in_grid(self, battleship):
        for (x, y) in battleship.ship_points:
            grid_point = self.battlefield.grid[x][y]
            grid_point.assignedObject = battleship

    def divide_grid_among_players(self, n):
        for i in range(n):
            for j in range(n):
                point = self.battlefield.grid[i][j]
                if j < n//2:
                    point.assignedPlayer = self.players[0].id
                else:
                    point.assignedPlayer = self.players[1].id

    def check_game_end(self):
        for player in self.players:
            if not player.activeBattleships:
                print("Player{} has lost all battleships. Ending the game".format(player.id))
                return True

        return False

    def play_game(self):
        previous_point = [-1, -1]
        while not self.check_game_end():
            current_player = self.players.popleft()
            firing_position = self.firingStrategy.fire(current_player, self.battlefield, previous_point)
            print(firing_position)
            previous_point = firing_position
            if firing_position.assignedObject:
                print("Player{}'s turn: Missile fired at ({}, {}). 'Hit'. Player{}'s ship with id '{}' destroyed".format(
                    current_player.id, firing_position.x, firing_position.y, firing_position.assignedPlayer, firing_position.assignedObject.id))
                destroyed_ship = firing_position.assignedObject
                self.dfs(firing_position.x, firing_position.y, destroyed_ship)
                player = self.playersMap[firing_position.assignedPlayer]
                player.activeBattleships.remove(destroyed_ship.id)
                firing_position.assignedObject = None
            else:
                print("Player{}'s turn: Missile fired at ({}, {}). Miss".format(current_player.id, firing_position.x, firing_position.y))
            self.players.append(current_player)
            self.battlefield.print_battlefield()
            print(self.players)

    def dfs(self, x, y, ship):
        if x < 0 or y < 0 or x >= self.battlefield.n or y >= self.battlefield.n:
            return

        point = self.battlefield.grid[x][y]
        if not point.assignedObject or point.assignedObject.id != ship.id:
            return

        point.assignedObject = None
        self.dfs(x+1, y, ship)
        self.dfs(x-1, y, ship)
        self.dfs(x, y+1, ship)
        self.dfs(x, y-1, ship)


if __name__ == '__main__':
    input_file_path = '../input.json'
    game = GameService()
    game.init_game(input_file_path)