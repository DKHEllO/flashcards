#!/usr/bin/env python

import doctest


def sum_dc(nums):
    """
    1、基线条件：数组为空或者数组剩余一个元素
    ２、如何缩小规模符合基线条件：每次从数组中拿出一个元素并与剩余数组的和相加，问题从求长度为len(nums)长度的数组之和缩小为求len(nums)-1长度的数
    组之和，这样不断递归会达到基线条件
    :param nums:
    :return:
    >>> sum_dc([])
    0
    >>> sum_dc([1])
    1
    >>> sum_dc([1,2,3,4])
    10
    """
    if not nums:
        return 0
    elif len(nums) == 1:
        return nums[0]
    else:
        num = nums.pop(0)
        return num + sum_dc(nums)


if __name__ == '__main__':
    doctest.testmod()
