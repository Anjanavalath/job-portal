JobFlow: Automated Recruitment & Applicant Tracking System
JobFlow is a full-stack web application developed with Django designed to streamline the recruitment process. It bridges the gap between employers and job seekers by providing a secure, automated, and role-based environment for posting jobs and managing applications.

🚀 Key Features
🏢 For Employers
Professional Dashboard: Manage all job postings in one centralized view.

Applicant Tracking: View student details and download submitted CVs/Resumes.

Decision Integrity: A "Selection Finalized" logic that locks an application status once a candidate is accepted to prevent administrative errors.

Automated Notifications: Instant email alerts sent to candidates upon acceptance via Gmail SMTP.

🎓 For Students
Job Board: Browse active job listings with real-time status updates.

Seamless Application: Simple form-based application process with secure file upload for resumes.

🛠️ Technical Stack
Framework: Django 5.x (Python)

Database: SQLite (Development) / PostgreSQL (Production ready)

Frontend: HTML5, CSS3 (Modern UI with status-based badges), JavaScript

Communication: SMTP Integration (Google Mail Server)

Authentication: Django Built-in Auth with Role-Based Access Control (RBAC)

📂 Project Structure
Plaintext
JobPortal/
├── core/               # Main logic: Dashboards, Job CRUD, and Email triggers
├── users/              # Authentication, User Registration, and Groups
├── application/        # Student application forms and CV upload handling
├── media/              # Directory for stored Resumes/PDFs
└── templates/          # Global base templates and navigation
⚙️ Setup & Installation
Clone the repository

Bash
git clone https://github.com/Anjanavalath/job-portal
cd JobFlow
Create a Virtual Environment

Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies

Bash
pip install -r requirements.txt
Configure Environment Variables
Create a .env file or update settings.py with your Gmail SMTP credentials:

Python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
Run Migrations & Start Server

Bash
python manage.py migrate
python manage.py runserver
🛡️ Security Features
CSRF Protection: All forms are protected against Cross-Site Request Forgery.

Group Permissions: Custom logic ensures Students cannot access Employer dashboards.

Safe File Handling: Resumes are served through secure media roots, preventing unauthorized script execution.
