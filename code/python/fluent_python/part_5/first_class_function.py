#!/usr/bin/env python

import random

# 在 Python 中，函数是一等对象。编程语言理论家把“一等对象”定义为满足下述条件的程序实体：
# - 在运行时创建
# - 能赋值给变量或数据结构中的元素
# - 能作为参数传给函数
# - 能作为函数的返回结果

# 把函数视作对象
# 里我们创建了一个函数，然后调用它，读取它的 __doc__ 属性，并且确定函数对象本身是 function 类的实例。
"""
>>> def factorial(n): 
... '''returns n!'''
... return 1 if n < 2 else n * factorial(n-1)
...
>>> factorial(42)
1405006117752879898543142606244511569936384000000000
>>> factorial.__doc__ 
'returns n!'
>>> type(factorial) 
<class 'function'>
"""
# 通过别的名称使用函数，再把函数作为参数传递
"""
>>> fact = factorial
>>> fact
<function factorial at 0x...>
>>> fact(5)
120
>>> map(factorial, range(11))
<map object at 0x...>
>>> list(map(fact, range(11)))
[1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]
"""

# 高阶函数
# 接受函数为参数，或者把函数作为结果返回的函数是高阶函数（higher-order function）。map 函数就是一例。内置函数 sorted 也是：可选的 key 参数用
# 于提供一个函数，它会应用到各个元素上进行排序。
"""
>>> fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
>>> sorted(fruits, key=len)
['fig', 'apple', 'cherry', 'banana', 'raspberry', 'strawberry']
>>>
"""
# 任何单参数函数都能作为 key 参数的值。例如，为了创建押韵词典，可以把各个单词反过来拼写，然后排序。
"""
>>> def reverse(word):
... return word[::-1]
>>> reverse('testing')
'gnitset'
>>> sorted(fruits, key=reverse)
['banana', 'apple', 'fig', 'raspberry', 'strawberry', 'cherry']
>>>
"""
# map、filter和reduce的现代替代品。列表推导或生成器表达式具有 map 和 filter 两个函数的功能，而且更易于阅读。
# 在 Python 3 中，map 和 filter 返回生成器（一种迭代器），因此现在它们的直接替代品是生成器表达式（在 Python 2 中，这两个函数返回列表，因此最接
# 近的替代品是列表推导）。
# all 和 any 也是内置的归约函数。
# all(iterable)：如果 iterable 的每个元素都是真值，返回 True；all([]) 返回 True。
# any(iterable)：只要 iterable 中有元素是真值，就返回 True；any([]) 返回 False。

# 匿名函数
# 为了使用高阶函数，有时创建一次性的小型函数更便利。这便是匿名函数存在的原因。lambda 关键字在 Python 表达式内创建匿名函数。
# Python 简单的句法限制了 lambda 函数的定义体只能使用纯表达式。换句话说，lambda 函数的定义体中不能赋值，也不能使用 while 和 try 等 Python
# 语句。
# 使用 lambda 表达式反转拼写，然后依此给单词列表排序
"""
>>> fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
>>> sorted(fruits, key=lambda word: word[::-1])
['banana', 'apple', 'fig', 'raspberry', 'strawberry', 'cherry']
>>>
"""

# Lundh 提出的 lambda 表达式重构秘笈
# 如果使用 lambda 表达式导致一段代码难以理解，Fredrik Lundh 建议像下面这样重构。
# - 编写注释，说明 lambda 表达式的作用。
# - 研究一会儿注释，并找出一个名称来概括注释。
# - 把 lambda 表达式转换成 def 语句，使用那个名称来定义函数。
# - 删除注释。
# lambda 句法只是语法糖：与 def 语句一样，lambda 表达式会创建函数对象。这是Python 中几种可调用对象的一种。

# 可调用对象
# 除了用户定义的函数，调用运算符（即 ()）还可以应用到其他对象上。如果想判断对象能否调用，可以使用内置的 callable() 函数。Python 数据模型文档列出
# 了 7 种可调用对象。
# - 用户定义的函数:使用 def 语句或 lambda 表达式创建。
# - 内置函数:使用 C 语言（CPython）实现的函数，如 len 或 time.strftime。
# - 内置方法:使用 C 语言实现的方法，如 dict.get。
# - 方法:在类的定义体中定义的函数。
# - 类:调用类时会运行类的 __new__ 方法创建一个实例，然后运行 __init__ 方法，初始化实例，最后把实例返回给调用方。
# - 类的实例:如果类定义了 __call__ 方法，那么它的实例可以作为函数调用
# - 生成器函数:使用 yield 关键字的函数或方法。调用生成器函数返回的是生成器对象。

