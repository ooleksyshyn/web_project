from development_app.app import app, db
import development_app.models as md
from development_app.forms import DepartmentForm, EmployeeForm

from flask import render_template, request
from flask import url_for, redirect


from functools import wraps


def search_decorator(f):
    def search():
        q = request.args.get('q', '')
        if q:
            deps = md.Department.query.filter(md.Department.name.contains(q) |
                                              md.Department.slug.contains(q)).all()
            if len(deps):
                return render_template("departments.html", deps=deps, len=len(deps))
            else:
                empls = (db.session.query(md.Employee, md.Department)).join(
                    md.Employee,
                    md.Employee.department_id == md.Department.id).filter(md.Employee.name.contains(q) |
                                                                          md.Employee.surname.contains(q) |
                                                                          md.Employee.slug.contains(q)).all()
                if len(empls):
                    return render_template("employees.html", dep="all departments", employees=empls,
                                           len=len(empls), all=True)
        return None

    @wraps(f)
    def wrapper(*args, **kwargs):
        search_results = search()

        if search_results:
            return search_results

        return f(*args, **kwargs)

    return wrapper


@app.route("/")
@search_decorator
def index():
    return render_template("index.html")


@app.route("/create_department", methods=["POST", "GET"])
@search_decorator
def create_department():

    if request.method == "POST":
        name = request.form["name"]

        try:
            department = md.Department(name=name)
            db.session.add(department)
            db.session.commit()
        except:
            return "Something went wrong!"

        return redirect(url_for("departments"))

    form = DepartmentForm()
    return render_template("create_department.html", form=form)


@app.route("/add_employee/<slug>", methods=["POST", "GET"])
@search_decorator
def add_employee(slug):

    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["name"]
        department_id = md.Department.query.filter(md.Department.slug == slug).first().id
        print(name, surname, department_id)

        try:
            new_employee = md.Employee(name=name, surname=surname, department_id=department_id)

            db.session.add(new_employee)
            db.session.commit()
        except:
            return "Something went wrong!"

        return redirect(url_for("department_detail", slug=slug))

    form = EmployeeForm()
    department = md.Department.query.filter(md.Department.slug == slug).first()
    return render_template("add_employee.html", form=form, dep=department)


@app.route("/dep")
@search_decorator
def departments():

    deps = md.Department.query.all()
    return render_template("departments.html", deps=deps, len=len(deps))


@app.route("/dep/<slug>")
@search_decorator
def department_detail(slug):

    empls = (db.session.query(md.Employee, md.Department)).join(md.Employee,
                                                                md.Employee.department_id == md.Department.id)\
                                                            .filter(md.Department.slug == slug).all()

    if len(empls) > 0:
        department = empls[0][1]
    else:
        department = md.Department.query.filter(md.Department.slug == slug).first()
    return render_template("employees.html", dep=department, employees=empls, len=len(empls), all=False)


@app.route("/employees")
@search_decorator
def employees():

    empls = (db.session.query(md.Employee, md.Department))\
        .join(md.Employee, md.Employee.department_id == md.Department.id).all()

    return render_template("employees.html", dep="all departments", employees=empls, len=len(empls), all=True)
