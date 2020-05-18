#!/usr/bin/env python

from functools import singledispatch
from collections import abc
import numbers
import html


@singledispatch
def htmlize(obj):
    content = html.escape(repr(obj))
    return '<pre>{}</pre>'.format(content)


# 各个专门函数使用 @«base_function».register(«type») 装饰。
@htmlize.register(str)  # 专门函数的名称无关紧要；_ 是个不错的选择，简单明了
def _(text):
    content = html.escape(text).replace('\n', '<br>\n')
    return '<p>{0}</p>'.format(content)


@htmlize.register(numbers.Integral)  # 为每个需要特殊处理的类型注册一个函数。numbers.Integral 是 int 的虚拟超类。
def _(n):
    return '<pre>{0} (0x{0:x})</pre>'.format(n)


@htmlize.register(tuple)  # 可以叠放多个 register 装饰器，让同一个函数支持不同类型。
@htmlize.register(abc.MutableSequence)
def _(seq):
    inner = '</li>\n<li>'.join(htmlize(item) for item in seq)
    return '<ul>\n<li>' + inner + '</li>\n</ul>'

# 只要可能，注册的专门函数应该处理抽象基类（如 numbers.Integral 和 abc.MutableSequence），不要处理具体实现（如 int 和 list）。这样，代码支
# 持的兼容类型更广泛。例如，Python 扩展可以子类化 numbers.Integral，使用固定的位数实现 int 类型。

# singledispatch 机制的一个显著特征是，你可以在系统的任何地方和任何模块中注册专门函数。如果后来在新的模块中定义了新的类型，可以轻松地添加一个新的
# 专门函数来处理那个类型。此外，你还可以为不是自己编写的或者不能修改的类添加自定义函数。

# 这个机制最好的文档是“PEP 443 — Single-dispatch generic functions”（https://www.python.org/dev/peps/pep-0443/）。

