
from ctypes import *


def bar(x):
    return x + 40


bar_type = CFUNCTYPE(c_int, c_int)
bar_callback = bar_type(bar)


@CFUNCTYPE(c_int, c_int)
def bar2(x):
    return x + 40


# cc -fPIC -shared -o foo.so foo.c
foo = CDLL("./foo.so")

# print(foo.foo(5))
print(foo.foo2(5, bar_callback))
print(foo.foo2(5, bar2))
