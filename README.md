# Hux Ventures Fullstack Developer Assessment 2024 - BACKEND

This template provides a minimal setup to run the application.

The app was built with Django and Django Rest Framework and PostgreSQL

# Assumptions:

1. You have downloaded and installed PostgresQL, as you will be connecting to it via the 'settings.py' file
   If not, head on to https://www.postgresql.org/download/ and download and install.

2. You have installed Python (version 3.10 and above). You can confirm by running 'py --version'.

3. You have pip version 24.0 and above. You can confirm by running 'pip --version'.

# To run the app:

1. Clone the repository

2. Create and activate a Virtual Environments.

3. Install app dependencies by running 'pip install -r requirements.txt'

4. Go to the 'huxassessment/settings.py' file and edit the 'DATABASES' connection details. Provide your own Database's 'NAME', 'USER' and 'PASSWORD'

5. Make migrations to the database by running 'python manage.py makemigrations'

6. Migrate to the database by running 'python manage.py migrate'

7. Run the server with 'python manage.py runserver localhost:8000'
