from development_app.app import db
import re


def slugify(s):
    pattern = r"[^\w+]"
    return re.sub(pattern, '-', s)


class Department(db.Model):
    name = db.Column(db.String(140))
    slug = db.Column(db.String(140), primary_key=True)

    def __init__(self, *args, **kwargs):
        super(Department, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)

    def __repr__(self):
        return f"<Department : name={self.name}>"


class Employee(db.Model):
    name = db.Column(db.String(140))
    surname = db.Column(db.String(140))
    slug = db.Column(db.String(140), primary_key=True)
    department = db.Column(db.String(140))

    def __init__(self, *args, **kwargs):
        super(Employee, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.name + self.surname:
            self.slug = slugify(self.name + " " + self.surname)

    def __repr__(self):
        return f"<Employee : name: {self.name}, surname: {self.surname}, department: {self.department}>"
