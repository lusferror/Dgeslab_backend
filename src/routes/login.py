# IMPORTED METHODS
from flask import Blueprint , request, jsonify
from flask_jwt_extended import create_access_token
from models import db
import json

# IMPORTED CLASSES MODEL
from models import User , Role 

# ROUTES
login = Blueprint('login', __name__,url_prefix='/login')

@login.route("", methods=["POST"])
def index():
    try:
        user_request= request.json.get("user", None)
        password = request.json.get("password", None)
        user_role = db.session.query(User,Role).join(Role).where(User.user_name==user_request).where(User.password==password).one_or_none()
        if not user_role:
            return jsonify({'msg':'Email or password incorrect',"status":"nok"}), 401
        else:
            user = user_role[0]
            rol = user_role[1]   
        access_token = create_access_token(identity=user.id)
        return jsonify({'status':'ok',"token": access_token,"rol":user.role_id,"user":user.name+" "+user.last_name,"id_user":user.id, "rol_name":rol.name}), 200

    except Exception as e:
        print("Error: ",e)
        return jsonify({"message":str(e)}), 500