import json

# Mapping for Set Counters (Chinese Stat Key -> English Set Name)
# This ensures that when an item gives a set point (e.g., "Black Feather": 1),
# the code (which looks for "Black Feather" in the status) can find it.
stat_mapping = {
    "黑羽": "Black Feather",
    "苦毒": "Venom",
    "诅咒": "Cursed",
    "闪鳞": "Glimmer",
    "蝶舞": "Butterfly",
    "恶欲": "Avarice",
    "魔心": "Demon Heart",
    "阳炎": "Solar",
    "圣辉": "Holy Glory",
    "魔影": "Demon Shadow",
    "新天空": "New Sky",
    "老天空": "Old Sky",

    # Stats
    "属强": "ENH",
    "暴击": "Crit Rate",
    "暴伤": "Crit DMG",
    "克制": "DMG to Debuff",
    "伤提": "DMG Bonus",
    "技伤": "Skill DMG",
    "共鸣伤": "DMG during Resonance",
    "属伤": "ENH DMG",
    "基础攻击": "Base ATK",
    "攻击加成": "ATK Bonus",
    "力量": "Strength",
    "敏捷": "Agility",
    "力量加成": "Str Bonus",
    "破防攻击": "PDEF Shred",
    "破防加成": "PDEF Shred Bonus",
    "穿透": "PEN",
    "附伤": "Bonus DMG",
    "防御降低": "Shield Break Eff",
    "倍率": "Skill Ratio",
    "技能伤害提升": "Skill DMG Boost",
    "冷却": "CD Rating",
    "职业增伤": "Class-Specific DMG Bonus",
    "技能加速": "Skill Haste",
    "特殊": "Special Stats",
    "共鸣效果I": "Resonance Effect I",
    "共鸣效果II": "Resonance Effect II",
    "特效占比": "Effect Ratio",
    "载具收藏": "Car Collection",

    # Engravings / Techniques Set Points
    "超然": "Transcendence",
    "适应": "Adaptation",
    "破坏": "Destruction",
    "迅捷": "Swiftness",
    "连续": "Combo",
    "攻势": "Offensive",
    "不凡": "Extraordinary",
    "淬火": "Tempering",
    "高阶": "High-Tier",
    "异常": "Status Break",
    "基本": "Basic",
    "穿刺": "Pierce",
    "攻坚": "Fortification",
    "卓越": "Excellence",
    "痛击": "Smite",
    "同盟": "Alliance",
    "不破": "Unbreakable",
    "属性": "Elem Master",
    "挑战": "Challenger",
    "共鸣": "Resonance",
    "回避": "Evasion",
    "耐力": "Elem Resist",
    "痊愈": "Recovery"
}

def update_json():
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Sort keys by length descending to avoid partial replacement (e.g. replacing 'Attack' inside 'Base Attack')
        sorted_mapping = sorted(stat_mapping.items(), key=lambda x: len(x[0]), reverse=True)
        # Replace the specific Chinese keys with English keys
        for cn_key, eng_key in sorted_mapping:
            # We replace "KEY": with "VALUE": to target the dictionary keys
            old_str = f'"{cn_key}":'
            new_str = f'"{eng_key}":'
            content = content.replace(old_str, new_str)
            
        with open('data.json', 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("Successfully updated data.json with English set keys.")
        
    except Exception as e:
        print(f"Error updating data.json: {e}")

if __name__ == "__main__":
    update_json()