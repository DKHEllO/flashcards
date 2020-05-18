#!/usr/bin/env python

# 函数装饰器用于在源码中“标记”函数，以某种方式增强函数的行为。
# nonlocal 是新近出现的保留关键字,如果严格遵守基于类的面向对象编程方式，即便不知道这个关键字也不会受到影响。然而，如果你想自己实现函数装饰器，那就
# 必须了解闭包的方方面面，因此也就需要知道nonlocal。

# 除了在装饰器中有用处之外，闭包还是回调式异步编程和函数式编程风格的基础。

# 装饰器基础知识
# 装饰器是可调用的对象，其参数是另一个函数（被装饰的函数）。 装饰器可能会处理被装饰的函数，然后把它返回，或者将其替换成另一个函数或可调用对象。
"""
@decorate
def target():
    print('running target()')

def target():
    print('running target()')
target = decorate(target)
"""
# 两种写法的最终结果一样：上述两个代码片段执行完毕后得到的 target 不一定是原来那个 target 函数，而是 decorate(target) 返回的函数。

"""
>>> def deco(func):
...     def inner():
...         print('running inner()')
...     return inner 
...
>>> @deco
... def target(): 
...     print('running target()')
...
>>> target() 
running inner()
>>> target 
<function deco.<locals>.inner at 0x10063b598>
"""

# 严格来说，装饰器只是语法糖。如前所示，装饰器可以像常规的可调用对象那样调用，其参数是另一个函数。有时，这样做更方便，尤其是做元编程（在运行时改变程序
# 的行为）时。
# 装饰器的一大特性是，能把被装饰的函数替换成其他函数。第二个特性是，装饰器在加载模块时立即执行。

# Python何时执行装饰器
# 装饰器的一个关键特性是，它们在被装饰的函数定义之后立即运行。这通常是在导入时（即 Python 加载模块时）,示例见registration.py
# 函数装饰器在导入模块时立即执行，而被装饰的函数只在明确调用时运行。这突出了 Python 程序员所说的导入时和运行时之间的区别。

# 考虑到装饰器在真实代码中的常用方式，registration有两个不寻常的地方。
# - 装饰器函数与被装饰的函数在同一个模块中定义。实际情况是，装饰器通常在一个模块中定义，然后应用到其他模块中的函数上。
# - register 装饰器返回的函数与通过参数传入的相同。实际上，大多数装饰器会在内部定义一个函数，然后将其返回。

# 虽然示例 7-2 中的 register 装饰器原封不动地返回被装饰的函数，但是这种技术并非没有用处。很多 Python Web 框架使用这样的装饰器把函数添加到某种中
# 央注册处，例如把URL 模式映射到生成 HTTP 响应的函数上的注册处。这种注册装饰器可能会也可能不会修改被装饰的函数。

# 使用装饰器改进“策略”模式
# 回顾一下，示例 6-6 的主要问题是，定义体中有函数的名称，但是 best_promo 用来判断哪个折扣幅度最大的 promos 列表中也有函数名称。这种重复是个问题
# ，因为新增策略函数后可能会忘记把它添加到 promos 列表中，导致 best_promo 忽略新策略，而且不报错，为系统引入了不易察觉的缺陷。

promos = []


def promotion(promo_func):
    promos.append(promo_func)
    return promo_func


@promotion
def fidelity(order):
    """为积分为1000或以上的顾客提供5%折扣"""
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0


@promotion
def bulk_item(order):
    """单个商品为20个或以上时提供10%折扣"""
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount


