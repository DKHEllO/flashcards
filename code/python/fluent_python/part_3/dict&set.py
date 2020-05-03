#!/usr/bin/env python

import random
import timeit
from array import array

# dict 类型不但在各种程序里广泛使用，它也是 Python 语言的基石
# 正是因为字典至关重要，Python 对它的实现做了高度优化，而散列表则是字典类型性能出众的根本原因。集合（set）的实现其实也依赖于散列表。

# 然而，非抽象映射类型一般不会直接继承这些抽象基类，它们会直接对 dict 或是collections.User.Dict 进行扩展。这些抽象基类的主要作用是作为形式化的
# 文档，它们定义了构建一个映射类型所需要的最基本的接口。然后它们还可以跟 isinstance 一起被用来判定某个数据是不是广义上的映射类型：
"""
>>> my_dict = {}
>>> isinstance(my_dict, abc.Mapping)
True
"""

# 可散列的数据类型
# 如果一个对象是可散列的，那么在这个对象的生命周期中，它的散列值是不变的，而且这个对象需要实现 __hash__() 方法。另外可散列对象还要有__qe__() 方法
# ，这样才能跟其他键做比较。

# 原子不可变数据类型（str、bytes 和数值类型）都是可散列类型，frozenset 也是可散列的，因为根据其定义，frozenset 里只能容纳可散列类型。元组的话，
# 只有当一个元组包含的所有元素都是可散列类型的情况下，它才是可散列的
"""
>>> tt = (1, 2, (30, 40))
>>> hash(tt)
8027212646858338501
>>> tl = (1, 2, [30, 40])
>>> hash(tl)
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
>>> tf = (1, 2, frozenset([30, 40]))
>>> hash(tf)
-4118419923444501110
"""

# 创建字典的不同方式：
"""
>>> a = dict(one=1, two=2, three=3)
>>> b = {'one': 1, 'two': 2, 'three': 3}
>>> c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
>>> d = dict([('two', 2), ('one', 1), ('three', 3)])
>>> e = dict({'three': 3, 'one': 1, 'two': 2})
>>> a == b == c == d == e
True
"""

# 字典推导
"""
>>> DIAL_CODES = [ 
... (86, 'China'),
... (91, 'India'),
... (1, 'United States'),
... (62, 'Indonesia'),
... (55, 'Brazil'),
... (92, 'Pakistan'),
... (880, 'Bangladesh'),
... (234, 'Nigeria'),
... (7, 'Russia'),
... (81, 'Japan'),
... ]
>>> country_code = {country: code for code, country in DIAL_CODES} 
>>> country_code
{'China': 86, 'India': 91, 'Bangladesh': 880, 'United States': 1,
'Pakistan': 92, 'Japan': 81, 'Russia': 7, 'Brazil': 55, 'Nigeria':
234, 'Indonesia': 62}
>>> {code: country.upper() for country, code in country_code.items() 
... if code < 66}
{1: 'UNITED STATES', 55: 'BRAZIL', 62: 'INDONESIA', 7: 'RUSSIA'}
"""

# ------------------------
# 用setdefault处理找不到的键
# 获取单词的出现情况列表，如果单词不存在，把单词和一个空列表放进映射，然后返回这个空列表，这样就能在不进行第二次查找的情况下更新列表了。如果该key存在
# 会返回该key对应的value
"""
my_dict.setdefault(key, []).append(new_value) 
"""
"""
if key not in my_dict:
my_dict[key] = []
my_dict[key].append(new_value)
"""
# 二者的效果是一样的，只不过后者至少要进行两次键查询——如果键不存在的话，就是三次，用 setdefault 只需要一次就可以完成整个操作。


# 映射的弹性查询

# - defaultdict
# dd = defaultdict(list)，如果键 'new-key' 在 dd中还不存在的话，表达式 dd['new-key'] 会按照以下的步骤来行事。
# -- 调用 list() 来建立一个新列表
# -- 把这个新列表作为值，'new-key' 作为它的键，放到 dd 中。
# -- 返回这个列表的引用。
# 而这个用来生成默认值的可调用对象存放在名为 default_factory 的实例属性里。
# defaultdict 里的 default_factory 只会在 __getitem__ 里被调用，在其他的方法里完全不会发挥作用。比如，dd 是个 defaultdict，k 是个找不到
# 的键， dd[k] 这个表达式会调用 default_factory 创造某个默认值，而 dd.get(k)则会返回 None。
# 所有这一切背后的功臣其实是特殊方法 __missing__。它会在 defaultdict 遇到找不到的键的时候调用 default_factory，而实际上这个特性是所有映射类
# 型都可以选择去支持的。

