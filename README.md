# Recurse
## Overview
### What is recurse
Recurse was made as a joke, and does not implement standart for/while loops. This functionality is to be achieved using recursion, and the language is designed to make recursion as convenient as possible to implement.

### Variables
Recurse functions similar to C in that everything is a number. Characters are numbers that correspond to ASCII characters, pointers are numbers that symbolize a memory address and strings are pointers to the first element in a sequence of characters. Because of this, Recurse does not have multiple variable types, only numbers. A variable will always evaluate to a number (integer, no float support yet). 

## Syntax
### Algebra
Doing basic math in recurse is much like you would do in any other language, or even in pure math. Standard orders of operations apply, and variables will always evaluate to a number which can be easily used in an equation

Ex:
```Python
a = 3
b = 10
x = 100
y = a * x + b
```

Inequalities and modulus (%) may also be used in statements, and inequalities will evaluate to 1 if they are true.

### Control flow
Since recurse lacks for and while loops, the only control flow statement is the if statement. If statements follow the following syntax:
```
if <condition> :
    <if body>
; else if <condition> :
    <else if body>
; else :
    <else body>
;
```
The characters : and ; are used instead of curly braces because they are easier to type, and since the semicolon was not used to terminate expressions. Parentheses are not required around the condition.

### Functions
The function syntax is similar to the if statement syntax, and is as follows:
```
fun name arg1, arg2, arg3:
    <body>
;
```
This form of function definition is convenient to implement a function such as the C printf function, which is solved by variadic functions. These functions are defined with '..' as their final argument, and automatically turn any argument provided in the function call past the static arguments into an array. These can be accessed with the local variables 'args' as a pointer to the array, and 'nargs' to give the number of arguments in the array. Finally to pass these variadic arguments on to recursive calls, you can supply '..' as the final argument to the recursive call and it will provide the current, updated version of args and nargs to the recursive call. Again note that args and nargs are supplied to the recursive call as they exist at the point in time in which the call is made, and previous modifications to args or nargs will apply. An example can be seen in tests/printf.rc

## Todos
- Comments
- Structs
- Including libraries
- Compilation