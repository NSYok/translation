/**
 * UI Options Configuration
 * Separated from code so adding new equipment only requires editing this + data.json
 * 
 * @module options
 */

export const ARMOR_SETS = ['Black Feather', 'Glimmer', 'Avarice', 'Venom', 'Butterfly', 'Demon Heart', 'Cursed', 'None'];
export const ACC_SETS = ['Solar', 'Holy Glory', 'Demon Shadow', 'None'];

export const SLOTS = {
  weapon: {
    label: 'Weapon',
    options: ['True Fate Sickle (Withered)', 'Abyssal Gaze', 'Desperate Dream Song', 'None'],
    default: 'True Fate Sickle (Withered)',
  },
  head: { label: 'Head', sets: ARMOR_SETS, suffix: 'Head', default: 'Black Feather Head' },
  armor: { label: 'Armor', sets: ARMOR_SETS, suffix: 'Armor', default: 'Black Feather Armor' },
  hand: { label: 'Hand', sets: ARMOR_SETS, suffix: 'Hand', default: 'Black Feather Hand' },
  legs: { label: 'Legs', sets: ARMOR_SETS, suffix: 'Legs', default: 'Black Feather Legs' },
  shoes: { label: 'Shoes', sets: ARMOR_SETS, suffix: 'Shoes', default: 'Black Feather Shoes' },
  neck: { label: 'Necklace', sets: ACC_SETS, suffix: 'Necklace', default: 'Holy Glory Necklace' },
  bracer: { label: 'Bracer', sets: ACC_SETS, suffix: 'Bracer', default: 'Holy Glory Bracer' },
  ring: { label: 'Ring', sets: ACC_SETS, suffix: 'Ring', default: 'Holy Glory Ring' },
  seal: { label: 'Seal', sets: ACC_SETS, suffix: 'Seal', default: 'Holy Glory Seal' },
  talisman: { label: 'Talisman', sets: ACC_SETS, suffix: 'Talisman', default: 'Holy Glory Talisman' },
  treasure: {
    label: 'Treasure',
    options: ["Hourglass of World's End", 'Hymn of Ancient Demon God', 'None'],
    default: "Hourglass of World's End",
  },
};

export const EMBLEMS = {
  weapon: { label: 'Weapon Emblem', options: ["Barbena", "Krag", "Void Sovereign", "Magitech Heavy Mech", "Hawke", "Kraken", "Mystic", "Steel Chimera", "Judgement Paladin", "Witch", "Mechanical Core", "Evolution's End", "None"], default: 'None' },
  head: { label: 'Head Emblem', options: ["Plague the Filth", "Kernnos", "Claudius", "Isaac", "Andre", "Polones", "Shimmerscale Poison Wing", "Rangovi", "Thunderous Trasher", "Hexchess Guard", "None"], default: 'None' },
  armor: { label: 'Armor Emblem', options: ["Ophelia", "Claudius", "Beelzebub", "Tower Shield Mech", "Adam", "Crystallian Beast", "Void Bladematron", "Golem Shield", "Darkflame Expeller", "Odyssa", "Charlotte", "Leotid", "None"], default: 'None' },
  hand: { label: 'Hand Emblem', options: ["Ophelia", "Boget", "Vik Brotherhood", "Isaac", "Chaos Breaker", "Meredia", "Ancient Guardian - Charm", "Ancient Guardian - Fist", "Skull", "Polones", "Deus", "Hexchess Guard", "Leotid", "None"], default: 'None' },
  legs: { label: 'Legs Emblem', options: ["Martin", "Sawblade Mech", "Bitter Behemoth", "Mars", "Adam", "Ulysses", "Golem Shield", "Darkflame Expeller", "Goramos", "Odyssa", "None"], default: 'None' },
  shoes: { label: 'Shoes Emblem', options: ["Joker", "Greedy Touch", "Isaac", "Meredia", "Ancient Guardian - Charm", "Maiden of Punishment", "Void Bladematron", "Electric Whip Guard", "Famine the Hungry", "Goliath", "Thunderous Trasher", "None"], default: 'None' },
  neck: { label: 'Necklace Emblem', options: ["Joker", "Clockwork Warden", "Void Ring Keeper", "Gorga", "Thunderbolt Striker", "Twin Prisoner", "Leviathan", "Electric Whip Guard", "Michael", "None"], default: 'None' },
  bracer: { label: 'Bracer Emblem', options: ["Clockwork Warden", "Gorga", "Vik Brotherhood", "Chaos Breaker", "Thunderbolt Striker", "Leviathan", "Ancient Guardian - Fist", "Eros", "Michael", "None"], default: 'None' },
  ring: { label: 'Ring Emblem', options: ["Kernnos", "Void Ring Keeper", "Ember of Soul", "Gorga", "Mars", "Andre", "Goliath", "None"], default: 'None' },
  seal: { label: 'Seal Emblem', options: ["Plague the Filth", "Sawblade Mech", "Azrael the Annihilation", "Fading Thoughts", "Goramos", "None"], default: 'None' },
  talisman: { label: 'Talisman Emblem', options: ["Annihilation of Thoughts", "Tower Shield Mech", "Azrael the Annihilation", "Crystallian Beast", "Famine the Hungry", "None"], default: 'None' },
};


