
import json

with open(r'c:\Users\UsEr\Desktop\Repository\COA-Calculator-Webapp\data.json', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "dmgToDebuff" in line:
        print(f"{i+1}: {line.strip()}")
