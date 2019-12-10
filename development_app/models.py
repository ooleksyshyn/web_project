from development_app.app import db


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    surname = db.Column(db.Integer)

    def __init__(self, *args, **kwargs):
        super(Department, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Department : id={self.id}, name={self.name}>"
