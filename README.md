# Crystal Core Panel Calculator (Streamlit Web App)

**Live Website:** [https://coa-translation.streamlit.app/](https://coa-translation.streamlit.app/)

This is a web-based damage calculator for the game **Crystal Core (晶核)**. It allows players to simulate their character's stats based on equipment, enchantments, emblems, pets, and buffs to calculate theoretical damage output.

This project is a web port of the original desktop application, designed to be easily accessible via a browser.

## Features

*   **Full Equipment Configuration**: Select Armor, Weapons, Accessories, and Treasures.
*   **Detailed Customization**: Configure Enchantments, Emblems, and Engravings (Techniques).
*   **Pet & Card System**: Support for Pet selection, Pet Souls, and Cards.
*   **Fashion & Buffs**: Include Fashion stats and consumable buffs (Potions, Wines, etc.).
*   **Real-time Calculation**: Instantly see Burst Damage and Sustained Damage (DPS) updates.
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

## Deployment

This app is designed to be deployed easily on **Streamlit Community Cloud**:

1.  Push this code to a GitHub repository.
2.  Go to share.streamlit.io.
3.  Select the repository and the main file (`streamlit_app.py`).
4.  Click **Deploy**.

## Credits

*   **Original Desktop App & Logic**: Bilibili: 丶霜月流星
*   **Translation & Web Port**: NSYok
