import ast

try:
    with open("inventory/views.py", "r", encoding="utf-8") as f:
        content = f.read()
    ast.parse(content)
    print("Syntax is valid!")
except SyntaxError as e:
    print(f"Syntax error at line {e.lineno}, column {e.offsetno}: {e.msg}")
except Exception as e:
    print(f"Error: {e}")
