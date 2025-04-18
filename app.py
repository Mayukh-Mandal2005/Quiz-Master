from flask import Flask
from application.database import db
from application.models import User
app = None

def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecretkey123"
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quizmaster.sqlite3"
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()
from application.controllers import *

def admin_setup():
    with app.app_context():
        db.create_all()

        admin = User.query.filter_by(username="admin@user.com").first()
        if not admin:
            admin = User(full_name="AdminUser", qualification="Owner", dob="2000-01-01", username="admin@user.com",password="1234", role="admin")
            db.session.add(admin)
            db.session.commit()

if __name__ == "__main__":
    admin_setup()
    app.run()
