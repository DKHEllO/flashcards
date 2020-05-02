#!/usr/bin/env python

import timeit

# 深入理解 Python 中的不同序列类型，不但能让我们避免重新发明轮子，它们的 API 还能帮助我们把自己定义的 API 设计得跟原生的序列一样，或者是跟未来可
# 能出现的序列类型保持兼容。

# 内置的序列类型
# - 容器序列：list、tuple 和 collections.deque 这些序列能存放不同类型的数据。
# - 扁平序列：str、bytes、bytearray、memoryview 和 array.array，这类序列只能容纳一种类型。
# 容器序列存放的是它们所包含的任意类型的对象的引用。而扁平序列里存放的是值而不是引用。换句话说，扁平序列其实是一段连续的内存空间。由此可见扁平序列其实
# 更加紧凑，但是它里面只能存放诸如字符、字节和数值这种基础类型。

# 序列类型还能按照能否被修改来分类。
# - 可变序列:list、bytearray、array.array、collections.deque 和 memoryview。
# - 不可变序列:tuple、str 和 bytes。

# ---------------------------
# 列表推导（list comprehension）。列表推导是构建列表（list）的快捷方式，而生成器表达式（generator expression）则可以用来创建其他任何类型
# 的序列。

# 通常的原则是，只用列表推导来创建新的列表，并且尽量保持简短。如果列表推导的代码超过了两行，你可能就要考虑是不是得用 for 循环重写了。

"""
>>> symbols = '$¢£¥€¤'
>>> codes = [ord(symbol) for symbol in symbols]
>>> codes
[36, 162, 163, 165, 8364, 164]
"""

# Python 2.x 中，在列表推导中 for 关键词之后的赋值操作可能会影响列表推导上下文中的同名变量
"""
>>> x = 'my precious'
>>> dummy = [x for x in 'ABC']
>>> x
'C'
"""

# 列表推导、生成器表达式，以及同它们很相似的集合（set）推导和字典（dict）推导，在 Python 3 中都有了自己的局部作用域，就像函数似的。表达式内部的变
# 量和赋值只在局部起作用，表达式的上下文里的同名变量还可以被正常引用，局部变量并不会影响到它们。
# 列表推导可以帮助我们把一个序列或是其他可迭代类型中的元素过滤或是加工，然后再新建一个列表。Python 内置的 filter 和 map 函数组合起来也能达到这一
# 效果，但是可读性上打了不小的折扣。

# map/filter实现类似列表推导的功能
"""
>>> symbols = '$¢£¥€¤'
>>> beyond_ascii = [ord(s) for s in symbols if ord(s) > 127]
>>> beyond_ascii
[162, 163, 165, 8364, 164]
>>> beyond_ascii = list(filter(lambda c: c > 127, map(ord, symbols)))
>>> beyond_ascii
[162, 163, 165, 8364, 164]
"""

# 可读性相比于列表推导较低，效率测试如下：

TIMES = 10000

SETUP = """
symbols = '$¢£¥€¤'
def non_ascii(c):
    return c > 127
"""


def clock(label, cmd):
    # 这是一个方便的函数，它反复调用 timeit() ，返回结果列表。第一个参数指定调用 timeit() 的次数。第二个参数指定 timeit() 的 number 参数
    res = timeit.repeat(cmd, setup=SETUP, number=TIMES, repeat=5)
    print(label, *('{:.3f}'.format(x) for x in res))


clock('listcomp        :', '[ord(s) for s in symbols if ord(s) > 127]')
clock('listcomp + func :', '[ord(s) for s in symbols if non_ascii(ord(s))]')
clock('filter + lambda :', 'list(filter(lambda c: c > 127, map(ord, symbols)))')
clock('filter + func   :', 'list(filter(non_ascii, map(ord, symbols)))')

# 列表推导的作用只有一个：生成列表。如果想生成其他类型的序列，生成器表达式就派上了用场。

