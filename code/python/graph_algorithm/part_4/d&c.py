#!/usr/bin/env python

import doctest


def sum_dc(nums):
    """
    计算数组之和

    1、基线条件：数组为空或者数组剩余一个元素
    ２、如何缩小规模符合基线条件：每次从数组中拿出一个元素并与剩余数组的和相加并返回，问题从求长度为len(nums)长度的数组之和缩小为求len(nums)-1
    长度的数组之和，这样不断递归会达到基线条件

    这样实现存在一个问题会改变外部传入的数组的值
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


def count_dc(items):
    """
    计算列表包含的元素数

    1、基线条件：数组为空
    ２、如何缩小规模符合基线条件：每次从数组中拿出一个元素计数器加１返回计数器与更新后的数组长度之和，数组的长度在不断缩小直到为空达到基线条件
    :param items: list
    :return:
    >>> count_dc([])
    0
    >>> count_dc([1])
    1
    >>> count_dc([0 for i in range(10)])
    10
    """
    if not items:
        return 0
    else:
        items.pop(0)
        return 1 + count_dc(items)


def max_dc(nums):
    """
    找出列表中最大的数字

    1、基线条件：数组为空或长度为１
    ２、如何缩小规模符合基线条件：比较列表中第一个元素和数组中除第一个数字之外的最大值并返回较大的元素
    :param nums:　list
    :return:
    >>> max_dc([])
    -1
    >>> max_dc([0])
    0
    >>> max_dc([0, 0, 0, 0, 0])
    0
    >>> max_dc([1,2,1,2,3,4,1,2,3,4,5,5])
    5
    """
    if not nums:
        return -1
    elif len(nums) == 1:
        return nums[0]
    else:
        num = nums.pop(0)
        return num if num > max_dc(nums) else max_dc(nums)


def binary_search_dc(items):
    """
    二分查找

    １、基线条件：左端位置大于右端
    ２、如何缩小规模符合基线条件：不断根据中点位置数字和左右两端位置数字的大小更新左端位置和右端位置，直到左端位置大于右端
    :param items:
    :return:
    """


if __name__ == '__main__':
    doctest.testmod()
