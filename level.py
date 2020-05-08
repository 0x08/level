import sys
import threading

from collections import deque
from time import sleep


class GameThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.shift = 1
        self.state = deque([0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0])
        self.previous = self.state.copy()
        self.speed = 0.2
        self.enter = False

    def run(self):

        self.print_line()
        print()

        while self.game_not_ended():

            self.go_to_next_line()
            self.change_direction()
            self.shift_line()
            self.print_line()

            sleep(self.speed)

    def game_not_ended(self):
        return any(self.state)

    def change_direction(self):
        if self.shift == 1 and self.state[-1] == 1:
            self.shift = -1
        elif self.state[0] == 1:
            self.shift = 1

    def shift_line(self):
        self.state.rotate(self.shift)

    def print_line(self):
        line = ""
        for i in self.state:
            line += "*" if i == 1 else " "
        print(line, end="\r", flush=True)

    def go_to_next_line(self):
        if self.enter:
            self.enter = False
            state = self.state
            self.state = deque([a and b for a, b in zip(self.state, self.previous)])
            self.previous = state

    def enter_pressed(self):
        self.enter = True


class InputThread(threading.Thread):
    def __init__(self, game):
        super().__init__()
        self.game = game

    def run(self):
        while self.game.game_not_ended():
            char = sys.stdin.read(1)
            if char == "\n":
                self.game.enter_pressed()


game_thread = GameThread()
input_thread = InputThread(game_thread)

game_thread.start()
input_thread.start()

game_thread.join()
input_thread.join()

print("well done!")
