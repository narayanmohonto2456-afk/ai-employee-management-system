# Employee Management System (EMS)

A production-style **Employee Management System** built with Django and Django REST Framework. The project provides centralized management of employees, departments, attendance, leave applications, reporting, authentication, role-based permissions, and an AI chatbot powered by Ollama.

The project was developed as a full-stack Django application with both a traditional web interface and REST APIs.

---

## 📌 Project Overview

The Employee Management System is designed to help an organization manage its employee-related operations from a single platform.

The system supports multiple user roles, employee profiles, department management, attendance tracking, leave management, reporting, REST APIs, JWT authentication, and an AI-powered chatbot.

### Main objectives

* Manage employees and employee profiles
* Manage organizational departments
* Track employee attendance
* Handle employee leave applications
* Approve/reject leave requests
* Generate attendance reports
* Export attendance reports to Excel and PDF
* Provide REST APIs
* Provide JWT authentication for APIs
* Implement role-based access control
* Provide a dashboard with statistics
* Provide an AI chatbot using Ollama
* Maintain a clean and modular Django architecture

---

# 🚀 Features

## 🔐 Authentication & User Management

The project uses Django's authentication system with a custom user model.

### Features

* User registration
* User login
* User logout
* User profile
* Profile image
* Email verification
* Account activation
* Role-based users
* Password management
* Authentication-protected pages

### Supported roles

* **ADMIN**
* **HR**
* **EMPLOYEE**

Different roles receive different permissions and access to different sections of the system.

---

# 👥 Employee Management

The Employee module provides complete employee management functionality.

### Features

* Create employee
* View employee list
* View employee details
* Update employee
* Delete employee
* Employee profile
* Employee ID
* Designation
* Department
* Joining date
* Gender
* Employee-related user information
* Search and filtering
* Pagination

Employee records are linked with the custom user model.

---

# 🏢 Department Management

The Department module allows administrators and HR users to manage organizational departments.

### Features

* Create department
* View department list
* View department details
* Update department
* Delete department
* Department code
* Department name
* Department description
* Department-related employee information
* Search
* Filtering
* Pagination

---

# 🕐 Attendance Management

The Attendance module manages daily employee attendance.

### Attendance statuses

* Present
* Absent
* Leave
* Half Day

### Features

* Attendance list
* Create attendance record
* Update attendance
* View attendance details
* Delete attendance
* Employee-specific attendance
* Check-in
* Check-out
* Automatic working-hours calculation
* Date filtering
* Employee filtering
* Status filtering
* Pagination
* AJAX-compatible check-in/check-out responses

### Check-in workflow

```text
Employee Login
      ↓
Attendance
      ↓
Check In
      ↓
Attendance record created
      ↓
Status = Present
```

### Check-out workflow

```text
Employee
   ↓
Check Out
   ↓
Check-out time recorded
   ↓
Working hours calculated
   ↓
Attendance updated
```

The system prevents duplicate check-ins and prevents checkout before check-in.

---

# 🏖️ Leave Management

Employees can submit leave applications through the Leave Management module.

### Features

* Leave types
* Apply for leave
* View leave requests
* View leave details
* Update leave request
* Leave status management
* HR/Admin approval
* HR/Admin rejection
* Employee-specific leave visibility

### Leave statuses

```text
Pending
Approved
Rejected
```

### Leave workflow

```text
Employee
   ↓
Apply for Leave
   ↓
Pending
   ↓
HR / Admin Review
   ↓
 ┌───────────────┐
 │               │
Approved       Rejected
```

---

# 📊 Dashboard

The dashboard provides a quick overview of the organization's data.

### Dashboard statistics

* Total employees
* Total departments
* Total attendance records
* Total leave requests
* Today's present employees
* Today's absent employees
* Today's leave
* Today's half-day attendance

### Dashboard sections

* Quick actions
* Recent employees
* Recent leave requests
* Attendance overview
* Attendance statistics chart

The dashboard uses Chart.js for visualizing attendance statistics.

---

# 📑 Attendance Reports

The reporting module provides attendance reporting functionality.

### Features

* Attendance report page
* Employee filtering
* Department filtering
* Status filtering
* Start-date filtering
* End-date filtering
* Attendance statistics

### Export formats

The system supports:

* Excel
* PDF

### Excel report

Excel reports are generated using **openpyxl**.

The report contains information such as:

