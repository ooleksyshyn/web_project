from development_app.app import manager, migrate, db, app

if __name__ == "__main__":
    manager.run()

# python3 manage.py db migrate
# python3 manage.py db update