# -----------
# 生成器表达式。虽然也可以用列表推导来初始化元组、数组或其他序列类型，但是生成器表达式是更好的选择。这是因为生成器表达式背后遵守了迭代器协议，可以逐个
# 地产出元素，而不是先建立一个完整的列表，然后再把这个列表传递到某个构造函数里。前面那种方式显然能够节省内存。
# 生成器表达式的语法跟列表推导差不多，只不过把方括号换成圆括号而已。
"""
>>> symbols = '$¢£¥€¤'
如果生成器表达式是一个函数调用过程中的唯一参数，那么不需要额外再用括号把它围起来。
>>> tuple(ord(symbol) for symbol in symbols) 
(36, 162, 163, 165, 8364, 164)
>>> import array
>>> array.array('I', (ord(symbol) for symbol in symbols)) 
array('I', [36, 162, 163, 165, 8364, 164])
"""

# -----------
# 元组。元组其实是对数据的记录：元组中的每个元素都存放了记录中一个字段的数据，外加这个字段的位置。正是这个位置信息给数据赋予了意义。
# 如果只把元组理解为不可变的列表，那其他信息——它所含有的元素的总数和它们的位置——似乎就变得可有可无。但是如果把元组当作一些字段的集合，那么数量和位置
# 信息就变得非常重要了。

# 元组拆包
"""
>>> lax_coordinates = (33.9425, -118.408056)
>>> latitude, longitude = lax_coordinates # 元组拆包
>>> latitude
33.9425
>>> longitude
-118.408056
"""
# 不使用中间变量交换两个变量的值：
"""
>>> b, a = a, b
"""
# 还可以用 * 运算符把一个可迭代对象拆开作为函数的参数：
"""
>>> divmod(20, 8)
(2, 4)
>>> t = (20, 8)
>>> divmod(*t)
(2, 4)
>>> quotient, remainder = divmod(*t)
>>> quotient, remainder
(2, 4)
"""

# 在进行拆包的时候，我们不总是对元组里所有的数据都感兴趣，_ 占位符能帮助处理这种情况，上面这段代码也展示了它的用法。
# 除此之外，在元组拆包中使用 * 也可以帮助我们把注意力集中在元组的部分元素上。用*来处理剩下的元素.在 Python 中，函数用 *args 来获取不确定数量的参
# 数算是一种经典写法了。于是 Python 3 里，这个概念被扩展到了平行赋值中：
"""
>>> a, b, *rest = range(5)
>>> a, b, rest
(0, 1, [2, 3, 4])
>>> a, b, *rest = range(3)
>>> a, b, rest
(0, 1, [2])
>>> a, b, *rest = range(2)
>>> a, b, rest
(0, 1, [])
"""

# 嵌套元组拆包
# 接受表达式的元组可以是嵌套式的，例如 (a, b, (c, d))。只要这个接受元组的嵌套结构符合表达式本身的嵌套结构，Python 就可以作出正确的对应。
"""
>>> metro_areas = [
('Tokyo','JP',36.933,(35.689722,139.691667)), 
('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]
>>> print('{:15} | {:^9} | {:^9}'.format('', 'lat.', 'long.'))
>>> fmt = '{:15} | {:9.4f} | {:9.4f}'
>>> for name, cc, pop, (latitude, longitude) in metro_areas: 
        if longitude <= 0: 
            print(fmt.format(name, latitude, longitude))
"""

# 具名元组
# collections.namedtuple 是一个工厂函数，它可以用来构建一个带字段名的元组和一个有名字的类——这个带名字的类对调试程序有很大帮助。为啥对调试程序有
# 比较大的帮助？
# 用 namedtuple 构建的类的实例所消耗的内存跟元组是一样的，因为字段名都被存在对应的类里面。这个实例跟普通的对象实例比起来也要小一些，因为 Python
# 不会用 __dict__ 来存放这些实例的属性。
# 除了从普通元组那里继承来的属性之外，具名元组还有一些自己专有的属性。示例 2-10中就展示了几个最有用的：_fields 类属性、类方法 _make(iterable)
# 和实例方法_asdict()。
"""
>>> City._fields 
('name', 'country', 'population', 'coordinates')
>>> LatLong = namedtuple('LatLong', 'lat long')
>>> delhi_data = ('Delhi NCR', 'IN', 21.935, LatLong(28.613889, 77.208889))
>>> delhi = City._make(delhi_data) 
>>> delhi._asdict() 
OrderedDict([('name', 'Delhi NCR'), ('country', 'IN'), ('population',
21.935), ('coordinates', LatLong(lat=28.613889, long=77.208889))])
>>> for key, value in delhi._asdict().items():
        print(key + ':', value)
name: Delhi NCR
country: IN
population: 21.935
coordinates: LatLong(lat=28.613889, long=77.208889)
>>>
"""