* Employee ID
* Employee name
* Department
* Date
* Check-in
* Check-out
* Working hours
* Status

### PDF report

PDF reports are generated using **ReportLab**.

---

# 🤖 AI Chatbot

The project includes an AI chatbot powered by **Ollama**.

### AI stack

```text
Django
   ↓
Chatbot View
   ↓
Ollama
   ↓
Local AI Model
```

The chatbot uses a locally running Ollama model rather than relying on an external AI API.

### Current model

```text
llama3.2:3b
```

This provides a local AI assistant while keeping the application independent from cloud AI APIs.

---

# 🌐 REST API

The project includes a REST API built with **Django REST Framework**.

The API provides programmatic access to important EMS functionality.

## API authentication

JWT authentication is implemented using:

```text
djangorestframework-simplejwt
```

### JWT endpoints

```text
/api/token/
/api/token/refresh/
```

### Profile API

```text
/api/profile/
```

### Employee APIs

```text
/api/employees/
/api/employees/<id>/
```

### Employee profile API

```text
/api/my-profile/
```

---

# 🔎 API Features

The Employee API supports:

* List employees
* Create employee
* Retrieve employee
* Update employee
* Delete employee
* Search
* Filtering
* Ordering

### Search examples

Employee search can use fields such as:

```text
employee_id
first_name
last_name
username
department
designation
```

### Filtering

Employee records can be filtered using fields such as:

```text
department
designation
gender
```

### Ordering

Employee records can be ordered using:

```text
employee_id
joining_date
created_at
```

---

# 🔒 Permissions & Security

The project implements role-based access control.

### Main roles

| Role     | Main responsibilities                                     |
| -------- | --------------------------------------------------------- |
| ADMIN    | Full system administration                                |
| HR       | Employee, attendance and leave management                 |
| EMPLOYEE | Personal profile, attendance and leave-related operations |

The application uses Django authentication and permission mechanisms to restrict protected functionality.

REST APIs use authentication and custom permissions such as:

```text
IsAuthenticated
IsAdminOrReadOnly
```

---

# 🧩 Project Architecture

The project follows Django's modular application architecture.

```text
Employee Management System
│
├── accounts
├── api
├── attendance
├── chatbot
├── dashboard
├── departments
├── employees
├── leave_management
├── reports
│
├── config
│
├── templates
│   ├── base.html
│   ├── accounts
│   ├── attendance
│   ├── dashboard
│   ├── departments
│   ├── employees
│   ├── leave_management
│   ├── reports
│   └── includes
│
├── static
│   ├── css
│   └── js
│
├── manage.py
├── requirements.txt
└── README.md
```

---

# 🛠️ Technology Stack

## Backend

* Python
* Django
* Django REST Framework
* Django Filters
* Simple JWT

## Database

* PostgreSQL

## Frontend

* HTML5
* CSS3
* Bootstrap 5
* Bootstrap Icons
* JavaScript
* jQuery
* AJAX
* Chart.js

## Reporting

* openpyxl
* ReportLab

## AI

* Ollama
* Llama 3.2 3B

## API Testing

* Postman

## Development Tools

* Visual Studio Code
* Git
* GitHub
* pgAdmin 4

---

# 📦 Main Python Dependencies

The project uses packages including:

```text
Django
djangorestframework
djangorestframework-simplejwt
django-filter
psycopg
openpyxl
reportlab
```

Ollama is installed separately as a local application.

---

# 💻 Installation

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Move into the project:

```bash
cd employee_management_system
```

---

## 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🗄️ PostgreSQL Configuration

Create a PostgreSQL database using PostgreSQL or pgAdmin.

Configure the database credentials in:

```text
config/settings.py
```

Example:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "employee_management_system",
        "USER": "postgres",
        "PASSWORD": "your_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

Use your own database credentials.

---

# 🔑 Environment Variables

For a production deployment, sensitive configuration should not be hardcoded.

Recommended variables include:

```text
SECRET_KEY
DEBUG
DATABASE_NAME
DATABASE_USER
DATABASE_PASSWORD
DATABASE_HOST
DATABASE_PORT
```

For production:

```text
DEBUG=False
```

and configure the appropriate:

```text
ALLOWED_HOSTS
```

---

# 🗃️ Database Migration

Run:

```bash
python manage.py makemigrations
```

Then:

```bash
python manage.py migrate
```

