#!/usr/bin/env python

# 名称不是对象，而是单独的东西。本章先以一个比喻说明 Python 的变量：变量是标注，而不是盒子。如果你不知道引用式变量是什么，可以像这样对别人解释别名。
# - 本章讨论对象标识、值和别名等概念
# - 本章会揭露元组的一个神奇特性：元组是不可变的，但是其中的值可以改变，之后就引申到浅复制和深复制
# - 引用和函数参数：可变的参数默认值导致的问题，以及如何安全地处理函数的调用者传入的可变参数。
# - 垃圾回收、del 命令，以及如何使用弱引用“记住”对象，而无需对象本身存在。

# 首先，我们要抛弃变量是存储数据的盒子这一错误观念。

# 变量不是盒子
# Python 变量类似于 Java 中的引用式变量，因此最好把它们理解为附加在对象上的标注。
# 变量 a 和 b 引用同一个列表，而不是那个列表的副本
"""
>>> a = [1, 2, 3]
>>> b = a
>>> a.append(4)
>>> b
[1, 2, 3, 4]
"""
# 对引用式变量来说，说把变量分配给对象更合理，反过来说就有问题。

# 创建对象之后才会把变量分配给对象
"""
>>> class Gizmo:
... def __init__(self):
... print('Gizmo id: %d' % id(self))
...
>>> x = Gizmo()
Gizmo id: 4301489152 
>>> y = Gizmo() * 10 
Gizmo id: 4301489432 
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for *: 'Gizmo' and 'int'
>>>
>>> dir() # dir() 函数不带参数时，返回当前范围内的变量、方法和定义的类型列表；带参数时，返回参数的属性、方法列表。如果参数包含方法__dir__()， 
          # 该方法将被调用。如果参数不包含__dir__()，该方法将最大限度地收集参数信息。
['Gizmo', '__builtins__', '__doc__', '__loader__', '__name__', '__package__', '__spec__', 'x']
"""

# 为了理解 Python 中的赋值语句，应该始终先读右边。对象在右边创建或获取，在此之后左边的变量才会绑定到对象上，这就像为对象贴上标注。因为变量只不过是标
# 注，所以无法阻止为对象贴上多个标注。贴的多个标注，就是别名

# 标识、相等性和别名
# charles 和 lewis 指代同一个对象
"""
>>> charles = {'name': 'Charles L. Dodgson', 'born': 1832}
>>> lewis = charles  # lewis 是 charles 的别名
>>> lewis is charles
True
>>> id(charles), id(lewis) 
(4300473992, 4300473992)
>>> lewis['balance'] = 950 # 向 lewis 中添加一个元素相当于向 charles 中添加一个元素。
>>> charles
{'name': 'Charles L. Dodgson', 'balance': 950, 'born': 1832}
"""

# 然而，假如有冒充者（姑且叫他 Alexander Pedachenko 博士）生于 1832 年，声称他是Charles L. Dodgson。这个冒充者的证件可能一样，但是
# Pedachenko 博士不是 Dodgson 教授。
# alex 与 charles 比较的结果是相等，但 alex 不是 charles
"""
>>> alex = {'name': 'Charles L. Dodgson', 'born': 1832, 'balance': 950} 
>>> alex == charles # 比较两个对象，结果相等，这是因为 dict 类的 __eq__ 方法就是这样实现的。
True
>>> alex is not charles # 但它们是不同的对象
True
"""

# alex 不是 charles 的别名，因为二者绑定的是不同的对象。alex 和　charles 绑定的对象具有相同的值（== 比较的就是值），但是它们的标识不同。
# 每个变量都有标识、类型和值。对象一旦创建，它的标识绝不会变；你可以把标识理解为对象在内存中的地址。is 运算符比较两个对象的标识；id() 函数返回对象标
# 识的整数表示。
# 在 CPython 中，id() 返回对象的内存地址，但是在其他 Python 解释器中可能是别的值。关键是，ID 一定是唯一的数值标注，而且在对象的生命周期中绝不会变。

