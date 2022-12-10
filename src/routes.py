import os
from flask import Flask, request, jsonify, url_for, Blueprint
# from api.models import db, User
# from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from typing import List

api = Blueprint('api', __name__)

