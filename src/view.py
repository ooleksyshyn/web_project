from src.app import app, db
import src.models as md
from src.forms import DepartmentForm, EmployeeForm, SearchForm

from flask import render_template, request
from flask import url_for, redirect
from sqlalchemy.sql import func


from functools import wraps


def search_decorator(f):
    def search():
        q = request.args.get('q', '')
        if q:
            deps = md.Department.query.filter(md.Department.name.contains(q) or
                                              md.Department.slug.contains(q)).all()
            if len(deps):
                return render_template("departments.html", deps=deps, len=len(deps))
            else:
                empls = (db.session.query(md.Employee, md.Department)).join(
                    md.Department.employees).filter(md.Employee.name.contains(q) or
                                                    md.Employee.surname.contains(q)).all()
                if len(empls):
                    return render_template("employees.html", dep="all departments (searched)", employees=empls,
                                           len=len(empls), all=True, form=SearchForm())
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


@app.route("/search_results", methods=["POST"])
def search_employees():
    first_date = request.form["first_date"]
    last_date = request.form["last_date"]

    empls = db.session.query(md.Employee, md.Department).join(md.Department.employees).filter(
        last_date >= func.date(md.Employee.birth_date), md.Employee.birth_date >= first_date).all()

    return render_template("employees.html", dep="all departments (searched)", employees=empls,
                           len=len(empls), all=True, form=SearchForm())


@app.route("/create_department", methods=["POST", "GET"])
@search_decorator
def create_department():
    print("WTF???")

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


@app.route("/edit_department/<slug>", methods=["POST", "GET"])
@search_decorator
def edit_department(slug):
    department = md.Department.query.filter(md.Department.slug == slug).first()
    print(department.name, slug)
    if request.method == "POST":
        form = DepartmentForm(formdata=request.form, onj=department)
        form.populate_obj(department)

        db.session.commit()

        return redirect(url_for("departments"))

    form = DepartmentForm(obj=department)

    return render_template("edit_department.html", form=form, department=department)


@app.route("/add_employee/<slug>", methods=["POST", "GET"])
@search_decorator
def add_employee(slug):

    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        salary = request.form["salary"]
        birth_date = request.form["birth_date"]
        department_id = md.Department.query.filter(md.Department.slug == slug).first().id

        try:
            new_employee = md.Employee(name=name, surname=surname, department_id=department_id,
                                       salary=salary, birth_date=birth_date)

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

    empls = (db.session.query(md.Employee, md.Department)).join(md.Department.employees)\
        .filter(md.Department.slug == slug)

    average_salary = 0
    for employee in empls.all():
        average_salary += employee[0].salary
    if len(empls.all()):
        average_salary = average_salary/len(empls.all())

    if len(empls.all()) > 0:
        department = empls[0][1]
    else:
        department = md.Department.query.filter(md.Department.slug == slug).first()
    return render_template("employees.html", dep=department, employees=empls.all(),
                           len=len(empls.all()), all=False, average_salary=average_salary, form=SearchForm())


@app.route("/employees")
@search_decorator
def employees():

    empls = (db.session.query(md.Employee, md.Department)).join(md.Department.employees).all()

    return render_template("employees.html", dep="all departments", employees=empls, len=len(empls),
                           all=True, form=SearchForm())


@app.route("/employee/<slug>")
@search_decorator
def employee_detail(slug):
    employee = md.Employee.query.filter(md.Employee.slug == slug).first()

    return render_template("employee.html", employee=employee)
