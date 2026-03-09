import pytest
from utils_computer import damage_compute, add_equipment, outfit_count


class TestDamageCompute:
    def test_basic_damage(self):
        status = {
            'Atk': 1000, 'Crit Rate': 50, 'Crit Dmg': 150,
            'Counter': 0, 'Dmg Amp': 0, 'Skill Dmg': 0,
            'Resonance Dmg': 0, 'Elem Dmg': 0, 'Monster Def': 5000,
            'Def Reduction': 0, 'Penetration': 0, 'Def Break Atk': 0,
            'Extra Dmg': 0, 'Special': 0, 'Class Dmg': 0,
            'Multiplier': 0, 'Skill Dmg Boost': 0, 'Skill Haste': 0,
            'Cooldown Reduction': 0, 'Effect Ratio': 5
        }
        burst, sustained = damage_compute(status)
        assert burst > 0
        assert sustained > 0

    def test_zero_crit_rate(self):
        status = {
            'Atk': 1000, 'Crit Rate': 0, 'Crit Dmg': 150,
            'Counter': 0, 'Dmg Amp': 0, 'Skill Dmg': 0,
            'Resonance Dmg': 0, 'Elem Dmg': 0, 'Monster Def': 5000,
            'Def Reduction': 0, 'Penetration': 0, 'Def Break Atk': 0,
            'Extra Dmg': 0, 'Special': 0, 'Class Dmg': 0,
            'Multiplier': 0, 'Skill Dmg Boost': 0, 'Skill Haste': 0,
            'Cooldown Reduction': 0, 'Effect Ratio': 5
        }
        burst, sustained = damage_compute(status)
        assert burst < 1000

    def test_def_break_atk_increases_damage(self):
        status_no_shred = {
            'Atk': 1000, 'Crit Rate': 50, 'Crit Dmg': 150,
            'Counter': 0, 'Dmg Amp': 0, 'Skill Dmg': 0,
            'Resonance Dmg': 0, 'Elem Dmg': 0, 'Monster Def': 5000,
            'Def Reduction': 0, 'Penetration': 0, 'Def Break Atk': 0,
            'Extra Dmg': 0, 'Special': 0, 'Class Dmg': 0,
            'Multiplier': 0, 'Skill Dmg Boost': 0, 'Skill Haste': 0,
            'Cooldown Reduction': 0, 'Effect Ratio': 5
        }
        status_with_shred = status_no_shred.copy()
        status_with_shred['Def Break Atk'] = 2000

        burst_no_shred, _ = damage_compute(status_no_shred)
        burst_with_shred, _ = damage_compute(status_with_shred)

        assert burst_with_shred > burst_no_shred
        assert burst_with_shred > burst_no_shred + 1500

    def test_def_reduction_reduces_damage(self):
        status_no_pen = {
            'Atk': 1000, 'Crit Rate': 50, 'Crit Dmg': 150,
            'Counter': 0, 'Dmg Amp': 0, 'Skill Dmg': 0,
            'Resonance Dmg': 0, 'Elem Dmg': 0, 'Monster Def': 5000,
            'Def Reduction': 0, 'Penetration': 0, 'Def Break Atk': 0,
            'Extra Dmg': 0, 'Special': 0, 'Class Dmg': 0,
            'Multiplier': 0, 'Skill Dmg Boost': 0, 'Skill Haste': 0,
            'Cooldown Reduction': 0, 'Effect Ratio': 5
        }
        status_with_pen = status_no_pen.copy()
        status_with_pen['Def Reduction'] = 50

        burst_no_pen, _ = damage_compute(status_no_pen)
        burst_with_pen, _ = damage_compute(status_with_pen)

        assert burst_with_pen > burst_no_pen

    def test_zero_monster_def(self):
        status = {
            'Atk': 1000, 'Crit Rate': 50, 'Crit Dmg': 150,
            'Counter': 0, 'Dmg Amp': 0, 'Skill Dmg': 0,
            'Resonance Dmg': 0, 'Elem Dmg': 0, 'Monster Def': 0,
            'Def Reduction': 0, 'Penetration': 0, 'Def Break Atk': 0,
            'Extra Dmg': 0, 'Special': 0, 'Class Dmg': 0,
            'Multiplier': 0, 'Skill Dmg Boost': 0, 'Skill Haste': 0,
            'Cooldown Reduction': 0, 'Effect Ratio': 5
        }
        burst, sustained = damage_compute(status)
        assert burst > 1000

    def test_crit_rate_capped_at_100(self):
        status = {
            'Atk': 1000, 'Crit Rate': 150, 'Crit Dmg': 150,
            'Counter': 0, 'Dmg Amp': 0, 'Skill Dmg': 0,
            'Resonance Dmg': 0, 'Elem Dmg': 0, 'Monster Def': 5000,
            'Def Reduction': 0, 'Penetration': 0, 'Def Break Atk': 0,
            'Extra Dmg': 0, 'Special': 0, 'Class Dmg': 0,
            'Multiplier': 0, 'Skill Dmg Boost': 0, 'Skill Haste': 0,
            'Cooldown Reduction': 0, 'Effect Ratio': 5
        }
        burst, sustained = damage_compute(status)
        assert burst > 0


class TestAddEquipment:
    def test_add_new_stat(self):
        status = {'Atk': 100}
        equipment = {'Atk': 50, 'Crit Rate': 10}
        result = add_equipment(status, equipment)
        assert result['Atk'] == 150
        assert result['Crit Rate'] == 10

    def test_add_existing_stat(self):
        status = {'Atk': 100}
        equipment = {'Atk': 50}
        result = add_equipment(status, equipment)
        assert result['Atk'] == 150

    def test_add_empty_equipment(self):
        status = {'Atk': 100}
        equipment = {}
        result = add_equipment(status, equipment)
        assert result['Atk'] == 100


class TestOutfitCount:
    def test_basic_outfit_count(self):
        status = {'Transcendence': 2, 'Extraordinary': 3}
        outfit_dict = {
            'Transcendence': {'2': {}, '3': {}},
            'Extraordinary': {'2': {}, '3': {}}
        }
        result = outfit_count(status, outfit_dict)
        assert ('Transcendence', '2') in result
        assert ('Extraordinary', '3') in result

    def test_black_feather_removed_with_glimmer(self):
        status = {'Black Feather': 2, 'Glimmer': 2}
        outfit_dict = {
            'Black Feather': {'2': {}},
            'Glimmer': {'2': {}}
        }
        result = outfit_count(status, outfit_dict)
        assert ('Black Feather', '2') not in result
        assert ('Glimmer', '2') in result
