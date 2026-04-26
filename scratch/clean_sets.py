import json

def clean_data_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    sets_keys = set(data.get("Sets", {}).keys())

    modified = False
    if "Single" in data:
        for name, item in data["Single"].items():
            keys_to_remove = []
            for k in item.keys():
                if k in sets_keys:
                    keys_to_remove.append(k)
            for k in keys_to_remove:
                del item[k]
                modified = True

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Cleaned {file_path}")

clean_data_json('data.json')
clean_data_json('web/public/data.json')
print("Done.")
