#!/usr/bin/env python

import collections
from math import hypot


# 我们用 collections.namedtuple 构建了一个简单的类来表示一张纸牌。自Python 2.6 开始，namedtuple 就加入到 Python 里，用以构建只有少数属性
# 但是没有方法的对象，比如数据库条目。
Card = collections.namedtuple('Card', ['rank', 'suit'])

"""
>>> card = Card('7', 'Spades')
>>> card
Card(rank='7', suit='diamonds')
"""


# 定义纸牌盒类，里面包含一摞纸牌，可以对这一系列纸牌进行任意操作
class FrenchDeck(object):
    """
    >>> deck = FrenchDeck()
    >>> len(deck)
    52
    >>> deck[0]
    Card(rank='2', suit='spades')
    >>> deck[-1]
    Card(rank='A', suit='hearts')

    Pick a card at random, for example:
    >>> from random import choice
    >>> choice(deck)
    Card(rank='3', suit='hearts')
    >>> choice(deck)
    Card(rank='K', suit='spades')
    >>> choice(deck)
    Card(rank='2', suit='clubs')

    现在已经可以体会到通过实现特殊方法来利用 Python 数据模型的两个好处
    - 作为你的类的用户，他们不必去记住标准操作的各式名称（“怎么得到元素的总数？是 .size() 还是 .length() 还是别的什么？”）。
    - 可以更加方便地利用 Python 的标准库，比如 random.choice 函数，从而不用重新发明轮子。

    因为 __getitem__ 方法把 [] 操作交给了 self._cards 列表，所以我们的 deck 类自动支持切片（slicing）操作。下面列出了查看一摞牌最上面 3
    张和只看牌面是 A 的牌的操作。其中第二种操作的具体方法是，先抽出索引是 12 的那张牌，然后每隔 13 张牌拿 1张。
    >>> deck[:3]
    [Card(rank='2', suit='spades'), Card(rank='2', suit='diamonds'), Card(rank='2', suit='clubs')]

    >>> deck[12::13]
    [Card(rank='5', suit='spades'), Card(rank='8', suit='diamonds'), Card(rank='J', suit='clubs'), Card(rank='A', suit='hearts')]

    另外，仅仅实现了 __getitem__ 方法，这一摞牌就变成可迭代的了：
    >>> for card in deck: # doctest: +ELLIPSIS
    ...     print(card)
    Card(rank='2', suit='spades')
    Card(rank='2', suit='diamonds')
    Card(rank='2', suit='clubs')
    ...

    反向迭代也没关系：
    >>> for card in reversed(deck): # doctest: +ELLIPSIS
    ...     print(card)
    Card(rank='A', suit='hearts')
    Card(rank='A', suit='clubs')
    Card(rank='A', suit='diamonds')
    ...

    TIPS:
    在测试中，如果可能的输出过长的话，那么过长的内容就会被如上面例子的最后一行的省略号（...）所替代。此时就需要 #doctest: +ELLIPSIS这个指令来保
    证 doctest 能够通过。

    迭代通常是隐式的，譬如说一个集合类型没有实现 __contains__ 方法，那么 in 运算符就会按顺序做一次迭代搜索。
    >>> Card('Q', 'hearts') in deck
    True

    我们按照常规，用点数来判定扑克牌的大小，2 最小、A 最大；同时还要加上对花色的判定，黑桃最大、红桃次之、方块再次、梅花最小。下面就是按照这个规则来
    给扑克牌排序的函数，梅花 2 的大小是 0，黑桃 A 是 51：
    >>> for card in sorted(deck, key=spades_high): # doctest: +ELLIPSIS
    ...     print(card)
    Card(rank='2', suit='clubs')
    Card(rank='2', suit='diamonds')
    Card(rank='2', suit='hearts')
    ...
    Card(rank='A', suit='diamonds')
    Card(rank='A', suit='hearts')
    Card(rank='A', suit='spades')

    虽然 FrenchDeck 隐式地继承了 object 类， 但功能却不是继承而来的。我们通过数据模型和一些合成来实现这些功能。通过实现 __len__ 和
    __getitem__ 这两个特殊方法，FrenchDeck 就跟一个 Python 自有的序列数据类型一样，可以体现出 Python 的核心语言特性（例如迭代和切片）。同时
    这个类还可以用于标准库中诸如random.choice、reversed 和 sorted 这些函数。另外，对合成的运用使得 __len__ 和__getitem__ 的具体实现可以
    代理给 self._cards 这个 Python 列表（即 list 对象）。

    TIPS:
    在 Python 2 中，对 object 的继承需要显式地写为 FrenchDeck(object)；而在 Python 3 中，这个继承关系是默认的

    如何洗牌？
    按照目前的设计，FrenchDeck 是不能洗牌的，因为这摞牌是不可变的（immutable）：卡牌和它们的位置都是固定的，除非我们破坏这个类的封装性，直接对
    _cards 进行操作。
    """
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for rank in self.ranks for suit in self.suits]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


suit_value = dict(spades=3, hearts=2, diamonds=1, clubs=0)


def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value*len(suit_value) + suit_value[card.suit]


# 特殊方法的存在是为了被 Python 解释器调用的，你自己并不需要调用它们。也就是说没有 my_object.__len__() 这种写法，而应该使用 len(my_object)。
# 在执行 len(my_object) 的时候，如果 my_object 是一个自定义类的对象，那么 Python 会自己去调用其中由你实现的 __len__ 方法。

