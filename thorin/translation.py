# translation from python to thorin code (maybe first to C/llvm)


preamble = """
I will give you a description of a programming language.
Afterward, I will write you python code snippets.
Please only reply with a single code block containing the code in my programming language.

The language uses continuation passing style.
The language can handle dependent types.
For instance, `%mem.Ptr («n; T», 0:.Nat)` is a pointer to an array of type `T` with `n` elements.
Please use pointers to arrays to represent python lists.
""".strip()

axioms = """
The type of types is `*`.

The available memory operations are:
```
%mem.load:  [T: *, as: .Nat] -> [%mem.M, %mem.Ptr(T, as)] -> [%mem.M, T];
%mem.store: [T: *, as: .Nat] -> [%mem.M, %mem.Ptr(T, as), T] -> %mem.M;
%mem.alloc: [T: *, as: .Nat] -> %mem.M -> [%mem.M, %mem.Ptr(T, as)];
%mem.slot: [T: *, as: .Nat] -> [%mem.M, id: .Nat] -> [%mem.M, %mem.Ptr(T, as)];
%mem.free: [T: *, as: .Nat] -> [%mem.M, %mem.Ptr(T, as)] -> %mem.M;
%mem.lea: [n: .Nat, Ts: «n; *», as: .Nat] -> [%mem.Ptr(«j: n; Ts#j», as), i: .Idx n] -> %mem.Ptr(Ts#i, as), normalize_lea;
``` 
""".strip()

examples=[
"""
The power function in my language looks like:

```
.con .extern pow ((a b: I32), ret: .Cn I32) = {
    .con pow_then [] = ret (1:I32);

    .con pow_cont [v:I32] = {
        .let m = %core.wrap.mul _32 0 (a,v);
        ret m
    };
    .con pow_else [] = {
        .let b_1 = %core.wrap.sub _32 0 (b,1:I32);
        pow ((a,b_1),pow_cont)
    };
    .let cmp = %core.icmp.e _32 (b,0:I32);
    ((pow_else, pow_then)#cmp) ()
};
```

The call for $3^5$ in main would be 
```
.con .extern main [mem : %mem.M, argc : I32, argv : %mem.Ptr (%mem.Ptr (.Idx 256, 0:.Nat), 0:.Nat), return : .Cn [%mem.M, I32]] = {
    .con ret_cont r::[I32] = return (mem, r);

    .let c = (3:I32, 5:I32);
    pow (c,ret_cont)
};
```
""".strip()
]

def query(code):
  return f"""
Please translate 
```
{code}
```
""".strip()

repetition_query = """
If your last answer was not complete, please write the remaining part of your answer in a single code block. Do not repeat the first part of your answer.
""".strip()

example_text = "\n\n".join(examples)

gpt_query = lambda code: f"""
{preamble}

{example_text}

{axioms}

{query(code)}
""".strip()


# print(gpt_query("""
# def foo(x):
#   return (x + 35)**2
# """.strip()))

from chatgpt_wrapper import ChatGPT

bot = ChatGPT()
question = gpt_query("""
# def foo(x):
#   return (x + 35)**2
# """.strip())
# response = bot.ask("Lorem ipsum dolor sit amet.")
response = bot.ask(question)
print(response)  

# ```
# .con .extern foo [(x: I32), ret: .Cn I32] = {
#     .con foo_cont [v:I32] = ret v;
#     .con foo_then [] = {
#         .let m = %core.wrap.add _32 0 (x, 35:I32);
#         .let c = (m, 2:I32);
#         pow (c,foo_cont)
#     };
#     foo_then ()
# };
# ```
