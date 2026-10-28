# Campusly — Student Dashboard & College Management Portal

A responsive Flask + SQLite prototype based on the provided problem statement and project-report format. It centralizes attendance, grades, campus events, notices, student profile information, and a basic admin notice-publishing page.

## Features
- Student login and role-based admin access
- Overview dashboard with attendance, average score, and course summaries
- Attendance by subject with progress bars
- Grades and score overview
- Campus events and notices
- Editable student profile
- Admin page to view demo users and publish notices
- Responsive layout with sidebar navigation and mobile menu
- SQLite database automatically initialized with demonstration data

## Run locally
1. Install Python 3.10 or newer.
2. Extract the ZIP and open this folder in VS Code.
3. Open a terminal in this folder and run:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\\Scripts\\activate
   # macOS/Linux:
   source .venv/bin/activate
   pip install -r requirements.txt
   python app.py
   ```
4. Open `http://127.0.0.1:5000`.

## Demo credentials
- Student: `student@campus.edu` / `Student@123`
- Admin: `admin@campus.edu` / `Admin@123`

## Project structure
```
student_dashboard_portal/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── attendance.html
│   ├── grades.html
│   ├── events.html
│   ├── notices.html
│   ├── profile.html
│   └── admin.html
└── static/
    ├── css/style.css
    └── js/app.js
```

## Notes
- This is a college-project prototype, not a production student information system.
- Demo credentials and sample records are seeded for presentation; replace them before real deployment.
- Before production use, configure a strong `SECRET_KEY`, add CSRF protection, enforce HTTPS, and implement institution-approved access controls.
- Attendance and grades are demonstration data and are not connected to a real college database.
