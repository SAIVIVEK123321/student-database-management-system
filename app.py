from flask import *
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_student")
def add_student():
    return render_template("add_student.html")

@app.route("/saverecord", methods=["POST", "GET"])
def saveRecord():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            gender = request.form["gender"]
            contact = request.form["contact"]
            dob = request.form["dob"]
            address = request.form["address"]
            with sqlite3.connect("student_detials.db") as connection:
                cursor = connection.cursor()
                cursor.execute("INSERT into Student_Info (name, email, gender, contact, dob, address) values (?,?,?,?,?,?)",(name, email, gender, contact, dob, address))
                connection.commit()
                msg = "Student details successfully added"
        except:
            connection.rollback()
            msg = "We cannot add student details to the database"
        finally:
            connection.close()
            return render_template("success_record.html", msg=msg)

@app.route("/student_info")
def student_info():
    connection = sqlite3.connect("student_detials.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Student_Info")
    rows = cursor.fetchall()
    connection.close()
    return render_template("student_info.html", rows=rows)

@app.route("/delete_student")
def delete_student():
    return render_template("delete_student.html")
@app.route("/deleterecord", methods=["POST"])
def deleterecord():
    id = request.form["id"]

    with sqlite3.connect("student_detials.db") as connection:
        cursor = connection.cursor()

        cursor.execute("select * from Student_Info where id=?", (id,))
        rows = cursor.fetchall()

        if rows:  # Simplified the check for empty list
            cursor.execute("delete from Student_Info where id = ?", (id,))
            msg = "Student detail successfully deleted"
            return render_template("delete_record.html", msg=msg)
        else:
            msg = "can't be deleted"
            return render_template("delete_record.html", msg=msg)
@app.route("/update_student")
def update_student():
    return render_template("update_student.html")

@app.route("/updaterecord",methods = ["POST"])
def updaterecord():
    id = request.form["id"]
    name = request.form["name"]
    email = request.form["email"]
    gender = request.form["gender"]
    contact = request.form["contact"]
    dob = request.form["dob"]
    address = request.form["address"]
    with sqlite3.connect("student_detials.db") as connection:
        cursor = connection.cursor()
        cursor.execute("select * from Student_Info where id=?", (id,))
        rows = cursor.fetchall()
        if not rows == []:
            cursor.execute("UPDATE Student_Info SET name=?, email=?, gender=?, contact=?, dob=?, address=? WHERE id=?", (name,email, gender, contact,dob,address, id))
            msg = "Student detail successfully updated"
            return render_template("update_record.html", msg=msg)
        else:
            msg = "can't be updated"
            return render_template("update_record.html", msg=msg)

if __name__=="__main__":
    app.run(debug=True)