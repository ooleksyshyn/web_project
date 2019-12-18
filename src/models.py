from src.app import db
import re


def slugify(s):
    pattern = r"[^\w+]"
    return re.sub(pattern, '-', s)


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    employees = db.relationship("Employee")

    def __init__(self, *args, **kwargs):
        super(Department, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)

    def __repr__(self):
        return f"<Department : name={self.name}, id={self.id}>"


class Employee(db.Model):
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))
    name = db.Column(db.String(140))
    surname = db.Column(db.String(140))
    slug = db.Column(db.String(140), primary_key=True)

    def __init__(self, *args, **kwargs):
        super(Employee, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.name + self.surname:
            self.slug = slugify(self.name + " " + self.surname)

    def __repr__(self):
        return f"<Employee : name: {self.name}, surname: {self.surname}, department: {self.department_id}>"
