# AGENTS.md - Crystal Core Panel Calculator

## Project Overview

Streamlit-based web app for calculating damage stats in game "晶核" (Crystal Core).

- `streamlit_app.py` - Main web UI
- `utils_computer.py` - Core damage calculation logic  
- `data.json` - Equipment/stats data
- `tests/test_calculator.py` - Unit tests

---

## Build & Run Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit web app
streamlit run streamlit_app.py

# Run on custom port
streamlit run streamlit_app.py --server.port 8501

# Testing
pip install pytest pytest-cov
pytest                              # Run all tests
pytest tests/test_calculator.py     # Run single file
pytest tests/test_calculator.py::test_name  # Run single test
pytest -k "damage"                 # Run matching pattern
pytest --cov=. --cov-report=html   # With coverage

# Linting
pip install ruff black mypy
ruff check .        # Lint
ruff check --fix .  # Auto-fix
black .             # Format
mypy .              # Type check
```

---

## Features

### Save/Load Builds
- **Save**: Click "💾 Save Build" to download JSON file
- **Load**: Upload a previously saved JSON build file
- Build files contain all equipment, enhancements, engravings, pets, cards, fashion, buffs, and manual inputs

### Damage Formula
The damage calculation uses the game's formula:
```
Damage Reduction % = Defense / (3000 + Defense)
Actual Attack = Total PATK * (1 - Damage Reduction %) + PDEF Shred
```
Where:
- `Def Reduction` = Physical PEN%
- `Def Break Atk` = PDEF Shred (flat defense reduction)
- `Penetration` = Additional flat defense reduction

---

## Code Style Guidelines

### Import Organization
```python
# Standard library (alphabetical)
import json
import os

# Third-party
import streamlit as st

# Local
from utils_computer import damage_compute, add_equipment
```

### Type Hints (Required)
```python
# Good
def damage_compute(status_dict: dict[str, float]) -> tuple[float, float]:
    """Calculate burst and sustained damage."""
    ...

# Avoid - no type hints
def calculate(x):
    ...
```

### Naming Conventions
- **Functions/variables**: `snake_case` (`burst_damage`, `run_calculation`)
- **Classes**: `PascalCase` (`Ui_Form` for PyQt6)
- **Constants**: `UPPER_SNAKE_CASE` (`DEFAULT_BASE_STATUS`)
- **Private**: `_leading_underscore`

### Function Structure
- Max 50 lines per function
- Docstrings for public functions
- Early returns for errors

```python
def run_calculation(equipment_list: list[str], manual_inputs: dict) -> tuple[dict, float, float]:
    """Run damage calculation with equipment and inputs."""
    if not equipment_list:
        return {}, 0.0, 0.0
    base_status = DEFAULT_BASE_STATUS.copy()
    # Process equipment...
    return final_status, burst_damage, total_damage
```

### Error Handling
```python
@st.cache_data
def load_data() -> dict:
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Could not find data.json")
        return {"Single": {}, "Sets": {}}
    except json.JSONDecodeError as e:
        st.error(f"Invalid JSON: {e}")
        return {"Single": {}, "Sets": {}}

# Never use bare except
```

### Streamlit Patterns

**Session State:**
```python
if 'snapshot' not in st.session_state:
    st.session_state.snapshot = None
```

**Caching:**
```python
@st.cache_data
def load_data() -> dict:
    ...

# With TTL
@st.cache_data(ttl=300)
def fetch_remote_data() -> dict:
    ...
```

**Fragment (isolated recalculation):**
```python
@st.fragment
def calculation_fragment(equipment_list, manual_inputs):
    final_status, burst_damage, total_damage = run_calculation(equipment_list, manual_inputs)
    return final_status, burst_damage, total_damage
```

**Build Save/Load (must be before widgets):**
```python
def handle_build_load():
    """Process build file upload at startup, before any widgets are created."""
    upload_key = "_build_upload"
    if upload_key in st.session_state and st.session_state[upload_key] is not None:
        # Load and apply build to session state
        ...
```

---

## Data Conventions

- `data.json`: `Single` for items, `Sets` for set bonuses
- Constants at module level (`DEFAULT_BASE_STATUS`)
- Descriptive keys matching game terminology

---

## Testing Guidelines

```python
import pytest
from utils_computer import damage_compute, add_equipment

class TestDamageCompute:
    def test_basic_damage(self):
        status = {'Crit Rate': 50, 'Crit Dmg': 150, 'Atk': 1000}
        burst, sustained = damage_compute(status)
        assert burst > 0
        
    def test_zero_crit_rate(self):
        status = {'Crit Rate': 0, 'Crit Dmg': 150, 'Atk': 1000}
        burst, sustained = damage_compute(status)
        assert burst < 1000
```

---

## Performance Tips

1. Use `@st.fragment` for expensive calculations that should run independently
2. Cache icon file existence checks with `@st.cache_data`
3. Validate data.json structure at load time
4. Use `BUILD_WIDGET_KEYS` constant to track all session state keys for save/load

---

## Changelog

### v1.1 - Performance & Quality Improvements
- Fixed critical bug: Weapon Enhancement (Def Break Atk) now correctly affects burst damage
- Added `@st.fragment` for partial re-rendering (improves performance)
- Added type hints to all functions
- Implemented save/load build functionality with JSON files
- Added icon file existence caching
- Added data validation on load
- Created comprehensive unit tests (11 tests passing)
- Updated `.gitignore` with proper patterns

### Known Issues
- **Resonance Effect I/II**: Enhancement tiers add these stats but they are collected but not applied to damage calculation (needs research)

---

## Deployment

- Deploy to Streamlit Community Cloud
- Key files: `streamlit_app.py`, `requirements.txt`, `data.json`, `utils_computer.py`, `tests/`
- No build step required
