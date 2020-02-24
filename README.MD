My web project -- website on Flask, Python

Description: the website contains information about departnments and its employees.
All the data is stored in local database.
You can add new department or employee to existing department.
There is also search function: you can search for employees or departments by their names.

The application also has a RESTful API, which you can use to get, delete or change information using http queries.
 
 To start project:
 * download code or clone repository
 * download Python and MySQL

 Execute following commands in terminal:
 - Create database: 
   * mysql -e 'CREATE DATABASE `testdb`;'
   * mysql -e 'CREATE USER oleksii@localhost IDENTIFIED BY "1";'
   * mysql -e 'GRANT ALL PRIVILEGES ON testdb.* TO oleksii@localhost;'
   * mysql testdb < mysql/main_db_bootstrap.sql
 - Get dependencies:
   * pip3 install -r requirements.txt
 - Run code:
   * python3 -m src (website)
   * python3 -m RESTful (API)
 
 
 Technologies I used:
 * backend: Python (Flask)
 * frontend: HTML/CSS + Jinja2
 * database: MySQL + SQLAlchemy and my own ORM for better integration with Python
 * continuous integration: Travis CI