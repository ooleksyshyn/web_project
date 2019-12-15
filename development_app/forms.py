from wtforms import Form, StringField


class DepartmentForm(Form):
    name = StringField("Name")


class EmployeeForm(Form):
    name = StringField("Name")
    surname = StringField("Surname")
