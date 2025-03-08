#from IPython.utils.coloransi import value
from lexer import Lexer
from Token import Types
from parser import Parser
from interpreter import Interpreter
import sys


#from enum import Enum

def read_lexer_from_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue
        print(f"Expression: {line}")
        lexer = Lexer(line)
        while True:
            token = lexer.get_next_token()
            print(token)
            if token.type == Types.EOF:
                break
        print("-" * 30)

"""
if read_lexer_from_file == "__main__":
    if len(sys.argv) > 1:
        source_file = sys.argv[1]
else:
    source_file = "C:\\Users\\ldi\\Language Design\\test.src"  # Default file path
    read_lexer_from_file("C:\\Users\\ldi\\Language Design\\test.src")
"""
if __name__ == "__main__":
    if len(sys.argv) > 1:
        source_file = sys.argv[1]
    else:
        source_file = "C:\\Users\\ldi\\Language Design\\test.src"  # Default file path
    try:
        with open(source_file, "r") as file:
            lines = file.readlines()
    except IOError:
        print(f"Error: Could not open file {source_file}")
        sys.exit(1)

    for line in lines:
        line = line.strip()
        if not line:
            continue  # Skip blank lines
        print(f"Expression: {line}")
        try:
            # Create a new lexer, parser, and interpreter for each expression
            lexer = Lexer(line)
            parser = Parser(lexer)
            interpreter = Interpreter(parser)
            result = interpreter.interpret()
            print(f"{line} = {result}")
        except Exception as e:
            print(f"Error processing expression '{line}': {e}")
        print("-" * 30)
