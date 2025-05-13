# HungerHeal 🍲

**HungerHeal** is a real-time, location-based platform to connect food donors (restaurants, grocery stores, bakeries, caterers, individuals) with receivers (NGOs, shelters, volunteers, families in need). The goal is to reduce food waste and help those in need by making surplus food available quickly and safely.

## Features
- **Post Surplus Food:** Donors can post available food with details, contact info, and optional ID verification for credibility.
- **Find Available Food:** Receivers can search for food by address and view posts on an interactive map.
- **Trust Score:** Each post displays a trust score based on provided information and verification, with color-coded markers for quick assessment.
- **Safety Guidelines:** Built-in safety tips for both donors and receivers.
- **Real-Time Countdown:** Each food post shows the time left to claim it, based on expiry.

## How It Works
1. **Donors** fill out a form with food details, contact info, and pickup address. Optionally, they can upload an ID for extra credibility.
2. **Receivers** search for food by entering an address and view available posts on a map.
3. Each post includes all relevant info, trust score, and a countdown timer for how long the food will be available.

## Setup Instructions

### Prerequisites
- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/)

### Installation
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd HungerHeal
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Firebase Setup:**
   - Create a Firebase project and Firestore database.
   - Download your service account key as `service_account.json` and place it in the project root.
   - See instructions in the app if you need help.

### Running the App
```bash
streamlit run app.py
```

## File Structure
- `app.py` - Main Streamlit app
- `firebase_config.py` - Firebase/Firestore integration
- `geo_utils.py` - Geocoding utilities
- `requirements.txt` - Python dependencies

## Customization
- You can adjust trust score logic, marker colors, and safety guidelines in `app.py`.
- To add more fields or change the form, edit the food post form section in `app.py`.

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](LICENSE)

---
**HungerHeal**: No one should go hungry while good food is thrown away. 