# 用户定义的可调用类型
# 不仅 Python 函数是真正的对象，任何 Python 对象都可以表现得像函数。为此，只需实现实例方法 __call__。


class BingoCage:
    """
    >>> bingo = BingoCage(range(3))
    >>> bingo.pick()
    1
    >>> bingo()
    0
    >>> callable(bingo)
    True
    """
    def __init__(self, items):
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self):
        return self.pick()

# 实现 __call__ 方法的类是创建函数类对象的简便方式，此时必须在内部维护一个状态，让它在调用之间可用，例如 BingoCage 中的剩余元素。装饰器就是这样。
# 装饰器必须是函数，而且有时要在多次调用之间“记住”某些事 [ 例如备忘（memoization），即缓存消耗大的计算结果，供后面使用 ]。
# 创建保有内部状态的函数，还有一种截然不同的方式——使用闭包。

# 函数内省
# 除了 __doc__，函数对象还有很多属性。使用 dir 函数可以探知 factorial 具有下述属性：
"""
>>> dir(factorial)
['__annotations__', '__call__', '__class__', '__closure__', '__code__',
'__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__',
'__format__', '__ge__', '__get__', '__getattribute__', '__globals__',
'__gt__', '__hash__', '__init__', '__kwdefaults__', '__le__', '__lt__',
'__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__',
'__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__',
'__subclasshook__']
>>>
"""
# 与用户定义的常规类一样，函数使用 __dict__ 属性存储赋予它的用户属性。这相当于一种基本形式的注解。一般来说，为函数随意赋予属性不是很常见的做法，但
# 是 Django 框架这么做了。
# 这篇 Django 文档中举了下述示例，把 short_description 属性赋予一个方法，Django 管理后台使用这个方法时，在记录列表中会出现指定的描述文本：
"""
def upper_case_name(obj):
return ("%s %s" % (obj.first_name, obj.last_name)).upper()
upper_case_name.short_description = 'Customer name'
"""
# 下面重点说明函数专有而用户定义的一般对象没有的属性。计算两个属性集合的差集便能得到函数专有属性列表
"""
>>> class C: pass 
>>> obj = C() 
>>> def func(): pass 
>>> sorted(set(dir(func)) - set(dir(obj))) 
['__annotations__', '__call__', '__closure__', '__code__', '__defaults__',
'__get__', '__globals__', '__kwdefaults__', '__name__', '__qualname__']
>>>
"""

# 从定位参数到仅限关键字参数
# Python 最好的特性之一是提供了极为灵活的参数处理机制，而且 Python 3 进一步提供了仅限关键字参数
# tag 函数用于生成 HTML 标签；使用名为 cls 的关键字参数传入“class”属性，这是一种变通方法


def tag(name, *content, cls=None, **attrs):
    """
    生成一个或多个HTML标签
    >>> tag('br')
    '<br />'
    >>> tag('p', 'hello')
    '<p>hello</p>'
    >>> print(tag('p', 'hello', 'world'))
    <p>hello</p>
    <p>world</p>
    >>> tag('p', 'hello', id=33)
    '<p id="33">hello</p>'
    >>> print(tag('p', 'hello', 'world', cls='sidebar'))
    <p class="sidebar">hello</p>
    <p class="sidebar">world</p>
    >>> tag(content='testing', name="img")
    '<img content="testing" />'
    >>> my_tag = {'name': 'img', 'title': 'Sunset Boulevard',
    ... 'src': 'sunset.jpg', 'cls': 'framed'}
    >>> tag(**my_tag)
    '<img class="framed" src="sunset.jpg" title="Sunset Boulevard" />'
    """
    if cls is not None:
        attrs['class'] = cls
    if attrs:
        attr_str = ''.join(' %s="%s"' % (attr, value) for attr, value in sorted(attrs.items()))
    else:
        attr_str = ''
    if content:
        return '\n'.join('<%s%s>%s</%s>' % (name, attr_str, c, name) for c in content)
    else:
        return '<%s%s />' % (name, attr_str)

# 仅限关键字参数是 Python 3 新增的特性。在示例 5-10 中，cls 参数只能通过关键字参数指定，它一定不会捕获未命名的定位参数。定义函数时若想指定仅限关
# 键字参数，要把它们放到前面有 * 的参数后面。如果不想支持数量不定的定位参数，但是想支持仅限关键字参数，在签名中放一个 *
"""
>>> def f(a, *, b):
... return a, b
...
>>> f(1, b=2)
(1, 2)
"""

