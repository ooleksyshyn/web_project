from src.app import db
import re


def slugify(s):
    pattern = r"[^\w+]"
    return re.sub(pattern, '-', s)


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    slug = db.Column(db.String(255))
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
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))
    name = db.Column(db.String(250))
    surname = db.Column(db.String(250))
    slug = db.Column(db.String(250))
    salary = db.Column(db.Integer)
    birth_date = db.Column(db.Date)

    def __init__(self, *args, **kwargs):
        super(Employee, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name + self.surname)

    def __repr__(self):
        return f"<Employee : name: {self.name}, surname: {self.surname}, department: {self.department_id}>"
