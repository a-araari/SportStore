# Django Profile Project

A Django web application for user profiles with authentication, profile management, and products listing.

## Prerequisites

Before you begin, make sure you have the following installed:
- Python 3.8 or higher
- Git
- pip (Python package installer)

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/a-araari/SportStore.git .
```

### 2. Create Virtual Environment

Create and activate a virtual environment to isolate project dependencies:

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt indicating the virtual environment is active.

### 3. Install Dependencies

Install all required packages from requirements.txt:

```bash
pip install -r requirements.txt
```

### 4. Database Setup

Run migrations to set up the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)

Create an admin user to access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to enter username, email, and password.

### 6. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`



This project is licensed under the MIT License - see the LICENSE file for details.
