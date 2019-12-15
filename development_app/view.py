from flask import render_template
from development_app.app import app
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
    department = md.Department.query.filter(md.Department.slug == slug).first()
    empls = md.Employee.query.filter(md.Employee.department == department.name).all()
    return render_template("employees.html", dep=department.name, employees=empls, len=len(empls))


@app.route("/employees")
def employees():
    empls = md.Employee.query.all()
    return render_template("employees.html", dep="all departments", employees=empls, len=len(empls))
