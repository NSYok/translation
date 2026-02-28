import streamlit as st
import json
import math
import sys
import os

# Import functions from utils_computer.py
try:
    from utils_computer import damage_compute, add_equipment, outfit_count
except ImportError:
    st.error("Could not find `utils_computer.py`. Please ensure the file is in the same directory.")
    st.stop()

# --- Page Config and Data Loading ---
st.set_page_config(page_title="Crystal Core Calculator", layout="wide")

@st.cache_data
def load_data():
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Could not find `data.json`. Please ensure the file is in the same directory.")
        return {"Single": {}, "Sets": {}}

data = load_data()

# --- Calculation Core (Ported from calculator_COA70.py) ---
def run_calculation(equipment_list, manual_inputs):
    """
    This function replicates the exact calculation logic from the `compute_damage`
    method in the original calculator_COA70.py file.
    """
    # 1. Initialize base_status with the same defaults
    base_status = {
        'Elem Boost': 0, 'Crit Rate': 0, 'Crit Dmg': 56, 'Counter': 0, 'Dmg Amp': 3,
        'Skill Dmg': 0, 'Resonance Dmg': 20, 'Elem Dmg': 0, 'Base Atk': 201,
        'Atk Bonus': 0, 'Strength': 685, 'Agility': 445, 'Str Bonus': 0,
        'Def Break Atk': 0, 'Def Break Bonus': 0, 'Penetration': 0, 'Extra Dmg': 0,
        'Def Reduction': 0, 'Monster Def': manual_inputs['monster_def'], 'Multiplier': 0,
        'Skill Dmg Boost': 0, 'Cooldown': 61.8, 'Class Dmg': 28.8,
        'Skill Haste': 0, 'Special': 0
    }

    # 2. Add stats from all selected equipment
    for equip_name in equipment_list:
        if equip_name and equip_name != 'None' and equip_name in data['Single']:
            add_equipment(base_status, data['Single'][equip_name])

    # 3. Apply manual stat adjustments from UI
    base_status['Effect Ratio'] = manual_inputs['dot_ratio']
    base_status['Base Atk'] += manual_inputs['man_atk']
    base_status['Crit Dmg'] += manual_inputs['man_crit_dmg']
    base_status['Crit Rate'] += manual_inputs['man_crit_rate']
    base_status['Elem Boost'] += manual_inputs['man_elem']
    base_status['Cooldown'] += manual_inputs['man_cd']
    base_status['Agility'] += manual_inputs['man_agi']
    base_status['Strength'] += manual_inputs['man_str']
    base_status['Skill Dmg'] += manual_inputs['man_skill_dmg']
    base_status['Atk Bonus'] += manual_inputs['man_atk_bonus']
    base_status['Car Collection'] = manual_inputs['man_car']

    # 4. Handle set bonuses using the original outfit_count function
    outfits = outfit_count(base_status, outfit_dict=data['Sets'])
    special_boost = 1

    # 5. Apply set bonuses and special tech boosts
    for outfit in outfits:
        set_name, count = outfit
        key = set_name + count

        # Check for special tech boosts that override normal set bonuses
        if key == 'Extraordinary4' and manual_inputs['boost_bufan4'] > 0:
            special_boost *= 1 + manual_inputs['boost_bufan4'] / 100
        elif key == 'Extraordinary6' and manual_inputs['boost_bufan6'] > 0:
            special_boost *= 1 + manual_inputs['boost_bufan6'] / 100
        elif key == 'Excellence4' and manual_inputs['boost_zhuoyue4'] > 0:
            special_boost *= 1 + manual_inputs['boost_zhuoyue4'] / 100
        elif key == 'Excellence7' and manual_inputs['boost_zhuoyue7'] > 0:
            special_boost *= 1 + manual_inputs['boost_zhuoyue7'] / 100
        elif key == 'Excellence9' and manual_inputs['boost_zhuoyue9'] > 0:
            special_boost *= 1 + manual_inputs['boost_zhuoyue9'] / 100
        elif key == 'Transcendence9' and manual_inputs['boost_chaoran9'] > 0:
            special_boost *= 1 + manual_inputs['boost_chaoran9'] / 100
        else:
            # Apply normal set bonus
            if set_name in data['Sets'] and count in data['Sets'][set_name]:
                add_equipment(base_status, data['Sets'][set_name][count])

    # 6. Apply special item/set interactions
    if 'Avarice Shoes' in equipment_list:
        base_status['Crit Dmg'] += 3 * base_status.get('Avarice', 0)
    elif 'Demon Heart Shoes' in equipment_list:
        base_status['Crit Dmg'] += 4 * base_status.get('Avarice', 0)

    if ('Venom', '2') in outfits:
        extra_kezhi = min(4 * base_status.get('Venom', 0), 16)
        base_status['Counter'] += extra_kezhi
    elif ('Cursed', '2') in outfits:
        extra_kezhi = min(4 * base_status.get('Venom', 0) + base_status.get('Cursed', 0), 22)
        base_status['Counter'] += extra_kezhi

    # 7. Calculate derived stats and create the final_status dictionary
    cdr_percentage = (base_status['Cooldown'] / (base_status['Cooldown'] + 1133)) * 100

    final_status = {
        'Elem Boost': base_status['Elem Boost'],
        'Crit Rate': base_status['Crit Rate'] - 7e-07 * base_status['Agility'] + 0.0125 * base_status['Agility'] + 0.3034,
        'Crit Dmg': base_status['Crit Dmg'],
        'Counter': base_status['Counter'],
        'Dmg Amp': base_status['Dmg Amp'],
        'Skill Dmg': base_status['Skill Dmg'],
        'Resonance Dmg': base_status['Resonance Dmg'],
        'Elem Dmg': base_status.get('Elem Dmg', 0) + base_status['Elem Boost'] / 2.2,
        'Def Break Atk': base_status['Def Break Atk'] * (1 + base_status.get('Def Break Bonus', 0) / 100),
        'Atk': (base_status['Base Atk'] + base_status['Strength'] * 2.5) * (1 + base_status['Atk Bonus'] / 100),
        'Monster Def': base_status['Monster Def'],
        'Penetration': base_status['Penetration'],
        'Def Reduction': base_status.get('Def Reduction', 0),
        'Extra Dmg': base_status['Extra Dmg'],
        'Special': base_status['Special'],
        'Class Dmg': base_status['Class Dmg'],
        'Multiplier': base_status.get('Multiplier', 0),
        'Skill Dmg Boost': base_status.get('Skill Dmg Boost', 0),
        'Skill Haste': base_status.get('Skill Haste', 0),
        'Cooldown Reduction': cdr_percentage,
        'Effect Ratio': base_status.get('Effect Ratio', 0),
        'Def Shred': base_status.get('Def Reduction', 0) # For UI display consistency
    }

    # 8. Final damage computation using the imported function
    burst_damage, total_damage = damage_compute(final_status)

    # Apply the special tech boost at the end
    burst_damage *= special_boost
    total_damage *= special_boost

    return final_status, burst_damage, total_damage

