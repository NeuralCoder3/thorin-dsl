# Thorin Python DSL

Thorin is powerful and extensible.
However, it is not designed to be a replacement for a full-fledged programming language.
For one, it is quite low-level.
Also, it is not designed to handle large programs.

It would be tedious to write the control logic and interfaces for full programs. 
Additionally, the compilation would be quite slow.

Therefore, we want to embed/interface with other languages.

## Examples

We show an example how the user experience in Python could look like.

### String FFI

This part is already implemented.

```python

def bar(x):
    return x + 35

```
```python
code = """
```
```rust
[...] // omitted for brevity

// could also be automatically generated
.con bar [mem: %mem.M, a: I32, return : .Cn [%mem.M, I32]];

.con .extern foo [mem: %mem.M, a: I32, return : .Cn [%mem.M, I32]] = {
    .let b = %core.wrap.add _32 0 (a, 2:I32);
    bar (mem, b, return)
};
```
```python
"""
```
```python

thorin_interface = thorin(
    code, 
    [(bar, c_int, [c_int])] # could also be automatically generated
  )

# run the code
print(thorin_interface.foo(5)) # 42
```

### Framework

The framework is a (partly) reimplementation of `Def` with
additional quoting and unquoting features.
It makes heavy use of runtime types and overloading.
Additionally, combinators are provided to ease the creation of control flow.

There has to be a balance to not make the framework too complex
and keep the user from thinking general python code could be reified.

```python

def bar(x):
    return x + 35

def thorin_foo():
    # overloading for quoting unquoting
    thorin_bar = thorin(bar) # this call is resolved to thorin_wrap(bar)
    foo = function(int, [int])
    a = foo.arg(0)
    foo.return = thorin_bar(a + 2)
    # alternatively using more reflection (needs inversion/reflection of lambda terms)
    # foo = thorin(lambda a: thorin_bar(a + 2))
    return foo

foo = thorin(thorin_foo()) # resolved to thorin_execute(thorin_foo())
print(foo(5))
```

There are frameworks available that compile / transpile nearly complete python programs:
* [numba](https://numba.pydata.org/) for JIT compilation python to LLVM
* [JAX](https://jax.readthedocs.io/en/latest/notebooks/quickstart.html) for autograd, JIT compilation, python to XLA
* [AutoGrad](https://github.com/HIPS/autograd) (replaced by JAX) automatic differentiation, writes a log trace during execution (DAG)
* [Pythran](https://pythran.readthedocs.io/en/latest/) for compilation python to C++ 

On a related note, the python bytecode and interpreter is not as complicated as one might think:
* [Byterun](https://www.aosabook.org/en/500L/a-python-interpreter-written-in-python.html#fn1) a python interpreter written in python
    * [Github](https://github.com/nedbat/byterun)

## Concepts

We will present multiple non-exclusive approaches to implement a DSL.

### High-Level

The low-level interface can be solved by creating a high-level language that compiles down to Thorin.
Thorin acts as an intermediate representation for the high-level language.

Examples of high-level languages are:
* Impala
* Artic
* Future: Impala2
* possibly Future: Rust (via MIR)
* possibly Future: Idris (dependent types)

Advantage:
* No interface needed
* Full control over the features

Disadvantage:
* Limited to the features of the high-level language
* Another language to add to the other 9000
* Compilers are tedious to write
* Compilation time issue

### ABI/FFI

We could just write Thorin programs, compile them, and then interface with them via the C interface.
It is easy (and common) to call c functions from python. 
We can also let the inner c function call python functions. This can be handled using a callback function, a deep python embedding, or using communication.

Advantage:
* No need to write a compiler
* No need to design a high-level language

Disadvantage:
* Low-level code

Tools:
* Ctypes
* [cffi](https://cffi.readthedocs.io/en/latest/overview.html)
* [MessagePack](https://msgpack.org/)
  * analog to [call-haskell-from-anything](https://github.com/nh2/call-haskell-from-anything) (communication wrapper on top of c ffi)

### Communication

Similar to the ABI/FFI approach, but we actively communicate (e.g. using named pipes)
between both programs.

### Transpiler

We could transpile high-level code to Thorin code and use the binary interface approach.
We would need a good way to handle bidirectional communication between the high-level language and Thorin.

One option could be to translate python to C (using cython) and C to Thorin.

Advantage:
* Direct inclusion => Easy to use

Disadvantage:
* Translate High-level code code
