#!/usr/bin/env python
from array import array
import reprlib
import math

# 我使用 reprlib.repr 的方式需要做些说明。这个函数用于生成大型结构或递归结构的安全表示形式，它会限制输出字符串的长度，用 '...' 表示截断的部分。
# 我希望 Vector实例的表示形式是 Vector([3.0, 4.0, 5.0]) 这样，而不是 Vector(array('d',[3.0, 4.0, 5.0]))，因为 Vector 实例中的数组是
# 实现细节

class Vector:
    typecode = 'd'

    def __init__(self, components):
        # self._components 是“受保护的”实例属性，把 Vector 的分量保存在一个数组中
        self._components = array(self.typecode, components)

    def __iter__(self):
        # 为了迭代，我们使用 self._components 构建一个迭代器
        return iter(self._components)

    def __repr__(self):
        # 使用 reprlib.repr() 函数获取 self._components 的有限长度表示形式（如array('d', [0.0, 1.0, 2.0, 3.0, 4.0, ...])
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        # 直接使用 self._components 构建 bytes 对象
        return bytes([ord(self.typecode)]) + bytes(self._components)

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)
