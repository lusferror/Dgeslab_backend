
from flask import Flask, request, jsonify, url_for, Blueprint
from models import db, Salida, Asignacion, Revision_movil, Equipos,Entrada,Series, User
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
        # asignacion=(db.update(Asignacion).where(Asignacion.id==5).values(check=True,estado="Aprobado"))
        execute=db.session.execute(asignacion,registros)
        db.session.commit()
        # print("series: ",registros  )
        # print("consulta: ",asignacion)
        return jsonify({"msg":"ok"})
    except Exception as e:
        print(e)
        return jsonify({"msg":"nok"})


# @api.route("/asignacion", methods=["POST"])
# def register_asignacion():
#     id  =  request.json.get("id",None)
#     id_asignacion= request.json.get("id_asignacion",None)
#     fecha_asignacion =  request.json.get("fecha_asignacion",None)
#     serie=request.json.get("serie", None)
#     check = request.json.get("check", None)
#     estado= request.json.get("estado", None) 



#     return jsonify({
#         "id": new_asignacion.id,
#         "id_asignacion": new_asignacion.id_asignacion,
#         "fecha_asignacion": new_asignacion.fecha_asignacion,
#         "serie" : new_asignacion.serie,
#         "check"  : new_asignacion.check,
#         "estado"  : new_asignacion.estado
#     })

# @api.route('/asignacion/<int:id>', methods=['PUT'])
# def updateAsignacion(id):
#     asignacionM = Asignacion.query.get(id)
#     RQ = request.get_json()
#     asignacionM.fecha_asignacion = RQ["fecha_asignacion"]
#     asignacionM.serie = RQ["serie"]
#     asignacionM.check = RQ["check"]
#     asignacionM.estado = RQ["estado"]
#     db.session.commit()            
#     return 'ok'



# @api.route('/asignacion/<int:id>', methods=['DELETE'])
# def deleteAsignacion(id):
#     asignacionM = Asignacion.query.get(id)
#     db.session.delete(asignacionM)
#     db.session.commit()  
#     return 'Asignacion Borrada'
    



# ENPOINT REVISION MOVIL

