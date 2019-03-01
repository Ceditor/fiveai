from checkerboard import CheckerBoard, Location
from MCTS import MCTSNode
import random


class Player:
    def __init__(self, color: int):
        self.color = color

    def next_loc(self, checkerboard: CheckerBoard, win_length: int) -> Location:
        if len(checkerboard.empty_locations) > 0:
            loc = random.sample(checkerboard.empty_locations, 1)[0]
            return loc
        else:
            raise Exception


class DeepSearchPlayer(Player):
    def __init__(self, color, depth):
        super().__init__(color)
        self.depth = depth

    def next_loc(self, checkerboard: CheckerBoard, win_length: int) -> Location:
        wins = {}
        state = checkerboard.state
        if len(checkerboard.empty_locations) > 0:
            locations = set(checkerboard.empty_locations)
            for loc in locations:
                res = self.simulate(checkerboard, loc, self.color, self.depth, win_length)
                checkerboard.state = state
                wins[loc] = res
                print(loc, res)
            return min(wins, key=lambda k: (wins[k][-1 * self.color]) / (
                    sum(wins[k].values())))
        else:
            raise Exception

    def simulate(self, checkerboard: CheckerBoard, loc: Location, color: int,
                 depth: int, win_length: int):
        res = {1: 0, -1: 0, 0: 0}
        checkerboard.move(color, loc)
        if checkerboard.judge(color, win_length):
            # win the game
            res[color] += 1
            return res
        elif depth == 0:
            # random play
            player = player1 = Player(-color)
            player2 = Player(color)
            while True:
                try:
                    loc = player.next_loc(checkerboard, win_length)
                    checkerboard.move(player.color, loc)
                except:
                    res[0] += 1
                    return res
                if checkerboard.judge(player.color, win_length):
                    res[player.color] += 1
                    return res
                player = player == player1 and player2 or player1
        else:
            state = checkerboard.state
            locations = set(checkerboard.empty_locations)
            if len(locations) > 0:
                for loc in locations:
                    result = self.simulate(checkerboard, loc, -color, depth - 1, win_length)
                    res[0] += result[0]
                    res[1] += result[1]
                    res[-1] += result[-1]
                    checkerboard.state = state
            else:
                return res
        return res


class MCTSPlayer(Player):
    def __init__(self, color, max_turns):
        super().__init__(color)
        self.max_turns = max_turns

    def next_loc(self, checkerboard: CheckerBoard, win_length: int) -> Location:
        root = MCTSNode(checkerboard, checkerboard.state, self.color)
        for i in range(self.max_turns):
            current_node = root
            while not current_node.judge(-current_node.next_player, win_length) and len(
                    current_node.empty_locations) > 0:
                if len(current_node.children) < len(
                        current_node.empty_locations):
                    next_node = current_node.expansion()
                    res = self.simulate(-next_node.next_player, next_node, win_length)
                    break
                else:
                    next_node = current_node.selection()
                    current_node = next_node
            else:
                if current_node.judge(-current_node.next_player):
                    res = -current_node.next_player
                else:
                    res = 0

            current_node.back_update(res)

        best_loc = (
                root.empty_locations - root.selection().empty_locations).pop()
        return best_loc

    @staticmethod
    def simulate(color, checkerboard, win_length):
        state = checkerboard.state
        player = player1 = Player(-color)
        player2 = Player(color)
        while True:
            if checkerboard.judge(player.color, win_length):
                checkerboard.state = state
                return player.color
            try:
                loc = player.next_loc(checkerboard, win_length)
                checkerboard.move(player.color, loc)
            except:
                checkerboard.state = state
                return 0

            player = player == player1 and player2 or player1


class HumanPlayer(Player):
    def __init__(self, color, max_waiting_times=60):
        super().__init__(color)
        self.max_waiting_times = max_waiting_times

    def next_loc(self, checkerboard: CheckerBoard, win_length: int) -> Location:
        while True:
            input_str = input("Input Loc, like 0,0")
            loc_str = input_str.split(',')
            if len(loc_str) == 2:
                loc = Location(int(loc_str[0].strip()), int(loc_str[1].strip()))
                if loc not in checkerboard.empty_locations:
                    print("Can't loc here")
                else:
                    return loc
            else:
                print("Error Input")