# 在==和is之间选择
# == 运算符比较两个对象的值（对象中保存的数据），而 is 比较对象的标识。
# 在变量和单例值之间比较时，应该使用 is
# is 运算符比 == 速度快，因为它不能重载，所以 Python 不用寻找并调用特殊方法，而是直接比较两个整数 ID。而 a == b 是语法糖，等同于 a.__eq__(b)。
# 继承自 object 的__eq__ 方法比较两个对象的 ID，结果与 is 一样。但是多数内置类型使用更有意义的方式覆盖了 __eq__ 方法，会考虑对象属性的值。
# 相等性测试可能涉及大量处理工作，例如，比较大型集合或嵌套层级深的结构时。

# 元组的相对不可变性
# 元组与多数 Python 集合（列表、字典、集，等等）一样，保存的是对象的引用(而 str、bytes 和 array.array 等单一类型序列是扁平的，它们保存的不是引
# 用，而是在连续的内存中保存数据本身（字符、字节和数字）。)。如果引用的元素是可变的，即便元组本身不可变，元素依然可变。也就是说，元组的不可变性其实是
# 指 tuple 数据结构的物理内容（即保存的引用）不可变，与引用的对象无关。
# 元组的值会随着引用的可变对象的变化而变。元组中不可变的是元素的标识。
"""
>>> t1 = (1, 2, [30, 40]) # t1 不可变，但是 t1[-1] 可变。
>>> t2 = (1, 2, [30, 40]) 
>>> t1 == t2 
True
>>> id(t1[-1]) # 查看 t1[-1] 列表的标识。
4302515784
>>> t1[-1].append(99) 
>>> t1
(1, 2, [30, 40, 99])
>>> id(t1[-1]) # t1[-1] 的标识没变，只是值变了。
4302515784
>>> t1 == t2 
False
"""
# 元组的相对不可变性解释了 2.6.1 节的谜题。这也是有些元组不可散列（参见 3.1 节中的“什么是可散列的数据类型”附注栏）的原因
# 复制对象时，相等性和标识之间的区别有更深入的影响


# 默认做浅复制
# 复制列表（或多数内置的可变集合）最简单的方式是使用内置的类型构造方法。
"""
>>> l1 = [3, [55, 44], (7, 8, 9)]
>>> l2 = list(l1) # list(l1) 创建 l1 的副本。
>>> l2
[3, [55, 44], (7, 8, 9)]
>>> l2 == l1 
True
>>> l2 is l1 # 但是二者指代不同的对象。对列表和其他可变序列来说，还能使用简洁的 l2 = l1[:]语句创建副本。
False
"""
# 然而，构造方法或 [:] 做的是浅复制（即复制了最外层容器，副本中的元素是源容器中元素的引用）。如果有可变的元素，可能就会导致意想不到的问题。
"""
l1 = [3, [66, 55, 44], (7, 8, 9)]
l2 = list(l1) 
l1.append(100) 
l1[1].remove(55) 
print('l1:', l1)
print('l2:', l2)
l2[1] += [33, 22] # 对可变的对象来说，如 l2[1] 引用的列表，+= 运算符就地修改列表。这次修改在 l1[1] 中也有体现，因为它是 l2[1] 的别名。
l2[2] += (10, 11) # 对元组来说，+= 运算符创建一个新元组，然后重新绑定给变量 l2[2]。这等同于l2[2] = l2[2] + (10, 11)。
print('l1:', l1)
print('l2:', l2)

输出
l1: [3, [66, 44], (7, 8, 9), 100]
l2: [3, [66, 44], (7, 8, 9)]
l1: [3, [66, 44, 33, 22], (7, 8, 9), 100]
l2: [3, [66, 44, 33, 22], (7, 8, 9, 10, 11)]
"""

