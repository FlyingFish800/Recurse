# Alexander Symons | Dec 20 2023 | interperter.py | recurse
# Contains the interpreter class, which holds the global state of
# the interpreter

import lexer

class interperter:
    # Array of variable contexts, 0 is globals and -1 is current context
    # Layout: variables, globally_declared_vars
    vars = [({}, [])]

    # Function bodies
    functions = {}

    returned = False

    def __init__(self):
        pass

    # Assign a variable to an expression
    def assignment(self, name, val):
        level = -1
        if name in self.vars[-1][1]:
            level = 0
        
        self.vars[level][0][name] = val.interpret(self)

    # Reference a variable to get its value
    def reference(self, name, line):
        level = -1
        if name in self.vars[-1][1]:
            level = 0

        val = self.vars[level][0].get(name)
        if val == None:
            print(f"ERROR: {'Global ' if level == 0 else ''}Variable '{name}' referenced before assignment on line {line} at depth {len(self.vars)}")
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
                print("Print only takes 1 arg")
                exit(1)

            print(args[0].interpret(self))
            return
        
        if self.functions.get(name) == None:
            print(f"ERROR: Function '{name}' has not been declared")
            exit(1)

        # TODO: Variadic functions

        #print("TODO: Variadic functions")

        fun_args, body = self.functions.get(name)
        if len(args) != len(fun_args):
            print("ERROR: Call signature and function signature do not match: Length")
            print(f"{name}'s signature has {len(fun_args)} arguments, call has {len(args)} arguments, and is not variadic")
            exit(1)

        # TODO:
        # Should add args as local variables
        self.vars.append(({str(name):value.interpret(self) for name, value in zip(fun_args, args)}, []))

        ret = 0
        current = 0
        while True:
            ret = body[current].interpret(self)
            if self.returned: break
            current += 1
            if current >= len(body): break
        print(ret)
        return ret

    # Return from a function
    def return_fun(self, value):
        val = value.interpret(self)
        self.vars.pop()
        self.returned = True
        return val