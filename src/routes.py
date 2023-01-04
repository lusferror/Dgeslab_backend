from flask import Flask, request, jsonify, url_for, Blueprint
from models import db, Salida, Asignacion, Revision_movil, Equipos,Entrada,Series, User, Role
import json
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

api = Blueprint('api', __name__)

@api.route('/', methods = ['GET'])
def home():
    return 'hello world 2'

#Para obtener todos los roles registrados
@api.route("/role", methods=["GET"])
def getRole():

    roles = Role.query.all()
    roles_list = list(map(lambda x: x.serialize(), roles))    
    
    return jsonify(roles_list), 200

#Para obtener todos los usuarios registrados
@api.route("/user", methods=["GET"])
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
@api.route("/register", methods=["POST"])
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
@api.route("/role", methods=["POST"])
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
@api.route('/role/<int:id>', methods=['PUT'])
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
@api.route('/user/<int:id>', methods=['PUT'])
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
@api.route('/role/<int:id>', methods=['DELETE'])

def deleteRole(id):
    role1 = Role.query.get(id)
    if role1 == None:
        return "User not found", 404
    db.session.delete(role1)
    db.session.commit()  
    return 'Role deleted'

@api.route('/delete', methods=['DELETE'])
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

@api.route("/login", methods=["POST"])
def create_token():

    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email:
        return "Missing email", 400
    if not password:
        return "Missing password", 400    

    user = User.query.filter_by(email=email, password=password).first()
    rol=Role.query.filter_by(id=user.role_id).first()
    if not user:
        return jsonify({'msg':'Email or password incorrect',"status":"nok"}), 401
        
    access_token = create_access_token(identity=user.id)
    
    return jsonify({'status':'ok',"token": access_token,"rol":user.role_id,"user":user.name+" "+user.last_name,"id_user":user.id, "rol_name":rol.name}), 200

@api.route("/private", methods=["GET"])
@jwt_required()
def protected():

    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)

    role_id = user.role_id
    user_name = user.name
    
    return jsonify({"role_id": role_id, "user_name": user_name+" "+user.last_name}), 200

@api.route('/salida', methods = ['GET'])
def get_salida():
    try:
        salidas = db.session.query(Salida).all()
        list_sal = list()
        for salida in salidas:
            print('salida-->>', salida.serie)
            fecha_embalaje = salida.fecha_embalaje.strftime('%d/%m/%Y')            
            fecha_empacado = salida.fecha_empacado.strftime('%d/%m/%Y')            
            fecha_documento = salida.fecha_documento.strftime('%d/%m/%Y')            
            f_despacho_fisico = salida.f_despacho_fisico.strftime('%d/%m/%Y')            
            list_sal.append(
                {
                    "id": salida.id, 
                    "serie": salida.serie, 
                    "material": salida.material, 
                    "denominacion": salida.denominacion,
                    "empacado": salida.empacado, 
                    "fecha_empacado": fecha_empacado,
                    "responsable_id": salida.responsable_id,
                    "tipo_caja": salida.tipo_caja,
                    "nro_caja": salida.nro_caja,
                    "fecha_embalaje": fecha_embalaje,
                    "documento": salida.documento, 
                    "guia_despacho": salida.guia_despacho, 
                    "b_origen_salida": salida.b_origen_salida, 
                    "b_destino_salida": salida.b_destino_salida, 
                    "fecha_documento": fecha_documento, 
                    "f_despacho_fisico": f_despacho_fisico,
                    "revision_movil_id": salida.revision_movil_id
                })
        print(list_sal)
        return jsonify({"salida": list_sal}), 200
    except Exception as e:
        mens=str(e)
        error = {'Error':mens}
        print('Error: ', error)
        return jsonify({"message":error}), 500

#Para borrar tabla salida
@api.route('/salida/<int:serie>', methods=['DELETE'])
def deleteSalida(serie):
    salida = Salida.query.filter_by(serie=serie).first()
    if salida == None:
        return "User not found", 404
    db.session.delete(salida)
    db.session.commit()  
    return jsonify({"message":"salida delete success"}), 200


