import re
from functools import wraps
from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db

bp = Blueprint('main', __name__)
EMAIL_RE = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
ALLOWED_STATUS = {'New', 'In Progress', 'Responded', 'Closed'}

@bp.get('/')
def home():
    return render_template('index.html')

@bp.get('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'velcoris-enquiry-api'})

@bp.post('/api/enquiries')
def create_enquiry():
    data = request.get_json(silent=True) if request.is_json else request.form
    data = data or {}
    # Honeypot field: bots often fill hidden fields; silently accept without storing.
    if (data.get('website') or '').strip():
        return jsonify({'message': 'Thank you. Your enquiry has been received.'}), 201
    fields = {key: (data.get(key) or '').strip() for key in ['name','email','organisation','enquiry_type','subject','message']}
    errors = {}
    if not 2 <= len(fields['name']) <= 100: errors['name'] = 'Enter a name between 2 and 100 characters.'
    if not EMAIL_RE.match(fields['email']) or len(fields['email']) > 254: errors['email'] = 'Enter a valid email address.'
    if len(fields['organisation']) > 120: errors['organisation'] = 'Organisation must be 120 characters or fewer.'
    if fields['enquiry_type'] not in {'Sample request','Technical consultation','Partnership','General enquiry'}: errors['enquiry_type'] = 'Choose a valid enquiry type.'
    if not 3 <= len(fields['subject']) <= 140: errors['subject'] = 'Subject must be 3–140 characters.'
    if not 10 <= len(fields['message']) <= 3000: errors['message'] = 'Message must be 10–3000 characters.'
    if errors:
        return jsonify({'message':'Please correct the highlighted fields.','errors':errors}), 400
    db = get_db()
    db.execute('INSERT INTO enquiries (name,email,organisation,enquiry_type,subject,message) VALUES (?,?,?,?,?,?)',
               tuple(fields[k] for k in ['name','email','organisation','enquiry_type','subject','message']))
    db.commit()
    return jsonify({'message':'Thank you. Your enquiry has been received. Our team will review it shortly.'}), 201

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('main.admin_login', next=request.path))
        return fn(*args, **kwargs)
    return wrapper

@bp.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username','')
        password = request.form.get('password','')
        configured = current_app.config['ADMIN_PASSWORD']
        # Compare against configured local/demo secret. Production should use managed identities/secrets.
        if username == current_app.config['ADMIN_USERNAME'] and password == configured:
            session.clear()
            session['admin_logged_in'] = True
            session.permanent = True
            return redirect(url_for('main.admin_dashboard'))
        flash('Invalid username or password.', 'error')
    return render_template('login.html')

@bp.post('/admin/logout')
@login_required
def admin_logout():
    session.clear()
    return redirect(url_for('main.admin_login'))

@bp.get('/admin')
@login_required
def admin_dashboard():
    db = get_db()
    enquiries = db.execute('SELECT * FROM enquiries ORDER BY datetime(created_at) DESC').fetchall()
    counts = {s: db.execute('SELECT COUNT(*) FROM enquiries WHERE status=?',(s,)).fetchone()[0] for s in ALLOWED_STATUS}
    return render_template('admin.html', enquiries=enquiries, counts=counts)

@bp.post('/admin/enquiries/<int:enquiry_id>/status')
@login_required
def update_status(enquiry_id):
    status = request.form.get('status','')
    if status not in ALLOWED_STATUS:
        flash('Invalid status selected.', 'error')
    else:
        db = get_db()
        cur = db.execute('UPDATE enquiries SET status=? WHERE id=?',(status,enquiry_id))
        db.commit()
        flash('Enquiry status updated.' if cur.rowcount else 'Enquiry not found.', 'success' if cur.rowcount else 'error')
    return redirect(url_for('main.admin_dashboard'))
