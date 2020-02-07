from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_restful import Api


class Configuration:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://oleksii:1@localhost/testdb"


app = Flask(__name__, template_folder="../templates")
app.config.from_object(Configuration)

api = Api(app)

db = SQLAlchemy(app)


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)
