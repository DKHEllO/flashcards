#!/usr/bin/env python

# 二位数组中的查找
# 在一个二维数组中（每个一维数组的长度相同），每一行都按照从左到右递增的顺序排序，每一列都按照从上到下递增的顺序排序。请完成一个函数，输入这样的一个二
# 维数组和一个整数，判断数组中是否含有该整数。


class Solution:
    # array 二维列表

    def Find(self, target, array):
        # write code here
        row = array[0]
        start = 0
        end = len(row) - 1
        mid = (start + end) // 2
        while start <= end:
            if target > row[mid]:
                start = mid + 1
            elif target < row[mid]:
                end = mid - 1
            else:
                return True
            mid = (start + end) // 2
        col = end
        for i in range(col + 1):
            tmp = [j[i] for j in array]
            start = 0
            end = len(array) - 1
            mid = (start + end) // 2
            while start <= end:
                if target > tmp[mid]:
                    start = mid + 1
                elif target < tmp[mid]:
                    end = mid - 1
                else:
                    return True
                mid = (start + end) // 2
        return False

