class Battleship:
    def __init__(self, ship_id, size, top_left_edge):
        self.id = ship_id
        self.size = size
        self.top_left_edge = top_left_edge
        self.ship_points = set()
        self._populate_points()
        self.isActive = True

    def _populate_points(self):
        x, y = self.top_left_edge
        for i in range(x, x + self.size):
            for j in range(y, y + self.size):
                self.ship_points.add((i,j))

    @staticmethod
    def validate_battleship(grid_size, size, top_left_edge):
        x, y = top_left_edge
        if x >= 0 and y >= 0 and x+size-1 < grid_size and y+size-1 < grid_size:
            return True

        return False