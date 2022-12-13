import os
from flask import Flask, jsonify, request
from models import db, User
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from routes import api
BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="mysql://root:@34.70.198.182/dgeslab"

Migrate(app, db)
db.init_app(app)
CORS(app)

app.register_blueprint(api)


if __name__=='__main__':
    app.run(port=3100, debug=True)