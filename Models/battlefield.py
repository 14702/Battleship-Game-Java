from Models.gridPoint import Water


class Battlefield:
    def __init__(self, n):
        self.n = n
        self.grid = [[Water(i, j) for j in range(self.n)] for i in range(self.n)]

    def print_battlefield(self):
        width = 20
        border = "+".join("-" * width for _ in range(self.n))
        print("+" + border + "+")  # Bottom border
        for i in range(self.n):
            row = self.grid[i]
            print("|" + "|".join("{!r:<{w}}".format(cell, w=width) for cell in row) + "|")

        print("+" + border + "+")  # Top border
