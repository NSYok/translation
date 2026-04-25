import './styles.css';
import { runCalculation, DEFAULT_BASE_STATUS } from './calculator.js';
import { initState, getState, setState, subscribe, saveSnapshot, getSnapshot, clearSnapshot, exportBuild, importBuild, getAllState } from './state.js';
import { SLOTS, EMBLEMS, ENHANCEMENT_SLOTS, ENHANCEMENTS, ENGRAVING_SLOTS, ENGRAVINGS, PETS, CARDS, FASHION, FASHION_EMBLEMS, BUFFS, MANUAL_DEFAULTS, generateDefaults } from './options.js';
import { fetchGameData } from './firebase.js';

let gameData = null;

async function loadGameData() {
  let data = await fetchGameData();
  if (!data) {
    try {
      const resp = await fetch('/data.json');
      data = await resp.json();
    } catch (e) {
      console.error("Local fallback failed:", e);
    }
  }
  gameData = data;
  
  if (gameData && gameData.Single) {
    const injectOptions = (objMap) => {
      for (const obj of Object.values(objMap)) {
        if (!obj.options) continue;
        const typeLabel = obj.label;
        const matchingItems = Object.keys(gameData.Single).filter(itemName => {
          const item = gameData.Single[itemName];
          return (item.type === typeLabel || item.Type === typeLabel);
        });
        for (const itemName of matchingItems) {
          if (!obj.options.includes(itemName)) {
            const noneIdx = obj.options.indexOf('None');
            if (noneIdx !== -1) obj.options.splice(noneIdx, 0, itemName);
            else obj.options.push(itemName);
          }
        }
      }
    };
    injectOptions(FASHION);
    injectOptions(FASHION_EMBLEMS);
    injectOptions(BUFFS);
    injectOptions(EMBLEMS);
    
    const injectSingle = (obj, label) => {
      if (!obj.options) return;
      const matchingItems = Object.keys(gameData.Single).filter(itemName => {
        const item = gameData.Single[itemName];
        return (item.type === label || item.Type === label);
      });
      for (const itemName of matchingItems) {
        if (!obj.options.includes(itemName)) {
          const noneIdx = obj.options.indexOf('None');
          if (noneIdx !== -1) obj.options.splice(noneIdx, 0, itemName);
          else obj.options.push(itemName);
        }
      }
    };
    injectSingle(PETS, 'Pet');
    injectSingle(CARDS, 'Card');

    // CRITICAL: Rebuild tabs after data is injected so dropdowns see the new items
    buildAllTabs();
  }
}

// --- Icon path helper ---
function iconPath(name) {
  if (!name || name === 'None') return '/icons/None.png';
  return `/icons/${name}.png`;
}

// --- Modal System ---
const modalOverlay = () => document.getElementById('icon-modal');
const modalGrid = () => document.getElementById('modal-grid');
const modalTitle = () => document.getElementById('modal-title');

let _modalResolve = null;

function openModal(title, options, current) {
  modalTitle().textContent = title;
  const grid = modalGrid();
  grid.innerHTML = '';
  
  for (const opt of options) {
    const item = document.createElement('div');
    item.className = `icon-grid-item${opt === current ? ' active' : ''}`;
    item.innerHTML = `<img src="${iconPath(opt)}" alt="${opt}" loading="lazy" onerror="this.style.display='none'"><span>${opt}</span>`;
    item.addEventListener('click', () => {
      modalOverlay().classList.add('hidden');
      if (_modalResolve) _modalResolve(opt);
    });
    grid.appendChild(item);
  }
  
  modalOverlay().classList.remove('hidden');
  return new Promise(resolve => { _modalResolve = resolve; });
}

// Close modal on overlay click
document.addEventListener('click', (e) => {
  if (e.target === modalOverlay()) {
    modalOverlay().classList.add('hidden');
    if (_modalResolve) _modalResolve(null);
  }
});

