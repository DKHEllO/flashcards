#!/usr/bin/env python
from unicodedata import normalize
import string
import unicodedata
import re

# 文本和字节序列
# Python 3 明确区分了人类可读的文本字符串和原始的字节序列。隐式地把字节序列转换成Unicode 文本已成过去。本章将要讨论 Unicode 字符串、二进制序列，
# 以及在二者之间转换时使用的编码。

#---------------------
# 字符问题
# 从 Python 3 的 str 对象中获取的元素是 Unicode 字符，这相当于从 Python 2 的 unicode 对象中获取的元素，而不是从Python 2 的 str 对象中获
# 取的原始字节序列。
# Unicode 标准把字符的标识和具体的字节表述进行了如下的明确区分:
# - 字符的标识，即码位，是 0~1 114 111 的数字（十进制），在 Unicode 标准中以 4~6个十六进制数字表示，而且加前缀“U+”。例如，字母 A 的码位是
# U+0041，欧元符号的码位是 U+20AC，高音谱号的码位是 U+1D11E。
# - 字符的具体表述取决于所用的编码。编码是在码位和字节序列之间转换时使用的算法。在 UTF-8 编码中，A（U+0041）的码位编码成单个字节 \x41，而在 UTF
# -16LE编码中编码成两个字节 \x41\x00。再举个例子，欧元符号（U+20AC）在 UTF-8 编码中是三个字节——\xe2\x82\xac，而在 UTF-16LE 中编码成两个字
# 节：\xac\x20。

# 非常重要！！！！
# 把码位转换成字节序列的过程是编码；把字节序列转换成码位的过程是解码。
"""
>>> s = 'café'
>>> len(s) 
4 >>> b
=
s.encode('utf8') 
>>> b
b'caf\xc3\xa9' # 前 3 个字节 b'caf' 在可打印的ASCII 范围内，后两个字节则不然。
>>> len(b) 
5 >>> b.decode('utf8') 
'café
"""

# -------------------
# 字节概要
# Python 内置了两种基本的二进制序列类型：Python 3 引入的不可变 bytes 类型和 Python 2.6 添加的可变bytearray 类型。
# bytes 或 bytearray 对象的各个元素是介于 0~255（含）之间的整数，而不像 Python 2的 str 对象那样是单个的字符。然而，二进制序列的切片始终是同一
# 类型的二进制序列，包括长度为 1 的切片
"""
>>> cafe = bytes('café', encoding='utf_8') 
>>> cafe
b'caf\xc3\xa9'
>>> cafe[0] 
99
>>> cafe[:1] 
b'c'
>>> cafe_arr = bytearray(cafe)
>>> cafe_arr 
bytearray(b'caf\xc3\xa9')
>>> cafe_arr[-1:] 
bytearray(b'\xa9')
"""

# 非常重要！！！！！、
# my_bytes[0] 获取的是一个整数，而 my_bytes[:1] 返回的是一个长度为 1的 bytes 对象——这一点应该不会让人意外。s[0] == s[:1] 只对 str 这个序
# 列类型成立。不过，str 类型的这个行为十分罕见。对其他各个序列类型来说，s[i] 返回一个元素，而 s[i:i+1] 返回一个相同类型的序列，里面是 s[i] 元素。

# 各个字节的值可能会使用下列三种不同的方式显示：
# - 可打印的 ASCII 范围内的字节（从空格到 ~），使用 ASCII 字符本身。
# - 制表符、换行符、回车符和 \ 对应的字节，使用转义序列 \t、\n、\r 和 \\。
# - 其他字节的值，使用十六进制转义序列（例如，\x00 是空字节）。

# 如果正则表达式编译自二进制序列而不是字符串，re 模块中的正则表达式函数也能处理二进制序列.二进制序列有个类方法是 str 没有的，名为 fromhex，它的作
# 用是解析十六进制数字对（数字对之间的空格是可选的），构建二进制序列：
"""
>>> bytes.fromhex('31 4B CE A9')
b'1K\xce\xa9'
"""

