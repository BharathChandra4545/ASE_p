from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3, os
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-change-this-secret")
DB_PATH = os.path.join(os.path.dirname(__file__), "portal.db")

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS users(
          id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL,
          password TEXT NOT NULL, role TEXT NOT NULL DEFAULT 'student', student_id TEXT,
          department TEXT, year TEXT
        );
        CREATE TABLE IF NOT EXISTS attendance(
          id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, subject TEXT NOT NULL,
          attended INTEGER NOT NULL, total INTEGER NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS grades(
          id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, subject TEXT NOT NULL,
          code TEXT, score INTEGER NOT NULL, grade TEXT NOT NULL, semester TEXT,
          FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS events(
          id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, category TEXT, event_date TEXT,
          location TEXT, description TEXT
        );
        CREATE TABLE IF NOT EXISTS notices(
          id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, body TEXT, posted_on TEXT,
          priority TEXT DEFAULT 'Normal'
        );
        """)
        if con.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
            con.execute("INSERT INTO users(name,email,password,role,student_id,department,year) VALUES(?,?,?,?,?,?,?)",
                ("Bharath Chandra","student@campus.edu",generate_password_hash("Student@123"),"student","STU2026","CSE · AI & ML","3rd Year"))
            con.execute("INSERT INTO users(name,email,password,role,student_id,department,year) VALUES(?,?,?,?,?,?,?)",
                ("Campus Admin","admin@campus.edu",generate_password_hash("Admin@123"),"admin","ADM001","Administration","Staff"))
            uid = con.execute("SELECT id FROM users WHERE email='student@campus.edu'").fetchone()["id"]
            rows = [
                ("Data Structures",18,20),("Database Systems",16,18),("Machine Learning",17,20),
                ("Operating Systems",14,16),("Computer Networks",15,18),("Software Engineering",19,20)]
            for s,a,t in rows: con.execute("INSERT INTO attendance(user_id,subject,attended,total) VALUES(?,?,?,?)",(uid,s,a,t))
            grade_rows = [
                ("Data Structures","CS301",91,"A+","Semester 5"),("Database Systems","CS302",86,"A","Semester 5"),
                ("Machine Learning","AI305",94,"O","Semester 5"),("Operating Systems","CS303",82,"A","Semester 5"),
                ("Computer Networks","CS304",78,"B+","Semester 5"),("Software Engineering","SE306",89,"A","Semester 5")]
            for s,c,score,g,sem in grade_rows: con.execute("INSERT INTO grades(user_id,subject,code,score,grade,semester) VALUES(?,?,?,?,?,?)",(uid,s,c,score,g,sem))
            con.executemany("INSERT INTO events(title,category,event_date,location,description) VALUES(?,?,?,?,?)",[
                ("AI & Innovation Summit","Technology","2026-11-04","Innovation Hub","Explore applied AI, responsible technology and student projects."),
                ("Project Review — Phase I","Academic","2026-11-06","Block C · Room 204","Bring your project prototype, progress notes and test evidence."),
                ("Campus Sports Day","Community","2026-11-12","Main Sports Ground","Team events, friendly matches and campus activities."),
                ("Career Connect Workshop","Career","2026-11-18","Seminar Hall","Resume reviews and interview preparation with alumni.")])
            con.executemany("INSERT INTO notices(title,body,posted_on,priority) VALUES(?,?,?,?)",[
                ("Mid-semester schedule published","The updated timetable is available in the academic office. Check your course portal before attending.","2026-10-27","Important"),
                ("Library hours extended","The central library will remain open until 9:00 PM during project review week.","2026-10-25","Normal"),
                ("Update your student profile","Please verify your contact information and department details before the next review.","2026-10-23","Reminder")])

def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if "user_id" not in session: return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapped

@app.context_processor
def inject_user():
    if "user_id" in session:
        with db() as con:
            user=con.execute("SELECT * FROM users WHERE id=?",(session["user_id"],)).fetchone()
        return {"current_user":user}
    return {"current_user":None}

@app.route("/")
def home():
    return redirect(url_for("dashboard") if "user_id" in session else url_for("login"))

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form.get("email","").strip().lower()
        password=request.form.get("password","")
        with db() as con: user=con.execute("SELECT * FROM users WHERE email=?",(email,)).fetchone()
        if user and check_password_hash(user["password"],password):
            session.clear(); session["user_id"]=user["id"]; session["role"]=user["role"]
            return redirect(url_for("dashboard"))
        flash("Email or password is incorrect. Please try again.","error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear(); return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    with db() as con:
        user=con.execute("SELECT * FROM users WHERE id=?",(session["user_id"],)).fetchone()
        attendance=con.execute("SELECT * FROM attendance WHERE user_id=?",(user["id"],)).fetchall()
        grades=con.execute("SELECT * FROM grades WHERE user_id=? ORDER BY score DESC",(user["id"],)).fetchall()
        events=con.execute("SELECT * FROM events ORDER BY event_date LIMIT 3").fetchall()
        notices=con.execute("SELECT * FROM notices ORDER BY posted_on DESC LIMIT 3").fetchall()
    total_att=sum(r["total"] for r in attendance); attended=sum(r["attended"] for r in attendance)
    pct=round(attended/total_att*100) if total_att else 0
    avg=round(sum(r["score"] for r in grades)/len(grades)) if grades else 0
    return render_template("dashboard.html",attendance=attendance,grades=grades,events=events,notices=notices,attendance_pct=pct,avg=avg)

@app.route("/attendance")
@login_required
def attendance_page():
    with db() as con: rows=con.execute("SELECT * FROM attendance WHERE user_id=? ORDER BY subject",(session["user_id"],)).fetchall()
    total=sum(r["total"] for r in rows); attended=sum(r["attended"] for r in rows)
    return render_template("attendance.html",rows=rows,pct=round(attended/total*100) if total else 0)

@app.route("/grades")
@login_required
def grades_page():
    with db() as con: rows=con.execute("SELECT * FROM grades WHERE user_id=? ORDER BY subject",(session["user_id"],)).fetchall()
    avg=round(sum(r["score"] for r in rows)/len(rows)) if rows else 0
    return render_template("grades.html",rows=rows,avg=avg)

@app.route("/events")
@login_required
def events_page():
    with db() as con: rows=con.execute("SELECT * FROM events ORDER BY event_date").fetchall()
    return render_template("events.html",rows=rows)

@app.route("/notices")
@login_required
def notices_page():
    with db() as con: rows=con.execute("SELECT * FROM notices ORDER BY posted_on DESC").fetchall()
    return render_template("notices.html",rows=rows)

@app.route("/profile", methods=["GET","POST"])
@login_required
def profile():
    if request.method=="POST":
        name=request.form.get("name","").strip()
        if name:
            with db() as con: con.execute("UPDATE users SET name=?, department=?, year=? WHERE id=?",
                (name,request.form.get("department","").strip(),request.form.get("year","").strip(),session["user_id"]))
            flash("Your profile has been updated.","success")
            return redirect(url_for("profile"))
        flash("Name cannot be empty.","error")
    with db() as con: user=con.execute("SELECT * FROM users WHERE id=?",(session["user_id"],)).fetchone()
    return render_template("profile.html",user=user)

@app.route("/admin", methods=["GET","POST"])
@login_required
def admin():
    if session.get("role")!="admin":
        flash("Admin access is required for that page.","error"); return redirect(url_for("dashboard"))
    if request.method=="POST":
        title=request.form.get("title","").strip(); body=request.form.get("body","").strip()
        if title and body:
            with db() as con: con.execute("INSERT INTO notices(title,body,posted_on,priority) VALUES(?,?,date('now'),?)",
                (title,body,request.form.get("priority","Normal")))
            flash("Notice published successfully.","success")
        else: flash("Enter both a title and message.","error")
        return redirect(url_for("admin"))
    with db() as con:
        users=con.execute("SELECT id,name,email,role,student_id,department,year FROM users ORDER BY role,name").fetchall()
        notices=con.execute("SELECT * FROM notices ORDER BY posted_on DESC").fetchall()
        events=con.execute("SELECT * FROM events ORDER BY event_date").fetchall()
    return render_template("admin.html",users=users,notices=notices,events=events)

@app.route("/health")
def health(): return {"status":"ok","app":"Campusly Student Portal"}

init_db()
if __name__ == "__main__":
    app.run(debug=True)