// --- Component: Icon Selector Button ---
function createIconSelect(stateKey, label, options, container) {
  const el = document.createElement('div');
  el.className = 'icon-select';
  el.id = `sel-${stateKey}`;
  
  const render = () => {
    const val = getState(stateKey);
    el.innerHTML = `<img src="${iconPath(val)}" alt="${val}" onerror="this.style.display='none'"><div class="icon-name" title="${val}">${val === 'None' ? label : val}</div>`;
  };
  render();
  
  el.addEventListener('click', async () => {
    const picked = await openModal(label, options, getState(stateKey));
    if (picked !== null) {
      setState(stateKey, picked);
      render();
      recalculate();
    }
  });
  
  container.appendChild(el);
  return { render };
}

// --- Component: Dropdown Select ---
function createSelect(stateKey, label, options, container) {
  const wrapper = document.createElement('div');
  wrapper.className = 'select-wrapper';
  
  const sel = document.createElement('select');
  sel.title = label;
  for (const opt of options) {
    const o = document.createElement('option');
    o.value = opt;
    o.textContent = opt;
    if (opt === getState(stateKey)) o.selected = true;
    sel.appendChild(o);
  }
  sel.addEventListener('change', () => {
    setState(stateKey, sel.value);
    recalculate();
  });
  
  wrapper.appendChild(sel);
  container.appendChild(wrapper);
}

// --- Component: Number Input ---
function createNumInput(stateKey, label, container, step = 1) {
  const group = document.createElement('div');
  group.className = 'num-input-group';
  group.innerHTML = `<label>${label}</label>`;
  
  const input = document.createElement('input');
  input.type = 'number';
  input.step = step;
  input.value = getState(stateKey) ?? 0;
  input.addEventListener('input', () => {
    setState(stateKey, parseFloat(input.value) || 0);
    recalculate();
  });
  
  group.appendChild(input);
  container.appendChild(group);
}

// ====== BUILD TABS ======

function buildGearTab() {
  const tab = document.getElementById('tab-gear');
  tab.innerHTML = '';
  
  const gearSlots = ['weapon', 'head', 'armor', 'hand', 'legs', 'shoes', 'neck', 'bracer', 'ring', 'seal', 'amulet', 'treasure'];
  
  for (const slotKey of gearSlots) {
    const slot = SLOTS[slotKey];
    const section = document.createElement('div');
    section.className = 'slot-section';
    section.innerHTML = `<div class="slot-label">${slot.label}</div>`;
    
    // Equipment + Emblem row
    const row = document.createElement('div');
    row.className = 'slot-row';
    
    const options = slot.options || slot.sets.filter(s => s !== 'None').map(s => `${s} ${slot.suffix}`).concat('None');
    createIconSelect(`s_${slotKey}`, slot.label, options, row);
    
    if (EMBLEMS[slotKey]) {
      createIconSelect(`emb_${slotKey}`, EMBLEMS[slotKey].label, EMBLEMS[slotKey].options, row);
    }
    section.appendChild(row);
    
    // Engravings row
    if (ENGRAVING_SLOTS[slotKey]) {
      const engRow = document.createElement('div');
      engRow.className = 'slot-row-3';
      const engType = ENGRAVING_SLOTS[slotKey].type;
      for (let i = 0; i < 3; i++) {
        createIconSelect(`eng_${slotKey}_${i}`, `Engrave ${i+1}`, ENGRAVINGS[engType], engRow);
      }
      section.appendChild(engRow);
    }
    
    tab.appendChild(section);
  }
}

