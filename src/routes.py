
from flask import Flask, request, jsonify, url_for, Blueprint
from models import db, Salida, Asignacion, Revision_movil, Equipos,Entrada,Series, User
import json
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import datetime
from flask_sqlalchemy import SQLAlchemy


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