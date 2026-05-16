from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Complaint, Review
import random

app = Flask(__name__)
app.config['SECRET_KEY']                  = 'yashdeep-greennest-secret-2026'
app.config['SQLALCHEMY_DATABASE_URI']     = 'sqlite:///greennest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

# ────────────────────────────────────────────────
#  PAGES
# ────────────────────────────────────────────────
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/success')
def success():
    order_id = 'GN-' + str(random.randint(10000, 99999))
    return render_template('success.html', order_id=order_id)

@app.route('/support')
def support():
    reviews = Review.query.order_by(Review.created.desc()).all()
    return render_template('support.html', reviews=reviews)

@app.route('/about')
def about():
    return render_template('about.html')

# ────────────────────────────────────────────────
#  AUTH
# ────────────────────────────────────────────────
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
        user   = User(name=name, email=email, password=hashed)
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
        user     = User.query.filter_by(email=email).first()
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

# ────────────────────────────────────────────────
#  COMPLAINT
# ────────────────────────────────────────────────
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

# ────────────────────────────────────────────────
#  REVIEW
# ────────────────────────────────────────────────
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

# ────────────────────────────────────────────────
#  RAZORPAY — verify payment after success
#  This route receives the payment_id from frontend
#  and logs it. In production you should also verify
#  the signature using razorpay Python SDK.
# ────────────────────────────────────────────────
@app.route('/verify-payment', methods=['POST'])
def verify_payment():
    data       = request.get_json()
    payment_id = data.get('payment_id', '')
    amount     = data.get('amount', 0)

    # Log it (in production save to an Order table in DB)
    print(f"[RAZORPAY] Payment received: {payment_id} | Amount: ₹{amount}")

    # TODO (production): use razorpay SDK to verify signature
    # pip install razorpay
    # import razorpay
    # client = razorpay.Client(auth=("YOUR_KEY_ID", "YOUR_KEY_SECRET"))
    # client.utility.verify_payment_signature({
    #     'razorpay_order_id':   data['order_id'],
    #     'razorpay_payment_id': data['payment_id'],
    #     'razorpay_signature':  data['signature']
    # })

    return jsonify({'status': 'success', 'payment_id': payment_id})

# ────────────────────────────────────────────────
#  ADMIN
# ────────────────────────────────────────────────
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
    complaint        = Complaint.query.get_or_404(complaint_id)
    complaint.status = request.form.get('status', 'Pending')
    db.session.commit()
    return redirect(url_for('admin'))

# ────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)