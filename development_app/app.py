from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Configuration:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://oleksii:1@localhost/test1"


app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)