# 为任意对象做深复制和浅复制
# 浅复制没什么问题，但有时我们需要的是深复制（即副本不共享内部对象的引用）。copy 模块提供的 deepcopy 和 copy 函数能为任意对象做深复制和浅复制。
# 为了演示 copy() 和 deepcopy() 的用法，示例 8-8 定义了一个简单的类，Bus。这个类表示运载乘客的校车，在途中乘客会上车或下车。


class Bus:
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = list(passengers)

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)


# 使用 copy 和 deepcopy 产生的影响
"""
>>> import copy
>>> bus1 = Bus(['Alice', 'Bill', 'Claire', 'David'])
>>> bus2 = copy.copy(bus1)
>>> bus3 = copy.deepcopy(bus1)
>>> id(bus1), id(bus2), id(bus3)
(4301498296, 4301499416, 4301499752) 
>>> bus1.drop('Bill')
>>> bus2.passengers
['Alice', 'Claire', 'David'] 
>>> id(bus1.passengers), id(bus2.passengers), id(bus3.passengers)
(4302658568, 4302658568, 4302657800) 
>>> bus3.passengers
['Alice', 'Bill', 'Claire', 'David'] 
"""

# 注意，一般来说，深复制不是件简单的事。如果对象有循环引用，那么这个朴素的算法会进入无限循环
# 循环引用：b 引用 a，然后追加到 a 中；deepcopy 会想办法复制 a
"""
>>> a = [10, 20]
>>> b = [a, 30]
>>> a.append(b)
>>> a
[10, 20, [[...], 30]]
>>> from copy import deepcopy
>>> c = deepcopy(a)
>>> c
[10, 20, [[...], 30]]
"""
# 深复制有时可能太深了。例如，对象可能会引用不该复制的外部资源或单例值。我们可以实现特殊方法 __copy__() 和 __deepcopy__()，控制 copy 和
# deepcopy 的行为
# 通过别名共享对象还能解释 Python 中传递参数的方式，以及使用可变类型作为参数默认值引起的问题

# 函数的参数作为引用时
# Python 唯一支持的参数传递模式是共享传参（call by sharing）。多数面向对象语言都采用这一模式，包括 Ruby、Smalltalk 和 Java（Java 的引用类
# 型是这样，基本类型按值传参）。
# 共享传参指函数的各个形式参数获得实参中各个引用的副本。也就是说，函数内部的形参是实参的别名（形参若为可变对象可能会改变实参内容）。这种方案的结果是，
# 函数可能会修改作为参数传入的可变对象，但是无法修改那些对象的标识（即不能把一个对象替换成另一个对象。
"""
>>> def f(a, b):
... a += b
... return a
...
>>> x = 1
>>> y = 2
>>> f(x, y)
3 
>>> x, y
(1, 2)
>>> a = [1, 2]
>>> b = [3, 4]
>>> f(a, b)
[1, 2, 3, 4]
>>> a, b  # a的值发生了变化
([1, 2, 3, 4], [3, 4])
>>> t = (10, 20)
>>> u = (30, 40)
>>> f(t, u)
(10, 20, 30, 40)
>>> t, u 
((10, 20), (30, 40))
"""

# 不要使用可变类型作为参数的默认值
# 可选参数可以有默认值，这是 Python 函数定义的一个很棒的特性，这样我们的 API 在进化的同时能保证向后兼容。然而，我们应该避免使用可变的对象作为参数的
# 默认值。
# 一个简单的类，说明可变默认值的危险


class HauntedBus:
    """备受幽灵乘客折磨的校车"""
    def __init__(self, passengers=[]):
        self.passengers = passengers

    def pick(self, name):
        self.passengers.append(name)  # 在 self.passengers 上调用 .remove() 和 .append() 方法时，修改的其实是默认列表，它是函数对象
                                      # 的一个属性。

    def drop(self, name):
        self.passengers.remove(name)