# 构建 bytes 或 bytearray 实例还可以调用各自的构造方法，传入下述参数。
# - 一个 str 对象和一个 encoding 关键字参数。
# - 一个可迭代对象，提供 0~255 之间的数值。
# - 一个整数，使用空字节创建对应长度的二进制序列。
# - 一个实现了缓冲协议的对象（如bytes、bytearray、memoryview、array.array）；此时，把源对象中的字节序列复制到新建的二进制序列中。
"""
>>> import array
>>> numbers = array.array('h', [-2, -1, 0, 1, 2]) 
>>> octets = bytes(numbers) 
>>> octets
b'\xfe\xff\xff\xff\x00\x00\x01\x00\x02\x00' 
"""
# 使用缓冲类对象创建 bytes 或 bytearray 对象时，始终复制源对象中的字节序列。与之相反，memoryview 对象允许在二进制数据结构之间共享内存。如果想从
# 二进制序列中提取结构化信息，struct 模块是重要的工具。


# ---------------
# 结构体和内存视图
# struct 模块提供了一些函数，把打包的字节序列转换成不同类型字段组成的元组，还有一些函数用于执行反向转换，把元组转换成打包的字节序列。struct 模块能
# 处理bytes、bytearray 和 memoryview 对象。
# memoryview 类不是用于创建或存储字节序列的，而是共享内存，让你访问其他二进制序列、打包的数组和缓冲中的数据切片，而无需复制字节序列，例如
# Python Imaging Library（PIL） 就是这样处理图像的
"""
使用 memoryview 和 struct 查看一个 GIF 图像的首部
>>> import struct
>>> fmt = '<3s3sHH' # 结构体的格式：< 是小字节序，3s3s 是两个 3 字节序列，HH 是两个 16 位二进制整数。 
>>> with open('filter.gif', 'rb') as fp:
...     img = memoryview(fp.read()) # 使用内存中的文件内容创建一个 memoryview 对象
...
>>> header = img[:10] # 再创建一个 memoryview 对象；这里不会复制字节序列。
>>> bytes(header) # 
b'GIF89a+\x02\xe6\x00'
>>> struct.unpack(fmt, header) # 拆包 memoryview 对象，得到一个元组，包含类型、版本、宽度和高度。
(b'GIF', b'89a', 555, 230)
>>> del header # 删除引用，释放 memoryview 实例所占的内存。
>>> del img
"""
# 注意！！！
# memoryview 对象的切片是一个新 memoryview 对象，而且不会复制字节序列。


# --------------
# 基本的编解码器
# Python 自带了超过 100 种编解码器（codec, encoder/decoder），用于在文本和字节之间相互转换。
"""
>>> for codec in ['latin_1', 'utf_8', 'utf_16']:
...     print(codec, 'El Niño'.encode(codec), sep='\t')
...
latin_1 b'El Ni\xf1o'
utf_8 b'El Ni\xc3\xb1o'
utf_16 b'\xff\xfeE\x00l\x00 \x00N\x00i\x00\xf1\x00o\x00'
"""
# 编解码问题
# 虽然有个一般性的 UnicodeError 异常，但是报告错误时几乎都会指明具体的异常：UnicodeEncodeError（把字符串转换成二进制序列时）或
# UnicodeDecodeError（把二进制序列转换成字符串时）。如果源码的编码与预期不符，加载 Python 模块时还可能抛出 SyntaxError。
# - 处理UnicodeEncodeError:多数非 UTF 编解码器只能处理 Unicode 字符的一小部分子集。把文本转换成字节序列时，如果目标编码中没有定义某个字符，
# 那就会抛出 UnicodeEncodeError 异常，除非把 errors 参数传给编码方法或函数，对错误进行特殊处理。
"""
编码成字节序列：成功和错误处理
>>> city = 'São Paulo'
>>> city.encode('utf_8') 
b'S\xc3\xa3o Paulo'
>>> city.encode('utf_16')
b'\xff\xfeS\x00\xe3\x00o\x00 \x00P\x00a\x00u\x00l\x00o\x00'
>>> city.encode('iso8859_1') 
b'S\xe3o Paulo'
>>> city.encode('cp437') # 'cp437' 无法编码 'ã'（带波形符的“a”）。默认的错误处理方式 'strict' 抛出UnicodeEncodeError。
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
File "/.../lib/python3.4/encodings/cp437.py", line 12, in encode
return codecs.charmap_encode(input,errors,encoding_map)
UnicodeEncodeError: 'charmap' codec can't encode character '\xe3' in
position 1: character maps to <undefined>
>>> city.encode('cp437', errors='ignore') 
b'So Paulo'
>>> city.encode('cp437', errors='replace') # 编码时指定 error='replace'，把无法编码的字符替换成 '?'；数据损坏了，但是用户知道出了问题。
b'S?o Paulo'
>>> city.encode('cp437', errors='xmlcharrefreplace') # 'xmlcharrefreplace' 把无法编码的字符替换成 XML 实体。
b'São Paulo'
"""
# 编解码器的错误处理方式是可扩展的。你可以为 errors 参数注册额外的字符串，方法是把一个名称和一个错误处理函数传给 codecs.register_error 函数。
# 参见 codecs.register_error 函数的文档（https://docs.python.org/3/library/codecs.html#codecs.register_error）。

