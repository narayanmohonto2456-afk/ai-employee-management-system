Employee Management System (EMS)

A production-oriented Employee Management System built with Django and Django REST Framework. The project provides employee management, department management, attendance tracking, leave management, role-based authorization, JWT authentication, and attendance reporting.

Features

Authentication & Authorization

Custom Django User model

Email/password authentication

Email verification support

JWT authentication using Simple JWT

Access and refresh tokens

Role-based access control:

ADMIN

HR

EMPLOYEE

Django Groups and model permissions

Login-required protection for web views

API authentication and permission checks

Employee Management

Employee profiles linked one-to-one with users

Employee ID

Department and designation

Gender and date of birth

Joining date

Address information

Profile picture

Employee search, filtering, ordering, and pagination

Admin/HR protected employee management

Department Management

Department name and code

Department description

Department CRUD operations

Search, filtering, and ordering

Admin-only modification through API permissions

Attendance Management

Daily attendance records

Check-in and check-out

Automatic working-hours calculation

Attendance statuses:

Present

Absent

Leave

Half Day

Employee-specific attendance visibility

Attendance search and filtering

AJAX check-in/check-out support

Leave Management

Leave types

Employee leave applications

Start/end dates and reason

Leave statuses:

Pending

Approved

Rejected

Admin/HR approval and rejection

Employee-specific leave visibility

Dashboard

Total employee count

Department count

Attendance statistics

Leave request statistics

Today's attendance summary

Recent employees

Recent leave requests

Attendance overview chart

Reports

Attendance report page

Employee, department, status, and date filtering

Excel attendance export

PDF attendance export

REST API

JWT token obtain/refresh endpoints

User profile endpoint

Employee list/create endpoint

Employee detail/update/delete endpoint

Department list/create endpoint

Department detail/update/delete endpoint

Logged-in employee profile endpoint

Django REST Framework permissions and filtering

Technology Stack

Python 3.14.3

Django 6.0.7

Django REST Framework

PostgreSQL

Simple JWT

django-filter

Bootstrap 5

HTML5 / CSS3

JavaScript / jQuery / AJAX

Chart.js

Postman

Git / GitHub

openpyxl

ReportLab

Pillow

Project Applications

accounts/
api/
attendance/
dashboard/
departments/
employees/
leave_management/
reports/

Project Structure

employee_management_system/
│
├── accounts/
├── api/
├── attendance/
├── dashboard/
├── departments/
├── employees/
├── leave_management/
├── reports/
├── config/
├── templates/
├── static/
├── media/
├── manage.py
├── requirements.txt
└── README.md

Installation

1. Clone the repository

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd employee_management_system

2. Create a virtual environment

Windows:

python -m venv venv
venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Configure environment variables

Create a .env file for local development and configure values such as:

SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=employee_management_system
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=127.0.0.1
DB_PORT=5432

Do not commit real passwords, secret keys, email credentials, or other sensitive values to GitHub.

5. Apply migrations

python manage.py migrate

6. Create an admin/superuser if required

python manage.py createsuperuser

7. Run system checks

python manage.py check

8. Start the development server

python manage.py runserver

Open:

http://127.0.0.1:8000/

API Authentication

The API uses JWT authentication.

Token endpoint:

/api/token/

Refresh endpoint:

/api/token/refresh/

Example request:

{
    "email": "your-email@example.com",
    "password": "your-password"
}

Use the returned access token in Postman:

Authorization: Bearer <access_token>

API Testing

The APIs were tested using Postman, including:

Authentication

JWT token generation and refresh

User profile

Department CRUD

Employee CRUD

Employee profile

Role-based permissions

Authenticated and unauthorized requests

HTTP status responses

Security Notes

Before deploying to production:

Set DEBUG=False

Use a strong secret key

Keep database credentials in environment variables

Configure ALLOWED_HOSTS

Configure CSRF and CORS appropriately

Use HTTPS

Do not commit .env, database passwords, or secret keys

Configure secure cookies and production security settings

Development Status

Core modules are implemented and tested:

Authentication

Authorization

JWT authentication

Employee management

Department management

Attendance management

Leave management

Dashboard

Attendance reports

Excel export

PDF export

REST APIs

License

This project is intended for educational, portfolio, and demonstration purposes.