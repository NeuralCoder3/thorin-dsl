clang -S -emit-llvm -o tmp.ll test.c
clang lib_bar.c tmp.ll -o tmp.out
