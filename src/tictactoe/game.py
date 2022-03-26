#!/usr/bin/env python

import sys
from enum import Enum
from typing import Tuple

Coordinate = Tuple[int, int] # for typing

# Nice to have a dedicated type for this
class Entry(Enum):
    EMPTY =  0
    X     =  1
    O     = -1

def fail(*args, **kwargs):
    print("Error:", *args, **kwargs)
    sys.exit(1)


def parse_input(s : str) -> Coordinate:
    def get_number(s : str) -> int:
        try:
            val = int(s)
        except:
            fail(f"{s} IS NOT A NUMBER, YOU MORON")
        return val

    s = s.replace(","," ")
    match len(split := s.split()):
        case 1: # flattened array index
            val = get_number(s)
            return int(val/3), val%3
        case 2: # 2D index, which is what we want anyway
            return get_number(split[1])-1, get_number(split[0])-1
        case n:
            fail(f"Input '{s}' has {n} numbers, not allowed")