"""
>>> bus1 = HauntedBus(['Alice', 'Bill'])
>>> bus1.passengers
['Alice', 'Bill']
>>> bus1.pick('Charlie')
>>> bus1.drop('Alice')
>>> bus1.passengers 
['Bill', 'Charlie']
>>> bus2 = HauntedBus() 
>>> bus2.pick('Carrie')
>>> bus2.passengers
['Carrie']
>>> bus3 = HauntedBus() 
>>> bus3.passengers 
['Carrie']
>>> bus3.pick('Dave')
>>> bus2.passengers 
['Carrie', 'Dave']
>>> bus2.passengers is bus3.passengers 
True
"""
# 问题在于，没有指定初始乘客的 HauntedBus 实例会共享同一个乘客列表，也就是默认传入的空列表。
# self.passengers 变成了 passengers 参数默认值的别名。出现这个问题的根源是，默认值在定义函数时计算（通常在加载模块时），因此默认值变成了函数对
# 象的属性。因此，如果默认值是可变对象，而且修改了它的值，那么后续的函数调用都会受到影响。
"""
>>> dir(HauntedBus.__init__) # doctest: +ELLIPSIS
['__annotations__', '__call__', ..., '__defaults__', ...]
>>> HauntedBus.__init__.__defaults__
(['Carrie', 'Dave'],)
# 我们可以验证 bus2.passengers 是一个别名，它绑定到HauntedBus.__init__.__defaults__ 属性的第一个元素上
>>> HauntedBus.__init__.__defaults__[0] is bus2.passengers
True
"""
# 可变默认值导致的这个问题说明了为什么通常使用 None 作为接收可变值的参数的默认值。在示例 8-8 中，__init__ 方法检查 passengers 参数的值是不是
# None，如果是就把一个新的空列表赋值给 self.passengers

# 防御可变参数
# 如果定义的函数接收可变参数，应该谨慎考虑调用方是否期望修改传入的参数。
# 如果函数接收一个字典，而且在处理的过程中要修改它，那么这个副作用要不要体现到函数外部？

# 在本章最后一个校车示例中，TwilightBus 实例与客户共享乘客列表，这会产生意料之外的结果。在分析实现之前，我们先从客户的角度看看 TwilightBus 类是
# 如何工作的。
"""
>>> basketball_team = ['Sue', 'Tina', 'Maya', 'Diana', 'Pat'] 
>>> bus = TwilightBus(basketball_team) 
>>> bus.drop('Tina') 
>>> bus.drop('Pat')
>>> basketball_team 
['Sue', 'Maya', 'Diana']
"""


class TwilightBus:
    """让乘客销声匿迹的校车"""
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = passengers # 这个赋值语句把 self.passengers 变成 passengers 的别名，而后者是传给__init__ 方法的实参
                                         # （即示例 8-14 中的 basketball_team）的别名。修正的方法很简单：在 __init__ 中，传入
                                         # passengers 参数时，应该把参数值的副本赋值给 self.passengers，像示例 8-8 中那样做（8.3 节）。

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)


# 创建 passengers 列表的副本；如果不是列表，就把它转换成列表。
"""
def __init__(self, passengers=None):
    if passengers is None:
        self.passengers = []
    else:
        self.passengers = list(passengers) 
"""
# 在内部像这样处理乘客列表，就不会影响初始化校车时传入的参数了。此外，这种处理方式还更灵活：现在，传给 passengers 参数的值可以是元组或任何其他可迭
# 代对象，例如set 对象，甚至数据库查询结果，因为 list 构造方法接受任何可迭代对象。自己创建并管理列表可以确保支持所需的 .remove() 和 .append()
# 操作，这样 .pick() 和 .drop() 方法才能正常运作。


# del和垃圾回收
# 对象绝不会自行销毁；然而，无法得到对象时，可能会被当作垃圾回收。
# del 语句删除名称，而不是对象。del 命令可能会导致对象被当作垃圾回收，但是仅当删除的变量保存的是对象的最后一个引用，或者无法得到对象时。 重新绑定也
# 可能会导致对象的引用数量归零，导致对象被销毁。