# PUT solo un registro
@api.route('/salida/<int:id>', methods = ['PUT'])
def update_salida(id):
    try:
        salida = db.session.query(Salida).get(id)
        if salida is not None:
            salida.documento = request.json.get("documento")
            salida.serie = request.json.get("serie")

            strFecha = request.json.get("fecha_documento")
            fecha = datetime.datetime.strptime(strFecha, '%d/%m/%Y').date()
            salida.fechadocumento = fecha

            salida.b_origen_salida = request.json.get("b_origen_salida")
            salida.b_destino_salida = request.json.get("b_destino_salida")
            salida.guia_despacho = request.json.get("guia_despacho")

            strFecha = request.json.get("f_despacho_fisico")
            fecha = datetime.datetime.strptime(strFecha, '%d/%m/%Y').date()
            salida.f_despacho_fisico = fecha

            db.session.commit()
            return jsonify(salida.serialize()), 200
        else:
            return jsonify({"message":"salida not found"}), 404
    except Exception as e:
        mens=str(e)
        error = {'Error':mens}
        print('Error: ', error)
        return jsonify({"message":error}), 500


# POST solo un registro
@api.route('/salida', methods = ['POST'])
def create_salida():
    try:
        salida = Salida()
        salida.serie = request.json.get("serie")
        salida.material = request.json.get("material")
        salida.denominacion = request.json.get("denominacion")
        salida.empacado = request.json.get("empacado")

        strFecha = request.json.get("fecha_empacado")
        fecha = datetime.datetime.strptime(strFecha, '%d/%m/%Y').date()
        salida.fecha_empacado = fecha

        salida.responsable_id = request.json.get("responsable_id")
        salida.tipo_caja = request.json.get("tipo_caja")
        salida.nro_caja = request.json.get("nro_caja")

        strFecha = request.json.get("fecha_embalaje")
        fecha = datetime.datetime.strptime(strFecha, '%d/%m/%Y').date()
        salida.fecha_embalaje = fecha

        salida.documento = request.json.get("documento")
        salida.guia_despacho = request.json.get("guia_despacho")
        salida.b_origen_salida = request.json.get("b_origen_salida")
        salida.b_destino_salida = request.json.get("b_destino_salida")

        strFecha = request.json.get("fecha_documento")
        fecha = datetime.datetime.strptime(strFecha, '%d/%m/%Y').date()
        salida.fecha_documento = fecha

        strFecha = request.json.get("f_despacho_fisico")
        fecha = datetime.datetime.strptime(strFecha, '%d/%m/%Y').date()
        salida.f_despacho_fisico = fecha

        salida.revision_movil_id = request.json.get("revision_movil_id")
        db.session().add(salida)
        db.session().commit()
        print('salida: ', salida)
        return jsonify(salida.serialize()), 201
    except Exception as e:
        mens=str(e)
        error = {'Error':mens}
        print('Error: ', error)
        return jsonify({"message":error}), 500

@api.route("/asignacionUsers", methods=["GET"])
@jwt_required()
def getAsignacion():
    try:
        users=db.engine.connect().execute(db.select(User))
        list_user=[]
        for user in users:
            list_user.append(user._asdict())
        return jsonify({"msg":"ok","list_users":list_user}),200
    except Exception as e:
        print("Error: ",e)
        return jsonify({"msg":"nok"}),400

@api.route('/serieAsignacion',methods=['POST'])
@jwt_required()
def serie_asignacion():
    try:
        body=request.json.get("serie")
        serie=Equipos.query.filter_by(serie=body).first()
        print(serie)
        if serie!=None:
            return jsonify({"msg":"ok"}),200
        else:
            return jsonify({"msg":"nok"}),200
    except Exception as e:
        print(e)
        return jsonify({"msg":"nok"}),400

@api.route('/asignacionGuardar',methods=['POST'])
@jwt_required()
def asignacion_guardar():
    try:
        series=request.json.get("lista")
        registro=(db.insert(Asignacion,series))
        asignacion=db.session.execute(registro)
        db.session.commit()
        return jsonify({"msg":"ok"})
    except Exception as e:
        print(e)
        return jsonify({"msg":"nok"}),404

@api.route('/listaAprobacion', methods=['POST'])
@jwt_required() 
def lista_aprobacion():
    try:
        rol=request.json.get("rol")
        id=request.json.get("id")
        lista=[]
        if rol=="1":
            aprobacion=db.engine.connect().execute(db.select(Asignacion))
            for record in aprobacion:
                lista.append(record._asdict())
            return jsonify({"msg":"ok","lista":lista}),200
        else:
            consulta=(db.select(Asignacion).where(Asignacion.tecnico_id==int(id)))
            aprobacion=db.engine.connect().execute(consulta)
            print(consulta)
            for record in aprobacion:
                lista.append(record._asdict())
            print(lista)
            return jsonify({"msg":"ok","lista":lista}),200
    except Exception as e:
        print("EL ERROR: ",e)
        return jsonify({"msg":"nok"}),404

