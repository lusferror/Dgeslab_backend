from flask import Flask, request, jsonify, url_for, Blueprint
from models import db, Salida
import json

api = Blueprint('api', __name__)

@api.route('/', methods = ['GET'])
def home():
    return 'hello world 2'


@api.route('/salida', methods = ['GET'])
def get_salida():
    try:
        salidas = db.session.query(Salida).all()
        list_user = list()
        for salida in salidas:
            print('salida-->>', salida)
            list_user.append({"documento": salida.documento, "serie": salida.serie})
        print(salidas)
        return jsonify({"users:", list_user}), 200
    except Exception as e:
        mens=str(e)
        error = {'Error':mens}
        print('Error: ', error)
        return jsonify({"message":error}), 500



    # try:
    #     salida = db.session.query(Salida).all()
    #     if salida is not None:
    #         return jsonify(salida.serialize()), 200
    #     else:
    #         return jsonify({"message":"salida not exist data"}), 404
    # except Exception as e:
    #     return jsonify({"message":e}), 500

@api.route('/salida/<int:id>', methods = ['PUT'])
def update_salida(id):
    try:
        salida = db.session.query(Salida).get(id)
        if salida is not None:
            salida.documento = request.json.get("documento")
            salida.serie = request.json.get("serie")
            salida.fechadocumento = request.json.get("fechadocumento")
            salida.b_origen_salida = request.json.get("b_origen_salida")
            salida.b_destino_salida = request.json.get("b_destino_salida")
            salida.guia_despacho = request.json.get("guia_despacho")
            salida.f_despacho_fisico = request.json.get("f_despacho_fisico")
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
        salida.fecha_empacado = request.json.get("fecha_empacado")
        salida.responsable_id = request.json.get("responsable_id")
        salida.tipo_caja = request.json.get("tipo_caja")
        salida.nro_caja = request.json.get("nro_caja")
        salida.fecha_embalaje = request.json.get("fecha_embalaje")
        salida.documento = request.json.get("documento")
        salida.guia_despacho = request.json.get("guia_despacho")
        salida.b_origen_salida = request.json.get("b_origen_salida")
        salida.b_destino_salida = request.json.get("b_destino_salida")
        salida.fecha_documento = request.json.get("fecha_documento")
        salida.f_despacho_fisico = request.json.get("f_despacho_fisico")
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

