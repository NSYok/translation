/**
 * Crystal of Atlan — Damage Calculation Engine
 * Ported from Python utils_computer.py with formula corrections
 * 
 * @module calculator
 */

/**
 * Core damage computation formula
 * @param {Object} status - Final computed stats dictionary
 * @returns {{ burst: number, sustained: number }}
 */
export function damageCompute(status) {
  const critMultiplier = 1 + Math.min(status['Crit Rate'] / 100, 1) * (status['Crit Dmg'] / 100);
  const dmgToDebuffMultiplier = 1 + status['dmgToDebuff'] / 100;
  const dmgToBossMultiplier = 1 + status['Boss Dmg'] / 100;
  const dmgAmp = 1 + status['Dmg Amp'] / 100;

  const skillResonance = 1 + (status['Skill Dmg'] + status['Resonance Dmg']) / 100;
  const elemDmgMultiplier = 1 + status['Elem Dmg'] / 100;

  // Defense formula: Damage Reduction % = Defense / (3000 + Defense)
  const defAfterPen = Math.max(0,
    status['Monster Def'] * (1 - (status['Def Reduction'] || 0) / 100) - (status['Penetration'] || 0)
  );
  const dmgReductionPct = defAfterPen / (3000 + defAfterPen);

  // Actual Attack = Total PATK * (1 - Damage Reduction %) + PDEF Shred
  const attackZone = status['Atk'] * (1 - dmgReductionPct) + (status['Def Break Atk'] || 0);

  const extraDmg = 1 + status['Extra Dmg'] / 100;
  const special = 1 + status['Special'] / 100;
  const classDmg = 1 + status['Class Dmg'] / 100;
  const multiplier = 1 + status['Multiplier'] / 100;
  const skillDmgBoost = 1 + status['Skill Dmg Boost'] / 100;
  const skillHaste = 1 + status['Skill Haste'] / 100;
  const cdr = 1 / (1 - status['Cooldown Reduction'] / 100);
  const effectRatio = 1 + status['Effect Ratio'] / (100 - status['Effect Ratio']);

  const burst = critMultiplier * dmgToDebuffMultiplier * dmgToBossMultiplier * dmgAmp * skillResonance
    * elemDmgMultiplier * attackZone * extraDmg * special * classDmg
    * multiplier * skillDmgBoost * effectRatio;

  return { burst, sustained: burst * skillHaste * cdr };
}

/**
 * Add equipment stats to status dictionary (mutates status)
 * @param {Object} statusDict - Current stats
 * @param {Object} equipment - Equipment stats to add
 * @returns {Object} Modified status dict
 */
export function addEquipment(statusDict, equipment) {
  for (const key of Object.keys(equipment)) {
    if (key.toLowerCase() === 'type') continue;
    
    if (!(key in statusDict)) {
      statusDict[key] = equipment[key];
    } else {
      statusDict[key] = statusDict[key] + equipment[key];
    }
  }
  return statusDict;
}

/**
 * Count active set bonuses from accumulated set points
 * @param {Object} status - Status dict with set counters
 * @param {Object} outfitDict - Set definitions from data.json
 * @returns {Array<[string, string]>} Active set bonuses as [setName, tier] pairs
 */
export function outfitCount(status, outfitDict) {
  const outfits = [];

  for (const outfitName of Object.keys(outfitDict)) {
    if (outfitName in status) {
      for (const num of Object.keys(outfitDict[outfitName])) {
        if (status[outfitName] >= parseInt(num)) {
          outfits.push([outfitName, num]);
        }
      }
    }
  }

  // Set priority overrides (data-driven)
  const overrides = [
    // Black Feather removed when upgraded sets exist
    { if: ['Avarice', 'Black Feather'], remove: 'Black Feather' },
    { if: ['Glimmer', 'Black Feather'], remove: 'Black Feather' },
    { if: ['Venom', 'Black Feather'], remove: 'Black Feather' },
    // Upgraded set removes base set
    { if: ['Demon Heart', 'Avarice'], remove: 'Avarice' },
    { if: ['Butterfly', 'Glimmer'], remove: 'Glimmer' },
    { if: ['Cursed', 'Venom'], remove: 'Venom' },
    // New Sky supersedes Old Sky
    { if: ['New Sky', 'Old Sky'], remove: 'Old Sky' },
  ];

  const tiers = ['2', '3', '5'];
  for (const rule of overrides) {
    for (const tier of tiers) {
      const hasA = outfits.some(o => o[0] === rule.if[0] && o[1] === tier);
      const hasB = outfits.some(o => o[0] === rule.if[1] && o[1] === tier);
      if (hasA && hasB) {
        const idx = outfits.findIndex(o => o[0] === rule.remove && o[1] === tier);
        if (idx !== -1) outfits.splice(idx, 1);
      }
    }
  }

  return outfits;
}

