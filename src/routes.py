
from flask import Flask, request, jsonify, url_for, Blueprint
from models import db, Salida, User, Role
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





