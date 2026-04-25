# Crystal of Atlan Panel Calculator (Streamlit Web App)

**Live Website (Fast Web Version):** [https://coa-calculator.netlify.app/](https://coa-calculator.netlify.app/)
**Live Website (Python Version):** [https://coa-calculator-webapp.streamlit.app/](https://coa-calculator-webapp.streamlit.app/)

This is a web-based damage calculator for the game **Crystal of Atlan (晶核)**. It allows players to simulate their character's stats based on equipment, enchantments, emblems, pets, and buffs to calculate theoretical damage output.

This project is a web port of the original desktop application, designed to be easily accessible via a browser.

## Features

*   **Full Equipment Configuration**: Select Armor, Weapons, Accessories, and Treasures.
*   **Detailed Customization**: Configure Enchantments, Emblems, and Engravings (Techniques).
*   **Pet & Card System**: Support for Pet selection, Pet Souls, and Cards.
*   **Fashion & Buffs**: Include Fashion stats and consumable buffs (Potions, Wines, etc.).
*   **Real-time Calculation**: Instantly see Burst Damage and Sustained Damage (DPS) updates.
*   **Save/Load Builds**: Save and load complete build configurations to/from JSON files.
*   **Snapshot Comparison**: Compare your current build against a saved snapshot.

## How to Run Locally

1.  **Prerequisites**: Ensure you have Python installed (version 3.8 or higher recommended).

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**:
    ```bash
    streamlit run streamlit_app.py
    ```

4.  The app should open automatically in your default web browser at `http://localhost:8501`.

## Development

### Testing
To run the test suite:
```bash
pip install pytest pytest-cov
pytest
```

### Linting & Formatting
To lint and format the codebase:
```bash
# Lint
ruff check .
# Auto-fix
ruff check --fix .
# Format
black .
```

## Deployment

### Python Version (Streamlit)
This app is designed to be deployed easily on **Streamlit Community Cloud**:

1.  Push this code to a GitHub repository.
2.  Go to share.streamlit.io.
3.  Select the repository and the main file (`streamlit_app.py`).
4.  Click **Deploy**.

### Web Version (Netlify / Vercel / GitHub Pages)
The Vite-based web version (located in the `web/` directory) can be deployed to any static hosting provider:

1.  **Build the project**:
    ```bash
    cd web
    npm install
    npm run build
    ```
2.  **Deploy**:
    *   **Netlify**: Drag and drop the `web/dist` folder or connect your GitHub repository and set the build command to `npm run build` and the publish directory to `web/dist`.
    *   **Vercel**: Import the repository, set the "Root Directory" to `web`, and it will automatically detect the Vite configuration.
    *   **Cloudflare Pages**: Connect your GitHub, select the `web` directory, and use the Vite preset.

## Credits

*   **Original Desktop App & Logic**: Bilibili: 丶霜月流星
*   **Translation & Web Port**: NSYok
*   **Damage Formula Reference**: [Boarhat - Damage Formula Guide](https://boarhat.gg/games/crystal-of-atlan/guide/damage-formula-guide/)

## Data Schema (data.json)

The data.json file contains all the equipment, sets, and buffs. Here is an explanation of the statistics used within the JSON to calculate damage:

### Primary Stats
*   **Base Atk**: Flat Base Attack (PATK or MATK).
*   **Atk Bonus**: Percentage increase to Base Attack (ATK %).
*   **Strength**: Primary main stat (Strength for Physical, Intelligence for Magic).
*   **Str Bonus**: Percentage increase to Strength.
*   **Agility**: Agility stat (provides base Crit Rate).

### Critical & Elemental
*   **Crit Rate**: Critical Hit Rate percentage.
*   **Crit Dmg**: Critical Damage multiplier percentage.
*   **Elem Boost**: Elemental Boost stat (scales into Elem Dmg).
*   **Elem Dmg**: Flat Elemental Damage (also known as ENH DMG).

### Damage Multipliers
*   **Dmg Amp**: General Damage Bonus / Amplification (%).
*   **Skill Dmg**: Bonus damage applied to skills.
*   **dmgToDebuff**: Damage multiplier against Debuffed/Abnormal status targets.
*   **Boss Dmg**: Damage multiplier specifically against Boss enemies.
*   **Class Dmg**: Class-specific damage bonus (%).
*   **Resonance Dmg**: Bonus damage while in Resonance state.
*   **Extra Dmg**: Additional/Extra damage modifier (Can find it in set Bonus).
*   **Special**: Special independent damage multiplier.
*   **Multiplier**: Skill ratio multiplier (Active Skill Lv 1-30:0.5, 30-60:2.5, 45-60:2, 1-60:3, 1-70:4) .
*   **Skill Dmg Boost**: Overall skill damage boost.

### Defense Penetration
*   **Def Reduction**: Percentage-based Defense Penetration (%).
*   **Def Break Atk**: Flat Defense Shred.
*   **Penetration**: Additional Flat Defense Reduction.

### Utility
*   **Skill Haste**: Attack speed / animation speed modifier (ASPD).
*   **Cooldown**: Cooldown reduction (%).
*   **Effect Ratio**: Status effect application ratio.
