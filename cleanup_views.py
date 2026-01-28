import sys

# Read file
with open("inventory/views.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Keep lines 1-1438 and delete everything else
new_lines = lines[:1438]

# Write back
with open("inventory/views.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print(f"Kept first 1438 lines, deleted {len(lines) - 1438} lines")
