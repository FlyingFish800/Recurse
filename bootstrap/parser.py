import lexer

class node:
    line = 0
    def __init__(self, line):
        self.line = line

# Binary operation
class binary(node):
    def __init__(self, line, left, op, right):
        super().__init__(line)
        self.left = left
        self.op = op
        self.right = right

    # Evaluate in interpreter mode
    def interpret(self, i):
        if self.op.type == lexer.lexemeType.MINUS:
            return self.left.interpret(i) - self.right.interpret(i)
        elif self.op.type == lexer.lexemeType.PLUS:
            return self.left.interpret(i) + self.right.interpret(i)
        elif self.op.type == lexer.lexemeType.STAR:
            return self.left.interpret(i) * self.right.interpret(i)
        elif self.op.type == lexer.lexemeType.SLASH:
            return self.left.interpret(i) + self.right.interpret(i)
        elif self.op.type == lexer.lexemeType.EQUAL_EQUAL:
            return (int) (self.left.interpret(i) == self.right.interpret(i))
        elif self.op.type == lexer.lexemeType.BANG_EQUAL:
            return (int) (self.left.interpret(i) != self.right.interpret(i))
        elif self.op.type == lexer.lexemeType.GT_EQUAL:
            return (int) (self.left.interpret(i) >= self.right.interpret(i))
        elif self.op.type == lexer.lexemeType.LT_EQUAL:
            return (int) (self.left.interpret(i) <= self.right.interpret(i))
        elif self.op.type == lexer.lexemeType.GT:
            return (int) (self.left.interpret(i) > self.right.interpret(i))
        elif self.op.type == lexer.lexemeType.LT:
            return (int) (self.left.interpret(i) < self.right.interpret(i))
        elif self.op.type == lexer.lexemeType.PCT:
            return self.left.interpret(i) % self.right.interpret(i)
        else: 
            print(f"ERROR: Unimplemented binary operation {self.op}")
            exit(1)

    def __str__(self):
        return f"({self.left} {self.op} {self.right})"
    
    def __repr__(self):
        return str(self)

# Unary operations
class unary(node):
    def __init__(self, line, op, right):
        super().__init__(line)
        self.op = op
        self.right = right

    # Evaluate in interpreter mode
    def interpret(self, i):
        if self.op.type == lexer.lexemeType.MINUS:
            return -self.right.interpret(i)
        elif self.op.type == lexer.lexemeType.BANG:
            return not self.right.interpret(i)
        else: 
            print(f"ERROR: Unimplemented unary operation {self.op}")
            exit(1)

    def __str__(self):
        return f"({self.op} {self.right})"
    
    def __repr__(self):
        return str(self)

# Number literals
class number(node):
    def __init__(self, line, val):
        super().__init__(line)
        self.val = val

    # Evaluate in interpreter mode
    def interpret(self, i):
        return self.val

    def __str__(self):
        return f"{self.val}"
    
    def __repr__(self):
        return str(self)

# Variables or function names
class identifier(node):
    def __init__(self, line, val):
        super().__init__(line)
        self.val = val

    # Evaluate in interpreter mode
    def interpret(self, i):
        return i.reference(self.val, self.line)

    def __str__(self):
        return f"{self.val}"
    
    def __repr__(self):
        return str(self)
    
# Declaration of the use of a global variable
class glob(node):
    def __init__(self, line, name):
        super().__init__(line)
        self.name = name

    # Evaluate in interpreter mode
    def interpret(self, i):
        i.register_global(self.name)

    def __str__(self):
        return f"glob {self.name}"
    
    def __repr__(self):
        return str(self)
    
# Assignment of variable
class assignment(node):
    def __init__(self, line, name, val):
        super().__init__(line)
        self.name = name
        self.val = val

    # Evaluate in interpreter mode
    def interpret(self, i):
        value = self.val.interpret(i)
        i.assignment(self.name, value)
        return value

    def __str__(self):
        return f"{self.name} = {self.val}"
    
    def __repr__(self):
        return str(self)
    
# Assignment of a pointer
class ptr_assignment(node):
    def __init__(self, line, ptr, val):
        super().__init__(line)
        self.ptr = ptr
        self.val = val

    # Evaluate in interpreter mode
    def interpret(self, i):
        if type(self.ptr.val) != str:
            print("Multiple deref in assignment")
            exit(1)

        addr = i.reference(self.ptr.val, self.line)
        val = self.val.interpret(i)
        
        i.pointer_assignment(addr, val)
        return val

    def __str__(self):
        point = self.ptr
        level = 0
        while type(point) != str:
            level += 1
            point = point.val
        
        return f"{'*'*level}{point} = {self.val}"
    
    def __repr__(self):
        return str(self)
    