@api.route('/aprobarAsignacion',methods=['PUT'])
def aprobar_asignacion():
    try:
        registros=request.json.get("lista")
        asignacion=(db.update(Asignacion).where(Asignacion.id==db.bindparam("b_id")).values(check=db.bindparam("check"),estado=db.bindparam("estado")))
        execute=db.session.execute(asignacion,registros)
        db.session.commit()
        return jsonify({"msg":"ok"})
    except Exception as e:
        print(e)
        return jsonify({"msg":"nok"})


@api.route("/datos_movil_basico", methods=['POST'])
def datos_movil_basico():
    try:
        serie=request.json.get("serie")
        datos={}
        execute=db.engine.connect().execute("select series.id,series.serie, datos_basicos.denominacion,datos_basicos.material from (select serie, revision.id from asignacion join (select id,id_asignacion from revision_movil)as revision on asignacion.id=revision.id_asignacion) as series join (select id,serie,denominacion,material from entrada join (select max(id) as max from entrada group by serie order by max asc) as diferentes on entrada.id=diferentes.max) as datos_basicos on series.serie=datos_basicos.serie where datos_basicos.serie="+serie+";")
        for row in execute:
            print(row._asdict())
            datos=row._asdict()
        if datos=={}:
            return jsonify({"msg":"nok"})
        else:
            return jsonify({"msg":"ok","datos":datos})
    except Exception as e:
        print(e)
        return jsonify({"msg":"error"})

@api.route("/datos_revision_movil/<int:serie>", methods=["GET"])
# @jwt_required()
def get_DatosRevisionMovil(serie):
    connection = db.engine.connect()
    strSerie = str(serie)
    query = "select asignacion.serie, datos_basicos.denominacion,datos_basicos.material from asignacion join (select serie,denominacion,material from entrada join (select max(id) as m from entrada group by serie order by m asc) as id_entrada on id_entrada.m=entrada.id) as datos_basicos on asignacion.serie=datos_basicos.serie where asignacion.serie = %s" % strSerie
    result = connection.execute(query)        
    for equipo in result:
        res = equipo._asdict()
    print('result:', res)
    return jsonify({"result":res})
    # strSerie = str(serie)
    # lista = list()
    # sql = " :p"
    # equipo = db.session.execute(sql, p=strSerie)
    # print('Datos: ', equipo)


