# 💸 Finance Tracker API

A Django-based finance tracking application that empowers users to manage their personal expenses and income securely. It provides an intuitive frontend experience with real-time filtering, summaries, and exports — along with a robust RESTful API secured by JWT authentication.

---

## 🚀 Why Use This App?

Whether you're budgeting for groceries or tracking your income, this app offers a clean UI and powerful backend to:

- Record transactions  
- Analyze monthly spending  
- Export data as reports  

---

## 🧩 Features

### 🔐 Authentication

- User registration and login required
- JWT-based API authentication

### 💰 Transactions

- Full **CRUD**: Create, update, delete, and view personal transactions
- Filter by **category** or **date**
- Search by **transaction description or amount**, **category name**

### 🗂️ Categories

- Only **admins** can add/update/delete categories
- Authenticated users can **list** or **retrieve** categories

### 📆 Monthly Summaries

- Automatically calculate monthly **income**, **expenses**, and **balance**
- View all summaries or retrieve a specific one by month

### 📤 CSV Export

- Export **all** or **filtered** transactions as downloadable CSV

### 🧠 Secure API

- All endpoints are protected via **JWT tokens**
- A ready-to-import **Postman collection** is included for testing

---

## ⚙️ Environment Setup

### 🧾 .env File

Create a `.env` file in the root directory:

```env
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost         # Use 'db' when running Docker
DB_PORT=5432

# For Docker PostgreSQL container
POSTGRES_DB=finance_tracker
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_db_password

Note: Each of the DB_PASSWORD and POSTGRES_PASSWORD have the same value 
```

---

## 📡 Celery & Redis Configuration

In `settings.py`:

```python
# For running locally
CELERY_BROKER_URL = 'redis://localhost:6379/0'

# For running with Docker
CELERY_BROKER_URL = 'redis://redis:6379/0'

# Timezone setup
TIME_ZONE = 'Africa/Cairo'
USE_TZ = True
CELERY_TIMEZONE = 'Africa/Cairo'
```

---

## 🖥️ Running Locally (Without Docker)

```bash
# Create and activate virtual environment
python -m venv env
source env/bin/activate        # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver

# In separate terminal: Start Redis
redis-server

# In another terminal: Start Celery worker
celery -A config worker -l info
# on Windows OS 
celery -A config worker -l info -P solo

# In another terminal: Start Celery beat
celery -A config beat -l info
```

---

## 🐳 Running with Docker

```bash
# Build and start containers
docker-compose up --build

# Create superuser inside Docker container
docker-compose exec web python manage.py createsuperuser
```

### 🔗 Access

- App: <http://localhost:8000/>
- Admin Panel: <http://localhost:8000/admin/>
- Flower Dashboard (Celery monitor): <http://localhost:5555/>

---

## ⏰ Monthly Summary Scheduler (via Celery Beat)

To automate generation of monthly summaries:

1. Log in to the **Django Admin Panel**
2. Go to `Periodic Tasks` (under **Periodic Tasks**)
3. Add a new task (e.g., `generate_monthly_summary`)
4. Set it to run on the 1st of every month at 00:00 (Cairo time)

Celery Beat will take care of scheduling; Celery workers will execute the task.

---

## 📬 Postman Collection

A ready-to-import **Postman Collection** is included to test:

- ✅ JWT Registration/Login
- 🔄 CRUD for Transactions
- 🔍 Filter and Search
- 📤 Export CSV
- 📂 Category & Summary Retrieval