# If statement
class if_stmt(node):
    def __init__(self, line, cond, body, else_body):
        super().__init__(line)
        self.cond = cond
        self.body = body
        self.else_body = else_body

    # Evaluate in interpreter mode
    def interpret(self, i):
        condition = self.cond.interpret(i)

        if condition:
            for line in self.body:
                val = line.interpret(i)
                if i.returned:
                    return val
        elif self.else_body != []:
            for line in self.else_body:
                val = line.interpret(i)
                if i.returned:
                    return val

    def __str__(self):
        nl = "\n"
        return f"if {str(self.cond)} : \n{nl.join(list(map(lambda x:str(x), self.body)))}\n; else :\n{nl.join(list(map(lambda x:str(x), self.else_body)))}\n; "
    
    def __repr__(self):
        return str(self)
    
# Function declaration
class fun_declaration(node):
    def __init__(self, line, name, args, body):
        super().__init__(line)
        self.name = name
        self.args = args
        self.body = body

    # Evaluate in interpreter mode
    def interpret(self, i):
        i.declare_fun(self.name, self.args, self.body)

    def __str__(self):
        nl = "\n"
        return f"fun {self.name} {self.args}: \n{self.body} \n;"
    
    def __repr__(self):
        return str(self)
    
# Function call
class fun_call(node):
    def __init__(self, line, name, args):
        super().__init__(line)
        self.name = name
        self.args = args

    # Evaluate in interpreter mode
    # Note that this ends up 
    def interpret(self, i):
        ret = i.invoke_fun(self.name, self.args)
        #if self.name != "print": print("RETURNING", ret)
        return ret

    def __str__(self):
        nl = "\n"
        return f"{self.name}<INVOKE>({', '.join(list(map(lambda x:str(x), self.args)))})"
    
    def __repr__(self):
        return str(self)
    
# Return from a function
class fun_ret(node):
    def __init__(self, line, val):
        super().__init__(line)
        self.val = val

    # Evaluate in interpreter mode
    def interpret(self, i):
        return i.return_fun(self.val)

    def __str__(self):
        return f"ret {self.val}"
    
    def __repr__(self):
        return str(self)
    
# Dereference a pointer
class deref(node):
    def __init__(self, line, val):
        super().__init__(line)
        self.val = val

    # Evaluate in interpreter mode
    def interpret(self, i):
        addr = self.val.interpret(i)

        return i.pointer_reference(addr)

    def __str__(self):
        return f"*({self.val})"
    
    def __repr__(self):
        return str(self)
    
# Dereference a pointer
class variadic_recursion_arg(node):
    def __init__(self, line):
        super().__init__(line)

    # Evaluate in interpreter mode
    def interpret(self, i):
        print("ERROR: UNimplement variad")
        exit(1)

    def __str__(self):
        return f".."
    
    def __repr__(self):
        return str(self)
    
# Contains a string literal
class literal_string(node):
    def __init__(self, line, val):
        super().__init__(line)
        self.val = val

    # Evaluate in interpreter mode
    def interpret(self, i):
        addr = i.alloc_mem(len(self.val) + 1)

        for offset, char in enumerate(self.val):
            i.pointer_assignment(addr + offset, ord(char))
        i.pointer_assignment(addr + len(self.val), 0) # Null terminate

        #print(f"{self.val} @ {addr}")
        #for j in range(len(self.val) + 1):
        #    print(f"{addr+j}: {(i.pointer_reference(addr+j))}/{chr(i.pointer_reference(addr+j))}")
        #print(f"{self.val}: {addr}:{len(self.val)}")
        return addr

    def __str__(self):
        return f"\"{self.val}\""
    
    def __repr__(self):
        return str(self)
    
# Contains an array literal
class literal_array(node):
    def __init__(self, line, val):
        super().__init__(line)
        self.val = val

    # Evaluate in interpreter mode
    def interpret(self, i):
        addr = i.alloc_mem(len(self.val))

        for offset, val in enumerate(self.val):
            i.pointer_assignment(addr + offset, int(val))

        return addr

    def __str__(self):
        return f"[{', '.join(self.val)}]"
    
    def __repr__(self):
        return str(self)

