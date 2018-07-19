import numpy as np


class Location:
    def __init__(self, x: int, y: int):
        self.loc = (x, y)

    def __gt__(self, other):
        if self[0] > other[0] or self[1] > other[1]:
            return True
        else:
            return False

    def __lt__(self, other):
        if self[0] < other[0] or self[1] < other[1]:
            return True
        else:
            return False

    def __eq__(self, other):
        if self[0] == other[0] and self[1] == other[1]:
            return True

    def __ge__(self, other):
        if self[0] >= other[0] or self[1] >= other[1]:
            return True
        else:
            return False

    def __add__(self, other):
        return Location(self[0] + other[0], self[1] + other[1])

    def __call__(self):
        return self.loc

    def __getitem__(self, item):
        return self.loc[item]

    def __hash__(self):
        return self.loc.__hash__()


_ = Location


class CheckerBoard:
    arrows = (
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1),
        (-1, 0),
        (-1, 1)
    )

    def __init__(self, size: tuple):
        self.size = size
        self.empty_locations = {_(i, j) for i in range(size[0]) for j in
                                range(size[1])}
        self.black_locations = set()
        self.white_locations = set()

    def __getitem__(self, location: Location):
        if location >= self.size or location < (0, 0):
            return np.nan
        if location in self.black_locations:
            return -1
        elif location in self.white_locations:
            return 1
        elif location in self.empty_locations:
            return 0
        else:
            return np.nan

    def __setitem__(self, location: Location, value: int):
        if location >= self.size or location < (0, 0):
            return False
        if value == 1:
            if location in self.empty_locations:
                self.empty_locations.remove(location)
            elif location in self.black_locations:
                self.black_locations.remove(location)
            self.white_locations.add(location)
        elif value == -1:
            if location in self.empty_locations:
                self.empty_locations.remove(location)
            elif location in self.white_locations:
                self.white_locations.remove(location)
            self.black_locations.add(location)
        elif value == 0:
            if location in self.black_locations:
                self.black_locations.remove(location)
            elif location in self.white_locations:
                self.white_locations.remove(location)
            self.empty_locations.add(location)
        else:
            raise Exception

    def __str__(self):
        boundary = "+" + "---+" * self.size[1] + "\n"
        board_string = boundary
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self[_(i, j)] == -1:
                    board_string += "| X "
                elif self[_(i, j)] == 1:
                    board_string += "| O "
                else:
                    board_string += "|   "
            board_string += "|\n"
            board_string += boundary
        return board_string

    def judge(self, color, win_length):
        if color == 1:
            locations = self.white_locations
        elif color == -1:
            locations = self.black_locations
        else:
            raise Exception
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                location = _(i, j)
                if location in locations:
                    length = 1
                    for arrow in self.arrows:
                        location = _(i, j) + arrow
                        while location in locations:
                            length += 1
                            if length >= win_length:
                                return True
                            location += arrow
        return False

    def move(self, color: int, location: Location):
        self.empty_locations.remove(location)
        if color == 1:
            self.white_locations.add(location)
        elif color == -1:
            self.black_locations.add(location)
        else:
            raise Exception


class Game:
    def __init__(self, size: tuple, win_length: int):
        self.win_length = win_length
        self.checkerboard = CheckerBoard(size)

    def __str__(self):
        return str(self.checkerboard)


if __name__ == "__main__":
    g = Game((9, 9), 3)
    print(g)
    g.checkerboard.move(1, _(1, 1))
    g.checkerboard.move(1, _(2, 2))
    g.checkerboard.move(1, _(0, 0))
    g.checkerboard.move(-1, _(2, 0))
    g.checkerboard.move(-1, _(0, 2))
    print(g)
    print(g.checkerboard.judge(1, 3))
    print(g.checkerboard.judge(-1, 3))
