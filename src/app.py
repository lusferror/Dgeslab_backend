import os
import datetime
from utils import generate_sitemap, APIException
from flask import Flask, jsonify, request
from models import db, User, Role
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from routes.routes import api
from routes.login import login

#CONFIG
BASEDIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="mysql://root:password@localhost:3306/dgeslab"
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)
Migrate(app, db)
db.init_app(app)
CORS(app)

#ROUTES
app.register_blueprint(api)
app.register_blueprint(login)

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
# @jwt_required()
def getUsers():
    try:
        users = User.query.all()
        print(users)
        users_list = list(map(lambda x: x.serialize(), users))    
        print(users_list)
        return jsonify(users_list), 200
    except Exception as e:
        print("error: ", e)
        return jsonify({"error":"error"}),422

#Para rgistrar nuevos usuarios supervisores o técnicos
@app.route("/register", methods=["POST"])
def registerUsers():
    try:
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
        
        return jsonify({"msg":'User was added'}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg":"error"}),500

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


@app.route("/private", methods=["GET"])
@jwt_required()
def protected():

    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)

    role_id = user.role_id
    user_name = user.name
    
    return jsonify({"role_id": role_id, "user_name": user_name+" "+user.last_name}), 200
    

if __name__=='__main__':
    app.run(host="192.168.0.6",port=3100, debug=True)