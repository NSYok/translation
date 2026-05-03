import './styles.css';
import { runCalculation } from './calculator.js';
import {
  initState,
  getState,
  setState,
  subscribe,
  saveSnapshot,
  getSnapshot,
  clearSnapshot,
  exportBuild,
  importBuild,
  getAllState,
} from './state.js';
import {
  SLOTS,
  EMBLEMS,
  ENHANCEMENT_SLOTS,
  ENHANCEMENTS,
  ENGRAVING_SLOTS,
  ENGRAVINGS,
  PETS,
  CARDS,
  FASHION,
  FASHION_EMBLEMS,
  BUFFS,
  MANUAL_DEFAULTS,
  generateDefaults,
  ARMOR_SETS,
  ACC_SETS,
} from './options.js';
import { fetchGameData } from './firebase.js';

initState(generateDefaults());

let gameData = null;
let latestResult = null;
let modalSearchHandler = null;
let modalEscapeHandler = null;
let modalResolver = null;

function getItemType(itemName) {
  if (!itemName || itemName === 'None') return 'Empty';
  return gameData?.Single?.[itemName]?.type || gameData?.Single?.[itemName]?.Type || 'Custom';
}

function matchesConfiguredType(itemName, item, config) {
  const type = item.type || item.Type || '';
  const acceptedTypes = config.matchTypes || [config.label];

  // ── Fashion items ──────────────────────────────────────────────────────────
  // 1. The destination slot must explicitly list 'Fashion' in its matchTypes.
  //    Gear slots (Head, Armor, Badge…) never do, so Fashion items can't bleed in.
  // 2. Among Fashion slots that DO accept Fashion, further restrict to items
  //    pre-defined in that slot's options list (prevents "Fashion Weapon" showing
  //    in the "Fashion Aura" slot, since they all share type = "Fashion").
  if (type === 'Fashion') {
    if (!acceptedTypes.includes('Fashion')) return false;
    const predefined = config._originalOptions ?? config.options ?? [];
    return predefined.includes(itemName);
  }

  // ── Emblem items ───────────────────────────────────────────────────────────
  // Same two-gate rule: slot must accept 'Emblem', then check predefined list
  // to distinguish "Mingjin Weapon Emblem" from "Mingjin Armor Emblem".
  if (type === 'Emblem') {
    if (!acceptedTypes.includes('Emblem')) return false;
    const predefined = config._originalOptions ?? config.options ?? [];
    return predefined.includes(itemName);
  }

  // ── All other types (Weapon, Armor, Head, Badge, Buff, Pet…) ──────────────
  return acceptedTypes.includes(type);
}


async function loadGameData(source = getState('dataSource') || 'local') {
  let data = null;

  if (source === 'firebase') {
    data = await fetchGameData();
    if (!data) {
      console.warn('Firebase failed, falling back to local data.json');
    }
  }

  if (!data) {
    const response = await fetch('/data.json');
    data = await response.json();
  }

  gameData = data;

  if (!gameData?.Single) return;

  const allKnownSets = Object.keys(gameData.Sets || {});
  for (const setName of allKnownSets) {
    const headItem = gameData.Single[`${setName} Head`];
    const neckItem = gameData.Single[`${setName} Necklace`];

    const isArmor = headItem && (headItem.type === 'Head' || headItem.Type === 'Head');
    const isAcc = neckItem && (neckItem.type === 'Necklace' || neckItem.Type === 'Necklace');

    if (isArmor && !ARMOR_SETS.includes(setName)) {
      ARMOR_SETS.splice(ARMOR_SETS.length - 1, 0, setName);
    }
    if (isAcc && !ACC_SETS.includes(setName)) {
      ACC_SETS.splice(ACC_SETS.length - 1, 0, setName);
    }
  }

  const injectOptions = (objMap) => {
    for (const obj of Object.values(objMap)) {
      if (!obj.options && !obj.sets) continue;

      if (obj.sets) {
        obj._originalOptions = obj.sets
          .filter((setName) => setName !== 'None')
          .map((setName) => `${setName} ${obj.suffix}`)
          .concat('None');
      } else if (obj.options && !obj._originalOptions) {
        obj._originalOptions = [...obj.options];
      }

      if (obj._originalOptions) {
        obj.options = [...obj._originalOptions];
      }

      const matchingItems = Object.keys(gameData.Single).filter((itemName) => {
        const item = gameData.Single[itemName];
        return matchesConfiguredType(itemName, item, obj);
      });

      for (const itemName of matchingItems) {
        if (obj.options.includes(itemName)) continue;

        const noneIndex = obj.options.indexOf('None');
        if (noneIndex !== -1) {
          obj.options.splice(noneIndex, 0, itemName);
        } else {
          obj.options.push(itemName);
        }
      }
    }
  };

  injectOptions(SLOTS);
  injectOptions(FASHION);
  injectOptions(FASHION_EMBLEMS);
  injectOptions(BUFFS);
  injectOptions(EMBLEMS);

  if (!PETS._originalOptions) PETS._originalOptions = [...PETS.options];
  PETS.options = [...PETS._originalOptions];
  for (const name of Object.keys(gameData.Single).filter((key) => (gameData.Single[key].type || gameData.Single[key].Type) === 'Pet')) {
    if (!PETS.options.includes(name)) {
      PETS.options.splice(PETS.options.indexOf('None'), 0, name);
    }
  }

  if (!CARDS._originalOptions) CARDS._originalOptions = [...CARDS.options];
  CARDS.options = [...CARDS._originalOptions];
  for (const name of Object.keys(gameData.Single).filter((key) => (gameData.Single[key].type || gameData.Single[key].Type) === 'Card')) {
    if (!CARDS.options.includes(name)) {
      CARDS.options.splice(CARDS.options.indexOf('None'), 0, name);
    }
  }
}