function buildEnhanceTab() {
  const tab = document.getElementById('tab-enhance');
  tab.innerHTML = '';
  
  const title = document.createElement('div');
  title.className = 'section-title';
  title.textContent = 'Enhancement Levels';
  tab.appendChild(title);
  
  const grid = document.createElement('div');
  grid.className = 'slot-row-3';
  
  const order = ['head', 'armor', 'hand', 'legs', 'shoes', 'weapon', 'neck', 'bracer', 'ring', 'seal', 'amulet'];
  for (const slotKey of order) {
    const cfg = ENHANCEMENT_SLOTS[slotKey];
    const opts = ENHANCEMENTS[cfg.type].options;
    const wrapper = document.createElement('div');
    wrapper.innerHTML = `<div class="slot-label">${SLOTS[slotKey]?.label || slotKey}</div>`;
    createSelect(`enh_${slotKey}`, `${slotKey} Enhancement`, opts, wrapper);
    grid.appendChild(wrapper);
  }
  
  tab.appendChild(grid);
}

function buildPetTab() {
  const tab = document.getElementById('tab-pet');
  tab.innerHTML = '';
  
  // Pet 1
  const pet1Title = document.createElement('div');
  pet1Title.className = 'section-title';
  pet1Title.textContent = 'Primary Pet';
  tab.appendChild(pet1Title);
  const p1Row = document.createElement('div');
  p1Row.className = 'slot-row';
  createIconSelect('pet_main', 'Primary Pet', PETS.options, p1Row);
  const starWrap1 = document.createElement('div');
  starWrap1.innerHTML = '<div class="slot-label">Star</div>';
  createSelect('pet_star_1', 'Stars', PETS.stars, starWrap1);
  p1Row.appendChild(starWrap1);
  tab.appendChild(p1Row);
  
  const s1Row = document.createElement('div');
  s1Row.className = 'slot-row-3';
  createIconSelect('pet_soul_1_str', PETS.souls.str.label, PETS.souls.str.options, s1Row);
  createIconSelect('pet_soul_1_skill', PETS.souls.skill.label, PETS.souls.skill.options, s1Row);
  createIconSelect('pet_soul_1_spd', PETS.souls.spd.label, PETS.souls.spd.options, s1Row);
  tab.appendChild(s1Row);
  
  // Pet 2
  const sep = document.createElement('div');
  sep.className = 'section-title mt-6';
  sep.textContent = 'Secondary Pet';
  tab.appendChild(sep);
  
  const p2Row = document.createElement('div');
  p2Row.className = 'slot-row';
  createIconSelect('pet_2', 'Secondary Pet', PETS.options, p2Row);
  const starWrap2 = document.createElement('div');
  starWrap2.innerHTML = '<div class="slot-label">Star</div>';
  createSelect('pet_star_2', 'Stars', PETS.stars, starWrap2);
  p2Row.appendChild(starWrap2);
  tab.appendChild(p2Row);
  
  const s2Row = document.createElement('div');
  s2Row.className = 'slot-row-3';
  createIconSelect('pet_soul_2_str', PETS.souls.str.label, PETS.souls.str.options, s2Row);
  createIconSelect('pet_soul_2_skill', PETS.souls.skill.label, PETS.souls.skill.options, s2Row);
  createIconSelect('pet_soul_2_spd', PETS.souls.spd.label, PETS.souls.spd.options, s2Row);
  tab.appendChild(s2Row);
  
  // Cards
  const cardTitle = document.createElement('div');
  cardTitle.className = 'section-title mt-6';
  cardTitle.textContent = 'Cards';
  tab.appendChild(cardTitle);
  
  const cRow = document.createElement('div');
  cRow.className = 'slot-row';
  for (let i = 1; i <= 4; i++) {
    createIconSelect(`card_${i}`, `Card ${i}`, CARDS.options, cRow);
  }
  tab.appendChild(cRow);
}