/**
 * Default base status for a new character
 */
export const DEFAULT_BASE_STATUS = {
  'Elem Boost': 0, 'Crit Rate': 0, 'Crit Dmg': 56, 'dmgToDebuff': 0, 'Boss Dmg': 0, 'Dmg Amp': 3,
  'Skill Dmg': 0, 'Resonance Dmg': 20, 'Elem Dmg': 0, 'Base Atk': 201,
  'Atk Bonus': 0, 'Strength': 685, 'Agility': 445, 'Str Bonus': 0,
  'Def Break Atk': 0, 'Def Break Bonus': 0, 'Penetration': 0, 'Extra Dmg': 0,
  'Def Reduction': 0, 'Multiplier': 0,
  'Skill Dmg Boost': 0, 'Cooldown': 61.8, 'Class Dmg': 0,
  'Skill Haste': 0, 'Special': 0
};

/**
 * Run the full calculation pipeline
 * @param {string[]} equipmentList - Names of all selected equipment
 * @param {Object} manualInputs - Manual stat overrides from UI
 * @param {Object} gameData - Loaded data.json
 * @returns {{ finalStatus: Object, burst: number, sustained: number }}
 */
export function runCalculation(equipmentList, manualInputs, gameData) {
  // 1. Initialize base_status
  const baseStatus = { ...DEFAULT_BASE_STATUS };

  // Update with user-defined base stats
  if (manualInputs.baseStats) {
    Object.assign(baseStatus, manualInputs.baseStats);
  }

  baseStatus['Monster Def'] = manualInputs.monsterDef;

  // 2. Add stats from all selected equipment
  for (const equipName of equipmentList) {
    if (equipName && equipName !== 'None' && equipName in gameData.Single) {
      addEquipment(baseStatus, gameData.Single[equipName]);
    }
  }

  // 3. Apply manual stat adjustments
  baseStatus['Effect Ratio'] = manualInputs.dotRatio;
  baseStatus['Base Atk'] += manualInputs.manAtk;
  baseStatus['Crit Dmg'] += manualInputs.manCritDmg;
  baseStatus['Crit Rate'] += manualInputs.manCritRate;
  baseStatus['Elem Boost'] += manualInputs.manElem;
  baseStatus['Cooldown'] += manualInputs.manCd;
  baseStatus['Agility'] += manualInputs.manAgi;
  baseStatus['Strength'] += manualInputs.manStr;
  baseStatus['Skill Dmg'] += manualInputs.manSkillDmg;
  baseStatus['Atk Bonus'] += manualInputs.manAtkBonus;
  baseStatus['Car Collection'] = manualInputs.manCar;

  // 4. Handle set bonuses
  const outfits = outfitCount(baseStatus, gameData.Sets);
  let specialBoost = 1;

  // 5. Apply set bonuses and tech boosts
  for (const [setName, count] of outfits) {
    const key = setName + count;

    if (setName in gameData.Sets && count in gameData.Sets[setName]) {
      addEquipment(baseStatus, gameData.Sets[setName][count]);
    }

    if (key === 'Extraordinary4' && manualInputs.boostBufan4 > 0) {
      specialBoost *= 1 + manualInputs.boostBufan4 / 100;
    } else if (key === 'Extraordinary6' && manualInputs.boostBufan6 > 0) {
      specialBoost *= 1 + manualInputs.boostBufan6 / 100;
    } else if (key === 'Excellence4' && manualInputs.boostZhuoyue4 > 0) {
      specialBoost *= 1 + manualInputs.boostZhuoyue4 / 100;
    } else if (key === 'Excellence7' && manualInputs.boostZhuoyue7 > 0) {
      baseStatus['Dmg Amp'] += manualInputs.boostZhuoyue7;
    } else if (key === 'Excellence9' && manualInputs.boostZhuoyue9 > 0) {
      baseStatus['Extra Dmg'] += manualInputs.boostZhuoyue9;
    } else if (key === 'Transcendence9' && manualInputs.boostChaoran9 > 0) {
      specialBoost *= 1 + manualInputs.boostChaoran9 / 100;
    }
  }

  // 6. Apply special item/set interactions
  if (equipmentList.includes('Avarice Shoes')) {
    baseStatus['Crit Dmg'] += 3 * (baseStatus['Avarice'] || 0);
  } else if (equipmentList.includes('Demon Heart Shoes')) {
    baseStatus['Crit Dmg'] += 4 * (baseStatus['Avarice'] || 0);
  }

  if (outfits.some(o => o[0] === 'Venom' && o[1] === '2')) {
    const extraKezhi = Math.min(4 * (baseStatus['Venom'] || 0), 16);
    baseStatus['dmgToDebuff'] += extraKezhi;
  } else if (outfits.some(o => o[0] === 'Cursed' && o[1] === '2')) {
    const extraKezhi = Math.min(4 * (baseStatus['Venom'] || 0) + (baseStatus['Cursed'] || 0), 22);
    baseStatus['dmgToDebuff'] += extraKezhi;
  }

  // 7. Calculate derived stats
  const cdrPercentage = (baseStatus['Cooldown'] / (baseStatus['Cooldown'] + 1133)) * 100;

  const finalStatus = {
    'Elem Boost': baseStatus['Elem Boost'],
    'Crit Rate': baseStatus['Crit Rate'] - 7e-07 * baseStatus['Agility'] + 0.0125 * baseStatus['Agility'] + 0.3034,
    'Crit Dmg': baseStatus['Crit Dmg'],
    'dmgToDebuff': baseStatus['dmgToDebuff'],
    'Boss Dmg': baseStatus['Boss Dmg'],
    'Dmg Amp': baseStatus['Dmg Amp'],
    'Skill Dmg': baseStatus['Skill Dmg'],
    'Resonance Dmg': baseStatus['Resonance Dmg'],
    'Elem Dmg': (baseStatus['Elem Dmg'] || 0) + baseStatus['Elem Boost'] / 2.2,
    'Def Break Atk': baseStatus['Def Break Atk'] * (1 + (baseStatus['Def Break Bonus'] || 0) / 100),
    // Following Boarhat guide: Total PATK = PATK * (1 + STR Increase %) * (1 + PATK%)
    // Where every 10 Strength = 1% STR Increase -> STR Increase % = Strength / 1000
    'Atk': baseStatus['Base Atk'] * (1 + (baseStatus['Strength'] * (1 + (baseStatus['Str Bonus'] || 0) / 100)) / 1000) * (1 + (baseStatus['Atk Bonus'] || 0) / 100),
    'Monster Def': baseStatus['Monster Def'],
    'Penetration': baseStatus['Penetration'],
    'Def Reduction': baseStatus['Def Reduction'] || 0,
    'Extra Dmg': baseStatus['Extra Dmg'],
    'Special': baseStatus['Special'],
    'Class Dmg': baseStatus['Class Dmg'],
    'Multiplier': baseStatus['Multiplier'] || 0,
    'Skill Dmg Boost': baseStatus['Skill Dmg Boost'] || 0,
    'Skill Haste': baseStatus['Skill Haste'] || 0,
    'Cooldown Reduction': cdrPercentage,
    'Cooldown': baseStatus['Cooldown'],
    'Effect Ratio': baseStatus['Effect Ratio'] || 0,
    'Def Shred': baseStatus['Def Reduction'] || 0,
  };

  // 8. Final damage computation
  const { burst, sustained } = damageCompute(finalStatus);

  return {
    finalStatus,
    burst: burst * specialBoost,
    sustained: sustained * specialBoost,
  };
}
