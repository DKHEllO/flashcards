#!/usr/bin/env python

from collections import UserDict


class StrKeyDict0(dict):
    def __missing__(self, key):
        # 如果找不到的键本身就是字符串，那就抛出 KeyError 异常。
        if isinstance(key, str):
            raise KeyError(key)
        # 如果找不到的键不是字符串，转换成字符串再进行查找
        return self[str(key)]

    # get 方法把查找工作用 self[key] 的形式委托给 __getitem__，这样在宣布查找失败之前，还能通过 __missing__ 再给某个键一个机会。
    def get(self, k, default=None):
        try:
            return self[k]
        # 如果抛出 KeyError，那么说明 __missing__ 也失败了，于是返回 default。
        except KeyError:
            return default

    # 先按照传入键的原本的值来查找（我们的映射类型中可能含有非字符串的键），如果没找到，再用 str() 方法把键转换成字符串再查找一次。
    # __contains__ 里还有个细节，就是我们这里没有用更具 Python 风格的方式——k in my_dict——来检查键是否存在，因为那也会导致 __contains__
    # 被递归调用。为了避免这一情况，这里采取了更显式的方法，直接在这个 self.keys() 里查询。
    def __contains__(self, item):
        return item in self.keys() or str(item) in self.keys()

# 思考一个问题为什么 isinstance(key, str) 测试在上面的 __missing__ 中是必需的？


# 进阶版
class StrKeyDict1(UserDict):
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    # 这里可以放心假设所有已经存储的键都是字符串。因此，只要在 self.data 上查询就好了
    def __contains__(self, key):
        return str(key) in self.data

    # 会把所有的键都转换成字符串。由于把具体的实现委托给了 self.data属性，这个方法写起来也不难
    def __setitem__(self, key, item):
        self.data[str(key)] = item


# 因为 UserDict 继承的是 MutableMapping，所以 StrKeyDict 里剩下的那些映射类型的方法都是从 UserDict、MutableMapping 和 Mapping 这些超
# 类继承而来的。特别是最后的 Mapping 类，它虽然是一个抽象基类（ABC），但它却提供了好几个实用的方法。以下两个方法值得关注。
# - MutableMapping.update:这个方法不但可以为我们所直接利用，它还用在 __init__ 里，让构造方法可以利用传入的各种参数（其他映射类型、元素是
# (key, value) 对的可迭代对象和键值参数）来新建实例。因为这个方法在背后是用 self[key] = value 来添加新值的，所以它其实是在使用我们的 __seti
# tem__ 方法。
# - Mapping.get:在 StrKeyDict0（示例 3-7）中，我们不得不改写 get 方法，好让它的表现跟__getitem__ 一致。而在示例 3-8 中就没这个必要了，因
# 为它继承了 Mapping.get 方法，而 Python 的源码（https://hg.python.org/cpython/file/3.4/Lib/_collections_abc.py#l422）显示，这个
# 方法的实现方式跟 StrKeyDict0.get 是一模一样的。
