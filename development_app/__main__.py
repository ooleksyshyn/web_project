from development_app.app import app
import development_app.view

from development_app.departments import departments

app.register_blueprint(departments, url_prefix="/dep")


if __name__ == "__main__":
    app.run(debug=True)
