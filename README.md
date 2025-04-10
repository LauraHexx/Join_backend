# Task Management API

This is an API for managing tasks, categories, contacts, and subtasks. It allows creating, updating, retrieving, and deleting tasks and their related subtasks and contacts.

## Features

- **Tasks**: Create, update, and delete tasks.
- **Categories**: Categorize tasks.
- **Contacts**: Assign contacts to tasks.
- **Subtasks**: Create and manage subtasks for each task.
- **User Management**: Each task is associated with a user.

## Requirements

Ensure the following prerequisites are installed on your system:

- Python 3.8 or higher
- Django 3.x or higher
- Django REST Framework
- A database like SQLite (default in Django) or another relational database (e.g., PostgreSQL)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/task-management-api.git
    cd task-management-api
    ```

2. Create a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run migrations to set up the database:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser to access the admin interface:

    ```bash
    python manage.py createsuperuser
    ```

6. Start the development server:

    ```bash
    python manage.py runserver
    ```

## Authentication

This API requires user authentication. You can use the Django admin interface to create a user and obtain authentication tokens or implement token-based authentication through the Django REST Framework.