@api.route("/revision_movil", methods=["GET"])
# @jwt_required()
def getRevisionMovil():
    # try:
    #     revision = Revision_movil.query.all()
    #     revision_list = list(map(lambda x: x.serialize(), revision))    
        
    #     return jsonify(revision_list)
    # except Exception as e:
    #     print(e)
    #     return jsonify({"msg":"error"})
    try:
        # revisiones = db.session.query(Revision_movil).all()
        # query = (db.select(Revision_movil).join(Revision_movil.id_asignacion))
        # revisiones = db.session.scalars(query).all()
        # print('revisiones-->>', revisiones)
        lista = list()
        equipos = db.session.execute('select series.id,series.serie, datos_basicos.denominacion,datos_basicos.material from (select serie, revision.id from asignacion join (select id,id_asignacion from revision_movil)as revision on asignacion.id=revision.id_asignacion) as series join (select id,serie,denominacion,material from entrada join (select max(id) as max from entrada group by serie order by max asc) as diferentes on entrada.id=diferentes.max) as datos_basicos on series.serie=datos_basicos.serie;')
        for equipo in equipos:
            lista.append(equipo._asdict())


        list_rev = list()
        for r, a, e, u in db.session.query(Revision_movil, Asignacion, Equipos, User).filter(Revision_movil.id_asignacion == Asignacion.id).filter(Asignacion.serie == Equipos.serie).filter(Asignacion.tecnico_id == User.id).all():
        # for revision in revisiones:
            print('salida-->>', r.id)
            # fecha_embalaje = revision.fecha_embalaje.strftime('%d/%m/%Y')            
            # fecha_empacado = revision.fecha_empacado.strftime('%d/%m/%Y')            
            # fecha_documento = revision.fecha_documento.strftime('%d/%m/%Y')            
            # f_despacho_fisico = revision.f_despacho_fisico.strftime('%d/%m/%Y')            
            list_rev.append(
                {
                    # "id": r.id, 
                    "encendido": r.encendido, 
                    "frontal": r.frontal, 
                    "frontal_r": r.frontal_r,
                    "trasera": r.trasera, 
                    "trasera_r": r.trasera_r,
                    "superior": r.superior,
                    "superior_r": r.superior_r,
                    "inferior": r.inferior,
                    "inferior_r": r.inferior_r,
                    "izquierdo": r.izquierdo, 
                    "izquierdo_r": r.izquierdo_r, 
                    "derecho": r.derecho, 
                    "derecho_r": r.derecho_r,
                    "puntaje_cos": r.puntaje_cos, 
                    "pantalla": r.pantalla,
                    "tactil": r.tactil,
                    "botones": r.botones,
                    "mic": r.mic,
                    "audio": r.audio,
                    "bateria": r.bateria,
                    "conector_c": r.conector_c,
                    "bluetooth": r.bluetooth,
                    "wifi": r.wifi,
                    "zona_w": r.zona_w,
                    "nfc": r.nfc,
                    "conector_a": r.conector_a,
                    "porta_sim": r.porta_sim,
                    "filtracion": r.filtracion,
                    "llamadas_e": r.llamadas_e,
                    "llamadas_r": r.llamadas_r,
                    "msj_e": r.msj_e,
                    "msj_r": r.msj_r,
                    "foto_f": r.foto_f,
                    "foto_t": r.foto_t,
                    "video_f": r.video_f,
                    "video_t": r.video_t,
                    "sen_proximidad": r.sen_proximidad,
                    "vibrador": r.vibrador,
                    "puntaje_tec": r.puntaje_tec,
                    "bloqueo": r.bloqueo,
                    "act_sw": r.act_sw,
                    "restauracion": r.restauracion,
                    "fecha_rev": r.fecha_rev,
                    "clasificacion": r.clasificacion,
                    "ert": r.ert,
                    "observaciones": r.observaciones,
                    "id_asignacion": r.id_asignacion,

                    "serie": a.serie,
                    "fecha_asignacion": a.fecha_asignacion,
                    # "tecnico_id": a.tecnico_id,
                    # "check": a.check,
                    # "estado": a.estado,

                    "material": e.material,
                    # "serieEquipo": e.serie,
                    "denominacion": e.denominacion,
                    "nom_tecnico": u.name  + " " + u.last_name
                })
        print(list_rev)

        for listaRev in list_rev:
            for lista_id in lista:
                if(listaRev["serie"] == lista_id["serie"]):
                    listaRev["material"] = lista_id["material"]
                    listaRev["denominacion"] = lista_id["denominacion"]

        return jsonify({"status":"ok","salida": list_rev}), 200
    except Exception as e:
        mens=str(e)
        error = {'Error':mens}
        print('Error: ', error)
        return jsonify({"message":error}), 500


@api.route("/revision_movil", methods=["POST"])
def register_RevisionMovil():
    id  =  request.json.get("id",None)
    serie = request.json.get("serie",None)
    material = request.json.get("material",None)
    denominacion = request.json.get("denominacion",None)
    tecnico_id=request.json.get("tecnico_id", None)

    # fecha=request.json.get("fecha", None) # --- fecha
    strFecha = request.json.get("fecha", None)
    print('FECHA:', strFecha)
    fecha = datetime.datetime.strptime(strFecha, '%d/%m/%Y').date()
    print('FECHA2:', fecha)

    encendido = request.json.get("encendido", None)
    #----revision cosmetica----
    frontal= request.json.get("frontal", None) 
    frontal_r= request.json.get("frontal_r", None) 
    trasera= request.json.get("trasera", None) 
    trasera_r= request.json.get("trasera_r", None) 
    superior= request.json.get("superior", None) 
    superior_r= request.json.get("superior_r", None) 
    inferior= request.json.get("inferior", None) 
    inferior_r= request.json.get("inferior_r", None) 
    izquierdo= request.json.get("izquierdo", None) 
    izquierdo_r= request.json.get("izquierdo_r", None) 
    derecho= request.json.get("derecho", None) 
    derecho_r= request.json.get("derecho_r", None) 
    puntaje_cos= request.json.get("puntaje_cos", None) 
     #---revision técnica----
    pantalla= request.json.get("pantalla", None) 
    tactil = request.json.get("tactil", None) 
    botones= request.json.get("botones", None) 
    mic= request.json.get("mic", None) 
    audio= request.json.get("audio", None) 
    bateria= request.json.get("bateria", None) 
    conector_c= request.json.get("conector_c", None) 
    bluetooth= request.json.get("bluetooth", None) 
    wifi= request.json.get("wifi", None) 
    zona_w= request.json.get("zona_w", None)
    nfc= request.json.get("nfc", None)
    conector_a= request.json.get("conector_a", None)
    porta_sim= request.json.get("porta_sim", None)
    filtracion= request.json.get("filtracion", None)
    llamadas_e= request.json.get("llamadas_e", None)
    llamadas_r= request.json.get("llamadas_r", None)
    msj_e= request.json.get("msj_e", None)
    msj_r= request.json.get("msj_r", None)
    foto_f= request.json.get("foto_f", None)
    foto_t= request.json.get("foto_t", None)
    video_f= request.json.get("video_f", None)
    video_t= request.json.get("video_t", None)
    sen_proximidad= request.json.get("sen_proximidad", None)
    vibrador= request.json.get("vibrador", None)
    puntaje_tec= request.json.get("puntaje_tec", None)
    #--------revision de software---------
    bloqueo= request.json.get("bloqueo", None)
    act_sw= request.json.get("act_sw", None)
    restauracion= request.json.get("restauracion", None)
    #------fin revision-----------
    # fecha_rev= request.json.get("fecha_rev", None)# --- fecha

    strFecha = request.json.get("fecha_rev", None)
    print('FECHA:', strFecha)
    fecha_rev = datetime.datetime.strptime(strFecha, '%d/%m/%Y').date()
    print('FECHA2:', fecha)

    clasificacion= request.json.get("clasificacion", None)
    ert= request.json.get("ert", None)
    observaciones= request.json.get("observaciones", None)