---

# 👤 Create Superuser

Create an administrator account:

```bash
python manage.py createsuperuser
```

Follow the prompts.

---

# 🔍 Run System Checks

Before starting the server:

```bash
python manage.py check
```

Expected result:

```text
System check identified no issues (0 silenced).
```

---

# ▶️ Run the Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# 🤖 Ollama Setup

Install Ollama separately.

Verify the installation:

```bash
ollama --version
```

Pull the required model:

```bash
ollama pull llama3.2:3b
```

Verify installed models:

```bash
ollama list
```

Expected model:

```text
llama3.2:3b
```

Start Ollama if required by your environment and make sure the Ollama service is available before using the chatbot.

---

# 🧪 API Testing

The REST API was tested using **Postman**.

Important API operations include:

### JWT

```text
POST /api/token/
POST /api/token/refresh/
```

### Profile

```text
GET /api/profile/
```

### Employees

```text
GET    /api/employees/
POST   /api/employees/
GET    /api/employees/<id>/
PATCH  /api/employees/<id>/
PUT    /api/employees/<id>/
DELETE /api/employees/<id>/
```

### My Profile

```text
GET /api/my-profile/
```

JWT authentication is required for protected endpoints.

---

# 📋 Functional Testing

The major application modules have been tested during development.

### Authentication

* Registration
* Login
* Logout
* Profile
* Role-based access
* Email verification

### Employees

* Create
* Read
* Update
* Delete
* Search
* Filtering

### Departments

* Create
* Read
* Update
* Delete
* Search
* Filtering

### Attendance

* Create attendance
* Check-in
* Check-out
* Working-hours calculation
* Duplicate check-in prevention
* Attendance filtering

### Leave

* Apply leave
* View leave
* Approve leave
* Reject leave
* Status management

### Reports

* Attendance report
* Excel export
* PDF export

### APIs

* JWT authentication
* Profile API
* Employee APIs
* Employee detail API
* My profile API
* Search
* Filtering
* Ordering

### AI

* Ollama connection
* Local Llama model
* Chatbot functionality

---

# 📁 Important Django Applications

## `accounts`

Responsible for:

* Custom user model
* Authentication
* Registration
* Login
* Logout
* User profile
* Email verification
* Roles

## `employees`

Responsible for:

* Employee model
* Employee CRUD
* Employee profiles

## `departments`

Responsible for:

* Department model
* Department CRUD

## `attendance`

Responsible for:

* Attendance model
* Attendance CRUD
* Check-in
* Check-out
* Working hours

## `leave_management`

Responsible for:

* Leave types
* Leave applications
* Approval
* Rejection

## `reports`

Responsible for:

* Attendance reports
* Excel export
* PDF export

## `dashboard`

Responsible for:

* Dashboard statistics
* Recent employees
* Recent leave requests
* Attendance overview

## `api`

Responsible for:

* REST API
* Serializers
* API views
* JWT authentication
* API permissions
* Search/filter/order functionality

## `chatbot`

Responsible for:

* AI chatbot interface
* Ollama integration
* Local LLM communication

---

# 🔄 Overall System Workflow

```text
                    ┌───────────────┐
                    │     User      │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Authentication│
                    └───────┬───────┘
                            │
               ┌────────────┼────────────┐
               ▼            ▼            ▼
            ADMIN           HR        EMPLOYEE
               │            │            │
               └────────────┼────────────┘
                            ▼
                    ┌───────────────┐
                    │   Dashboard   │
                    └───────┬───────┘
                            │
       ┌────────────┬───────┼────────┬─────────────┐
       ▼            ▼       ▼        ▼             ▼
   Employees   Departments Attendance Leave      Reports
       │            │       │        │             │
       └────────────┴───────┴────────┴─────────────┘
                            │
                            ▼
                       PostgreSQL
```

---

# 🧠 AI Chatbot Architecture

```text
User
 │
 ▼
Django Chatbot UI
 │
 ▼
Chatbot View
 │
 ▼
Ollama API
 │
 ▼
Llama 3.2 3B
 │
 ▼
AI Response
 │
 ▼
Django UI
```

The AI model runs locally through Ollama.

---

# 📊 Reporting Architecture

```text
Attendance Database
        │
        ▼
Attendance QuerySet
        │
        ├───────────────┐
        ▼               ▼
   Excel Export      PDF Export
        │               │
        ▼               ▼
    openpyxl         ReportLab
        │               │
        ▼               ▼
    .xlsx             .pdf
```

