#!/usr/bin/env python

import bisect
import sys
import random

# bisect 的表现可以从两个方面来调教。
# 首先可以用它的两个可选参数——lo 和 hi——来缩小搜寻的范围。lo 的默认值是 0，hi的默认值是序列的长度，即 len() 作用于该序列的返回值。其次，bisect
# 函数其实是 bisect_right 函数的别名，后者还有个姊妹函数叫bisect_left。它们的区别在于，bisect_left 返回的插入位置是原序列中跟被插入元素相等的
# 元素的位置也就是新元素会被放置于它相等的元素的前面，而 bisect_right返回的则是跟它相等的元素之后的位置。这个细微的差别可能对于整数序列来讲没什么用
# ，但是对于那些值相等但是形式不同的数据类型来讲，结果就不一样了。比如说虽然 1== 1.0 的返回值是 True，1 和 1.0 其实是两个不同的元素。图 2-5 显示
# 的是用bisect_left 来运行上述示例的结果。


HAYSTACK = [1, 4, 5, 6, 8, 12, 15, 20, 21, 23, 23, 26, 29, 30]
NEEDLES = [0, 1, 2, 5, 8, 10, 22, 23, 29, 30, 31]
ROW_FMT = '{0:2d} @ {1:2d}     {2}{0:<2d}'


def demo(bisect_fn):
    for needle in reversed(NEEDLES):
        position = bisect_fn(HAYSTACK, needle)
        offset = position * ' | '
        print(ROW_FMT.format(needle, position, offset))


# bisect 可以用来建立一个用数字作为索引的查询表格，比如说把分数和成绩 对应起来:
def grade(score, breakpoints=[60, 70, 80, 90], grades='FDCBA'):
    """
    >>> [grade(score) for score in [33, 99, 77, 70, 89, 90, 100]]
    ['F', 'A', 'C', 'C', 'B', 'A', 'A']
    """
    i = bisect.bisect(breakpoints, score)
    return grades[i]

# 用bisect.insort插入新元素
# insort(seq, item) 把变量 item 插入到序列 seq 中，并能保持 seq 的升序顺序。详见示例 2-19 和它在图 2-6 里的输出。


SIZE = 7
random.seed(1729)
my_list = []
for i in range(SIZE):
    new_item = random.randrange(SIZE*2)
    bisect.insort(my_list, new_item)
    print('%2d ->' % new_item, my_list)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    if sys.argv[-1] == 'left':
        bisect_fn = bisect.bisect_left
    else:
        bisect_fn = bisect.bisect
    print('DEMO:', bisect_fn.__name__)
    print('haystack ->', ' '.join('%2d' % n for n in HAYSTACK))
    demo(bisect_fn)