# _asdict() 把具名元组以 collections.OrderedDict 的形式返回，我们可以利用它来把元组里的信息友好地呈现出来。


# -----------------
# 切片。符合这本书的哲学：先讲用法，第四部分中再来讲如何创建新类。
# 为什么切片和区间会忽略最后一个元素?
# - 当只有最后一个位置信息时，我们也可以快速看出切片和区间里有几个元素：range(3) 和 my_list[:3] 都返回 3 个元素。
# - 当起止位置信息都可见时，我们可以快速计算出切片和区间的长度，用后一个数减去第一个下标（stop - start）即可。
# - 这样做也让我们可以利用任意一个下标来把序列分割成不重叠的两部分，只要写成my_list[:x] 和 my_list[x:] 就可以了，如下所示。
"""
>>> l = [10, 20, 30, 40, 50, 60]
>>> l[:2] # 在下标2的地方分割
[10, 20]
>>> l[2:]
[30, 40, 50, 60]
>>> l[:3] # 在下标3的地方分割
[10, 20, 30]
>>> l[3:]
[40, 50, 60]
"""

# 我们还可以用 s[a:b:c] 的形式对 s 在 a 和 b 之间以 c 为间隔取值。c 的值还可以为负，负值意味着反向取值。
"""
>>> s = 'bicycle'
>>> s[::3]
'bye'
>>> s[::-1]
'elcycib'
>>> s[::-2]
'eccb'
"""
# 给切片命名
# 对 seq[start:stop:step] 进行求值的时候，Python 会调用seq.__getitem__(slice(start, stop, step))。就算你还不会自定义序列类型，了
# 解一下切片对象也是有好处的。例如你可以给切片命名，就像电子表格软件里给单元格区域取名字一样。
# 比如，要解析示例 2-11 中所示的纯文本文件，这时使用有名字的切片比用硬编码的数字区间要方便得多，注意示例里的 for 循环的可读性有多强。
"""
>>> invoice = "
    0.....6................................40........52...55........
    1909 Pimoroni PiBrella $17.50 3 $52.50
    1489 6mm Tactile Switch x20 $4.95 2 $9.90
    1510 Panavise Jr. - PV-201 $28.00 1 $28.00
    1601 PiTFT Mini Kit 320x240 $34.95 1 $34.95
    "
>>> SKU = slice(0, 6)
>>> DESCRIPTION = slice(6, 40)
>>> UNIT_PRICE = slice(40, 52)
>>> QUANTITY = slice(52, 55)
>>> ITEM_TOTAL = slice(55, None)
>>> line_items = invoice.split('\n')[2:]
>>> for item in line_items:
... print(item[UNIT_PRICE], item[DESCRIPTION])
...
$17.50 Pimoroni PiBrella
$4.95 6mm Tactile Switch x20
$28.00 Panavise Jr. - PV-201
$34.95 PiTFT Mini Kit 320x240
"""

# 对序列使用+和*
# + 和 * 都遵循这个规律，不修改原有的操作对象，而是构建一个全新的序列。

# 如果在 a * n 这个语句中，序列 a 里的元素是对其他可变对象的引用的话，你就需要格外注意了，因为这个式子的结果可能会出乎意料。比如，你想用my_list =
# [[]] * 3 来初始化一个由列表组成的列表，但是你得到的列表里包含的 3 个元素其实是 3 个引用，而且这 3 个引用指向的都是同一个列表。这可能不是你想要的
# 效果。

"""
>>> board = [['_'] * 3 for i in range(3)] 
>>> board
[['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
>>> board[1][2] = 'X' 
>>> board
[['_', '_', '_'], ['_', '_', 'X'], ['_', '_', '_']]
"""

