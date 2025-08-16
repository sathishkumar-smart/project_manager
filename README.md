# 🗂️ Project Manager Backend (Django + DRF)

A lightweight **project management system** (similar to Jira) built with **Django REST Framework**.  
Implements a **clean architecture** with `Repositories → Services → Views` for scalability and maintainability.  

---

## 🚀 Features
- 🔑 User authentication (Django built-in users)
- 📂 Project management (create, update, delete, list projects)
- ✅ Task management within projects
- 💬 Nested resources:
  - Task comments
  - Task attachments
  - Project members
- 📊 Interactive API documentation (Swagger & ReDoc via `drf-yasg`)
- 🏗️ Clean architecture (Repository + Service layers)
- ⚡ Caching (Redis/Django cache)
- ⏳ Background tasks with Celery (e.g., email notifications)

---

## 🏗️ Project Structure

```
project_manager/
│
├── projects/                   # Core project management app
│   ├── models.py                # Database models
│   ├── serializers.py           # DRF serializers
│   ├── views.py                 # ViewSets (API endpoints)
│   ├── urls.py                  # API routes using routers
│   │
│   ├── repositories/            # Data access layer
│   │   ├── project_repository.py
│   │   ├── member_repository.py
│   │   ├── task_repository.py
│   │   ├── comment_repository.py
│   │   └── attachment_repository.py
│   │
│   ├── services/                # Business logic layer
│   │   ├── project_service.py
│   │   ├── member_service.py
│   │   ├── task_service.py
│   │   ├── comment_service.py
│   │   └── attachment_service.py
│   │
│   └── migrations/
│
└── project_manager/             # Django project config
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

---

## 🔑 Architecture

### 1. **Models**
Database schema:  
- `Project`  
- `ProjectMember`  
- `Task`  
- `TaskComment`  
- `TaskAttachment`

### 2. **Repositories**
- Handle **database access only** (Django ORM queries).
- No business logic here.

### 3. **Services**
- Contain **business logic**.  
- Orchestrate repositories, apply rules, handle validations.

### 4. **Views**
- Expose API endpoints (`ViewSets`).  
- Keep them thin by delegating logic to **services**.

### 5. **URLs**
- Organized with **nested routers** (`drf-nested-routers`) for clean RESTful design:

```
/projects/                       → CRUD projects
/projects/{project_id}/members/  → Manage project members
/tasks/                          → CRUD tasks
/tasks/{task_id}/comments/       → Manage comments
/tasks/{task_id}/attachments/    → Manage attachments
```

---

## ⚡ API Documentation

Once the server is running:

- **Swagger UI** → [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)  
- **ReDoc** → [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)  
- **OpenAPI JSON** → [http://127.0.0.1:8000/swagger.json](http://127.0.0.1:8000/swagger.json)  

---

## 🛠️ Setup Instructions

### 1. Clone repository
```bash
git clone https://github.com/yourusername/project_manager.git
cd project_manager
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the project root:
```env
# Database
DATABASE_URL=postgres://user:password@localhost:5432/project_db

# Cache / Celery
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0

# Email
EMAIL_HOST=smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_HOST_USER=your_mailtrap_user
EMAIL_HOST_PASSWORD=your_mailtrap_pass
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL="Project Manager <noreply@project.com>"
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Start server
```bash
python manage.py runserver
```

### 7. Start Celery (for background tasks)
```bash
celery -A project_manager worker -l info
```

---

## 🧪 Testing

Unit tests are structured by layers:

- **Repository tests** → database queries  
- **Service tests** → business logic  
- **API tests** → endpoints using DRF test client  

Run tests:
```bash
pytest
```

---

## 📌 Notes & Best Practices
- Store sensitive info in `.env` (never commit it).  
- Use `.gitignore` to exclude `venv/`, `__pycache__/`, `.env`, migrations (optional).  
- Follow **clean architecture**: Keep Views thin, put logic in Services, DB calls in Repositories.  
- Logging + error handling included (`config.utils.logger`).  
- Example background jobs: task assignment email via Celery.  

---

## 📖 License
MIT License – free to use and modify.  
