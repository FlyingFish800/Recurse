import lexer

class node:
    def __init__(self):
        pass

class binary(node):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return f"({self.left} {self.op} {self.right})"
    
    def __repr__(self):
        return str(self)


class unary(node):
    def __init__(self, op, right):
        super().__init__()
        self.op = op
        self.right = right

    def __str__(self):
        return f"({self.op} {self.right})"
    
    def __repr__(self):
        return str(self)

class number(node):
    def __init__(self, val):
        super().__init__()
        self.val = val

    def __str__(self):
        return f"{self.val}"
    
    def __repr__(self):
        return str(self)

class identifier(node):
    def __init__(self, val):
        super().__init__()
        self.val = val

    def __str__(self):
        return f"{self.val}"
    
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
    
    # Look at the previously consumed token
    def previous(self):
        return self.tokens[self.current - 1]
    
    # Highest priority structure, the equality expression
    def expression(self):
        left = self.comparison()

        while not self.done() and self.match((lexer.lexemeType.BANG_EQUAL, lexer.lexemeType.EQUAL_EQUAL, lexer.lexemeType.GT_EQUAL, lexer.lexemeType.LT_EQUAL)):
            op = self.previous()
            right = self.comparison()
            left = binary(left, op, right)

        return left
    
    # Next highest priority structure, the comparison
    def comparison(self):
        left = self.term()

        while not self.done() and self.match((lexer.lexemeType.GT, lexer.lexemeType.LT, lexer.lexemeType.GT_EQUAL, lexer.lexemeType.LT_EQUAL)):
            op = self.previous()
            right = self.term()
            left = binary(left, op, right)

        return left
    
    # +/-
    def term(self):
        left = self.factor()

        while not self.done() and self.match((lexer.lexemeType.PLUS, lexer.lexemeType.MINUS)):
            op = self.previous()
            right = self.factor()
            left = binary(left, op, right)

        return left
    
    # * and /
    def factor(self):
        left = self.unary()

        while not self.done() and self.match((lexer.lexemeType.STAR, lexer.lexemeType.SLASH)):
            op = self.previous()
            right = self.unary()
            left = binary(left, op, right)

        return left
    
    # Things with a - or ! before them
    def unary(self):
        if not self.done() and self.match((lexer.lexemeType.MINUS, lexer.lexemeType.BANG)):
            op = self.previous()
            right = self.unary()
            return unary(op, right)

        return self.primary()
    
    # Smallest possible thing, or ()
    def primary(self):
        if self.done():
            print("ERROR: Ran out of tokens")

        if self.match((lexer.lexemeType.NUMBER)):
            return number(self.previous().value)

        if self.match((lexer.lexemeType.IDENTIFIER)):
            return number(self.previous().value)

        if self.match((lexer.lexemeType.PAREN_L)):
            epxression = self.expression()

            if self.done() or not self.match((lexer.lexemeType.PAREN_R)):
                print("ERROR: Couldn't find right paren")
                exit(1)
            
            return epxression
        
        

    # Parse the tokens and generate AST
    def parse(self, tokens):
        self.tokens = tokens

        while not self.done():
            print(self.expression())

    # Reset state of parser
    def reset(self):
        self.tokens = []
        self.current = 0
    