# 在 CPython 中，垃圾回收使用的主要算法是引用计数。实际上，每个对象都会统计有多少引用指向自己。当引用计数归零时，对象立即就被销毁：CPython 会在对
# 象上调用__del__ 方法（如果定义了），然后释放分配给对象的内存。CPython　2.0 增加了分代垃圾回收算法，用于检测引用循环中涉及的对象组——如果一组对象
# 之间全是相互引用，即使再出色的引用方式也会导致组中的对象不可获取。Python 的其他实现有更复杂的垃圾回收程序，而且不依赖引用计数，这意味着，对象的引用
# 数量为零时可能不会立即调用__del__ 方法

# 使用 weakref.finalize 注册一个回调函数，在销毁对象时调用。没有指向对象的引用时，监视对象生命结束时的情形
"""
>>> import weakref
>>> s1 = {1, 2, 3}
>>> s2 = s1 
>>> def bye():  # 这个函数一定不能是要销毁的对象的绑定方法，否则会有一个指向对象的引用
... print('Gone with the wind...')
...
>>> ender = weakref.finalize(s1, bye) # 在 s1 引用的对象上注册 bye 回调
>>> ender.alive 
True
>>> del s1 # 如前所述，del 不删除对象，而是删除对象的引用
>>> ender.alive 
True
>>> s2 = 'spam' # 重新绑定最后一个引用 s2，让 {1, 2, 3} 无法获取。对象被销毁了，调用了 bye 回调，ender.alive 的值变成了 False。
Gone with the wind...
>>> ender.alive
False
"""
# 示例的目的是明确指出 del 不会删除对象，但是执行 del 操作后可能会导致对象不可获取，从而被删除。
# 你可能觉得奇怪，为什么示例 8-16 中的 {1, 2, 3} 对象被销毁了？毕竟，我们把 s1 引用传给 finalize 函数了，而为了监控对象和调用回调，必须要有引
# 用。这是因为，finalize 持有 {1, 2, 3} 的弱引用。


# 弱引用
# 正是因为有引用，对象才会在内存中存在。当对象的引用数量归零后，垃圾回收程序会把对象销毁。但是，有时需要引用对象，而不让对象存在的时间超过所需时间。这
# 经常用在缓存中。
# 弱引用不会增加对象的引用数量。引用的目标对象称为所指对象（referent）。因此我们说，弱引用不会妨碍所指对象被当作垃圾回收。
# 弱引用在缓存应用中很有用，因为我们不想仅因为被缓存引用着而始终保存缓存对象。
# 示例 8-17 展示了如何使用 weakref.ref 实例获取所指对象。如果对象存在，调用弱引用可以获取对象；否则返回 None
# 示例 8-17 是一个控制台会话，Python 控制台会自动把 _ 变量绑定到结果不为None 的表达式结果上。这对我想演示的行为有影响，不过却凸显了一个实际问题：
# 微观管理内存时，往往会得到意外的结果，因为不明显的隐式赋值会为对象创建新引用。控制台中的 _ 变量是一例。调用跟踪对象也常导致意料之外的引用。
# 弱引用是可调用的对象，返回的是被引用的对象；如果所指对象不存在了，返回 None
"""
>>> import weakref
>>> a_set = {0, 1}
>>> wref = weakref.ref(a_set) # 创建弱引用对象 wref
>>> wref
<weakref at 0x100637598; to 'set' at 0x100636748>
>>> wref() # 调用 wref() 返回的是被引用的对象，{0, 1}。因为这是控制台会话，所以 {0, 1} 会绑定给 _ 变量。
{0, 1}
>>> a_set = {2, 3, 4} # a_set 不再指代 {0, 1} 集合，因此集合的引用数量减少了。但是 _ 变量仍然指代它。
>>> wref() 
{0, 1}
>>> wref() is None # 计算这个表达式时，{0, 1} 存在，因此 wref() 不是 None。但是，随后 _ 绑定到结果值 False。现在 {0, 1} 没有强引用了。
False
>>> wref() is None # 因为 {0, 1} 对象不存在了，所以 wref() 返回 None
True
"""

