# Project report notes — Student Dashboard & College Management Portal

This file maps the prototype to the supplied **Project Report Format** (CO2: Software Process Models and Application Lifecycle Management).

## Chapter 1 — Project Introduction
**Project title:** Campusly — Student Dashboard & College Management Portal

**Background:** Academic information is often spread across notices, classroom updates, grade sheets, and attendance records. Students may need to check multiple places to understand their academic status and campus activities.

**Problem statement:** Managing academic activities, schedules, and resources manually is inefficient. Students need a centralized dashboard to track attendance, grades, events, and notices. Staff need a simple way to publish announcements and help keep campus information organized.

**Objectives**
1. Provide a single student dashboard for key academic information.
2. Display attendance by subject and summarize overall attendance.
3. Present subject-wise grades and score summaries.
4. Publish and browse campus events and notices.
5. Allow students to update basic profile information.
6. Provide an admin-only prototype screen for publishing notices.

**Scope:** This prototype includes demo login, a student overview, attendance, grades, events, notices, profile editing, and admin notice publishing. It does not connect to a real college SIS, biometric attendance system, payment system, or official examination database.

**Expected outcome:** A working web prototype that demonstrates how a centralized portal can improve access to campus information.

## Chapter 2 — Requirement Analysis
### Stakeholders
- **Student:** Views attendance, grades, events, notices, and profile.
- **Administrator:** Views demo accounts and publishes notices.
- **Faculty/management:** Potential future users for managing course records and viewing reports; those workflows are not fully implemented in this prototype.

### Functional requirements
| ID | Requirement | Prototype status |
|---|---|---|
| FR01 | User login and logout | Implemented |
| FR02 | View dashboard summary | Implemented |
| FR03 | View subject-wise attendance | Implemented |
| FR04 | View grades and score summaries | Implemented |
| FR05 | Browse campus events | Implemented |
| FR06 | Browse notices | Implemented |
| FR07 | Edit student profile details | Implemented |
| FR08 | Admin publishes a notice | Implemented |
| FR09 | Admin views demo accounts | Implemented |
| FR10 | Real institutional record integration | Out of scope |

### Non-functional requirements
- **Usability:** Responsive navigation, clear summaries, readable tables, and feedback messages.
- **Performance:** Lightweight Flask application with local SQLite storage.
- **Security:** Password hashes are stored instead of plain-text passwords; admin route checks role. For production, add CSRF protection, secure cookies, HTTPS, rate limiting, and institution-approved authorization.
- **Reliability:** SQLite tables are initialized automatically on application start.
- **Maintainability:** Routes, templates, styles, and JavaScript are separated into individual files.

### Constraints and assumptions
- Developed as a student-project prototype with a small sample dataset.
- Sample attendance, grades, users, events, and notices are not real institutional records.
- A local Python installation and Flask dependency are required.

## Chapter 3 — Software Process Model Analysis and Selection
**Recommended model: Incremental model.**

The project can be built in increments so that each delivery provides usable functionality and can be evaluated before the next feature is added.

| Candidate model | Suitability | Reason |
|---|---|---|
| Waterfall | Medium | Easy to plan, but changes to dashboard needs can be costly late in the process. |
| Incremental | High | Dashboard, attendance, grades, notices, events, and admin functions can be delivered in separate increments. |
| Agile | High | Student and faculty feedback can refine layout and workflows after each iteration. |
| Spiral | Low–Medium | Formal repeated risk analysis may be excessive for a small local prototype. |
| Prototyping | High | Early UI feedback is valuable for a dashboard-oriented project. |

**Suggested increments**
1. Login and student profile.
2. Dashboard and attendance.
3. Grades and academic summary.
4. Events and notices.
5. Admin notice publishing, testing, and polish.

## Chapter 4 — Application Lifecycle Management
Suggested lifecycle: Requirements → Planning → UI/Database Design → Development → Testing → Release → Maintenance.

| Requirement | Priority | Current status |
|---|---|---|
| Login/logout | High | Implemented |
| Dashboard summary | High | Implemented |
| Attendance | High | Implemented |
| Grades | High | Implemented |
| Events/notices | Medium | Implemented |
| Profile editing | Medium | Implemented |
| Admin notice publishing | Medium | Implemented |
| Live college database integration | Low for prototype | Not implemented |

### Work breakdown structure
1. Requirement analysis and report planning.
2. UI layout and responsive design.
3. Flask routes and authentication.
4. SQLite schema and sample data.
5. Attendance, grades, events, and notices pages.
6. Admin and profile workflows.
7. Functional and negative testing.
8. Deployment preparation and maintenance.

## Chapter 5 — Software Design
**Architecture:** Browser UI (HTML/CSS/JavaScript) → Flask routes and session-based access control → SQLite database.

**Core data entities:** Users, Attendance, Grades, Events, Notices.

**Key flow:** User submits login form → Flask validates the password hash → session stores user ID and role → dashboard loads the user's academic records and campus updates.

## Chapter 6 — Prototype Implementation
- **Frontend:** HTML5, CSS3, JavaScript, Lucide icons.
- **Backend:** Python Flask.
- **Database:** SQLite.
- **IDE:** VS Code recommended.
- **Modules:** Authentication, dashboard, attendance, grades, events, notices, profile, admin console.

The interface uses responsive cards, progress indicators, clear typography, status labels, tables, and mobile navigation. External fonts and icons load from CDNs when an internet connection is available; core page structure and styles are local.

## Chapter 7 — Software Testing
Suggested test cases to run after installing dependencies:

| Test ID | Requirement | Scenario | Expected result |
|---|---|---|---|
| TC01 | FR01 | Correct student credentials | Student dashboard opens |
| TC02 | FR01 | Incorrect password | Error message is shown |
| TC03 | FR03 | Open attendance page | Subject rows and percentages appear |
| TC04 | FR04 | Open grades page | Scores and grades appear |
| TC05 | FR05 | Open events page | Event cards appear |
| TC06 | FR06 | Open notices page | Notice list appears |
| TC07 | FR07 | Save a non-empty profile name | Success message and updated name |
| TC08 | FR08 | Student opens `/admin` | Access denied by redirect and flash message |
| TC09 | FR08 | Admin publishes title and body | Notice is added to the notice list |
| TC10 | FR08 | Admin submits empty title/body | Validation message appears |

Record actual results and screenshots after running the project locally; do not mark test cases as passed without executing them.

## AI-assisted development disclosure
If your course requires it, describe any AI tool used to scaffold or refine code, identify the parts you reviewed, and include the tests you personally ran. Verify all generated code and replace demo content with approved project data before submission.