@api.route("/datos_movil_basico", methods=['POST'])
def datos_movil_basico():
    try:
        serie=int(request.json.get("serie"))
        print(serie)
        datos= Equipos.query.filter_by(serie=serie).one_or_none()
        print("resultado: ",datos)
        return jsonify({"denominacion":datos.denominacion})
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


    # new_Revision = Revision_movil( id=id, serie=serie ,material=material, denominacion=denominacion, tecnico_id=tecnico_id , fecha = fecha, encendido=encendido, 
    # frontal=frontal, frontal_r=frontal_r, trasera=trasera, trasera_r=trasera_r, superior=superior, superior_r=superior_r, inferior=inferior
    # , inferior_r=inferior_r, izquierdo=izquierdo, izquierdo_r=izquierdo_r, derecho=derecho, derecho_r=derecho_r, puntaje_cos=puntaje_cos
    # , pantalla=pantalla, tactil=tactil, botones=botones, mic=mic, audio=audio, bateria=bateria, conector_c=conector_c, bluetooth=bluetooth, wifi=wifi
    # , zona_w=zona_w, nfc=nfc, conector_a=conector_a, porta_sim=porta_sim, filtracion=filtracion
    # ,llamadas_e=llamadas_e, llamadas_r=llamadas_r, msj_e=msj_e, msj_r=msj_r, foto_f=foto_f, foto_t=foto_t, 
    # video_f=video_f, video_t=video_t, sen_proximidad=sen_proximidad, vibrador=vibrador, puntaje_tec=puntaje_tec, bloqueo=bloqueo,
    # act_sw=act_sw, restauracion=restauracion, fecha_rev=fecha_rev, clasificacion=clasificacion, ert=ert, observaciones=observaciones)    

    # db.session.add(new_Revision)
    # db.session.commit()

    # return jsonify({
    #     "id": new_Revision.id,
    #     "serie": new_Revision.serie,
    #     "material": new_Revision.material,
    #     "denominacion" : new_Revision.denominacion,
    #     "tecnico_id"  : new_Revision.tecnico_id,
    #     "fecha"  : new_Revision.fecha,
    #     "encendido" : new_Revision.encendido,
    #     "frontal"  : new_Revision.frontal,
    #     "frontal_r"  : new_Revision.frontal_r,
    #     "trasera" : new_Revision.trasera,
    #     "trasera_r"  : new_Revision.trasera_r,
    #     "superior"  : new_Revision.superior,
    #     "superior_r" : new_Revision.superior_r,
    #     "inferior"  : new_Revision.inferior,
    #     "inferior_r"  : new_Revision.inferior_r,
    #     "izquierdo" : new_Revision.izquierdo,
    #     "izquierdo_r"  : new_Revision.izquierdo_r,
    #     "derecho"  : new_Revision.derecho,
    #     "derecho_r" : new_Revision.derecho_r,
    #     "puntaje_cos"  : new_Revision.puntaje_cos,
    #     "pantalla"  : new_Revision.pantalla,
    #     "tactil" : new_Revision.tactil,
    #     "mic"  : new_Revision.mic,
    #     "audio"  : new_Revision.audio,
    #     "bateria" : new_Revision.bateria,
    #     "conector_c"  : new_Revision.conector_c,
    #     "bluetooth"  : new_Revision.bluetooth,
    #     "wifi" : new_Revision.wifi,
    #     "zona_w"  : new_Revision.zona_w,
    #     "nfc"  : new_Revision.nfc,
    #     "conector_a"  : new_Revision.conector_a,
    #     "porta_sim"  : new_Revision.porta_sim,
    #     "filtracion"  : new_Revision.filtracion,
    #     "llamadas_e"  : new_Revision.llamadas_e,
    #     "llamadas_r"  : new_Revision.llamadas_r,
    #     "msj_e"  : new_Revision.msj_e,
    #     "msj_r"  : new_Revision.msj_r,
    #     "foto_f"  : new_Revision.foto_f,
    #     "foto_t"  : new_Revision.foto_t,
    #     "video_f"  : new_Revision.video_f,
    #     "video_t"  : new_Revision.video_t,
    #     "sen_proximidad"  : new_Revision.sen_proximidad,
    #     "vibrador"  : new_Revision.vibrador,
    #     "puntaje_tec"  : new_Revision.puntaje_tec,
    #     "bloqueo"  : new_Revision.bloqueo,
    #     "act_sw"  : new_Revision.act_sw,
    #     "restauracion"  : new_Revision.restauracion,
    #     "fecha_rev"  : new_Revision.fecha_rev,
    #     "clasificacion"  : new_Revision.clasificacion,
    #     "ert"  : new_Revision.ert,
    #     "observaciones"  : new_Revision.observaciones,
        
    # })

