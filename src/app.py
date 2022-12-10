import os
import datetime
from flask import Flask, jsonify, request
from models import db, User, Role
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from utils import APIException, generate_sitemap #Averiguar como importar esto
BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="mysql://root:@34.70.198.182/dgeslab"

Migrate(app, db)
db.init_app(app)
CORS(app)

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

    date_object = datetime.date.today()

    create_at = date_object.strftime("%x")    

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

    new_user = User(name=body["name"], second_name=body["second_name"], last_name=body["last_name"], second_last_name=body["second_last_name"], email=body["email"], rut=body["rut"], create_at=create_at, role_id=body["role_id"])

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
        return "Add therole name", 400
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

#Tengo que averiguar como importar el APIException
# @app.route('/role/<int:id>', methods=['DELETE'])
# def deleteRole(id):
#     user1 = Role.query.get(id)
#     if user1 == None:
#         raise APIException('User not found', status_code=404)
#     db.session.delete(user1)
#     db.session.commit()  
#     return 'User deleted'
    

# if __name__=='__main__':
#     app.run(port=3100, debug=True)