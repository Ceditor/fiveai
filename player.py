from checkerboard import CheckerBoard, Location as _
from MCTS import MCTSNode
import random
import numpy as np


class Player:
    def __init__(self, color):
        self.color = color

    def next_loc(self, checkerboard: CheckerBoard):
        if len(checkerboard.empty_locations) > 0:
            loc = random.sample(checkerboard.empty_locations, 1)[0]
            return loc
        else:
            raise Exception


class DeepSearchPlayer(Player):
    def __init__(self, color, deepth):
        super().__init__(color)
        self.deepth = deepth

    def next_loc(self, checkerboard: CheckerBoard):
        wins = {}
        board = checkerboard.to_numpy()
        if len(checkerboard.empty_locations) > 0:
            locations = set(checkerboard.empty_locations)
            for loc in locations:
                res = self.emulate(checkerboard, loc, self.color, self.deepth)
                checkerboard.from_numpy(board)
                wins[loc] = res
            return max(wins, key=lambda k: (wins[k][self.color] + 1) / (
                    sum(wins[k].values()) + 1))
        else:
            raise Exception

    def emulate(self, checkerboard: CheckerBoard, loc: _, color: int,
                deepth: int):
        res = {1: 0, -1: 0, 0: 0}
        checkerboard.move(color, loc)
        if checkerboard.judge(color):
            # win the game
            res[color] += 1
            return res
        elif deepth == 0:
            # random play
            player = player1 = Player(-color)
            player2 = Player(color)
            while True:
                try:
                    loc = player.next_loc(checkerboard)
                    checkerboard.move(player.color, loc)
                except:
                    res[0] += 1
                    return res
                if checkerboard.judge(player.color):
                    res[player.color] += 1
                    return res
                player = player == player1 and player2 or player1
        else:
            board = checkerboard.to_numpy()
            locations = set(checkerboard.empty_locations)
            if len(locations) > 0:
                for loc in locations:
                    result = self.emulate(checkerboard, loc, -color,
                                          deepth - 1)
                    res[0] += result[0]
                    res[1] += result[1]
                    res[-1] += result[-1]
                    checkerboard.from_numpy(board)
            else:
                return res
        return res


class MCTSPlayer(Player):
    def __init__(self, color, max_turns):
        super().__init__(color)
        self.max_turns = max_turns

    def next_loc(self, checkerboard: CheckerBoard):
        root = MCTSNode(checkerboard, checkerboard.to_numpy(),
                        self.color)
        current_node = root
        for i in range(self.max_turns):
            while not current_node.judge(-current_node.next_player):
                if len(current_node.children) < len(
                        current_node.legal_locations):
                    loc = current_node.legal_locations.pop()
                    checkerboard.move(current_node.next_player, loc)
                    state = checkerboard.to_numpy()
                    next_node = MCTSNode(current_node, state,
                                         -current_node.next_player)
                    current_node.children.append(next_node)
                    checkerboard.from_numpy(state)
                    res = self.simulate(current_node.next_player, checkerboard)
                    break
                current_state = checkerboard.to_numpy()
                next_node = current_node.best_child()

                checkerboard.from_numpy(current_state)
                current_node = next_node
            else:
                res = current_node.judge(-current_node.next_player)
            current_node.back_update(res)
        best_loc = (
                root.empty_locations - root.best_child().empty_locations).pop()
        return best_loc

    def simulate(self, color, checkerboard):
        board = checkerboard.to_numpy()
        player = player1 = Player(-color)
        player2 = Player(color)
        while True:
            if checkerboard.judge(player.color):
                checkerboard.from_numpy(board)
                return player.color
            try:
                loc = player.next_loc(checkerboard)
                checkerboard.move(player.color, loc)
            except:
                checkerboard.from_numpy(board)
                return 0

            player = player == player1 and player2 or player1
