import sqlite3
import os
import random
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bal_sadan.db')

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # 1. Donations Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt_no TEXT UNIQUE NOT NULL,
            donor_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            category TEXT NOT NULL,
            amount REAL DEFAULT 0,
            item_description TEXT,
            payment_method TEXT DEFAULT 'UPI / QR',
            status TEXT DEFAULT 'Pledged',
            occasion TEXT,
            blessing_message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Visits & Snack Distribution Appointments Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_ref TEXT UNIQUE NOT NULL,
            visitor_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            visit_date TEXT NOT NULL,
            time_slot TEXT NOT NULL,
            purpose TEXT NOT NULL,
            snack_items TEXT,
            guest_count INTEGER DEFAULT 1,
            status TEXT DEFAULT 'Confirmed',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 3. Volunteer Applications Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS volunteers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            skills TEXT,
            availability TEXT,
            occupation TEXT,
            message TEXT,
            status TEXT DEFAULT 'New',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 4. Inquiries Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            subject TEXT,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'Unread',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 5. Inventory & Urgent Needs Wishlist Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory_needs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT NOT NULL,
            target_qty INTEGER NOT NULL,
            fulfilled_qty INTEGER DEFAULT 0,
            unit TEXT NOT NULL,
            urgency TEXT DEFAULT 'High',
            description TEXT
        )
    ''')

    # 6. AI Chat Logs Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_query TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            intent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()

    # Seed initial inventory items if empty
    cursor.execute('SELECT COUNT(*) as count FROM inventory_needs')
    if cursor.fetchone()['count'] == 0:
        seed_inventory(cursor)
        seed_sample_records(cursor)
        conn.commit()

    conn.close()

def seed_inventory(cursor):
    initial_items = [
        ("Evening Snacks Packs (Biscuits, Fruit Cakes, Poha)", "Snacks & Nutrition", 100, 65, "Packs", "Urgent", "Nutritious daily afternoon snacks for 45 children (3:00 PM slot)"),
        ("Fresh Seasonal Fruits (Bananas, Apples, Oranges)", "Snacks & Nutrition", 60, 42, "Kg", "High", "Weekly fresh fruit distribution for child immunity & health"),
        ("Milk & Health Drink Mix (Bournvita/Horlicks)", "Snacks & Nutrition", 30, 18, "Kg", "High", "Daily morning & evening nutritional drinks"),
        ("School Notebooks & Geometry Sets", "Education", 120, 85, "Sets", "Urgent", "Class 1 to 10 school supplies for current academic term"),
        ("School Uniforms & Casual Shoes", "Clothing", 45, 30, "Pairs", "Moderate", "All season comfortable clothes and footwear"),
        ("Personal Hygiene Kits (Soap, Toothpaste, Oil)", "Health & Hygiene", 50, 38, "Kits", "Moderate", "Monthly hygiene & wellness supplies")
    ]
    cursor.executemany('''
        INSERT INTO inventory_needs (item_name, category, target_qty, fulfilled_qty, unit, urgency, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', initial_items)

def seed_sample_records(cursor):
    # Sample Donations
    sample_donations = [
        ('SKD-2026-1001', 'Anand Kulkarni', '9822345678', 'anand.k@example.com', 'Afternoon Snacks & Fruits', 3500, 'Donated 50 fruit packs and biscuits for evening snack time', 'UPI / QR', 'Completed', 'Son Birthday', 'Blessing the children on Aarav 10th birthday!'),
        ('SKD-2026-1002', 'Sunita R. Agrawal', '9423112233', 'sunita.ag@example.com', 'School Education Kits', 5000, '20 sets of notebooks, geometry boxes, and backpacks', 'Bank Transfer', 'Completed', 'Annual Remembrance', 'May every child achieve their education dreams.'),
        ('SKD-2026-1003', 'Ramesh & Priya Joshi', '7798123456', 'ramesh.joshi@example.com', 'Birthday Meal Sponsorship', 4500, 'Hot afternoon snacks (Samosa, Sweet treat & Mango juice)', 'UPI / QR', 'Completed', 'Wedding Anniversary', 'Sharing joy with the lovely kids of Bal Sadan.')
    ]
    cursor.executemany('''
        INSERT INTO donations (receipt_no, donor_name, phone, email, category, amount, item_description, payment_method, status, occasion, blessing_message)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_donations)

    # Sample Visits
    sample_visits = [
        ('VISIT-101', 'Dr. Meena Deshmukh', '9890123456', 'meena.d@example.com', '2026-10-25', '3:00 PM - 4:00 PM', 'Snack Distribution', 'Fresh Bananas, Frooti and Marie Biscuits for 45 children', 3, 'Approved', 'Will arrive at 3:15 PM sharp at Lakad Ganj campus.'),
        ('VISIT-102', 'Vikram Patel', '9765432109', 'vikram.p@example.com', '2026-10-27', '4:00 PM - 5:00 PM', 'Birthday Celebration', 'Birthday cake, vegetable patties and sweet laddoos', 4, 'Approved', 'Celebrating daughter birthday with all kids.')
    ]
    cursor.executemany('''
        INSERT INTO visits (booking_ref, visitor_name, phone, email, visit_date, time_slot, purpose, snack_items, guest_count, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_visits)

def generate_receipt_no():
    year = datetime.now().year
    rand_num = random.randint(1000, 9999)
    return f"SKD-{year}-{rand_num}"

def generate_booking_ref():
    rand_num = random.randint(100, 999)
    return f"VISIT-{rand_num}"

# CRUD Helper functions
def add_donation(donor_name, phone, email, category, amount, item_description, payment_method, occasion, blessing_message):
    receipt_no = generate_receipt_no()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO donations (receipt_no, donor_name, phone, email, category, amount, item_description, payment_method, status, occasion, blessing_message)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Confirmed', ?, ?)
    ''', (receipt_no, donor_name, phone, email, category, float(amount or 0), item_description, payment_method, occasion, blessing_message))
    conn.commit()
    donation_id = cursor.lastrowid
    conn.close()
    return receipt_no, donation_id

def add_visit(visitor_name, phone, email, visit_date, time_slot, purpose, snack_items, guest_count, notes):
    booking_ref = generate_booking_ref()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO visits (booking_ref, visitor_name, phone, email, visit_date, time_slot, purpose, snack_items, guest_count, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Confirmed', ?)
    ''', (booking_ref, visitor_name, phone, email, visit_date, time_slot, purpose, snack_items, int(guest_count or 1), notes))
    conn.commit()
    visit_id = cursor.lastrowid
    conn.close()
    return booking_ref, visit_id

def add_volunteer(name, phone, email, skills, availability, occupation, message):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO volunteers (name, phone, email, skills, availability, occupation, message)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, phone, email, skills, availability, occupation, message))
    conn.commit()
    vol_id = cursor.lastrowid
    conn.close()
    return vol_id

