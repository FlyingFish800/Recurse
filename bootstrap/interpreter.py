# Alexander Symons | Dec 20 2023 | interperter.py | recurse
# Contains the interpreter class, which holds the global state of
# the interpreter

class interperter:
    # Variables
    vars = {}

    # Function bodies
    functions = {}

    def __init__(self):
        pass

    # Assign a variable to an expression
    def assignment(self, name, val):
        self.vars[name] = val

    # Reference a variable to get its value
    def reference(self, name, line):
        val = self.vars.get(name)
        if val == None:
            print(f"ERROR: Variable '{name}' referenced before assignment on line {line}")
            exit(1)

        return val

    # Define a function
    def declare_fun(self, name, args, body):
        if not self.functions.get(name) == None:
            print(f"ERROR: Redeclaration of function {name}")
            exit(1)

        self.functions[name] = (args, body)

    # Call a function
    def invoke_fun(self, name, args):
        if name == "print":
            if len(args) != 1:
                print("Print only takes 1 arg")
                exit(1)

            print(args[0].interpret(self))
            return
        print("TODO: Wtf is a local variable")
        exit(1)

    # Return from a function
    def return_fun(self, value):
        print("TODO: Wtf is a return")
        exit(1)