# weakref 模块的文档（http://docs.python.org/3/library/weakref.html）指出，weakref.ref类其实是低层接口，供高级用途使用，多数程序最好使
# 用 weakref 集合和 finalize。也就是说，应该使用 WeakKeyDictionary、WeakValueDictionary、WeakSet 和finalize（在内部使用弱引用），不要
# 自己动手创建并处理 weakref.ref 实例。我们在示例 8-17 中那么做是希望借助实际使用 weakref.ref 来褪去它的神秘色彩。但是实际上，多数时候 Python
# 程序都使用 weakref 集合。

# WeakValueDictionary简介
# WeakValueDictionary 类实现的是一种可变映射，里面的值是对象的弱引用。被引用的对象在程序中的其他地方被当作垃圾回收后，对应的键会自动从
# WeakValueDictionary中删除。因此，WeakValueDictionary 经常用于缓存。
# 我们对 WeakValueDictionary 的演示受到来自英国六人喜剧团体 Monty Python 的经典短剧《奶酪店》的启发，在那出短剧里，客户问了 40 多种奶酪，包
# 括切达干酪和马苏里拉奶酪，但是都没有货

# Cheese 有个 kind 属性和标准的字符串表示形式


class Cheese:
    def __init__(self, kind):
        self.kind = kind

    def __repr__(self):
        return 'Cheese(%r)' % self.kind


# 我们把 catalog 中的各种奶酪载入 WeakValueDictionary 实现的stock 中。然而，删除 catalog 后，stock 中只剩下一种奶酪了。你知道为什么帕尔马
# 干酪（Parmesan）比其他奶酪保存的时间长吗？
"""
>>> import weakref
>>> stock = weakref.WeakValueDictionary() 
>>> catalog = [Cheese('Red Leicester'), Cheese('Tilsit'),
... Cheese('Brie'), Cheese('Parmesan')]
...
>>> for cheese in catalog:
...     stock[cheese.kind] = cheese 
...
>>> sorted(stock.keys())
['Brie', 'Parmesan', 'Red Leicester', 'Tilsit'] 
>>> del catalog
>>> sorted(stock.keys())
['Parmesan']  # 删除 catalog 之后，stock 中的大多数奶酪都不见了，这是 WeakValueDictionary的预期行为。为什么不是全部呢？
>>> del cheese
>>> sorted(stock.keys())
[]
"""
# 临时变量引用了对象，这可能会导致该变量的存在时间比预期长。通常，这对局部变量来说不是问题，因为它们在函数返回时会被销毁。但是在示例 8-19 中，for
# 循环中的变量 cheese 是全局变量，除非显式删除，否则不会消失。

# 与 WeakValueDictionary 对应的是 WeakKeyDictionary，后者的键是弱引用。weakref.WeakKeyDictionary 的文档
# （https://docs.python.org/3/library/weakref.html?highlight=weakref#weakref.WeakKeyDictionary）指出了一些可能的用途：
# （WeakKeyDictionary 实例）可以为应用中其他部分拥有的对象附加数据，这样就无需为对象添加属性。这对覆盖属性访问权限的对象尤其有用。

# weakref 模块还提供了 WeakSet 类，按照文档的说明，这个类的作用很简单：“保存元素弱引用的集合类。元素没有强引用时，集合会把它删除。”如果一个类需要
# 知道所有实例，一种好的方案是创建一个 WeakSet 类型的类属性，保存实例的引用。如果使用常规的 set，实例永远不会被垃圾回收，因为类中有实例的强引用，而
# 类存在的时间与 Python进程一样长，除非显式删除类。