# @api.route('/revision_movil/<int:id>', methods=['PUT'])
# def updateRevisionMovil(id):
#     RevisionM = Revision_movil.query.get(id)
#     RQ = request.get_json()
#     RevisionM.id = RQ["id"]
#     RevisionM.serie = RQ["serie"]
#     RevisionM.material = RQ["material"]
#     RevisionM.denominacion = RQ["denominacion"]
#     RevisionM.tecnico_id = RQ["tecnico_id"]
#     RevisionM.fecha = RQ["fecha"]
#     RevisionM.encendido = RQ["encendido"]
#     RevisionM.frontal = RQ["frontal"]
#     RevisionM.frontal_r = RQ["frontal_r"]
#     RevisionM.trasera = RQ["trasera"]
#     RevisionM.trasera_r = RQ["trasera_r"]
#     RevisionM.superior = RQ["superior"]
#     RevisionM.superior_r = RQ["superior_r"]
#     RevisionM.inferior = RQ["inferior"]
#     RevisionM.inferior_r = RQ["inferior_r"]
#     RevisionM.izquierdo = RQ["izquierdo"]
#     RevisionM.izquierdo_r = RQ["izquierdo_r"]
#     RevisionM.derecho = RQ["derecho"]
#     RevisionM.derecho_r = RQ["derecho_r"]
#     RevisionM.puntaje_cos = RQ["puntaje_cos"]
#     RevisionM.pantalla = RQ["pantalla"]
#     RevisionM.tactil = RQ["tactil"]
#     RevisionM.botones = RQ["botones"]
#     RevisionM.mic = RQ["mic"]
#     RevisionM.audio = RQ["audio"]
#     RevisionM.bateria = RQ["bateria"]
#     RevisionM.conector_c = RQ["conector_c"]
#     RevisionM.bluetooth = RQ["bluetooth"]
#     RevisionM.wifi = RQ["wifi"]
#     RevisionM.zona_w = RQ["zona_w"]
#     RevisionM.nfc = RQ["nfc"]
#     RevisionM.conector_a = RQ["conector_a"]
#     RevisionM.porta_sim = RQ["porta_sim"]
#     RevisionM.filtracion = RQ["filtracion"]
#     RevisionM.llamadas_e = RQ["llamadas_e"]
#     RevisionM.llamadas_r = RQ["llamadas_r"]
#     RevisionM.msj_e = RQ["msj_e"]
#     RevisionM.msj_r = RQ["msj_r"]
#     RevisionM.foto_f = RQ["foto_f"]
#     RevisionM.foto_t = RQ["foto_t"]
#     RevisionM.video_f = RQ["video_f"]
#     RevisionM.video_t = RQ["video_t"]
#     RevisionM.sen_proximidad = RQ["sen_proximidad"]
#     RevisionM.vibrador = RQ["vibrador"]
#     RevisionM.puntaje_tec = RQ["puntaje_tec"]
#     RevisionM.bloqueo = RQ["bloqueo"]
#     RevisionM.act_sw = RQ["act_sw"]
#     RevisionM.restauracion = RQ["restauracion"]
#     RevisionM.fecha_rev = RQ["fecha_rev"]
#     RevisionM.clasificacion = RQ["serie"]
#     RevisionM.ert = RQ["ert"]
#     RevisionM.observaciones = RQ["observaciones"]    
#     db.session.commit()            
#     return 'ok'


# @api.route('/revision_movil/<int:id>', methods=['DELETE'])
# def deleteRevision(id):
#     RevisionM = Asignacion.query.get(id)
#     db.session.delete(RevisionM)
#     db.session.commit()  
#     return 'reivision Borrada'


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




@api.route('/borrarRegistroRecepcion',methods=['DELETE'])
@jwt_required()
def borrar_registros_recepcion():
    return
# queda esta funcion en standby


@api.route('/prueba1',methods=['GET'])
def prueba1():
    lista=[]
    # diferentes=db.session.execute(db.select(Entrada).distinct(Entrada.serie))
    # diferentes=db.session.query(Entrada).distinct(Entrada.serie)
    distintos=db.select(Equipos.serie).subquery()
    distintos_subquery=db.aliased(Equipos,distintos,name="distintos")
    q=(db.select(Entrada.serie).distinct(Entrada.serie).join(distintos_subquery,Entrada.serie!=distintos_subquery.serie,isouter = True).subquery())
    query=db.insert(Equipos).from_select(["serie"],q)
    execute=db.session.execute(query)
    db.session.commit()
    # query=db.session.execute(db.select(Entrada).join(distintos_subquery,Entrada.serie==distintos_subquery.serie))
    # for row in query:
    # #     # lista.append(row.__dict__)
    # #     lista.append(row._asdict())
    #     # print(row.__dict__)
    #     print(row._asdict())
    print(query)
    # print(distintos_subquery)
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
