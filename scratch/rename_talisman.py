import json
import os

def rename_amulet_to_talisman(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple string replace for item names in keys and values
    # We use " Amulet" and "(Amulet)" to be safer
    content = content.replace(" Amulet", " Talisman")
    content = content.replace("(Amulet)", "(Talisman)")
    
    # Also check if it's just "Amulet" as a key or value
    # But be careful with "type": "Amulet" (though it should be Talisman now)
    
    data = json.loads(content)
    
    # Re-verify types just in case
    if "Single" in data:
        for name, item in data["Single"].items():
            if isinstance(item, dict) and "type" in item:
                if item["type"] == "Amulet":
                    item["type"] = "Talisman"

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

rename_amulet_to_talisman('data.json')
rename_amulet_to_talisman('web/public/data.json')
print("Renaming completed.")
