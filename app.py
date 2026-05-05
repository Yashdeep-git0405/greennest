from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Complaint, Review

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yashdeep-greennest-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///greennest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create all DB tables on first run
with app.app_context():
    db.create_all()

# ─── PAGES ───────────────────────────────────────────────

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/support')
def support():
    reviews = Review.query.order_by(Review.created.desc()).all()
    return render_template('support.html', reviews=reviews)

# ─── AUTH ────────────────────────────────────────────────

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name     = request.form['name']
        email    = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Email already registered.')
            return redirect(url_for('register'))
        hashed = generate_password_hash(password)
        user = User(name=name, email=email, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid email or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# ─── COMPLAINT ───────────────────────────────────────────

@app.route('/submit-complaint', methods=['POST'])
def submit_complaint():
    data = request.get_json()
    complaint = Complaint(
        name        = data.get('name'),
        order_id    = data.get('order'),
        email       = data.get('email'),
        issue_type  = data.get('type'),
        description = data.get('desc')
    )
    db.session.add(complaint)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Complaint saved!'})

# ─── REVIEW ──────────────────────────────────────────────

@app.route('/submit-review', methods=['POST'])
def submit_review():
    data = request.get_json()
    review = Review(
        name     = data.get('name'),
        stars    = int(data.get('stars', 5)),
        category = data.get('category'),
        text     = data.get('text')
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Review saved!'})

# ─── ADMIN ───────────────────────────────────────────────

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Admin access only.')
        return redirect(url_for('home'))
    complaints = Complaint.query.order_by(Complaint.created.desc()).all()
    reviews    = Review.query.order_by(Review.created.desc()).all()
    users      = User.query.order_by(User.created.desc()).all()
    return render_template('admin.html',
                           complaints=complaints,
                           reviews=reviews,
                           users=users)

@app.route('/admin/update-status/<int:complaint_id>', methods=['POST'])
@login_required
def update_status(complaint_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    complaint = Complaint.query.get_or_404(complaint_id)
    complaint.status = request.form.get('status', 'Pending')
    db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)