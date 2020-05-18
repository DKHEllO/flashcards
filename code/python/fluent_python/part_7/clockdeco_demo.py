#!/usr/bin/env python

import time
import functools


def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked # 返回内部函数，取代被装饰的函数

# 上述的装饰器存在一些缺陷：不支持关键字参数，而且遮盖了被装饰函数的 __name__ 和 __doc__ 属性。使用 functools.wraps 装饰器把相关的
# 属性从 func 复制到 clocked 中。


def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(', '.join(pairs))
        arg_str = ', '.join(arg_lst)
        print('[%0.8fs] %s(%s) -> %r ' % (elapsed, name, arg_str, result))
        return result
    return clocked


@clock
def snooze(seconds):
    time.sleep(seconds)


@clock
def factorial(n):
    return 1 if n < 2 else n*factorial(n-1)


@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)


print(fibonacci(6))


# 使用缓存实现
@functools.lru_cache() # 必须像常规函数那样调用 lru_cache。这一行中有一对括号：@functools.lru_cache()。这么做的原因是，lru_cache 可以接受配置参数，稍后说明。
@clock # 这里叠放了装饰器：@lru_cache() 应用到 @clock 返回的函数上
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)


print(fibonacci(6))

# 在计算 fibonacci(30) 的另一个测试中,做缓存的函数在 0.0005 秒内调用了 31 次fibonacci 函数，未缓存的版本调用 fibonacci 函数 2 692 537次
# ，在使用 Intel Core i7 处理器的笔记本电脑中耗时 17.7 秒。

# if __name__ == '__main__':
#     print('*' * 40, 'Calling snooze(.123)')
#     snooze(.123)
#     print('*' * 40, 'Calling factorial(6)')
#     print('6! =', factorial(6))


# 参数化clock装饰器
DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'


def clock(fmt=DEFAULT_FMT):
    def decorate(func):
        def clocked(*_args):
            t0 = time.time()
            _result = func(*_args)
            elapsed = time.time() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)
            result = repr(_result)
            print(fmt.format(**locals()))
            return _result
        return clocked
    return decorate


@clock()
def snooze(seconds):
    time.sleep(seconds)


for i in range(3):
    snooze(.123)


@clock('{name}: {elapsed}s')
def snooze(seconds):
    time.sleep(seconds)


for i in range(3):
    snooze(.123)


@clock('{name}({args}) dt={elapsed:0.3f}s')
def snooze(seconds):
    time.sleep(seconds)


for i in range(3):
    snooze(.123)