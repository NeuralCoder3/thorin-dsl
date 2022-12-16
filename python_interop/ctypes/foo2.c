// extern int bar(int);

typedef int (*bar_type)(int);
bar_type bar;
void init(bar_type bar_) { bar = bar_; }

int foo(int x) { return bar(x + 2); }

