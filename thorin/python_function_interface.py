from ctypes import *
import tempfile
import os


def type_text(t):
    if t == c_int:
        return "int"
    else:
        raise Exception(f"Unknown type: {t}")


def prepare_function(functions):
    # type_defs, ptr, wrapper_funcs
    fun_list = []
    fun_names = {}
    type_defs = {}
    ptr_defs = {}
    wrappers = {}
    c_func_ty = {}
    c_func_ptr = {}
    for f, return_type, args in functions:
        name = f.__name__
        # result = f_type.restype
        # print(return_type)
        return_name = type_text(return_type)
        arg_names = [type_text(t) for t in args]
        type_def = f"typedef {return_name} (*{name}_type)({', '.join(arg_names)});"
        ptr = f"{name}_type g_{name};"
        arguments = [f"x{i}" for i in range(len(args))]
        typed_arguments = [
            f"{type_text(t)} {a}" for t, a in zip(args, arguments)]
        wrapper = f"""
{return_name} {name}({', '.join(typed_arguments)}) {{
    return g_{name}({', '.join(arguments)});
}}
      """.strip()

        fun_list.append(f)

        fun_names[f] = name
        type_defs[f] = type_def
        ptr_defs[f] = ptr
        wrappers[f] = wrapper

        c_func_ty[f] = CFUNCTYPE(return_type, *args)
        c_func_ptr[f] = c_func_ty[f](f)

    init_code = "void init("
    init_code += ', '.join([f"{fun_names[f]}_type {fun_names[f]}_" for f,
                            _, _ in functions])
    init_code += ") {\n"
    fun_assignments = []
    for f, _, _ in functions:
        fun_assignments.append(f"  g_{fun_names[f]} = {fun_names[f]}_;")
    init_code += "\n".join(fun_assignments)
    init_code += "\n}"

    interface = ""

    for f, _, _ in functions:
        interface += type_defs[f]+"\n"
        interface += ptr_defs[f]+"\n"
        interface += wrappers[f]+"\n"
        interface += "\n"
    interface += init_code+"\n"

    init_arguments = [c_func_ptr[f] for f, _, _ in functions]

    return interface, init_arguments


def compile(code, functions):
    temp_code = tempfile.mktemp(".c")
    temp_so = tempfile.mktemp(".so")

    with open(temp_code, "w") as f:
        f.write(code)

    os.system("cc -fPIC -shared -o %s %s" % (temp_so, temp_code))

    lib = CDLL(temp_so)
    lib.init(*functions)

    return lib


if __name__ == "__main__":
    def bar(x):
        return x + 35

    functions = [
        (bar, c_int, [c_int]),
    ]

    interface, init_arguments = prepare_function(functions)
    print(interface)
