<!-- # 🌿 GreenNest — Online Grocery Store

> A Yashdeep™ Brand | Built with Flask + SQLite + HTML/CSS

GreenNest is a full-stack grocery store web application built from
scratch using Python Flask. It includes a beautiful frontend,
user authentication, complaint management, customer reviews,
and a powerful admin dashboard.

---

## 🚀 Features

- 🏠 Homepage with hero banner, categories & featured products
- 🔐 User Registration & Login with hashed passwords
- 📦 Complaint submission with status tracking
- ⭐ Customer reviews with star ratings
- 🛡️ Admin dashboard to manage complaints, reviews & users
- 🗃️ SQLite database for permanent data storage
- 🌐 Deploy-ready with Gunicorn & Render.com

---

## 🛠️ Tech Stack

| Layer     | Technology              |
|-----------|-------------------------|
| Frontend  | HTML, CSS, JavaScript   |
| Backend   | Python, Flask           |
| Database  | SQLite, Flask-SQLAlchemy|
| Auth      | Flask-Login, Werkzeug   |
| Deploy    | Gunicorn, Render.com    |

---

## 📁 Project Structure
greennest/
├── static/
│   └── style.css
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── support.html
│   ├── login.html
│   ├── register.html
│   └── admin.html
├── app.py
├── models.py
├── requirements.txt
└── Procfile

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/greennest.git
cd greennest
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

### 5. Open in browser
http://127.0.0.1:5000

---

## 👤 Default Admin Login

| Field    | Value                  |
|----------|------------------------|
| Email    | admin@greennest.com    |
| Password | admin123               |

> ⚠️ Change the password after first login in production.

---

## 📸 Pages

| Page             | URL              |
|------------------|------------------|
| Homepage         | `/`              |
| Support & Reviews| `/support`       |
| Login            | `/login`         |
| Register         | `/register`      |
| Admin Dashboard  | `/admin`         |

---

## 🌐 Deployment (Render.com)

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn app:app`
6. Click **Deploy** 🚀

---

## 👨‍💻 Developer

**Yashdeep** — Built with passion using Python & Flask.

---

## 📄 License

This project is open source and free to use for learning purposes. -->