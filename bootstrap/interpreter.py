# Alexander Symons | Dec 20 2023 | interperter.py | recurse
# Contains the interpreter class, which holds the global state of
# the interpreter

import lexer
import parser

class interperter:
    # Array of variable contexts, 0 is globals and -1 is current context
    # Layout: variables, globally_declared_vars
    vars = [({}, [])]

    # Function bodies
    functions = {}

    returned = False

    memory = {}

    def __init__(self):
        pass

    # Allocate <entries> sequential unsused memeory addresses
    def alloc_mem (self, entries):
        used = self.memory.keys()
        addresses = list(range(entries))

        # While addresses are in the used set, increment all addrs and try that
        while used & addresses != set():
            addresses = set([i+1 for i in addresses])

        for addr in addresses:
            self.memory[addr] = 0

        return min(addresses)

    # Assign a variable to an expression
    def pointer_assignment(self, addr, val):
        if type(val) != int:
            print(f"ERROR: (internal) memory adress can only be set to ints, not {type(val)}")
            exit(1)

        self.memory[addr] = val

    # Assign a variable to an expression
    def pointer_reference(self, addr):
        val = self.memory.get(addr)
        #print(f"ACCESSED [{addr}]:{val}/{chr(val)}")
        if val == None:
            print(f"ERROR: (runtime) Memory address dereferenced before assignment")
            exit(1)

        return val

    # Assign a variable to an expression
    def assignment(self, name, val):
        level = -1
        if name in self.vars[-1][1]:
            level = 0
        
        if type(val) != int: val = val.interpret(self)
        self.vars[level][0][name] = val

    # Reference a variable to get its value
    def reference(self, name, line):
        level = -1
        if name in self.vars[-1][1]:
            level = 0

        val = self.vars[level][0].get(name)
        if val == None:
            print(f"ERROR: {'Global ' if level == 0 else ''}Variable '{name}' referenced before assignment on line {line} at depth {len(self.vars) - 1}")
            exit(1)

        if type(val) != int: 
            print(f"ERROR: (internal) variable {name} set to expression on line {line}")
            exit(1)
        
        return val

    # Define a function
    def declare_fun(self, name, args, body):
        if not self.functions.get(name) == None:
            print(f"ERROR: Redeclaration of function {name}")
            exit(1)

        self.functions[name] = (args, body)

    # Register a variable as a global variable
    def register_global(self, name):
        self.vars[-1][1].append(name)

    # Call a function
    def invoke_fun(self, name, args):
        if name == "print":
            if len(args) != 1:
                print("ERROR: Print only takes 1 arg")
                exit(1)
            
            #print("PRINT", chr(args[0].interpret(self)))

            #print(f"RECURSE: {args[0].interpret(self)} on line {args[0].line} at recursion level {len(self.vars)-1}")
            val = chr(args[0].interpret(self))
            print(val, end="")
            return
        
        if name == "printi":
            if len(args) != 1:
                print("ERROR: Print only takes 1 arg")
                exit(1)

            #print(f"RECURSE: {args[0].interpret(self)} on line {args[0].line} at recursion level {len(self.vars)-1}")
            print((args[0].interpret(self)), end="")
            return
        
        if self.functions.get(name) == None:
            print(f"ERROR: Function '{name}' has not been declared")
            exit(1)

        # TODO: Variadic functions

        #print("TODO: Variadic functions")

        fun_args, body = self.functions.get(name)
        variadic = fun_args[-1].type == lexer.lexemeType.DOT_DOT

        if len(args) != len(fun_args) and not variadic:
            print("ERROR: Call signature and function signature do not match: Length")
            print(f"{name}'s signature has {len(fun_args)} arguments, call has {len(args)} arguments, and is not variadic")
            exit(1)
        elif len(args) < len(fun_args) - 1:
            print("ERROR: Variadic functions need to have at least all static arguments satisfied")
            print(f"{name} was called with {len(args)} arguments, needs at least {len(fun_args) - 1}")
            exit(1)

        dynamic_args = len(args) - len(fun_args) + 1
        start = len(fun_args) - 1

        variadic_recursion = False

        if type(args[-1]) == parser.variadic_recursion_arg:
            variadic_nargs = self.reference("nargs", args[-1].line)
            variadic_args = self.reference("args", args[-1].line)
            variadic_recursion = True

        # Arguments are local variables
        locals = ({str(name):value.interpret(self) for name, value in zip(fun_args, args) if name.type != lexer.lexemeType.DOT_DOT}, [])
        #if len(self.vars) == 1: print(locals)
        if variadic and not variadic_recursion:
            # Variadic has nargs (number of args) and args (array)
            locals[0]["nargs"] = dynamic_args

            # TODO: Check this out, validate it
            addr = self.alloc_mem(dynamic_args)
            for i in range(dynamic_args):
                self.pointer_assignment(addr + i, args[start + i].interpret(self))

            locals[0]["args"] = addr

        if variadic and variadic_recursion:
            locals[0]["nargs"] = variadic_nargs
            locals[0]["args"] = variadic_args



        self.vars.append(locals)

        ret = 0
        current = 0
        while True:
            ret = body[current].interpret(self)
            if self.returned: break
            current += 1
            if current >= len(body): break

        self.returned = False
        
        return ret

    # Return from a function
    def return_fun(self, value):
        val = value.interpret(self)
        self.vars.pop()
        self.returned = True
        return val