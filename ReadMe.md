# Thorin Python DSL

Thorin is powerful and extensible.
However, it is not designed to be a replacement for a full-fledged programming language.
For one, it is quite low-level.
Also, it is not designed to handle large programs.

It would be tedious to write the control logic and interfaces for full programs. 
Additionally, the compilation would be quite slow.

Therefore, we want to embed/interface with other languages.

## High-Level

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

## ABI

We could just write Thorin programs, compile them, and then interface with them via the C interface.
It is easy (and common) to call c functions from python. 
We can also let the inner c function call python functions. This can be handled using a callback function, a deep python embedding, or using communication.

Advantage:
* No need to write a compiler
* No need to design a high-level language

Disadvantage:
* Low-level code

## Transpiler

We could transpile high-level code to Thorin code and use the binary interface approach.
We would need a good way to handle bidirectional communication between the high-level language and Thorin.

One option could be to translate python to C (using cython) and C to Thorin.

Advantage:
* Direct inclusion => Easy to use

Disadvantage:
* Translate High-level code code
