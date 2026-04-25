/**
 * State Manager — Build state with localStorage persistence
 * Replaces Streamlit's st.session_state
 * 
 * @module state
 */

const STORAGE_KEY = 'coa_calculator_state';
const SNAPSHOT_KEY = 'coa_calculator_snapshot';

/** @type {Object} */
let _state = {};

/** @type {Set<Function>} */
const _listeners = new Set();

/**
 * Initialize state from localStorage or defaults
 * @param {Object} defaults - Default values for all keys
 */
export function initState(defaults) {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (saved) {
    try {
      _state = { ...defaults, ...JSON.parse(saved) };
    } catch {
      _state = { ...defaults };
    }
  } else {
    _state = { ...defaults };
  }
}

/**
 * Get a state value
 * @param {string} key 
 * @returns {*}
 */
export function getState(key) {
  return _state[key];
}

/**
 * Set a state value and notify listeners
 * @param {string} key 
 * @param {*} value 
 */
export function setState(key, value) {
  _state[key] = value;
  _persist();
  _notify();
}

/**
 * Batch-set multiple values and notify once
 * @param {Object} updates 
 */
export function setStateBatch(updates) {
  Object.assign(_state, updates);
  _persist();
  _notify();
}

/**
 * Get all state
 * @returns {Object}
 */
export function getAllState() {
  return { ..._state };
}

/**
 * Subscribe to state changes
 * @param {Function} listener 
 * @returns {Function} Unsubscribe function
 */
export function subscribe(listener) {
  _listeners.add(listener);
  return () => _listeners.delete(listener);
}

/**
 * Save a snapshot for comparison
 * @param {{ finalStatus: Object, burst: number, sustained: number }} snapshot 
 */
export function saveSnapshot(snapshot) {
  localStorage.setItem(SNAPSHOT_KEY, JSON.stringify(snapshot));
}

/**
 * Get saved snapshot
 * @returns {{ finalStatus: Object, burst: number, sustained: number } | null}
 */
export function getSnapshot() {
  const saved = localStorage.getItem(SNAPSHOT_KEY);
  if (saved) {
    try { return JSON.parse(saved); } catch { return null; }
  }
  return null;
}

/** Clear snapshot */
export function clearSnapshot() {
  localStorage.removeItem(SNAPSHOT_KEY);
}

/**
 * Export current build as JSON string
 * @returns {string}
 */
export function exportBuild() {
  return JSON.stringify(_state, null, 2);
}

/**
 * Import a build from JSON string
 * @param {string} jsonStr 
 */
export function importBuild(jsonStr) {
  try {
    const loaded = JSON.parse(jsonStr);
    Object.assign(_state, loaded);
    _persist();
    _notify();
    return true;
  } catch {
    return false;
  }
}

function _persist() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(_state));
}

function _notify() {
  for (const listener of _listeners) {
    try { listener(_state); } catch (e) { console.error('State listener error:', e); }
  }
}
