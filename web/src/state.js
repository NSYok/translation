/**
 * State Manager with localStorage persistence and lightweight subscriptions.
 *
 * @module state
 */

const STORAGE_KEY = 'coa_calculator_state';
const SNAPSHOT_KEY = 'coa_calculator_snapshot';

/** @type {Record<string, unknown>} */
let _state = {};

/** @type {Map<string, Set<Function>>} */
const _keyListeners = new Map();

/** @type {Set<Function>} */
const _globalListeners = new Set();

/**
 * Initialize state from localStorage or defaults.
 * @param {Record<string, unknown>} defaults
 */
export function initState(defaults) {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (!saved) {
    _state = { ...defaults };
    return;
  }

  try {
    _state = { ...defaults, ...JSON.parse(saved) };
  } catch {
    _state = { ...defaults };
  }
}

/**
 * Get a single state value.
 * @param {string} key
 * @returns {unknown}
 */
export function getState(key) {
  return _state[key];
}

/**
 * Get a shallow copy of the current state.
 * @returns {Record<string, unknown>}
 */
export function getAllState() {
  return { ..._state };
}

/**
 * Set a single state value and notify listeners.
 * @param {string} key
 * @param {unknown} value
 */
export function setState(key, value) {
  _state[key] = value;
  _persist();
  _notify([key]);
}

/**
 * Batch-set multiple values and notify listeners once.
 * @param {Record<string, unknown>} updates
 */
export function setStateBatch(updates) {
  Object.assign(_state, updates);
  _persist();
  _notify(Object.keys(updates));
}

/**
 * Subscribe to state changes.
 * Supports either `subscribe(listener)` or `subscribe(key, listener)`.
 * `key` may also be `*` for all updates.
 *
 * @param {string|Function} keyOrListener
 * @param {Function=} maybeListener
 * @returns {Function}
 */
export function subscribe(keyOrListener, maybeListener) {
  if (typeof keyOrListener === 'function') {
    _globalListeners.add(keyOrListener);
    return () => _globalListeners.delete(keyOrListener);
  }

  const key = keyOrListener;
  const listener = maybeListener;
  if (typeof listener !== 'function') {
    return () => {};
  }

  if (key === '*') {
    _globalListeners.add(listener);
    return () => _globalListeners.delete(listener);
  }

  if (!_keyListeners.has(key)) {
    _keyListeners.set(key, new Set());
  }
  const bucket = _keyListeners.get(key);
  bucket.add(listener);
  return () => bucket.delete(listener);
}

/**
 * Save a build result snapshot for later comparison.
 * @param {{ finalStatus: Record<string, number>, burst: number, sustained: number } | null} snapshot
 */
export function saveSnapshot(snapshot) {
  if (!snapshot) {
    localStorage.removeItem(SNAPSHOT_KEY);
    return;
  }
  localStorage.setItem(SNAPSHOT_KEY, JSON.stringify(snapshot));
}

/**
 * Read the saved snapshot, if any.
 * @returns {{ finalStatus: Record<string, number>, burst: number, sustained: number } | null}
 */
export function getSnapshot() {
  const saved = localStorage.getItem(SNAPSHOT_KEY);
  if (!saved) return null;

  try {
    return JSON.parse(saved);
  } catch {
    return null;
  }
}

/**
 * Remove the saved snapshot.
 */
export function clearSnapshot() {
  localStorage.removeItem(SNAPSHOT_KEY);
}

/**
 * Export the current build JSON.
 * @returns {string}
 */
export function exportBuild() {
  return JSON.stringify(_state, null, 2);
}

/**
 * Import a build from either a JSON string or a plain object.
 * @param {string|Record<string, unknown>} payload
 * @returns {boolean}
 */
export function importBuild(payload) {
  try {
    const loaded = typeof payload === 'string' ? JSON.parse(payload) : payload;
    if (!loaded || typeof loaded !== 'object') {
      return false;
    }
    Object.assign(_state, loaded);
    _persist();
    _notify(Object.keys(loaded));
    return true;
  } catch {
    return false;
  }
}

function _persist() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(_state));
}

/**
 * @param {string[]} changedKeys
 */
function _notify(changedKeys) {
  const seen = new Set();

  for (const key of changedKeys) {
    const listeners = _keyListeners.get(key);
    if (!listeners) continue;

    for (const listener of listeners) {
      if (seen.has(listener)) continue;
      seen.add(listener);
      try {
        listener(_state[key], key, { ..._state });
      } catch (error) {
        console.error('State listener error:', error);
      }
    }
  }

  for (const listener of _globalListeners) {
    if (seen.has(listener)) continue;
    try {
      listener({ ..._state }, changedKeys);
    } catch (error) {
      console.error('State listener error:', error);
    }
  }
}
