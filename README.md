# Recurse
## Syntax


## EBNF
if statement:
```"if" expression ":" {expression} ";"```

if day == birthday :
    age++
;

function:
```"fun" name [arg1 {"," arg2}] ":" {expression} ";"```

fun function_name arg1, arg2, arg3:
    a = 1
    b = 1
    c = a + b
;

int = {digit}+
id = char{char | "_"}

expression = "(" expression ")" | int | digit
term = factor ("+" | "-") factor
factor = unary ("*" | "/") unary
unary = ("!" | "-") expression

expression = paren_expr | bin_expr | unary_expr | number;
paren_expr = "(" expression ")";
bin_expr = expression op expression;
unary_expr = unary_op expression;
unary_op = "-" | "!";
op = "+" | "-" | "/" | "*" | "==" | "<=" | ">=" | "<" | ">" | "&&" | "||";