# 错误的做法
"""
>>> weird_board = [['_'] * 3] * 3 
>>> weird_board
[['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
>>> weird_board[1][2] = 'O' 
>>> weird_board
[['_', '_', 'O'], ['_', '_', 'O'], ['_', '_', 'O']]
"""
# 外面的列表其实包含 3 个指向同一个列表的引用。当我们不做修改的时候，看起来都还好。
# 一旦我们试图标记第 1 行第 2 列的元素，就立马暴露了列表内的 3 个引用指向同一个对象的事实

# 序列的增量赋值
# += 背后的特殊方法是 __iadd__ （用于“就地加法”）。但是如果一个类没有实现这个方法的话，Python 会退一步调用 __add__ 。
# >>> a += b
# 如果 a 实现了 __iadd__ 方法，就会调用这个方法。同时对可变序列（例如list、bytearray 和 array.array）来说，a 会就地改动，就像调用了 a.ext
# end(b)一样。但是如果 a 没有实现 __iadd__ 的话，a += b 这个表达式的效果就变得跟 a = a + b 一样了：首先计算 a + b，得到一个新的对象，然后赋
# 值给 a。也就是说，在这个表达式中，变量名会不会被关联到新的对象，完全取决于这个类型有没有实现 __iadd__ 这个方法。

# 接下来有个小例子，展示的是 *= 在可变和不可变序列上的作用：
"""
>>> l = [1, 2, 3]
>>> id(l)
4311953800 
>>> l *= 2
>>> l
[1, 2, 3, 1, 2, 3]
>>> id(l)
4311953800 
>>> t = (1, 2, 3)
>>> id(t)
4312681568 
>>> t *= 2
>>> id(t)
4301348296 
"""

# 对不可变序列进行重复拼接操作的话，效率会很低，因为每次都有一个新对象，而解释器需要把原来对象中的元素先复制到新的对象里，然后再追加新的元素

# 一个关于+=的谜题
# 示例 2-14 中的两个表达式到底会产生什么结果？
"""
>>> t = (1, 2, [30, 40])
>>> t[2] += [50, 60]
"""
# 没人料到的结果：t[2] 被改动了，但是也有异常抛出
"""
>>> t = (1, 2, [30, 40])
>>> t[2] += [50, 60]
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
>>> t
(1, 2, [30, 40, 50, 60])
"""
# s[a] = b 背后的字节码
"""
>>> dis.dis('s[a] += b')
1 0 LOAD_NAME 0(s)
3 LOAD_NAME 1(a)
6 DUP_TOP_TWO
7 BINARY_SUBSCR # 将 s[a] 的值存入 TOS（Top Of Stack，栈的顶端）。
8 LOAD_NAME 2(b)
11 INPLACE_ADD # 计算 TOS += b。这一步能够完成，是因为 TOS 指向的是一个可变对象（也就是示例2-15 里的列表）。
12 ROT_THREE
13 STORE_SUBSCR # s[a] = TOS 赋值。这一步失败，是因为 s 是不可变的元组（示例 2-15 中的元组t）。
14 LOAD_CONST 0(None)
17 RETURN_VALUE
"""

# 划重点
# - 不要把可变对象放在元组里
# - 增量赋值不是一个原子操作。我们刚才也看到了，它虽然抛出了异常，但还是完成了操作。
# - 查看 Python 的字节码并不难，而且它对我们了解代码背后的运行机制很有帮助。

# 排序
# list.sort 方法会就地排序列表，也就是说不会把原列表复制一份。如果一个函数或者方法对对象进行的是就地改动，那它就应该返回 None，好让调用者知道传入
# 的参数发生了变动，而且并未产生新的对象。例如，random.shuffle 函数也遵守了这个惯例。
# 与 list.sort 相反的是内置函数 sorted，它会新建一个列表作为返回值。这个方法可以接受任何形式的可迭代对象作为参数，甚至包括不可变序列或生成器（见
# 第 14 章）。而不管 sorted 接受的是怎样的参数，它最后都会返回一个列表。
# sort和sorted的参数：
# - reverse：如果被设定为 True，被排序的序列里的元素会以降序输出（也就是说把最大值当作最小值来排序）。这个参数的默认值是 False。
# - key：一个只有一个参数的函数，这个函数会被用在序列里的每一个元素上，所产生的结果将是排序算法依赖的对比关键字。比如说，在对一些字符串排序时，可以用
#        key=str.lower 来实现忽略大小写的排序，或者是用 key=len 进行基于字符串长度的排序。这个参数的默认值是恒等函数（identity function），
#        也就是默认用元素自己的值来排序。
fruits = ['grape', 'raspberry', 'apple', 'banana']
"""
>>> sorted(fruits)
['apple', 'banana', 'grape', 'raspberry'] 
>>> fruits
['grape', 'raspberry', 'apple', 'banana'] 
>>> sorted(fruits, reverse=True)
['raspberry', 'grape', 'banana', 'apple'] 
>>> sorted(fruits, key=len)
['grape', 'apple', 'banana', 'raspberry'] 
>>> sorted(fruits, key=len, reverse=True)
['raspberry', 'banana', 'grape', 'apple'] 
>>> fruits
['grape', 'raspberry', 'apple', 'banana'] 
>>> fruits.sort() 
>>> fruits
['apple', 'banana', 'grape', 'raspberry'] 
"""
# 已排序的序列可以用来进行快速搜索，而标准库的 bisect 模块给我们提供了二分查找算法

