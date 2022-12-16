// extern int bar(int);
// int foo(int x) { return bar(x + 2); }

typedef int (*bar_type)(int);
int foo2(int x, bar_type bar) { return bar(x + 2); }
