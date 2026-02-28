# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: '晶核面板计算器.py'
# Bytecode version: 3.9.0beta5 (3425)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys
from gui import Ui_Form as GUI
import json
from utils_computer import *

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = GUI()
        self.ui.setupUi(self)
        self.setStyleSheet('background:rgb(199,237,204);color:black;')
        self.setWindowTitle('Crystal Core Panel Calculator')
        self.setWindowIcon(QIcon('icon\\icon.png'))
        self.default_equipment = ['' for i in range(115)]
        for i in range(6):
            self.default_equipment.append('-1.0')
        self.default_equipment.append('0.0')
        self.default_equipment.append('0')
        self.previous_equipment = ['' for i in range(123)]
        self.current_equipment = ['' for i in range(123)]
        menu = QMenu()
        name_list = ['Black Feather Head', 'Glimmer Head', 'Avarice Head', 'Venom Head', 'Butterfly Head', 'Demon Heart Head', 'Cursed Head', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.equip_head, name, 0)
        self.ui.equip_head.setMenu(menu)
        menu = QMenu()
        name_list = ['Black Feather Armor', 'Glimmer Armor', 'Avarice Armor', 'Venom Armor', 'Butterfly Armor', 'Demon Heart Armor', 'Cursed Armor', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.equip_armor, name, 1)
        self.ui.equip_armor.setMenu(menu)
        menu = QMenu()
        name_list = ['Black Feather Hand', 'Glimmer Hand', 'Avarice Hand', 'Venom Hand', 'Butterfly Hand', 'Demon Heart Hand', 'Cursed Hand', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.equip_hand, name, 2)
        self.ui.equip_hand.setMenu(menu)
        menu = QMenu()
        name_list = ['Black Feather Legs', 'Glimmer Legs', 'Avarice Legs', 'Venom Legs', 'Butterfly Legs', 'Demon Heart Legs', 'Cursed Legs', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.equip_leg, name, 3)
        self.ui.equip_leg.setMenu(menu)
        menu = QMenu()
        name_list = ['Black Feather Shoes', 'Glimmer Shoes', 'Avarice Shoes', 'Venom Shoes', 'Butterfly Shoes', 'Demon Heart Shoes', 'Cursed Shoes', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.equip_shoe, name, 4)
        self.ui.equip_shoe.setMenu(menu)
        menu = QMenu()
        name_list = ['True Fate Sickle (Withered)', 'Abyssal Gaze', 'Desperate Dream Song', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.equip_weapon, name, 5)
        self.ui.equip_weapon.setMenu(menu)
        menu = QMenu()
        name_list = ['Solar Necklace', 'Holy Glory Necklace', 'Demon Shadow Necklace', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.equip_necklace, name, 6)
        self.ui.equip_necklace.setMenu(menu)
        menu = QMenu()
        name_list = ['Solar Bracer', 'Holy Glory Bracer', 'Demon Shadow Bracer', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.equip_bracer, name, 7)
        self.ui.equip_bracer.setMenu(menu)
        menu = QMenu()
        name_list = ['Solar Ring', 'Holy Glory Ring', 'Demon Shadow Ring', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.equip_ring, name, 8)
        self.ui.equip_ring.setMenu(menu)
        menu = QMenu()
        name_list = ['Solar Seal', 'Holy Glory Seal', 'Demon Shadow Seal', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.equip_seal, name, 9)
        self.ui.equip_seal.setMenu(menu)
        menu = QMenu()
        name_list = ['Solar Amulet', 'Holy Glory Amulet', 'Demon Shadow Amulet', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.equip_amulet, name, 10)
        self.ui.equip_amulet.setMenu(menu)
        menu = QMenu()
        name_list = ["Hourglass of World's End", 'Hymn of Ancient Demon God', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.equip_treasure, name, 11)
        self.ui.equip_treasure.setMenu(menu)
        menu = QMenu()
        name_list = ['Soldier', 'Chariot', 'King', 'Plague', 'Glimmer Venom Wing', 'Andre', 'Isaac', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.emblem_head, name, 12)
        self.ui.emblem_head.setMenu(menu)
        menu = QMenu()
        name_list = ['Eclipse Creator', 'Centaur', 'Bishop', 'King', 'Charlotte', 'Heavy Shield', 'Odisha', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.emblem_armor, name, 13)
        self.ui.emblem_armor.setMenu(menu)
        menu = QMenu()
        name_list = ['Soldier', 'Centaur', 'Bishop', 'Chariot', 'Queen', 'Skull', 'Bogit', 'Ice Fist (Vic)', 'Isaac', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.emblem_hand, name, 14)
        self.ui.emblem_hand.setMenu(menu)
        menu = QMenu()
        name_list = ['Mars', 'Venom Behemoth', 'Goramos', 'Odisha', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.emblem_leg, name, 15)
        self.ui.emblem_leg.setMenu(menu)
        menu = QMenu()
        name_list = ['Eclipse Creator', 'Queen', 'Famion', 'Touch of Greed', 'Electric Whip (Joker)', 'Isaac', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.emblem_shoe, name, 16)
        self.ui.emblem_shoe.setMenu(menu)
        menu = QMenu()
        name_list = ['Elem Mark', 'Verbena', 'Hawk', 'Demon Heart Kraken', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.emblem_weapon, name, 17)
        self.ui.emblem_weapon.setMenu(menu)
        menu = QMenu()
        name_list = ['Michael', 'Sword of Power', 'Electric Whip (Joker)', 'Thunder Light', 'Gorga', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.emblem_necklace, name, 18)
        self.ui.emblem_necklace.setMenu(menu)
        menu = QMenu()
        name_list = ['Michael', 'Sword of Power', 'Ice Fist (Vic)', 'Thunder Light', 'Gorga', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.emblem_bracer, name, 19)
        self.ui.emblem_bracer.setMenu(menu)
        menu = QMenu()
        name_list = ['Mars', 'Andre', 'Gorga', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.emblem_ring, name, 20)
        self.ui.emblem_ring.setMenu(menu)
        menu = QMenu()
        name_list = ['Azrael', 'Plague', 'Puzzle', 'Goramos', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.emblem_seal, name, 21)
        self.ui.emblem_seal.setMenu(menu)
        menu = QMenu()
        name_list = ['Azrael', 'Famion', 'Puzzle', 'Heavy Shield', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.emblem_amulet, name, 22)
        self.ui.emblem_amulet.setMenu(menu)
        menu = QMenu()
        name_list = ['+15(Str_Int)', '+16(Str_Int)', '+17(Str_Int)', '+18(Str_Int)', '+19(Str_Int)', '+20(Str_Int)', '+21(Str_Int)', '+22(Str_Int)', '+23(Str_Int)', '+24(Str_Int)', '+25(Str_Int)', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.enhancement_head, name, 23)
        self.ui.enhancement_head.setMenu(menu)
        menu = QMenu()
        name_list = ['+15(HP)', '+16(HP)', '+17(HP)', '+18(HP)', '+19(HP)', '+20(HP)', '+21(HP)', '+22(HP)', '+23(HP)', '+24(HP)', '+25(HP)', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.enhancement_armor, name, 24)
        self.ui.enhancement_armor.setMenu(menu)
        menu = QMenu()
        name_list = ['+15(Str_Int)', '+16(Str_Int)', '+17(Str_Int)', '+18(Str_Int)', '+19(Str_Int)', '+20(Str_Int)', '+21(Str_Int)', '+22(Str_Int)', '+23(Str_Int)', '+24(Str_Int)', '+25(Str_Int)', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.enhancement_hand, name, 25)
        self.ui.enhancement_hand.setMenu(menu)
        menu = QMenu()
        name_list = ['+15(HP)', '+16(HP)', '+17(HP)', '+18(HP)', '+19(HP)', '+20(HP)', '+21(HP)', '+22(HP)', '+23(HP)', '+24(HP)', '+25(HP)', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.enhancement_leg, name, 26)
        self.ui.enhancement_leg.setMenu(menu)
        menu = QMenu()
        name_list = ['+15(Str_Int)', '+16(Str_Int)', '+17(Str_Int)', '+18(Str_Int)', '+19(Str_Int)', '+20(Str_Int)', '+21(Str_Int)', '+22(Str_Int)', '+23(Str_Int)', '+24(Str_Int)', '+25(Str_Int)', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.enhancement_shoe, name, 27)
        self.ui.enhancement_shoe.setMenu(menu)
        menu = QMenu()
        name_list = ['+18(Weapon)', '+19(Weapon)', '+20(Weapon)', '+21(Weapon)', '+22(Weapon)', '+23(Weapon)', '+24(Weapon)', '+25(Weapon)', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.enhancement_weapon, name, 28)
        self.ui.enhancement_weapon.setMenu(menu)
        menu = QMenu()
        name_list = ['+15(Str_Int)', '+16(Str_Int)', '+17(Str_Int)', '+18(Str_Int)', '+19(Str_Int)', '+20(Str_Int)', '+21(Str_Int)', '+22(Str_Int)', '+23(Str_Int)', '+24(Str_Int)', '+25(Str_Int)', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.enhancement_necklace, name, 29)
        self.ui.enhancement_necklace.setMenu(menu)
        menu = QMenu()
        name_list = ['+15(Str_Int)', '+16(Str_Int)', '+17(Str_Int)', '+18(Str_Int)', '+19(Str_Int)', '+20(Str_Int)', '+21(Str_Int)', '+22(Str_Int)', '+23(Str_Int)', '+24(Str_Int)', '+25(Str_Int)', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.enhancement_bracer, name, 30)
        self.ui.enhancement_bracer.setMenu(menu)
        menu = QMenu()
        name_list = ['+15(Str_Int)', '+16(Str_Int)', '+17(Str_Int)', '+18(Str_Int)', '+19(Str_Int)', '+20(Str_Int)', '+21(Str_Int)', '+22(Str_Int)', '+23(Str_Int)', '+24(Str_Int)', '+25(Str_Int)', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.enhancement_ring, name, 31)
        self.ui.enhancement_ring.setMenu(menu)
        menu = QMenu()
        name_list = ['+15(L_R Slot)', '+16(L_R Slot)', '+17(L_R Slot)', '+18(L_R Slot)', '+19(L_R Slot)', '+20(L_R Slot)', '+21(L_R Slot)', '+22(L_R Slot)', '+23(L_R Slot)', '+24(L_R Slot)', '+25(L_R Slot)', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.enhancement_seal, name, 32)
        self.ui.enhancement_seal.setMenu(menu)
        menu = QMenu()
        name_list = ['+15(L_R Slot)', '+16(L_R Slot)', '+17(L_R Slot)', '+18(L_R Slot)', '+19(L_R Slot)', '+20(L_R Slot)', '+21(L_R Slot)', '+22(L_R Slot)', '+23(L_R Slot)', '+24(L_R Slot)', '+25(L_R Slot)', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.enhancement_amulet, name, 33)
        self.ui.enhancement_amulet.setMenu(menu)
        menu = QMenu()
        name_list = ['Transcendence 3', 'Adaptation 3', 'Destruction 3', 'Swiftness 3', 'Combo 3', 'Transcendence 2', 'Adaptation 2', 'Destruction 2', 'Swiftness 2', 'Combo 2', 'Transcendence 1', 'Adaptation 1', 'Destruction 1', 'Swiftness 1', 'Combo 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_head_1, name, 34)
        self.ui.engrave_head_1.setMenu(menu)
        menu = QMenu()
        name_list = ['Transcendence 3', 'Adaptation 3', 'Destruction 3', 'Swiftness 3', 'Combo 3', 'Transcendence 2', 'Adaptation 2', 'Destruction 2', 'Swiftness 2', 'Combo 2', 'Transcendence 1', 'Adaptation 1', 'Destruction 1', 'Swiftness 1', 'Combo 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_head_2, name, 35)
        self.ui.engrave_head_2.setMenu(menu)
        menu = QMenu()
        name_list = ['Transcendence 3', 'Adaptation 3', 'Destruction 3', 'Swiftness 3', 'Combo 3', 'Transcendence 2', 'Adaptation 2', 'Destruction 2', 'Swiftness 2', 'Combo 2', 'Transcendence 1', 'Adaptation 1', 'Destruction 1', 'Swiftness 1', 'Combo 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_head_3, name, 36)
        self.ui.engrave_head_3.setMenu(menu)
        menu = QMenu()
        name_list = ['Extraordinary 3', 'Tempering 3', 'High-Tier 3', 'Status Break 3', 'Basic 3', 'Pierce 3', 'Fortification 3', 'Extraordinary 2', 'Tempering 2', 'High-Tier 2', 'Status Break 2', 'Basic 2', 'Pierce 2', 'Fortification 2', 'Extraordinary 1', 'Tempering 1', 'High-Tier 1', 'Status Break 1', 'Basic 1', 'Pierce 1', 'Fortification 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_armor_1, name, 37)
        self.ui.engrave_armor_1.setMenu(menu)
        menu = QMenu()
        name_list = ['Extraordinary 3', 'Tempering 3', 'High-Tier 3', 'Status Break 3', 'Basic 3', 'Pierce 3', 'Fortification 3', 'Extraordinary 2', 'Tempering 2', 'High-Tier 2', 'Status Break 2', 'Basic 2', 'Pierce 2', 'Fortification 2', 'Extraordinary 1', 'Tempering 1', 'High-Tier 1', 'Status Break 1', 'Basic 1', 'Pierce 1', 'Fortification 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_armor_2, name, 38)
        self.ui.engrave_armor_2.setMenu(menu)
        menu = QMenu()
        name_list = ['Extraordinary 3', 'Tempering 3', 'High-Tier 3', 'Status Break 3', 'Basic 3', 'Pierce 3', 'Fortification 3', 'Extraordinary 2', 'Tempering 2', 'High-Tier 2', 'Status Break 2', 'Basic 2', 'Pierce 2', 'Fortification 2', 'Extraordinary 1', 'Tempering 1', 'High-Tier 1', 'Status Break 1', 'Basic 1', 'Pierce 1', 'Fortification 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_armor_3, name, 39)
        self.ui.engrave_armor_3.setMenu(menu)
        menu = QMenu()
        name_list = ['Transcendence 3', 'Adaptation 3', 'Destruction 3', 'Swiftness 3', 'Combo 3', 'Transcendence 2', 'Adaptation 2', 'Destruction 2', 'Swiftness 2', 'Combo 2', 'Transcendence 1', 'Adaptation 1', 'Destruction 1', 'Swiftness 1', 'Combo 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_hand_1, name, 40)
        self.ui.engrave_hand_1.setMenu(menu)
        menu = QMenu()
        name_list = ['Transcendence 3', 'Adaptation 3', 'Destruction 3', 'Swiftness 3', 'Combo 3', 'Transcendence 2', 'Adaptation 2', 'Destruction 2', 'Swiftness 2', 'Combo 2', 'Transcendence 1', 'Adaptation 1', 'Destruction 1', 'Swiftness 1', 'Combo 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_hand_2, name, 41)
        self.ui.engrave_hand_2.setMenu(menu)
        menu = QMenu()
        name_list = ['Transcendence 3', 'Adaptation 3', 'Destruction 3', 'Swiftness 3', 'Combo 3', 'Transcendence 2', 'Adaptation 2', 'Destruction 2', 'Swiftness 2', 'Combo 2', 'Transcendence 1', 'Adaptation 1', 'Destruction 1', 'Swiftness 1', 'Combo 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_hand_3, name, 42)
        self.ui.engrave_hand_3.setMenu(menu)
        menu = QMenu()
        name_list = ['Extraordinary 3', 'Tempering 3', 'High-Tier 3', 'Status Break 3', 'Basic 3', 'Pierce 3', 'Fortification 3', 'Extraordinary 2', 'Tempering 2', 'High-Tier 2', 'Status Break 2', 'Basic 2', 'Pierce 2', 'Fortification 2', 'Extraordinary 1', 'Tempering 1', 'High-Tier 1', 'Status Break 1', 'Basic 1', 'Pierce 1', 'Fortification 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_leg_1, name, 43)
        self.ui.engrave_leg_1.setMenu(menu)
        menu = QMenu()
        name_list = ['Extraordinary 3', 'Tempering 3', 'High-Tier 3', 'Status Break 3', 'Basic 3', 'Pierce 3', 'Fortification 3', 'Extraordinary 2', 'Tempering 2', 'High-Tier 2', 'Status Break 2', 'Basic 2', 'Pierce 2', 'Fortification 2', 'Extraordinary 1', 'Tempering 1', 'High-Tier 1', 'Status Break 1', 'Basic 1', 'Pierce 1', 'Fortification 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_leg_2, name, 44)
        self.ui.engrave_leg_2.setMenu(menu)
        menu = QMenu()
        name_list = ['Extraordinary 3', 'Tempering 3', 'High-Tier 3', 'Status Break 3', 'Basic 3', 'Pierce 3', 'Fortification 3', 'Extraordinary 2', 'Tempering 2', 'High-Tier 2', 'Status Break 2', 'Basic 2', 'Pierce 2', 'Fortification 2', 'Extraordinary 1', 'Tempering 1', 'High-Tier 1', 'Status Break 1', 'Basic 1', 'Pierce 1', 'Fortification 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_leg_3, name, 45)
        self.ui.engrave_leg_3.setMenu(menu)
        menu = QMenu()
        name_list = ['Transcendence 3', 'Adaptation 3', 'Destruction 3', 'Swiftness 3', 'Combo 3', 'Transcendence 2', 'Adaptation 2', 'Destruction 2', 'Swiftness 2', 'Combo 2', 'Transcendence 1', 'Adaptation 1', 'Destruction 1', 'Swiftness 1', 'Combo 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_shoe_1, name, 46)
        self.ui.engrave_shoe_1.setMenu(menu)
        menu = QMenu()
        name_list = ['Transcendence 3', 'Adaptation 3', 'Destruction 3', 'Swiftness 3', 'Combo 3', 'Transcendence 2', 'Adaptation 2', 'Destruction 2', 'Swiftness 2', 'Combo 2', 'Transcendence 1', 'Adaptation 1', 'Destruction 1', 'Swiftness 1', 'Combo 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_shoe_2, name, 47)
        self.ui.engrave_shoe_2.setMenu(menu)
        menu = QMenu()
        name_list = ['Transcendence 3', 'Adaptation 3', 'Destruction 3', 'Swiftness 3', 'Combo 3', 'Transcendence 2', 'Adaptation 2', 'Destruction 2', 'Swiftness 2', 'Combo 2', 'Transcendence 1', 'Adaptation 1', 'Destruction 1', 'Swiftness 1', 'Combo 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_shoe_3, name, 48)
        self.ui.engrave_shoe_3.setMenu(menu)
        menu = QMenu()
        name_list = ['Excellence 3', 'Smite 3', 'Alliance 3', 'Unbreakable 3', 'Excellence 2', 'Smite 2', 'Alliance 2', 'Unbreakable 2', 'Excellence 1', 'Smite 1', 'Alliance 1', 'Unbreakable 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_weapon_1, name, 49)
        self.ui.engrave_weapon_1.setMenu(menu)
        menu = QMenu()
        name_list = ['Excellence 3', 'Smite 3', 'Alliance 3', 'Unbreakable 3', 'Excellence 2', 'Smite 2', 'Alliance 2', 'Unbreakable 2', 'Excellence 1', 'Smite 1', 'Alliance 1', 'Unbreakable 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_weapon_2, name, 50)
        self.ui.engrave_weapon_2.setMenu(menu)
        menu = QMenu()
        name_list = ['Excellence 3', 'Smite 3', 'Alliance 3', 'Unbreakable 3', 'Excellence 2', 'Smite 2', 'Alliance 2', 'Unbreakable 2', 'Excellence 1', 'Smite 1', 'Alliance 1', 'Unbreakable 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_weapon_3, name, 51)
        self.ui.engrave_weapon_3.setMenu(menu)
        menu = QMenu()
        name_list = ['Elem Master 3', 'Challenger 3', 'Resonance 3', 'Evasion 3', 'Elem Resist 3', 'Recovery 3', 'Elem Master 2', 'Challenger 2', 'Resonance 2', 'Evasion 2', 'Elem Resist 2', 'Recovery 2', 'Elem Master 1', 'Challenger 1', 'Resonance 1', 'Evasion 1', 'Elem Resist 1', 'Recovery 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_necklace_1, name, 52)
        self.ui.engrave_necklace_1.setMenu(menu)
        menu = QMenu()
        name_list = ['Elem Master 3', 'Challenger 3', 'Resonance 3', 'Evasion 3', 'Elem Resist 3', 'Recovery 3', 'Elem Master 2', 'Challenger 2', 'Resonance 2', 'Evasion 2', 'Elem Resist 2', 'Recovery 2', 'Elem Master 1', 'Challenger 1', 'Resonance 1', 'Evasion 1', 'Elem Resist 1', 'Recovery 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_necklace_2, name, 53)
        self.ui.engrave_necklace_2.setMenu(menu)
        menu = QMenu()
        name_list = ['Elem Master 3', 'Challenger 3', 'Resonance 3', 'Evasion 3', 'Elem Resist 3', 'Recovery 3', 'Elem Master 2', 'Challenger 2', 'Resonance 2', 'Evasion 2', 'Elem Resist 2', 'Recovery 2', 'Elem Master 1', 'Challenger 1', 'Resonance 1', 'Evasion 1', 'Elem Resist 1', 'Recovery 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_necklace_3, name, 54)
        self.ui.engrave_necklace_3.setMenu(menu)
        menu = QMenu()
        name_list = ['Elem Master 3', 'Challenger 3', 'Resonance 3', 'Evasion 3', 'Elem Resist 3', 'Recovery 3', 'Elem Master 2', 'Challenger 2', 'Resonance 2', 'Evasion 2', 'Elem Resist 2', 'Recovery 2', 'Elem Master 1', 'Challenger 1', 'Resonance 1', 'Evasion 1', 'Elem Resist 1', 'Recovery 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_bracer_1, name, 55)
        self.ui.engrave_bracer_1.setMenu(menu)
        menu = QMenu()
        name_list = ['Elem Master 3', 'Challenger 3', 'Resonance 3', 'Evasion 3', 'Elem Resist 3', 'Recovery 3', 'Elem Master 2', 'Challenger 2', 'Resonance 2', 'Evasion 2', 'Elem Resist 2', 'Recovery 2', 'Elem Master 1', 'Challenger 1', 'Resonance 1', 'Evasion 1', 'Elem Resist 1', 'Recovery 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_bracer_2, name, 56)
        self.ui.engrave_bracer_2.setMenu(menu)
        menu = QMenu()
        name_list = ['Elem Master 3', 'Challenger 3', 'Resonance 3', 'Evasion 3', 'Elem Resist 3', 'Recovery 3', 'Elem Master 2', 'Challenger 2', 'Resonance 2', 'Evasion 2', 'Elem Resist 2', 'Recovery 2', 'Elem Master 1', 'Challenger 1', 'Resonance 1', 'Evasion 1', 'Elem Resist 1', 'Recovery 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_bracer_3, name, 57)
        self.ui.engrave_bracer_3.setMenu(menu)
        menu = QMenu()
        name_list = ['Elem Master 3', 'Challenger 3', 'Resonance 3', 'Evasion 3', 'Elem Resist 3', 'Recovery 3', 'Elem Master 2', 'Challenger 2', 'Resonance 2', 'Evasion 2', 'Elem Resist 2', 'Recovery 2', 'Elem Master 1', 'Challenger 1', 'Resonance 1', 'Evasion 1', 'Elem Resist 1', 'Recovery 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_ring_1, name, 58)
        self.ui.engrave_ring_1.setMenu(menu)
        menu = QMenu()
        name_list = ['Elem Master 3', 'Challenger 3', 'Resonance 3', 'Evasion 3', 'Elem Resist 3', 'Recovery 3', 'Elem Master 2', 'Challenger 2', 'Resonance 2', 'Evasion 2', 'Elem Resist 2', 'Recovery 2', 'Elem Master 1', 'Challenger 1', 'Resonance 1', 'Evasion 1', 'Elem Resist 1', 'Recovery 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_ring_2, name, 59)
        self.ui.engrave_ring_2.setMenu(menu)
        menu = QMenu()
        name_list = ['Elem Master 3', 'Challenger 3', 'Resonance 3', 'Evasion 3', 'Elem Resist 3', 'Recovery 3', 'Elem Master 2', 'Challenger 2', 'Resonance 2', 'Evasion 2', 'Elem Resist 2', 'Recovery 2', 'Elem Master 1', 'Challenger 1', 'Resonance 1', 'Evasion 1', 'Elem Resist 1', 'Recovery 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_ring_3, name, 60)
        self.ui.engrave_ring_3.setMenu(menu)
        menu = QMenu()
        name_list = ['Excellence 3', 'Smite 3', 'Alliance 3', 'Unbreakable 3', 'Excellence 2', 'Smite 2', 'Alliance 2', 'Unbreakable 2', 'Excellence 1', 'Smite 1', 'Alliance 1', 'Unbreakable 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_seal_1, name, 61)
        self.ui.engrave_seal_1.setMenu(menu)
        menu = QMenu()
        name_list = ['Excellence 3', 'Smite 3', 'Alliance 3', 'Unbreakable 3', 'Excellence 2', 'Smite 2', 'Alliance 2', 'Unbreakable 2', 'Excellence 1', 'Smite 1', 'Alliance 1', 'Unbreakable 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_seal_2, name, 62)
        self.ui.engrave_seal_2.setMenu(menu)
        menu = QMenu()
        name_list = ['Excellence 3', 'Smite 3', 'Alliance 3', 'Unbreakable 3', 'Excellence 2', 'Smite 2', 'Alliance 2', 'Unbreakable 2', 'Excellence 1', 'Smite 1', 'Alliance 1', 'Unbreakable 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_seal_3, name, 63)
        self.ui.engrave_seal_3.setMenu(menu)
        menu = QMenu()
        name_list = ['Excellence 3', 'Smite 3', 'Alliance 3', 'Unbreakable 3', 'Excellence 2', 'Smite 2', 'Alliance 2', 'Unbreakable 2', 'Excellence 1', 'Smite 1', 'Alliance 1', 'Unbreakable 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_amulet_1, name, 64)
        self.ui.engrave_amulet_1.setMenu(menu)
        menu = QMenu()
        name_list = ['Excellence 3', 'Smite 3', 'Alliance 3', 'Unbreakable 3', 'Excellence 2', 'Smite 2', 'Alliance 2', 'Unbreakable 2', 'Excellence 1', 'Smite 1', 'Alliance 1', 'Unbreakable 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_amulet_2, name, 65)
        self.ui.engrave_amulet_2.setMenu(menu)
        menu = QMenu()
        name_list = ['Excellence 3', 'Smite 3', 'Alliance 3', 'Unbreakable 3', 'Excellence 2', 'Smite 2', 'Alliance 2', 'Unbreakable 2', 'Excellence 1', 'Smite 1', 'Alliance 1', 'Unbreakable 1', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.engrave_amulet_3, name, 66)
        self.ui.engrave_amulet_3.setMenu(menu)
        menu = QMenu()
        name_list = ['Cat', 'Eagle', 'Panda', 'Dragon', 'PiaoPiao', 'Koto', 'Fox', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.pet_1, name, 67)
        self.ui.pet_1.setMenu(menu)
        menu = QMenu()
        name_list = ['Cat', 'Eagle', 'Panda', 'Dragon', 'PiaoPiao', 'Koto', 'Fox', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.pet_2, name, 68)
        self.ui.pet_2.setMenu(menu)
        menu = QMenu()
        name_list = ['1 Star', '2 Star', '3 Star', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.pet_level_1, name, 69)
        self.ui.pet_level_1.setMenu(menu)
        menu = QMenu()
        name_list = ['1 Star', '2 Star', '3 Star', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.pet_level_2, name, 70)
        self.ui.pet_level_2.setMenu(menu)
        menu = QMenu()
        name_list = ['Cat Paw', 'Emperor Thorn', 'Insight Eye', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.pet_emblem_1_1, name, 71)
        self.ui.pet_emblem_1_1.setMenu(menu)
        menu = QMenu()
        name_list = ['Cat Paw', 'Emperor Thorn', 'Insight Eye', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.pet_emblem_2_1, name, 72)
        self.ui.pet_emblem_2_1.setMenu(menu)
        menu = QMenu()
        name_list = ['Magic Witch', 'Beast Tooth Mark', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.pet_emblem_1_2, name, 73)
        self.ui.pet_emblem_1_2.setMenu(menu)
        menu = QMenu()
        name_list = ['Magic Witch', 'Beast Tooth Mark', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.pet_emblem_2_2, name, 74)
        self.ui.pet_emblem_2_2.setMenu(menu)
        menu = QMenu()
        name_list = ['Wind Butterfly', 'Maple Curse', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.pet_emblem_1_3, name, 75)
        self.ui.pet_emblem_1_3.setMenu(menu)
        menu = QMenu()
        name_list = ['Wind Butterfly', 'Maple Curse', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.pet_emblem_2_3, name, 76)
        self.ui.pet_emblem_2_3.setMenu(menu)
        menu = QMenu()
        name_list = ['Loyal Partner', 'The evil hook', 'Void Shadow', 'Chrome Arms', 'Ancient Guardian', 'Deep Space Swarm', 'Realm Creature', 'Magic Era', 'Dark Realm Madman', 'Light Chaser', 'Clockwork Legion', 'Mech Empire', 'Beast Legion', 'Gloomy Forbidden Area', 'Park Guard', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.card_1, name, 77)
        self.ui.card_1.setMenu(menu)
        menu = QMenu()
        name_list = ['Loyal Partner', 'The evil hook', 'Void Shadow', 'Chrome Arms', 'Ancient Guardian', 'Deep Space Swarm', 'Realm Creature', 'Magic Era', 'Dark Realm Madman', 'Light Chaser', 'Clockwork Legion', 'Mech Empire', 'Beast Legion', 'Gloomy Forbidden Area', 'Park Guard', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.card_2, name, 78)
        self.ui.card_2.setMenu(menu)
        menu = QMenu()
        name_list = ['Loyal Partner', 'The evil hook', 'Void Shadow', 'Chrome Arms', 'Ancient Guardian', 'Deep Space Swarm', 'Realm Creature', 'Magic Era', 'Dark Realm Madman', 'Light Chaser', 'Clockwork Legion', 'Mech Empire', 'Beast Legion', 'Gloomy Forbidden Area', 'Park Guard', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.card_3, name, 79)
        self.ui.card_3.setMenu(menu)
        menu = QMenu()
        name_list = ['Loyal Partner', 'The evil hook', 'Void Shadow', 'Chrome Arms', 'Ancient Guardian', 'Deep Space Swarm', 'Realm Creature', 'Magic Era', 'Dark Realm Madman', 'Light Chaser', 'Clockwork Legion', 'Mech Empire', 'Beast Legion', 'Gloomy Forbidden Area', 'Park Guard', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.card_4, name, 80)
        self.ui.card_4.setMenu(menu)
        menu = QMenu()
        name_list = ['Demon Touch', 'Void Crown', 'Gold Crown', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.title, name, 81)
        self.ui.title.setMenu(menu)
        menu = QMenu()
        name_list = ['Sun Decree Seat', 'S-Rank Fashion Weapon', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.weapon, name, 82)
        self.ui.weapon.setMenu(menu)
        menu = QMenu()
        name_list = ['Shining Star', 'Golden Slumber', 'Eclipse Realm', 'Eclipse Realm II', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.aureole, name, 83)
        self.ui.aureole.setMenu(menu)
        menu = QMenu()
        name_list = ['New Sky Head', 'Old Sky Head', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.headwear, name, 84)
        self.ui.headwear.setMenu(menu)
        menu = QMenu()
        name_list = ['New Sky Armor', 'Old Sky Armor', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.cloth, name, 85)
        self.ui.cloth.setMenu(menu)
        menu = QMenu()
        name_list = ['New Sky Accessory', 'Old Sky Accessory', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.accessory, name, 86)
        self.ui.accessory.setMenu(menu)
        menu = QMenu()
        name_list = ['New Sky Facewear', 'Old Sky Facewear', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.facewear, name, 87)
        self.ui.facewear.setMenu(menu)
        menu = QMenu()
        name_list = ['New Sky Badge', 'Old Sky Badge', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.badge, name, 88)
        self.ui.badge.setMenu(menu)
        menu = QMenu()
        name_list = ['Shining Star Footmark', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.footmark, name, 89)
        self.ui.footmark.setMenu(menu)
        menu = QMenu()
        name_list = ['Heat Wave Title Emblem', 'Mingjin Title Emblem', 'Demon Sickle Emblem', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.title_2, name, 90)
        self.ui.title_2.setMenu(menu)
        menu = QMenu()
        name_list = ['Mingjin Weapon Emblem', 'Demon Sickle Emblem', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.weapon_2, name, 91)
        self.ui.weapon_2.setMenu(menu)
        menu = QMenu()
        name_list = ['Star God Aura Emblem', 'Mingjin Aura Emblem', 'Demon Sickle Emblem', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.aureole_2, name, 92)
        self.ui.aureole_2.setMenu(menu)
        menu = QMenu()
        name_list = ['Mingjin Head Emblem', 'Demon Sickle Emblem', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.headwear_2, name, 93)
        self.ui.headwear_2.setMenu(menu)
        menu = QMenu()
        name_list = ['Mingjin Armor Emblem', 'Demon Sickle Emblem', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.cloth_2, name, 94)
        self.ui.cloth_2.setMenu(menu)
        menu = QMenu()
        name_list = ['Mingjin Accessory Emblem', 'Demon Sickle Emblem', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.accessory_2, name, 95)
        self.ui.accessory_2.setMenu(menu)
        menu = QMenu()
        name_list = ['Demon Sickle Emblem', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.facewear_2, name, 96)
        self.ui.facewear_2.setMenu(menu)
        menu = QMenu()
        name_list = ['Demon Sickle Emblem', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.badge_2, name, 97)
        self.ui.badge_2.setMenu(menu)
        menu = QMenu()
        name_list = ['Mingjin Footmark Emblem', 'Demon Sickle Emblem', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.footmark_2, name, 98)
        self.ui.footmark_2.setMenu(menu)
        menu = QMenu()
        name_list = ['22 Elem Potion', '25 Elem Potion', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.buff_stats, name, 99)
        self.ui.buff_stats.setMenu(menu)
        menu = QMenu()
        name_list = ['8 Crit', '6 Counter', '8 Skill Dmg', '8 Atk', '10 Crit Dmg', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.buff_atk, name, 100)
        self.ui.buff_atk.setMenu(menu)
        menu = QMenu()
        name_list = ['Morning', 'Cliff', 'East', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.buff_wine, name, 101)
        self.ui.buff_wine.setMenu(menu)
        menu = QMenu()
        name_list = ['Dragon Breath', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.buff_dragon, name, 102)
        self.ui.buff_dragon.setMenu(menu)
        menu = QMenu()
        name_list = ['Gale', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.buff_wind, name, 103)
        self.ui.buff_wind.setMenu(menu)
        menu = QMenu()
        name_list = ['Mine War', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.buff_mine, name, 104)
        self.ui.buff_mine.setMenu(menu)
        menu = QMenu()
        name_list = ['Counter', 'None']
        for name in name_list:
            self.add_menu(menu, self.ui.buff_counter, name, 105)
        self.ui.buff_counter.setMenu(menu)
        self._setup_menus()
        self.ui.save.clicked.connect(self.save)
        self.ui.load.clicked.connect(self.load)
        self.ui.compute.clicked.connect(self.compute_damage_new)

    def _setup_menus(self):
        engrave_transcendence = ['Transcendence 3', 'Adaptation 3', 'Destruction 3', 'Swiftness 3', 'Combo 3', 'Transcendence 2', 'Adaptation 2', 'Destruction 2', 'Swiftness 2', 'Combo 2', 'Transcendence 1', 'Adaptation 1', 'Destruction 1', 'Swiftness 1', 'Combo 1', 'None']
        engrave_extraordinary = ['Extraordinary 3', 'Tempering 3', 'High-Tier 3', 'Status Break 3', 'Basic 3', 'Pierce 3', 'Fortification 3', 'Extraordinary 2', 'Tempering 2', 'High-Tier 2', 'Status Break 2', 'Basic 2', 'Pierce 2', 'Fortification 2', 'Extraordinary 1', 'Tempering 1', 'High-Tier 1', 'Status Break 1', 'Basic 1', 'Pierce 1', 'Fortification 1', 'None']
        engrave_excellence = ['Excellence 3', 'Smite 3', 'Alliance 3', 'Unbreakable 3', 'Excellence 2', 'Smite 2', 'Alliance 2', 'Unbreakable 2', 'Excellence 1', 'Smite 1', 'Alliance 1', 'Unbreakable 1', 'None']
        engrave_elem_master = ['Elem Master 3', 'Challenger 3', 'Resonance 3', 'Evasion 3', 'Elem Resist 3', 'Recovery 3', 'Elem Master 2', 'Challenger 2', 'Resonance 2', 'Evasion 2', 'Elem Resist 2', 'Recovery 2', 'Elem Master 1', 'Challenger 1', 'Resonance 1', 'Evasion 1', 'Elem Resist 1', 'Recovery 1', 'None']
        enhancement_str_int = ['+15(Str_Int)', '+16(Str_Int)', '+17(Str_Int)', '+18(Str_Int)', '+19(Str_Int)', '+20(Str_Int)', '+21(Str_Int)', '+22(Str_Int)', '+23(Str_Int)', '+24(Str_Int)', '+25(Str_Int)', 'None']
        enhancement_hp = ['+15(HP)', '+16(HP)', '+17(HP)', '+18(HP)', '+19(HP)', '+20(HP)', '+21(HP)', '+22(HP)', '+23(HP)', '+24(HP)', '+25(HP)', 'None']
        enhancement_lr = ['+15(L_R Slot)', '+16(L_R Slot)', '+17(L_R Slot)', '+18(L_R Slot)', '+19(L_R Slot)', '+20(L_R Slot)', '+21(L_R Slot)', '+22(L_R Slot)', '+23(L_R Slot)', '+24(L_R Slot)', '+25(L_R Slot)', 'None']
        card_list = ['Loyal Partner', 'The evil hook', 'Void Shadow', 'Chrome Arms', 'Ancient Guardian', 'Deep Space Swarm', 'Realm Creature', 'Magic Era', 'Dark Realm Madman', 'Light Chaser', 'Clockwork Legion', 'Mech Empire', 'Beast Legion', 'Gloomy Forbidden Area', 'Park Guard', 'None']
        pet_list = ['Cat', 'Eagle', 'Panda', 'Dragon', 'PiaoPiao', 'Koto', 'Fox', 'None']

        menu_configs = [
            (self.ui.equip_head, 0, ['Black Feather Head', 'Glimmer Head', 'Avarice Head', 'Venom Head', 'Butterfly Head', 'Demon Heart Head', 'Cursed Head', 'None']),
            (self.ui.equip_armor, 1, ['Black Feather Armor', 'Glimmer Armor', 'Avarice Armor', 'Venom Armor', 'Butterfly Armor', 'Demon Heart Armor', 'Cursed Armor', 'None']),
            (self.ui.equip_hand, 2, ['Black Feather Hand', 'Glimmer Hand', 'Avarice Hand', 'Venom Hand', 'Butterfly Hand', 'Demon Heart Hand', 'Cursed Hand', 'None']),
            (self.ui.equip_leg, 3, ['Black Feather Legs', 'Glimmer Legs', 'Avarice Legs', 'Venom Legs', 'Butterfly Legs', 'Demon Heart Legs', 'Cursed Legs', 'None']),
            (self.ui.equip_shoe, 4, ['Black Feather Shoes', 'Glimmer Shoes', 'Avarice Shoes', 'Venom Shoes', 'Butterfly Shoes', 'Demon Heart Shoes', 'Cursed Shoes', 'None']),
            (self.ui.equip_weapon, 5, ['True Fate Sickle (Withered)', 'Abyssal Gaze', 'Desperate Dream Song', 'None']),
            (self.ui.equip_necklace, 6, ['Solar Necklace', 'Holy Glory Necklace', 'Demon Shadow Necklace', 'None']),
            (self.ui.equip_bracer, 7, ['Solar Bracer', 'Holy Glory Bracer', 'Demon Shadow Bracer', 'None']),
            (self.ui.equip_ring, 8, ['Solar Ring', 'Holy Glory Ring', 'Demon Shadow Ring', 'None']),
            (self.ui.equip_seal, 9, ['Solar Seal', 'Holy Glory Seal', 'Demon Shadow Seal', 'None']),
            (self.ui.equip_amulet, 10, ['Solar Amulet', 'Holy Glory Amulet', 'Demon Shadow Amulet', 'None']),
            (self.ui.equip_treasure, 11, ["Hourglass of World's End", 'Hymn of Ancient Demon God', 'None']),
            (self.ui.emblem_head, 12, ['Soldier', 'Chariot', 'King', 'Plague', 'Glimmer Venom Wing', 'Andre', 'Isaac', 'None']),
            (self.ui.emblem_armor, 13, ['Eclipse Creator', 'Centaur', 'Bishop', 'King', 'Charlotte', 'Heavy Shield', 'Odisha', 'None']),
            (self.ui.emblem_hand, 14, ['Soldier', 'Centaur', 'Bishop', 'Chariot', 'Queen', 'Skull', 'Bogit', 'Ice Fist (Vic)', 'Isaac', 'None']),
            (self.ui.emblem_leg, 15, ['Mars', 'Venom Behemoth', 'Goramos', 'Odisha', 'None']),
            (self.ui.emblem_shoe, 16, ['Eclipse Creator', 'Queen', 'Famion', 'Touch of Greed', 'Electric Whip (Joker)', 'Isaac', 'None']),
            (self.ui.emblem_weapon, 17, ['Elem Mark', 'Verbena', 'Hawk', 'Demon Heart Kraken', 'None']),
            (self.ui.emblem_necklace, 18, ['Michael', 'Sword of Power', 'Electric Whip (Joker)', 'Thunder Light', 'Gorga', 'None']),
            (self.ui.emblem_bracer, 19, ['Michael', 'Sword of Power', 'Ice Fist (Vic)', 'Thunder Light', 'Gorga', 'None']),
            (self.ui.emblem_ring, 20, ['Mars', 'Andre', 'Gorga', 'None']),
            (self.ui.emblem_seal, 21, ['Azrael', 'Plague', 'Puzzle', 'Goramos', 'None']),
            (self.ui.emblem_amulet, 22, ['Azrael', 'Famion', 'Puzzle', 'Heavy Shield', 'None']),
            (self.ui.enhancement_head, 23, enhancement_str_int),
            (self.ui.enhancement_armor, 24, enhancement_hp),
            (self.ui.enhancement_hand, 25, enhancement_str_int),
            (self.ui.enhancement_leg, 26, enhancement_hp),
            (self.ui.enhancement_shoe, 27, enhancement_str_int),
            (self.ui.enhancement_weapon, 28, ['+18(Weapon)', '+19(Weapon)', '+20(Weapon)', '+21(Weapon)', '+22(Weapon)', '+23(Weapon)', '+24(Weapon)', '+25(Weapon)', 'None']),
            (self.ui.enhancement_necklace, 29, enhancement_str_int),
            (self.ui.enhancement_bracer, 30, enhancement_str_int),
            (self.ui.enhancement_ring, 31, enhancement_str_int),
            (self.ui.enhancement_seal, 32, enhancement_lr),
            (self.ui.enhancement_amulet, 33, enhancement_lr),
            (self.ui.engrave_head_1, 34, engrave_transcendence),
            (self.ui.engrave_head_2, 35, engrave_transcendence),
            (self.ui.engrave_head_3, 36, engrave_transcendence),
            (self.ui.engrave_armor_1, 37, engrave_extraordinary),
            (self.ui.engrave_armor_2, 38, engrave_extraordinary),
            (self.ui.engrave_armor_3, 39, engrave_extraordinary),
            (self.ui.engrave_hand_1, 40, engrave_transcendence),
            (self.ui.engrave_hand_2, 41, engrave_transcendence),
            (self.ui.engrave_hand_3, 42, engrave_transcendence),
            (self.ui.engrave_leg_1, 43, engrave_extraordinary),
            (self.ui.engrave_leg_2, 44, engrave_extraordinary),
            (self.ui.engrave_leg_3, 45, engrave_extraordinary),
            (self.ui.engrave_shoe_1, 46, engrave_transcendence),
            (self.ui.engrave_shoe_2, 47, engrave_transcendence),
            (self.ui.engrave_shoe_3, 48, engrave_transcendence),
            (self.ui.engrave_weapon_1, 49, engrave_excellence),
            (self.ui.engrave_weapon_2, 50, engrave_excellence),
            (self.ui.engrave_weapon_3, 51, engrave_excellence),
            (self.ui.engrave_necklace_1, 52, engrave_elem_master),
            (self.ui.engrave_necklace_2, 53, engrave_elem_master),
            (self.ui.engrave_necklace_3, 54, engrave_elem_master),
            (self.ui.engrave_bracer_1, 55, engrave_elem_master),
            (self.ui.engrave_bracer_2, 56, engrave_elem_master),
            (self.ui.engrave_bracer_3, 57, engrave_elem_master),
            (self.ui.engrave_ring_1, 58, engrave_elem_master),
            (self.ui.engrave_ring_2, 59, engrave_elem_master),
            (self.ui.engrave_ring_3, 60, engrave_elem_master),
            (self.ui.engrave_seal_1, 61, engrave_excellence),
            (self.ui.engrave_seal_2, 62, engrave_excellence),
            (self.ui.engrave_seal_3, 63, engrave_excellence),
            (self.ui.engrave_amulet_1, 64, engrave_excellence),
            (self.ui.engrave_amulet_2, 65, engrave_excellence),
            (self.ui.engrave_amulet_3, 66, engrave_excellence),
            (self.ui.pet_1, 67, pet_list),
            (self.ui.pet_2, 68, pet_list),
            (self.ui.pet_level_1, 69, ['1 Star', '2 Star', '3 Star', 'None']),
            (self.ui.pet_level_2, 70, ['1 Star', '2 Star', '3 Star', 'None']),
            (self.ui.pet_emblem_1_1, 71, ['Cat Paw', 'Emperor Thorn', 'Insight Eye', 'None']),
            (self.ui.pet_emblem_2_1, 72, ['Cat Paw', 'Emperor Thorn', 'Insight Eye', 'None']),
            (self.ui.pet_emblem_1_2, 73, ['Magic Witch', 'Beast Tooth Mark', 'None']),
            (self.ui.pet_emblem_2_2, 74, ['Magic Witch', 'Beast Tooth Mark', 'None']),
            (self.ui.pet_emblem_1_3, 75, ['Wind Butterfly', 'Maple Curse', 'None']),
            (self.ui.pet_emblem_2_3, 76, ['Wind Butterfly', 'Maple Curse', 'None']),
            (self.ui.card_1, 77, card_list),
            (self.ui.card_2, 78, card_list),
            (self.ui.card_3, 79, card_list),
            (self.ui.card_4, 80, card_list),
            (self.ui.title, 81, ['Demon Touch', 'Void Crown', 'Gold Crown', 'None']),
            (self.ui.weapon, 82, ['Sun Decree Seat', 'S-Rank Fashion Weapon', 'None']),
            (self.ui.aureole, 83, ['Shining Star', 'Golden Slumber', 'Eclipse Realm', 'Eclipse Realm II', 'None']),
            (self.ui.headwear, 84, ['New Sky Head', 'Old Sky Head', 'None']),
            (self.ui.cloth, 85, ['New Sky Armor', 'Old Sky Armor', 'None']),
            (self.ui.accessory, 86, ['New Sky Accessory', 'Old Sky Accessory', 'None']),
            (self.ui.facewear, 87, ['New Sky Facewear', 'Old Sky Facewear', 'None']),
            (self.ui.badge, 88, ['New Sky Badge', 'Old Sky Badge', 'None']),
            (self.ui.footmark, 89, ['Shining Star Footmark', 'None']),
            (self.ui.title_2, 90, ['Heat Wave Title Emblem', 'Mingjin Title Emblem', 'Demon Sickle Emblem', 'None']),
            (self.ui.weapon_2, 91, ['Mingjin Weapon Emblem', 'Demon Sickle Emblem', 'None']),
            (self.ui.aureole_2, 92, ['Star God Aura Emblem', 'Mingjin Aura Emblem', 'Demon Sickle Emblem', 'None']),
            (self.ui.headwear_2, 93, ['Mingjin Head Emblem', 'Demon Sickle Emblem', 'None']),
            (self.ui.cloth_2, 94, ['Mingjin Armor Emblem', 'Demon Sickle Emblem', 'None']),
            (self.ui.accessory_2, 95, ['Mingjin Accessory Emblem', 'Demon Sickle Emblem', 'None']),
            (self.ui.facewear_2, 96, ['Demon Sickle Emblem', 'None']),
            (self.ui.badge_2, 97, ['Demon Sickle Emblem', 'None']),
            (self.ui.footmark_2, 98, ['Mingjin Footmark Emblem', 'Demon Sickle Emblem', 'None']),
            (self.ui.buff_stats, 99, ['22 Elem Potion', '25 Elem Potion', 'None']),
            (self.ui.buff_atk, 100, ['8 Crit', '6 Counter', '8 Skill Dmg', '8 Atk', '10 Crit Dmg', 'None']),
            (self.ui.buff_wine, 101, ['Morning', 'Cliff', 'East', 'None']),
            (self.ui.buff_dragon, 102, ['Dragon Breath', 'None']),
            (self.ui.buff_wind, 103, ['Gale', 'None']),
            (self.ui.buff_mine, 104, ['Mine War', 'None']),
            (self.ui.buff_counter, 105, ['Counter', 'None']),
        ]

        for button, rank, name_list in menu_configs:
            menu = QMenu()
            for name in name_list:
                self.add_menu(menu, button, name, rank)
            button.setMenu(menu)

    def add_menu(self, menu: QMenu, button: QPushButton, name: str, rank: int):
        action = QAction(name, self)
        action.triggered.connect(lambda: self.trans_equipment(button, name, rank))
        menu.addAction(action)
        return menu
    def set_icon(self, button: QPushButton, equipment_list: list, rank: int):
        button.setText('')
        name = equipment_list[rank]
        button.setIcon(QIcon('icon\\' + name + '.png'))
        button.setIconSize(QSize(100, 50))
    def trans_equipment(self, button: QPushButton, name: str, rank: int):
        button.setText('')
        button.setIcon(QIcon('icon\\' + name + '.png'))
        button.setIconSize(QSize(100, 50))
        self.current_equipment[rank] = name
    def save(self):
        self.current_equipment[106] = str(self.ui.dot_ratio.value())
        self.current_equipment[107] = str(self.ui.loop_atk.value())
        self.current_equipment[108] = str(self.ui.loop_critical_damage.value())
        self.current_equipment[109] = str(self.ui.loop_critical.value())
        self.current_equipment[110] = str(self.ui.loop_stats.value())
        self.current_equipment[111] = str(self.ui.loop_cd.value())
        self.current_equipment[112] = str(self.ui.loop_agility.value())
        self.current_equipment[113] = str(self.ui.loop_strength.value())
        self.current_equipment[114] = str(self.ui.loop_skill_damage.value())
        self.current_equipment[115] = str(self.ui.boost_bufan4.value())
        self.current_equipment[116] = str(self.ui.boost_bufan6.value())
        self.current_equipment[117] = str(self.ui.boost_zhuoyue4.value())
        self.current_equipment[118] = str(self.ui.boost_zhuoyue7.value())
        self.current_equipment[119] = str(self.ui.boost_zhuoyue9.value())
        self.current_equipment[120] = str(self.ui.boost_chaoran9.value())
        self.current_equipment[121] = str(self.ui.atk_boost.value())
        self.current_equipment[122] = str(self.ui.car_level.value())
        self.previous_equipment = self.current_equipment
        with open('save.txt', 'w', encoding='utf-8') as file:
            for i in range(len(self.previous_equipment)):
                s = self.previous_equipment[i] + '\n'
                file.write(s)
        self.compute_damage_old()
        self.compute_damage_new()
    def load(self):
        with open('save.txt', 'r', encoding='utf-8') as file:
            self.previous_equipment = file.readlines()
        for i in range(len(self.previous_equipment)):
            self.previous_equipment[i] = self.previous_equipment[i][:(-1)]
        if len(self.previous_equipment) < len(self.default_equipment):
            self.previous_equipment += self.default_equipment[len(self.previous_equipment):]
        self.current_equipment = self.previous_equipment
        self.set_icon(self.ui.equip_head, self.current_equipment, 0)
        self.set_icon(self.ui.equip_armor, self.current_equipment, 1)
        self.set_icon(self.ui.equip_hand, self.current_equipment, 2)
        self.set_icon(self.ui.equip_leg, self.current_equipment, 3)
        self.set_icon(self.ui.equip_shoe, self.current_equipment, 4)
        self.set_icon(self.ui.equip_weapon, self.current_equipment, 5)
        self.set_icon(self.ui.equip_necklace, self.current_equipment, 6)
        self.set_icon(self.ui.equip_bracer, self.current_equipment, 7)
        self.set_icon(self.ui.equip_ring, self.current_equipment, 8)
        self.set_icon(self.ui.equip_seal, self.current_equipment, 9)
        self.set_icon(self.ui.equip_amulet, self.current_equipment, 10)
        self.set_icon(self.ui.equip_treasure, self.current_equipment, 11)
        self.set_icon(self.ui.emblem_head, self.current_equipment, 12)
        self.set_icon(self.ui.emblem_armor, self.current_equipment, 13)
        self.set_icon(self.ui.emblem_hand, self.current_equipment, 14)
        self.set_icon(self.ui.emblem_leg, self.current_equipment, 15)
        self.set_icon(self.ui.emblem_shoe, self.current_equipment, 16)
        self.set_icon(self.ui.emblem_weapon, self.current_equipment, 17)
        self.set_icon(self.ui.emblem_necklace, self.current_equipment, 18)
        self.set_icon(self.ui.emblem_bracer, self.current_equipment, 19)
        self.set_icon(self.ui.emblem_ring, self.current_equipment, 20)
        self.set_icon(self.ui.emblem_seal, self.current_equipment, 21)
        self.set_icon(self.ui.emblem_amulet, self.current_equipment, 22)
        self.set_icon(self.ui.enhancement_head, self.current_equipment, 23)
        self.set_icon(self.ui.enhancement_armor, self.current_equipment, 24)
        self.set_icon(self.ui.enhancement_hand, self.current_equipment, 25)
        self.set_icon(self.ui.enhancement_leg, self.current_equipment, 26)
        self.set_icon(self.ui.enhancement_shoe, self.current_equipment, 27)
        self.set_icon(self.ui.enhancement_weapon, self.current_equipment, 28)
        self.set_icon(self.ui.enhancement_necklace, self.current_equipment, 29)
        self.set_icon(self.ui.enhancement_bracer, self.current_equipment, 30)
        self.set_icon(self.ui.enhancement_ring, self.current_equipment, 31)
        self.set_icon(self.ui.enhancement_seal, self.current_equipment, 32)
        self.set_icon(self.ui.enhancement_amulet, self.current_equipment, 33)
        self.set_icon(self.ui.engrave_head_1, self.current_equipment, 34)
        self.set_icon(self.ui.engrave_head_2, self.current_equipment, 35)
        self.set_icon(self.ui.engrave_head_3, self.current_equipment, 36)
        self.set_icon(self.ui.engrave_armor_1, self.current_equipment, 37)
        self.set_icon(self.ui.engrave_armor_2, self.current_equipment, 38)
        self.set_icon(self.ui.engrave_armor_3, self.current_equipment, 39)
        self.set_icon(self.ui.engrave_hand_1, self.current_equipment, 40)
        self.set_icon(self.ui.engrave_hand_2, self.current_equipment, 41)
        self.set_icon(self.ui.engrave_hand_3, self.current_equipment, 42)
        self.set_icon(self.ui.engrave_leg_1, self.current_equipment, 43)
        self.set_icon(self.ui.engrave_leg_2, self.current_equipment, 44)
        self.set_icon(self.ui.engrave_leg_3, self.current_equipment, 45)
        self.set_icon(self.ui.engrave_shoe_1, self.current_equipment, 46)
        self.set_icon(self.ui.engrave_shoe_2, self.current_equipment, 47)
        self.set_icon(self.ui.engrave_shoe_3, self.current_equipment, 48)
        self.set_icon(self.ui.engrave_weapon_1, self.current_equipment, 49)
        self.set_icon(self.ui.engrave_weapon_2, self.current_equipment, 50)
        self.set_icon(self.ui.engrave_weapon_3, self.current_equipment, 51)
        self.set_icon(self.ui.engrave_necklace_1, self.current_equipment, 52)
        self.set_icon(self.ui.engrave_necklace_2, self.current_equipment, 53)
        self.set_icon(self.ui.engrave_necklace_3, self.current_equipment, 54)
        self.set_icon(self.ui.engrave_bracer_1, self.current_equipment, 55)
        self.set_icon(self.ui.engrave_bracer_2, self.current_equipment, 56)
        self.set_icon(self.ui.engrave_bracer_3, self.current_equipment, 57)
        self.set_icon(self.ui.engrave_ring_1, self.current_equipment, 58)
        self.set_icon(self.ui.engrave_ring_2, self.current_equipment, 59)
        self.set_icon(self.ui.engrave_ring_3, self.current_equipment, 60)
        self.set_icon(self.ui.engrave_seal_1, self.current_equipment, 61)
        self.set_icon(self.ui.engrave_seal_2, self.current_equipment, 62)
        self.set_icon(self.ui.engrave_seal_3, self.current_equipment, 63)
        self.set_icon(self.ui.engrave_amulet_1, self.current_equipment, 64)
        self.set_icon(self.ui.engrave_amulet_2, self.current_equipment, 65)
        self.set_icon(self.ui.engrave_amulet_3, self.current_equipment, 66)
        self.set_icon(self.ui.pet_1, self.current_equipment, 67)
        self.set_icon(self.ui.pet_2, self.current_equipment, 68)
        self.set_icon(self.ui.pet_level_1, self.current_equipment, 69)
        self.set_icon(self.ui.pet_level_2, self.current_equipment, 70)
        self.set_icon(self.ui.pet_emblem_1_1, self.current_equipment, 71)
        self.set_icon(self.ui.pet_emblem_2_1, self.current_equipment, 72)
        self.set_icon(self.ui.pet_emblem_1_2, self.current_equipment, 73)
        self.set_icon(self.ui.pet_emblem_2_2, self.current_equipment, 74)
        self.set_icon(self.ui.pet_emblem_1_3, self.current_equipment, 75)
        self.set_icon(self.ui.pet_emblem_2_3, self.current_equipment, 76)
        self.set_icon(self.ui.card_1, self.current_equipment, 77)
        self.set_icon(self.ui.card_2, self.current_equipment, 78)
        self.set_icon(self.ui.card_3, self.current_equipment, 79)
        self.set_icon(self.ui.card_4, self.current_equipment, 80)
        self.set_icon(self.ui.title, self.current_equipment, 81)
        self.set_icon(self.ui.weapon, self.current_equipment, 82)
        self.set_icon(self.ui.aureole, self.current_equipment, 83)
        self.set_icon(self.ui.headwear, self.current_equipment, 84)
        self.set_icon(self.ui.cloth, self.current_equipment, 85)
        self.set_icon(self.ui.accessory, self.current_equipment, 86)
        self.set_icon(self.ui.facewear, self.current_equipment, 87)
        self.set_icon(self.ui.badge, self.current_equipment, 88)
        self.set_icon(self.ui.footmark, self.current_equipment, 89)
        self.set_icon(self.ui.title_2, self.current_equipment, 90)
        self.set_icon(self.ui.weapon_2, self.current_equipment, 91)
        self.set_icon(self.ui.aureole_2, self.current_equipment, 92)
        self.set_icon(self.ui.headwear_2, self.current_equipment, 93)
        self.set_icon(self.ui.cloth_2, self.current_equipment, 94)
        self.set_icon(self.ui.accessory_2, self.current_equipment, 95)
        self.set_icon(self.ui.facewear_2, self.current_equipment, 96)
        self.set_icon(self.ui.badge_2, self.current_equipment, 97)
        self.set_icon(self.ui.footmark_2, self.current_equipment, 98)
        self.set_icon(self.ui.buff_stats, self.current_equipment, 99)
        self.set_icon(self.ui.buff_atk, self.current_equipment, 100)
        self.set_icon(self.ui.buff_wine, self.current_equipment, 101)
        self.set_icon(self.ui.buff_dragon, self.current_equipment, 102)
        self.set_icon(self.ui.buff_wind, self.current_equipment, 103)
        self.set_icon(self.ui.buff_mine, self.current_equipment, 104)
        self.set_icon(self.ui.buff_counter, self.current_equipment, 105)

        # Create a list of all icon buttons in order
        icon_buttons = [
            self.ui.equip_head, self.ui.equip_armor, self.ui.equip_hand, self.ui.equip_leg, self.ui.equip_shoe,
            self.ui.equip_weapon, self.ui.equip_necklace, self.ui.equip_bracer, self.ui.equip_ring, self.ui.equip_seal, self.ui.equip_amulet,
            self.ui.equip_treasure, self.ui.emblem_head, self.ui.emblem_armor, self.ui.emblem_hand, self.ui.emblem_leg, self.ui.emblem_shoe,
            self.ui.emblem_weapon, self.ui.emblem_necklace, self.ui.emblem_bracer, self.ui.emblem_ring, self.ui.emblem_seal, self.ui.emblem_amulet,
            self.ui.enhancement_head, self.ui.enhancement_armor, self.ui.enhancement_hand, self.ui.enhancement_leg, self.ui.enhancement_shoe,
            self.ui.enhancement_weapon, self.ui.enhancement_necklace, self.ui.enhancement_bracer, self.ui.enhancement_ring, self.ui.enhancement_seal, self.ui.enhancement_amulet,
            self.ui.engrave_head_1, self.ui.engrave_head_2, self.ui.engrave_head_3, self.ui.engrave_armor_1, self.ui.engrave_armor_2, self.ui.engrave_armor_3,
            self.ui.engrave_hand_1, self.ui.engrave_hand_2, self.ui.engrave_hand_3, self.ui.engrave_leg_1, self.ui.engrave_leg_2, self.ui.engrave_leg_3,
            self.ui.engrave_shoe_1, self.ui.engrave_shoe_2, self.ui.engrave_shoe_3, self.ui.engrave_weapon_1, self.ui.engrave_weapon_2, self.ui.engrave_weapon_3,
            self.ui.engrave_necklace_1, self.ui.engrave_necklace_2, self.ui.engrave_necklace_3, self.ui.engrave_bracer_1, self.ui.engrave_bracer_2, self.ui.engrave_bracer_3,
            self.ui.engrave_ring_1, self.ui.engrave_ring_2, self.ui.engrave_ring_3, self.ui.engrave_seal_1, self.ui.engrave_seal_2, self.ui.engrave_seal_3,
            self.ui.engrave_amulet_1, self.ui.engrave_amulet_2, self.ui.engrave_amulet_3, self.ui.pet_1, self.ui.pet_2, self.ui.pet_level_1, self.ui.pet_level_2,
            self.ui.pet_emblem_1_1, self.ui.pet_emblem_2_1, self.ui.pet_emblem_1_2, self.ui.pet_emblem_2_2, self.ui.pet_emblem_1_3, self.ui.pet_emblem_2_3,
            self.ui.card_1, self.ui.card_2, self.ui.card_3, self.ui.card_4, self.ui.title, self.ui.weapon, self.ui.aureole, self.ui.headwear, self.ui.cloth,
            self.ui.accessory, self.ui.facewear, self.ui.badge, self.ui.footmark, self.ui.title_2, self.ui.weapon_2, self.ui.aureole_2, self.ui.headwear_2,
            self.ui.cloth_2, self.ui.accessory_2, self.ui.facewear_2, self.ui.badge_2, self.ui.footmark_2, self.ui.buff_stats, self.ui.buff_atk,
            self.ui.buff_wine, self.ui.buff_dragon, self.ui.buff_wind, self.ui.buff_mine, self.ui.buff_counter
        ]

        for i, button in enumerate(icon_buttons):
            self.set_icon(button, self.current_equipment, i)

        self.ui.dot_ratio.setValue(float(self.current_equipment[106]))
        self.ui.loop_atk.setValue(int(self.current_equipment[107]))
        self.ui.loop_critical_damage.setValue(float(self.current_equipment[108]))
        self.ui.loop_critical.setValue(float(self.current_equipment[109]))
        self.ui.loop_stats.setValue(float(self.current_equipment[110]))
        self.ui.loop_cd.setValue(float(self.current_equipment[111]))
        self.ui.loop_agility.setValue(int(self.current_equipment[112]))
        self.ui.loop_strength.setValue(int(self.current_equipment[113]))
        self.ui.loop_skill_damage.setValue(int(self.current_equipment[114]))
        self.ui.boost_bufan4.setValue(float(self.current_equipment[115]))
        self.ui.boost_bufan6.setValue(float(self.current_equipment[116]))
        self.ui.boost_zhuoyue4.setValue(float(self.current_equipment[117]))
        self.ui.boost_zhuoyue7.setValue(float(self.current_equipment[118]))
        self.ui.boost_zhuoyue9.setValue(float(self.current_equipment[119]))
        self.ui.boost_chaoran9.setValue(float(self.current_equipment[120]))
        self.ui.atk_boost.setValue(float(self.current_equipment[121]))
        self.ui.car_level.setValue(int(float(self.current_equipment[122])))
        self.compute_damage_old()
        self.compute_damage_new()
    def compute_damage_new(self):
        self.current_equipment[106] = str(self.ui.dot_ratio.value())
        self.current_equipment[107] = str(self.ui.loop_atk.value())
        self.current_equipment[108] = str(self.ui.loop_critical_damage.value())
        self.current_equipment[109] = str(self.ui.loop_critical.value())
        self.current_equipment[110] = str(self.ui.loop_stats.value())
        self.current_equipment[111] = str(self.ui.loop_cd.value())
        self.current_equipment[112] = str(self.ui.loop_agility.value())
        self.current_equipment[113] = str(self.ui.loop_strength.value())
        self.current_equipment[114] = str(self.ui.loop_skill_damage.value())
        self.current_equipment[115] = str(self.ui.boost_bufan4.value())
        self.current_equipment[116] = str(self.ui.boost_bufan6.value())
        self.current_equipment[117] = str(self.ui.boost_zhuoyue4.value())
        self.current_equipment[118] = str(self.ui.boost_zhuoyue7.value())
        self.current_equipment[119] = str(self.ui.boost_zhuoyue9.value())
        self.current_equipment[120] = str(self.ui.boost_chaoran9.value())
        self.current_equipment[121] = str(self.ui.atk_boost.value())
        self.current_equipment[122] = str(self.ui.car_level.value())
        final_status, burst_damage, total_damage = self.compute_damage(self.current_equipment)
        self.ui.new_stats.setText(str(int(final_status['Elem Boost'])))
        self.ui.new_critical.setText(str('%.1f' % final_status['Crit Rate']))
        self.ui.new_critical_damage.setText(str(int(final_status['Crit Dmg'])))
        self.ui.new_counter.setText(str(int(final_status['Counter'])))
        self.ui.new_damage_amp.setText(str(int(final_status['Dmg Amp'])))
        self.ui.new_skill_damage.setText(str(int(final_status['Skill Dmg'])))
        self.ui.new_resonance_damage.setText(str(int(final_status['Resonance Dmg'])))
        self.ui.new_stats_damage.setText(str('%.1f' % final_status['Elem Dmg']))
        self.ui.new_pure_atk.setText(str(int(final_status['Def Break Atk'])))
        self.ui.new_atk.setText(str(int(final_status['Atk'])))
        self.ui.new_addition_damage.setText(str(int(final_status['Extra Dmg'])))
        self.ui.new_spetial_damage.setText(str(int(final_status['Special'])))
        self.ui.new_shuangyue.setText(str(int(final_status['Class Dmg'])))
        self.ui.new_amp.setText(str(int(final_status['Multiplier'])))
        self.ui.new_skill_amp.setText(str(int(final_status['Skill Dmg Boost'])))
        self.ui.new_skill_acc.setText(str(int(final_status['Skill Haste'])))
        self.ui.new_cd_reduction.setText(str('%.1f' % final_status['Cooldown Reduction']))
        self.ui.new_dot_ratio.setText(str(int(final_status['Effect Ratio'])))
        self.ui.new_defense_ignore.setText(str(int(final_status['Penetration'])))
        self.ui.new_defense_reduction.setText(str(int(final_status['Def Shred'])))
        self.ui.new_burst_damage.setText(str(int(burst_damage)))
        self.ui.new_total_damage.setText(str(int(total_damage)))
        if self.ui.old_total_damage.toPlainText()!= '':
            boost = (total_damage / int(self.ui.old_total_damage.toPlainText()) - 1) * 100
            self.ui.boost_ratio.setText(str('%.4f' % boost))
        if self.ui.old_burst_damage.toPlainText()!= '':
            boost = (burst_damage / int(self.ui.old_burst_damage.toPlainText()) - 1) * 100
            self.ui.boost_ratio_burst.setText(str('%.4f' % boost))
    def compute_damage_old(self):
        final_status, burst_damage, total_damage = self.compute_damage(self.current_equipment)
        self.ui.old_stats.setText(str(int(final_status['Elem Boost'])))
        self.ui.old_critical.setText(str('%.1f' % final_status['Crit Rate']))
        self.ui.old_critical_damage.setText(str(int(final_status['Crit Dmg'])))
        self.ui.old_counter.setText(str(int(final_status['Counter'])))
        self.ui.old_damage_amp.setText(str(int(final_status['Dmg Amp'])))
        self.ui.old_skill_damage.setText(str(int(final_status['Skill Dmg'])))
        self.ui.old_resonance_damage.setText(str(int(final_status['Resonance Dmg'])))
        self.ui.old_stats_damage.setText(str('%.1f' % final_status['Elem Dmg']))
        self.ui.old_pure_atk.setText(str(int(final_status['Def Break Atk'])))
        self.ui.old_atk.setText(str(int(final_status['Atk'])))
        self.ui.old_addition_damage.setText(str(int(final_status['Extra Dmg'])))
        self.ui.old_spetial_damage.setText(str(int(final_status['Special'])))
        self.ui.old_shuangyue.setText(str(int(final_status['Class Dmg'])))
        self.ui.old_amp.setText(str(int(final_status['Multiplier'])))
        self.ui.old_skill_amp.setText(str(int(final_status['Skill Dmg Boost'])))
        self.ui.old_skill_acc.setText(str(int(final_status['Skill Haste'])))
        self.ui.old_cd_reduction.setText(str('%.1f' % final_status['Cooldown Reduction']))
        self.ui.old_dot_ratio.setText(str(int(final_status['Effect Ratio'])))
        self.ui.old_defense_ignore.setText(str(int(final_status['Penetration'])))
        self.ui.old_defense_reduction.setText(str(int(final_status['Def Shred'])))
        self.ui.old_burst_damage.setText(str(int(burst_damage)))
        self.ui.old_total_damage.setText(str(int(total_damage)))
    def compute_damage(self, equipment):
        equipment_list = equipment.copy()
        equipment_list[67] = equipment_list[69] + equipment_list[67]
        equipment_list[68] = equipment_list[70] + equipment_list[68]
        del equipment_list[70]
        del equipment_list[69]
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        base_status = {'Elem Boost': 0, 'Crit Rate': 0, 'Crit Dmg': 56, 'Counter': 0, 'Dmg Amp': 3, 'Skill Dmg': 0, 'Resonance Dmg': 20, 'Elem Dmg': 0, 'Base Atk': 201, 'Atk Bonus': 0, 'Strength': 685, 'Agility': 445, 'Str Bonus': 0, 'Def Break Atk': 0, 'Def Break Bonus': 0, 'Penetration': 0, 'Extra Dmg': 0, 'Def Reduction': 0, 'Monster Def': self.ui.defense.value(), 'Multiplier': 0, 'Skill Dmg Boost': 0, 'Cooldown': 61.8, 'Class Dmg': 28.8, 'Skill Haste': 0, 'Special': 0}
        for equip in equipment_list:
            if equip in data['Single'].keys():
                add_equipment(base_status, data['Single'][equip])
        base_status['Effect Ratio'] = float(equipment_list[104])
        # print(equipment_list[107])
        base_status['Base Atk'] += int(equipment_list[105])
        base_status['Crit Dmg'] += float(equipment_list[106])
        base_status['Crit Rate'] += float(equipment_list[107])
        base_status['Elem Boost'] += float(equipment_list[108])
        base_status['Cooldown'] += float(equipment_list[109])
        base_status['Agility'] += int(equipment_list[110])
        base_status['Strength'] += int(equipment_list[111])
        base_status['Skill Dmg'] += int(equipment_list[112])
        base_status['Atk Bonus'] += float(equipment_list[119])
        base_status['Car Collection'] = int(equipment_list[120])
        # print (base_status)
        outfits = outfit_count(base_status, outfit_dict=data['Sets'])
        special_boost = 1
        for outfit in outfits:
            if outfit[0] + outfit[1] == 'Extraordinary4' and float(equipment_list[113]) > 0:
                special_boost *= 1 + float(equipment_list[113]) / 100
            else:
                if outfit[0] + outfit[1] == 'Extraordinary6' and float(equipment_list[114]) > 0:
                    special_boost *= 1 + float(equipment_list[114]) / 100
                else:
                    if outfit[0] + outfit[1] == 'Excellence4' and float(equipment_list[115]) > 0:
                        special_boost *= 1 + float(equipment_list[115]) / 100
                    else:
                        if outfit[0] + outfit[1] == 'Excellence7' and float(equipment_list[116]) > 0:
                            special_boost *= 1 + float(equipment_list[116]) / 100
                        else:
                            if outfit[0] + outfit[1] == 'Excellence9' and float(equipment_list[117]) > 0:
                                special_boost *= 1 + float(equipment_list[117]) / 100
                            else:
                                if outfit[0] + outfit[1] == 'Transcendence9' and float(equipment_list[118]) > 0:
                                    special_boost *= 1 + float(equipment_list[118]) / 100
                                else:
                                    add_equipment(base_status, data['Sets'][outfit[0]][outfit[1]])
        if 'Avarice Shoes' in equipment_list:
            base_status['Crit Dmg'] += 3 * base_status['Avarice']
        else:
            if 'Demon Heart Shoes' in equipment_list:
                base_status['Crit Dmg'] += 4 * base_status['Avarice']
        if ('Venom', '2') in outfits:
            extra_kezhi = min(4 * base_status['Venom'], 16)
            base_status['Counter'] += extra_kezhi
        else:
            if ('Cursed', '2') in outfits:
                extra_kezhi = min(4 * base_status['Venom'] + base_status['Cursed'], 22)
                base_status['Counter'] += extra_kezhi
        
        # Calculate CDR % from Rating (Formula derived from user data: 200->15%, 328.4->22.5% => K approx 1133)
        cdr_percentage = (base_status['Cooldown'] / (base_status['Cooldown'] + 1133)) * 100
        
        # Construct final_status with ALL keys required by damage_compute
        final_status = {
            'Elem Boost': base_status['Elem Boost'], 
            'Crit Rate': base_status['Crit Rate'] - 7e-07 * base_status['Agility'] + 0.0125 * base_status['Agility'] + 0.3034, 
            'Crit Dmg': base_status['Crit Dmg'], 
            'Counter': base_status['Counter'], 
            'Dmg Amp': base_status['Dmg Amp'], 
            'Skill Dmg': base_status['Skill Dmg'], 
            'Resonance Dmg': base_status['Resonance Dmg'], 
            'Elem Dmg': base_status['Elem Dmg'] + base_status['Elem Boost'] / 2.2, 
            'Def Break Atk': base_status['Def Break Atk'] * (1 + base_status['Def Break Bonus'] / 100), 
            'Atk': (base_status['Base Atk'] + base_status['Strength'] * 2.5) * (1 + base_status['Atk Bonus'] / 100), 
            'Monster Def': base_status['Monster Def'], 
            'Penetration': base_status['Penetration'], 
            'Def Reduction': base_status['Def Reduction'], 
            'Extra Dmg': base_status['Extra Dmg'],
            'Special': base_status['Special'],
            'Class Dmg': base_status['Class Dmg'],
            'Multiplier': base_status['Multiplier'],
            'Skill Dmg Boost': base_status['Skill Dmg Boost'],
            'Skill Haste': base_status['Skill Haste'],
            'Cooldown Reduction': cdr_percentage,
            'Effect Ratio': base_status['Effect Ratio'],
            'Def Shred': base_status['Def Reduction'] # Map for UI display consistency if needed
        }
        
        burst_damage, total_damage = damage_compute(final_status)
        return (final_status, burst_damage * special_boost, total_damage * special_boost)
if __name__ == '__main__':
    print(sys.argv)
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())