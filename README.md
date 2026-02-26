# Secure FastAPI To-Do API

A secure, multi-user To-Do API built with FastAPI and SQLModel. Features JWT authentication, automatic timestamps, and owner-based access control to ensure users can only manage their own data.

**production-ready** Task Management REST API built with:

- **FastAPI**  
- **SQLModel** (SQLAlchemy + Pydantic)  
- **FastAPI Users** (authentication)

Features **stateless JWT authentication** and strict **Owner-Based Access Control (OBAC)** — users can only see and modify **their own** tasks.

## ✨ Key Features

- Secure JWT-based authentication (stateless)
- Multi-user support with data isolation
- Full CRUD operations on tasks
- Partial updates (PATCH) supported
- Automatic timestamps: `created_at`, `updated_at`, `completed_at`
- 4-tier Pydantic validation schemas (Base, Create, Update, Read)
- Alembic migrations for database versioning
- SQLite support out of the box (easy to switch to PostgreSQL)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repository-url>
cd ToDoList

# Create and activate virtual environment
python -m venv env
source env/bin/activate          # Linux/macOS
# or
.\env\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
Create a .env file in the project root:
``` Bash 
# .env
SECRET_KEY=your-very-secure-random-string-here
```
###### Generate a strong secret key:
``` Bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
⚠️ Important
Never commit .env or the database file (todo.db) to version control.

### 3. Database Setup
``` Bash
# Apply migrations (creates tables)
alembic upgrade head
```

### 4. Run the Application
``` Bash
# Development server with auto-reload
fastapi dev main.py
# or
uvicorn main:app --reload


API will be available at:
→ http://127.0.0.1:8000
→ Interactive docs: http://127.0.0.1:8000/docs

```
## 🔐 API Reference

### Authentication (Public endpoints)

| Method | Endpoint             | Description                              |
|--------|----------------------|------------------------------------------|
| POST   | `/auth/register`     | Create new user (email + password + name) |
| POST   | `/auth/jwt/login`    | Login → receive JWT access token         |

### Task Management  
*(requires `Authorization: Bearer <token>` header)*

| Method | Endpoint          | Description                              |
|--------|-------------------|------------------------------------------|
| GET    | `/todos/`         | List all your tasks                      |
| POST   | `/todos/`         | Create a new task                        |
| GET    | `/todos/{id}`     | Get single task (by UUID)                |
| PATCH  | `/todos/{id}`     | Partially update task (e.g. mark done)   |
| DELETE | `/todos/{id}`     | Delete a task                            |
## 📋 Example Usage Flow

##### Register a User

```http
POST /auth/register HTTP/1.1
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "strongpassword123",
  "name": "John Doe"
}
```

##### Login to Get Access Token

Use **form data (OAuth2 password flow)**:

```http
POST /auth/jwt/login HTTP/1.1
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=strongpassword123
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

##### Create a Task (Authenticated)

```http
POST /todos/ HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

##### Mark Task as Completed (Partial Update)


```http
PATCH /todos/<task-uuid> HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "completed": true
}
```
#### Project Structure

ToDoList/
├── alembic.ini
├── api.http
├── database.py
├── init_db.py
├── main.py
├── migrations
│   ├── env.py
│   ├── __pycache__
│   │   └── env.cpython-313.pyc
│   ├── README
│   ├── script.py.mako
│   └── versions
│       ├── 4ab7aa792551_initial_migrations.py
│       ├── cd9f02ee314b_initial_migrations.py
│       └── __pycache__
│           ├── 4ab7aa792551_initial_migrations.cpython-313.pyc
│           └── cd9f02ee314b_initial_migrations.cpython-313.pyc
├── models.py
├── __pycache__
│   ├── database.cpython-313.pyc
│   ├── main.cpython-313.pyc
│   ├── models.cpython-313.pyc
│   ├── schemas.cpython-313.pyc
│   └── users.cpython-313.pyc
├── Readme.md
├── requirements.txt
├── schemas.py
├── todo.db
└── users.py

Lience

MIT

**Would you like me to help you create a `.gitignore` file now to make sure you don't accidentally upload your database or environment files to GitHub?**