# ---------
# 用bisect来管理已排序的序列.
# bisect 模块包含两个主要函数，bisect 和 insort，两个函数都利用二分查找算法来在有序序列中查找或插入元素。bisect(haystack, needle) 在 hays
# tack（干草垛）里搜索 needle（针）的位置，该位置满足的条件是，把 needle 插入这个位置之后，haystack 还能保持升序。也就是在说这个函数返回的位置
# 前面的值，都小于或等于 needle 的值。其中 haystack 必须是一个有序的序列。你可以先用 bisect(haystack, needle) 查找位置 index，再用haysta
# ck.insert(index, needle) 来插入新值。但你也可用 insort 来一步到位，并且后者的速度更快一些。

# 具体示例见bisect_demo

# ---------
# 当列表不是首选。虽然列表既灵活又简单，但面对各类需求时，我们可能会有更好的选择。比如，要存放1000 万个浮点数的话，数组（array）的效率要高得多，因为
# 数组在背后存的并不是float 对象，而是数字的机器翻译，也就是字节表述。这一点就跟 C 语言中的数组一样。再比如说，如果需要频繁对序列做先进先出的操作，
# deque（双端队列）的速度应该会更快。
# 如果在你的代码里，包含操作（比如检查一个元素是否出现在一个集合中）的频率很高，用 set（集合）会更合适。set 专为检查元素是否存在做过优化。但是它
# 并不是序列，因为 set 是无序的。

# 数组
# 如果我们需要一个只包含数字的列表，那么 array.array 比 list 更高效。数组支持所有跟可变序列有关的操作，包括 .pop、.insert 和 .extend。另外，
# 数组还提供从文件读取和存入文件的更快的方法，如 .frombytes 和 .tofile。
# Python 数组跟 C 语言数组一样精简。创建数组需要一个类型码，这个类型码用来表示在底层的 C 语言应该存放怎样的数据类型。比如 b 类型码代表的是有符号的
# 字符（signedchar），因此 array('b') 创建出的数组就只能存放一个字节大小的整数，范围从 -128到 127，这样在序列很大的时候，我们能节省很多空间。
# 而且 Python 不会允许你在数组里存放除指定类型之外的数据。
# array类型码：https://docs.python.org/zh-cn/3/library/array.html

# 创建一个有 1000 万个随机浮点数的数组
"""
>>> from array import array 
>>> from random import random
>>> floats = array('d', (random() for i in range(10**7))) 
>>> floats[-1] 
0.07802343889111107
>>> fp = open('floats.bin', 'wb')
>>> floats.tofile(fp) 
>>> fp.close()
>>> floats2 = array('d') 
>>> fp = open('floats.bin', 'rb')
>>> floats2.fromfile(fp, 10**7) 
>>> fp.close()
>>> floats2[-1] 
0.07802343889111107
>>> floats2 == floats 
True
"""
# 从上面的代码我们能得出结论，array.tofile 和 array.fromfile 用起来很简单。把这段代码跑一跑，你还会发现它的速度也很快。一个小试验告诉我，用
# array.fromfile从一个二进制文件里读出 1000 万个双精度浮点数只需要 0.1 秒，这比从文本文件里读取的速度要快 60 倍，因为后者会使用内置的 float
# 方法把每一行文字转换成浮点数。另外，使用 array.tofile 写入到二进制文件，比以每行一个浮点数的方式把所有数字写入到文本文件要快 7 倍。另外，1000
# 万个这样的数在二进制文件里只占用 80 000 000 个字节（每个浮点数占用 8 个字节，不需要任何额外空间），如果是文本文件的话，我们需要 181 515 739
# 个字节。
# 另外一个快速序列化数字类型的方法是使用pickle（https://docs.python.org/3/library/pickle.html）模块。pickle.dump 处理浮点数组的速度几乎
# 跟 array.tofile 一样快。不过前者可以处理几乎所有的内置数字类型，包含复数、嵌套集合，甚至用户自定义的类。前提是这些类没有什么特别复杂的实现。


