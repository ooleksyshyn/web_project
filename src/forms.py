from wtforms import Form, StringField, IntegerField, DateField


class DepartmentForm(Form):
    name = StringField("Name")


class EmployeeForm(Form):
    name = StringField("Name")
    surname = StringField("Surname")
    salary = IntegerField("Salary")
    birth_date = DateField("Date of birth")


class SearchForm(Form):
    first_date = DateField("Beginning of period")
    last_date = DateField("End of period")
