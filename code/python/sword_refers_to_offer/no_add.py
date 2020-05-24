#!/usr/bin/env python

# 不用加减乘除做加法


class Solution:
    def Add(self, num1, num2):
        if (num1 < 0 and num2 > 0) or (num2 < 0 and num1 > 0):
            symbol = ''
            abs_num1 = abs(num1)
            abs_num2 = abs(num2)
            if (abs_num1 < abs_num2 and num1 < 0) or (abs_num1 > abs_num2 and num1 > 0):
                symbol = ''
            else:
                symbol = '-'
            num1_bin = [int(i) for i in bin(abs_num1)[2:]]
            num2_bin = [int(i) for i in bin(abs_num2)[2:]]
            res = []
            if len(num1_bin) < len(num2_bin):
                for i in range(len(num2_bin) - len(num1_bin)):
                    num1_bin.insert(0, 0)
            else:
                for i in range(len(num1_bin) - len(num2_bin)):
                    num2_bin.insert(0, 0)
            if abs_num1 < abs_num2:
                big = num2_bin
                small = num1_bin
            else:
                big = num1_bin
                small = num2_bin
            print(big)
            print(small)
            for i in range(len(num1_bin) - 1, -1, -1):
                if big[i] < small[i]:
                    count = i - 1
                    while count >= 0:
                        if big[count] == 1:
                            big[count] = 0
                            for j in range(count + 1, i + 1):
                                big[j] = 1
                            break
                        else:
                            count -= 1
                    res.insert(0, 1)
                else:
                    tmp = big[i] - small[i]
                    res.insert(0, tmp)
                print(i, big)
                print(res)
            res = [str(i) for i in res]
            r = int(''.join(res), 2)
            if symbol == '-':
                return -r
            else:
                return r
        else:
            if num1 >= 0 and num2 >= 0:
                symbol = ''
            else:
                symbol = '-'
            num1 = abs(num1)
            num2 = abs(num2)
            num1_bin = [int(i) for i in bin(num1)[2:]]
            num2_bin = [int(i) for i in bin(num2)[2:]]
            if len(num1_bin) < len(num2_bin):
                for i in range(len(num2_bin) - len(num1_bin)):
                    num1_bin.insert(0, 0)
            else:
                for i in range(len(num1_bin) - len(num2_bin)):
                    num2_bin.insert(0, 0)
            print(num1_bin)
            print(num2_bin)
            res = []
            decade = 0
            for i in range(len(num1_bin)-1, -1, -1):
                residue = (num1_bin[i] + num2_bin[i] + decade) % 2
                decade = (num1_bin[i] + num2_bin[i] + decade) // 2
                res.insert(0, residue)
                print(residue, decade, res)
            res.insert(0, decade)
            res = [str(i) for i in res]
            if symbol == '-':
                return -int(''.join(res), 2)
            else:
                return int(''.join(res), 2)


