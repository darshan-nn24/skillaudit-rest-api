# SkillAudit REST API — Task Management System

A simple RESTful API developed using **FastAPI, Python, SQLAlchemy, and SQLite** for managing tasks through CRUD (Create, Read, Update, Delete) operations.

This project was developed as part of the SkillAudit internship task to demonstrate REST API development, database integration, request validation, error handling, and interactive API documentation.

## Features

- Create tasks with title, description, status, and priority.
- Retrieve all tasks.
- Retrieve an individual task by ID.
- Update existing tasks.
- Delete tasks.
- Persist task data using SQLite and SQLAlchemy.
- Validate request data using Pydantic.
- Handle missing tasks with appropriate HTTP errors.
- Explore and test endpoints through Swagger UI.

## Tech Stack

- **Language:** Python
- **API Framework:** FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **ASGI Server:** Uvicorn
- **API Documentation:** Swagger UI / OpenAPI

## Project Structure

```text
skillaudit_rest_api/
├── app/
│   └── main.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

The SQLite database is created or stored locally by the application.

## Getting Started

### Prerequisites

- Python 3.10 or a compatible version supported by the installed dependencies
- pip
- Git (for cloning the repository)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/skillaudit-rest-api.git
cd skillaudit-rest-api
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell activation is blocked, use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the API

```bash
python -m uvicorn app.main:app --reload
```

The API should be available at:

- **Base URL:** http://127.0.0.1:8000
- **Interactive API documentation:** http://127.0.0.1:8000/docs
- **OpenAPI schema:** http://127.0.0.1:8000/openapi.json

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API availability |
| POST | `/tasks` | Create a task |
| GET | `/tasks` | Retrieve all tasks |
| GET | `/tasks/{task_id}` | Retrieve a task by ID |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

## Example Request

Create a task using `POST /tasks`:

```json
{
  "title": "Complete SkillAudit API",
  "description": "Test and document the REST API",
  "status": "pending",
  "priority": "high"
}
```

The API returns the created task with its generated ID when the request succeeds. The allowed status and priority values depend on the validation rules defined in the application.

## Testing

1. Start the API server.
2. Open http://127.0.0.1:8000/docs.
3. Expand each endpoint.
4. Select **Try it out** and execute requests.
5. Verify response codes and response bodies.
6. Test missing task IDs to verify 404 error handling.

## Learning Outcomes

- RESTful API design and HTTP methods
- CRUD operations
- Relational database integration
- Request validation and exception handling
- API testing and interactive documentation
- Python project organization and version control

## Author

**Darshan Nagaraj Naik**

GitHub: https://github.com/darshan-nn24

LinkedIn: https://www.linkedin.com/in/darshan-nagaraj-naik-7b004a299/

---

*Developed as an internship project for learning and demonstrating backend API development.*
