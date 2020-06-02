from src.app import api, db
from src.models import Employee, Department
from flask_restful import Resource, reqparse
from sqlalchemy.sql import func
from src.models import slugify


class Index(Resource):
    def get(self):
        return {"Hello": "World"}, 200


class Search(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("first_date")
        parser.add_argument("last_date")

        args = parser.parse_args()

        first_date = args["first_date"]
        last_date = args["last_date"]

        res = {employee.name + " " + employee.surname + " " + str(employee.birth_date): department.name
               for employee, department in db.session.query(Employee, Department).join(Department.employees).filter(
                last_date >= func.date(Employee.birth_date), Employee.birth_date >= first_date).all()}
        return res, 201


class Departments(Resource):
    def get(self):
        res = {department.name: department.id for department in Department.query.all()}

        return res, 200


class AddDepartment(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")

        name = parser.parse_args()["name"]

        try:
            department = Department(name=name)
            db.session.add(department)
            db.session.commit()
        except:
            return 404

        return {department.name: department.id}, name


class EditDepartment(Resource):
    def post(self, slug):
        parser = reqparse.RequestParser()
        parser.add_argument("name")

        new_name = parser.parse_args()["name"]
        if not new_name:
            return 200

        try:
            Department.query.filter(Department.slug == slug).update(values={"name": new_name,
                                                                            "slug": slugify(new_name)})
            db.session.commit()
        except:
            return 404

        return {}, 201


class Employees(Resource):
    def get(self):
        res = {employee.name + " " + employee.surname: department.name
               for employee, department in db.session.query(Employee, Department).join(Department.employees).all()}

        return res, 200


class EmployeeDetails(Resource):
    def get(self, slug):
        try:
            employee, department = db.session.query(Employee, Department).join(
                                                            Department.employees).filter(Employee.slug == slug).first()

        except:
            return 404

        return {
            "id": employee.id,
            "name": employee.name,
            "surname": employee.surname,
            "salary": employee.salary,
            "birth_date": str(employee.birth_date),
            "slug": employee.slug,
            "department": department.name
        }, 200


class AddEmployee(Resource):
    def post(self, slug):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("surname")
        parser.add_argument("salary")
        parser.add_argument("birth_date")

        args = parser.parse_args()

        try:
            department = Department.query.filter(Department.slug == slug).first()
            new_employee = Employee(name=args["name"], surname=args["surname"], department_id=department.id,
                                    salary=args["salary"], birth_date=args["birth_date"])
            db.session.add(new_employee)
            db.session.commit()
        except:
            return 404

        return {
            "id": new_employee.id,
            "name": new_employee.name,
            "surname": new_employee.surname,
            "slug": new_employee.slug,
            "salary": new_employee.salary,
            "birth_date": str(new_employee.birth_date),
            "department": department.name,
            "department_id": department.id
        }, 201


class EditEmployee(Resource):
    def post(self, slug):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("surname")
        parser.add_argument("salary")
        parser.add_argument("birth_date")

        args = parser.parse_args()

        employee = Employee.query.filter(Employee.slug == slug).first()

        if not employee:
            return 404

        if not args["name"]:
            args["name"] = employee.name

        if not args["surname"]:
            args["surname"] = employee.surname

        args["slug"] = slugify(args["name"] + " " + args["surname"])

        new_args = {k: v for k, v in args.items() if v is not None}

        try:
            Employee.query.filter(Employee.slug == slug).update(values=new_args)
            db.session.commit()
        except:
            return 404

        return new_args, 201


class DepartmentEmployees(Resource):
    def get(self, slug):
        res = {employee.name + " " + employee.surname: department.name
               for employee, department in db.session.query(Employee, Department).join(Department.employees).filter(
                                                                                            Department.slug == slug)}
        return res, 200


class DeleteDepartment(Resource):
    def delete(self, slug):
        employees = db.session.query(Employee, Department).join(
            Department.employees).filter(Department.slug == slug).all()

        res = {}

        print(employees)

        if employees:
            res = [{
                "id": employee[0].id,
                "name": employee[0].name,
                "surname": employee[0].surname,
                "salary": employee[0].salary,
                "birth_date": str(employee[0].birth_date),
                "slug": employee[0].slug,
                "department": employee[1].name
                } for employee in employees]

        Department.query.filter(Department.slug == slug).delete()
        db.session.commit()

        if employees:
            return res, 201
        else:
            return res, 200


class DeleteEmployee(Resource):
    def delete(self, slug):
        employee, department = db.session.query(Employee, Department).join(
            Department.employees).filter(Employee.slug == slug).first()

        Employee.query.filter(Employee.slug == slug).delete()
        db.session.commit()

        if employee:
            return {
                    "id": employee.id,
                    "name": employee.name,
                    "surname": employee.surname,
                    "slug": employee.slug,
                    "salary": employee.salary,
                    "birth_date": str(employee.birth_date),
                    "department": department.name,
                    "department_id": department.id
                }, 201
        else:
            return {}, 200


api.add_resource(Index, "/")
api.add_resource(Departments, "/dep")
api.add_resource(Employees, "/employees")
api.add_resource(Search, "/search_results")
api.add_resource(AddDepartment, "/create_department")
api.add_resource(EditDepartment, "/edit_department/<slug>")
api.add_resource(DepartmentEmployees, "/dep/<slug>")
api.add_resource(AddEmployee, "/add_employee/<slug>")
api.add_resource(EmployeeDetails, "/employee/<slug>")
api.add_resource(EditEmployee, "/edit_employee/<slug>")
api.add_resource(DeleteDepartment, "/delete_department/<slug>")
api.add_resource(DeleteEmployee, "/delete_employee/<slug>")