export const ENHANCEMENTS = {
  strength: { label: 'Strength/Intelligence', options: Array.from({ length: 11 }, (_, i) => `+${i + 15}(Strength_Intelligence)`).concat('None') },
  hp: { label: 'HP', options: Array.from({ length: 11 }, (_, i) => `+${i + 15}(HP)`).concat('None') },
  weapon: { label: 'Weapon', options: Array.from({ length: 8 }, (_, i) => `+${i + 18}(Weapon)`).concat('None') },
  lr: { label: 'L/R Slot', options: Array.from({ length: 11 }, (_, i) => `+${i + 15}(L_R Slot)`).concat('None') },
};

export const ENHANCEMENT_SLOTS = {
  head: { type: 'strength', default: '+18(Strength_Intelligence)' },
  armor: { type: 'hp', default: '+16(HP)' },
  hand: { type: 'strength', default: '+16(Strength_Intelligence)' },
  legs: { type: 'hp', default: '+15(HP)' },
  shoes: { type: 'strength', default: '+17(Strength_Intelligence)' },
  weapon: { type: 'weapon', default: '+21(Weapon)' },
  neck: { type: 'strength', default: '+18(Strength_Intelligence)' },
  bracer: { type: 'strength', default: '+17(Strength_Intelligence)' },
  ring: { type: 'strength', default: '+17(Strength_Intelligence)' },
  seal: { type: 'lr', default: '+18(L_R Slot)' },
  talisman: { type: 'lr', default: '+18(L_R Slot)' },
};

const engraveLevels = (names) => {
  const result = [];
  for (const name of names) {
    result.push(`${name} 3`, `${name} 2`, `${name} 1`);
  }
  result.push('None');
  return result;
};

export const ENGRAVINGS = {
  HGS: engraveLevels(['Transcendence', 'Adaptation', 'Destruction', 'Swiftness', 'Combo', 'Offensive', 'Suppress', 'Unyielding', 'Sprint']),
  BP: engraveLevels(['Extraordinary', 'Quenching', 'Advanced Tech', 'Status Break', 'Basic', 'Pierce', 'Siege', 'Charge', 'Wall Break']),
  WSA: engraveLevels(['Excellence', 'Smite', 'Alliance', 'Unbreakable', 'Adversity', 'Fullness', 'Air Supremacy']),
  RBN: engraveLevels(['Elem Master', 'Challenger', 'Resonance', 'Evasion', 'Elem Resist', 'Recovery', 'Solitary', 'Lightning Summon']),
};

export const ENGRAVING_SLOTS = {
  weapon: { type: 'WSA', defaults: ['Excellence 3', 'Unbreakable 3', 'Smite 3'] },
  head: { type: 'HGS', defaults: ['Destruction 3', 'Adaptation 3', 'Combo 1'] },
  armor: { type: 'BP', defaults: ['Extraordinary 3', 'Quenching 3', 'Basic 1'] },
  hand: { type: 'HGS', defaults: ['Destruction 3', 'Adaptation 3', 'Combo 1'] },
  legs: { type: 'BP', defaults: ['Extraordinary 3', 'Basic 3', 'Quenching 1'] },
  shoes: { type: 'HGS', defaults: ['Destruction 3', 'Adaptation 3', 'Combo 1'] },
  neck: { type: 'RBN', defaults: ['Elem Master 1', 'Elem Resist 3', 'Challenger 3'] },
  bracer: { type: 'RBN', defaults: ['Elem Master 1', 'Elem Resist 3', 'Challenger 3'] },
  ring: { type: 'RBN', defaults: ['Elem Master 2', 'Elem Resist 2', 'Challenger 3'] },
  seal: { type: 'WSA', defaults: ['Excellence 3', 'Unbreakable 3', 'Smite 1'] },
  talisman: { type: 'WSA', defaults: ['Excellence 3', 'Unbreakable 2', 'Smite 2'] },
};