# ----------
# 内存视图
# memoryview 是一个内置类，它能让用户在不复制内容的情况下操作同一个数组的不同切片。
# 内存视图其实是泛化和去数学化的 NumPy 数组。它让你在不需要复制内容的前提下，在数据结构之间共享内存。其中数据结构可以是任何形式，比如 PIL 图片、
# SQLite 数据库和 NumPy 的数组，等等。这个功能在处理大型数据集合的时候非常重要。

# memoryview.cast 的概念跟数组模块类似，能用不同的方式读写同一块内存数据，而且内容字节不会随意移动。这听上去又跟 C 语言中类型转换的概念差不多。
# memoryview.cast 会把同一块内存里的内容打包成一个全新的 memoryview 对象给你。
"""
>>> numbers = array.array('h', [-2, -1, 0, 1, 2])
>>> memv = memoryview(numbers) 利用含有 5 个短整型有符号整数的数组（类型码是 'h'）创建一个 memoryview
>>> len(memv)
5 >>> memv[0] memv 里的 5 个元素跟数组里的没有区别。
-2
>>> memv_oct = memv.cast('B') 创建一个 memv_oct，这一次是把 memv 里的内容转换成 'B' 类型，也就是无符号字符。
>>> memv_oct.tolist() 以列表的形式查看 memv_oct 的内容。
[254, 255, 255, 255, 0, 0, 1, 0, 2, 0]
>>> memv_oct[5] = 4 把位于位置 5 的字节赋值成 4。
>>> numbers
array('h', [-2, -1, 1024, 1, 2]) 因为我们把占 2 个字节的整数的高位字节改成了 4，所以这个有符号整数的值就变成了 1024。
"""
# 有符号整数和无符号整数的区别？

# ------------
# NumPy和SciPy
# NumPy 实现了多维同质数组（homogeneous array）和矩阵，这些数据结构不但能处理数字，还能存放其他由用户定义的记录。通过 NumPy，用户能对这些数据
# 结构里的元素进行高效的操作。
# SciPy 是基于 NumPy 的另一个库，它提供了很多跟科学计算有关的算法，专为线性代数、数值积分和统计学而设计。

# ------------
# 双向队列和其他形式的队列
# 利用 .append 和 .pop 方法，我们可以把列表当作栈或者队列来用（比如，把 .append和 .pop(0) 合起来用，就能模拟栈的“先进先出”的特点）。但是删除列
# 表的第一个元素（抑或是在第一个元素之前添加一个元素）之类的操作是很耗时的，因为这些操作会牵扯到移动列表里的所有元素。

