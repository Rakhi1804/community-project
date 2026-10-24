# Sir Kasturchand Daga Bal Sadan, Kamptee
### Official Website with Integrated Database & AI Assistant

An elegant, full-featured web application built for **Sir Kasturchand Daga Bal Sadan**, a historic orphanage and children's home located in **Lakad Ganj, Kamptee, Maharashtra 441001**.

---

## 📍 Key Orphanage Information
- **Organization Name:** Sir Kasturchand Daga Bal Sadan
- **Category:** Orphanage & Children's Home (Bal Sadan)
- **Address:** Lakad Ganj, Kamptee, Maharashtra 441001 (Nagpur District)
- **Direct Phone:** `077095 58334` (+91 77095 58334)
- **WhatsApp Support:** [+91 77095 58334](https://wa.me/917709558334)
- **Office Opening Hours:** Daily from **11:00 AM** onwards
- **Core Announcement & Snack Visiting Policy:** 
  > *"Donation towards children like snacks for this time is **Monday to Saturday from 3:00 PM onwards**."*

---

## 🌟 Key Features

### 1. Dedicated Afternoon Snack & Nutrition Portal (`/donate-snacks`)
- Prominently highlights the visiting schedule: **Monday to Saturday from 3:00 PM onwards**.
- Recommended snack categories table (Fresh Fruits, Warm Savory Snacks, Branded Biscuits & Juice Cartons).
- Interactive **Schedule a Snack Drop-off & Visit** form directly connected to the SQLite database.
- Immediate generation of confirmation reference ID (`VISIT-XXX`) to prevent overlapping visits.

### 2. Full SQLite Database Integration (`bal_sadan.db`)
- **Donations Table:** Records donor particulars, amount, category, payment method, occasion, and timestamp.
- **Visits Table:** Tracks visitor appointments for afternoon snack distributions and birthday celebrations.
- **Inventory & Urgent Needs:** Live database tracking target vs. fulfilled items (notebooks, fruits, snack packs, hygiene kits) with real-time percentage progress bars.
- **Volunteers Table:** Captures applications for academic tutoring, evening snack assistance, sports, and arts.
- **Inquiries Table:** Stores messages and queries from the public.
- **AI Logs Table:** Records chatbot questions and responses for audit and continuous improvement.

### 3. Integrated AI Engine & Assistant ("Mitra")
- **Floating AI Assistant Widget:** Available on every page with quick query pills and intelligent responses in **English, Hindi, and Marathi**.
- **AI Snack & Nutrition Meal Planner (`/ai-assistant`):**
  - Interactive calculator based on child count (default: 45 children) and budget.
  - Generates recommended nutritious menus (proteins, natural vitamins) with itemized serving portions.
- **AI Blessing & Gratitude Letter Generator:**
  - Auto-composes heartfelt personalized prayer and acknowledgment letters from the children for donors and birthday celebrants.
- **Dual Engine Architecture:**
  - Fast, context-aware NLP Semantic Engine running 100% locally with zero external API dependencies.
  - Automatic upgrade to Google Gemini API when `GEMINI_API_KEY` is provided in the environment.

### 4. Monetary Donation & Sponsorship Portal (`/donate`)
- Interactive UPI QR code preview (Google Pay, PhonePe, Paytm, BHIM) and official bank transfer details.
- Preset amounts for snacks, birthday meals, school kits, and general welfare.
- **Instant Official Receipt Generator (`/receipt/<receipt_no>`):**
  - Generates a print-ready, high-trust donation receipt with a unique serial number (`SKD-2026-XXXX`), official stamp, and personalized AI blessing note.

### 5. Administration Dashboard (`/admin`)
- Secure admin login (PIN: `balsadan123`).
- Real-time KPI statistics: Total funds raised, scheduled visits, active volunteers, unread inquiries.
- Tabular management to approve/complete visits, update live inventory quantities, review donor pledges, and inspect messages.

---

## 🚀 How to Run the Application

### Prerequisites
- Python 3.10+ (Tested on Python 3.15)
- Pip

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the Application
```bash
python app.py
```

### 3. Open in Browser
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

### 4. Admin Access
- URL: `http://127.0.0.1:5000/admin`
- Security PIN: `balsadan123`

---

## 📁 Project Directory Structure
```
community-project/
├── app.py                  # Main Flask application and API routes
├── database.py             # SQLite schema, CRUD operations, and sample seeds
├── ai_engine.py            # AI assistant, snack planner, and blessing generator
├── bal_sadan.db            # SQLite database file (auto-generated on startup)
├── requirements.txt        # Python package dependencies
├── README.md               # Complete project documentation
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Base layout with navbar, footer & floating AI widget
│   ├── index.html          # Homepage with hero, stats, urgent wishlist & routine
│   ├── donate_snacks.html  # Dedicated page for 3 PM+ snack donation & slot booking
│   ├── donate.html         # Monetary donation portal with UPI QR code
│   ├── receipt.html        # Official printable donation acknowledgment receipt
│   ├── ai_assistant.html   # Full AI suite (Chat, Snack Planner & Blessing Generator)
│   ├── volunteer.html      # Volunteer application page
│   ├── contact.html        # Contact details, Kamptee directions & inquiry form
│   ├── admin_login.html    # Secure admin authentication
│   └── admin.html          # Administrative management dashboard
└── static/
    ├── css/
    │   └── style.css       # Custom modern stylesheet, animations & responsive styles
    └── js/
        ├── main.js         # Core UI interactions, date validation & toast handling
        └── ai-chat.js      # Asynchronous chat widget script
```
