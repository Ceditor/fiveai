import numpy


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

    def __str__(self):
        return str(self.loc)


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

    # def __getitem__(self, location: Location):
    #     if location >= self.size or location < (0, 0):
    #         return np.nan
    #     if location in self.black_locations:
    #         return -1
    #     elif location in self.white_locations:
    #         return 1
    #     elif location in self.empty_locations:
    #         return 0
    #     else:
    #         return np.nan
    #
    # def __setitem__(self, location: Location, value: int):
    #     if location >= self.size or location < (0, 0):
    #         return False
    #     if value == 1:
    #         if location in self.empty_locations:
    #             self.empty_locations.remove(location)
    #         elif location in self.black_locations:
    #             self.black_locations.remove(location)
    #         self.white_locations.add(location)
    #     elif value == -1:
    #         if location in self.empty_locations:
    #             self.empty_locations.remove(location)
    #         elif location in self.white_locations:
    #             self.white_locations.remove(location)
    #         self.black_locations.add(location)
    #     elif value == 0:
    #         if location in self.black_locations:
    #             self.black_locations.remove(location)
    #         elif location in self.white_locations:
    #             self.white_locations.remove(location)
    #         self.empty_locations.add(location)
    #     else:
    #         raise Exception

    def __str__(self):
        boundary = "+" + "---+" * self.size[1] + "\n"
        board_string = boundary
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if _(i, j) in self.black_locations:
                    board_string += "| X "
                elif _(i, j) in self.white_locations:
                    board_string += "| O "
                else:
                    board_string += "|   "
            board_string += "|\n"
            board_string += boundary
        return board_string

    def judge(self, color, win_length=3):
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
                    for arrow in self.arrows:
                        length = 1
                        location = _(i, j) + arrow
                        while location in locations:
                            length += 1
                            if length >= win_length:
                                return True
                            location += arrow
        return False

    def move(self, color: int, location: Location):
        if location in self.empty_locations:
            self.empty_locations.remove(location)
        else:
            raise Exception
        if color == 1:
            self.white_locations.add(location)
        elif color == -1:
            self.black_locations.add(location)
        else:
            raise Exception

    def to_numpy(self):
        board = numpy.zeros(self.size, dtype=int)
        for loc in self.black_locations:
            board[loc()] = -1
        for loc in self.white_locations:
            board[loc()] = 1
        return board

    def from_numpy(self, board):
        self.size = (board.shape[0], board.shape[1])
        self.white_locations = set()
        self.black_locations = set()
        self.empty_locations = set()
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if board[i, j] == 1:
                    self.white_locations.add(_(i, j))
                elif board[i, j] == -1:
                    self.black_locations.add(_(i, j))
                else:
                    self.empty_locations.add(_(i, j))
