import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import database
import ai_engine

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "bal-sadan-kamptee-secret-2026")

# Initialize database on startup
database.init_db()

@app.context_processor
def inject_global_data():
    return {
        'org_name': ai_engine.BAL_SADAN_INFO['name'],
        'org_address': ai_engine.BAL_SADAN_INFO['location'],
        'org_phone': ai_engine.BAL_SADAN_INFO['phone'],
        'org_phone_display': ai_engine.BAL_SADAN_INFO['phone_display'],
        'org_opening': ai_engine.BAL_SADAN_INFO['opening_time'],
        'snack_notice': ai_engine.BAL_SADAN_INFO['snack_donation_notice'],
        'visiting_hours': ai_engine.BAL_SADAN_INFO['visiting_hours'],
        'children_count': ai_engine.BAL_SADAN_INFO['current_children_count']
    }

# ================= PAGES =================

@app.route('/')
def home():
    inventory = database.get_inventory()
    stats = database.get_dashboard_stats()
    return render_template('index.html', inventory=inventory, stats=stats)

@app.route('/donate-snacks')
def donate_snacks():
    return render_template('donate_snacks.html', recommended_snacks=ai_engine.RECOMMENDED_SNACKS)

@app.route('/donate')
def donate():
    return render_template('donate.html')

@app.route('/receipt/<receipt_no>')
def view_receipt(receipt_no):
    donation = database.get_donation_by_receipt(receipt_no)
    if not donation:
        flash("Donation receipt not found.", "warning")
        return redirect(url_for('home'))
    return render_template('receipt.html', donation=donation)

@app.route('/ai-assistant')
def ai_assistant_page():
    return render_template('ai_assistant.html')

