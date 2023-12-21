from enum import Enum, auto

# Token type
class lexemeType(Enum):
    PLUS = auto()
    MINUS = auto()
    PAREN_L = auto()
    PAREN_R = auto()
    STAR = auto()
    SLASH = auto()
    COLON = auto()
    SEMICOLON = auto()
    BANG = auto()
    EQUAL = auto()
    GT = auto()
    LT = auto()

    EQUAL_EQUAL = auto()
    BANG_EQUAL = auto()
    LT_EQUAL = auto()
    GT_EQUAL = auto()

    NUMBER = auto()
    IDENTIFIER = auto()

singletLexemeDict = {lexemeType.PLUS:"+", lexemeType.MINUS:"-", lexemeType.PAREN_L:"(", lexemeType.PAREN_R:")", lexemeType.STAR:"*", lexemeType.SLASH:"/", lexemeType.COLON:":", lexemeType.SEMICOLON:";", lexemeType.BANG:"!", lexemeType.EQUAL:"=", lexemeType.LT:"<", lexemeType.GT:">"}
doubletLexemeDict = {lexemeType.EQUAL_EQUAL:"==", lexemeType.BANG_EQUAL:"!=", lexemeType.LT_EQUAL:"<=", lexemeType.GT_EQUAL:">="}

# Each token, has a type and value
class lexeme:
    type : lexemeType = None
    value = None

    def __init__(self, type : lexemeType, value = None):
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        char = singletLexemeDict.get(self.type)
        if char != None: return f"{char}"

        char = doubletLexemeDict.get(self.type)
        if char != None: return f"{char}"
        
        return f"{self.value}"


# Handles lexing operations
class lexer:
    # Current char in line, and line num
    current = 0
    line = 1

    # Tokenized tokens
    tokens = []

    start_current = 0

    def __init__(self):
        pass

    # Skip all whitespace chars
    def skipWhitespace(self, line):
        whitespace = (" ", "\t", "\n", "\r")
        
        if line[self.current] == "\n": self.line += 1
        if line[self.current] in whitespace: self.current += 1

    # Returns true if the char is a part of a single char token
    def isSinglet(self, char):
        return char in list(singletLexemeDict.values())
    
    # Returns true if char is part of 2 char token
    def isDoublet(self, char, peek):
        if not char in list(map(lambda x:x[0], list(doubletLexemeDict.values()))):
            return False # First char wrong
        
        return peek in list(map(lambda x:x[1], list(doubletLexemeDict.values())))

    # Look at current char
    def peek(self, line):
        return line[self.current]

    # Get current, and advance to next
    def getc(self, line):
        char = line[self.current]
        self.current += 1
        return char
    
    def done(self, line):
        return self.current >= len(line)

    # Get one token
    def getToken(self, line):
        self.skipWhitespace(line)

        # Try to handle as double char first
        char = self.getc(line)

        if not self.done(line) and self.isDoublet(char, self.peek(line)):
            next_char = self.getc(line)
            for item in doubletLexemeDict.items():
                seq = item[1]
                print(seq)
                if seq[0] == char and seq[1] == next_char:
                    return lexeme(item[0])

        if self.isSinglet(char):
            for item in singletLexemeDict.items():
                if item[1] == char:
                    return lexeme(item[0])
        
        # Otherwise handle multi-char token

        # First char number means it must be number
        if char.isnumeric():
            number = []
            while True:
                number.append(char)

                if self.done(line) or not self.peek(line).isnumeric(): break
                char = self.getc(line)

            return lexeme(lexemeType.NUMBER, int("".join(number)))
        
        else:
            # Otherwise it must be identifier
            id = []
            while True:
                id.append(char)

                if self.done(line) or (not self.peek(line).isalpha() and not self.peek(line) == "_"): break
                char = self.getc(line)

            # TODO:
            # Check for keywords here!
                
            # NOTE:
            # afadfs?adffa? gets turned into [afadfs, ?adffa, ?] idk why

            return lexeme(lexemeType.IDENTIFIER, "".join(id))

        


    # Turn a line of code into a string of tokens
    def tokenize(self, line):
        # While chars left in string, tokenize it
        while self.current < len(line):
            self.start_current = self.current
            self.tokens.append(self.getToken(line))

    # After done tokenizing a line reset
    def reset(self):
        self.current = 0
        self.line = 1
        self.tokens = []




# Test code
if __name__ == "__main__":
    l = lexer()
    l.tokenize("(2 + 3) * 4")
    print(l.tokens)