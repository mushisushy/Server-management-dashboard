import os
import time

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "potato"
    if os.getenv("DOCKER_ENV") == "true":
        DB_USER = os.getenv("DB_USER", "myuser")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "mypassword")
        DB_HOST = os.getenv("DB_HOST", "db")
        DB_NAME = os.getenv("DB_NAME", "mydatabase")

        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
        )
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"

    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    create_database(app)

    from .views import main_page

    app.register_blueprint(main_page)

    create_database(app)

    return app


def create_database(app):
    with app.app_context():
        for i in range(10):  # try up to 10 times
            try:
                db.create_all()
                print("✅ Database tables created.")
                break
            except OperationalError:
                print(f"⏳ Waiting for DB... attempt {i+1}/10")
                time.sleep(3)
        else:
            print("❌ Could not connect to DB after several tries.")
