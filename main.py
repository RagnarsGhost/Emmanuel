from lexer import Lexer
from Token import Types

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

if __name__ == "__main__":
    read_lexer_from_file(r"test.src")