# - 定义一个 dict 的子类，然后在子类中实现__missing__ 方法。如果有一个类继承了 dict，然后这个继承类提供了__missing__ 方法，那么在 __getite
# m__ 碰到找不到的键的时候，Python 就会自动调用它，而不是抛出一个 KeyError 异常。
# __missing__ 方法只会被 __getitem__ 调用（比如在表达式 d[k] 中）。提供 __missing__ 方法对 get 或者 __contains__（in 运算符会用到这个
# 方法）这些方法的使用没有影响。
# 如果要自定义一个映射类型，更合适的策略其实是继承collections.UserDict 类
# __ｍｉｓｓ__方法具体解释见ｓtr_key_dict文件


# -------------
# 字典的变种
# - collections.OrderedDict:这个类型在添加键的时候会保持顺序，因此键的迭代次序总是一致的。OrderedDict 的 popitem 方法默认删除并返回的是字
# 典里的最后一个元素，但是如果像 my_odict.popitem(last=False) 这样调用它，那么它删除并返回第一个被添加进去的元素。
# - collections.ChainMap:该类型可以容纳数个不同的映射对象，然后在进行键查找操作的时候，这些对象会被当作一个整体被逐个查找，直到键被找到为止。这
# 个功能在给有嵌套作用域的语言做解释器的时候很有用，可以用一个映射对象来代表一个作用域的上下文
# - collections.Counter:这个映射类型会给键准备一个整数计数器。每次更新一个键的时候都会增加这个计数器。所以这个类型可以用来给可散列表对象计数，或
# 者是当成多重集来用——多重集合就是集合里的元素可以出现不止一次。Counter 实现了 + 和 - 运算符用来合并记录，还有像 most_common([n]) 这类很有用
# 的方法。most_common([n]) 会按照次序返回映射里最常见的 n 个键和它们的计数
"""
>>> ct = collections.Counter('abracadabra')
>>> ct
Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
>>> ct.update('aaaaazzz')
>>> ct
Counter({'a': 10, 'z': 3, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
>>> ct.most_common(2)
[('a', 10), ('z', 3)]
"""
# - colllections.UserDict:这个类其实就是把标准 dict 用纯 Python 又实现了一遍。跟 OrderedDict、ChainMap 和 Counter 这些开箱即用的类型
# 不同，UserDict 是让用户继承写子类的。下面就来试试。


# -----------
# 子类化UserDict:更倾向于从 UserDict 而不是从 dict 继承的主要原因是，后者有时会在某些方法的实现上走一些捷径，导致我们不得不在它的子类中重写这些
# 方法，但是 UserDict 就不会带来这些问题。
# UserDict 并不是 dict 的子类，但是 UserDict 有一个叫作 data 的属性，是 dict 的实例，这个属性实际上是 UserDict 最终存储数据的地方。这样做
# 的好处是，比起示例 3-7，UserDict 的子类就能在实现 __setitem__ 的时候避免不必要的递归，也可以让 __contains__ 里的代码更简洁。
# 具体应用见　str_key_dict


# ----------
# 不可变映射类型
# 从 Python 3.3 开始，types 模块中引入了一个封装类名叫 MappingProxyType。如果给这个类一个映射，它会返回一个只读的映射视图。虽然是个只读视图，
# 但是它是动态的。这意味着如果对原映射做出了改动，我们通过这个视图可以观察到，但是无法通过这个视图对原映射做出修改。
"""
用 MappingProxyType 来获取字典的只读实例 mappingproxy
>>> from types import MappingProxyType
>>> d = {1:'A'}
>>> d_proxy = MappingProxyType(d)
>>> d_proxy
mappingproxy({1: 'A'})
>>> d_proxy[1] 
'A'
>>> d_proxy[2] = 'x' 
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
TypeError: 'mappingproxy' object does not support item assignment
>>> d[2] = 'B'
>>> d_proxy 
mappingproxy({1: 'A', 2: 'B'})
>>> d_proxy[2]
'B'
>>>
"""
# 因此在 Pingo.io 中我们是这样用它的：Board 的具体子类会提供一个包含针脚信息的私有映射成员，然后通过公开属性 .pins 把这个映射暴露给 API 的客户，
# 而 .pins 属性其实就是用 mappingproxy 实现的。一旦这样写好了，客户就不能对这个映射进行任何意外的添加、移除或者修改操作。


# -----------------------------------------
# 集合论：集合的本质是许多唯一对象的聚集。因此集合可以去重。
# 集合中的元素必须是可散列的，set 类型本身是不可散列的，但是 frozenset 可以。

