from player import *
from checkerboard import CheckerBoard, Location as _


class Game:
    def __init__(self, size: tuple, p1,
                 p2):
        self.checkerboard = CheckerBoard(size)
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return str(self.checkerboard)

    def play(self):
        player = self.p1
        while True:
            try:
                loc = player.next_loc(self.checkerboard)
                self.checkerboard.move(player.color, loc)
            except Exception as ex:
                print(repr(ex))
                return 0
            if self.checkerboard.judge(player.color):
                return player.color
            player = self._next(player)

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


if __name__ == "__main__":
    import time

    # start = time.time()
    # print(caculate_win_times(10))
    # end = time.time()
    # print(end - start)
    p1 = MCTSPlayer(1, 500)
    p2 = Player(-1)
    g = Game((3, 3), p1, p2)
    print(g.play())
