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
  const critMultiplier = 1 + Math.min(status['Crit Rate (%)'] / 100, 1) * (status['Crit Dmg (%)'] / 100);
  const dmgToDebuffMultiplier = 1 + status['Dmg Debuff (%)'] / 100;
  const dmgToBossMultiplier = 1 + status['DMG to Boss (%)'] / 100;
  const dmgAmp = 1 + status['Dmg Bonus (%)'] / 100;

  const skillResonance = 1 + (status['Skill DMG (%)'] + status['Resonance DMG (%)']) / 100;
  const elemDmgMultiplier = 1 + status['Elem Dmg (%)'] / 100;

  // Defense formula: Damage Reduction % = Defense / (3000 + Defense)
  const defAfterPen = Math.max(0,
    status['Monster Def (flat)'] * (1 - (status['Def Reduction (%)'] || 0) / 100) - (status['PEN (flat)'] || 0)
  );
  const dmgReductionPct = defAfterPen / (3000 + defAfterPen);

  // Actual Attack = Total PATK * (1 - Damage Reduction %) + PDEF Shred
  const attackZone = status['Atk (flat)'] * (1 - dmgReductionPct) + (status['PDEF Shred (flat)'] || 0);

  const extraDmg = 1 + status['Additional (%)'] / 100;
  const special = 1 + status['Special (%)'] / 100;
  const classDmg = 1 + status['Class DMG Bonus (%)'] / 100;
  const multiplier = 1 + status['Skill Ratio (%)'] / 100;
  const skillDmgBoost = 1 + status['Skill DMG Boost (%)'] / 100;
  const skillHaste = 1 + status['ASPD (%)'] / 100;
  const cdr = 1 / (1 - (status['Cooldown Reduction (%)'] || 0) / 100);
  const effectRatio = 1 + status['Effect Ratio (%)'] / (100 - status['Effect Ratio (%)']);

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

  // Define the crossover pairs (Upgraded -> Base)
  const crossovers = [
    { up: 'Demon Heart', base: 'Avarice' },
    { up: 'Butterfly', base: 'Glimmer' },
    { up: 'Cursed', base: 'Venom' },
    { up: 'New Sky', base: 'Old Sky' },
  ];

  const baseToUp = {};
  crossovers.forEach(c => baseToUp[c.base] = c.up);

  for (const outfitName of Object.keys(outfitDict)) {
    let effectiveCount = status[outfitName] || 0;
    
    // Base sets inherit the piece count of their upgraded counterparts
    if (baseToUp[outfitName]) {
      effectiveCount += (status[baseToUp[outfitName]] || 0);
    }

    if (effectiveCount > 0) {
      for (const numStr of Object.keys(outfitDict[outfitName])) {
        const num = parseInt(numStr);
        if (effectiveCount >= num) {
          outfits.push([outfitName, numStr]);
        }
      }
    }
  }

  // Set priority overrides (data-driven)
  const overrides = [
    // Black Feather removed when upgraded sets exist
    { if: ['Avarice', 'Black Feather'], remove: 'Black Feather', tierByTier: false },
    { if: ['Glimmer', 'Black Feather'], remove: 'Black Feather', tierByTier: false },
    { if: ['Venom', 'Black Feather'], remove: 'Black Feather', tierByTier: false },
    // Upgraded set removes base set tier-by-tier
    { if: ['Demon Heart', 'Avarice'], remove: 'Avarice', tierByTier: true },
    { if: ['Butterfly', 'Glimmer'], remove: 'Glimmer', tierByTier: true },
    { if: ['Cursed', 'Venom'], remove: 'Venom', tierByTier: true },
    // New Sky supersedes Old Sky
    { if: ['New Sky', 'Old Sky'], remove: 'Old Sky', tierByTier: true },
  ];

  for (const rule of overrides) {
    if (rule.tierByTier) {
      const upTiers = outfits.filter(o => o[0] === rule.if[0]).map(o => o[1]);
      for (const t of upTiers) {
        for (let i = outfits.length - 1; i >= 0; i--) {
          if (outfits[i][0] === rule.remove && outfits[i][1] === t) {
            outfits.splice(i, 1);
          }
        }
      }
    } else {
      const hasA = outfits.some(o => o[0] === rule.if[0]);
      if (hasA) {
        // Remove all tiers of the suppressed set
        for (let i = outfits.length - 1; i >= 0; i--) {
          if (outfits[i][0] === rule.remove) {
            outfits.splice(i, 1);
          }
        }
      }
    }
  }

  return outfits;
}

