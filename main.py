from game import Game
from player import *

import time

# start = time.time()
# print(caculate_win_times(10))
# end = time.time()
# print(end - start)
p1 = MCTSPlayer(1, 1000)
# p1 = DeepSearchPlayer(1, 4)
# p1 = Player(1)
p2 = HumanPlayer(-1)
g = Game((3, 3), p1, p2, 3)
print(g.play())
