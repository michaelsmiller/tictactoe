#!/usr/bin/env python

import time
from copy import deepcopy
from typing import List, Tuple
import numpy as np
import sys # for exit

from tictactoe.game import Entry, Coordinate, parse_input, fail
from tictactoe.graphics import MOVE_DOWN, MOVE_UP, MOVE_START, draw_board, entry_to_char, draw_board2, ncolors

options  = [Entry.X, Entry.O] # The valid options, in order
DIM = 3
index_domain = list(range(DIM))

runs : List[Tuple[Coordinate,Coordinate,Coordinate]]    = [
    # Horizontals
    ((0,0),(0,1),(0,2)),
    ((1,0),(1,1),(1,2)),
    ((2,0),(2,1),(2,2)),

    # Verticals
    ((0,0),(1,0),(2,0)),
    ((0,1),(1,1),(2,1)),
    ((0,2),(1,2),(2,2)),

    # Diagonals
    ((0,0),(1,1),(2,2)),
    ((2,0),(1,1),(0,2))
]

def main() -> None:
    # state is a numpy array of Entry
    state = np.full((3,3), Entry.EMPTY) # 3x3 grid of empty states

    turn = 0
    draw_board2(state) # default end="\n" and overwrite=False
    done = False
    while not done:
        print(" "*30, end="\r")
        print("Gimme your fucks: ", end="")
        row, col = parse_input(input())
        if row not in index_domain or col not in index_domain:
            fail(f"Coordinate ({col+1},{row+1}) not a square...YOU ASSHOLE")

        if state[row,col] != Entry.EMPTY:
            fail(f"({col+1},{row+1}) IS ALREADY THERE YOU BITCH")
        new_value = options[turn % 2]
        state[row,col] = new_value

        # draw_board(state, end=MOVE_DOWN+MOVE_START, overwrite=True)
        draw_board2(state, end=MOVE_DOWN+MOVE_START, overwrite=True)
        print(" "*20 + MOVE_START, end="") # Necessary to overwrite input line, since clear_line doesn't work

        # If no one claims the middle square on their first turn, abort the game
        # This rule is Gene's suggestion
        if turn == 1 and state[1,1] == Entry.EMPTY:
            fail("YOU FUCKING MORONS, GET A GRIP")

        # Check if all spaces filled
        if np.all(state != Entry.EMPTY):
            print("Good job coloring it in; you really stayed in the lines :)")
            done = True

        # check for winning by going through all possible runs and checking if any are made up of all X or O
        for run in runs:
            vals = [state[row, col] for (row,col) in run]
            if (v0 := vals[0]) != Entry.EMPTY and all([v == v0 for v in vals]):
                print(f"{entry_to_char[new_value]} wins! Yayyyy!\n({entry_to_char[options[(turn+1)%2]]}, did you really just let that happen?)", end=MOVE_UP+MOVE_START);
                # print("There is a winner", end=MOVE_START+MOVE_DOWN)
                for t in range(20):
                    color = t%ncolors
                    draw_board2(state, end=MOVE_DOWN+MOVE_START, overwrite=True, color=color)
                    print(MOVE_START, end=MOVE_DOWN)
                    time.sleep(0.2)

                done = True
        turn += 1

if __name__ == "__main__":
    main()
