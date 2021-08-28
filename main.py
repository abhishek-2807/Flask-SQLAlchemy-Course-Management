from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key = True, unique = True, autoincrement = True)
    course_name = db.Column(db.String, nullable= False)
    course_code = db.Column(db.Integer, unique = True, nullable = False)
    course_description = db.Column(db.String)
    enroll_course = db.relationship('Enrollments', backref='course')


class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key = True, unique = True, autoincrement = True)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String)
    roll_number = db.Column(db.String, unique = True, nullable = False)
    enroll_student = db.relationship('Enrollments', backref='student')

class Enrollments(db.Model):
    enrollment_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    estudent_id = db.Column(db.Integer, db.ForeignKey('student.roll_number'),
        nullable=False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey('course.course_code'),
        nullable=False)

@app.route("/")
def index():
    # num_rows_deleted = db.session.query(Enrollments).delete()
    # db.session.commit()
    return render_template("index.html")

@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/read")
def read():
    return render_template("read.html")

@app.route("/update")
def update():
    return render_template("update.html")

@app.route("/delete")
def delete():
    return render_template("delete.html")

@app.route("/adddetails", methods=["GET", "POST"])
def adddetails():
    if request.method == "POST" :
        first_name = request.form["f_name"]
        last_name = request.form["l_name"]
        roll_number = request.form["roll"]
        courses = request.form.getlist("c1")
        
        result = Student.query.filter_by(roll_number = roll_number).first()
        if result :
            print(result)
            return render_template("status.html", status = "Student already exists")

        else :
            if last_name :
                student = Student(first_name = first_name, last_name = last_name, roll_number = roll_number)
                db.session.add(student)
                db.session.commit()
                # print(last_name, type(last_name), len(last_name))

            if "v1" in courses:
                current = Student.query.filter_by(roll_number = roll_number).first()
                enr = Enrollments(estudent_id = current.student_id, ecourse_id = "1")
                db.session.add(enr)
                db.session.commit()

            if "v2" in courses:
                current = Student.query.filter_by(roll_number = roll_number).first()
                enr = Enrollments(estudent_id = current.student_id, ecourse_id = "2")
                db.session.add(enr)
                db.session.commit()

            if "v3" in courses:
                current = Student.query.filter_by(roll_number = roll_number).first()
                enr = Enrollments(estudent_id = current.student_id, ecourse_id = "3")
                db.session.add(enr)
                db.session.commit()

            if "v4" in courses:
                current = Student.query.filter_by(roll_number = roll_number).first()
                enr = Enrollments(estudent_id = current.student_id, ecourse_id = "4")
                db.session.add(enr)
                db.session.commit()

            return render_template("status.html", status = "Student successfully added")

@app.route("/readdetails", methods = ["GET", "POST"])
def readdetails():
    if request.method == "POST" :
        roll_number = request.form["roll"]

        result = Student.query.filter_by(roll_number = roll_number).first()

        if result :
            total = Enrollments.query.filter_by(estudent_id = result.student_id).all()

            all = []

            for entry in total :
                c = Course.query.filter_by(course_id = entry.ecourse_id).first()
                all.append(c)

            if len(str(result.last_name).strip()) == 0 :
                last = "NULL"
            else :
                last = result.last_name

            return render_template("readsuccess.html", first_name = result.first_name, last_name = last, roll_number = result.roll_number, all = all)

        else :
            return render_template("status.html", status = "Student doesn't exist")

@app.route("/updatedetails", methods = ["GET", "POST"])
def updatedetails():
    if request.method == "POST" :
        first_name = request.form["f_name"]
        last_name = request.form["l_name"]
        roll_number = request.form["roll"]
        courses = request.form.getlist("c1")
        
        result = Student.query.filter_by(roll_number = roll_number).first()
        if result :
            result.first_name = first_name
            result.last_name = last_name
            db.session.commit()

            enr = Enrollments.query.filter_by(estudent_id = result.student_id).all()
            for e in enr:
                db.session.delete(e)
                db.session.commit()

            if "v1" in courses:
                current = Student.query.filter_by(roll_number = roll_number).first()
                enr = Enrollments(estudent_id = current.student_id, ecourse_id = "1")
                db.session.add(enr)
                db.session.commit()

            if "v2" in courses:
                current = Student.query.filter_by(roll_number = roll_number).first()
                enr = Enrollments(estudent_id = current.student_id, ecourse_id = "2")
                db.session.add(enr)
                db.session.commit()

            if "v3" in courses:
                current = Student.query.filter_by(roll_number = roll_number).first()
                enr = Enrollments(estudent_id = current.student_id, ecourse_id = "3")
                db.session.add(enr)
                db.session.commit()

            if "v4" in courses:
                current = Student.query.filter_by(roll_number = roll_number).first()
                enr = Enrollments(estudent_id = current.student_id, ecourse_id = "4")
                db.session.add(enr)
                db.session.commit()

            return render_template("status.html", status = "Student successfuly Updated")

        else :
            return render_template("status.html", status = "Student doesn't exist")


@app.route("/deletedetails", methods=["GET", "POST"])
def deletedetails():
    if request.method == "POST" :
        roll_number = request.form["roll"]
        result = Student.query.filter_by(roll_number = roll_number).first()

        if result :

            ens = Enrollments.query.filter_by(estudent_id = result.student_id).all()
            for e in ens:
                db.session.delete(e)
                db.session.commit()

            db.session.delete(result)
            db.session.commit()
            return render_template("status.html", status = "Student Successfully deleted")
            # print(result)

        else :
            return render_template("status.html", status = "Student doesn't exist")
        
if __name__ == "__main__":
    app.run(debug = True)