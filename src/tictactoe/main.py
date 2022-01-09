#!/usr/bin/env python

from copy import deepcopy
from typing import List, Tuple
from enum import Enum
import numpy as np
import sys # for exit

# Types

# Nice to have a dedicated type for this
class Entry(Enum):
    EMPTY =  0
    X     =  1
    O     = -1
Coordinate = Tuple[int,int] # for typing

def fail(*args, **kwargs):
    print("Error:", *args, **kwargs)
    sys.exit(1)

# Globals

MOVE_UP    = "\x1b[1A"
MOVE_DOWN  = "\x1b[1B"
MOVE_START = '\r'

entry_to_char = {
    Entry.EMPTY: " ",
    Entry.X    : "X",
    Entry.O    : "O"
}
options  = [Entry.X, Entry.O] # The valid options, in order
index_domain = list(range(3))

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


def draw_board(state : np.ndarray, end : str="\n", overwrite : bool=False) -> None:
    assert state.shape == (3,3)
    horizontal = "-------"
    # if we are overwriting, then that means something has already been written, and we need to move the cursor in place first
    if overwrite:
        print(8*MOVE_UP + MOVE_START, end="")
    for i in range(3):
        print(horizontal, end=end)
        print("|" + "|".join([entry_to_char[s] for s in state[i,:]]) + "|", end=end)
    print(horizontal, end=end)

def parse_input(s : str) -> Tuple[int, int]:
    try:
        val = int(s)
    except:
        fail("DID NOT ENTER A NUMBER, YOU MORON")
    return int(val/3), val%3

def main() -> None:
    state = np.full((3,3), Entry.EMPTY) # 3x3 grid of empty states

    turn = 0
    draw_board(state) # default end="\n" and overwrite=False
    done = False
    while not done:
        print("Gimme your fucks: ", end="")
        row, col = parse_input(input())
        if row not in index_domain or col not in index_domain:
            fail(f"Coordinate ({row},{col}) not a square...YOU ASSHOLE")

        current_value = state[row][col] # assigns row, col with := walrus operator
        if current_value != Entry.EMPTY:
            fail(f"{current} IS ALREADY THERE YOU BITCH")
        new_value = options[turn % 2]
        state[row,col] = new_value

        draw_board(state, end=MOVE_DOWN+MOVE_START, overwrite=True)
        print(" "*20 + MOVE_START, end="") # Necessary to overwrite input line, since clear_line doesn't work

        # If no one claims the middle square on their first turn, abort the game
        # This rule is Gene's suggestion
        if turn == 1 and state[1,1] == Entry.EMPTY:
            fail("YOU FUCKING MORONS, GET A GRIP")

        # Check if all spaces filled
        if np.all(state == Entry.EMPTY):
            print("Good job coloring it in; you really stayed in the lines :)")
            done = True

        # check for winning by going through all possible runs and checking if any are made up of all X or O
        for run in runs:
            vals = [state[row, col] for (row,col) in run]
            if (v0 := vals[0]) != Entry.EMPTY and all([v == v0 for v in vals]):
                print(f"{entry_to_char[new_value]} wins! Yayyyy!\n({entry_to_char[options[(turn+1)%2]]}, did you really just let that happen?)");
                done = True

        turn += 1

if __name__ == "__main__":
    print("FUCK")
    # main()
