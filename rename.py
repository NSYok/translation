import os

# ชื่อโฟลเดอร์ที่เก็บรูป (ต้องวางไฟล์นี้ไว้ข้างๆ โฟลเดอร์ icon)
icon_folder = 'icon'

# พจนานุกรมแปลชื่อไฟล์ (จีน -> อังกฤษ)
# สร้างจาก List ไฟล์ที่คุณให้มาโดยเฉพาะ
mapping = {
    # --- Enhancements (เปลี่ยน + เป็น Plus เพื่อความชัวร์ หรือคงเดิมก็ได้ แต่ห้ามมี /) ---
    '+15(力智)': '+15(Str_Int)',
    '+15(左右槽)': '+15(L_R Slot)',
    '+15(武器)': '+15(Weapon)',
    '+15(生命)': '+15(HP)',
    '+16(力智)': '+16(Str_Int)',
    '+16(左右槽)': '+16(L_R Slot)',
    '+16(武器)': '+16(Weapon)',
    '+16(生命)': '+16(HP)',
    '+17(力智)': '+17(Str_Int)',
    '+17(左右槽)': '+17(L_R Slot)',
    '+17(武器)': '+17(Weapon)',
    '+17(生命)': '+17(HP)',
    '+18(力智)': '+18(Str_Int)',
    '+18(左右槽)': '+18(L_R Slot)',
    '+18(武器)': '+18(Weapon)',
    '+18(生命)': '+18(HP)',
    '+19(力智)': '+19(Str_Int)',
    '+19(左右槽)': '+19(L_R Slot)',
    '+19(武器)': '+19(Weapon)',
    '+19(生命)': '+19(HP)',
    '+20(力智)': '+20(Str_Int)',
    '+20(左右槽)': '+20(L_R Slot)',
    '+20(武器)': '+20(Weapon)',
    '+20(生命)': '+20(HP)',
    '+21(力智)': '+21(Str_Int)',
    '+21(左右槽)': '+21(L_R Slot)',
    '+21(武器)': '+21(Weapon)',
    '+21(生命)': '+21(HP)',
    '+22(力智)': '+22(Str_Int)',
    '+22(左右槽)': '+22(L_R Slot)',
    '+22(武器)': '+22(Weapon)',
    '+22(生命)': '+22(HP)',
    '+23(力智)': '+23(Str_Int)',
    '+23(左右槽)': '+23(L_R Slot)',
    '+23(武器)': '+23(Weapon)',
    '+23(生命)': '+23(HP)',
    '+24(力智)': '+24(Str_Int)',
    '+24(左右槽)': '+24(L_R Slot)',
    '+24(武器)': '+24(Weapon)',
    '+24(生命)': '+24(HP)',
    '+25(力智)': '+25(Str_Int)',
    '+25(左右槽)': '+25(L_R Slot)',
    '+25(武器)': '+25(Weapon)',
    '+25(生命)': '+25(HP)',

    # --- Buffs & Potions ---
    '10爆伤': '10 Crit Dmg',
    '1星': '1 Star',
    '22属强药': '22 Elem Potion',
    '25属强药': '25 Elem Potion',
    '2星': '2 Star',
    '3星': '3 Star',
    '6克制': '6 Counter',
    '8技伤': '8 Skill Dmg',
    '8攻击': '8 Atk',
    '8暴击': '8 Crit',
    '清晨': 'Morning',
    '悬崖': 'Cliff',
    '东方': 'East',
    '龙息': 'Dragon Breath',
    '疾风': 'Gale',
    '矿战': 'Mine War',
    '克制': 'Counter',

    # --- Equipment Sets ---
    # Black Feather (Heiyu)
    '黑羽头': 'Black Feather Head',
    '黑羽胸': 'Black Feather Armor',
    '黑羽手': 'Black Feather Hand',
    '黑羽裤': 'Black Feather Legs',
    '黑羽鞋': 'Black Feather Shoes',
    
    # Glimmer (Shanlin)
    '闪鳞头': 'Glimmer Head',
    '闪鳞胸': 'Glimmer Armor',
    '闪鳞手': 'Glimmer Hand',
    '闪鳞裤': 'Glimmer Legs',
    '闪鳞鞋': 'Glimmer Shoes',
    '闪鳞毒翼': 'Glimmer Venom Wing', # Emblem

    # Venom (Kudu)
    '苦毒头': 'Venom Head',
    '苦毒胸': 'Venom Armor',
    '苦毒手': 'Venom Hand',
    '苦毒裤': 'Venom Legs',
    '苦毒鞋': 'Venom Shoes',
    '苦毒巨兽': 'Venom Behemoth', # Emblem

    # Avarice (Eyu)
    '恶欲头': 'Avarice Head',
    '恶欲胸': 'Avarice Armor',
    '恶欲手': 'Avarice Hand',
    '恶欲裤': 'Avarice Legs',
    '恶欲鞋': 'Avarice Shoes',

    # Butterfly (Diewu)
    '蝶舞头': 'Butterfly Head',
    '蝶舞胸': 'Butterfly Armor',
    '蝶舞手': 'Butterfly Hand',
    '蝶舞裤': 'Butterfly Legs',
    '蝶舞鞋': 'Butterfly Shoes',

    # Demon Heart (Moxin)
    '魔心头': 'Demon Heart Head',
    '魔心胸': 'Demon Heart Armor',
    '魔心手': 'Demon Heart Hand',
    '魔心裤': 'Demon Heart Legs',
    '魔心鞋': 'Demon Heart Shoes',
    '魔心克拉肯': 'Demon Heart Kraken', # Emblem

    # Cursed (Zuzhou)
    '诅咒头': 'Cursed Head',
    '诅咒胸': 'Cursed Armor',
    '诅咒手': 'Cursed Hand',
    '诅咒裤': 'Cursed Legs',
    '诅咒鞋': 'Cursed Shoes',

    # --- Accessories ---
    # Solar (Yangyan)
    '阳炎项链': 'Solar Necklace',
    '阳炎腕带': 'Solar Bracer',
    '阳炎戒指': 'Solar Ring',
    '阳炎印章': 'Solar Seal',
    '阳炎护符': 'Solar Amulet',

    # Holy Glory (Shenghui)
    '圣辉项链': 'Holy Glory Necklace',
    '圣辉腕带': 'Holy Glory Bracer',
    '圣辉戒指': 'Holy Glory Ring',
    '圣辉印章': 'Holy Glory Seal',
    '圣辉护符': 'Holy Glory Amulet',

    # Demon Shadow (Moying)
    '魔影项链': 'Demon Shadow Necklace',
    '魔影腕带': 'Demon Shadow Bracer',
    '魔影戒指': 'Demon Shadow Ring',
    '魔影印章': 'Demon Shadow Seal',
    '魔影护符': 'Demon Shadow Amulet',
    '末影项链': 'Ender Necklace', # Likely unique/typo in source, mapped safely

    # --- Weapons ---
    '真逆命镰干涸': 'True Fate Sickle (Withered)',
    '渊影之垂眸': 'Abyssal Gaze',
    '绝念梦谣': 'Desperate Dream Song',
    'S级时装武器': 'S-Rank Fashion Weapon',
    '烈阳敕赐之座': 'Sun Decree Seat',

    # --- Emblems ---
    '属强徽记': 'Elem Mark',
    '芭蓓娜': 'Verbena',
    '霍克': 'Hawk',
    '虚空龙': 'Void Dragon',
    '黑蚀缔造者': 'Eclipse Creator',
    '士兵': 'Soldier',
    '人马': 'Centaur',
    '主教': 'Bishop',
    '战车': 'Chariot',
    '国王': 'King',
    '女王': 'Queen',
    '普拉格': 'Plague',
    '法米恩': 'Famion',
    '阿泽瑞尔': 'Azrael',
    '马尔斯': 'Mars',
    '米迦勒': 'Michael',
    '斯库尔': 'Skull',
    '波吉特': 'Bogit',
    '夏洛特': 'Charlotte',
    '强欲之触': 'Touch of Greed',
    '冰拳（维克）': 'Ice Fist (Vic)',
    '电鞭（Joker）': 'Electric Whip (Joker)',
    '哥拉莫斯': 'Goramos',
    '安德烈': 'Andre',
    '发条': 'Clockwork',
    '雷光': 'Thunder Light',
    '重盾': 'Heavy Shield',
    '艾萨克': 'Isaac',
    '奥荻莎': 'Odisha',
    '戈尔珈': 'Gorga',
    '迷局': 'Puzzle',
    '权剑': 'Sword of Power',
    
    # --- Techniques (Engravings) ---
    '超然技法1': 'Transcendence 1',
    '超然技法2': 'Transcendence 2',
    '超然技法3': 'Transcendence 3',
    '适应技法1': 'Adaptation 1',
    '适应技法2': 'Adaptation 2',
    '适应技法3': 'Adaptation 3',
    '破坏1': 'Destruction 1',
    '破坏2': 'Destruction 2',
    '破坏3': 'Destruction 3',
    '攻势1': 'Offensive 1',
    '攻势2': 'Offensive 2',
    '攻势3': 'Offensive 3',
    '迅捷1': 'Swiftness 1',
    '迅捷2': 'Swiftness 2',
    '迅捷3': 'Swiftness 3',
    '连续击1': 'Combo 1',
    '连续击2': 'Combo 2',
    '连续击3': 'Combo 3',
    '不凡技法1': 'Extraordinary 1',
    '不凡技法2': 'Extraordinary 2',
    '不凡技法3': 'Extraordinary 3',
    '淬火1': 'Tempering 1',
    '淬火2': 'Tempering 2',
    '淬火3': 'Tempering 3',
    '高阶技巧1': 'High-Tier 1',
    '高阶技巧2': 'High-Tier 2',
    '高阶技巧3': 'High-Tier 3',
    '异常击破1': 'Status Break 1',
    '异常击破2': 'Status Break 2',
    '异常击破3': 'Status Break 3',
    '基本功1': 'Basic 1',
    '基本功2': 'Basic 2',
    '基本功3': 'Basic 3',
    '穿刺术1': 'Pierce 1',
    '穿刺术2': 'Pierce 2',
    '穿刺术3': 'Pierce 3',
    '攻坚1': 'Fortification 1',
    '攻坚2': 'Fortification 2',
    '攻坚3': 'Fortification 3',
    '卓越技法1': 'Excellence 1',
    '卓越技法2': 'Excellence 2',
    '卓越技法3': 'Excellence 3',
    '痛击1': 'Smite 1',
    '痛击2': 'Smite 2',
    '痛击3': 'Smite 3',
    '同盟1': 'Alliance 1',
    '同盟2': 'Alliance 2',
    '同盟3': 'Alliance 3',
    '不破之身1': 'Unbreakable 1',
    '不破之身2': 'Unbreakable 2',
    '不破之身3': 'Unbreakable 3',
    '属性大师1': 'Elem Master 1',
    '属性大师2': 'Elem Master 2',
    '属性大师3': 'Elem Master 3',
    '挑战者1': 'Challenger 1',
    '挑战者2': 'Challenger 2',
    '挑战者3': 'Challenger 3',
    '共鸣1': 'Resonance 1',
    '共鸣2': 'Resonance 2',
    '共鸣3': 'Resonance 3',
    '回避1': 'Evasion 1',
    '回避2': 'Evasion 2',
    '回避3': 'Evasion 3',
    '元素耐力1': 'Elem Resist 1',
    '元素耐力2': 'Elem Resist 2',
    '元素耐力3': 'Elem Resist 3',
    '痊愈1': 'Recovery 1',
    '痊愈2': 'Recovery 2',
    '痊愈3': 'Recovery 3',
    '破壁1': 'Wall Breaker 1', # Extra item
    '破壁2': 'Wall Breaker 2',
    '破壁3': 'Wall Breaker 3',
    '劣化灾变': 'Degenerate Cataclysm',

    # --- Pets & Cards ---
    '猫': 'Cat',
    '鹰': 'Eagle',
    '熊猫': 'Panda',
    '龙': 'Dragon',
    '漂漂': 'PiaoPiao',
    '科托': 'Koto',
    '狐狸': 'Fox',
    '灵喵爪印': 'Cat Paw',
    '帝王荆棘': 'Emperor Thorn',
    '洞察之眼': 'Insight Eye',
    '魔道巫灵': 'Magic Witch',
    '兽齿之印': 'Beast Tooth Mark',
    '凛风蝶舞': 'Wind Butterfly',
    '枫落之咒': 'Maple Curse',
    '忠实好伙伴': 'Loyal Partner',
    '虚空的灾影': 'Void Shadow',
    '克罗姆军工': 'Chrome Arms',
    '远古守护者': 'Ancient Guardian',
    '深空之虫潮': 'Deep Space Swarm',
    '秘境生灵': 'Realm Creature',
    '魔导纪元': 'Magic Era',
    '黑域狂徒': 'Dark Realm Madman',
    '逐光行者': 'Light Chaser',
    '发条军团': 'Clockwork Legion',
    '机械帝国': 'Mech Empire',
    '野兽军团': 'Beast Legion',
    '幽暗禁域': 'Gloomy Forbidden Area',
    '游园护卫队': 'Park Guard',
    '怪奇马戏团': 'Weird Circus',

    # --- Fashion / Titles / Misc ---
    '恶魔之触': 'Demon Touch',
    '虚空华冕': 'Void Crown',
    '金冕之尊': 'Gold Crown',
    '黄金梦乡': 'Golden Slumber',
    '暗蚀之界': 'Eclipse Realm',
    '暗蚀之界II': 'Eclipse Realm II',
    '熠熠星罗': 'Shining Star',
    '璀璨星流': 'Shining Star Footmark',
    '新天空头饰': 'New Sky Head',
    '新天空徽章': 'New Sky Badge',
    '新天空服装': 'New Sky Armor',
    '新天空配饰': 'New Sky Accessory',
    '新天空面饰': 'New Sky Facewear',
    '老天空头饰': 'Old Sky Head',
    '老天空徽章': 'Old Sky Badge',
    '老天空服装': 'Old Sky Armor',
    '老天空配饰': 'Old Sky Accessory',
    '老天空面饰': 'Old Sky Facewear',
    '魔镰徽记': 'Demon Sickle Emblem',
    '热浪称号徽记': 'Heat Wave Title Emblem',
    '鸣金称号徽记': 'Mingjin Title Emblem',
    '鸣金武器徽记': 'Mingjin Weapon Emblem',
    '鸣金光环徽记': 'Mingjin Aura Emblem',
    '星神光环徽记': 'Star God Aura Emblem',
    '鸣金服装徽记': 'Mingjin Armor Emblem',
    '鸣金配饰徽记': 'Mingjin Accessory Emblem',
    '鸣金头饰徽记': 'Mingjin Head Emblem',
    '鸣金足迹徽记': 'Mingjin Footmark Emblem',
    '世界终焉的沙漏': "Hourglass of World's End",
    '旧日魔神的咏歌': 'Hymn of Ancient Demon God',
    '无': 'None',
    'icon': 'icon' # กันพลาดถ้ามีไฟล์ชื่อ icon.png
}

