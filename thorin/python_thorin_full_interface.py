import os
import sys
import shutil
import tempfile
from ctypes import *

thorin_path = "./thorin"


@CFUNCTYPE(c_int, c_int)
def bar(x):
    return x + 35


c_interface_code = """
typedef int (*bar_type)(int);
bar_type g_bar;
int bar(int x) { return g_bar(x); }

void init(bar_type bar_) { g_bar = bar_; }
"""

with open("foo.thorin", "r") as f:
    thorin_code = f.read()

temp_c_code = tempfile.mktemp(".c")
temp_thorin_code = tempfile.mktemp(".thorin")
temp_so = tempfile.mktemp(".so")
temp_ll = tempfile.mktemp(".ll")

with open(temp_c_code, "w") as f:
    f.write(c_interface_code)

with open(temp_thorin_code, "w") as f:
    f.write(thorin_code)

# compile thorin to llvm
os.system(f"{thorin_path} --output-ll {temp_ll} {temp_thorin_code}")
# compile with c interface to so
os.system(
    f"clang -fPIC -shared -o {temp_so} {temp_c_code} {temp_ll} -Wno-override-module")

lib = CDLL(temp_so)
lib.init(bar)

print(lib.square(5))
print(lib.square(6))
print(lib.foo(5))