# Parse tokens into AST
class parser:
    tokens = []
    current = 0

    def __init__(self):
        pass

    # Returns true if we are at or past last token
    def done(self):
        return self.current >= len(self.tokens)
    
    # Returns true and consumes next token if it matches any in to_match
    def match(self, to_match):
        if type(to_match) == lexer.lexemeType:
            if to_match == self.tokens[self.current].type:
                self.current += 1
                return True
        elif type(to_match) == tuple:
            for current in to_match:
                if current == self.tokens[self.current].type:
                    self.current += 1
                    return True
            
        return False
    
    # Check value of next token
    def peek(self, to_match):
        if self.current < len(self.tokens): return False
        return to_match == self.tokens[self.current].type

    
    # Look at the previously consumed token
    def previous(self):
        return self.tokens[self.current - 1]
    
    # Highest priority structure, the equality expression
    def expression(self):
        left = self.comparison()

        while not self.done() and self.match((lexer.lexemeType.BANG_EQUAL, lexer.lexemeType.EQUAL_EQUAL, lexer.lexemeType.GT_EQUAL, lexer.lexemeType.LT_EQUAL)):
            op = self.previous()
            right = self.comparison()
            left = binary(self.previous().line, left, op, right)

        return left
    
    # Next highest priority structure, the comparison
    def comparison(self):
        left = self.modulo()

        while not self.done() and self.match((lexer.lexemeType.GT, lexer.lexemeType.LT, lexer.lexemeType.GT_EQUAL, lexer.lexemeType.LT_EQUAL)):
            op = self.previous()
            right = self.modulo()
            left = binary(self.previous().line, left, op, right)

        return left
    
    # modulus
    def modulo(self):
        left = self.term()

        while not self.done() and self.match((lexer.lexemeType.PCT)):
            op = self.previous()
            right = self.term()
            left = binary(self.previous().line, left, op, right)

        return left
    
    # +/-
    def term(self):
        left = self.factor()

        while not self.done() and self.match((lexer.lexemeType.PLUS, lexer.lexemeType.MINUS)):
            op = self.previous()
            right = self.factor()
            left = binary(self.previous().line, left, op, right)

        return left
    
    # * and /
    def factor(self):
        left = self.unary()

        while not self.done() and self.match((lexer.lexemeType.STAR, lexer.lexemeType.SLASH)):
            op = self.previous()
            right = self.unary()
            left = binary(self.previous().line, left, op, right)

        return left
    
    # Things with a - or ! before them
    def unary(self):
        if not self.done() and self.match((lexer.lexemeType.MINUS, lexer.lexemeType.BANG)):
            op = self.previous()
            right = self.unary()
            return unary(self.previous().line, op, right)

        return self.primary()
    
    # Smallest possible thing, or ()
    def primary(self):
        if self.done():
            print("ERROR: Ran out of tokens")
            exit(1)

        if self.match((lexer.lexemeType.STRING)):
            return literal_string(self.previous().line, self.previous().value)

        if self.match((lexer.lexemeType.ARRAY)):
            return literal_array(self.previous().line, self.previous().value)

        if self.match((lexer.lexemeType.NUMBER)):
            return number(self.previous().line, self.previous().value)

        if self.match((lexer.lexemeType.IDENTIFIER)):
            name = self.previous().value

            if not self.done() and self.match((lexer.lexemeType.PAREN_L)):
                args = []
                done = False
                while not self.match((lexer.lexemeType.PAREN_R)):
                    if done:
                        print(f"ERROR: Arguments found after variadic recursion argment in {name} on line {self.previous().line}")
                        exit(1)

                    if self.match((lexer.lexemeType.DOT_DOT)):
                        args.append(variadic_recursion_arg(self.previous().line))
                        done = True
                    else:
                        args.append(self.comparison())
                    
                    if self.match((lexer.lexemeType.PAREN_R)): break
                    elif self.match((lexer.lexemeType.COMMA)): continue
                    else:
                        print("ERROR: Incorrect syntax in function call")
                        exit(1)

                return fun_call(self.previous().line, name, args)
            
            return identifier(self.previous().line, name)

        if self.match((lexer.lexemeType.PAREN_L)):
            epxression = self.expression()

            if self.done() or not self.match((lexer.lexemeType.PAREN_R)):
                print("ERROR: Couldn't find right paren")
                exit(1)
            
            return epxression
        
        if self.match((lexer.lexemeType.STAR)):
            dereferences = 1
            while self.match((lexer.lexemeType.STAR)):
                if self.done():
                    print(f"ERROR: No identifier found in dereference on line {self.previous().line}")
                    exit(1)
                dereferences += 1
            
            prim = self.primary()

            dereference = deref(self.previous().line, prim)
            for i in range(dereferences - 1):
                dereference = deref(self.previous().line, dereference)

            return dereference
        
        print(f"ERROR: Unhandled lexeme {self.tokens[self.current].type} on line {self.tokens[self.current].line}")
        exit(1)
        
    # A line of recurse
    def statement(self):
        if self.done():
            print("ERROR: No more tokens")
            exit(1)

        # Dereferenceing a variable
        if self.tokens[self.current].type == lexer.lexemeType.STAR:
            dereference = self.primary()
            if type(dereference) != deref:
                print("ERROR: Not a deref")
                exit(1)

            if not self.done() and self.match((lexer.lexemeType.EQUAL)):
                value = self.statement()
                return ptr_assignment(dereference.line, dereference, value)
            
            # Not assignment, unparse the dereferencing
            point = dereference
            level = 0
            while type(point) != str:
                level += 1
                point = point.val

            self.current -= level + 1

        # Assignment
        if self.match((lexer.lexemeType.IDENTIFIER)):
            left = identifier(self.previous().line, self.previous().value)
            if not self.done() and self.match((lexer.lexemeType.EQUAL)):
                op = self.previous()
                right = self.statement()
                return assignment(self.previous().line, left.val, right)
            else: 
                # Go back if not assignment
                self.current -= 1

        # If statement
        if self.match((lexer.lexemeType.IF)):
            cond = self.expression()

            if self.done():
                print(f"ERROR: Missing body of if statement on line {cond.line}")
                exit(1)

            if not self.match((lexer.lexemeType.COLON)):
                print(f"ERROR: No colon in if statement on line {cond.line}")
                exit(1)

            body = []
            while not self.match((lexer.lexemeType.SEMICOLON)):
                body.append(self.statement())

                if self.done():
                    print(f"ERROR: If block not closed on line {cond.line}")
                    exit(1)

            # Else block exists
            else_body = []
            if not self.done() and self.match((lexer.lexemeType.ELSE)):
                if self.done():
                    print(f"ERROR: Expected block after else on line {self.previous().line}")
                    exit(1)

                # Else body
                if self.match((lexer.lexemeType.COLON)):
                    while not self.match((lexer.lexemeType.SEMICOLON)):
                        else_body.append(self.statement())

                        if self.done():
                            print(f"ERROR: Else block not closed on line {cond.line}")
                            exit(1)
                else: else_body.append(self.statement())


            return if_stmt(self.previous().line, cond, body, else_body)

        # Function declaration
        if self.match((lexer.lexemeType.FUN)):
            if not self.match((lexer.lexemeType.IDENTIFIER)):
                print("ERROR: Function name required")
                exit(1)

            name = self.previous()
            args = []

            variadic = False

            # Get args if they exist
            while not self.match((lexer.lexemeType.COLON)):
                if variadic:
                    print("ERROR: Variadic functions may not have any static args after variadic arg")
                    exit(1)

                if not self.match((lexer.lexemeType.IDENTIFIER)) and not self.match((lexer.lexemeType.DOT_DOT)):
                    print("ERROR: Function args must be identifiers")
                    exit(1)
                
                if self.previous().type == lexer.lexemeType.DOT_DOT:
                    variadic = True
                args.append(self.previous())

                if self.match((lexer.lexemeType.COMMA)):
                    continue
                elif self.match((lexer.lexemeType.COLON)):
                    break
                else:
                    print("ERROR: Incorrect format for function declaration args")
                    exit(1)

            # Get function body
            body = []
            while not self.match((lexer.lexemeType.SEMICOLON)) and not self.done():
                body.append(self.statement())
                
            if len(body) == 0:
                print(f"ERROR: Empty functions not allowed. '{name.value}' is empty on line {name.line}")
                exit(1)

            # Make sure every function returns
            if type(body[-1]) != fun_ret:
                print(f"WARN: ret not found at the end of function '{name.value}', injecting 'ret' at last line")
                body.append(fun_ret(self.previous().line, number(self.previous().line, 0)))

            return fun_declaration(name.line, name.value, args, body)
        
        # Function return
        if self.match((lexer.lexemeType.RET)):
            # If last token or next token is on different line, return 
            ## TODO: Check not semicolon
            if self.done() or self.tokens[self.current].line != self.previous().line or self.tokens[self.current].type == lexer.lexemeType.SEMICOLON:
                return fun_ret(self.previous().line, number(self.previous().line, 0))
            
            return fun_ret(self.previous().line, self.comparison())
        
        # Global function declaration
        if self.match((lexer.lexemeType.GLOB)):
            if not self.done() and self.match((lexer.lexemeType.IDENTIFIER)):
                return glob(self.previous().line, self.previous().value)
            
            print(f"ERROR: Incorrect use of global declaration 'glob' on line {self.previous().line}")
            exit(1)
            
            
        return self.expression()
         

    # Parse the tokens and generate AST
    def parse(self, tokens):
        self.tokens = tokens

        statements = []

        while not self.done():
            statements.append(self.statement())

        return statements

    # Reset state of parser
    def reset(self):
        self.tokens = []
        self.current = 0
    