def rename_files():
    if not os.path.exists(icon_folder):
        print(f"Error: Folder '{icon_folder}' not found!")
        return

    count = 0
    # วนลูปไฟล์ทั้งหมดในโฟลเดอร์ icon
    for filename in os.listdir(icon_folder):
        if not filename.endswith('.png'):
            continue
            
        # แยกชื่อไฟล์ (จีน) กับ นามสกุล (.png)
        chinese_name = os.path.splitext(filename)[0]
        
        # เช็คว่าชื่อจีนนี้ มีคำแปลใน Dictionary ไหม
        if chinese_name in mapping:
            english_name = mapping[chinese_name]
            
            # ตรวจสอบว่าชื่อใหม่เหมือนชื่อเก่าไหม (เช่น 'icon' -> 'icon')
            if chinese_name == english_name:
                continue

            # สร้าง path เต็ม
            old_path = os.path.join(icon_folder, filename)
            new_path = os.path.join(icon_folder, english_name + '.png')
            
            try:
                # ถ้าไฟล์ปลายทางมีอยู่แล้ว ให้ลบก่อน (กัน Error)
                if os.path.exists(new_path):
                    os.remove(new_path)
                    
                os.rename(old_path, new_path)
                print(f"[OK] Renamed: {filename} -> {english_name}.png")
                count += 1
            except Exception as e:
                print(f"[Error] Could not rename {filename}: {e}")
        else:
            print(f"[Skip] No translation found for: {filename}")

    print(f"\n--- Summary: Renamed {count} files ---")

if __name__ == '__main__':
    rename_files()