import os
import datetime
from datetime import timezone
from utils import generate_sitemap, APIException
from datetime import timedelta
from flask import Flask, jsonify, request
from models import db, User, Role
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from routes import api

from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from routes import api

BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="mysql://root:@34.70.198.182/dgeslab"

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!


jwt = JWTManager(app)


Migrate(app, db)
db.init_app(app)
CORS(app)

app.register_blueprint(api)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

if __name__=='__main__':
    app.run(port=3100, debug=True)