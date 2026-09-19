from flask import Flask, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "student_result_secret"

DB = "students.db"


# ---------- DATABASE ----------

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


def create_database():

    con = db()

    con.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            mark1 INTEGER,
            mark2 INTEGER,
            mark3 INTEGER,
            mark4 INTEGER,
            mark5 INTEGER
        )
    """)

    count = con.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    if count == 0:

        students = [
            ("STU001", "Jenilia", "1234", 85, 86, 87, 88, 89),
            ("STU002", "Nisha", "1234", 90, 88, 86, 85, 86),
            ("STU003", "Prakash Raj", "1234", 92, 87, 85, 86, 85),
            ("STU004", "Dhamodharan", "1234", 88, 86, 87, 89, 85)
        ]

        con.executemany("""
            INSERT INTO students
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, students)

        con.commit()

    con.close()


# ---------- HTML DESIGN ----------

def page(content):

    return f"""
<!DOCTYPE html>

<html>

<head>

<title>Student Result Management System</title>

<meta name="viewport" content="width=device-width, initial-scale=1">

<style>

* {{
    box-sizing: border-box;
    font-family: Arial, sans-serif;
}}

body {{
    margin: 0;
    background: #eef2f7;
}}

header {{
    background: #172b4d;
    color: white;
    text-align: center;
    padding: 22px;
}}

.container {{
    width: 95%;
    max-width: 1100px;
    margin: 30px auto;
}}

.box {{
    background: white;
    padding: 25px;
    margin-bottom: 25px;
    border-radius: 12px;
    box-shadow: 0 3px 12px #ccc;
}}

h2 {{
    color: #172b4d;
}}

input {{
    width: 100%;
    padding: 11px;
    margin: 7px 0 12px;
    border: 1px solid #aaa;
    border-radius: 6px;
}}

button {{
    background: #172b4d;
    color: white;
    border: none;
    padding: 11px 18px;
    border-radius: 6px;
    cursor: pointer;
}}

button:hover {{
    opacity: .85;
}}

.delete {{
    background: #c62828;
}}

.logout {{
    display: inline-block;
    background: #555;
    color: white;
    text-decoration: none;
    padding: 10px 15px;
    border-radius: 6px;
}}

.message {{
    background: #ffe0e0;
    color: #b00000;
    padding: 12px;
    border-radius: 6px;
    margin-bottom: 20px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
}}

th {{
    background: #172b4d;
    color: white;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 10px;
    text-align: center;
}}

.subject {{
    background: #f4f6f8;
    padding: 15px;
    border-radius: 8px;
    margin: 15px 0;
}}

@media(max-width:700px) {{

    table {{
        font-size: 11px;
    }}

    th, td {{
        padding: 6px;
    }}

}}

</style>

</head>

<body>

<header>

<h1>Student Result Management System</h1>

</header>

<div class="container">

{content}

</div>

</body>

</html>
"""


# ---------- HOME ----------

@app.route("/")
def home():

    content = """

<div class="box">

<h2>Student Login</h2>

<form action="/student_login" method="POST">

<input
type="text"
name="student_id"
placeholder="Student ID"
required>

<input
type="password"
name="password"
placeholder="Password"
required>

<button type="submit">
Student Login
</button>

</form>

</div>


<div class="box">

<h2>Admin Login</h2>

<form action="/admin_login" method="POST">

<input
type="text"
name="admin_id"
placeholder="Admin ID"
required>

<input
type="password"
name="password"
placeholder="Password"
required>

<button type="submit">
Admin Login
</button>

</form>

</div>

"""

    return page(content)


# ---------- STUDENT LOGIN ----------

@app.route("/student_login", methods=["POST"])
def student_login():

    student_id = request.form["student_id"]
    password = request.form["password"]

    con = db()

    student = con.execute("""
        SELECT * FROM students
        WHERE id=? AND password=?
    """, (student_id, password)).fetchone()

    con.close()

    if not student:

        return page("""
        <div class="box message">
        Wrong Student ID or Password!
        </div>

        <div class="box">
        <a class="logout" href="/">Back</a>
        </div>
        """)

    total = (
        student["mark1"]
        + student["mark2"]
        + student["mark3"]
        + student["mark4"]
        + student["mark5"]
    )

    average = total / 5

    content = f"""

<div class="box">

<a class="logout" href="/">Logout</a>

<h2>Student Result</h2>

<table>

<tr>
<th>Student ID</th>
<td>{student["id"]}</td>
</tr>

<tr>
<th>Name</th>
<td>{student["name"]}</td>
</tr>

</table>


<h2>Subject Marks</h2>

<table>

<tr>
<th>Subject</th>
<th>Marks</th>
</tr>

<tr>
<td>Python Programming</td>
<td>{student["mark1"]}</td>
</tr>

<tr>
<td>Database Management System</td>
<td>{student["mark2"]}</td>
</tr>

<tr>
<td>Data Structures</td>
<td>{student["mark3"]}</td>
</tr>

<tr>
<td>Object Oriented Programming</td>
<td>{student["mark4"]}</td>
</tr>

<tr>
<td>Computer Organization</td>
<td>{student["mark5"]}</td>
</tr>

<tr>
<th>Total</th>
<th>{total} / 500</th>
</tr>

<tr>
<th>Average</th>
<th>{average:.2f} / 100</th>
</tr>

</table>

</div>

"""

    return page(content)


