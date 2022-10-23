from jinja2 import Template
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import url_for


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db = SQLAlchemy()
db.init_app(app)
app.app_context().push


class student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)


class course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)


class enrollments(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey(
        "student.student_id"), nullable=False)
    ecourse_id = db.Column(db.Integer,  db.ForeignKey(
        "course.course_id"),      nullable=False)


@app.route("/", methods=["GET", "POST"])
def main():
    students = student.query.all()
    length = len(students)
    return render_template("index.html", students=students, length=length)


@app.route("/student/create", methods=["GET"])
def add():
    return render_template("add.html")


@app.route("/student/create", methods=["POST"])
def create():
    courses = course.query.all()
    student_list = student.query.all()
    if request.method == 'POST':
        r_n = request.form['roll']
        for s in student_list:
            if s.roll_number == r_n:
                return render_template("error.html")
        student1 = student(
            roll_number=request.form['roll'], first_name=request.form['f_name'], last_name=request.form['l_name'])
        db.session.add(student1)
        db.session.commit()
        s_list = student.query.all()
        s_id = 0
        for s in s_list:
            if(s.roll_number == request.form['roll']):
                s_id = s.student_id
                break

        student_course = request.form['courses']
        course_list = course.query.all()
        c_id = 0

        for cou in request.form.getlist('courses'):
            if(cou == 'course_1'):
                c_id = 1
                en = enrollments(estudent_id=s_id, ecourse_id=c_id)
                db.session.add(en)
                db.session.commit()
            if(cou == 'course_2'):
                c_id = 2
                en = enrollments(estudent_id=s_id, ecourse_id=c_id)
                db.session.add(en)
                db.session.commit()
            if(cou == 'course_3'):
                c_id = 3
                en = enrollments(estudent_id=s_id, ecourse_id=c_id)
                db.session.add(en)
                db.session.commit()
            if(cou == 'course_4'):
                c_id = 4
                en = enrollments(estudent_id=s_id, ecourse_id=c_id)
                db.session.add(en)
                db.session.commit()

        return redirect(url_for("main"))


@app.route('/student/<int:student_id>/update', methods=["GET"])
def update_in(student_id):
    students = student.query.all()
    enroll = enrollments.query.all()
    cid = []
    for c in enroll:
        if c.estudent_id == student_id:
            cid.append(c.ecourse_id)
    for studen in students:
        if studen.student_id == student_id:
            rets = studen
            break
    return render_template("update.html", student=rets, cid=cid)


@app.route('/student/<int:student_id>/update', methods=["POST"])
def update_out(student_id):
    if request.method == 'POST':
        user = student.query.get(student_id)
        user.first_name = request.form['f_name']
        user.last_name = request.form['l_name']
        db.session.commit()
        obj = enrollments.query.filter_by(estudent_id=student_id).all()
        for o in obj:
            db.session.delete(o)
            db.session.commit()
        for cou in request.form.getlist('courses'):
            if(cou == 'course_1'):
                c_id = 1
                en = enrollments(estudent_id=student_id, ecourse_id=c_id)
                db.session.add(en)
                db.session.commit()
            if(cou == 'course_2'):
                c_id = 2
                en = enrollments(estudent_id=student_id, ecourse_id=c_id)
                db.session.add(en)
                db.session.commit()
            if(cou == 'course_3'):
                c_id = 3
                en = enrollments(estudent_id=student_id, ecourse_id=c_id)
                db.session.add(en)
                db.session.commit()
            if(cou == 'course_4'):
                c_id = 4
                en = enrollments(estudent_id=student_id, ecourse_id=c_id)
                db.session.add(en)
                db.session.commit()
    return redirect(url_for('main'))


@app.route('/student/<int:student_id>/delete', methods=["GET"])
def delete(student_id):
    user = student.query.filter_by(student_id=student_id)
    user.delete()
    db.session.commit()
    use = enrollments.query.filter_by(estudent_id=student_id)
    use.delete()
    db.session.commit()
    return redirect(url_for('main'))


@app.route('/student/<int:student_id>', methods=["GET"])
def show(student_id):
    students = student.query.filter_by(student_id=student_id)
    enroll = enrollments.query.filter_by(estudent_id=student_id).all()
    courses = []
    for e in enroll:
        courses.append(course.query.filter_by(course_id=e.ecourse_id).one())
    return render_template("show.html", students=students, courses=courses)


if __name__ == "__main__":
    app.debug = True
    app.run(port=8000)