@api.route('/recepcion',methods=['POST'])
@jwt_required()
def recepcion():
    
    try:
        registros=request.json.get("registros")
        entrada= db.session.execute(db.insert(Entrada, registros))
        distintos=db.select(Equipos.serie).subquery()
        distintos_subquery=db.aliased(Equipos,distintos,name="distintos")
        q=(db.select(Entrada.serie).distinct(Entrada.serie).join(distintos_subquery,Entrada.serie!=distintos_subquery.serie,isouter = True).subquery())
        query=db.insert(Equipos).from_select(["serie"],q)
        execute=db.session.execute(query)
        db.session.commit()
        return jsonify({"msg":"ok"})  
    
    except Exception as e:
        print (e)
        return jsonify({"msg":"error"})

@api.route('/registrosRecepcion', methods=['GET'])
@jwt_required()
def registros_recepcion():
    try:
        entrada=db.engine.connect().execute(db.select(Entrada))
        lista=[]
        for row in entrada:
            lista.append(row._asdict())
        return jsonify({"status":"ok","lista":lista})
    except Exception as e:
        print(e)
        return jsonify({"status":"nok"})

@api.route('/nroCajaVerificacion', methods=['GET'])
@jwt_required()
def nro_caja_verficacion():
    try:
        consulta=db.select(db.func.max(Entrada.nro_caja))
        max=db.engine.connect().execute(consulta)
        for i in max:
            max_r=i._asdict()
        return jsonify({"msg":"ok","result":max_r["max_1"]})
    except Exception as e:
        print(e)
        return jsonify({"msg":"nok"})

@api.route('/nroDocumento',methods=['POST'])
@jwt_required()
def nro_documento():
    try:
        lista=[]
        documento=request.json.get("documento")
        nro=Entrada.query.filter_by(documento=documento,estado="Pendiente").all()
        if nro==None:
            return ({"msg":"nok"})
        else:
            for record in nro:
                lista.append(record.serie)
            return jsonify({"msg":"ok","lista":lista})
    except Exception as e:
        print(e)
        return jsonify({"msg":"nok"})


# ------------------ actualiza los equipos verificados de entrada -----------------------------------------------------
@api.route('/guardarVerficacionRecepcion',methods=['PUT'])
@jwt_required()
def guardar_verificacion_recepcion():
    try:
        lista=request.json.get("lista")
        consulta=db.update(Entrada).where(Entrada.serie==db.bindparam("serie_b"),Entrada.documento==db.bindparam("documento_b")).values(f_verificacion=db.bindparam("f_verificacion"),\
            responsable_ver=db.bindparam("responsable_ver"),tipo_caja=db.bindparam("tipo_caja"),estado=db.bindparam("estado"),observaciones=db.bindparam("observaciones"))
        db.session.execute(consulta,lista)
        db.session.commit()
        consulta=db.select(db.func.max(Entrada.nro_caja))
        max=db.engine.connect().execute(consulta)
        for i in max:
            max_r=i._asdict()
        return jsonify({"msg":"ok","nro_caja":max_r["max_1"]})
    except Exception as e:
        print(e)
        return jsonify({"msg":"nok"})

