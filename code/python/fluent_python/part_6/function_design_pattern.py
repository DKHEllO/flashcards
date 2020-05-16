#!/usr/bin/env python

# 所用的语言决定了哪些模式可用
# 程序设计语言的选择非常重要，它将影响人们理解问题的出发点。我们的设计模式采用了 Smalltalk 和 C++ 层的语言特性，这个选择实际上决定了哪些机制可以方
# 便地实现，而哪些则不能。若我们采用过程式语言，可能就要包括诸如“集成”“封装”和“多态”的设计模式。相应地，一些特殊的面向对象语言可以直接支持我们的某些
# 模式，例如 CLOS 支持多方法概念，这就减少了访问者模式的必要性。

# Norvig 建议在有一等函数的语言中重新审视“策略”“命令”“模板方法”和“访问者”模式。通常，我们可以把这些模式中涉及的某些类的实例替换成简单的函数，从而减
# 少样板代码。

# 案例分析：重构“策略”模式
# 如果合理利用作为一等对象的函数，某些设计模式可以简化，“策略”模式就是其中一个很好的例子。

# 经典的策略模式
# 《设计模式：可复用面向对象软件的基础》一书是这样概述“策略”模式的：定义一系列算法，把它们一一封装起来，并且使它们可以相互替换。本模式使得算法可以独
# 立于使用它的客户而变化。
# 电商领域有个功能明显可以使用“策略”模式，即根据客户的属性或订单中的商品计算折扣。
# 假如一个网店制定了下述折扣规则:
# - 有 1000 或以上积分的顾客，每个订单享 5% 折扣。
# - 同一订单中，单个商品的数量达到 20 个或以上，享 10% 折扣。
# - 订单中的不同商品达到 10 个或以上，享 7% 折扣。
# 简单起见，我们假定一个订单一次只能享用一个折扣。

# “策略”模式的 UML 类图见策略模式对类的编排.png，其中涉及下列内容。
# 上下文:把一些计算委托给实现不同算法的可互换组件，它提供服务。在这个电商示例中，上下文是 Order，它会根据不同的算法计算促销折扣。
# 策略:实现不同算法的组件共同的接口。在这个示例中，名为 Promotion 的抽象类扮演这个角色。
# 具体策略:“策略”的具体子类。fidelityPromo、BulkPromo 和 LargeOrderPromo 是这里实现的三个具体策略。

# 具体策略由上下文类的客户选择。实例化订单之前，系统会以某种方式选择一种促销折扣策略，然后把它传给 Order 构造方法。具体怎么选择策略，不在这个模式的
# 职责范围内。

from abc import ABC, abstractmethod
from collections import namedtuple
Customer = namedtuple('Customer', 'name fidelity')


class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order: # 上下文
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())


class Promotion(ABC):  # 策略：抽象基类
    @abstractmethod
    def discount(self, order):
        """返回折扣金额（正值）"""


class FidelityPromo(Promotion): # 第一个具体策略
    """为积分为1000或以上的顾客提供5%折扣"""
    def discount(self, order):
        return order.total() * .05 if order.customer.fidelity >= 1000 else 0


class BulkItemPromo(Promotion): # 第二个具体策略
    """单个商品为20个或以上时提供10%折扣"""
    def discount(self, order):
        discount = 0
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * .1
        return discount


class LargeOrderPromo(Promotion): # 第三个具体策略
    """订单中的不同商品达到10个或以上时提供7%折扣"""
    def discount(self, order):
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * .07
        return 0


"""
>>> joe = Customer('John Doe', 0) 
>>> ann = Customer('Ann Smith', 1100)
>>> cart = [LineItem('banana', 4, .5), 
... LineItem('apple', 10, 1.5),
... LineItem('watermellon', 5, 5.0)]
>>> Order(joe, cart, FidelityPromo()) 
<Order total: 42.00 due: 42.00>
>>> Order(ann, cart, FidelityPromo()) 
<Order total: 42.00 due: 39.90>
>>> banana_cart = [LineItem('banana', 30, .5), 
... LineItem('apple', 10, 1.5)]
>>> Order(joe, banana_cart, BulkItemPromo()) 
<Order total: 30.00 due: 28.50>
>>> long_order = [LineItem(str(item_code), 1, 1.0) 
... for item_code in range(10)]
>>> Order(joe, long_order, LargeOrderPromo()) 
<Order total: 10.00 due: 9.30>
>>> Order(joe, cart, LargeOrderPromo())
<Order total: 42.00 due: 42.00>
"""