# collections.deque 类（双向队列）是一个线程安全、可以快速从两端添加或者删除元素的数据类型。而且如果想要有一种数据类型来存放“最近用到的几个元素”，
# deque 也是一个很好的选择。这是因为在新建一个双向队列的时候，你可以指定这个队列的大小，如果这个队列满员了，还可以从反向端删除过期的元素，然后在尾端
# 添加新的元素。示例2-23 中有几个双向队列的典型操作。
"""
>>> from collections import deque
>>> dq = deque(range(10), maxlen=10) maxlen 是一个可选参数，代表这个队列可以容纳的元素的数量，而且一旦设定，这个属性就不能修改了。
>>> dq
deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], maxlen=10)
>>> dq.rotate(3) 队列的旋转操作接受一个参数 n，当 n > 0 时，队列的最右边的 n 个元素会被移动到队列的左边。当 n < 0 时，最左边的 n 个元素会被移
动到右边。
>>> dq
deque([7, 8, 9, 0, 1, 2, 3, 4, 5, 6], maxlen=10)
>>> dq.rotate(-4)
>>> dq
deque([1, 2, 3, 4, 5, 6, 7, 8, 9, 0], maxlen=10)
>>> dq.appendleft(-1) 当试图对一个已满（len(d) == d.maxlen）的队列做尾部添加操作的时候，它头部的元素会被删除掉。注意在下一行里，元素 0 被
删除了。
>>> dq
deque([-1, 1, 2, 3, 4, 5, 6, 7, 8, 9], maxlen=10)
>>> dq.extend([11, 22, 33]) 在尾部添加 3 个元素的操作会挤掉 -1、1 和 2。
>>> dq
deque([3, 4, 5, 6, 7, 8, 9, 11, 22, 33], maxlen=10)
>>> dq.extendleft([10, 20, 30, 40]) extendleft(iter) 方法会把迭代器里的元素逐个添加到双向队列的左边，因此迭代器里的元素会逆序出现在队列里。
>>> dq
deque([40, 30, 20, 10, 3, 4, 5, 6, 7, 8], maxlen=10)
"""

# dequeue从队列中间删除元素的操作会慢一些，因为它只对在头尾的操作进行了优化。append 和 popleft 都是原子操作，也就说是 deque 可以在多线程程序中
# 安全地当作先进先出的栈使用，而使用者不需要担心资源锁的问题。

# queue
# 提供了同步（线程安全）类 Queue、LifoQueue 和 PriorityQueue，不同的线程可以利用这些数据类型来交换信息。这三个类的构造方法都有一个可选参数
# maxsize，它接收正整数作为输入值，用来限定队列的大小。但是在满员的时候，这些类不会扔掉旧的元素来腾出位置。相反，如果队列满了，它就会被锁住，直到另
# 外的线程移除了某个元素而腾出了位置。这一特性让这些类很适合用来控制活跃线程的数量。

# asyncio
# Python 3.4 新提供的包，里面有 Queue、LifoQueue、PriorityQueue 和JoinableQueue，这些类受到 queue 和 multiprocessing 模块的影响，
# 但是为异步编程里的任务管理提供了专门的便利。

# heapq
# 跟上面三个模块不同的是，heapq 没有队列类，而是提供了 heappush 和 heappop方法，让用户可以把可变序列当作堆队列或者优先队列来使用。


### 小结
# Python 序列类型最常见的分类就是可变和不可变序列。但另外一种分类方式也很有用，那就是把它们分为扁平序列和容器序列。前者的体积更小、速度更快而且用起
# 来更简单，但是它只能保存一些原子性的数据
# 新引入的 * 句法让元组拆包的便利性更上一层楼，让用户可以选择性忽略不需要的字段。

# 扁平序列和容器序列
# 为了解释不同序列类型里不同的内存模型，我用了容器序列和扁平序列这两个说法。其中“容器”一词来自“Data Model”文档
# （https://docs.python.org/3/reference/datamodel.html#objects-values-and-types）
# 有些对象里包含对其他对象的引用；这些对象称为容器。

# 混合类型列表
# python 入门教材往往会强调列表是可以同时容纳不同类型的元素的，但是实际上这样做并没有什么特别的好处。我们之所以用列表来存放东西，是期待在稍后使用它
# 的时候，其中的元素有一些通用的特性（比如，列表里存的是一类可以“呱呱”叫的动物，那么所有的元素都应该会发出这种叫声，即便其中一部分元素类型并不是鸭子）
# 元组则恰恰相反，它经常用来存放不同类型的的元素。这也符合它的本质，元组就是用作存放彼此之间没有关系的数据的记录。

# sorted 和 list.sort 背后的排序算法是 Timsort，它是一种自适应算法，会根据原始数据的顺序特点交替使用插入排序和归并排序，以达到最佳效率。这样的
# 算法被证明是很有效的，因为来自真实世界的数据通常是有一定的顺序特点的。维基百科上有一个条目是关于这个算法的（https://en.wikipedia.org/wiki/
# Timsort）。


if __name__ == '__main__':
    import doctest
    doctest.testmod()