function iconPath(name) {
  if (!name || name === 'None') return '/icons/None.png';
  return `/icons/${name}.png`;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function modalOverlay() {
  return document.getElementById('icon-modal');
}

function modalGrid() {
  return document.getElementById('modal-grid');
}

function modalTitle() {
  return document.getElementById('modal-title');
}

function modalSearch() {
  return document.getElementById('modal-search');
}

function renderModalOptions(options, current, onPick, searchTerm = '') {
  const grid = modalGrid();
  const normalizedSearch = searchTerm.trim().toLowerCase();
  const filtered = normalizedSearch
    ? options.filter((option) => option.toLowerCase().includes(normalizedSearch))
    : options;

  grid.innerHTML = '';

  for (const option of filtered) {
    const itemType = getItemType(option);
    const item = document.createElement('button');
    item.type = 'button';
    item.className = `icon-grid-item${option === current ? ' active' : ''}`;
    item.innerHTML = `
      <img src="${iconPath(option)}" alt="${escapeHtml(option)}" loading="lazy" onerror="this.style.display='none'">
      <span>${escapeHtml(option)}</span>
      <small class="item-type">${escapeHtml(itemType)}</small>
    `;
    item.addEventListener('click', () => onPick(option));
    grid.appendChild(item);
  }

  if (filtered.length === 0) {
    grid.innerHTML = '<div class="modal-empty">No matching items</div>';
  }
}

function closeModal() {
  modalOverlay().classList.add('hidden');

  if (modalSearchHandler) {
    modalSearch().removeEventListener('input', modalSearchHandler);
    modalSearchHandler = null;
  }

  if (modalEscapeHandler) {
    document.removeEventListener('keydown', modalEscapeHandler);
    modalEscapeHandler = null;
  }
}

function openModal(title, options, current) {
  modalTitle().textContent = title;
  modalSearch().value = '';

  return new Promise((resolve) => {
    modalResolver = resolve;
    const pick = (value) => {
      closeModal();
      modalResolver = null;
      resolve(value);
    };

    renderModalOptions(options, current, pick);

    modalSearchHandler = (event) => {
      renderModalOptions(options, current, pick, event.target.value);
    };
    modalSearch().addEventListener('input', modalSearchHandler);

    modalEscapeHandler = (event) => {
      if (event.key === 'Escape') {
        pick(null);
      }
    };
    document.addEventListener('keydown', modalEscapeHandler);

    modalOverlay().classList.remove('hidden');
    modalSearch().focus();
  });
}

document.addEventListener('click', (event) => {
  if (event.target === modalOverlay()) {
    closeModal();
    if (modalResolver) {
      modalResolver(null);
      modalResolver = null;
    }
  }
});

function createIconSelect(stateKey, label, options, container, helperText = '') {
  const wrapper = document.createElement('div');
  wrapper.className = 'field-card';

  const labelRow = document.createElement('div');
  labelRow.className = 'field-header';
  labelRow.innerHTML = `
    <div class="field-label">${escapeHtml(label)}</div>
    ${helperText ? `<div class="field-helper">${escapeHtml(helperText)}</div>` : ''}
  `;

  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'icon-select';
  button.id = `sel-${stateKey}`;

  const render = () => {
    const value = getState(stateKey);
    const displayName = value && value !== 'None' ? value : `Select ${label}`;
    const itemType = value && value !== 'None' ? getItemType(value) : 'Empty';
    button.classList.toggle('selected', Boolean(value && value !== 'None'));
    button.innerHTML = `
      <img src="${iconPath(value)}" alt="${escapeHtml(displayName)}" loading="lazy" onerror="this.style.display='none'">
      <div class="icon-copy">
        <div class="icon-name">${escapeHtml(displayName)}</div>
        <div class="icon-meta">${value && value !== 'None' ? `${escapeHtml(label)} · ${escapeHtml(itemType)}` : 'No item selected'}</div>
      </div>
    `;
  };

  render();

  button.addEventListener('click', async () => {
    const picked = await openModal(label, options, getState(stateKey));
    if (picked !== null) {
      setState(stateKey, picked);
    }
  });

  wrapper.appendChild(labelRow);
  wrapper.appendChild(button);
  container.appendChild(wrapper);
  subscribe(stateKey, render);
}

function createNumericInput(stateKey, label, container) {
  const field = document.createElement('div');
  field.className = 'num-input-group';
  field.innerHTML = `
    <label for="${stateKey}">${escapeHtml(label)}</label>
    <input id="${stateKey}" type="number" step="0.1" value="${getState(stateKey)}">
  `;

  const input = field.querySelector('input');
  input.addEventListener('input', (event) => {
    const parsed = Number.parseFloat(event.target.value);
    setState(stateKey, Number.isFinite(parsed) ? parsed : 0);
  });

  container.appendChild(field);
  subscribe(stateKey, (value) => {
    input.value = value;
  });
}

function createSection(title, description = '', layoutClass = 'selection-grid') {
  const section = document.createElement('section');
  section.className = 'panel-section';
  section.innerHTML = `
    <div class="section-heading">
      <h2>${escapeHtml(title)}</h2>
      ${description ? `<p>${escapeHtml(description)}</p>` : ''}
    </div>
    <div class="${layoutClass}"></div>
  `;
  return section;
}

function createManualFieldLabel(key) {
  return key
    .replace(/^man/, '')
    .replace(/^boost/, 'Boost ')
    .replace(/([A-Z])/g, ' $1')
    .replace(/^./, (match) => match.toUpperCase())
    .trim();
}

function collectEquipment(state) {
  const equipment = [];

  for (const key of Object.keys(SLOTS)) {
    const value = state[key];
    if (value && value !== 'None') equipment.push(value);
  }

  for (const key of Object.keys(EMBLEMS)) {
    const value = state[`emblem_${key}`];
    if (value && value !== 'None') equipment.push(value);
  }

  for (const key of Object.keys(ENHANCEMENT_SLOTS)) {
    const value = state[`enhance_${key}`];
    if (value && value !== 'None') equipment.push(value);
  }

  for (let petIndex = 1; petIndex <= 2; petIndex += 1) {
    const petValue = state[`pet_${petIndex}`];
    if (petValue && petValue !== 'None') {
      equipment.push(`${state[`pet_${petIndex}_star`] || 'State 1'} ${petValue}`);
    }

    for (const key of Object.keys(PETS.souls)) {
      const value = state[`pet_${petIndex}_soul_${key}`];
      if (value && value !== 'None') equipment.push(value);
    }
  }

  for (let index = 1; index <= 4; index += 1) {
    const value = state[`card_${index}`];
    if (value && value !== 'None') equipment.push(value);
  }

  for (const key of Object.keys(ENGRAVING_SLOTS)) {
    for (let index = 0; index < 3; index += 1) {
      const value = state[`engrave_${key}_${index}`];
      if (value && value !== 'None') equipment.push(value);
    }
  }

  for (const key of Object.keys(FASHION)) {
    const value = state[`fashion_${key}`];
    if (value && value !== 'None') equipment.push(value);
  }

  for (const key of Object.keys(FASHION_EMBLEMS)) {
    const value = state[`fash_emb_${key}`];
    if (value && value !== 'None') equipment.push(value);
  }

  for (const key of Object.keys(BUFFS)) {
    const value = state[`buff_${key}`];
    if (value && value !== 'None') equipment.push(value);
  }

  return equipment;
}

function collectManualInputs(state) {
  const manual = {
    baseStats: {},
  };

  for (const key of Object.keys(MANUAL_DEFAULTS)) {
    manual[key] = state[`manual_${key}`];
    manual.baseStats[key] = state[`manual_${key}`];
  }

  return manual;
}

function countSelections(state) {
  return collectEquipment(state).length;
}

function renderSnapshotDelta(result) {
  const snapshot = getSnapshot();
  const deltaNode = document.getElementById('snapshot-delta');
  const clearButton = document.getElementById('btn-clear-snap');

  if (!snapshot || !result) {
    deltaNode.style.display = 'none';
    deltaNode.innerHTML = '';
    clearButton.disabled = !snapshot;
    return;
  }

  const burstDelta = result.burst - snapshot.burst;
  const sustainedDelta = result.sustained - snapshot.sustained;
  const burstClass = burstDelta > 0 ? 'positive' : burstDelta < 0 ? 'negative' : 'neutral';
  const sustainedClass = sustainedDelta > 0 ? 'positive' : sustainedDelta < 0 ? 'negative' : 'neutral';
  const sign = (value) => (value > 0 ? '+' : '');
  const roundedBurstDelta = Math.round(burstDelta);
  const roundedSustainedDelta = Math.round(sustainedDelta);

  const burstPct = snapshot.burst ? (burstDelta / snapshot.burst * 100).toFixed(1) + '%' : '0%';
  const sustainedPct = snapshot.sustained ? (sustainedDelta / snapshot.sustained * 100).toFixed(1) + '%' : '0%';

  deltaNode.style.display = 'grid';
  deltaNode.innerHTML = `
    <div class="delta-card">
      <span class="delta-label">Compared with snapshot</span>
      <span class="delta-chip ${burstClass}">Burst ${sign(roundedBurstDelta)}${roundedBurstDelta.toLocaleString()} (${sign(burstDelta)}${burstPct})</span>
      <span class="delta-chip ${sustainedClass}">Sustain ${sign(roundedSustainedDelta)}${roundedSustainedDelta.toLocaleString()} (${sign(sustainedDelta)}${sustainedPct})</span>
    </div>
  `;
  clearButton.disabled = false;
}

function renderSummary(result) {
  document.getElementById('val-burst').textContent = Math.round(result.burst).toLocaleString();
  document.getElementById('val-sustained').textContent = Math.round(result.sustained).toLocaleString();
  document.getElementById('val-cdr').textContent = `${(result.finalStatus['Cooldown Reduction (%)'] || 0).toFixed(1)}%`;
  document.getElementById('selected-count').textContent = countSelections(getAllState()).toLocaleString();
  renderSnapshotDelta(result);
}

function renderActiveSets(result) {
  const container = document.getElementById('active-sets');
  if (!container) return;

  if (!result.outfits || result.outfits.length === 0) {
    container.innerHTML = `
      <div class="stat-row" style="margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid var(--border-light);">
        <span class="stat-name" style="color: var(--text-dim);">Active Sets</span>
        <span class="stat-value">None</span>
      </div>
    `;
    return;
  }

  // Sort outfits: by set name, then tier number
  const sortedOutfits = [...result.outfits].sort((a, b) => {
    if (a[0] !== b[0]) return a[0].localeCompare(b[0]);
    return parseInt(a[1]) - parseInt(b[1]);
  });

  const setStrings = sortedOutfits.map(o => `${o[0]} ${o[1]}`);

  container.innerHTML = `
    <div class="stat-row" style="margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid var(--border-light);">
      <span class="stat-name" style="color: var(--accent-primary);">Active Sets</span>
      <span class="stat-value" style="font-size: 0.85rem; text-align: right; max-width: 60%; line-height: 1.4;">
        ${escapeHtml(setStrings.join(', '))}
      </span>
    </div>
  `;
}

function renderStats(result) {
  const list = document.getElementById('stat-list');
  list.innerHTML = '';

  for (const statName of Object.keys(result.finalStatus).sort()) {
    const row = document.createElement('div');
    row.className = 'stat-row';
    row.innerHTML = `
      <span class="stat-name">${escapeHtml(statName)}</span>
      <span class="stat-value">${result.finalStatus[statName].toFixed(1)}</span>
    `;
    list.appendChild(row);
  }
}

function updateResults() {
  if (!gameData) return;

  const state = getAllState();
  latestResult = runCalculation(collectEquipment(state), collectManualInputs(state), gameData);
  renderSummary(latestResult);
  renderActiveSets(latestResult);
  renderStats(latestResult);
}

function downloadBuild() {
  const json = exportBuild();
  const blob = new Blob([json], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  const stamp = new Date().toISOString().slice(0, 10);
  link.href = url;
  link.download = `coa-build-${stamp}.json`;
  link.click();
  URL.revokeObjectURL(url);
}

async function init() {
  await loadGameData();

  const tabGear = document.getElementById('tab-gear');
  const tabEnhance = document.getElementById('tab-enhance');
  const tabPet = document.getElementById('tab-pet');
  const tabFashion = document.getElementById('tab-fashion');
  const tabManual = document.getElementById('tab-manual');

  const gearSection = createSection('Equipment', 'Pick your core loadout. Large lists are searchable when you open a slot.');
  const gearGrid = gearSection.querySelector('.selection-grid');
  for (const [key, slot] of Object.entries(SLOTS)) {
    createIconSelect(key, slot.label, slot.options, gearGrid);
  }
  tabGear.appendChild(gearSection);

  const emblemSection = createSection('Emblems', 'Add slot-specific emblems that scale your build.');
  const emblemGrid = emblemSection.querySelector('.selection-grid');
  for (const [key, slot] of Object.entries(EMBLEMS)) {
    createIconSelect(`emblem_${key}`, slot.label, slot.options, emblemGrid);
  }
  tabGear.appendChild(emblemSection);

  const enhancementSection = createSection('Enhancements', 'Refine each slot with enhancement tiers.');
  const enhancementGrid = enhancementSection.querySelector('.selection-grid');
  for (const [key, slot] of Object.entries(ENHANCEMENT_SLOTS)) {
    createIconSelect(`enhance_${key}`, `${SLOTS[key].label} Enhance`, ENHANCEMENTS[slot.type].options, enhancementGrid);
  }
  tabEnhance.appendChild(enhancementSection);

  const petSection = createSection('Pet Setup', 'The build now supports two pets, each with its own star tier and soul loadout.', 'pet-layout');
  const petGrid = petSection.querySelector('.pet-layout');
  for (let petIndex = 1; petIndex <= 2; petIndex += 1) {
    const petCard = document.createElement('div');
    petCard.className = 'pet-card';
    petCard.innerHTML = `<div class="subsection-title">Pet ${petIndex}</div><div class="selection-grid compact-grid"></div>`;
    const petCardGrid = petCard.querySelector('.selection-grid');
    createIconSelect(`pet_${petIndex}`, `Pet ${petIndex}`, PETS.options, petCardGrid);
    createIconSelect(`pet_${petIndex}_star`, `Pet ${petIndex} Star`, PETS.stars, petCardGrid);
    for (const [key, soul] of Object.entries(PETS.souls)) {
      createIconSelect(`pet_${petIndex}_soul_${key}`, `Pet ${petIndex} ${soul.label}`, soul.options, petCardGrid);
    }
    petGrid.appendChild(petCard);
  }
  tabPet.appendChild(petSection);

  const cardSection = createSection('Cards', 'Four card slots for additional offensive effects.');
  const cardGrid = cardSection.querySelector('.selection-grid');
  for (let index = 1; index <= 4; index += 1) {
    createIconSelect(`card_${index}`, `Card ${index}`, CARDS.options, cardGrid);
  }
  tabPet.appendChild(cardSection);

  const engravingSection = createSection('Engravings', 'Each equipment piece carries three engraving slots.', 'selection-grid engrave-grid');
  const engravingGrid = engravingSection.querySelector('.selection-grid.engrave-grid');
  for (const [key, slot] of Object.entries(ENGRAVING_SLOTS)) {
    const group = document.createElement('div');
    group.className = 'engrave-slot';
    group.innerHTML = `<div class="engrave-title">${escapeHtml(SLOTS[key].label)}</div><div class="engrave-stack"></div>`;
    const stack = group.querySelector('.engrave-stack');
    for (let index = 0; index < 3; index += 1) {
      createIconSelect(`engrave_${key}_${index}`, `${SLOTS[key].label} Engraving ${index + 1}`, ENGRAVINGS[slot.type], stack, `Slot ${index + 1}`);
    }
    engravingGrid.appendChild(group);
  }
  tabEnhance.appendChild(engravingSection);

  const fashionSection = createSection('Fashion', 'Cosmetic slots that still affect combat stats.');
  const fashionGrid = fashionSection.querySelector('.selection-grid');
  for (const [key, slot] of Object.entries(FASHION)) {
    createIconSelect(`fashion_${key}`, slot.label, slot.options, fashionGrid);
  }
  tabFashion.appendChild(fashionSection);

  const fashionEmblemSection = createSection('Fashion Emblems', 'Slot emblems for cosmetics, kept separate for easier scanning.');
  const fashionEmblemGrid = fashionEmblemSection.querySelector('.selection-grid');
  for (const [key, slot] of Object.entries(FASHION_EMBLEMS)) {
    createIconSelect(`fash_emb_${key}`, slot.label, slot.options, fashionEmblemGrid);
  }
  tabFashion.appendChild(fashionEmblemSection);

  const buffsSection = createSection('Manual Inputs & Buffs', 'Tune assumptions like monster defense, panel attack, temporary buffs, and set boosts.', 'manual-layout');
  const buffsPanel = buffsSection.querySelector('.manual-layout');
  const buffsBox = document.createElement('div');
  buffsBox.className = 'manual-card';
  buffsBox.innerHTML = '<div class="subsection-title">Buff Presets</div><div class="selection-grid compact-grid"></div>';
  const buffsGrid = buffsBox.querySelector('.selection-grid');
  for (const [key, slot] of Object.entries(BUFFS)) {
    createIconSelect(`buff_${key}`, slot.label, slot.options, buffsGrid);
  }
  buffsPanel.appendChild(buffsBox);

  const manualBox = document.createElement('div');
  manualBox.className = 'manual-card';
  manualBox.innerHTML = '<div class="subsection-title">Manual Values</div><div class="manual-grid"></div>';
  const manualGrid = manualBox.querySelector('.manual-grid');
  for (const key of Object.keys(MANUAL_DEFAULTS)) {
    createNumericInput(`manual_${key}`, createManualFieldLabel(key), manualGrid);
  }
  buffsPanel.appendChild(manualBox);
  tabManual.appendChild(buffsSection);

  subscribe('*', updateResults);
  updateResults();

  const tabButtons = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');
  tabButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const target = button.dataset.tab;
      tabButtons.forEach((item) => item.classList.remove('active'));
      tabContents.forEach((item) => item.classList.remove('active'));
      button.classList.add('active');
      document.getElementById(`tab-${target}`).classList.add('active');
    });
  });

  document.getElementById('btn-snapshot').addEventListener('click', () => {
    if (!latestResult) return;
    saveSnapshot(latestResult);
    renderSnapshotDelta(latestResult);
  });

  document.getElementById('btn-clear-snap').addEventListener('click', () => {
    clearSnapshot();
    renderSnapshotDelta(latestResult);
  });

  document.getElementById('btn-export').addEventListener('click', downloadBuild);
  document.getElementById('btn-import').addEventListener('click', () => {
    document.getElementById('file-import').click();
  });
  document.getElementById('file-import').addEventListener('change', (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (readerEvent) => {
      const success = importBuild(readerEvent.target?.result || '');
      if (success) {
        updateResults();
      } else {
        window.alert('Invalid build file.');
      }
      event.target.value = '';
    };
    reader.readAsText(file);
  });

  const dataSourceSelect = document.getElementById('data-source-select');
  dataSourceSelect.value = getState('dataSource') || 'firebase';
  dataSourceSelect.addEventListener('change', async (event) => {
    setState('dataSource', event.target.value);
    await loadGameData(event.target.value);
    updateResults();
  });
}

init().catch((error) => {
  console.error('App init failed:', error);
  document.getElementById('val-burst').textContent = 'Error';
});
