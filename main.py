from lexer import Lexer
from Token import Types
from parser import Parser
from interpreter import Interpreter
import sys

def run_file(source_file):
    try:
        with open(source_file, "r") as file:
            lines = file.readlines()
    except IOError:
        print(f"Error: Could not open file {source_file}")
        sys.exit(1)

    interpreter = Interpreter(source_file)  # Holds global state like variable environment

    for line in lines:
        line = line.strip()
        if not line:
            continue

        print(f"Expression: {line}")
        try:
            lexer = Lexer(line)
            parser = Parser(lexer)
            statements = parser.parse()

            for stmt in statements:
                result = interpreter.visit(stmt)
                # Only print output for expressions and print statements
                if result is not None:
                    print(f"{line} = {result}")
        except Exception as e:
            print(f"Error processing expression '{line}': {e}")
        print("-" * 30)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        source_file = sys.argv[1]
    else:
        source_file = "C:\\Users\\ldi\\Language Design\\test.src"
    run_file(source_file)