# - 处理UnicodeDecodeError:不是每一个字节都包含有效的 ASCII 字符，也不是每一个字符序列都是有效的 UTF-8 或 UTF-16。因此，把二进制序列转换成
# 文本时，如果假设是这两个编码中的一个，遇到无法转换的字节序列时会抛出 UnicodeDecodeError。
"""
把字节序列解码成字符串：成功和错误处理
>>> octets = b'Montr\xe9al' 
>>> octets.decode('cp1252') 
'Montréal'
>>> octets.decode('iso8859_7') # ISO-8859-7 用于编码希腊文，因此无法正确解释 '\xe9' 字节，而且没有抛出错误。
'Montrιal'
>>> octets.decode('koi8_r') # ISO-8859-7 用于编码希腊文，因此无法正确解释 '\xe9' 字节，而且没有抛出错误。
'MontrИal'
>>> octets.decode('utf_8') # 'utf_8' 编解码器检测到 octets 不是有效的 UTF-8 字符串，抛出UnicodeDecodeError。
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 5:
invalid continuation byte
>>> octets.decode('utf_8', errors='replace') # 使用 'replace' 错误处理方式，\xe9 替换成了“ ”（码位是 U+FFFD），这是官方指定的 
REPLACEMENT CHARACTER（替换字符），表示未知字符。
'Montral'
"""

# - 使用预期之外的编码加载模块时抛出的SyntaxError:Python 3 默认使用 UTF-8 编码源码，Python 2（从 2.5 开始）则默认使用 ASCII。如果加载
# 的 .py 模块中包含 UTF-8 之外的数据，而且没有声明编码，会得到类似下面的
"""
SyntaxError: Non-UTF-8 code starting with '\xe1' in file ola.py on line
1, but no encoding declared; see http://python.org/dev/peps/pep-0263/
for details
"""
# GNU/Linux 和 OS X 系统大都使用 UTF-8，因此打开在 Windows 系统中使用 cp1252 编码的 .py 文件时可能发生这种情况。注意，这个错误在 Windows
# 版 Python 中也可能会发生，因为 Python 3 为所有平台设置的默认编码都是 UTF-8。为了修正这个问题，可以在文件顶部添加一个神奇的 coding 注释
"""
# coding: cp1252
print('Olá, Mundo!')
"""
# 源码应该便于目标群体阅读和编辑，而不是“所有人”。如果代码属于跨国公司，或者是开源的，想让来自世界各地的人作贡献，那么标识符应该使用英语，也就是说只
# 能使用 ASCII 字符。
# 但是，如果你是巴西的一位老师，那么使用葡萄牙语正确拼写变量和函数名更便于学生阅读代码。而且，这些学生在本地化的键盘中不难打出变音符号和重音元音字母。

# 处理文本文件
# 处理文本的最佳实践是“Unicode 三明治”（如图 4-2 所示）。 意思是，要尽早把输入（例如读取文件时）的字节序列解码成字符串。这种三明治中的“肉片”是程
# 序的业务逻辑，在这里只能处理字符串对象。在其他处理过程中，一定不能编码或解码。对输出来说，则要尽量晚地把字符串编码成字节序列。
# 需要在多台设备中或多种场合下运行的代码，一定不能依赖默认编码。打开文件时始终应该明确传入 encoding= 参数，因为不同的设备使用的默认编码可能不同，有
# 时隔一天也会发生变化。
# 如果打开文件时没有指定 encoding 参数，默认值由locale.getpreferredencoding() 提供

# 重要！！！
# 关于编码默认值的最佳建议是：别依赖默认值。

