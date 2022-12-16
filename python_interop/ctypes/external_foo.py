
from ctypes import *


@CFUNCTYPE(c_int, c_int)
def bar(x):
    return x + 40


# cc -fPIC -shared -o foo2.so foo2.c
foo = CDLL("./foo2.so")

foo.init(bar)
print(foo.foo(5))
