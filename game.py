from checkerboard import CheckerBoard


class Game:
    def __init__(self, size: tuple, p1, p2, win_length):
        self.checkerboard = CheckerBoard(size)
        self.p1 = p1
        self.p2 = p2
        self.win_length = min(size[0], win_length)

    def __str__(self):
        return str(self.checkerboard)

    def play(self):
        player = self.p1
        while len(self.checkerboard.empty_locations) > 0:
            try:
                loc = player.next_loc(self.checkerboard, self.win_length)
                self.checkerboard.move(player.color, loc)
                print(self.checkerboard)
            except Exception as ex:
                print(ex)
                return 0
            if self.checkerboard.judge(player.color, self.win_length):
                return player.color
            player = self._next(player)
        return 0

    def _next(self, player):
        if player == self.p1:
            return self.p2
        else:
            return self.p1

    def refresh(self):
        self.checkerboard = CheckerBoard(self.checkerboard.size)


def caculate_win_times(times, game):
    res = {1: 0, -1: 0, 0: 0}
    for i in range(times):
        res[game.play()] += 1
        print(g)
        game.refresh()
    return res