function buildFashionTab() {
  const tab = document.getElementById('tab-fashion');
  tab.innerHTML = '<div class="section-title">Fashion</div>';
  
  const fRow = document.createElement('div');
  fRow.className = 'slot-row-3';
  for (const [key, f] of Object.entries(FASHION)) {
    createIconSelect(`fashion_${key}`, f.label, f.options, fRow);
  }
  tab.appendChild(fRow);
  
  const feTitle = document.createElement('div');
  feTitle.className = 'section-title mt-6';
  feTitle.textContent = 'Fashion Emblems';
  tab.appendChild(feTitle);
  
  const feRow = document.createElement('div');
  feRow.className = 'slot-row-3';
  for (const [key, f] of Object.entries(FASHION_EMBLEMS)) {
    createIconSelect(`fashion_emb_${key}`, f.label, f.options, feRow);
  }
  tab.appendChild(feRow);
  
  const bTitle = document.createElement('div');
  bTitle.className = 'section-title mt-6';
  bTitle.textContent = 'Buffs';
  tab.appendChild(bTitle);
  
  const bRow = document.createElement('div');
  bRow.className = 'slot-row-3';
  for (const [key, b] of Object.entries(BUFFS)) {
    createIconSelect(`buff_${key}`, b.label, b.options, bRow);
  }
  tab.appendChild(bRow);
}

function buildManualTab() {
  const tab = document.getElementById('tab-manual');
  tab.innerHTML = '<div class="section-title">Combat Settings</div>';
  
  const g1 = document.createElement('div');
  g1.className = 'slot-row';
  createNumInput('monsterDef', 'Monster Def', g1, 100);
  createNumInput('dotRatio', 'Effect Ratio', g1, 0.1);
  tab.appendChild(g1);
  
  const t2 = document.createElement('div');
  t2.className = 'section-title mt-4';
  t2.textContent = 'Circuit Adjustments';
  tab.appendChild(t2);

  const g2 = document.createElement('div');
  g2.className = 'slot-row-3';
  const circuitFields = [
    ['manAtk', 'Base Atk (+)'], ['manCritDmg', 'Crit Dmg (+)'], ['manCritRate', 'Crit Rate (+)'],
    ['manElem', 'Elem Boost (+)'], ['manCd', 'Cooldown (+)'], ['manAgi', 'Agility (+)'],
    ['manStr', 'Strength (+)'], ['manSkillDmg', 'Skill Dmg (+)'], ['manAtkBonus', 'Atk Bonus (+)'],
  ];
  for (const [key, label] of circuitFields) {
    createNumInput(key, label, g2, key.includes('Rate') || key.includes('Dmg') || key.includes('Elem') || key.includes('Cd') || key.includes('Bonus') ? 0.1 : 1);
  }
  tab.appendChild(g2);
  
  const t3 = document.createElement('div');
  t3.className = 'section-title mt-4';
  t3.textContent = 'Other';
  tab.appendChild(t3);

  const g3 = document.createElement('div');
  g3.className = 'slot-row';
  createNumInput('manCar', 'Car Collection Level', g3);
  tab.appendChild(g3);
  
  const t4 = document.createElement('div');
  t4.className = 'section-title mt-4';
  t4.textContent = 'Custom Tech Boosts (%)';
  tab.appendChild(t4);

  const g4 = document.createElement('div');
  g4.className = 'slot-row';
  const boostFields = [
    ['boostBufan4', 'Extraordinary 4'], ['boostBufan6', 'Extraordinary 6'],
    ['boostZhuoyue4', 'Excellence 4'], ['boostZhuoyue7', 'Excellence 7'],
    ['boostZhuoyue9', 'Excellence 9'], ['boostChaoran9', 'Transcendence 9'],
  ];
  for (const [key, label] of boostFields) {
    createNumInput(key, label, g4, 0.1);
  }
  tab.appendChild(g4);
}

// ====== COLLECT EQUIPMENT LIST ======

