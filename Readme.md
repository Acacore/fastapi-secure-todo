# Secure FastAPI To-Do API

A production-ready Task Management API built with **FastAPI**, **SQLModel**, and **FastAPI Users**. This system features stateless **JWT Authentication** and strict **Owner-Based Access Control (OBAC)** to ensure data privacy and security.



## Key Features
* **JWT Authentication:** Secure, stateless sessions using JSON Web Tokens.
* **Multi-User Support:** Users can only manage their own tasks.
* **Full CRUD:** Create, Read, Update (Partial/PATCH), and Delete functionality.
* **Auto-Timestamps:** Tracks `created_at`, `updated_at`, and `completed_at` automatically.
* **Robust Validation:** 4-tier Pydantic schema system (Base, Create, Update, Read) to prevent bad data.

---

## Getting Started

### 1. Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd ToDoList

# Create and activate virtual environment
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```

---
### 2. Database Setup
```bash
#Initialize the SQLite database and run migrations
alembic upgrade head
```


### 3. Running the Application
```bash
# Running the app in the terminal
fastapi dev main.py

# The API will be live at http://127.0.0.1:8000. Explore the interactive documentation at /docs.

```

##### API Reference
###### Authentication (Public)

Method,Endpoint,Description / Payload
POST,/auth/register,"Create a new user account (email, password, names)"
POST,/auth/jwt/login,Exchange credentials for a JWT Access Token

##### To-Do Management (Requires Authorization: Bearer <token>)

###### Method,Endpoint,Description
GET,/todos/,List all tasks belonging to the authenticated user
POST,/todos/,Create a new task
GET,/todos/{id},Get details for a specific task by UUID
PATCH,/todos/{id},"Partially update a task (e.g., mark as completed)"
DELETE,/todos/{id},Permanently remove a task

---

Gemini said
Here is your complete, professional README.md content. You can copy this directly into a file named README.md in your project root.

Markdown
# 🚀 Secure FastAPI To-Do API

A production-ready Task Management API built with **FastAPI**, **SQLModel**, and **FastAPI Users**. This system features stateless **JWT Authentication** and strict **Owner-Based Access Control (OBAC)** to ensure data privacy and security.



## ✨ Key Features
* **JWT Authentication:** Secure, stateless sessions using JSON Web Tokens.
* **Multi-User Support:** Users can only manage their own tasks.
* **Full CRUD:** Create, Read, Update (Partial/PATCH), and Delete functionality.
* **Auto-Timestamps:** Tracks `created_at`, `updated_at`, and `completed_at` automatically.
* **Robust Validation:** 4-tier Pydantic schema system (Base, Create, Update, Read) to prevent bad data.

---

## 🚦 Getting Started

### 1. Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd ToDoList

# Create and activate virtual environment
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
```

# Install dependencies
```bash pip install fastapi[all] sqlmodel fastapi-users[sqlalchemy] alembic```

2. Database Setup
``` bash
# Initialize the SQLite database and run migrations
alembic upgrade head
```
3. Running the Application
```bash
fastapi dev main.py
# The API will be live at http://127.0.0.1:8000. Explore the interactive documentation at /docs.
```

#### API Reference
Authentication (Public)
Method	Endpoint	Payload
POST	/auth/register	Create an account (email, password, names)
POST	/auth/jwt/login	Login to receive a JWT Access Token
To-Do Management (Requires Authorization: Bearer <token>)
Method	Endpoint	Description
GET	/todos/	List all tasks for the logged-in user
POST	/todos/	Create a new task
GET	/todos/{id}	Get a specific task by UUID
PATCH	/todos/{id}	Partially update a task (e.g., mark as completed)
DELETE	/todos/{id}	Remove a task permanently

🔑 Usage Guide (Example Flow)

1. Register & Login
First, register a user via /auth/register. Then, log in to get your token:

Request:
POST http://127.0.0.1:8000/auth/jwt/login

Body (Form-Data): username=john.doe@example.com&password=securepassword123

2. Perform CRUD
Use the access_token from the login response in the header for all subsequent calls:

Header: Authorization: Bearer <your_token>

Create a Task Example:


Create a Task Example:JSON// POST /todos/
{
  "title": "Buy groceries",
  "description": "Milk, Eggs, and Bread"
}
Partial Update Example (Marking Done):JSON// PATCH /todos/<userId>
{
  "completed": true
}

##### TroubleshootingError

Error Code,Meaning,Common Fix
401 Unauthorized,Token missing or expired,Re-authenticate via /auth/jwt/login.
403 Forbidden,Ownership mismatch,You are trying to access a task belonging to another user.
422 Unprocessable,Validation Error,Your JSON body is missing a required field or has the wrong type.
404 Not Found,Missing Resource,The UUID provided does not exist in the database.

### Project Structure

main.py: Entry point and route definitions.

models.py: SQLModel database definitions and relationships.

schemas.py: Pydantic CRUD validation models.

users.py: FastAPI Users authentication configuration.

database.py: Session, engine, and database lifecycle setup.

api.http: Full testing suite for VS Code REST Client.




License
MIT

**Would you like me to help you set up the `.gitignore` file now to make sure you don't accidentally commit your `todo.db` or `env` folder?**