# --- UI Definition (Sidebar) ---
st.title("Crystal Core Panel Calculator (Web App)")

input_col, result_col = st.columns([2, 1])

with input_col:
    st.header("Build Configuration")

    # Helper to display selectbox with icon
    def icon_selector(label, options, default, key, omit_trait=None):
        # Initialize session state for this key if not exists
        if key not in st.session_state:
            st.session_state[key] = default
        
        current_val = st.session_state[key]
        
        c1, c2 = st.columns([1, 3])
        
        with c1:
            # Show current selection icon
            icon_path = os.path.join("icon", f"{current_val}.png")
            if os.path.exists(icon_path):
                st.image(icon_path, use_container_width=True)
            else:
                st.markdown("<div style='height:60px; display:flex; align-items:center; justify-content:center; background:#f0f0f0; border-radius:5px;'>No Icon</div>", unsafe_allow_html=True)
        
        with c2:
            # Shorten display text
            display_val = current_val
            if omit_trait and current_val.endswith(omit_trait):
                display_val = current_val[:-len(omit_trait)].strip()

            # Expander for selection
            with st.expander(display_val):
                # Create a grid for options
                cols = st.columns(3) # 3 items per row inside expander
                for i, option in enumerate(options):
                    col = cols[i % 3]
                    with col:
                        icon_path = os.path.join("icon", f"{option}.png")
                        if os.path.exists(icon_path):
                            st.image(icon_path, use_container_width=True)
                        
                        btn_text = option
                        if omit_trait and option.endswith(omit_trait):
                            btn_text = option[:-len(omit_trait)].strip()
                        
                        st.markdown(f"<div style='text-align: center; font-size: 0.7em; margin-bottom: 2px; line-height:1.1;'>{btn_text}</div>", unsafe_allow_html=True)
                        
                        if st.session_state[key] == option:
                            st.button("✅", key=f"btn_{key}_{i}", disabled=True, use_container_width=True)
                        else:
                            if st.button("Select", key=f"btn_{key}_{i}", use_container_width=True):
                                st.session_state[key] = option
                                st.rerun()
            
        return st.session_state[key]
    
    # Helper for simple index retrieval (for non-icon fields)
    def get_index(options, value):
        if value in options:
            return options.index(value)
        return 0

    # Define Options from calculator_COA70.py
    opts_armor_set = ['Black Feather', 'Glimmer', 'Avarice', 'Venom', 'Butterfly', 'Demon Heart', 'Cursed', 'None']
    opts_acc_set = ['Solar', 'Holy Glory', 'Demon Shadow', 'None']
    opts_weapon = ['True Fate Sickle (Withered)', 'Abyssal Gaze', 'Desperate Dream Song', 'None']
    enh_opts_str = [f'+{i}(Str_Int)' for i in range(15, 26)] + ['None']
    enh_opts_hp = [f'+{i}(HP)' for i in range(15, 26)] + ['None']
    enh_opts_wep = [f'+{i}(Weapon)' for i in range(18, 26)] + ['None']
    enh_opts_lr = [f'+{i}(L_R Slot)' for i in range(15, 26)] + ['None']
    engrave_transcendence = ['Transcendence 3', 'Adaptation 3', 'Destruction 3', 'Swiftness 3', 'Combo 3', 'Transcendence 2', 'Adaptation 2', 'Destruction 2', 'Swiftness 2', 'Combo 2', 'Transcendence 1', 'Adaptation 1', 'Destruction 1', 'Swiftness 1', 'Combo 1', 'None']
    engrave_extraordinary = ['Extraordinary 3', 'Tempering 3', 'High-Tier 3', 'Status Break 3', 'Basic 3', 'Pierce 3', 'Fortification 3', 'Extraordinary 2', 'Tempering 2', 'High-Tier 2', 'Status Break 2', 'Basic 2', 'Pierce 2', 'Fortification 2', 'Extraordinary 1', 'Tempering 1', 'High-Tier 1', 'Status Break 1', 'Basic 1', 'Pierce 1', 'Fortification 1', 'None']
    engrave_excellence = ['Excellence 3', 'Smite 3', 'Alliance 3', 'Unbreakable 3', 'Excellence 2', 'Smite 2', 'Alliance 2', 'Unbreakable 2', 'Excellence 1', 'Smite 1', 'Alliance 1', 'Unbreakable 1', 'None']
    engrave_elem_master = ['Elem Master 3', 'Challenger 3', 'Resonance 3', 'Evasion 3', 'Elem Resist 3', 'Recovery 3', 'Elem Master 2', 'Challenger 2', 'Resonance 2', 'Evasion 2', 'Elem Resist 2', 'Recovery 2', 'Elem Master 1', 'Challenger 1', 'Resonance 1', 'Evasion 1', 'Elem Resist 1', 'Recovery 1', 'None']
    card_list = ['Loyal Partner', 'The evil hook', 'Void Shadow', 'Chrome Arms', 'Ancient Guardian', 'Deep Space Swarm', 'Realm Creature', 'Magic Era', 'Dark Realm Madman', 'Light Chaser', 'Clockwork Legion', 'Mech Empire', 'Beast Legion', 'Gloomy Forbidden Area', 'Park Guard', 'None']

    # Create Tabs for better organization
    tab_gear, tab_enhance, tab_pet, tab_fashion, tab_manual = st.tabs(
        ["Gear", "Enhance", "Pet/Card", "Fashion/Buff", "Manual"]
    )

    with tab_gear:
        # Head
        st.caption("Head")
        c1, c2 = st.columns(2)
        with c1: s_head = icon_selector("Equip", [f"{s} Head" for s in opts_armor_set], "Black Feather Head", "s_head", "Head")
        with c2: emb_head = icon_selector("Emblem", ['Soldier', 'Chariot', 'King', 'Plague', 'Glimmer Venom Wing', 'Andre', 'Isaac', 'None'], "Soldier", "emb_head", "Emblem")
        c1, c2, c3 = st.columns(3)
        with c1: t_head_1 = icon_selector("Engrave 1", engrave_transcendence, "Destruction 3", "t_h_1")
        with c2: t_head_2 = icon_selector("Engrave 2", engrave_transcendence, "Adaptation 3", "t_h_2")
        with c3: t_head_3 = icon_selector("Engrave 3", engrave_transcendence, "Combo 1", "t_h_3")
        st.markdown("---")

        # Armor
        st.caption("Armor")
        c1, c2 = st.columns(2)
        with c1: s_armor = icon_selector("Equip", [f"{s} Armor" for s in opts_armor_set], "Black Feather Armor", "s_armor", "Armor")
        with c2: emb_armor = icon_selector("Emblem", ['Eclipse Creator', 'Centaur', 'Bishop', 'King', 'Charlotte', 'Heavy Shield', 'Odisha', 'None'], "King", "emb_armor", "Emblem")
        c1, c2, c3 = st.columns(3)
        with c1: t_armor_1 = icon_selector("Engrave 1", engrave_extraordinary, "Extraordinary 2", "t_ar_1")
        with c2: t_armor_2 = icon_selector("Engrave 2", engrave_extraordinary, "Tempering 3", "t_ar_2")
        with c3: t_armor_3 = icon_selector("Engrave 3", engrave_extraordinary, "Basic 2", "t_ar_3")
        st.markdown("---")

        # Hand
        st.caption("Hand")
        c1, c2 = st.columns(2)
        with c1: s_hand = icon_selector("Equip", [f"{s} Hand" for s in opts_armor_set], "Black Feather Hand", "s_hand", "Hand")
        with c2: emb_hand = icon_selector("Emblem", ['Soldier', 'Centaur', 'Bishop', 'Chariot', 'Queen', 'Skull', 'Bogit', 'Ice Fist (Vic)', 'Isaac', 'None'], "Bishop", "emb_hand", "Emblem")
        c1, c2, c3 = st.columns(3)
        with c1: t_hand_1 = icon_selector("Engrave 1", engrave_transcendence, "Destruction 3", "t_ha_1")
        with c2: t_hand_2 = icon_selector("Engrave 2", engrave_transcendence, "Adaptation 3", "t_ha_2")
        with c3: t_hand_3 = icon_selector("Engrave 3", engrave_transcendence, "Combo 1", "t_ha_3")
        st.markdown("---")

        # Legs
        st.caption("Legs")
        c1, c2 = st.columns(2)
        with c1: s_legs = icon_selector("Equip", [f"{s} Legs" for s in opts_armor_set], "Black Feather Legs", "s_legs", "Legs")
        with c2: emb_legs = icon_selector("Emblem", ['Mars', 'Venom Behemoth', 'Goramos', 'Odisha', 'None'], "Goramos", "emb_legs", "Emblem")
        c1, c2, c3 = st.columns(3)
        with c1: t_legs_1 = icon_selector("Engrave 1", engrave_extraordinary, "Extraordinary 2", "t_l_1")
        with c2: t_legs_2 = icon_selector("Engrave 2", engrave_extraordinary, "Basic 3", "t_l_2")
        with c3: t_legs_3 = icon_selector("Engrave 3", engrave_extraordinary, "Tempering 2", "t_l_3")
        st.markdown("---")

        # Shoes
        st.caption("Shoes")
        c1, c2 = st.columns(2)
        with c1: s_shoes = icon_selector("Equip", [f"{s} Shoes" for s in opts_armor_set], "Black Feather Shoes", "s_shoes", "Shoes")
        with c2: emb_shoes = icon_selector("Emblem", ['Eclipse Creator', 'Queen', 'Famion', 'Touch of Greed', 'Electric Whip (Joker)', 'Isaac', 'None'], "Eclipse Creator", "emb_shoes", "Emblem")
        c1, c2, c3 = st.columns(3)
        with c1: t_shoes_1 = icon_selector("Engrave 1", engrave_transcendence, "Destruction 3", "t_s_1")
        with c2: t_shoes_2 = icon_selector("Engrave 2", engrave_transcendence, "Adaptation 3", "t_s_2")
        with c3: t_shoes_3 = icon_selector("Engrave 3", engrave_transcendence, "Combo 1", "t_s_3")
        st.markdown("---")

        # Weapon
        st.caption("Weapon")
        c1, c2 = st.columns(2)
        with c1: s_weapon = icon_selector("Equip", opts_weapon, "True Fate Sickle (Withered)", "s_weapon")
        with c2: emb_weapon = icon_selector("Emblem", ['Elem Mark', 'Verbena', 'Hawk', 'Demon Heart Kraken', 'None'], "Elem Mark", "emb_weapon", "Emblem")
        c1, c2, c3 = st.columns(3)
        with c1: t_weapon_1 = icon_selector("Engrave 1", engrave_excellence, "Excellence 3", "t_w_1")
        with c2: t_weapon_2 = icon_selector("Engrave 2", engrave_excellence, "Unbreakable 2", "t_w_2")
        with c3: t_weapon_3 = icon_selector("Engrave 3", engrave_excellence, "None", "t_w_3")
        st.markdown("---")

        # Necklace
        st.caption("Necklace")
        c1, c2 = st.columns(2)
        with c1: s_neck = icon_selector("Equip", [f"{s} Necklace" for s in opts_acc_set], "Holy Glory Necklace", "s_neck", "Necklace")
        with c2: emb_neck = icon_selector("Emblem", ['Michael', 'Sword of Power', 'Electric Whip (Joker)', 'Thunder Light', 'Gorga', 'None'], "Thunder Light", "emb_neck", "Emblem")
        c1, c2, c3 = st.columns(3)
        with c1: t_neck_1 = icon_selector("Engrave 1", engrave_elem_master, "Elem Master 1", "t_n_1")
        with c2: t_neck_2 = icon_selector("Engrave 2", engrave_elem_master, "Elem Resist 3", "t_n_2")
        with c3: t_neck_3 = icon_selector("Engrave 3", engrave_elem_master, "Challenger 3", "t_n_3")
        st.markdown("---")

        # Bracer
        st.caption("Bracer")
        c1, c2 = st.columns(2)
        with c1: s_bracer = icon_selector("Equip", [f"{s} Bracer" for s in opts_acc_set], "Holy Glory Bracer", "s_bracer", "Bracer")
        with c2: emb_bracer = icon_selector("Emblem", ['Michael', 'Sword of Power', 'Ice Fist (Vic)', 'Thunder Light', 'Gorga', 'None'], "Michael", "emb_bracer", "Emblem")
        c1, c2, c3 = st.columns(3)
        with c1: t_bracer_1 = icon_selector("Engrave 1", engrave_elem_master, "Elem Master 1", "t_b_1")
        with c2: t_bracer_2 = icon_selector("Engrave 2", engrave_elem_master, "Elem Resist 3", "t_b_2")
        with c3: t_bracer_3 = icon_selector("Engrave 3", engrave_elem_master, "Challenger 3", "t_b_3")
        st.markdown("---")

        # Ring
        st.caption("Ring")
        c1, c2 = st.columns(2)
        with c1: s_ring = icon_selector("Equip", [f"{s} Ring" for s in opts_acc_set], "Holy Glory Ring", "s_ring", "Ring")
        with c2: emb_ring = icon_selector("Emblem", ['Mars', 'Andre', 'Gorga', 'None'], "Mars", "emb_ring", "Emblem")
        c1, c2, c3 = st.columns(3)
        with c1: t_ring_1 = icon_selector("Engrave 1", engrave_elem_master, "Elem Master 2", "t_r_1")
        with c2: t_ring_2 = icon_selector("Engrave 2", engrave_elem_master, "Elem Resist 2", "t_r_2")
        with c3: t_ring_3 = icon_selector("Engrave 3", engrave_elem_master, "Challenger 3", "t_r_3")
        st.markdown("---")

        # Seal
        st.caption("Seal")
        c1, c2 = st.columns(2)
        with c1: s_seal = icon_selector("Equip", [f"{s} Seal" for s in opts_acc_set], "Holy Glory Seal", "s_seal", "Seal")
        with c2: emb_seal = icon_selector("Emblem", ['Azrael', 'Plague', 'Puzzle', 'Goramos', 'None'], "Azrael", "emb_seal", "Emblem")
        c1, c2, c3 = st.columns(3)
        with c1: t_seal_1 = icon_selector("Engrave 1", engrave_excellence, "Excellence 3", "t_se_1")
        with c2: t_seal_2 = icon_selector("Engrave 2", engrave_excellence, "Unbreakable 2", "t_se_2")
        with c3: t_seal_3 = icon_selector("Engrave 3", engrave_excellence, "Smite 2", "t_se_3")
        st.markdown("---")

        # Amulet
        st.caption("Amulet")
        c1, c2 = st.columns(2)
        with c1: s_amulet = icon_selector("Equip", [f"{s} Amulet" for s in opts_acc_set], "Holy Glory Amulet", "s_amulet", "Amulet")
        with c2: emb_amulet = icon_selector("Emblem", ['Azrael', 'Famion', 'Puzzle', 'Heavy Shield', 'None'], "Heavy Shield", "emb_amulet", "Emblem")
        c1, c2, c3 = st.columns(3)
        with c1: t_amulet_1 = icon_selector("Engrave 1", engrave_excellence, "Excellence 2", "t_am_1")
        with c2: t_amulet_2 = icon_selector("Engrave 2", engrave_excellence, "Unbreakable 3", "t_am_2")
        with c3: t_amulet_3 = icon_selector("Engrave 3", engrave_excellence, "Smite 2", "t_am_3")
        st.markdown("---")

        # Treasure
        st.caption("Treasure")
        s_treasure = icon_selector("Equip", ["Hourglass of World's End", 'Hymn of Ancient Demon God', 'None'], "Hourglass of World's End", "s_treasure")

    with tab_enhance:
        e_head, e_armor, e_hand = st.columns(3)
        e_head.selectbox("Head", enh_opts_str, key="enh_head", index=get_index(enh_opts_str, "+18(Str_Int)"))
        e_armor.selectbox("Armor", enh_opts_hp, key="enh_armor", index=get_index(enh_opts_hp, "+16(HP)"))
        e_hand.selectbox("Hand", enh_opts_str, key="enh_hand", index=get_index(enh_opts_str, "+16(Str_Int)"))
        
        e_legs, e_shoes, e_weapon = st.columns(3)
        e_legs.selectbox("Legs", enh_opts_hp, key="enh_legs", index=get_index(enh_opts_hp, "+15(HP)"))
        e_shoes.selectbox("Shoes", enh_opts_str, key="enh_shoes", index=get_index(enh_opts_str, "+17(Str_Int)"))
        e_weapon.selectbox("Weapon", enh_opts_wep, key="enh_weapon", index=get_index(enh_opts_wep, "+21(Weapon)"))
        
        e_neck, e_bracer, e_ring = st.columns(3)
        e_neck.selectbox("Necklace", enh_opts_str, key="enh_neck", index=get_index(enh_opts_str, "+18(Str_Int)"))
        e_bracer.selectbox("Bracer", enh_opts_str, key="enh_bracer", index=get_index(enh_opts_str, "+17(Str_Int)"))
        e_ring.selectbox("Ring", enh_opts_str, key="enh_ring", index=get_index(enh_opts_str, "+17(Str_Int)"))
        
        e_seal, e_amulet, _ = st.columns(3)
        e_seal.selectbox("Seal", enh_opts_lr, key="enh_seal", index=get_index(enh_opts_lr, "+18(L_R Slot)"))
        e_amulet.selectbox("Amulet", enh_opts_lr, key="enh_amulet", index=get_index(enh_opts_lr, "+18(L_R Slot)"))

    with tab_pet:
        star_options = ['1 Star', '2 Star', '3 Star']
        star_map = {'1 Star': '⭐', '2 Star': '⭐⭐', '3 Star': '⭐⭐⭐'}

        st.caption("Primary Pet")
        c1, c2 = st.columns([3, 1])
        with c1: pet_main = icon_selector("Pet", ['Cat', 'Eagle', 'Panda', 'Dragon', 'PiaoPiao', 'Koto', 'Fox', 'None'], "Dragon", "pet_main", "Pet")
        with c2: 
            st.write("")
            st.write("")
            pet_star = st.selectbox("Star", star_options, index=get_index(star_options, "3 Star"), format_func=lambda x: star_map[x], key="pet_star_1")
        
        c1, c2, c3 = st.columns(3)
        with c1: pet_emb_1_1 = icon_selector("Str Soul", ['Cat Paw', 'Emperor Thorn', 'Insight Eye', 'None'], "None", "pe11")
        with c2: pet_emb_1_2 = icon_selector("Skill Soul", ['Magic Witch', 'Beast Tooth Mark', 'None'], "None", "pe12")
        with c3: pet_emb_1_3 = icon_selector("Spd Soul", ['Wind Butterfly', 'Maple Curse', 'None'], "None", "pe13")
        
        st.markdown("---")
        st.caption("Secondary Pet")
        c1, c2 = st.columns([3, 1])
        with c1: pet_2 = icon_selector("Pet", ['Cat', 'Eagle', 'Panda', 'Dragon', 'PiaoPiao', 'Koto', 'Fox', 'None'], "Cat", "pet_2", "Pet")
        with c2: 
            st.write("")
            st.write("")
            pet_2_star = st.selectbox("Star", star_options, index=get_index(star_options, "3 Star"), format_func=lambda x: star_map[x], key="pet_star_2")
        
        c1, c2, c3 = st.columns(3)
        with c1: pet_emb_2_1 = icon_selector("Str Soul", ['Cat Paw', 'Emperor Thorn', 'Insight Eye', 'None'], "None", "pe21")
        with c2: pet_emb_2_2 = icon_selector("Skill Soul", ['Magic Witch', 'Beast Tooth Mark', 'None'], "None", "pe22")
        with c3: pet_emb_2_3 = icon_selector("Spd Soul", ['Wind Butterfly', 'Maple Curse', 'None'], "None", "pe23")
        
        st.markdown("---")

        st.write("Cards")
        c1, c2 = st.columns(2)
        with c1: card_1 = icon_selector("Card 1", card_list, "Void Shadow", "c1", "Card")
        with c2: card_2 = icon_selector("Card 2", card_list, "Chrome Arms", "c2", "Card")
        
        c1, c2 = st.columns(2)
        with c1: card_3 = icon_selector("Card 3", card_list, "Ancient Guardian", "c3", "Card")
        with c2: card_4 = icon_selector("Card 4", card_list, "None", "c4", "Card")

    with tab_fashion:
        c1, c2, c3 = st.columns(3)
        with c1: f_title = icon_selector("Title", ['Demon Touch', 'Void Crown', 'Gold Crown', 'None'], "Demon Touch", "f_title")
        with c2: f_weapon = icon_selector("Fashion Weapon", ['Sun Decree Seat', 'S-Rank Fashion Weapon', 'None'], "Sun Decree Seat", "f_weapon")
        with c3: f_aura = icon_selector("Aura", ['Shining Star', 'Golden Slumber', 'Eclipse Realm', 'Eclipse Realm II', 'None'], "Golden Slumber", "f_aura")
        
        c1, c2, c3 = st.columns(3)
        with c1: f_head = icon_selector("Fashion Head", ['New Sky Head', 'Old Sky Head', 'None'], "New Sky Head", "f_head", "Head")
        with c2: f_cloth = icon_selector("Fashion Cloth", ['New Sky Armor', 'Old Sky Armor', 'None'], "New Sky Armor", "f_cloth", "Armor")
        with c3: f_acc = icon_selector("Fashion Accessory", ['New Sky Accessory', 'Old Sky Accessory', 'None'], "New Sky Accessory", "f_acc", "Accessory")
        
        c1, c2, c3 = st.columns(3)
        with c1: f_face = icon_selector("Fashion Face", ['New Sky Facewear', 'Old Sky Facewear', 'None'], "New Sky Facewear", "f_face", "Facewear")
        with c2: f_badge = icon_selector("Fashion Badge", ['New Sky Badge', 'Old Sky Badge', 'None'], "New Sky Badge", "f_badge", "Badge")
        with c3: f_foot = icon_selector("Footprint", ['Shining Star Footmark', 'None'], "Shining Star Footmark", "f_foot", "Footmark")
        
        st.write("Fashion Emblems")
        c1, c2, c3 = st.columns(3)
        with c1: f_title_emb = icon_selector("Title Emblem", ['Heat Wave Title Emblem', 'Mingjin Title Emblem', 'Demon Sickle Emblem', 'None'], "Heat Wave Title Emblem", "f_title_emb", "Emblem")
        with c2: f_weapon_emb = icon_selector("Weapon Emblem", ['Mingjin Weapon Emblem', 'Demon Sickle Emblem', 'None'], "Mingjin Weapon Emblem", "f_weapon_emb", "Emblem")
        with c3: f_aura_emb = icon_selector("Aura Emblem", ['Star God Aura Emblem', 'Mingjin Aura Emblem', 'Demon Sickle Emblem', 'None'], "Mingjin Aura Emblem", "f_aura_emb", "Emblem")
        
        c1, c2, c3 = st.columns(3)
        with c1: f_head_emb = icon_selector("Head Emblem", ['Mingjin Head Emblem', 'Demon Sickle Emblem', 'None'], "Mingjin Head Emblem", "f_head_emb", "Emblem")
        with c2: f_cloth_emb = icon_selector("Cloth Emblem", ['Mingjin Armor Emblem', 'Demon Sickle Emblem', 'None'], "Demon Sickle Emblem", "f_cloth_emb", "Emblem")
        with c3: f_acc_emb = icon_selector("Accessory Emblem", ['Mingjin Accessory Emblem', 'Demon Sickle Emblem', 'None'], "Mingjin Accessory Emblem", "f_acc_emb", "Emblem")
        
        c1, c2, c3 = st.columns(3)
        with c1: f_face_emb = icon_selector("Face Emblem", ['Demon Sickle Emblem', 'None'], "Demon Sickle Emblem", "f_face_emb", "Emblem")
        with c2: f_badge_emb = icon_selector("Badge Emblem", ['Demon Sickle Emblem', 'None'], "Demon Sickle Emblem", "f_badge_emb", "Emblem")
        with c3: f_foot_emb = icon_selector("Footprint Emblem", ['Mingjin Footmark Emblem', 'Demon Sickle Emblem', 'None'], "Mingjin Footmark Emblem", "f_foot_emb", "Emblem")

        st.write("Buffs")
        c1, c2, c3 = st.columns(3)
        with c1: in_buff_elem = icon_selector("Elem Potion", ['22 Elem Potion', '25 Elem Potion', 'None'], "25 Elem Potion", "in_buff_elem", "Elem Potion")
        with c2: in_buff_atk = icon_selector("Atk Buff", ['8 Crit', '6 Counter', '8 Skill Dmg', '8 Atk', '10 Crit Dmg', 'None'], "10 Crit Dmg", "in_buff_atk", "Buff")
        with c3: in_buff_wine = icon_selector("Wine", ['Morning', 'Cliff', 'East', 'None'], "Morning", "in_buff_wine")
        
        c1, c2, c3 = st.columns(3)
        with c1: in_buff_dragon = icon_selector("Dragon Breath", ['Dragon Breath', 'None'], "Dragon Breath", "in_buff_dragon")
        with c2: in_buff_wind = icon_selector("Gale", ['Gale', 'None'], "Gale", "in_buff_wind")
        with c3: in_buff_mine = icon_selector("Mine War", ['Mine War', 'None'], "Mine War", "in_buff_mine")
        
        c1, c2, c3 = st.columns(3)
        with c1: in_buff_counter = icon_selector("Counter Buff", ['Counter', 'None'], "Counter", "in_buff_counter")

    with tab_manual:
        in_monster_def = st.number_input("Monster Def", value=5000, step=50)
        in_dot_ratio = st.number_input("Effect Ratio", value=5.0, step=0.1) # Default matches save.txt
        st.subheader("Circuit Adjustments")
        c1, c2 = st.columns(2)
        man_atk = c1.number_input("Base Atk (+)", value=191)
        man_crit_dmg = c2.number_input("Crit Dmg (+)", value=34.7)
        man_crit_rate = c1.number_input("Crit Rate (+)", value=5.5)
        man_elem = c2.number_input("Elem Boost (+)", value=20.8)
        man_cd = c1.number_input("Cooldown (+)", value=0.0)
        man_agi = c2.number_input("Agility (+)", value=0)
        man_str = c1.number_input("Strength (+)", value=134)
        man_skill_dmg = c2.number_input("Skill Dmg (+)", value=8)
        man_atk_bonus = c1.number_input("Atk Bonus (+)", value=0.0)
        man_car = c2.number_input("Car Collection Level", value=34)

        st.subheader("Custom Tech Boosts (%)")
        c1, c2 = st.columns(2)
        boost_bufan4 = c1.number_input("Extraordinary 4", value=-1.0, help="Set to >0 to override")
        boost_bufan6 = c2.number_input("Extraordinary 6", value=-1.0, help="Set to >0 to override")
        boost_zhuoyue4 = c1.number_input("Excellence 4", value=-1.0, help="Set to >0 to override")
        boost_zhuoyue7 = c2.number_input("Excellence 7", value=-1.0, help="Set to >0 to override")
        boost_zhuoyue9 = c1.number_input("Excellence 9", value=-1.0, help="Set to >0 to override")
        boost_chaoran9 = c2.number_input("Transcendence 9", value=-1.0, help="Set to >0 to override")