# -----------------
# 为了正确比较而规范化Unicode字符串
# 因为 Unicode 有组合字符（变音符号和附加到前一个字符上的记号，打印时作为一个整体），所以字符串比较起来很复杂。
"""
>>> s1 = 'café'
>>> s2 = 'cafe\u0301'
>>> s1, s2
('café', 'café')
>>> len(s1), len(s2)
(4, 5)
>>> s1 == s2
False
"""
# U+0301 是 COMBINING ACUTE ACCENT，加在“e”后面得到“é”。在 Unicode 标准中，'é'和 'e\u0301' 这样的序列叫“标准等价物”（canonical
# equivalent），应用程序应该把它们视作相同的字符。但是，Python 看到的是不同的码位序列，因此判定二者不相等。

# NFC（Normalization Form C）使用最少的码位构成等价的字符串，而 NFD 把组合字符分解成基字符和单独的组合字符。这两种规范化方式都能让比较行为符合
# 预期：
"""
>>> from unicodedata import normalize
>>> s1 = 'café' # 把"e"和重音符组合在一起
>>> s2 = 'cafe\u0301' # 分解成"e"和重音符
>>> len(s1), len(s2)
(4, 5)
>>> len(normalize('NFC', s1)), len(normalize('NFC', s2))
(4, 4)
>>> len(normalize('NFD', s1)), len(normalize('NFD', s2))
(5, 5)
>>> normalize('NFC', s1) == normalize('NFC', s2)
True
>>> normalize('NFD', s1) == normalize('NFD', s2)
True
"""
# 西方键盘通常能输出组合字符，因此用户输入的文本默认是 NFC 形式。不过，安全起见，保存文本之前，最好使用 normalize('NFC', user_text) 清洗字符
# 串。

# 使用 NFC 时，有些单字符会被规范成另一个单字符。例如，电阻的单位欧姆（Ω）会被规范成希腊字母大写的欧米加。这两个字符在视觉上是一样的，但是比较时并不
# 相等.
"""
>>> from unicodedata import normalize, name
>>> ohm = '\u2126'
>>> name(ohm)
'OHM SIGN'
>>> ohm_c = normalize('NFC', ohm)
>>> name(ohm_c)
'GREEK CAPITAL LETTER OMEGA'
>>> ohm == ohm_c
False
>>> normalize('NFC', ohm) == normalize('NFC', ohm_c)
True
"""

# 大小写折叠
# 大小写折叠其实就是把所有文本变成小写，再做些其他转换。这个功能由str.casefold() 方法（Python 3.3 新增）支持。

# 规范化文本匹配实用函数
# 不区分大小写的比较应该使用 str.casefold()。如果要处理多语言文本，工具箱中应该有示例 4-13 中的 nfc_equal 和 fold_equal 函
# 数。
"""
Utility functions for normalized Unicode string comparison.
Using Normal Form C, case sensitive:
>>> s1 = 'café'
>>> s2 = 'cafe\u0301'
>>> s1 == s2
False
>>> nfc_equal(s1, s2)
True
>>> nfc_equal('A', 'a')
False
Using Normal Form C with case folding:
>>> s3 = 'Straße'
>>> s4 = 'strasse'
>>> s3 == s4
False
>>> nfc_equal(s3, s4)
False
>>> fold_equal(s3, s4)
True
>>> fold_equal(s1, s2)
True
>>> fold_equal('A', 'a')
True
"""


def nfc_equal(str1, str2):
    return normalize('NFC', str1) == normalize('NFC', str2)


def fold_equal(str1, str2):
    return normalize('NFC', str1).casefold() == normalize('NFC', str2).casefold()


# 极端“规范化”：去掉变音符号
# 去掉变音符号不是正确的规范化方式，因为这往往会改变词的意思，而且可能误判搜索结果。但是对现实生活却有所帮助：人们有时很懒，或者不知道怎么正确使用变音
# 符号，而且拼写规则会随时间变化，因此实际语言中的重音经常变来变去。
"""
http://en.wikipedia.org/wiki/S%C3%A3o_Paulo
http://en.wikipedia.org/wiki/Sao_Paulo
"""
# 如果想把字符串中的所有变音符号都去掉，可以使用示例 4-14 中的函数。


