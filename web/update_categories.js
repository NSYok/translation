import { SLOTS, EMBLEMS, PETS, CARDS, FASHION, FASHION_EMBLEMS, BUFFS, ARMOR_SETS, ACC_SETS } from './src/options.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const dataPath = path.join(__dirname, 'public/data.json');
let fileContent = fs.readFileSync(dataPath, 'utf8');
if (fileContent.charCodeAt(0) === 0xFEFF) {
  fileContent = fileContent.slice(1);
}
const data = JSON.parse(fileContent);

function getCategory(name) {
    if (SLOTS.weapon.options && SLOTS.weapon.options.includes(name)) return 'Weapon';
    if (SLOTS.treasure.options && SLOTS.treasure.options.includes(name)) return 'Treasure';
    if (PETS.options.includes(name)) return 'Pet';
    if (CARDS.options.includes(name)) return 'Card';
    
    for (const v of Object.values(EMBLEMS)) if (v.options.includes(name)) return 'Emblem';
    for (const v of Object.values(FASHION)) if (v.options.includes(name)) return 'Fashion';
    for (const v of Object.values(FASHION_EMBLEMS)) if (v.options.includes(name)) return 'Fashion Emblem';
    for (const v of Object.values(BUFFS)) if (v.options.includes(name)) return 'Buff';
    for (const v of Object.values(PETS.souls)) if (v.options.includes(name)) return 'Pet Soul';

    for (const set of ARMOR_SETS) {
      if (name === `${set} Head` || name === `${set} Armor` || name === `${set} Hand` || name === `${set} Legs` || name === `${set} Shoes`) return 'Armor';
    }
    for (const set of ACC_SETS) {
      if (name === `${set} Necklace` || name === `${set} Bracer` || name === `${set} Ring` || name === `${set} Seal` || name === `${set} Amulet`) return 'Accessory';
    }

    return 'Other';
}

let count = 0;
for (const name in data.Single) {
  const item = data.Single[name];
  if (name === 'None' || name === '') continue;
  const cat = getCategory(name);
  if (!item.type) {
    // Add type property as the first property if possible, or just add it
    // To make it look nice, we can recreate the object
    const newItem = { type: cat, ...item };
    data.Single[name] = newItem;
    count++;
  }
}

fs.writeFileSync(dataPath, JSON.stringify(data, null, 2));
console.log('Updated ' + count + ' items with category types.');
