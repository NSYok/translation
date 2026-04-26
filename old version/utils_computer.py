from typing import Any

def damage_compute(status_dict: dict[str, Any]) -> tuple[float, float]:
    crit_multiplier = 1 + min(status_dict['Crit Rate'] / 100, 1) * (status_dict['Crit Dmg'] / 100)
    dmg_to_debuff_multiplier = 1 + status_dict['dmgToDebuff'] / 100
    dmg_to_boss_multiplier = 1 + status_dict.get('Boss Dmg', 0) / 100
    dmg_amp = 1 + status_dict['Dmg Amp'] / 100
    
    skill_resonance = 1 + (status_dict['Skill Dmg'] + status_dict['Resonance Dmg']) / 100
    elem_dmg_multiplier = 1 + status_dict['Elem Dmg'] / 100
    
    # --- Fixed Defense Formula (matching game mechanics) ---
    # Damage Reduction % = Defense / (3000 + Defense)
    # Where Defense = Monster Def * (1 - Physical PEN%)
    # Def Reduction = Physical PEN%
    # Def Break Atk = PDEF Shred (flat)
    # Penetration = Additional flat defense reduction
    def_after_pen = status_dict['Monster Def'] * (1 - status_dict.get('Def Reduction', 0) / 100) - status_dict.get('Penetration', 0)
    def_after_pen = max(0, def_after_pen)  # Prevent negative
    dmg_reduction_pct = def_after_pen / (3000 + def_after_pen)
    
    # Actual Attack = Total PATK * (1 - Damage Reduction %) + PDEF Shred
    # PDEF Shred = Def Break Atk
    # Total PATK = Base Atk * (1 + STR Increase %) * (1 + PATK%) (From guide)
    # But wait, utils_computer.py uses status_dict['Atk'] which is already computed outside damage_compute?
    attack_zone = status_dict['Atk'] * (1 - dmg_reduction_pct) + status_dict.get('Def Break Atk', 0)
    
    extra_dmg = 1 + status_dict['Extra Dmg'] / 100
    special = 1 + status_dict['Special'] / 100
    
    class_dmg = 1 + status_dict['Class Dmg'] / 100 
    
    multiplier = 1 + status_dict['Multiplier'] / 100
    skill_dmg_boost = 1 + status_dict['Skill Dmg Boost'] / 100
    # ... (existing code) ...

    # Skill Haste Note:
    # 'Skill Haste' is a proxy for DPS increase from complex flat Cooldown Reduction (CDR) mechanics.
    # These values (e.g., for Destruction engraving) are pre-calculated "magic numbers".
    #
    # How they are calculated (Reverse Engineered Example for Destruction Lv. 7):
    # Effect: "Reduce Finisher CD by 0.5s every 2s." -> Mapped to "Skill Haste: 5.6"
    #
    # 1. Assumptions:
    #    - Finisher Base Cooldown: 60s
    #    - Finisher's share of total damage: ~17%
    #
    # 2. Calculate Effective Cooldown:
    #    - Over 60s, the effect triggers 60 / 2 = 30 times.
    #    - Total flat reduction = 30 * 0.5s = 15s.
    #    - New Effective Cooldown = 60s - 15s = 45s.
    #
    # 3. Calculate DPS Gain:
    #    - The skill can be used (60 / 45) = 1.333 times more often, a ~33.3% frequency increase.
    #
    # 4. Convert to Equivalent Skill Haste:
    #    - Equivalent Haste % = (Frequency Increase) * (Skill's Damage Share)
    #    - Equivalent Haste % = 33.3% * 17% ~= 5.66%
    #    - This is why data.json has {"Skill Haste": 5.6} for this effect.
    #
    # The same logic applies to other levels:
    # - Lv 4 (1.8): For a normal skill with a smaller damage share.
    # - Lv 9 (5.6): Adds another 0.5s reduction to the Finisher, so it adds another 5.6%.
    skill_haste = 1 + status_dict['Skill Haste'] / 100
    cooldown_reduction = 1 / (1 - status_dict['Cooldown Reduction'] / 100)
    effect_ratio = 1 + status_dict['Effect Ratio'] / (100 - status_dict['Effect Ratio'])
    
    burst_damage = crit_multiplier * dmg_to_debuff_multiplier * dmg_to_boss_multiplier * dmg_amp * skill_resonance * elem_dmg_multiplier * attack_zone * extra_dmg * special * class_dmg * multiplier * skill_dmg_boost * effect_ratio
    
    return (burst_damage, burst_damage * skill_haste * cooldown_reduction)
def add_equipment(status_dict: dict[str, Any], equipment: dict[str, Any]) -> dict[str, Any]:
    for key in equipment.keys():
        if key.lower() == 'type' or key == '_category': continue
        if key not in status_dict.keys():
            status_dict[key] = equipment[key]
        else:
            status_dict[key] = status_dict[key] + equipment[key]
    return status_dict

def remove_equipment(status_dict: dict[str, Any], equipment: dict[str, Any]) -> dict[str, Any]:
    for key in equipment.keys():
        if key.lower() == 'type' or key == '_category': continue
        if key not in status_dict.keys():
            status_dict[key] = equipment[key]
        else:
            status_dict[key] = status_dict[key] - equipment[key]
    return status_dict

def outfit_count(status: dict[str, Any], outfit_dict: dict[str, Any]) -> list[tuple[str, str]]:
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