def shave_marks(txt):
    """
    去掉全部变音符号
    >>> order = '“Herr Voß: • ½ cup of OEtker™ caffè latte • bowl of açaí.”'
    >>> shave_marks(order)
    '“Herr Voß: • ½ cup of OEtker™ caffe latte • bowl of acai.”'
    >>> Greek = 'Zέφupoς, Zéfiro'
    >>> shave_marks(Greek)
    'Ζεφupoς, Zefiro'
    """
    # 把所有字符分解成基字符和组合记号
    norm_txt = unicodedata.normalize('NFD', txt)
    # 过滤掉所有组合记号。
    shaved = ''.join(c for c in norm_txt if not unicodedata.combining(c))
    return unicodedata.normalize('NFC', shaved)


# 通常，去掉变音符号是为了把拉丁文本变成纯粹的 ASCII，但是 shave_marks 函数还会修改非拉丁字符（如希腊字母），而只去掉重音符并不能把它们变成
# ASCII 字符。因此，我们应该分析各个基字符，仅当字符在拉丁字母表中时才删除附加的记号
def shave_marks_latin(txt):
    """把拉丁基字符中所有的变音符号删除"""
    norm_txt = unicodedata.normalize('NFD', txt)
    latin_base = False
    keepers = []
    for c in norm_txt:
        if unicodedata.combining(c) and latin_base:
            continue  # 忽略拉丁基字符上的变音符号
        keepers.append(c)
        # 如果不是组合字符，那就是新的基字符
        if not unicodedata.combining(c):
            latin_base = c in string.ascii_letters
    shaved = ''.join(keepers)
    return unicodedata.normalize('NFC', shaved)

# 更彻底的规范化步骤是把西文文本中的常见符号（如弯引号、长破折号、项目符号，等等）替换成 ASCII 中的对等字符。示例 4-17 中的 asciize 函数就是这么
# 做的

# 可以避免代码或文本中出现中文字符，做中文字符校验


single_map = str.maketrans(""",ƒ,,†ˆ‹‘’“”•––˜›""", """'f''*^<''""---~>""")
multi_map = str.maketrans({
            '€': '<euro>',
            '…': '...',
            'O': 'O',
            'E': 'E',
            '™': '(TM)',
            'o': 'o',
            'e': 'e',
            '‰': '<per mille>',
            '‡': '**',
            })
multi_map.update(single_map)



def dewinize(txt):
    """把Win1252符号替换成ASCII字符或序列"""
    return txt.translate(multi_map)


def asciize(txt):
    no_marks = shave_marks_latin(dewinize(txt))
    no_marks = no_marks.replace('ß', 'ss')
    return unicodedata.normalize('NFKC', no_marks)

"""
>>> order = '“Herr Voß: • ½ cup of OEtker™ caffè latte • bowl of açaí.”'
>>> dewinize(order)
'"Herr Voß: - ½ cup of OEtker(TM) caffè latte - bowl of açaí."' 
>>> asciize(order)
'"Herr Voss: - 1⁄2 cup of OEtker(TM) caffe latte - bowl of acai."' 
"""


# Unicode文本排序
# Python 比较任何类型的序列时，会一一比较序列里的各个元素。对字符串来说，比较的是码位。可是在比较非 ASCII 字符时，得到的结果不尽如人意。
"""
>>> fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
>>> sorted(fruits)
['acerola', 'atemoia', 'açaí', 'caju', 'cajá']
"""
# 不同的区域采用的排序规则有所不同，葡萄牙语等很多语言按照拉丁字母表排序，重音符号和下加符对排序几乎没什么影响。 因此，排序时“cajá”视作“caja”，必定
# 排在“caju”前面。
# 排序后的 fruits 列表应该是：
"""
['açaí', 'acerola', 'atemoia', 'cajá', 'caju']
"""
# 使用 locale.strxfrm 函数之前，必须先为应用设定合适的区域设置，还要祈祷操作系统支持这项设置。在区域设为 pt_BR 的 GNU/Linux
"""
>>> import locale
>>> locale.setlocale(locale.LC_COLLATE, 'pt_BR.UTF-8')
'pt_BR.UTF-8'
>>> fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
>>> sorted_fruits = sorted(fruits, key=locale.strxfrm)
>>> sorted_fruits
['açaí', 'acerola', 'atemoia', 'cajá', 'caju']
"""
# 因此，使用 locale.strxfrm 函数做排序键之前，要调用 setlocale(LC_COLLATE,«your_locale»)。不过，有几点要注意。
# - 区域设置是全局的，因此不推荐在库中调用 setlocale 函数。应用或框架应该在进程启动时设定区域设置，而且此后不要再修改。
# - 操作系统必须支持区域设置，否则 setlocale 函数会抛出 locale.Error:unsupported locale setting 异常。
# - 必须知道如何拼写区域名称。它在 Unix 衍生系统中几乎已经形成标准，要通过'language_code.encoding' 获取。 但是在 Windows 中，句法复杂一些：
# Language Name-Language Variant_Region Name.codepage。注意，“Language Name”（语言名称）、“Language Variant”（语言变体）和
# “RegionName”（区域名）中可以包含空格；除了第一部分之外，其他部分的前面是不同的字符：一个连字符、一个下划线和一个点号。除了语言名称之外，其他部分
# 好像都是可选的。
# - 操作系统的制作者必须正确实现了所设的区域。我在 Ubuntu 14.04 中成功了，但在 OS X（Mavericks 10.9）中却失败了。在两台 Mac 中，调用
# setlocale(LC_COLLATE, 'pt_BR.UTF-8') 返回的都是字符串 'pt_BR.UTF-8'，没有任何问题。但是，sorted(fruits, key=locale.strxfrm)
# 得到的结果与sorted(fruits) 一样，是错误的。我还在 OS X 中尝试了 fr_FR、es_ES 和de_DE，但是 locale.strxfrm 并未起作用。

