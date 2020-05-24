#!/usr/bin/env python
from functools import reduce

# 构建乘积数组


class Solution:
    def multiply(self, A):
        B = []
        length = len(A)
        for i in range(length):
            tmp = A.pop(i)
            B.append(reduce(lambda a, b:a*b, A))
            A.insert(i, tmp)
        return B