---

# 🔮 Future Improvements

The current project can be extended further.

Possible improvements include:

### Background processing

Add:

```text
Celery + Redis
```

for:

* Background email sending
* Scheduled notifications
* Large report generation
* Automated attendance reminders

### Advanced security

* Production HTTPS
* CSRF/security hardening
* Rate limiting
* API throttling
* Secure secret management

### Advanced attendance

* Monthly attendance summaries
* Late-arrival tracking
* Overtime calculation
* Attendance calendar
* Automated absent marking

### Leave improvements

* Leave balance
* Annual leave limits
* Leave history
* Multi-level approval
* Email notifications

### Dashboard improvements

* More charts
* Monthly attendance trends
* Department-wise statistics
* Employee performance metrics

### Deployment

Possible deployment platforms include:

* AWS
* Azure
* DigitalOcean
* Render
* Railway

A production deployment could use:

```text
Nginx
   ↓
Gunicorn
   ↓
Django
   ↓
PostgreSQL
```

with Redis/Celery added for background processing.

---

# 🧑‍💻 Development Approach

The project was developed using a modular approach.

Each major business function is separated into its own Django application.

This makes the project:

* Easier to maintain
* Easier to debug
* Easier to extend
* Easier to test
* Easier to understand

The project also separates:

```text
Models
Views
Forms
Serializers
URLs
Templates
Static files
API logic
```

where appropriate.

---

# 📚 What This Project Demonstrates

This project demonstrates practical knowledge of:

* Python
* Django
* Django ORM
* Custom User Models
* Django Authentication
* Django Permissions
* Role-Based Access Control
* Class-Based Views
* Function-Based Views
* Django Forms
* ModelForms
* PostgreSQL
* Django REST Framework
* JWT Authentication
* API development
* API testing with Postman
* Search and filtering
* Pagination
* AJAX
* JavaScript
* Bootstrap
* Chart.js
* Excel generation
* PDF generation
* Local AI integration
* Ollama
* Git/GitHub
* Modular software architecture

---

# 🏆 Project Highlights

The project combines traditional Django web development with modern backend API development.

### Full-stack application

```text
Frontend
   ↓
Django Templates + Bootstrap + JavaScript
   ↓
Django
   ↓
PostgreSQL
```

### API architecture

```text
Client
   ↓
JWT
   ↓
Django REST Framework
   ↓
Serializers
   ↓
Django ORM
   ↓
PostgreSQL
```

### AI architecture

```text
Django
   ↓
Ollama
   ↓
Llama 3.2 3B
```

---

# 📸 Screenshots

Add screenshots of the application here after uploading them to the repository.

Recommended screenshots:

1. Login page
2. Dashboard
3. Employee list
4. Employee detail
5. Department list
6. Attendance page
7. Leave management
8. Attendance report
9. AI chatbot
10. Postman API testing

Example:

```markdown
![Dashboard](screenshots/dashboard.png)
```

---

# 📌 Project Status

**Status: Completed**

The core Employee Management System functionality has been implemented and tested.

The project currently includes:

* Authentication
* User roles
* Employee management
* Department management
* Attendance management
* Leave management
* Dashboard
* Reports
* Excel export
* PDF export
* REST APIs
* JWT authentication
* API filtering/search/ordering
* AI chatbot with Ollama

---

# 👨‍💻 Author

**Narayan Mohanta**

Diploma in Mechanical Engineering
Full-Stack Django / Python Project

---

# 📄 License

This project is intended primarily as an educational and portfolio project.

You may modify and extend it for learning and development purposes.

---

# ⭐ If You Like This Project

If this project helped you or you found it useful, consider giving the repository a ⭐ on GitHub.

---

## Final Architecture

```text
                    Employee Management System
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
     Web Application       REST API          AI Chatbot
          │                   │                   │
          ▼                   ▼                   ▼
      Django             DRF + JWT           Ollama
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
                              ▼
                         PostgreSQL
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
        Employees        Attendance          Leave
             │                │                │
             └────────────────┼────────────────┘
                              │
                              ▼
                           Reports
                         ┌─────────┐
                         │  Excel  │
                         │   PDF   │
                         └─────────┘
```

**Employee Management System — Django Full-Stack + REST API + Local AI**
