import ast

with open("inventory/views.py", "r", encoding="utf-8") as f:
    content = f.read()
    try:
        ast.parse(content)
        print("Syntax is valid!")
    except SyntaxError as e:
        print(f"Syntax error at line {e.lineno}, column {e.offset}: {e.msg}")