# 因此，标准库提供的国际化排序方案可用，但是似乎只支持 GNU/Linux（可能也支持Windows，但你得是专家）。即便如此，还要依赖区域设置，而这会为部署带来问题。
# 幸好，有个较为简单的方案：PyPI 中的 PyUCA 库。

# 使用Unicode排序算法排序
# PyUCA 库（https://pypi.python.org/pypi/pyuca/），这是 Unicode 排序算法（UnicodeCollation Algorithm，UCA）的纯 Python 实现
"""
>>> import pyuca
>>> coll = pyuca.Collator()
>>> fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
>>> sorted_fruits = sorted(fruits, key=coll.sort_key)
>>> sorted_fruits
['açaí', 'acerola', 'atemoia', 'cajá', 'caju']
"""
# PyUCA 没有考虑区域设置。如果想定制排序方式，可以把自定义的排序表路径传给Collator() 构造方法。

# ---------------------
# Unicode数据库
# Unicode 标准提供了一个完整的数据库（许多格式化的文本文件），不仅包括码位与字符名称之间的映射，还有各个字符的元数据，以及字符之间的关系。例如，
# Unicode 数据库记录了字符是否可以打印、是不是字母、是不是数字，或者是不是其他数值符号。字符串的 isidentifier、isprintable、isdecimal 和
# isnumeric 等方法就是靠这些信息作判断的。 str.casefold 方法也用到了 Unicode 表中的信息。
# unicodedata 模块中有几个函数用于获取字符的元数据。例如，字符在标准中的官方名称是不是组合字符（如结合波形符构成的变音符号等），以及符号对应的人类
# 可读数值（不是码位）。


re_digit = re.compile(r'\d')
sample = '1\xbc\xb2\u0969\u136b\u216b\u2466\u2480\u3285'
for char in sample:
    print('U+%04x' % ord(char),  # U+0000 格式的码位
          char.center(6),  # 在长度为 6 的字符串中居中显示字符。
          're_dig' if re_digit.match(char) else '-',  # 如果字符匹配正则表达式 r'\d'，显示 re_dig
          'isdig' if char.isdigit() else '-',  # 如果 char.isdigit() 返回 True，显示 isdig
          'isnum' if char.isnumeric() else '-',  # 如果 char.isnumeric() 返回 True，显示 isnum
          format(unicodedata.numeric(char), '5.2f'),  # 使用长度为 5、小数点后保留 2 位的浮点数显示数值
          unicodedata.name(char),  # Unicode 标准中字符的名称
          sep='\t')

# 正则表达式 r'\d' 能匹配数字“1”和梵文数字 3，但是不能匹配 isdigit 方法判断为数字的其他字符。re 模块对 Unicode 的支持并不充分。PyPI 中有个新
# 开发的regex 模块，它的最终目的是取代 re 模块，以提供更好的 Unicode 支持。 下一节会回过头来讨论 re 模块。

