<div align="center">

# 📘 Quiz Master
### A Full-Stack Quiz Management System

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-Backend-black?style=flat-square&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue?style=flat-square&logo=sqlite)
![Bootstrap](https://img.shields.io/badge/Bootstrap-Frontend-purple?style=flat-square&logo=bootstrap)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

*A robust quiz platform where admins manage content and users compete, track, and grow.*

</div>

---

## ✨ Features

### 👤 User
- Registration & login with **session-based authentication**
- Attempt quizzes **question-by-question** with real-time score tracking
- View **results**, **attempt history**, and **performance insights**
- Dashboard with **per-subject analytics** via matplotlib charts

### 🛠️ Admin
- Full **CRUD** for Subjects, Chapters, Quizzes, and Questions
- **Fuzzy search** across users, subjects, and quizzes
- System-wide analytics: users, quizzes, questions, attempts
- **Matplotlib-powered** visualization dashboard

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Flask (Python) |
| ORM | Flask-SQLAlchemy |
| Frontend | HTML + Jinja2 |
| Styling | Bootstrap |
| Database | SQLite |
| Charts | Matplotlib |
| Version Control | Git + GitHub |

---

## 📁 Project Structure

```
quiz-master/
│
├── application/
│   ├── controllers.py       # Routes & business logic
│   ├── models.py            # SQLAlchemy DB models
│   ├── database.py          # DB initialization
│   ├── templates/           # Jinja2 HTML templates
│   └── static/              # CSS & generated charts
│
├── app.py                   # Application entry point
├── requirements.txt
└── .gitignore
```

---

## ⚙️ Setup & Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/quiz-master.git
cd quiz-master

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py
```

App runs at: **http://localhost:5000**

---

## 📊 Database Design

**Entities:** `User` · `Subject` · `Chapter` · `Quiz` · `Question` · `Score`

**Relationships:**
```
Subject ──< Chapter ──< Quiz ──< Question
User ──< Score
```
- Subject → Chapters (One-to-Many)
- Chapter → Quizzes (One-to-Many)
- Quiz → Questions (One-to-Many)
- User → Scores (One-to-Many)

---

## 🧠 Core Concepts Implemented

- **MVC Architecture** — clean separation of Model, View, Controller
- **ORM** — SQLAlchemy relationships, cascade deletes, normalization
- **Session-based Auth** — login state, role separation (admin/user)
- **Fuzzy Search** — case-insensitive partial matching via `ilike`
- **Data Visualization** — server-side charts using matplotlib (no JS needed)
- **Jinja2 Templating** — template inheritance, dynamic rendering

---

## 🔐 Security

- Session integrity via Flask `secret_key`
- Role-based access control (admin vs. user routes)
- Input validation on all forms
- Session lifecycle managed via `session.get()` and `session.pop()`

---

## 🔍 Search Implementation

```python
Model.field.ilike(f"%{query}%")
```
- Case-insensitive, partial (fuzzy) matching
- Covers subjects, users, and quizzes

---

## 🚀 Roadmap

| Priority | Improvement |
|---|---|
| 🔥 Next | REST API endpoints (`/api/users`, `/api/quizzes`, `/api/scores`) |
| ⚡ Soon | JWT-based authentication (replace sessions) |
| 🎨 Design | React/Vue frontend consuming the API |
| ⚙️ Performance | Pagination, query optimization, Redis caching |
| 📱 Future | Mobile app integration, real-time leaderboard, timed quizzes |
| 🤖 Vision | AI-based question generation, multi-user competitive mode |

---

## ⚠️ Challenges & Learnings

**Struggled with:**
- Session handling bugs during quiz flow (`session.get()` vs direct access)
- SQLAlchemy cascade delete mapping
- Template repetition before discovering Jinja inheritance
- Arch Linux pip environment restrictions

**Learned deeply:**
- Flask internals: routing, request lifecycle, context
- SQLAlchemy ORM relationships and query optimization
- Difference between GET and POST in real scenarios
- Writing structured, scalable, and debuggable backend code

---

## 👨‍💻 Author

**Mayukh Mandal**  
*Flask + DSA + System Design Journey 🚀*

---

<div align="center">

⭐ *Started as a course requirement. Evolved into a backend development foundation.*  
If this helped you, consider giving it a star!

</div>