# 函数注解
# Python 3 提供了一种句法，用于为函数声明中的参数和返回值附加元数据。
# def clip(text:str, max_len:'int > 0'=80) -> str:
# 注解不会做任何处理，只是存储在函数的 __annotations__ 属性（一个字典）中：
"""
>>> from clip_annot import clip
>>> clip.__annotations__
{'text': <class 'str'>, 'max_len': 'int > 0', 'return': <class 'str'>}
"""
# Python 对注解所做的唯一的事情是，把它们存储在函数的 __annotations__ 属性里。仅此而已，Python 不做检查、不做强制、不做验证，什么操作都不做。
# 换句话说，注解对Python 解释器没有任何意义。注解只是元数据，可以供 IDE、框架和装饰器等工具使用。

# 从函数签名中提取注解
"""
>>> from clip_annot import clip
>>> from inspect import signature
>>> sig = signature(clip)
>>> sig.return_annotation
<class 'str'>
>>> for param in sig.parameters.values():
... note = repr(param.annotation).ljust(13)
... print(note, ':', param.name, '=', param.default)
<class 'str'> : text = <class 'inspect._empty'>
'int > 0' : max_len = 80
"""
# signature 函数返回一个 Signature 对象，它有一个 return_annotation 属性和一个parameters 属性，后者是一个字典，把参数名映射到 Parameter
# 对象上。每个Parameter 对象自己也有 annotation 属性。
# 使用 price:float注解的参数可以自动把查询字符串转换成函数期待的 float 类型；quantity:'int > 0' 这样的字符串注解可以转换成对参数的验证。
# 函数注解的最大影响或许不是让 Bobo 等框架自动设置，而是为 IDE 和 lint 程序等工具中的静态类型检查功能提供额外的类型信息。

# 支持函数式编程的包
# operator模块
# 在函数式编程中，经常需要把算术运算符当作函数使用。例如，不使用递归计算阶乘。求和可以使用 sum 函数，但是求积则没有这样的函数。我们可以使用 reduce
# 函数（5.2.1节是这么做的），但是需要一个函数计算序列中两个元素之积。
"""
from functools import reduce
def fact(n):
    return reduce(lambda a, b: a*b, range(1, n+1))
"""
# operator 模块为多个算术运算符提供了对应的函数，从而避免编写 lambda a, b: a*b 这种平凡的匿名函数。
"""
from functools import reduce
from operator import mul
def fact(n):
    return reduce(mul, range(1, n+1))
"""

# operator 模块中还有一类函数，能替代从序列中取出元素或读取对象属性的 lambda 表达式：因此，itemgetter 和 attrgetter 其实会自行构建函数。
# itemgetter 的常见用途：根据元组的某个字段给元组列表排序。在这个示例中，按照国家代码（第 2 个字段）的顺序打印各个城市的信息。其实，
# itemgetter(1) 的作用与 lambda fields: fields[1] 一样：创建一个接受集合的函数，返回索引位 1 上的元素。
"""
>>> metro_data = [
... ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
... ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
... ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
... ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
... ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
... ]
>>>
>>> from operator import itemgetter
>>> for city in sorted(metro_data, key=itemgetter(1)):
...     print(city)
...
('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833))
('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889))
('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
('Mexico City', 'MX', 20.142, (19.433333, -99.133333))
('New York-Newark', 'US', 20.104, (40.808611, -74.020386))
"""
# 如果把多个参数传给 itemgetter，它构建的函数会返回提取的值构成的元组：
"""
>>> cc_name = itemgetter(1, 0)
>>> for city in metro_data:
...     print(cc_name(city))
...
('JP', 'Tokyo')
('IN', 'Delhi NCR')
('MX', 'Mexico City')
('US', 'New York-Newark')
('BR', 'Sao Paulo')
>>>
"""

