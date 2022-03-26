#!/usr/bin/env python

from tictactoe.game import Entry, fail
import numpy as np

# Movement, only for UNIX systems probably
MOVE_UP    = "\x1b[1A"
MOVE_DOWN  = "\x1b[1B"
MOVE_RIGHT = "\x1b[1C"
MOVE_START = '\r'

CYAN    = '\033[36m'
MAGENTA = '\033[35m'
OTHER   = '\033[38m'
ENDC    = '\033[0m'

colors = [None, CYAN, MAGENTA, OTHER]
ncolors = len(colors)

entry_to_char = {
    Entry.EMPTY: " ",
    Entry.X    : "X",
    Entry.O    : "O"
}

def draw_board(state : np.ndarray, end : str="\n", overwrite : bool=False) -> None:
    assert state.shape == (3,3)
    horizontal = "-"*(state.shape[0]*2+1)
    # if we are overwriting, then that means something has already been written, and we need to move the cursor in place first
    if overwrite:
        print(8*MOVE_UP + MOVE_START, end="")
    for i in range(3):
        print(horizontal, end=end)
        print("|" + "|".join([entry_to_char[s] for s in state[i,:]]) + "|", end=end)
    print(horizontal, end=end)


def draw_board2(state : np.ndarray, end : str="\n", overwrite : bool=False, color : int = 0) -> None:
    with open("pototo/x.txt") as f:
        xstring = f.read().rstrip("\n")
    with open("pototo/o.txt") as f:
        ostring = f.read().rstrip("\n")
    h = len(xstring.split("\n"))
    w = len(xstring.split("\n")[0])
    blankstring = "\n".join([" "*w for _ in range(h)])

    xstring = np.char.asarray(list(xstring.replace("\n",""))).reshape((h,w))
    # xstring = np.char.asarray([MAGENTA+c+ENDC for c in xstring.replace("\n","")]).reshape((h,w))
    ostring = np.char.asarray(list(ostring.replace("\n",""))).reshape((h,w))
    blankstring = np.char.asarray(list(blankstring.replace("\n",""))).reshape((h,w))

    h = h+1
    w = w+2
    temparray = np.char.asarray(list(" "*h*w)).reshape((h,w))
    xarray = np.copy(temparray)
    oarray = np.copy(temparray)
    blankarray = np.copy(temparray)

    xarray[0:h-1, 1:w-1] = xstring
    oarray[0:h-1, 1:w-1] = ostring
    blankarray[0:h-1, 1:w-1] = blankstring

    array_map = {
        Entry.EMPTY : blankarray,
        Entry.X     : xarray,
        Entry.O     : oarray,
    }



    horizontal = "-"*(4 + w * 3)
    board_string = ""
    for _ in range(3):
        board_string += horizontal + "\n"
        line = "|" + "|".join([" "*w for x in range(3)]) + "|\n"
        board_string += line*h
    board_string += horizontal
    arr = np.chararray((3*h+4, len(horizontal)), unicode=False)
    for i, line in enumerate(board_string.split("\n")):
        for j, c in enumerate(line):
            arr[i,j] = c
            # print(c, type(c), type(arr[i,j]))

    i, j = 1, 2
    def augment(i, j, array):
        arr[i*(h+1)+1:i*(h+1)+h+1, j*(w+1)+1:j*(w+1)+w+1] = array

    for i in range(state.shape[0]):
        for j in range(state.shape[1]):
            augment(i, j, array_map[state[i,j]])

    if overwrite:
        print((h*3+5)*MOVE_UP + MOVE_START, end="")

    to_str = lambda x : x.decode("utf-8")
    n = arr.shape[0]
    for i in range(n):
        line = to_str(arr[i,:].tostring())
        if color != 0:
            print(colors[color] + line + ENDC, end=end)
        else:
            print(line, end=end)
