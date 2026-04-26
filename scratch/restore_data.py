
import json
import os

def normalize_data(data):
    key_map = {
        "Base Atk": "Atk (flat)",
        "Atk": "Atk (flat)",
        "Multiplier": "Skill Ratio (%)",
        "Penetration": "PEN (flat)",
        "Str Bonus": "Strength Bonus (%)",
        "Strength Bonus": "Strength Bonus (%)",
        "Skill Haste": "ASPD (%)",
        "Dmg To Boss": "DMG to Boss (%)",
        "Crit Rate": "Crit Rate (%)",
        "Crit Dmg": "Crit Dmg (%)",
        "Skill DMG": "Skill DMG (%)",
        "Skill Dmg": "Skill DMG (%)",
        "Skill DMG Boost": "Skill DMG Boost (%)",
        "Dmg Bonus": "Dmg Bonus (%)",
        "Dmg Debuff": "Dmg Debuff (%)",
        "dmgToDebuff": "Dmg Debuff (%)",
        "Elem Boost": "Elem Boost (%)",
        "Elem Dmg": "Elem Dmg (%)",
        "Additional": "Additional (%)",
        "Special": "Special (%)",
        "Strength": "Strength (flat)",
        "Agility": "Agility (flat)",
        "Intelligence": "Intelligence (flat)",
        "Def Shred": "PDEF Shred (flat)",
        "Def Shred (flat)": "PDEF Shred (flat)",
        "PDEF Shred": "PDEF Shred (flat)",
        "Def Break Bonus": "Def Break Bonus (%)",
        "Def Reduction": "Def Reduction (%)",
        "Class Dmg": "Class DMG Bonus (%)",
        "Class DMG Bonus": "Class DMG Bonus (%)",
        "Cooldown Reduction": "Cooldown Reduction (%)",
        "Effect Ratio": "Effect Ratio (%)",
    }

    def rename_keys(obj):
        if isinstance(obj, dict):
            new_obj = {}
            for k, v in obj.items():
                new_key = key_map.get(k, k)
                # Also handle case variations and trailing spaces
                if k not in key_map:
                    clean_k = k.strip()
                    if clean_k in key_map:
                        new_key = key_map[clean_k]
                    elif clean_k.lower() in [m.lower() for m in key_map.keys()]:
                        # Match lowercase
                        for mk in key_map.keys():
                            if mk.lower() == clean_k.lower():
                                new_key = key_map[mk]
                                break
                
                new_obj[new_key] = rename_keys(v)
            return new_obj
        elif isinstance(obj, list):
            return [rename_keys(i) for i in obj]
        else:
            return obj

    return rename_keys(data)

def process_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    normalized = normalize_data(data)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(normalized, f, indent=2, ensure_ascii=False)
    print(f"Normalized {file_path}")

# Local data.json
process_file(r'c:\Users\UsEr\Desktop\Repository\COA-Calculator-Webapp\data.json')
# Public data.json (if exists)
process_file(r'c:\Users\UsEr\Desktop\Repository\COA-Calculator-Webapp\web\public\data.json')
