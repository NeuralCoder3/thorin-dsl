
from ctypes import *

# cc -fPIC -shared -o square.so square.c
square_so = CDLL("./square.so")

print(square_so.square(5))
