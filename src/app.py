import os
from flask import Flask, jsonify, request
from models import db, User
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="mysql://root:tupassword@localhost/dgeslab"

Migrate(app, db)
db.init_app(app)
CORS(app)

if __name__=='__main__':
    app.run(port=3100, debug=True)