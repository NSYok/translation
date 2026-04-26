import json
import os

def migrate_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    def get_new_type(name, current_type):
        name_lower = name.lower()
        if current_type == "Armor":
            if "head" in name_lower: return "Head"
            if "hand" in name_lower: return "Hand"
            if "legs" in name_lower: return "Legs"
            if "shoes" in name_lower: return "Shoes"
            if "armor" in name_lower: return "Armor"
        if current_type == "Accessory":
            if "necklace" in name_lower: return "Necklace"
            if "bracer" in name_lower: return "Bracer"
            if "ring" in name_lower: return "Ring"
            if "seal" in name_lower: return "Seal"
            if "talisman" in name_lower or "amulet" in name_lower: return "Talisman"
        return current_type

    # Migrate Single items
    if "Single" in data:
        for name, item in data["Single"].items():
            if isinstance(item, dict) and "type" in item:
                old_type = item["type"]
                new_type = get_new_type(name, old_type)
                if new_type != old_type:
                    item["type"] = new_type

    # Migrate Sets items (though they are usually points, let's check)
    if "Sets" in data:
        for set_name, set_tiers in data["Sets"].items():
            for tier, stats in set_tiers.items():
                if isinstance(stats, dict) and "type" in stats:
                     # Sets usually don't have part-specific types, but let's be safe
                     pass

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

migrate_data('data.json')
migrate_data('web/public/data.json')
print("Migration completed.")
