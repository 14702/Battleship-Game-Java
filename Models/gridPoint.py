from abc import ABC, abstractproperty, abstractmethod


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "{}({}, {})".format(type(self), self.x, self.y)


class Water(Point):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.assignedPlayer = None
        self.assignedObject = None

    def __repr__(self):
        cell_width = 6
        if self.assignedObject:
            return "Player{}-BS{}({}, {})".format(self.assignedPlayer, self.assignedObject.id, self.x, self.y)

        if self.assignedPlayer:
            return "Player{}({}, {})".format(self.assignedPlayer, self.x, self.y)

        return "Water({}, {})".format(self.x, self.y)

class Island(Point):
    def __init__(self, x, y):
        super().__init__(x, y)