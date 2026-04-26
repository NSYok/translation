
import json

with open(r'c:\Users\UsEr\Desktop\Repository\COA-Calculator-Webapp\data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

keys = set()

def extract_keys(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            # Skip tier numbers and category names
            if k not in ["Single", "Sets", "type", "Type"] and not k.isdigit():
                keys.add(k)
            extract_keys(v)

extract_keys(data)
for k in sorted(list(keys)):
    print(k)
