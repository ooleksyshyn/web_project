from flask import Blueprint
from flask import render_template

from development_app.models import Department

departments = Blueprint("departments", __name__, template_folder="templates")


@departments.route("")
def index():
    deps = Department.query.all()
    return render_template("departments_page.html", deps=deps)


@departments.route("/<slug>")
def department_detail(slug):
    department = Department.query.filter(Department.slug == slug).first()
    return render_template("departments_detail.html", dep=department)
