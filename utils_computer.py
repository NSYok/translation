# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'utils_computer.py'
# Bytecode version: 3.9.0beta5 (3425)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import math
def damage_compute(status_dict: dict):
    crit_multiplier = 1 + min(status_dict['Crit Rate'] / 100, 1) * status_dict['Crit Dmg'] / 100
    counter_multiplier = 1 + status_dict['Counter'] / 100   # damage debuff from UI input
    dmg_amp = 1 + status_dict['Dmg Amp'] / 100  # damage bonus from UI input
    skill_resonance = 1 + (status_dict['Skill Dmg'] + status_dict['Resonance Dmg'] * 0.9) / 100
    elem_dmg_multiplier = 1 + status_dict['Elem Dmg'] / 100 # elemental damage bonus from UI input
    # Note: 'Monster Def' comes from UI input
    attack = status_dict['Def Break Atk'] + status_dict['Atk'] * 3500 / (3500 + status_dict['Monster Def'])
    extra_dmg = 1 + status_dict['Extra Dmg'] / 100
    special = 1 + status_dict['Special'] / 100
    class_dmg = 1.08 + status_dict['Class Dmg'] / 100
    multiplier = 1 + status_dict['Multiplier'] / 100
    skill_dmg_boost = 1 + status_dict['Skill Dmg Boost'] / 100
    skill_haste = 1 + status_dict['Skill Haste'] / 100
    # Note: 'Cooldown Reduction' corresponds to 'Cooldown' in base_status
    cooldown_reduction = 1 / (1 - status_dict['Cooldown Reduction'] / 100)
    effect_ratio = 1 + status_dict['Effect Ratio'] / (100 - status_dict['Effect Ratio'])
    burst_damage = crit_multiplier * counter_multiplier * dmg_amp * skill_resonance * elem_dmg_multiplier * attack * extra_dmg * special * class_dmg * multiplier * skill_dmg_boost * effect_ratio
    return (burst_damage, burst_damage * skill_haste * cooldown_reduction)
def add_equipment(status_dict: dict, equipment: dict):
    for key in equipment.keys():
        if key not in status_dict.keys():
            status_dict[key] = equipment[key]
        else:
            status_dict[key] = status_dict[key] + equipment[key]
    return status_dict
def remove_equipment(status_dict: dict, equipment: dict):
    for key in equipment.keys():
        if key not in status_dict.keys():
            status_dict[key] = equipment[key]
        else:
            status_dict[key] = status_dict[key] - equipment[key]
    return status_dict
def outfit_count(status: dict, outfit_dict: dict):
    outfits = []
    for outfit_name in outfit_dict.keys():
        if outfit_name in status.keys():
            for num in outfit_dict[outfit_name].keys():
                if status[outfit_name] >= int(num):
                    outfits.append((outfit_name, num))
    if ('Black Feather', '2') in outfits:
        if ('Avarice', '2') in outfits:
            outfits.remove(('Black Feather', '2'))
    if ('Black Feather', '2') in outfits:
        if ('Glimmer', '2') in outfits:
            outfits.remove(('Black Feather', '2'))
    if ('Black Feather', '2') in outfits:
        if ('Venom', '2') in outfits:
            outfits.remove(('Black Feather', '2'))
    if ('Black Feather', '3') in outfits:
        if ('Avarice', '3') in outfits:
            outfits.remove(('Black Feather', '3'))
    if ('Black Feather', '3') in outfits:
        if ('Glimmer', '3') in outfits:
            outfits.remove(('Black Feather', '3'))
    if ('Black Feather', '3') in outfits and ('Venom', '3') in outfits:
            outfits.remove(('Black Feather', '3'))
    if ('Black Feather', '5') in outfits:
        if ('Avarice', '5') in outfits:
            outfits.remove(('Black Feather', '5'))
    if ('Black Feather', '5') in outfits:
        if ('Glimmer', '5') in outfits:
            outfits.remove(('Black Feather', '5'))
    if ('Black Feather', '5') in outfits:
        if ('Venom', '5') in outfits:
            outfits.remove(('Black Feather', '5'))
    if ('Demon Heart', '2') in outfits:
        if ('Avarice', '2') in outfits:
            outfits.remove(('Avarice', '2'))
    if ('Butterfly', '2') in outfits:
        if ('Glimmer', '2') in outfits:
            outfits.remove(('Glimmer', '2'))
    if ('Cursed', '2') in outfits:
        if ('Venom', '2') in outfits:
            outfits.remove(('Venom', '2'))
    if ('Demon Heart', '3') in outfits:
        if ('Avarice', '3') in outfits:
            outfits.remove(('Avarice', '3'))
    if ('Butterfly', '3') in outfits:
        if ('Glimmer', '3') in outfits:
            outfits.remove(('Glimmer', '3'))
    if ('Cursed', '3') in outfits and ('Venom', '3') in outfits:
            outfits.remove(('Venom', '3'))
    if ('Demon Heart', '5') in outfits and ('Avarice', '5') in outfits:
            outfits.remove(('Avarice', '5'))
    if ('Butterfly', '5') in outfits and ('Glimmer', '5') in outfits:
            outfits.remove(('Glimmer', '5'))
    if ('Cursed', '5') in outfits and ('Venom', '5') in outfits:
            outfits.remove(('Venom', '5'))
    if ('Old Sky', '2') in outfits and ('New Sky', '2') in outfits:
            outfits.remove(('Old Sky', '2'))
    if ('Old Sky', '3') in outfits and ('New Sky', '3') in outfits:
            outfits.remove(('Old Sky', '3'))
    if ('Old Sky', '5') in outfits and ('New Sky', '5') in outfits:
            outfits.remove(('Old Sky', '5'))
    return outfits