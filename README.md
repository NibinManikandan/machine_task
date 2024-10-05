# Project Name

The objective of this machine test is to develop a RESTful API that
manages job listings, applications, and user roles ( Candidates,
Employers, Admins ) with role-based access control. Features such as
filtering, searching, authentication, and file uploads must be
implemented. This test assesses your ability to use Django REST
Framework to build scalable APIs and implement business logic while
adhering to industry best practices.

## Table of Contents

- [Project Setup](#project-setup)
- [Authentication Details](#authentication-details)
- [API Documentation](#api-documentation)
- [License](#license)

## Project Setup

### Prerequisites

- Python 3.x installed (or the specific language you’re using).
- [PostgreSQL](https://www.postgresql.org/) or the specific database for your project.
- Django or other dependencies (if any).
- `pip` for managing Python packages.

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/username/repository-name.git
    cd repository-name
    ```

2. **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:
    - On **Windows**:
      ```bash
      venv\Scripts\activate
      ```
    - On **macOS/Linux**:
      ```bash
      source venv/bin/activate
      ```

4. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Set up the database**:
   If using Django with PostgreSQL or SQLite:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Run the server**:
    ```bash
    python manage.py runserver
    ```

### Environment Variables

Ensure you have a `.env` file or set the necessary environment variables. Example:

```bash
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:password@localhost/dbname

# As a better approach we can create a .env file and move all the private datas using in the aplication and access it from the file through settings.py file.