# 弱引用的局限
# 不是每个 Python 对象都可以作为弱引用的目标（或称所指对象）。基本的 list 和 dict实例不能作为所指对象，但是它们的子类可以轻松地解决这个问题：
import weakref


class MyList(list):
    """list的子类，实例可以作为弱引用的目标"""


a_list = MyList(range(10))
# a_list可以作为弱引用的目标
wref_to_a_list = weakref.ref(a_list)


# set 实例可以作为所指对象，因此实例 8-17 才使用 set 实例。用户定义的类型也没问题，这就解释了示例 8-19 中为什么使用那个简单的 Cheese 类。但是，
# int 和 tuple 实例不能作为弱引用的目标，甚至它们的子类也不行。


# Python对不可变类型施加的把戏
# 我惊讶地发现，对元组 t 来说，t[:] 不创建副本，而是返回同一个对象的引用。此外，tuple(t) 获得的也是同一个元组的引用。
# str、bytes 和 frozenset 实例也有这种行为。注意，frozenset 实例不是序列，因此不能使用 fs[:]（fs 是一个 frozenset 实例）。但是，fs.copy()
# 具有相同的效果：它会欺骗你，返回同一个对象的引用，而不是创建一个副本

# 共享字符串字面量是一种优化措施，称为驻留（interning）。CPython 还会在小的整数上使用这个优化措施，防止重复创建“热门”数字，如 0、-1 和 42。注意，
# CPython 不会驻留所有字符串和整数，驻留的条件是实现细节
"""
>>> t1 = (1, 2, 3)
>>> t3 = (1, 2, 3) 
>>> t3 is t1 
False
>>> s1 = 'ABC'
>>> s2 = 'ABC' 
>>> s2 is s1 # 奇怪的事发生了，a 和 b 指代同一个字符串。
True
"""
# 本节讨论的把戏，包括 frozenset.copy() 的行为，是“善意的谎言”，能节省内存，提升解释器的速度

# 本章小结
# 每个 Python 对象都有标识、类型和值。只有对象的值会不时变化。
# 如果两个变量指代的不可变对象具有相同的值（a == b 为 True），实际上它们指代的是副本还是同一个对象的别名基本没什么关系，因为不可变对象的值不会变，
# 但有一个例外。这里说的例外是不可变的集合，如元组和 frozenset：如果不可变集合保存的是可变元素的引用，那么可变元素的值发生变化后，不可变集合也会随之
# 改变。实际上，这种情况不是很常见.
# 变量保存的是引用，这一点对 Python 编程有很多实际的影响。
# - 简单的赋值不创建副本
# - 对 += 或 *= 所做的增量赋值来说，如果左边的变量绑定的是不可变对象，会创建新对象；如果是可变对象，会就地修改。
# - 为现有的变量赋予新值，不会修改之前绑定的变量。这叫重新绑定：现在变量绑定了其他对象。如果变量是之前那个对象的最后一个引用，对象会被当作垃圾回收。
# - 函数的参数以别名的形式传递，这意味着，函数可能会修改通过参数传入的可变对象。这一行为无法避免，除非在本地创建副本，或者使用不可变对象（例如，传入元
# 组，而不传入列表）。
# - 使用可变类型作为函数参数的默认值有危险，因为如果就地修改了参数，默认值也就使用可变类型作为函数参数的默认值有危险，因为如果就地修改了参数，默认值也
# 就变了，这会影响以后使用默认值的调用。
# 在 CPython 中，对象的引用数量归零后，对象会被立即销毁。如果除了循环引用之外没有其他引用，两个对象都会被销毁。某些情况下，可能需要保存对象的引用，
# 但不留存对象本身。例如，有一个类想要记录所有实例。这个需求可以使用弱引用实现，这是一种低层机制，是 weakref 模块中 WeakValueDictionary、
# WeakKeyDictionary 和 WeakSet 等有用的集合类，以及 finalize 函数的底层支持。