# 除了保证唯一性，集合还实现了很多基础的中缀运算符。给定两个集合 a 和 b，a | b 返回的是它们的合集，a & b 得到的是交集，而 a - b 得到的是差集。
# 合理地利用这些操作，不仅能够让代码的行数变少，还能减少 Python 程序的运行时间。
"""
needles 的元素在 haystack 里出现的次数，两个变量都是 set 类型
found = len(needles & haystack)
needles 的元素在 haystack 里出现的次数（作用上述相同）
found = 0
for n in needles:
    if n in haystack:
        found += 1
"""
# 使用集合操作速度会快一些
# 除了速度极快的查找功能（这也得归功于它背后的散列表），内置的 set 和 frozenset提供了丰富的功能和操作，不但让创建集合的方式丰富多彩，而且对于 set
# 来讲，我们还可以对集合里已有的元素进行修改。

# 集合字面量
# 除空集之外，集合的字面量——{1}、{1, 2}，等等——看起来跟它的数学形式一模一样。如果是空集，那么必须写成 set() 的形式。如果只是写成 {} 的形式，跟以
# 前一样，你创建的其实是个空字典。
# 像 {1, 2, 3} 这种字面量句法相比于构造方法（set([1, 2, 3])）要更快且更易读。后者的速度要慢一些，因为 Python 必须先从 set 这个名字来查询构造
# 方法，然后新建一个列表，最后再把这个列表传入到构造方法里。但是如果是像 {1, 2, 3} 这样的字面量，Python 会利用一个专门的叫作 BUILD_SET 的字节码
# 来创建集合。

# 集合推导
"""
>>> from unicodedata import name 
>>> {chr(i) for i in range(32, 256) if 'SIGN' in name(chr(i),'')}
{'§', '=', '¢', '#', '¤', '<', '¥', 'μ', '×', '$', '¶', '£', '©', '°', '+', '÷', '±', '>', '¬', '®', '%'}
"""


# ------------------------------------------------------------------------------
# dict和set的背后
# - Python 里的 dict 和 set 的效率有多高？
# - 为什么它们是无序的？
# - 为什么并不是所有的 Python 对象都可以当作 dict 的键或 set 里的元素？
# - 为什么 dict 的键和 set 元素的顺序是跟据它们被添加的次序而定的，以及为什么在映射对象的生命周期中，这个顺序并不是一成不变的？
# - 为什么不应该在迭代循环 dict 或是 set 的同时往里添加元素？

# 一个关于效率的实验

TIMES = 10000
SETUP = """
import random
from array import array
haystack = array('d', (random.random() for _ in range(1000)))
needles = array('d', (random.choice(haystack) for _ in range(500)))
haystack = dict.fromkeys(haystack)
"""

command = """found = 0
for n in needles:
    if n in haystack:
        found += 1"""


def test_dict(label, cmd):
    res = timeit.repeat(cmd, setup=SETUP, number=10000)
    print(label, *('{:.3f}'.format(x) for x in res))


test_dict('dict', command)


# ---------------------------
# 字典中的散列表
# 散列表其实是一个稀疏数组（总是有空白元素的数组称为稀疏数组）。在一般的数据结构教材中，散列表里的单元通常叫作表元（bucket）。在 dict 的散列表当中，
# 每个键值对都占用一个表元，每个表元都有两个部分，一个是对键的引用，另一个是对值的引用。因为所有表元的大小一致，所以可以通过偏移量来读取某个表元。

# Python 会设法保证大概还有三分之一的表元是空的，所以在快要达到这个阈值的时候，原有的散列表会被复制到一个更大的空间里面。如果要把一个对象放入散列表，
# 那么首先要计算这个元素键的散列值。Python 中可以用hash() 方法来做这件事情。
# - 内置的 hash() 方法可以用于所有的内置类型对象。如果是自定义对象调用 hash()的话，实际上运行的是自定义的 __hash__。为了让散列值能够胜任散列表
# 索引这一角色，它们必须在索引空间中尽量分散开来。这意味着在最理想的状况下，越是相似但不相等的对象，它们散列值的差别应该越
# 大
# - 散列表算法。为了获取 my_dict[search_key] 背后的值，Python 首先会调用 hash(search_key)来计算 search_key 的散列值，把这个值最低的几位
# 数字当作偏移量，在散列表里查找表元（具体取几位，得看当前散列表的大小）。若找到的表元是空的，则抛出KeyError 异常。若不是空的，则表元里会有一对
# found_key:found_value。这时候 Python 会检验 search_key == found_key 是否为真，如果它们相等的话，就会返回 found_value。如果
# search_key 和 found_key 不匹配的话，这种情况称为散列冲突。发生这种情况是因为，散列表所做的其实是把随机的元素映射到只有几位的数字上，而散列表本
# 身的索引又只依赖于这个数字的一部分。为了解决散列冲突，算法会在散列值中另外再取几位，然后用特殊的方法处理一下，把新得到的数字再当作索引来寻找表元。
# 若这次找到的表元是空的，则同样抛出 KeyError；若非空，或者键匹配，则返回这个值；或者又发现了散列冲突，则重复以上的步骤。
# 添加新元素和更新现有键值的操作几乎跟上面一样。只不过对于前者，在发现空表元的时候会放入一个新元素；对于后者，在找到相对应的表元后，原表里的值对象会被
# 替换成新值。
# 另外在插入新值时，Python 可能会按照散列表的拥挤程度来决定是否要重新分配内存为它扩容。如果增加了散列表的大小，那散列值所占的位数和用作索引的位数都
# 会随之增加，这样做的目的是为了减少发生散列冲突的概率。
# 表面上看，这个算法似乎很费事，而实际上就算 dict 里有数百万个元素，多数的搜索过程中并不会有冲突发生，平均下来每次搜索可能会有一到两次冲突。在正常情
# 况下，就算是最不走运的键所遇到的冲突的次数用一只手也能数过来。

