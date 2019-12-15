from flask import render_template
from development_app.app import app, db
import development_app.models as md


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/#")
def first():
    return "Lol kek"


@app.route("/dep")
def departments():
    deps = md.Department.query.all()
    return render_template("departments.html", deps=deps, len=len(deps))


@app.route("/dep/<slug>")
def department_detail(slug):
    empls = (db.session.query(md.Employee, md.Department)).join(md.Employee,
                                                                md.Employee.department_id == md.Department.id)\
                                                            .filter(md.Department.slug == slug).all()

    if len(empls) > 0:
        department = empls[0][1]
    else:
        department = md.Department.query.filter(md.Department.slug == slug)
    return render_template("employees.html", department=department, employees=empls, len=len(empls))


@app.route("/employees")
def employees():
    empls = (db.session.query(md.Employee, md.Department))\
        .join(md.Employee, md.Employee.department_id == md.Department.id).all()

    return render_template("employees.html", dep="all departments", employees=empls, len=len(empls))