# --- Collect All Inputs ---
equipment_list = [
    s_head, s_armor, s_hand, s_legs, s_shoes, s_weapon,
    s_neck, s_bracer, s_ring, s_seal, s_amulet, s_treasure,
    emb_head, emb_armor, emb_hand, emb_legs, emb_shoes, emb_weapon,
    emb_neck, emb_bracer, emb_ring, emb_seal, emb_amulet,
    st.session_state.enh_head, st.session_state.enh_armor, st.session_state.enh_hand,
    st.session_state.enh_legs, st.session_state.enh_shoes, st.session_state.enh_weapon,
    st.session_state.enh_neck, st.session_state.enh_bracer, st.session_state.enh_ring,
    st.session_state.enh_seal, st.session_state.enh_amulet,
    t_head_1, t_head_2, t_head_3, t_armor_1, t_armor_2, t_armor_3,
    t_hand_1, t_hand_2, t_hand_3, t_legs_1, t_legs_2, t_legs_3,
    t_shoes_1, t_shoes_2, t_shoes_3, t_weapon_1, t_weapon_2, t_weapon_3,
    t_neck_1, t_neck_2, t_neck_3, t_bracer_1, t_bracer_2, t_bracer_3,
    t_ring_1, t_ring_2, t_ring_3, t_seal_1, t_seal_2, t_seal_3,
    t_amulet_1, t_amulet_2, t_amulet_3,
    pet_emb_1_1, pet_emb_1_2, pet_emb_1_3, pet_emb_2_1, pet_emb_2_2, pet_emb_2_3,
    card_1, card_2, card_3, card_4,
    f_title, f_weapon, f_aura, f_head, f_cloth, f_acc, f_face, f_badge, f_foot,
    f_title_emb, f_weapon_emb, f_aura_emb, f_head_emb, f_cloth_emb, f_acc_emb, f_face_emb, f_badge_emb, f_foot_emb,
    in_buff_elem, in_buff_atk, in_buff_wine, in_buff_dragon, in_buff_wind, in_buff_mine, in_buff_counter
]