# 很多时候，特殊方法的调用是隐式的，比如 for i in x: 这个语句，背后其实用的是iter(x)，而这个函数的背后则是 x.__iter__() 方法。当然前提是这个
# 方法在 x 中被实现了。

# 模拟数值类型
# 利用特殊方法，可以让自定义对象通过加号“+”（或是别的运算符）进行运算，我们来实现一个二维向量（vector）类，类似下面这种：
# 一个二维向量加法的例子，Vector(2,4) + Vextor(2,1) = Vector(4,5)
"""
>>> v1 = Vector(2, 4)
>>> v2 = Vector(2, 1)
>>> v1 + v2
Vector(4, 5)
"""

# abs 是一个内置函数，如果输入是整数或者浮点数，它返回的是输入值的绝对值；如果输入是复数（complex number），那么返回这个复数的模。为了保持一致性，
# 我们的 API 在碰到 abs 函数的时候，也应该返回该向量的模.
"""
>>> v = Vector(3, 4)
>>> abs(v)
5.0
"""

# 我们还可以利用 * 运算符来实现向量的标量乘法（即向量与数的乘法，得到的结果向量的方向与原向量一致 ，模变大）：
"""
>>> v * 3
Vector(9, 12)
>>> abs(v * 3)
15.0
"""


# Vector实现
class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # 交互式控制台和调试程序（debugger）用 repr 函数来获取字符串表示形式；在老的使用% 符号的字符串格式中，这个函数返回的结果用来代替 %r 所代表的
    # 对象；同样，str.format 函数所用到的新式字符串格式化语也是利用了 repr，才把!r 字段变成字符串。

    # 在 __repr__ 的实现中，我们用到了 %r 来获取对象各个属性的标准字符串表示形式——这是个好习惯，它暗示了一个关键：Vector(1, 2) 和
    # Vector('1', '2') 是不一样的，后者在我们的定义中会报错，因为向量对象的构造函数只接受数值，不接受字符串。

    # __repr__ 所返回的字符串应该准确、无歧义，并且尽可能表达出如何用代码创建出这个被打印的对象。因此这里使用了类似调用对象构造器的表达形式（比如
    # Vector(3, 4)就是个例子）。

    # __repr__ 和 __str__ 的区别在于，后者是在 str() 函数被使用，或是在用 print 函数打印一个对象的时候才被调用的，并且它返回的字符串对终端用
    # 户更友好。如果你只想实现这两个特殊方法中的一个，__repr__ 是更好的选择，因为如果一个对象没有 __str__ 函数，而 Python 又需要调用它的时候，
    # 解释器会用 __repr__ 作为替代。
    def __repr__(self):
        return 'Vector(%r, %r)' % (self.x, self.y)

    # 通过 __add__ 和 __mul__，示例 1-2 为向量类带来了 + 和 * 这两个算术运算符。值得注意的是，这两个方法的返回值都是新创建的向量对象，被操作的
    # 两个向量（self 或other）还是原封不动，代码里只是读取了它们的值而已。中缀运算符的基本原则就是不改变操作对象，而是产出一个新的值
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))


# 为什么ｌｅｎ不是一个普通方法？
# 如果 x 是一个内置类型的实例，那么 len(x) 的速度会非常快。背后的原因是 CPython 会直接从一个 C 结构体里读取对象的长度，完全不会调用任何方法。获
# 取一个集合中元素的数量是一个很常见的操作，在 str、list、memoryview等类型上，这个操作必须高效。

# 换句话说，len 之所以不是一个普通方法，是为了让 Python 自带的数据结构可以走后门，abs 也是同理。但是多亏了它是特殊方法，我们也可以把 len 用于自
# 定义数据类型。这种处理方式在保持内置类型的效率和保证语言的一致性(这个形容非常贴切，对于len这个方法内置类型和自定义类型即在表现上达到了一个统一内置
# 类型又在性能上得到了一个保证)之间找到了一个平衡点，也印证了“Python 之禅”中的另外一句话：“不能让特例特殊到开始破坏既定规则。”。

# 没有破坏规则的原因个人理解是不用去定义一个单独的特殊方法去解释内置类型的长度，而是去复用了len这个规则只不过做了特殊处理。关键在于len定义成了一个特
# 殊方法，这个设计找到了平衡点


# 总结
# 通过实现特殊方法，自定义数据类型可以表现得跟内置类型一样，从而让我们写出更具表达力的代码——或者说，更具 Python 风格的代码。


# 魔术方法
# 在 Ruby 中也有类似“特殊方法”的概念，但是 Ruby 社区称之为“魔术方法”，而实际上 Python 社区里也有不少人用的是后者。而我恰恰认为“特殊方法”是“魔术
# 方法”的对立面。Python 和 Ruby 都利用了这个概念来提供丰富的元对象协议，这不是魔术，而是让语言的用户和核心开发者\拥有并使用同样的工具\。
# 考虑一下 JavaScript，情况就正好反过来了。JavaScript 中的对象有不透明的魔术般的特性，而你无法在自定义的对象中模拟这些行为。


# 元对象
# 元对象所指的是那些对建构语言本身来讲很重要的对象，以此为前提，协议也可以看作接口。也就是说，元对象协议是对象模型的同义词，它们的意思都是构建核心语
# 言的 API。一套丰富的元对象协议能让我们对语言进行扩展，让它支持新的编程范式.


if __name__ == '__main__':
    import doctest
    doctest.testmod()

