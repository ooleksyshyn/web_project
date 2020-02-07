from src.app import db, app
from src.models import Department, Employee
from RESTful.restful import api

import unittest
import requests


# app.run(debug=True)


class DataBaseTest(unittest.TestCase):
    def setUp(self):

        Department.query.filter(Department.id < 0).delete()
        db.session.commit()

        return super().setUp()

    def test_database(self):
        department1 = Department(name="Test department 1", id=-1)
        department2 = Department(name="Test department 2", id=-2)
        department3 = Department(name="Test department 3", id=-3)

        db.session.add(department1)
        db.session.add(department2)
        db.session.add(department3)

        db.session.commit()

        self.assertEqual(
            Department.query.filter(Department.id == -1).first().name, "Test department 1"
        )

        self.assertEqual(
            Department.query.filter(Department.id == -2).first().name, "Test department 2"
        )

        self.assertEqual(
            Department.query.filter(Department.id == -3).first().name, "Test department 3"
        )

        employee1 = Employee(name="Employee 1", surname="Test", department_id=-1, salary=5000, birth_date="2000-01-01")
        employee2 = Employee(name="Employee 2", surname="Test", department_id=-1, salary=7000, birth_date="2000-02-04")
        employee3 = Employee(name="Employee 3", surname="Test", department_id=-2, salary=8000, birth_date="2001-02-04")
        employee4 = Employee(name="Employee 4", surname="Test", department_id=-3, salary=7500, birth_date="1999-12-04")

        db.session.add(employee1)
        db.session.add(employee2)
        db.session.add(employee3)
        db.session.add(employee4)
        db.session.commit()

        self.assertEqual(
            len(Employee.query.filter(Employee.department_id == -1).all()), 2
        )

        self.assertEqual(
            Employee.query.filter(Employee.department_id == -1).first(), employee1
        )

        self.assertEqual(
            len(Employee.query.filter(Employee.department_id == -2).all()), 1
        )

        self.assertEqual(
            Employee.query.filter(Employee.department_id == -2).first(), employee3
        )

        self.assertEqual(
            len(Employee.query.filter(Employee.department_id == -3).all()), 1
        )

        self.assertEqual(
            Employee.query.filter(Employee.department_id == -3).first(), employee4
        )

        employee5 = Employee(name="Employee 5", surname="Test", department_id=-3, salary=9500, birth_date="1998-12-04")

        db.session.add(employee5)
        db.session.commit()

        self.assertEqual(
            len(Employee.query.filter(Employee.department_id == -3).all()), 2
        )

        Department.query.filter(Department.id == -2).delete()
        db.session.commit()

        self.assertEqual(
            len(Department.query.filter(Department.id == -2).all()), 0
        )

        self.assertEqual(
            len(Employee.query.filter(Employee.department_id == -2).all()), 0
        )

        Department.query.filter(Department.id < 0).delete()
        db.session.commit()

        rest = Employee.query.filter(Employee.department_id < 0).all()

        self.assertEqual(len(rest), 0)


class ApiTest(unittest.TestCase):
    def test_api(self):
        pass
        # r = requests.get('http://localhost:5000/')

        # self.assertEqual(r.json(), {"Hello": "World"})
        # self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