function collectEquipmentList() {
  const list = [];
  const s = getAllState();
  
  // Equipment slots
  for (const slotKey of Object.keys(SLOTS)) {
    list.push(s[`s_${slotKey}`]);
  }
  // Emblems
  for (const slotKey of Object.keys(EMBLEMS)) {
    list.push(s[`emb_${slotKey}`]);
  }
  // Enhancements
  for (const slotKey of Object.keys(ENHANCEMENT_SLOTS)) {
    list.push(s[`enh_${slotKey}`]);
  }
  // Engravings
  for (const slotKey of Object.keys(ENGRAVING_SLOTS)) {
    for (let i = 0; i < 3; i++) {
      list.push(s[`eng_${slotKey}_${i}`]);
    }
  }
  // Pet souls
  for (const suffix of ['1_str', '1_skill', '1_spd', '2_str', '2_skill', '2_spd']) {
    list.push(s[`pet_soul_${suffix}`]);
  }
  // Cards
  for (let i = 1; i <= 4; i++) list.push(s[`card_${i}`]);
  // Fashion
  for (const key of Object.keys(FASHION)) list.push(s[`fashion_${key}`]);
  for (const key of Object.keys(FASHION_EMBLEMS)) list.push(s[`fashion_emb_${key}`]);
  // Buffs
  for (const key of Object.keys(BUFFS)) list.push(s[`buff_${key}`]);
  
  // Pets (star + name combo)
  if (s.pet_main && s.pet_main !== 'None') list.push(`${s.pet_star_1}${s.pet_main}`);
  if (s.pet_2 && s.pet_2 !== 'None') list.push(`${s.pet_star_2}${s.pet_2}`);
  
  return list;
}

function collectManualInputs() {
  const s = getAllState();
  return {
    monsterDef: s.monsterDef ?? MANUAL_DEFAULTS.monsterDef,
    dotRatio: s.dotRatio ?? MANUAL_DEFAULTS.dotRatio,
    manAtk: s.manAtk ?? MANUAL_DEFAULTS.manAtk,
    manCritDmg: s.manCritDmg ?? MANUAL_DEFAULTS.manCritDmg,
    manCritRate: s.manCritRate ?? MANUAL_DEFAULTS.manCritRate,
    manElem: s.manElem ?? MANUAL_DEFAULTS.manElem,
    manCd: s.manCd ?? MANUAL_DEFAULTS.manCd,
    manAgi: s.manAgi ?? MANUAL_DEFAULTS.manAgi,
    manStr: s.manStr ?? MANUAL_DEFAULTS.manStr,
    manSkillDmg: s.manSkillDmg ?? MANUAL_DEFAULTS.manSkillDmg,
    manAtkBonus: s.manAtkBonus ?? MANUAL_DEFAULTS.manAtkBonus,
    manCar: s.manCar ?? MANUAL_DEFAULTS.manCar,
    boostBufan4: s.boostBufan4 ?? -1,
    boostBufan6: s.boostBufan6 ?? -1,
    boostZhuoyue4: s.boostZhuoyue4 ?? -1,
    boostZhuoyue7: s.boostZhuoyue7 ?? -1,
    boostZhuoyue9: s.boostZhuoyue9 ?? -1,
    boostChaoran9: s.boostChaoran9 ?? -1,
    baseStats: { ...DEFAULT_BASE_STATUS },
  };
}

// ====== RESULTS RENDERING ======

const STATS_DISPLAY = [
  ['Attack (ATK)', 'Atk'], ['Crit Rate', 'Crit Rate'], ['Crit DMG', 'Crit Dmg'], ['Elem', 'Elem Boost'],
  ['ENH DMG', 'Elem Dmg'], ['Dmg Bonus', 'Dmg Amp'], ['Skill DMG', 'Skill Dmg'], ['Dmg Debuff', 'dmgToDebuff'], ['DMG to Boss', 'Boss Dmg'],
  ['Def Shred', 'Def Break Atk'], ['PEN', 'Penetration'], ['ASPD', 'Skill Haste'], ['Cooldown', 'Cooldown'],
  ['Additional', 'Extra Dmg'], ['Resonance DMG', 'Resonance Dmg'],
  ['Class DMG Bonus', 'Class Dmg'], ['Skill DMG Boost', 'Skill Dmg Boost'], ['Special', 'Special'], ['Skill Ratio', 'Multiplier'],
];

function formatNum(n) {
  if (Math.abs(n) >= 1000) return Math.round(n).toLocaleString();
  return n.toFixed(1);
}

