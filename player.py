from checkboard import CheckerBoard, Location as _
import random


class Player:
    def __init__(self, color):
        self.color = color

    def next_loc(self, checkboard: CheckerBoard):
        if len(checkboard.empty_locations) > 0:
            loc = random.sample(checkboard.empty_locations, 1)
            return loc[0]
        else:
            raise Exception
