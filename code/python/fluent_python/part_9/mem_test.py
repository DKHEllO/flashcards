#!/usr/bin/env python

import sys

import vector2d_v3
import vector2d_v3_slot

if len(sys.argv) == 2:
    if sys.argv[1] == 'vector2d_v3.py':
        [vector2d_v3.Vector2d(1, 2) for _ in range(10000000)]
    elif sys.argv[1] == 'vector2d_v3_slot.py':
        [vector2d_v3_slot.Vector2d(1, 2) for _ in range(10000000)]
    else:
        print('not support file')

