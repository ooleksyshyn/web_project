from development_app.app import db
import re


def slugify(s):
    pattern = r"[^\w+]"
    return re.sub(pattern, '-', s)


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    surname = db.Column(db.Integer)

    def __init__(self, *args, **kwargs):
        super(Department, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)

    def __repr__(self):
        return f"<Department : id={self.id}, name={self.name}>"