# 使用函数实现“策略”模式
# 上述每个具体策略都是一个类，而且都只定义了一个方法，即 discount。此外，策略实例没有状态（没有实例属性）。你可能会说，它们看起来像是普通的函数——
# 的确如此。


class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order: # 上下文
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())


def fidelity_promo(order):
    """为积分为1000或以上的顾客提供5%折扣"""
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0


def bulk_item_promo(order):
    """单个商品为20个或以上时提供10%折扣"""
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount


def large_order_promo(order):
    """订单中的不同商品达到10个或以上时提供7%折扣"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0

# 《设计模式：可复用面向对象软件的基础》一书的作者指出：“策略对象通常是很好的享元（flyweight）。” 那本书的另一部分对“享元”下了定义：“享元是可共享的
# 对象，可以同时在多个上下文中使用。” 共享是推荐的做法，这样不必在每个新的上下文（这里是 Order 实例）中使用相同的策略时不断新建具体策略对象，从而减
# 少消耗。因此，为了避免“策略”模式的一个缺点（运行时消耗），《设计模式：可复用面向对象软件的基础》的作者建议再使用另一个模式。但此时，代码行数和维护成
# 本会不断攀升。

# 在复杂的情况下，需要具体策略维护内部状态时，可能需要把“策略”和“享元”模式结合起来。但是，具体策略一般没有内部状态，只是处理上下文中的数据。此时，一
# 定要使用普通的函数，别去编写只有一个方法的类，再去实现另一个类声明的单函数接口。函数比用户定义的类的实例轻量，而且无需使用“享元”模式，因为各个策略函
# 数在 Python 编译模块时只会创建一次。普通的函数也是“可共享的对象，可以同时在多个上下文中使用”。

# 选择最佳策略：简单的方式
"""
>>> Order(joe, long_order, best_promo) 
<Order total: 10.00 due: 9.30>
>>> Order(joe, banana_cart, best_promo) 
<Order total: 30.00 due: 28.50>
>>> Order(ann, cart, best_promo) 
<Order total: 42.00 due: 39.90>
"""

# best_promo 函数的实现特别简单，如示例 6-6 所示。

# 将函数当做一等对象，习惯函数是一等对象后，自然而然就会构建这种数据结构存储函数。
promos = [fidelity_promo, bulk_item_promo, large_order_promo]


# 当前版本易于阅读，但是有些重复可能会导致不易察觉的缺陷：若想添加新的促销策略，要定义相应的函数，还要记得把它添加到 promos 列表中；否则，当新促销函
# 数显式地作为参数传给 Order 时，它是可用的，但是 best_promo 不会考虑它。
def best_promo(order):
    """选择可用的最佳折扣
    """
    return max(promo(order) for promo in promos)


# 找出模块中的全部策略
# 在 Python 中，模块也是一等对象，而且标准库提供了几个处理模块的函数。Python 文档是这样说明内置函数 globals 的。
# - globals():返回一个字典，表示当前的全局符号表。这个符号表始终针对当前模块（对函数或方法来说，是指定义它们的模块，而不是调用它们的模块）。

# 使用 globals 函数帮助 best_promo 自动找到其他可用的 *_promo 函数，过程有点曲折。
# 内省模块的全局命名空间，构建 promos 列表，这样best_promo内部没有任何变化
promos = [globals()[name] for name in globals() if name.endswith('_promo') and name != 'best_promo']


def best_promo(order):
    """选择可用的最佳折扣
    """
    return max(promo(order) for promo in promos)


# 收集所有可用促销的另一种方法是，在一个单独的模块中保存所有策略函数，把best_promo 排除在外。
# 最大的变化是内省名为 promotions 的独立模块，构建策略函数列表。注意，示例 6-8 要导入 promotions 模块，以及提供高阶内省函数的 inspect 模块
# （简单起见，这里没有给出导入语句，因为导入语句一般放在文件顶部）。
# 内省单独的 promotions 模块，构建 promos 列表
import inspect
import promotions
promos = [func for name, func in inspect.getmembers(promotions, inspect.isfunction)]

# inspect.getmembers 函数用于获取对象（这里是 promotions 模块）的属性，第二个参数是可选的判断条件（一个布尔值函数）。我们使用的是
# inspect.isfunction，只获取模块中的函数。
# 唯一重要的是，promotions 模块只能包含计算订单折扣的函数。当然，这是对代码的隐性假设。如果有人在 promotions 模块中使用不同的签名定义函数，那么
# best_promo 函数尝试将其应用到订单上时会出错。
# 我们可以添加更为严格的测试，审查传给实例的参数，进一步过滤函数。示例 6-8 的目的不是提供完善的方案，而是强调模块内省的一种用途。



# “命令”模式
# “命令”模式的目的是解耦调用操作的对象（调用者）和提供实现的对象（接收者）。在 《设计模式：可复用面向对象软件的基础》所举的示例中，调用者是图形应用程
# 序中的菜单项，而接收者是被编辑的文档或应用程序自身。
# 这个模式的做法是，在二者之间放一个 Command 对象，让它实现只有一个方法（execute）的接口，调用接收者中的方法执行所需的操作。这样，调用者无需了解接
# 收者的接口，而且不同的接收者可以适应不同的 Command 子类。调用者有一个具体的命令，通过调用 execute 方法执行。注意，图 6-2 中的 MacroCommand
# 可能保存一系列命令，它的 execute() 方法会在各个命令上调用相同的方法。

# Gamma 等人说过：“命令模式是回调机制的面向对象替代品。”问题是，我们需要回调机制的面向对象替代品吗？有时确实需要，但并非始终需要。
# 我们可以不为调用者提供一个 Command 实例，而是给它一个函数。此时，调用者不用调用 command.execute()，直接调用 command() 即可。MacroCommand
# 可以实现成定义了 __call__ 方法的类。这样，MacroCommand 的实例就是可调用对象，各自维护着一个函数列表，供以后调用，如示例 6-9 所示。


class MacroCommand:
    """一个执行一组命令的命令"""
    def __init__(self, commands):
        # 函数当做一等对象
        self.commands = list(commands)

    def __call__(self):
        for command in self.commands:
            command()


# 复杂的“命令”模式（如支持撤销操作）可能需要更多，而不仅是简单的回调函数。即便如此，也可以考虑使用 Python 提供的几个替代品。
# - 像示例 6-9 中 MacroCommand 那样的可调用实例，可以保存任何所需的状态，而且除了 __call__ 之外还可以提供其他方法。
# - 可以使用闭包在调用之间保存函数的内部状态。
# 使用一等函数对“命令”模式的重新审视到此结束。站在一定高度上看，这里采用的方式与“策略”模式所用的类似：把实现单方法接口的类的实例替换成可调用对象。
# 毕竟，每个Python 可调用对象都实现了单方法接口，这个方法就是 __call__。


# 小结
# 很多情况下，在 Python 中使用函数或可调用对象实现回调更自然，这比模仿 Gamma、Helm、Johnson 和 Vlissides 在书中所述的“策略”或“命令”模式要好。
# 本章对“策略”模式的重构和对“命令”模式的讨论是为了通过示例说明一个更为常见的做法：有时，设计模式或API 要求组件实现单方法接口，而那个方法的名称很宽泛，
# 例如“execute”“run”或“doIt”。在 Python 中，这些模式或 API 通常可以使用一等函数或其他可调用的对象实现，从而减少样板代码。

# Peter Norvig 那次设计模式演讲想表达的观点是，“命令”和“策略”模式（以及“模板方法”和“访问者”模式）可以使用一等函数实现，这样更简单，甚至“不见了”，
# 至少对这些模式的某些用途来说是如此。