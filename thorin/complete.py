import python_function_interface as interface
from ctypes import *


def bar(x):
    return x + 35


code = """
.con .extern square [mem: %mem.M, a: I32, return : .Cn [%mem.M, I32]] = {
    .let b = %core.wrap.mul _32 0 (a, a);
    return (mem, b)
};

.con .extern foo [mem: %mem.M, a: I32, return : .Cn [%mem.M, I32]] = {
    .let b = %core.wrap.add _32 0 (a, 2:I32);
    bar (mem, b, return)
};
"""

preamble, thorin_preamble, c_functions = interface.prepare_function(
    [(bar, c_int, [c_int])])
thorin = interface.compile(
    preamble, thorin_preamble+code, c_functions, verbose=True)

print(thorin.square(4))
print(thorin.foo(5))