def add_inquiry(name, email, phone, subject, message):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO inquiries (name, email, phone, subject, message)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, email, phone, subject, message))
    conn.commit()
    inq_id = cursor.lastrowid
    conn.close()
    return inq_id

def get_all_donations():
    conn = get_db()
    rows = conn.execute('SELECT * FROM donations ORDER BY created_at DESC').fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_donation_by_receipt(receipt_no):
    conn = get_db()
    row = conn.execute('SELECT * FROM donations WHERE receipt_no = ?', (receipt_no,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_visits():
    conn = get_db()
    rows = conn.execute('SELECT * FROM visits ORDER BY visit_date DESC, time_slot ASC').fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_volunteers():
    conn = get_db()
    rows = conn.execute('SELECT * FROM volunteers ORDER BY created_at DESC').fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_inquiries():
    conn = get_db()
    rows = conn.execute('SELECT * FROM inquiries ORDER BY created_at DESC').fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_inventory():
    conn = get_db()
    rows = conn.execute('SELECT * FROM inventory_needs ORDER BY id ASC').fetchall()
    conn.close()
    return [dict(r) for r in rows]

def log_ai_interaction(query, response, intent):
    conn = get_db()
    conn.execute('''
        INSERT INTO ai_conversations (user_query, bot_response, intent)
        VALUES (?, ?, ?)
    ''', (query, response, intent))
    conn.commit()
    conn.close()

def get_dashboard_stats():
    conn = get_db()
    cursor = conn.cursor()
    
    total_donations_count = cursor.execute('SELECT COUNT(*) FROM donations').fetchone()[0]
    total_funds = cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM donations').fetchone()[0]
    total_visits = cursor.execute('SELECT COUNT(*) FROM visits').fetchone()[0]
    total_volunteers = cursor.execute('SELECT COUNT(*) FROM volunteers').fetchone()[0]
    pending_inquiries = cursor.execute('SELECT COUNT(*) FROM inquiries WHERE status = "Unread"').fetchone()[0]
    
    conn.close()
    return {
        'donations_count': total_donations_count,
        'total_funds': total_funds,
        'visits_count': total_visits,
        'volunteers_count': total_volunteers,
        'unread_inquiries': pending_inquiries
    }