# dict的实现及其导致的结果
# - 键必须是可散列的:一个可散列的对象必须满足以下要求。
# (1) 支持 hash() 函数，并且通过 __hash__() 方法所得到的散列值是不变的。
# (2) 支持通过 __eq__() 方法来检测相等性。
# (3) 若 a == b 为真，则 hash(a) == hash(b) 也为真。
# 所有由用户自定义的对象默认都是可散列的，因为它们的散列值由 id() 来获取，而且它们都是不相等的。
# - 字典在内存上的开销巨大
# 由于字典使用了散列表，而散列表又必须是稀疏的，这导致它在空间上的效率低下。举例而言，如果你需要存放数量巨大的记录，那么放在由元组或是具名元组构成的列
# 表中会是比较好的选择；最好不要根据 JSON 的风格，用由字典组成的列表来存放这些记录。用元组取代字典就能节省空间的原因有两个：其一是避免了散列表所耗费
# 的空间，其二是无需把记录中字段的名字在每个元素里都存一遍。
# 在用户自定义的类型中，__slots__ 属性可以改变实例属性的存储方式，由 dict 变成 tuple
# - 键查询很快
# dict 的实现是典型的空间换时间：字典类型有着巨大的内存开销，但它们提供了无视数据量大小的快速访问——只要字典能被装在内存里。
# - 键的次序取决于添加顺序
# 当往 dict 里添加新键而又发生散列冲突的时候，新键可能会被安排存放到另一个位置。于是下面这种情况就会发生：由 dict([key1, value1), (key2, value2)]
# 和 dict([key2, value2], [key1, value1]) 得到的两个字典，在进行比较的时候，它们是相等的；但是如果在 key1 和 key2 被添加到字典里的过程中
# 有冲突发生的话，这两个键出现在字典里的顺序是不一样的。
# - 往字典里添加新键可能会改变已有键的顺序
# 无论何时往字典里添加新的键，Python 解释器都可能做出为字典扩容的决定。扩容导致的结果就是要新建一个更大的散列表，并把字典里已有的元素添加到新表里。
# 这个过程中可能会发生新的散列冲突，导致新散列表中键的次序变化.
# 如果你在迭代一个字典的所有键的过程中同时对字典进行修改，那么这个循环很有可能会跳过一些键——甚至是跳过那些字典中已经有的键。不要对字典同时进行迭代和
# 修改。如果想扫描并修改一个字典，最好分成两步来进行：首先对字典迭代，以得出需要添加的内容，把这些内容放在一个新字典里；迭代结束之后再对原有字典进行更
# 新。


# --------------
# set的实现以及导致的结果
# 集合很消耗内存。
# 可以很高效地判断元素是否存在于某个集合。
# 元素的次序取决于被添加到集合里的次序。
# 往集合里添加元素，可能会改变集合里已有元素的次序。


# 总结
# 1、特殊映射类型:比如 defaultdict、OrderedDict、ChainMap 和 Counter。便于扩展的 UserDict 类。
# ２、setdefault 和 update。setdefault 方法可以用来更新字典里存放的可变值（比如列表），从而避免了重复的键搜索。update方法则让批量更新成为可能，
# 它可以用来插入新值或者更新已有键值对，它的参数可以是包含 (key, value) 这种键值对的可迭代对象，或者关键字参数。
# 3、有个很好用的方法是 __missing__，当对象找不到某个键的时候，可以通过这个方法自定义会发生什么。
# 4、collections.abc 模块提供了 Mapping 和 MutableMapping 这两个抽象基类，利用它们，我们可以进行类型查询或者引用。不太为人所知的
# MappingProxyType 可以用来创建不可变映射对象，它被封装在 types 模块中。另外还有 Set 和 MutableSet 这两个抽象基类。
# 5、dict 和 set 背后的散列表效率很高，被保存的元素会呈现出不同的顺序，以及已有的元素顺序会发生变化，速度是以牺牲空间为代价而换来的。






