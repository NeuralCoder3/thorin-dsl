import os
import sys
import shutil
import tempfile
from ctypes import *


@CFUNCTYPE(c_int, c_int)
def bar(x):
    return x + 35


code = """
//extern int bar(int);
typedef int (*bar_type)(int);
bar_type bar;
void init(bar_type bar_) { bar = bar_; }


int foo(int x) { return bar(x + 2); }
int square(int x) { return x * x; }
"""

temp_code = tempfile.mktemp(".c")
temp_so = tempfile.mktemp(".so")

with open(temp_code, "w") as f:
    f.write(code)

os.system("cc -fPIC -shared -o %s %s" % (temp_so, temp_code))

lib = CDLL(temp_so)
lib.init(bar)

print(lib.foo(5))

# temp_ll = tempfile.mktemp(".ll")
# os.system("clang -S -emit-llvm -o %s %s" % (temp_ll, temp_code))