# attrgetter 与 itemgetter 作用类似，它创建的函数根据名称提取对象的属性。如果把多个属性名传给 attrgetter，它也会返回提取的值构成的元组。此外，
# 如果参数名中包含 .（点号），attrgetter 会深入嵌套对象，获取指定的属性。
# 定义一个 namedtuple，名为 metro_data（与示例 5-23 中的列表相同），演示使用 attrgetter 处理它
"""
>>> from collections import namedtuple
>>> LatLong = namedtuple('LatLong', 'lat long') 
>>> Metropolis = namedtuple('Metropolis', 'name cc pop coord') 
>>> metro_areas = [Metropolis(name, cc, pop, LatLong(lat, long)) 
...                 for name, cc, pop, (lat, long) in metro_data]
>>> metro_areas[0]
Metropolis(name='Tokyo', cc='JP', pop=36.933, coord=LatLong(lat=35.689722,
long=139.691667))
>>> metro_areas[0].coord.lat 
35.689722
>>> from operator import attrgetter
>>> name_lat = attrgetter('name', 'coord.lat') 
>>>
>>> for city in sorted(metro_areas, key=attrgetter('coord.lat')): 
...     print(name_lat(city)) 
...
('Sao Paulo', -23.547778)
('Mexico City', 19.433333)
('Delhi NCR', 28.613889)
('Tokyo', 35.689722)
('New York-Newark', 40.808611)
"""
# operator中定义的部分函数
"""
>>> [name for name in dir(operator) if not name.startswith('_')]
['abs', 'add', 'and_', 'attrgetter', 'concat', 'contains',
'countOf', 'delitem', 'eq', 'floordiv', 'ge', 'getitem', 'gt',
'iadd', 'iand', 'iconcat', 'ifloordiv', 'ilshift', 'imod', 'imul',
'index', 'indexOf', 'inv', 'invert', 'ior', 'ipow', 'irshift',
'is_', 'is_not', 'isub', 'itemgetter', 'itruediv', 'ixor', 'le',
'length_hint', 'lshift', 'lt', 'methodcaller', 'mod', 'mul', 'ne',
'neg', 'not_', 'or_', 'pos', 'pow', 'rshift', 'setitem', 'sub',
'truediv', 'truth', 'xor']
"""

# methodcaller 创建的函数会在对象上调用参数指定的方法
"""
>>> from operator import methodcaller
>>> s = 'The time has come'
>>> upcase = methodcaller('upper')
>>> upcase(s)
'THE TIME HAS COME'
>>> hiphenate = methodcaller('replace', ' ', '-')
>>> hiphenate(s)
'The-time-has-come'
"""

# 使用functools.partial冻结参数
# functools.partial 这个高阶函数用于部分应用一个函数。部分应用是指，基于一个函数创建一个新的可调用对象，把原函数的某些参数固定。使用这个函数可以
# 把接受一个或多个参数的函数改编成需要回调的 API，这样参数更少
"""
>>> from operator import mul
>>> from functools import partial
>>> triple = partial(mul, 3) # 使用 mul 创建 triple 函数，把第一个定位参数定为 3。
>>> triple(7) 
21
>>> list(map(triple, range(1, 10))) 
[3, 6, 9, 12, 15, 18, 21, 24, 27]
"""

# 使用 partial 构建一个便利的 Unicode 规范化函数
"""
>>> import unicodedata, functools
>>> nfc = functools.partial(unicodedata.normalize, 'NFC')
>>> s1 = 'café'
>>> s2 = 'cafe\u0301'
>>> s1, s2
('café', 'café')
>>> s1 == s2
False
>>> nfc(s1) == nfc(s2)
True
"""

# 把 partial 应用到示例 5-10 中定义的 tag 函数上
"""
>>> from tagger import tag
>>> tag
<function tag at 0x10206d1e0> 
>>> from functools import partial
>>> picture = partial(tag, 'img', cls='pic-frame') 
>>> picture(src='wumpus.jpeg')
'<img class="pic-frame" src="wumpus.jpeg" />' 
>>> picture
functools.partial(<function tag at 0x10206d1e0>, 'img', cls='pic-frame') 
>>> picture.func 
<function tag at 0x10206d1e0>
>>> picture.args
('img',)
>>> picture.keywords
{'cls': 'pic-frame'}
"""
# functools.partialmethod 函数（Python 3.4 新增）的作用与 partial 一样，不过是用于处理方法的。

# functools 模块中的 lru_cache 函数令人印象深刻，它会做备忘（memoization），这是一种自动优化措施，它会存储耗时的函数调用结果，避免重新计算。
# 第 7 章将会介绍这个函数，还将讨论装饰器，以及旨在用作装饰器的其他高阶函数：singledispatch 和 wraps。


# ---------------------
# 小结
# 本章的目标是探讨 Python 函数的一等本性。这意味着，我们可以把函数赋值给变量、传给其他函数、存储在数据结构中，以及访问函数的属性，供框架和一些工具
# 使用。列表推导（以及类似的结构，如生成器表达式）以及sum、all 和 any 等内置的归约函数。Python 中常用的高阶函数有内置函数sorted、min、max 和
# functools. partial。
# Python 函数及其注解有丰富的属性，在 inspect 模块的帮助下，可以读取它们。例如，Signature.bind 方法使用灵活的规则把实参绑定到形参上，这与
# Python 使用的规则一样。

