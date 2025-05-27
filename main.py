import sys
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

def run_source(source_code, source_name="<input>"):
    interpreter = Interpreter(source_name)
    buffer = ""
    open_braces = 0

    for raw_line in source_code.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        buffer += line + "\n"
        open_braces += line.count("{") - line.count("}")

        # If still inside a block, wait for more lines
        if open_braces > 0:
            continue

        # Try parsing and interpreting the full block
        print(f"Expression: {buffer.strip()}")
        try:
            lexer = Lexer(buffer)
            parser = Parser(lexer)
            statements = parser.parse()

            for stmt in statements:
                result = interpreter.visit(stmt)
                if result is not None and not isinstance(result, str):
                    print(f"{line} = {result}")
                elif isinstance(result, str):
                    print(result)
        except Exception as e:
            print(f"Error processing expression '{buffer.strip()}': {e}")

        print("-" * 30)
        buffer = ""
        open_braces = 0

def run_file(file_path):
    try:
        with open(file_path, "r") as file:
            source_code = file.read()
        print(f"\n=== Running {file_path} ===")
        run_source(source_code, file_path)
    except IOError:
        print(f"Error: Could not open file {file_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for file_path in sys.argv[1:]:
            run_file(file_path)
    else:
        print("Usage: python main.py <file1.src> <file2.src> ...")
        #run_file("C:\\Users\\ldi\\Language Design\\program.src")
        #run_file("C:\\Users\\ldi\\Language Design\\test.src")