# Handle pet key separately
if pet_main != 'None':
    equipment_list.append(f"{pet_star}{pet_main}")
if pet_2 != 'None':
    equipment_list.append(f"{pet_2_star}{pet_2}")

manual_inputs = {
    'monster_def': in_monster_def, 'dot_ratio': in_dot_ratio,
    'man_atk': man_atk, 'man_crit_dmg': man_crit_dmg, 'man_crit_rate': man_crit_rate,
    'man_elem': man_elem, 'man_cd': man_cd, 'man_agi': man_agi, 'man_str': man_str,
    'man_skill_dmg': man_skill_dmg, 'man_atk_bonus': man_atk_bonus, 'man_car': man_car,
    'boost_bufan4': boost_bufan4, 'boost_bufan6': boost_bufan6, 'boost_zhuoyue4': boost_zhuoyue4,
    'boost_zhuoyue7': boost_zhuoyue7, 'boost_zhuoyue9': boost_zhuoyue9, 'boost_chaoran9': boost_chaoran9
}

# --- Run Calculation and Display Results ---
try:
    final_status, burst_damage, total_damage = run_calculation(equipment_list, manual_inputs)

    with result_col:
        st.header("Calculation Results")

        # Main Damage Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Burst Damage", f"{int(burst_damage):,}")
        col2.metric("Sustained Damage (DPS)", f"{int(total_damage):,}")
        col3.metric("CD rate", f"{final_status['Cooldown Reduction']:.1f}%")

        # Comparison Feature
        if 'snapshot' not in st.session_state:
            st.session_state.snapshot = None

        c1, c2 = st.columns([1, 4])
        if c1.button("Save Snapshot"):
            st.session_state.snapshot = (final_status, burst_damage, total_damage)
            st.toast("Snapshot saved!")

        if st.session_state.snapshot:
            old_total = st.session_state.snapshot[2]
            if old_total > 0:
                diff = (total_damage - old_total) / old_total * 100
                c2.metric("Change vs Snapshot", f"{diff:+.2f}%")

        # Detailed Stats Display
        st.subheader("Detailed Panel Stats")
        # Map internal keys to user-friendly labels
        stats_to_show = [
            ('Attack (ATK)', 'Atk'), ('Crit Rate', 'Crit Rate'), ('Crit DMG', 'Crit Dmg'), ('Elem', 'Elem Boost'),
            ('ENH DMG', 'Elem Dmg'), ('Dmg Bonus', 'Dmg Amp'), ('Skill DMG', 'Skill Dmg'), ('Dmg Debuff', 'Counter'),
            ('Def Shred', 'Def Break Atk'), ('PEN', 'Penetration'), ('ASPD', 'Skill Haste'), ('DMG during Resonance', 'Resonance Dmg'),
            ('Class DMG Bonus', 'Class Dmg'), ('Skill DMG Boost', 'Skill Dmg Boost'), ('Special Stats', 'Special'), ('Skill Ratio', 'Multiplier')
        ]

        # Changed to 2 columns for better visibility in the 1/3 width layout
        cols = st.columns(2)
        for i, (label, key) in enumerate(stats_to_show):
            val = final_status.get(key, 0)
            cols[i % 2].metric(label, f"{val:,.1f}")

        if st.session_state.snapshot:
            st.markdown("---")
            st.subheader("Snapshot Panel Stats")
            snapshot_status = st.session_state.snapshot[0]
            cols_snap = st.columns(2)
            for i, (label, key) in enumerate(stats_to_show):
                val = snapshot_status.get(key, 0)
                cols_snap[i % 2].metric(label, f"{val:,.1f}")

except Exception as e:
    st.error(f"An error occurred during calculation: {e}")
    st.exception(e)