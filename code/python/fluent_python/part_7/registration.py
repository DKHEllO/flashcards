#!/usr/bin/env python

# 如果导入 registration.py 模块（不作为脚本运行），输出如下：
"""
>>> import registration
running register(<function f1 at 0x10063b1e0>)
running register(<function f2 at 0x10063b268>)
"""
# 此时查看 registry 的值，得到的输出如下：
"""
>>> registration.registry
[<function f1 at 0x10063b1e0>, <function f2 at 0x10063b268>]
"""

registry = []


def register(func):
    print('running register(%s)' % func)
    registry.append(func)
    return func


@register
def f1():
    print('running f1()')


@register
def f2():
    print('running f2()')


def f3():
    print('running f3()')


def main():
    print('running main()')
    print('registry ->', registry)
    f1()
    f2()
    f3()

# 参数化装饰器

# registry 现在是一个 set 对象，这样添加和删除函数的速度更快。
registry = set()


def register(active=True):
    def decorate(func):  # decorate 这个内部函数是真正的装饰器；注意，它的参数是一个函数。
        print('running register(active=%s)->decorate(%s)' % (active, func))
        if active:
            registry.add(func)
        else:
            registry.discard(func)
        return func
    return decorate


@register(active=False)
def f1():
    print('running f1()')


@register()
def f2():
    print('running f2()')


def f3():
    print('running f3()')


if __name__=='__main__':
    main()


