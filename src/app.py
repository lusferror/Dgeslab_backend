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
# from flask_jwt_extended import get_jwt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
# from flask_jwt_extended import set_access_cookies
# from flask_jwt_extended import unset_jwt_cookies

BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# app.config["JWT_COOKIE_SECURE"] = False
# app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["SQLALCHEMY_DATABASE_URI"]="mysql://root:@34.70.198.182/dgeslab"

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

jwt = JWTManager(app)

# @app.after_request
# def refresh_expiring_jwts(response):
#     try:
#         exp_timestamp = get_jwt()["exp"]
#         now = datetime.now(timezone.utc)
#         target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
#         if target_timestamp > exp_timestamp:
#             access_token = create_access_token(identity=get_jwt_identity())
#             set_access_cookies(response, access_token)
#         return response
#     except (RuntimeError, KeyError):
#         # Case where there is not a valid JWT. Just return the original response
#         return response

Migrate(app, db)
db.init_app(app)
CORS(app)

app.register_blueprint(api)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

#Para obtener todos los roles registrados
@app.route("/role", methods=["GET"])
def getRole():

    roles = Role.query.all()
    roles_list = list(map(lambda x: x.serialize(), roles))    
    
    return jsonify(roles_list), 200

#Para obtener todos los usuarios registrados
@app.route("/user", methods=["GET"])
def getUsers():

    users = User.query.all()
    users_list = list(map(lambda x: x.serialize(), users))    
    
    return jsonify(users_list), 200

#Para rgistrar nuevos usuarios supervisores o técnicos
@app.route("/register", methods=["POST"])
def registerUsers():

    body = request.get_json()

    date_object = datetime.datetime.now()

    create_at = date_object    

    if body is None:
        return "The request body is null", 400
    if 'name' not in body:
        return "Add the user name", 400
    if 'second_name' not in body:
        return "Add user second_name", 400
    if 'last_name' not in body:
        return "Add user last_name", 400
    if 'second_last_name' not in body:
        return "Add user second_last_name", 400
    if 'email' not in body:
        return "Add user email", 400
    if 'rut' not in body:
        return "Add user rut", 400
    if 'password' not in body:
        return "Add user password", 400    
    if 'role_id' not in body:
        return "Add user rut", 400                 

    new_user = User(name=body["name"], second_name=body["second_name"], last_name=body["last_name"], second_last_name=body["second_last_name"], email=body["email"], rut=body["rut"], password=body["password"], create_at=create_at, role_id=body["role_id"])

    db.session.add(new_user) 

    db.session.commit()             
    
    return 'User was added', 200

#Para registrar los roles que se asignaran a los users
@app.route("/role", methods=["POST"])
def registerRole():

    body = request.get_json()

    date_object = datetime.date.today()

    create_at = date_object.strftime("%x")    

    if body is None:
        return "The request body is null", 400
    if 'name' not in body:
        return "Add the role name", 400
    if 'description' not in body:
        return "Add role description", 400                    

    new_role = Role(name=body["name"], description=body["description"], create_at=create_at)

    db.session.add(new_role) 

    db.session.commit()             
    
    return 'Role was added', 200

#Para actualizar la información de los roles
@app.route('/role/<int:id>', methods=['PUT'])
def updateRole(id):
    role1 = Role.query.get(id)

    body = request.get_json()
    
    if body is None:
        return "The request body is null", 400
    if 'name' not in body:
        return "Add the role name", 400
    if 'description' not in body:
        return "Add role description", 400

    role1.name = body["name"]
    role1.description = body["description"]
    db.session.commit()            
    
    return 'ok'

#Para actualizar la información de los users
@app.route('/user/<int:id>', methods=['PUT'])
def updateUser(id):

    user1 = User.query.get(id)    

    body = request.get_json()
    
    if body is None:
        return "The request body is null", 400
    if 'name' not in body:
        return "Add the user name", 400
    if 'second_name' not in body:
        return "Add user second_name", 400
    if 'last_name' not in body:
        return "Add user last_name", 400
    if 'second_last_name' not in body:
        return "Add user second_last_name", 400
    if 'email' not in body:
        return "Add user email", 400
    if 'rut' not in body:
        return "Add user rut", 400
    if 'role_id' not in body:
        return "Add user rut", 400

    user1.name = body["name"]
    user1.second_name = body["second_name"]
    user1.last_name = body["last_name"]
    user1.second_last_name = body["second_last_name"]
    user1.email = body["email"]
    user1.rut = body["rut"]
    user1.role_id = body["role_id"]

    db.session.commit()            
    
    return 'ok'

#Para borrar la información de los roles
@app.route('/role/<int:id>', methods=['DELETE'])

def deleteRole(id):
    role1 = Role.query.get(id)
    if role1 == None:
        return "User not found", 404
    db.session.delete(role1)
    db.session.commit()  
    return 'Role deleted'

@app.route('/delete', methods=['DELETE'])
def deleteUser():

    body = request.get_json()        

    if body is None:
        return "The request body is null", 400
    if 'id' not in body:
        return "Add id", 400

    id = body["id"]    

    user1 = User.query.get(id)   

    if user1 == None:
        return "User not found", 404
    db.session.delete(user1)
    db.session.commit()

    return 'User deleted'   

@app.route("/login", methods=["POST"])
def create_token():

    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email:
        return "Missing email", 400
    if not password:
        return "Missing password", 400    

    user = User.query.filter_by(email=email, password=password).first()

    if not user:
        return 'Email or password incorrect', 404

    # response = jsonify({"msg": "login successful"})    
    access_token = create_access_token(identity=user.id)
    # set_access_cookies(response, access_token)

    return jsonify({"token": access_token}), 200

@app.route("/private", methods=["GET"])
@jwt_required()
def protected():

    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)

    role_id = user.role_id
    
    return jsonify({"role_id": role_id}), 200

# @app.route("/logout", methods=["POST"])
# def logout():
#     response = jsonify({"msg": "logout successful"})
#     unset_jwt_cookies(response)
#     return response    

if __name__=='__main__':
    app.run(port=3100, debug=True)