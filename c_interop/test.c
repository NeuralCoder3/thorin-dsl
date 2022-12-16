extern int bar(int);

int foo(int x) { return bar(x + 2); }

int main() {
  int x = 0;
  x = foo(x);
  return x;
}
