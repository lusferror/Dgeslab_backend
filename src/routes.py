
from flask import Flask, request, jsonify, url_for, Blueprint
from models import db, Salida, Asignacion, Revision_movil, Equipos
import json
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import datetime


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
            fecha_documento = salida.fecha_documento.strftime('%d/%m/%Y')            
            f_despacho_fisico = salida.f_despacho_fisico.strftime('%d/%m/%Y')            
            list_sal.append(
                {
                    "documento": salida.documento, 
                    "serie": salida.serie, 
                    "fecha_documento": fecha_documento, 
                    "b_origen_salida": salida.b_origen_salida, 
                    "b_destino_salida": salida.b_destino_salida, 
                    "guia_despacho": salida.guia_despacho, 
                    "f_despacho_fisico": f_despacho_fisico
                })
        print(list_sal)
        return jsonify({"salida": list_sal}), 200
    except Exception as e:
        mens=str(e)
        error = {'Error':mens}
        print('Error: ', error)
        return jsonify({"message":error}), 500


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

# @api.route("/asignacion", methods=["GET"])
# def getAsignacion():

#     asignacion = Asignacion.query.all()
#     asignacion_list = list(map(lambda x: x.serialize(), asignacion))    
    
#     return jsonify(asignacion_list)


# @api.route("/asignacion", methods=["POST"])
# def register_asignacion():
#     id  =  request.json.get("id",None)
#     id_asignacion= request.json.get("id_asignacion",None)
#     fecha_asignacion =  request.json.get("fecha_asignacion",None)
#     serie=request.json.get("serie", None)
#     check = request.json.get("check", None)
#     estado= request.json.get("estado", None) 


#     new_asignacion = Asignacion( id=id, id_asignacion=id_asignacion ,fecha_asignacion=fecha_asignacion, serie=serie , check = check, estado=estado)    

#     db.session.add(new_asignacion)
#     db.session.commit()

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


@api.route("/revision_movil", methods=["GET"])
def getRevisionMovil():
    try:
        revision = Revision_movil.query.all()
        revision_list = list(map(lambda x: x.serialize(), revision))    
        
        return jsonify(revision_list)
    except Exception as e:
        print(e)
        return jsonify({"msg":"error"})


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

# import os
# from flask import Flask, request, jsonify, url_for, Blueprint
# # from api.models import db, User
# # from api.utils import generate_sitemap, APIException
# from flask_jwt_extended import create_access_token
# from flask_jwt_extended import get_jwt_identity
# from flask_jwt_extended import jwt_required
# from typing import List

# import os
# from flask import Flask, request, jsonify, url_for, Blueprint
# # from api.models import db, User
# # from api.utils import generate_sitemap, APIException
# from flask_jwt_extended import create_access_token
# from flask_jwt_extended import get_jwt_identity
# from flask_jwt_extended import jwt_required
# from typing import List

@api.route('/recepcion',methods=['POST'])
def recepcion():
    try:
        body=request.json.get("series")
        for i in body:
            serie=Equipos.query.filter_by(serie=i["Imei"]).one_or_none()
            if serie==None:
                nuevo_equipo= Equipos(documento_entrada=i["Doc"],folio=i["Folio"],material=i["Material"],denominacion=i["Descripcion"],serie=i["Imei"],b_origen_entrada=i["Borg"],b_destino_entrada=i["Bdest"])
                db.session.add(nuevo_equipo)
        db.session.commit()
        # print(body)
        return jsonify({"msg":"ok"}),200
    except Exception as e:
        print (e)
        return jsonify({"msg":"error"}),400