@app.route('/volunteer')
def volunteer():
    return render_template('volunteer.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Admin login check (simple passcode: 'balsadan123' or toggle)
    if request.method == 'POST':
        pin = request.form.get('admin_pin', '').strip()
        if pin == 'balsadan123' or pin == 'admin':
            session['admin_logged_in'] = True
            flash("Welcome to the Admin Dashboard!", "success")
            return redirect(url_for('admin'))
        else:
            flash("Invalid security PIN. Please try again.", "danger")

    if not session.get('admin_logged_in'):
        return render_template('admin_login.html')

    donations = database.get_all_donations()
    visits = database.get_all_visits()
    volunteers = database.get_all_volunteers()
    inquiries = database.get_all_inquiries()
    inventory = database.get_inventory()
    stats = database.get_dashboard_stats()

    return render_template('admin.html',
                           donations=donations,
                           visits=visits,
                           volunteers=volunteers,
                           inquiries=inquiries,
                           inventory=inventory,
                           stats=stats)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash("You have logged out of the admin panel.", "info")
    return redirect(url_for('admin'))

# ================= APIS =================

@app.route('/api/ai/chat', methods=['POST'])
def api_ai_chat():
    data = request.get_json(silent=True) or request.form
    user_query = data.get('query', '').strip()
    if not user_query:
        return jsonify({'error': 'Query cannot be empty'}), 400

    result = ai_engine.process_ai_query(user_query)
    # Log to SQLite
    database.log_ai_interaction(user_query, result['reply'], result.get('intent', 'general'))

    return jsonify({
        'reply': result['reply'],
        'intent': result.get('intent', 'general')
    })

@app.route('/api/ai/plan-snack', methods=['POST'])
def api_plan_snack():
    data = request.get_json(silent=True) or request.form
    child_count = data.get('child_count', 45)
    budget = data.get('budget', None)
    occasion = data.get('occasion', 'General Visit')

    plan = ai_engine.plan_snack_menu(child_count, budget, occasion)
    return jsonify(plan)

@app.route('/api/ai/blessing', methods=['POST'])
def api_generate_blessing():
    data = request.get_json(silent=True) or request.form
    donor_name = data.get('donor_name', 'Generous Supporter')
    occasion = data.get('occasion', 'Blessing day')
    category = data.get('category', 'Afternoon Snacks & Nutrition')

    letter = ai_engine.generate_blessing_letter(donor_name, occasion, category)
    return jsonify({'letter': letter})

@app.route('/api/donate', methods=['POST'])
def api_submit_donation():
    donor_name = request.form.get('donor_name')
    phone = request.form.get('phone')
    email = request.form.get('email', '')
    category = request.form.get('category', 'Afternoon Snacks & Fruits')
    amount = request.form.get('amount', 0)
    item_description = request.form.get('item_description', '')
    payment_method = request.form.get('payment_method', 'UPI / QR')
    occasion = request.form.get('occasion', '')
    blessing_message = request.form.get('blessing_message', '')

    if not donor_name or not phone:
        flash("Name and Phone Number are required.", "danger")
        return redirect(url_for('donate'))

    # If blessing message not provided, generate warm letter
    if not blessing_message:
        blessing_message = ai_engine.generate_blessing_letter(donor_name, occasion, category)

    receipt_no, _ = database.add_donation(
        donor_name=donor_name,
        phone=phone,
        email=email,
        category=category,
        amount=amount,
        item_description=item_description,
        payment_method=payment_method,
        occasion=occasion,
        blessing_message=blessing_message
    )

    flash(f"Thank you, {donor_name}! Your pledge has been registered with Receipt #{receipt_no}.", "success")
    return redirect(url_for('view_receipt', receipt_no=receipt_no))

@app.route('/api/visit/book', methods=['POST'])
def api_book_visit():
    visitor_name = request.form.get('visitor_name')
    phone = request.form.get('phone')
    email = request.form.get('email', '')
    visit_date = request.form.get('visit_date')
    time_slot = request.form.get('time_slot', '3:00 PM - 4:00 PM')
    purpose = request.form.get('purpose', 'Snack Distribution')
    snack_items = request.form.get('snack_items', '')
    guest_count = request.form.get('guest_count', 1)
    notes = request.form.get('notes', '')

    if not visitor_name or not phone or not visit_date:
        flash("Please provide your Name, Phone Number, and Preferred Date.", "danger")
        return redirect(url_for('donate_snacks'))

    booking_ref, _ = database.add_visit(
        visitor_name=visitor_name,
        phone=phone,
        email=email,
        visit_date=visit_date,
        time_slot=time_slot,
        purpose=purpose,
        snack_items=snack_items,
        guest_count=guest_count,
        notes=notes
    )

    flash(f"Visit confirmed! Reference ID: {booking_ref}. We look forward to welcoming you at Lakad Ganj, Kamptee on {visit_date} at {time_slot}.", "success")
    return redirect(url_for('donate_snacks'))

@app.route('/api/volunteer', methods=['POST'])
def api_submit_volunteer():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email', '')
    skills = request.form.get('skills', '')
    availability = request.form.get('availability', '')
    occupation = request.form.get('occupation', '')
    message = request.form.get('message', '')

    if not name or not phone:
        flash("Please provide your name and phone number.", "danger")
        return redirect(url_for('volunteer'))

    database.add_volunteer(name, phone, email, skills, availability, occupation, message)
    flash(f"Thank you, {name}! Your volunteer application has been received. Our team will contact you shortly.", "success")
    return redirect(url_for('volunteer'))

@app.route('/api/contact', methods=['POST'])
def api_submit_contact():
    name = request.form.get('name')
    email = request.form.get('email', '')
    phone = request.form.get('phone', '')
    subject = request.form.get('subject', 'General Inquiry')
    message = request.form.get('message', '')

    if not name or not message:
        flash("Please provide your name and message.", "danger")
        return redirect(url_for('contact'))

    database.add_inquiry(name, email, phone, subject, message)
    flash(f"Thank you, {name}! Your inquiry has been sent to our Lakad Ganj office.", "success")
    return redirect(url_for('contact'))

@app.route('/api/admin/visit/status', methods=['POST'])
def api_admin_visit_status():
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 403
    visit_id = request.form.get('visit_id')
    status = request.form.get('status')
    
    conn = database.get_db()
    conn.execute('UPDATE visits SET status = ? WHERE id = ?', (status, visit_id))
    conn.commit()
    conn.close()
    
    flash("Visit status updated successfully.", "success")
    return redirect(url_for('admin'))

@app.route('/api/admin/inventory/update', methods=['POST'])
def api_admin_inventory_update():
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 403
    item_id = request.form.get('item_id')
    fulfilled_qty = request.form.get('fulfilled_qty')
    
    conn = database.get_db()
    conn.execute('UPDATE inventory_needs SET fulfilled_qty = ? WHERE id = ?', (fulfilled_qty, item_id))
    conn.commit()
    conn.close()
    
    flash("Inventory fulfillment updated.", "success")
    return redirect(url_for('admin'))

if __name__ == '__main__':
    # Run the Flask app
    print("=" * 60)
    print(" Sir Kasturchand Daga Bal Sadan - Kamptee Web Application")
    print(f" Address: {ai_engine.BAL_SADAN_INFO['location']}")
    print(f" Phone: {ai_engine.BAL_SADAN_INFO['phone']}")
    print(" Starting server on http://127.0.0.1:5000 ...")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