# --------------------------
# 支持字符串和字节序列的双模式API
# 标准库中的一些函数能接受字符串或字节序列为参数，然后根据类型展现不同的行为。re 和 os 模块中就有这样的函数。
# 正则表达式中的字符串和字节序列
# 如果使用字节序列构建正则表达式，\d 和 \w 等模式只能匹配 ASCII 字符；相比之下，如果是字符串模式，就能匹配 ASCII 之外的 Unicode 数字或字母。
# 示例 4-22 和图 4-4 展示了字符串模式和字节序列模式中字母、ASCII 数字、上标和泰米尔数字的匹配情况。
import re

re_numbers_str = re.compile(r'\d+')  # 前两个正则表达式是字符串类型
re_words_str = re.compile(r'\w+')
re_numbers_bytes = re.compile(rb'\d+')  # 后两个正则表达式是字节序列类型
re_words_bytes = re.compile(rb'\w+')

text_str = ("Ramanujan saw \u0be7\u0bed\u0be8\u0bef"  # 要搜索的 Unicode 文本，包括 1729 的泰米尔数字
            " as 1729 = 1³ + 12³ = 9³ + 10³.")
text_bytes = text_str.encode('utf_8')  # 字节序列只能用字节序列正则表达式搜索。

print('Text', repr(text_str), sep='\n ')
print('Numbers')
print(' str :', re_numbers_str.findall(text_str))  # 字符串模式 r'\d+' 能匹配泰米尔数字和 ASCII 数字
print(' bytes:', re_numbers_bytes.findall(text_bytes))  # 字节序列模式 rb'\d+' 只能匹配 ASCII 字节中的数字
print('Words')
print(' str :', re_words_str.findall(text_str))  # 字符串模式 r'\w+' 能匹配字母、上标、泰米尔数字和 ASCII 数字。
print(' bytes:', re_words_bytes.findall(text_bytes))  # 字节序列模式 rb'\w+' 只能匹配 ASCII 字节中的字母和数字。

# 注意！！！
# 可以使用正则表达式搜索字符串和字节序列，但是在后一种情况中，ASCII 范围外的字节不会当成数字和组成单词的字母。
# 字符串正则表达式有个 re.ASCII 标志，它让 \w、\W、\b、\B、\d、\D、\s 和 \S 只匹配 ASCII 字符

# -----------------
# os函数中的字符串和字节序列
# GNU/Linux 内核不理解 Unicode，因此你可能发现了，对任何合理的编码方案来说，在文件名中使用字节序列都是无效的，无法解码成字符串。
# 为了规避这个问题，os 模块中的所有函数、文件名或路径名参数既能使用字符串，也能使用字节序列。如果这样的函数使用字符串参数调用，该参数会使用
# sys.getfilesystemencoding() 得到的编解码器自动编码，然后操作系统会使用相同的编解码器解码。这几乎就是我们想要的行为，与 Unicode 三明治最佳实
# 践一致。
"""
把字符串和字节序列参数传给 listdir 函数得到的结果
>>> os.listdir('.') 
['abc.txt', 'digits-of-π.txt']
>>> os.listdir(b'.') 
[b'abc.txt', b'digits-of-\xcf\x80.txt']
"""
# 为了便于手动处理字符串或字节序列形式的文件名或路径名，os 模块提供了特殊的编码和解码函数。
# - fsencode(filename):如果 filename 是 str 类型（此外还可能是 bytes 类型），使用sys.getfilesystemencoding() 返回的编解码器把
# filename 编码成字节序列；否则，返回未经修改的 filename 字节序列。
# - fsdecode(filename):如果 filename 是 bytes 类型（此外还可能是 str 类型），使用sys.getfilesystemencoding() 返回的编解码器把
# filename 解码成字符串；否则，返回未经修改的 filename 字符串。

# 在 Unix 衍生平台中，这些函数使用 surrogateescape 错误处理方式（参见下述附注栏）以避免遇到意外字节序列时卡住。Non-decodable Bytes in System
# Character Interfaces”（https://www.python.org/dev/peps/pep-0383/。这种错误处理方式会把每个无法解码的字节替换成 Unicode 中 U+DC00
# 到 U+DCFF 之间的码位（Unicode 标准把这些码位称为“Low Surrogate Area”），这些码位是保留的，没有分配字符，供应用程序内部使用
"""
使用 surrogateescape 错误处理方式
>>> os.listdir('.') 
['abc.txt', 'digits-of-π.txt']
>>> os.listdir(b'.') 
[b'abc.txt', b'digits-of-\xcf\x80.txt']
>>> pi_name_bytes = os.listdir(b'.')[1] 
>>> pi_name_str = pi_name_bytes.decode('ascii', 'surrogateescape') 
>>> pi_name_str 
'digits-of-\udccf\udc80.txt'
>>> pi_name_str.encode('ascii', 'surrogateescape') 
b'digits-of-\xcf\x80.txt
"""