function renderResults(finalStatus, burst, sustained) {
  document.getElementById('val-burst').textContent = Math.round(burst).toLocaleString();
  document.getElementById('val-sustained').textContent = Math.round(sustained).toLocaleString();
  document.getElementById('val-cdr').textContent = `${finalStatus['Cooldown Reduction'].toFixed(1)}%`;
  
  const snapshot = getSnapshot();
  const deltaEl = document.getElementById('snapshot-delta');
  if (snapshot) {
    const diff = ((sustained - snapshot.sustained) / snapshot.sustained * 100);
    deltaEl.style.display = 'block';
    deltaEl.innerHTML = `<span class="stat-delta ${diff > 0 ? 'positive' : diff < 0 ? 'negative' : 'neutral'}">${diff >= 0 ? '+' : ''}${diff.toFixed(2)}% vs Snapshot</span>`;
  } else {
    deltaEl.style.display = 'none';
  }
  
  const list = document.getElementById('stat-list');
  list.innerHTML = '';
  for (const [label, key] of STATS_DISPLAY) {
    const val = finalStatus[key] || 0;
    const row = document.createElement('div');
    row.className = 'stat-row';
    
    let deltaHTML = '';
    if (snapshot) {
      const snapVal = snapshot.finalStatus[key] || 0;
      const d = val - snapVal;
      if (Math.abs(d) > 0.05) {
        const cls = d > 0 ? 'positive' : 'negative';
        deltaHTML = `<span class="stat-delta ${cls}">${d > 0 ? '+' : ''}${formatNum(d)}</span>`;
      }
    }
    
    row.innerHTML = `<span class="stat-name">${label}</span><span><span class="stat-value">${formatNum(val)}</span>${deltaHTML}</span>`;
    list.appendChild(row);
  }
}

// ====== RECALCULATE ======

function recalculate() {
  if (!gameData) return;
  try {
    const equipment = collectEquipmentList();
    const manual = collectManualInputs();
    const { finalStatus, burst, sustained } = runCalculation(equipment, manual, gameData);
    renderResults(finalStatus, burst, sustained);
  } catch (e) {
    console.error('Calculation error:', e);
  }
}

// ====== TAB NAVIGATION ======

document.getElementById('tab-nav').addEventListener('click', (e) => {
  const btn = e.target.closest('.tab-btn');
  if (!btn) return;
  const tabId = btn.dataset.tab;
  
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById(`tab-${tabId}`).classList.add('active');
});

// ====== SNAPSHOT ======

document.getElementById('btn-snapshot').addEventListener('click', () => {
  if (!gameData) return;
  const equipment = collectEquipmentList();
  const manual = collectManualInputs();
  const { finalStatus, burst, sustained } = runCalculation(equipment, manual, gameData);
  saveSnapshot({ finalStatus, burst, sustained });
  recalculate();
});

document.getElementById('btn-clear-snap').addEventListener('click', () => {
  clearSnapshot();
  recalculate();
});

// ====== BUILD SAVE/LOAD ======

document.getElementById('btn-export').addEventListener('click', () => {
  const json = exportBuild();
  const blob = new Blob([json], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `coa_build_${Date.now()}.json`;
  a.click();
  URL.revokeObjectURL(a.href);
});

document.getElementById('btn-import').addEventListener('click', () => {
  document.getElementById('file-import').click();
});

document.getElementById('file-import').addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    if (importBuild(reader.result)) {
      // Rebuild all tabs to reflect new state
      buildAllTabs();
      recalculate();
    }
  };
  reader.readAsText(file);
  e.target.value = '';
});

// ====== INIT ======

function buildAllTabs() {
  buildGearTab();
  buildEnhanceTab();
  buildPetTab();
  buildFashionTab();
  buildManualTab();
}

async function init() {
  initState(generateDefaults());
  await loadGameData();
  buildAllTabs();
  recalculate();
}

init();
