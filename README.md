# Task Manager

A Django-based to-do application with a REST API for managing tasks. Built as a university assignment, this project supports task creation, updating, deletion, and listing, with unit tests and Dockerized deployment.

## Features
- Create, read, update, and delete tasks via a REST API.
- User-friendly interface (optional, if implemented).
- Local SQLite database for simplicity.
- Unit tests with pytest.
- Docker support for consistent development and deployment.

## Prerequisites
- Python 3.10+
- Docker and Docker Compose (for containerized setup)
- Git

## Setup Instructions

### Running Locally
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/bobbysharma05/task_manager.git
   cd task_manager
2. **Set up the virtual enviornment**
   ```bash
   python -m venv venv
   source venv/bin/activate
3. Install Dependencies
   ```bash
   pip install -r requirements.txt
4. Appy Migration
   ```bash
   python manage.py migrate
5. Run the server
   ```bash
   python manage.py runserver

### Running with Docker
1. Start the container
   ```bash
   docker compose up
2. Stop the container
   ```bash
   docker compose down
Note: On Fedora, ensure SELinux allows file access:
1. ```bash
   chcon -R -t container_file_t .
### API Usage
1. List tasks: GET /api/tasks/
2. Create Tasks:POST /api/tasks/
   ```bash
   {
    "title": "New Task",
    "description": "Task details",
    "status": "pending"
   }
4. Update Tasks:PUT /api/tasks/<id>/
5. Delete Tasks: DELETE /api/tasks/<id>/

### Testing
Run unit test with pytest

1. ```bash
   pytest

### Troubleshooting
If you encounter a Permission denied error when running docker compose up (e.g., python: can't open file '/app/manage.py': [Errno 13] Permission denied), try these steps:
1. Ensure manage.py is executable
   ```bash
   ls -l manage.py
   chmod +x manage.py
2. Set the correct SELinux for Docker
   ```bash
   chcon -R -t container_file_t .
3. Test Without Volume Mount: Edit docker-compose.yml to comment out the volume mount and then run
   ```bash
   docker compose down
   docker compose build
   docker compose up
4. Update Dockerfile to use a non-root user matching your host’s UID/GID (e.g., 1000:1000):
   ```bash
   ARG UID=1000
   ARG GID=1000
   RUN groupadd -g ${GID} appuser && useradd -u ${UID} -g ${GID} -m appuser
   USER appuser
5. Rebuild and Run the docker

### Project Structure
1. manage.py: Django management script.
2. task_manager/: Core app with settings, URLs, and models.
3. api/: REST API logic (serializers, views).
4. Dockerfile: Docker image configuration.
5. docker-compose.yml: Docker Compose setup.
6. requirements.txt: Python dependencies.
7. pytest.ini: Testing configuration.

### Notes
1. The app uses SQLite for simplicity; for production, consider PostgreSQL.
2. Environment variables (if any) should be in a .env file (ignored by .gitignore).
3. Live code reloading is enabled in Docker via volume mounts.

### Author
Bobby Sharma

Second-year BTech Computer Science student