# 总结
# - 随着 Unicode 的广泛使用（80% 的网站已经使用 UTF-8），我们必须把文本字符串与它们在文件中的二进制序列表述区分开，而 Python 3 中这个区分是强制的。
# - 如何避免和处理臭名昭著的 UnicodeEncodeError 和 UnicodeDecodeError，以及由于 Python 源码文件编码错误导致的 SyntaxError。
# - 了如何打开文本文件，这是一项简单的任务，不过有个陷阱：打开文本文件时，encoding= 关键字参数不是必需的，但是应该指定。如果没有指定编码，那么程
# 序会想方设法生成“纯文本”，如此一来，不一致的默认编码就会导致跨平台不兼容性。然后，我们说明了 Python 用作默认值的几个编码设置，以及如何检测它
# 们：locale.getpreferredencoding()、sys.getfilesystemencoding()、sys.getdefaultencoding()以及标准 I/O 文件
# （如 sys.stdout.encoding）的编码。对 Windows 用户来说，现实不容乐观：这些设置在同一台设备中往往有不同的值，而且各个设置相互不兼容。而对
# GNU/ Linux 和 OS X 用户来说，情况就好多了，几乎所有地方使用的默认值都是 UTF-8。
# - 文本比较是个异常复杂的任务，因为 Unicode 为某些字符提供了不同的表示，所以匹配文本之前一定要先规范化。说明规范化和大小写折叠之后，我们提供了几个
# 实用函数，你可以根据自己的需求改编。其中有个函数所做的是极端转换，比如去掉所有重音符号。随后，我们说明了如何使用标准库中的 locale 模块正确地排序
# Unicode 文本（有一些注意事项）；此外，还可以使用外部的 PyUCA 包，从而无需依赖捉摸不定的区域配置。
# - Unicode 数据库（包含每个字符的元数据），双模式API（例如 re 和 os 模块，这两个模块中的某些函数可以接受字符串或字节序列参数，返回不同但合适的
# 结果）。

# “纯文本”是什么
# 对于经常处理非英语文本的人来说，“纯文本”并不是指“ASCII”。Unicode 词汇表（http://www.unicode.org/glossary/#plain_text）是这样定义纯文
# 本的：
# 只由特定标准的码位序列组成的计算机编码文本，其中不含其他格式化或结构化信息。
# 这个定义的前半句说得很好，但是我不同意后半句。HTML 就是包含格式化和结构化。信息的纯文本格式，但它依然是纯文本，因为 HTML 文件中的每个字节都表示文本
# 字符（通常使用 UTF-8 编码），没有任何字节表示文本之外的信息。.png 或 .xsl 文档则不同，其中多数字节表示打包的二进制值，例如 RGB 值和浮点数。
# 在纯文本中，数字使用数字符号序列表示。

# 在 RAM 中如何表示字符串
# 理论上，怎么存储都没关系：不管内部表述如何，输出时每个字符串都要编码成字节序列。
# 在内存中，Python 3 使用固定数量的字节存储字符串的各个码位，以便高效访问各个字符或切片。
# 从 Python 3.3 起，创建 str 对象时，解释器会检查里面的字符，然后为该字符串选择最经济的内存布局：如果字符都在 latin1 字符集中，那就使用 1 个字
# 节存储每个码位；否则，根据字符串中的具体字符，选择 2 个或 4 个字节存储每个码位。这是简述，完整细节参阅
# “PEP 393—Flexible String Representation”（https://www.python.org/dev/peps/pep-0393/）。
# 灵活的字符串表述类似于 Python 3 对 int 类型的处理方式：如果一个整数在一个机器字中放得下，那就存储在一个机器字中；否则解释器切换成变长表述，类似于
# Python 2 中的 long 类型。这种聪明的做法得到推广，真是让人欢喜！