# ---------- ADMIN LOGIN ----------

@app.route("/admin_login", methods=["POST"])
def admin_login():

    admin_id = request.form["admin_id"]
    password = request.form["password"]

    if admin_id == "admin" and password == "admin123":

        session["admin"] = True

        return redirect("/admin")

    return page("""
    <div class="box message">
    Wrong Admin ID or Password!
    </div>

    <div class="box">
    <a class="logout" href="/">Back</a>
    </div>
    """)


# ---------- ADMIN DASHBOARD ----------

@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect("/")

    con = db()

    students = con.execute(
        "SELECT * FROM students ORDER BY id"
    ).fetchall()

    con.close()

    rows = ""

    for s in students:

        total = (
            s["mark1"]
            + s["mark2"]
            + s["mark3"]
            + s["mark4"]
            + s["mark5"]
        )

        rows += f"""

<tr>

<td>{s["id"]}</td>

<td>{s["name"]}</td>

<td>{s["mark1"]}</td>

<td>{s["mark2"]}</td>

<td>{s["mark3"]}</td>

<td>{s["mark4"]}</td>

<td>{s["mark5"]}</td>

<td><b>{total}</b></td>

<td>

<form action="/delete/{s["id"]}" method="POST">

<button class="delete">
Delete
</button>

</form>

</td>

</tr>

"""

    content = f"""

<div class="box">

<a class="logout" href="/logout">
Logout
</a>

<h2>Admin Dashboard</h2>

<h3>Add New Student</h3>

<form action="/add" method="POST">

<input
type="text"
name="id"
placeholder="Student ID"
required>

<input
type="text"
name="name"
placeholder="Student Name"
required>

<input
type="password"
name="password"
placeholder="Student Password"
required>


<div class="subject">

<h3>Enter Marks</h3>

<label>Python Programming</label>

<input
type="number"
name="mark1"
min="0"
max="100"
required>


<label>Database Management System</label>

<input
type="number"
name="mark2"
min="0"
max="100"
required>


<label>Data Structures</label>

<input
type="number"
name="mark3"
min="0"
max="100"
required>


<label>Object Oriented Programming</label>

<input
type="number"
name="mark4"
min="0"
max="100"
required>


<label>Computer Organization</label>

<input
type="number"
name="mark5"
min="0"
max="100"
required>

</div>

<button type="submit">
Add Student
</button>

</form>

</div>


<div class="box">

<h2>Student Records</h2>

<table>

<tr>

<th>ID</th>
<th>Name</th>
<th>Python</th>
<th>DBMS</th>
<th>DS</th>
<th>OOP</th>
<th>CO</th>
<th>Total</th>
<th>Action</th>

</tr>

{rows}

</table>

</div>

"""

    return page(content)


# ---------- ADD STUDENT ----------

@app.route("/add", methods=["POST"])
def add_student():

    if not session.get("admin"):
        return redirect("/")

    con = db()

    try:

        con.execute("""
            INSERT INTO students
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            request.form["id"],
            request.form["name"],
            request.form["password"],
            request.form["mark1"],
            request.form["mark2"],
            request.form["mark3"],
            request.form["mark4"],
            request.form["mark5"]
        ))

        con.commit()

    except sqlite3.IntegrityError:
        pass

    con.close()

    return redirect("/admin")


# ---------- DELETE ----------

@app.route("/delete/<student_id>", methods=["POST"])
def delete_student(student_id):

    if not session.get("admin"):
        return redirect("/")

    con = db()

    con.execute(
        "DELETE FROM students WHERE id=?",
        (student_id,)
    )

    con.commit()
    con.close()

    return redirect("/admin")


# ---------- LOGOUT ----------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ---------- START ----------

create_database()

if __name__ == "__main__":
    app.run(debug=True)