/**
 * Default base status for a new character
 */
export const DEFAULT_BASE_STATUS = {
  'Elem Boost (%)': 0, 'Crit Rate (%)': 0, 'Crit Dmg (%)': 56, 'Dmg Debuff (%)': 0, 'DMG to Boss (%)': 0, 'Dmg Bonus (%)': 3,
  'Skill DMG (%)': 0, 'Resonance DMG (%)': 20, 'Elem Dmg (%)': 0, 'Atk (flat)': 201,
  'Atk Bonus (%)': 0, 'Strength (flat)': 685, 'Agility (flat)': 445, 'Intelligence (flat)': 0, 'Strength Bonus (%)': 0,
  'PDEF Shred (flat)': 0, 'Def Break Bonus (%)': 0, 'PEN (flat)': 0, 'Additional (%)': 0,
  'Def Reduction (%)': 0, 'Skill Ratio (%)': 0,
  'Skill DMG Boost (%)': 0, 'Cooldown (flat)': 61.8, 'Class DMG Bonus (%)': 0,
  'ASPD (%)': 0, 'Special (%)': 0,
  'Resonance Effect I': 0, 'Resonance Effect II': 0, 'Cooldown Reduction (%)': 0
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
  const config = gameData.Config || {};
  const defaultBase = config.DefaultBaseStatus || DEFAULT_BASE_STATUS;
  const baseStatus = { ...defaultBase };

  // Set global constants if provided
  if (config['Monster Def (flat)'] !== undefined) baseStatus['Monster Def (flat)'] = config['Monster Def (flat)'];
  if (config['Effect Ratio (%)'] !== undefined) baseStatus['Effect Ratio (%)'] = config['Effect Ratio (%)'];

  // Update with user-defined base stats
  if (manualInputs.baseStats) {
    Object.assign(baseStatus, manualInputs.baseStats);
  }

  baseStatus['Monster Def (flat)'] = manualInputs.monsterDef;

  // 2. Add stats from all selected equipment
  for (const equipName of equipmentList) {
    if (!equipName || equipName === 'None') continue;

    let itemData = gameData.Single[equipName];
    let star = null;

    // Detect Star/State prefix for pets (e.g. "3 StarDragon" or "State 4Dragon")
    if (!itemData) {
      const plusMatch = equipName.match(/^\+(\d+)\((.+)\)$/);
      if (plusMatch) {
        star = plusMatch[1];
        const baseName = plusMatch[2].trim();
        if (baseName in gameData.Single) {
          itemData = gameData.Single[baseName];
        }
      } else {
        const starMatch = equipName.match(/^(\d)\s*Star\s*(.+)$/i);
        if (starMatch) {
          star = starMatch[1];
          const baseName = starMatch[2];
          if (baseName in gameData.Single) {
            itemData = gameData.Single[baseName];
          }
        } else {
          const stateMatch = equipName.match(/^State\s*(\d)\s*(.+)$/i);
          if (stateMatch) {
            star = stateMatch[1];
            const baseName = stateMatch[2].trim();
            if (baseName in gameData.Single) {
              itemData = gameData.Single[baseName];
            }
          } else {
            // Detect [Name] [1-3] for engravings (e.g. "Excellence 3")
            const numMatch = equipName.match(/^(.+)\s+(\d)$/);
            if (numMatch) {
              const baseName = numMatch[1].trim();
              star = numMatch[2];
              if (baseName in gameData.Single) {
                itemData = gameData.Single[baseName];
              }
            }
          }
        }
      }
    }

    if (itemData) {
      // If it's a tiered item (like a Pet), apply specific tier stats
      if (itemData.tiers) {
        const tierKey = star || "0";
        addEquipment(baseStatus, itemData.tiers[tierKey] || {});
      } else {
        addEquipment(baseStatus, itemData);
      }

      // Check if item explicitly defines any set points (e.g. multi-sets like Avarice)
      let hasExplicitSet = false;
      for (const key of Object.keys(itemData)) {
        if (key in gameData.Sets) {
          hasExplicitSet = true;
          break;
        }
      }

      // Auto-detect set piece only if no sets are explicitly defined in stats
      if (!hasExplicitSet) {
        let setName = itemData.set_bonus || null;
        
        if (!setName) {
          // Fallback to name-based detection
          for (const s of Object.keys(gameData.Sets)) {
            if (equipName === s || equipName.startsWith(s + ' ') || equipName.startsWith(s + ' (')) {
              setName = s;
              break;
            }
          }
        }

        if (setName) {
          baseStatus[setName] = (baseStatus[setName] || 0) + 1;
        }
      }
    }
  }

  // 3. Apply manual stat adjustments
  baseStatus['Effect Ratio (%)'] = manualInputs.dotRatio;
  baseStatus['Atk (flat)'] += manualInputs.manAtk;
  baseStatus['Crit Dmg (%)'] += manualInputs.manCritDmg;
  baseStatus['Crit Rate (%)'] += manualInputs.manCritRate;
  baseStatus['Elem Boost (%)'] += manualInputs.manElem;
  baseStatus['Cooldown (flat)'] += manualInputs.manCd;
  baseStatus['Agility (flat)'] += manualInputs.manAgility;
  baseStatus['Strength (flat)'] += manualInputs.manStrength;
  baseStatus['Skill DMG (%)'] += manualInputs.manSkillDmg;
  baseStatus['Atk Bonus (%)'] += manualInputs.manAtkBonus;
  baseStatus['Vehicle Collection'] = manualInputs.manVehicle;

  // 4. Handle set bonuses
  const outfits = outfitCount(baseStatus, gameData.Sets);
  let specialBoost = 1;

  // 5. Apply set bonuses and tech boosts
  for (const [setName, count] of outfits) {
    const key = setName + count;

    if (setName in gameData.Sets && count in gameData.Sets[setName]) {
      addEquipment(baseStatus, gameData.Sets[setName][count]);
    }

    if (key === 'Extraordinary4' && manualInputs.boostExtraordinary4 > 0) {
      specialBoost *= 1 + manualInputs.boostExtraordinary4 / 100;
    } else if (key === 'Extraordinary6' && manualInputs.boostExtraordinary6 > 0) {
      specialBoost *= 1 + manualInputs.boostExtraordinary6 / 100;
    } else if (key === 'Excellence4' && manualInputs.boostExcellence4 > 0) {
      specialBoost *= 1 + manualInputs.boostExcellence4 / 100;
    } else if (key === 'Excellence7' && manualInputs.boostExcellence7 > 0) {
      baseStatus['Dmg Bonus (%)'] += manualInputs.boostExcellence7;
    } else if (key === 'Excellence9' && manualInputs.boostExcellence9 > 0) {
      baseStatus['Additional (%)'] += manualInputs.boostExcellence9;
    } else if (key === 'Transcendence9' && manualInputs.boostTranscendence9 > 0) {
      specialBoost *= 1 + manualInputs.boostTranscendence9 / 100;
    }
  }

  // 6. Apply special item/set interactions
  if (equipmentList.includes('Avarice Shoes')) {
    baseStatus['Crit Dmg (%)'] += 3 * (baseStatus['Avarice'] || 0);
  } else if (equipmentList.includes('Demon Heart Shoes')) {
    baseStatus['Crit Dmg (%)'] += 4 * (baseStatus['Avarice'] || 0);
  }

  if (outfits.some(o => o[0] === 'Venom' && o[1] === '2')) {
    const extraKezhi = Math.min(4 * (baseStatus['Venom'] || 0), 16);
    baseStatus['Dmg Debuff (%)'] += extraKezhi;
  } else if (outfits.some(o => o[0] === 'Cursed' && o[1] === '2')) {
    const extraKezhi = Math.min(4 * (baseStatus['Venom'] || 0) + (baseStatus['Cursed'] || 0), 22);
    baseStatus['Dmg Debuff (%)'] += extraKezhi;
  }

  // 7. Calculate derived stats
  const cdrPercentage = (baseStatus['Cooldown (flat)'] / (baseStatus['Cooldown (flat)'] + 1133)) * 100;

  const finalStatus = {
    'Elem Boost (%)': baseStatus['Elem Boost (%)'] || 0,
    'Crit Rate (%)': (baseStatus['Crit Rate (%)'] || 0) - 7e-07 * (baseStatus['Agility (flat)'] || 0) + 0.0125 * (baseStatus['Agility (flat)'] || 0) + 0.3034,
    'Crit Dmg (%)': baseStatus['Crit Dmg (%)'] || 0,
    'Dmg Debuff (%)': baseStatus['Dmg Debuff (%)'] || 0,
    'DMG to Boss (%)': baseStatus['DMG to Boss (%)'] || 0,
    'Dmg Bonus (%)': baseStatus['Dmg Bonus (%)'] || 0,
    'Skill DMG (%)': baseStatus['Skill DMG (%)'] || 0,
    'Resonance DMG (%)': baseStatus['Resonance DMG (%)'] || 0,
    'Elem Dmg (%)': (baseStatus['Elem Dmg (%)'] || 0) + (baseStatus['Elem Boost (%)'] || 0) / 2.2,
    'PDEF Shred (flat)': (baseStatus['PDEF Shred (flat)'] || 0) * (1 + (baseStatus['Def Break Bonus (%)'] || 0) / 100),
    'Atk (flat)': (baseStatus['Atk (flat)'] || 0) * (1 + ((baseStatus['Strength (flat)'] || 0) * (1 + (baseStatus['Strength Bonus (%)'] || 0) / 100)) / 1000) * (1 + (baseStatus['Atk Bonus (%)'] || 0) / 100),
    'Monster Def (flat)': baseStatus['Monster Def (flat)'] || 3000,
    'PEN (flat)': baseStatus['PEN (flat)'] || 0,
    'Def Reduction (%)': baseStatus['Def Reduction (%)'] || 0,
    'Additional (%)': baseStatus['Additional (%)'] || 0,
    'Special (%)': baseStatus['Special (%)'] || 0,
    'Class DMG Bonus (%)': baseStatus['Class DMG Bonus (%)'] || 0,
    'Skill Ratio (%)': baseStatus['Skill Ratio (%)'] || 0,
    'Skill DMG Boost (%)': baseStatus['Skill DMG Boost (%)'] || 0,
    'ASPD (%)': baseStatus['ASPD (%)'] || 0,
    'Cooldown Reduction (%)': (baseStatus['Cooldown Reduction (%)'] || 0) + cdrPercentage,
    'Cooldown (flat)': baseStatus['Cooldown (flat)'] || 0,
    'Effect Ratio (%)': baseStatus['Effect Ratio (%)'] || 0,
  };

  // 8. Final damage computation
  const { burst, sustained } = damageCompute(finalStatus);

  return {
    finalStatus,
    burst: burst * specialBoost,
    sustained: sustained * specialBoost,
    outfits
  };
}
