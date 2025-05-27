README: USING THE INTERPRETER

This is a custom language interpreter written in Python.

INSTRUCTIONS:

1. Write your program in a `.txt` file using the custom language syntax.
   Example program (saved as `test.src` and `program.src`):

Language Syntax:
----------------
- Assignment:       quickMaths = 10
- Arithmetic:       x + 5 * 2
- Boolean logic:    x > 5 and y < 20
- Strings:          message = "hello" + " world"
- Print:            print quickMaths
- Variable declaration: quickMaths = 10
- Variable reassignment: quickMaths = quickMaths + 1
- Variable deletion: del quickMaths
- input for user input: name = input("What is your name? ")
- Logical Comparison: true != false

- if and else statements:
if (x > 10) {
  print "Big"
} else {
  print "Small"
}

- While Loops:
while (x > 0) {
  print x
  x = x - 1
}


2. To run this file using the interpreter:
    In IntelliJ: Right-click `main.py`, edit run configuration to pass `test.src` or the `program.src` files as an argument. This will require using the already hardcoded file path in the main.py file which would have to be changed just in case you decide to run another program file to test the program
    Or, use terminal:
     `python3 main.py test.src, program.src` which can be used to run a single file or multiple files

3. The interpreter supports:
- Variable declarations
- Arithmetic operations
- Boolean logic
- String concatenation
- Logical and comparison operations
- Print statements
- Control Flow Statements (if, else, while loops, Nested statements)



