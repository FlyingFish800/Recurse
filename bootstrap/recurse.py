import argparse
import lexer
import parser
import interpreter

class Recurse:
    state = None
    l = None
    p = None

    def __init__(self):
        self.l = lexer.lexer()
        self.p = parser.parser()
        self.state = interpreter.interperter()

    # Load a recurse file to use its contents
    def loadFile(self, path):
        # Run file
        # Tokenize each line
        with open(path, "r") as f:
            line = f.readline()
            while line != "":
                # Trim off the nl
                line = line.split("\n")[0]
                self.l.tokenize(line)
                line = f.readline()

        #print("Toks:", l.tokens)

        ast = self.p.parse(self.l.tokens)

        #print(ast)

        for exp in ast:
            exp.interpret(self.state)

    def callFunction(self, function_name, args):
        self.l.reset()
        self.p.reset()

        recurse = f"{function_name}({', '.join(args)})"
        self.l.tokenize(recurse)
        ast = self.p.parse(self.l.tokens)
        return ast[0].interpret(self.state)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
                    prog='Recurse',
                    description='Compiles/Interprets recurse programs')
    
    argparser.add_argument("filename", nargs="?", default=None)

    args = argparser.parse_args()

    filepath = args.filename

    l = lexer.lexer()
    p = parser.parser()
    i = interpreter.interperter()

    if filepath == None:
        # REPL
        while True:
            # Get line of recurse
            line = input("> ")
            if line == "quit": break
            
            if line.replace(" ","").endswith(":"):
                depth = 1
                while depth > 0:
                    l.tokenize(line)
                    line = input("- ")
                    if line.replace(" ","").endswith(":"):
                        depth += 1
                    elif line.replace(" ","").endswith(";"):
                        depth -= 1

            
            l.tokenize(line)
            print(l.tokens)

            ast = p.parse(l.tokens)

            for exp in ast:
                print(exp.interpret(i))

            l.reset()
            p.reset()

    else: 
        # Run file
        # Tokenize each line
        with open(filepath, "r") as f:
            line = f.readline()
            while line != "":
                # Trim off the nl
                line = line.split("\n")[0]
                l.tokenize(line)
                line = f.readline()

        #print("Toks:", l.tokens)

        ast = p.parse(l.tokens)

        #print(ast)

        for exp in ast:
            exp.interpret(i)