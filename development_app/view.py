from flask import render_template
from development_app.app import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/#')
def first():
    return "Lol kek"