@promotion
def large_order(order):
    """订单中的不同商品达到10个或以上时提供7%折扣"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0


def best_promo(order):
    """选择可用的最佳折扣
    """
    return max(promo(order) for promo in promos)


# @promotion 装饰器突出了被装饰的函数的作用，还便于临时禁用某个促销策略：只需把装饰器注释掉。
# 促销折扣策略可以在其他模块中定义，在系统中的任何地方都行，只要使用@promotion 装饰即可。

# 不过，多数装饰器会修改被装饰的函数。通常，它们会定义一个内部函数，然后将其返回，替换被装饰的函数。使用内部函数的代码几乎都要靠闭包才能正确运作。为了
# 理解闭包，我们要退后一步，先了解 Python 中的变量作用域。

# 变量作用域规则
# 我们定义并测试了一个函数，它读取两个变量的值：一个是局部变量 a，是函数的参数；另一个是变量 b，这个函数没有定义它。
# 一个函数，读取一个局部变量和一个全局变量
"""
>>> def f1(a):
...     print(a)
...     print(b)
...
>>> f1(3)
3 Traceback (
most recent call last):
File "<stdin>", line 1, in <module>
File "<stdin>", line 3, in f1
NameError: global name 'b' is not defined
"""

# b 是局部变量，因为在函数的定义体中给它赋值了
"""
>>> b = 6
>>> def f2(a):
...     print(a)
...     print(b)
...     b = 9
...
>>> f2(3)
3 Traceback (
most recent call last):
File "<stdin>", line 1, in <module>
File "<stdin>", line 3, in f2
UnboundLocalError: local variable 'b' referenced before assignment
"""

# Python 编译函数的定义体时，它判断 b 是局部变量，因为在函数中给它赋值了。生成的字节码证实了这种判断，Python 会尝试从本地环境获取 b。后面调用
# f2(3)时， f2 的定义体会获取并打印局部变量 a 的值，但是尝试获取局部变量 b 的值时，发现b 没有绑定值。

# 这不是缺陷，而是设计选择：Python 不要求声明变量，但是假定在函数定义体中赋值的变量是局部变量。这比 JavaScript 的行为好多了，JavaScript 也不要
# 求声明变量，但是如果忘记把变量声明为局部变量（使用 var），可能会在不知情的情况下获取全局变量。

# 如果在函数中赋值时想让解释器把 b 当成全局变量，要使用 global 声明：
"""
>>> b = 6
>>> def f3(a):
... global b
... print(a)
... print(b)
... b = 9
...
>>> f3(3)
3
6 
>>> b
9
>>> f3(3)
3
9 
>>> b = 30
>>> b
30
>>>
"""

# 闭包
# 闭包指延伸了作用域的函数，其中包含函数定义体中引用、但是不在定义体中定义的非全局变量。函数是不是匿名的没有关系，关键是它能访问定义体之外定义的非全局
# 变量。

# 假如有个名为 avg 的函数，它的作用是计算不断增加的系列值的均值；例如，整个历史中某个商品的平均收盘价。每天都会增加新价格，因此平均值要考虑至目前为止
# 所有的价格。
"""
>>> avg(10)
10.0
>>> avg(11)
10.5
>>> avg(12)
11.0
"""
# 初学者可能会使用类实现。


class Averager():
    def __init__(self):
        self.series = []

    def __call__(self, new_value):
        self.series.append(new_value)
        total = sum(self.series)
        return total/len(self.series)

# 下面是函数式实现，使用高阶函数 make_averager。


def make_averager():
    series = []

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total/len(series)
    return averager


# 调用 make_averager 时，返回一个 averager 函数对象。每次调用 averager 时，它会把参数添加到系列值中，然后计算当前平均值，如下所示。
"""
>>> avg = make_averager()
>>> avg(10)
10.0
>>> avg(11)
10.5
>>> avg(12)
11.0
"""

# Averager 类的实例 avg 在哪里存储历史值很明显：self.series 实例属性。但是第二个示例中的 avg 函数在哪里寻找 series 呢？
# 注意，series 是 make_averager 函数的局部变量，因为那个函数的定义体中初始化了series：series = []。可是，调用 avg(10) 时，make_averager
# 函数已经返回了，而它的本地作用域也一去不复返了。
# 在 averager 函数中，series 是自由变量（free variable）。这是一个技术术语，指未在本地作用域中绑定的变量
# averager 的闭包延伸到那个函数的作用域之外，包含自由变量 series 的绑定

# 审查返回的 averager 对象，我们发现 Python 在 __code__ 属性（表示编译后的函数定义体）中保存局部变量和自由变量的名称
"""
>>> avg.__code__.co_varnames
('new_value', 'total')
>>> avg.__code__.co_freevars
('series',)
"""
# series 的绑定在返回的 avg 函数的 __closure__ 属性中。avg.__closure__ 中的各个元素对应于 avg.__code__.co_freevars 中的一个名称。这些
# 元素是 cell 对象，有个cell_contents 属性，保存着真正的值。
"""
>>> avg.__code__.co_freevars
('series',)
>>> avg.__closure__
(<cell at 0x107a44f78: list object at 0x107a91a48>,)
>>> avg.__closure__[0].cell_contents
[10, 11, 12]
"""

# 综上，闭包是一种函数，它会保留定义函数时存在的自由变量的绑定，这样调用函数时，虽然定义作用域不可用了，但是仍能使用那些绑定。只有嵌套在其他函数中的函
# 数才可能需要处理不在全局作用域中的外部变量。


# nonlocal声明
# 前面实现 make_averager 函数的方法效率不高。在示例 7-9 中，我们把所有值存储在历史数列中，然后在每次调用 averager 时使用 sum 求和。更好的实现
# 方式是，只存储目前的总值和元素个数，然后使用这两个数计算均值。
# 计算移动平均值的高阶函数，不保存所有历史值，但有缺陷

def make_averager():
    count = 0
    total = 0

    def averager(new_value):
        count += 1
        total += new_value
        return total / count
    return averager

# 问题是，当 count 是数字或任何不可变类型时，count += 1 语句的作用其实与 count = count + 1 一样。因此，我们在 averager 的定义体中为 count
# 赋值了，这会把count 变成局部变量。total 变量也受这个问题影响。
# 没遇到这个问题，因为我们没有给 series 赋值，我们只是调用series.append，并把它传给 sum 和 len。也就是说，我们利用了列表是可变的对象这一事实。
# 但是对数字、字符串、元组等不可变类型来说，只能读取，不能更新。如果尝试重新绑定，例如 count = count + 1，其实会隐式创建局部变量 count。这样，
# count 就不是自由变量了，因此不会保存在闭包中。
# 为了解决这个问题，Python 3 引入了 nonlocal 声明。它的作用是把变量标记为自由变量，即使在函数中为变量赋予新值了，也会变成自由变量。如果为
# nonlocal 声明的变量赋予新值，闭包中保存的绑定会更新。最新版 make_averager 的正确实现如下所示。


def make_averager():
    count = 0
    total = 0

    def averager(new_value):
        nonlocal count, total
        count += 1
        total += new_value
        return total / count
    return averager


# 实现一个简单的装饰器
# 定义了一个装饰器，它会在每次调用被装饰的函数时计时，然后把经过的时间、传入的参数和调用的结果打印出来。
# 装饰器的典型行为：把被装饰的函数替换成新函数，二者接受相同的参数，而且（通常）返回被装饰的函数本该返回的值，同时还会做些额外操作。
# Gamma 等人写的《设计模式：可复用面向对象软件的基础》一书是这样概述“装饰器”模式的：“动态地给一个对象添加一些额外的职责。”函数装饰器符合这一说法。
# 简单的装饰器见clockdeco_demo.py

# Python 内置了三个用于装饰方法的函数：property、classmethod 和 staticmethod。
# 另一个常见的装饰器是 functools.wraps，它的作用是协助构建行为良好的装饰器。我们在示例 7-17 中用过。标准库中最值得关注的两个装饰器是 lru_cache
# 和全新的singledispatch（Python 3.4 新增）。这两个装饰器都在 functools 模块中定义。接下来分别讨论它们

# 使用functools.lru_cache做备忘:
# functools.lru_cache 是非常实用的装饰器，它实现了备忘（memoization）功能。这是一项优化技术，它把耗时的函数的结果保存起来，避免传入相同的参数时
# 重复计算。LRU三个字母是“Least Recently Used”的缩写，表明缓存不会无限制增长，一段时间不用的缓存条目会被扔掉。
# 生成第 n 个斐波纳契数这种慢速递归函数适合使用 lru_cache
"""
$ python3 fibo_demo.py
[0.00000095s] fibonacci(0) -> 0
[0.00000095s] fibonacci(1) -> 1
[0.00007892s] fibonacci(2) -> 1
[0.00000095s] fibonacci(1) -> 1
[0.00000095s] fibonacci(0) -> 0
[0.00000095s] fibonacci(1) -> 1
[0.00003815s] fibonacci(2) -> 1
[0.00007391s] fibonacci(3) -> 2
[0.00018883s] fibonacci(4) -> 3
[0.00000000s] fibonacci(1) -> 1
[0.00000095s] fibonacci(0) -> 0
[0.00000119s] fibonacci(1) -> 1
[0.00004911s] fibonacci(2) -> 1
[0.00009704s] fibonacci(3) -> 2
[0.00000000s] fibonacci(0) -> 0
[0.00000000s] fibonacci(1) -> 1
[0.00002694s] fibonacci(2) -> 1
[0.00000095s] fibonacci(1) -> 1
[0.00000095s] fibonacci(0) -> 0
[0.00000095s] fibonacci(1) -> 1
[0.00005102s] fibonacci(2) -> 1
[0.00008917s] fibonacci(3) -> 2
[0.00015593s] fibonacci(4) -> 3
[0.00029993s] fibonacci(5) -> 5
[0.00052810s] fibonacci(6) -> 8
8
"""
# 浪费时间的地方很明显：fibonacci(1) 调用了 8 次，fibonacci(2) 调用了 5 次……但是，如果增加两行代码，使用 lru_cache，性能会显著改善

# 除了优化递归算法之外，lru_cache 在从 Web 中获取信息的应用中也能发挥巨大作用。
# lru_cache 可以使用两个可选的参数来配置。
# functools.lru_cache(maxsize=128, typed=False)
# maxsize 参数指定存储多少个调用的结果。缓存满了之后，旧的结果会被扔掉，腾出空间。为了得到最佳性能，maxsize 应该设为 2 的幂。typed 参数如果设为
# True，把不同参数类型得到的结果分开保存，即把通常认为相等的浮点数和整数参数（如 1 和 1.0）区分开。
# 因为 lru_cache 使用字典存储结果，而且键根据调用时传入的定位参数和关键字参数创建，所以被 lru_cache 装饰的函数，它的所有参数都必须是可散列的。



# 单分派泛函数
# 假设我们在开发一个调试 Web 应用的工具，我们想生成 HTML，显示不同类型的 Python 对象。
import html


def htmlize(obj):
    content = html.escape(repr(obj))
    return '<pre>{}</pre>'.format(content)

# 这个函数适用于任何 Python 类型，但是现在我们想做个扩展，让它使用特别的方式显示某些类型。
# - str:把内部的换行符替换为 '<br>\n'；不使用 <pre>，而是使用 <p>。
# - int:以十进制和十六进制显示数字。
# - list:输出一个 HTML 列表，根据各个元素的类型进行格式化。
"""
>>> htmlize({1, 2, 3})  # 默认情况下，在 <pre></pre> 中显示 HTML 转义后的对象字符串表示形式。
'<pre>{1, 2, 3}</pre>'
>>> htmlize(abs)
'<pre><built-in function abs></pre>'
>>> htmlize('Heimlich & Co.\n- a game') 
'<p>Heimlich & Co.<br>\n- a game</p>'
>>> htmlize(42) 
'<pre>42 (0x2a)</pre>'
>>> print(htmlize(['alpha', 66, {3, 2, 1}])) 
<ul>
<li><p>alpha</p></li>
<li><pre>66 (0x42)</pre></li>
<li><pre>{1, 2, 3}</pre></li>
</ul>
"""
# 因为 Python 不支持重载方法或函数，所以我们不能使用不同的签名定义 htmlize 的变体，也无法使用不同的方式处理不同的数据类型。在 Python 中，一种常
# 见的做法是把htmlize 变成一个分派函数，使用一串 if/elif/elif，调用专门的函数，如htmlize_str、htmlize_int，等等。这样不便于模块的用户扩展，
# 还显得笨拙：时间一长，分派函数 htmlize 会变得很大，而且它与各个专门函数之间的耦合也很紧密。

# Python 3.4 新增的 functools.singledispatch 装饰器可以把整体方案拆分成多个模块，甚至可以为你无法修改的类提供专门的函数。使用 @singledispatch
# 装饰的普通函数会变成泛函数（generic function）：根据第一个参数的类型，以不同方式执行相同操作的一组函数。

# singledispatch 创建一个自定义的 htmlize.register 装饰器，把多个函数绑在一起组成一个泛函数
# 用例详见singledispatch_demo.py

# 装饰器是函数，因此可以组合起来使用，即，可以在已经被装饰的函数上应用装饰器

# 叠放装饰器
# @lru_cache 应用到 @clock 装饰 fibonacci 得到的结果上，模块中最后一个函数应用了两个 @htmlize.register 装饰器
# 把 @d1 和 @d2 两个装饰器按顺序应用到 f 函数上，作用相当于 f = d1(d2(f))
"""
@d1
@d2
def f():
    print('f')
    
相当于

def f():
    print('f')
f = d1(d2(f))
"""


# 参数化装饰器
# 解析源码中的装饰器时，Python 把被装饰的函数作为第一个参数传给装饰器函数。那怎么让装饰器接受其他参数呢？答案是：创建一个装饰器工厂函数，把参数传给它，
# 返回一个装饰器，然后再把它应用到要装饰的函数上

# 为了便于启用或禁用 register 执行的函数注册功能，我们为它提供一个可选的 active 参数，设为 False 时，不注册被装饰的函数。。从概念上看，这个新的
# register 函数不是装饰器，而是装饰器工厂函数。调用它会返回真正的装饰器，这才是应用到目标函数上的装饰器。

# 参数化clock装饰器 见clockdeco_demo.py
# 延伸阅读中的资料讨论了构建工业级装饰器的技术，尤其是 Graham Dumpleton 的博客和 wrapt 模块。

# Graham Dumpleton 和 Lennart Regebro（本书的技术审校之一）认为，装饰器最好通过实现 __call__ 方法的类实现，不应该像本章的示例那样通过函数实
# 现。我同意使用他们建议的方式实现非平凡的装饰器更好，但是使用函数解说这个语言特性的基本思想更易于理解。



