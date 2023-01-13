import python_function_interface as interface
from ctypes import *


def bar(x):
    return x + 35


code = """
int foo(int x) { return bar(x + 2); }
int square(int x) { return x * x; }
"""

preamble, c_functions = interface.prepare_function([(bar, c_int, [c_int])])
thorin = interface.compile(preamble+code, c_functions)

print(thorin.square(4))
print(thorin.foo(5))
