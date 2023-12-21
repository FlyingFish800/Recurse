import argparse
import lexer
import parser

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
                    prog='Recurse',
                    description='Compiles/Interprets recurse programs')
    
    argparser.add_argument("filename", nargs="?", default=None)

    args = argparser.parse_args()

    filepath = args.filename

    l = lexer.lexer()
    p = parser.parser()

    if filepath == None:
        # REPL
        while True:
            # Get line of recurse
            line = input("> ")
            if line == "quit": break
            
            l.tokenize(line)
            print(l.tokens)

            ast = p.parse(l.tokens)

            l.reset()
            p.reset()

    else: 
        # Run file
        print(filepath)