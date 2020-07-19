#!/usr/bin/env python

import math
import doctest
from array import array


class Vector2d:
    """
    >>> v1 = Vector2d(3, 4)
    >>> x, y = v1
    >>> x, y
    (3.0, 4.0)
    >>> v1
    Vector2d(3.0,4.0)
    >>> v1_clone = eval(repr(v1))
    >>> v1 == v1_clone
    True
    >>> print(v1)
    (3.0, 4.0)
    >>> octets = bytes(v1)
    >>> octets
    b'd\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x10@'
    >>> abs(v1)
    5.0
    >>> bool(v1), bool(Vector2d(0, 0))
    (True, False)
    >>> format(Vector2d(1, 1), 'p')
    '<1.4142135623730951, 0.7853981633974483>'
    >>> format(Vector2d(1, 1), '.3ep')
    '<1.414e+00, 7.854e-01>'
    >>> format(Vector2d(1, 1), '0.5fp')
    '<1.41421, 0.78540>'
    """
    typecode = 'd'

    def __init__(self, x, y):
        # 把 x 和 y 转换成浮点数，尽早捕获错误，以防调用 Vector2d 函数时传入不当参数
        self.x = float(x)
        self.y = float(y)

    def __iter__(self):
        # 把 Vector2d 实例变成可迭代的对象，这样才能拆包（例如，x, y = my_vector）
        return (i for i in (self.x, self.y))

    def __repr__(self):
        # __repr__ 方法使用 {!r} 获取各个分量的表示形式，然后插值，构成一个字符串；因为 Vector2d 实例是可迭代的对象，所以 *self 会把 x 和 y
        # 分量提供给 format 函数。
        class_name = type(self).__name__
        # ！后面可以加s r a 分别对应str() repr() ascii() 作用是在填充前先用对应的函数来处理参数
        return "{}({!r},{!r})".format(class_name, *self)

    def __eq__(self, other):
        # 在两个操作数都是 Vector2d 实例时可用，不过拿 Vector2d 实例与其他具有相同数值的可迭代对象相比，结果也是 True（如Vector(3, 4) ==
        # [3, 4]）。这个行为可以视作特性，也可以视作缺陷。第 13 章讲到运算符重载时才能进一步讨论。
        return tuple(self) == tuple(other)

    def __str__(self):
        # 从可迭代的 Vector2d 实例中可以轻松地得到一个元组，显示为一个有序对。
        return str(tuple(self))

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __bytes__(self):
        return bytes([ord(self.typecode)]) + bytes(array(self.typecode, self))

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('p'):  # 如果格式代码以'p'结尾使用极坐标
            fmt_spec = fmt_spec[:-1]
            coords = (abs(self), self.angle())
            outer_fmt = '<{}, {}>'
        else:
            coords = self
            outer_fmt = '({}, {})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(*components)

    @classmethod
    def frombytes(cls, octets):  # 不用传入 self 参数；相反，要通过 cls 传入类本身。
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)  # 使用传入的 octets 字节序列创建一个 memoryview，然后使用 typecode 转换。
        return cls(*memv)  # 拆包转换后的 memoryview，得到构造方法所需的一对参数

    # 计算极坐标角度
    def angle(self):
        return math.atan2(self.y, self.x)


if __name__ == '__main__':
    test = Vector2d(1, 2)
    print(str(test))
    doctest.testmod()