export const PETS = {
  options: ['Cat', 'Eagle', 'Panda', 'Dragon', 'PiaoPiao', 'Koto', 'Fox', 'None'],
  stars: ['1 Star', '2 Star', '3 Star'],
  souls: {
    strength: { label: 'Strength Soul', options: ['Cat Paw', 'Emperor Thorn', 'Insight Eye', 'None'] },
    skill: { label: 'Skill Soul', options: ['Magic Witch', 'Beast Tooth Mark', 'None'] },
    spd: { label: 'Spd Soul', options: ['Wind Butterfly', 'Maple Curse', 'None'] },
  },
};

export const CARDS = {
  options: ['Loyal Partner', 'The evil hook', 'Void Shadow', 'Chrome Arms', 'Ancient Guardian', 'Deep Space Swarm', 'Realm Creature', 'Magic Era', 'Dark Realm Madman', 'Light Chaser', 'Clockwork Legion', 'Mech Empire', 'Beast Legion', 'Gloomy Forbidden Area', 'Park Guard', 'None'],
};

export const FASHION = {
  title: { label: 'Title', options: ['Demon Touch', 'Void Crown', 'Gold Crown', 'None'], default: 'Demon Touch' },
  weapon: { label: 'Fashion Weapon', options: ['Sun Decree Seat', 'S-Rank Fashion Weapon', 'None'], default: 'Sun Decree Seat' },
  aura: { label: 'Aura', options: ['Shining Star', 'Golden Slumber', 'Eclipse Realm', 'Eclipse Realm II', 'None'], default: 'Golden Slumber' },
  head: { label: 'Fashion Head', options: ['New Sky Head', 'Old Sky Head', 'None'], default: 'New Sky Head' },
  cloth: { label: 'Fashion Cloth', options: ['New Sky Armor', 'Old Sky Armor', 'None'], default: 'New Sky Armor' },
  acc: { label: 'Fashion Acc', options: ['New Sky Accessory', 'Old Sky Accessory', 'None'], default: 'New Sky Accessory' },
  face: { label: 'Fashion Face', options: ['New Sky Facewear', 'Old Sky Facewear', 'None'], default: 'New Sky Facewear' },
  badge: { label: 'Fashion Badge', options: ['New Sky Badge', 'Old Sky Badge', 'None'], default: 'New Sky Badge' },
  foot: { label: 'Footprint', options: ['Shining Star Footmark', 'None'], default: 'Shining Star Footmark' },
};

export const FASHION_EMBLEMS = {
  title: { label: 'Title Emblem', options: ['Heat Wave Title Emblem', 'Mingjin Title Emblem', 'Demon Sickle Emblem', 'None'], default: 'Heat Wave Title Emblem' },
  weapon: { label: 'Weapon Emblem', options: ['Mingjin Weapon Emblem', 'Demon Sickle Emblem', 'None'], default: 'Mingjin Weapon Emblem' },
  aura: { label: 'Aura Emblem', options: ['Star God Aura Emblem', 'Mingjin Aura Emblem', 'Demon Sickle Emblem', 'None'], default: 'Mingjin Aura Emblem' },
  head: { label: 'Head Emblem', options: ['Mingjin Head Emblem', 'Demon Sickle Emblem', 'None'], default: 'Mingjin Head Emblem' },
  cloth: { label: 'Cloth Emblem', options: ['Mingjin Armor Emblem', 'Demon Sickle Emblem', 'None'], default: 'Demon Sickle Emblem' },
  acc: { label: 'Acc Emblem', options: ['Mingjin Accessory Emblem', 'Demon Sickle Emblem', 'None'], default: 'Mingjin Accessory Emblem' },
  face: { label: 'Face Emblem', options: ['Demon Sickle Emblem', 'None'], default: 'Demon Sickle Emblem' },
  badge: { label: 'Badge Emblem', options: ['Demon Sickle Emblem', 'None'], default: 'Demon Sickle Emblem' },
  foot: { label: 'Foot Emblem', options: ['Mingjin Footmark Emblem', 'Demon Sickle Emblem', 'None'], default: 'Mingjin Footmark Emblem' },
};