@api.route('/ingresarEmpacados',methods=['POST'])
@jwt_required()
def actualizar_empacados():
    try:
        body=request.json.get("empacados")
        actualizarEmpacados= db.insert(Salida)
        consulta=db.session.execute(actualizarEmpacados,body)
        db.session.commit()
        return jsonify({"msg":"ok"})
    except Exception as e:
        print(e)
        return jsonify({"msg":"nok"})

@api.route('/tablaEmpacados', methods=['GET'])
@jwt_required()
def tabla_empacados():
    try:
        query=db.session.execute('select * from salida')
        lista=list()
        for row in query:
            lista.append(row._asdict())
        print(lista)
        return jsonify({"msg":"ok","lista":lista})
    except Exception as e:
        print(e)
        return jsonify({"msg":"nok"})

@api.route('/verificarSerieEmbalaje',methods=['POST'])
@jwt_required()
def verificar_serie_emabalaje():
    try:
        serie=request.json.get("serie")
        serie_salida=Salida.query.filter_by(serie=serie).one_or_none()
        if serie_salida==None:
            return jsonify({"msg":"nok"})
        else:
            return jsonify({"msg":"ok","denominacion":serie_salida.denominacion,"material":serie_salida.material,"id":serie_salida.id})
    except Exception as e:
        print(e)
        return jsonify({"msg":"nok"})

@api.route('/guardarEmbalaje',methods=['PUT'])
@jwt_required()
def guardar_emabalaje():
    try:
        lista=request.json.get("lista")
        consulta=db.update(Salida).where(Salida.id==db.bindparam("id_b")).values(tipo_caja=db.bindparam("tipo_caja"),nro_caja=db.bindparam("nro_caja"),fecha_embalaje=db.bindparam("fecha_embalaje"))
        db.session.execute(consulta,lista)
        db.session.commit()
        max=db.session.execute(db.select(db.func.max(Salida.nro_caja)))
        resulMax={}
        for i in max:
            resulMax=i._asdict()
        
        print(resulMax)
        return jsonify({"msg":"ok","nro_caja":resulMax["max"]})
    except Exception as e :
        print(e)
        return jsonify({"msg":"nok"})

@api.route('/borrarRegistroRecepcion',methods=['DELETE'])
@jwt_required()
def borrar_registros_recepcion():
    return
# queda esta funcion en standby


@api.route('/prueba1',methods=['GET'])
def prueba1():
    lista=[]
    # max=db.select(db.func.max(Entrada.id)).group_by(Entrada.serie).subquery()
    # maxAlias=db.aliased(Entrada,max)
    # ordermax=db.select(max).order_by(db.asc(max)).subquery()
    # ordermaxAlias=db.aliased(Entrada,ordermax)
    # join=db.select(Entrada.serie,Entrada.denominacion,Entrada.material).select_from(Entrada).join(ordermaxAlias, Entrada.id==ordermaxAlias)
    execute=db.engine.connect().execute("select series.id,series.serie, datos_basicos.denominacion,datos_basicos.material from (select serie, revision.id from asignacion join (select id,id_asignacion from revision_movil)as revision on asignacion.id=revision.id_asignacion) as series join (select id,serie,denominacion,material from entrada join (select max(id) as max from entrada group by serie order by max asc) as diferentes on entrada.id=diferentes.max) as datos_basicos on series.serie=datos_basicos.serie;")
    for row in execute:
        print(row._asdict())
    # print(join)
    print(len(list(execute)))

    return jsonify({"lista":"lista"})

@api.route("/equipos", methods=["GET"])
# @jwt_required()
def getEquipos():
    try:
        lista = list()
        # equipos = Equipos.query.all()
        # equipos_list = list(map(lambda x: x.serialize(), equipos))
        equipos = db.session.execute('select series.id,series.serie, datos_basicos.denominacion,datos_basicos.material from (select serie, revision.id from asignacion join (select id,id_asignacion from revision_movil)as revision on asignacion.id=revision.id_asignacion) as series join (select id,serie,denominacion,material from entrada join (select max(id) as max from entrada group by serie order by max asc) as diferentes on entrada.id=diferentes.max) as datos_basicos on series.serie=datos_basicos.serie;')
        for equipo in equipos:
            lista.append(equipo._asdict())
        return jsonify(lista)
        # return jsonify(equipos_list)
    except Exception as e:
        print(e)
        return jsonify({"msg":"error"})
