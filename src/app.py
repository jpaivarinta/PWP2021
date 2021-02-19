from flask import Flask
from flask import request
import json
from flask_sqlalchemy import SQLAlchemy
from database.cryptodb import db

# db.init_app(app=crea)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database//cpdata.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db.create_all()
@app.route("/")
def index():
    return "hello"