export const BUFFS = {
  elem: { label: 'Elem Potion', options: ['22 Elem Potion', '25 Elem Potion', 'None'], default: '25 Elem Potion' },
  atk: { label: 'Atk Buff', options: ['8 Crit', '6 dmgToDebuff', '8 Skill Dmg', '8 Atk', '10 Crit Dmg', 'None'], default: '10 Crit Dmg' },
  wine: { label: 'Wine', options: ['Morning', 'Cliff', 'East', 'None'], default: 'Morning' },
  dragon: { label: 'Dragon Breath', options: ['Dragon Breath', 'None'], default: 'Dragon Breath' },
  wind: { label: 'Gale', options: ['Gale', 'None'], default: 'Gale' },
  mine: { label: 'Mine War', options: ['Mine War', 'None'], default: 'Mine War' },
  counter: { label: 'Debuff Buff', options: ['Dmg Debuff (%)', 'None'], default: 'Dmg Debuff (%)' },
};

export const MANUAL_DEFAULTS = {
  monsterDef: 5000,
  dotRatio: 5.0,
  manAtk: 191,
  manCritDmg: 34.7,
  manCritRate: 5.5,
  manElem: 20.8,
  manCd: 0.0,
  manAgility: 0,
  manStrength: 134,
  manSkillDmg: 8,
  manAtkBonus: 0.0,
  manCar: 34,
  boostBufan4: -1.0,
  boostBufan6: -1.0,
  boostZhuoyue4: -1.0,
  boostZhuoyue7: -1.0,
  boostZhuoyue9: -1.0,
  boostChaoran9: -1.0,
  dataSource: 'firebase',
};

/**
 * Generate all default state values
 * @returns {Object}
 */
export function generateDefaults() {
  const defaults = {};

  // Equipment slots
  for (const [slotKey, slot] of Object.entries(SLOTS)) {
    defaults[`s_${slotKey}`] = slot.default;
  }

  // Emblems
  for (const [slotKey, emb] of Object.entries(EMBLEMS)) {
    defaults[`emb_${slotKey}`] = emb.default;
  }

  // Enhancements
  for (const [slotKey, enh] of Object.entries(ENHANCEMENT_SLOTS)) {
    defaults[`enh_${slotKey}`] = enh.default;
  }

  // Engravings
  for (const [slotKey, eng] of Object.entries(ENGRAVING_SLOTS)) {
    for (let i = 0; i < 3; i++) {
      defaults[`eng_${slotKey}_${i}`] = eng.defaults[i];
    }
  }

  // Pets
  defaults.pet_main = 'Dragon';
  defaults.pet_star_1 = '3 Star';
  defaults.pet_soul_1_strength = 'None';
  defaults.pet_soul_1_skill = 'None';
  defaults.pet_soul_1_spd = 'None';
  defaults.pet_2 = 'Cat';
  defaults.pet_star_2 = '3 Star';
  defaults.pet_soul_2_strength = 'None';
  defaults.pet_soul_2_skill = 'None';
  defaults.pet_soul_2_spd = 'None';

  // Cards
  defaults.card_1 = 'Void Shadow';
  defaults.card_2 = 'Chrome Arms';
  defaults.card_3 = 'Ancient Guardian';
  defaults.card_4 = 'None';

  // Fashion
  for (const [key, f] of Object.entries(FASHION)) {
    defaults[`fashion_${key}`] = f.default;
  }
  for (const [key, f] of Object.entries(FASHION_EMBLEMS)) {
    defaults[`fashion_emb_${key}`] = f.default;
  }

  // Buffs
  for (const [key, b] of Object.entries(BUFFS)) {
    defaults[`buff_${key}`] = b.default;
  }

  // Manual inputs
  Object.assign(defaults, MANUAL_DEFAULTS);

  return defaults;
}
