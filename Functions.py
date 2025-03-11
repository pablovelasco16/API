from bson import ObjectId, json_util as j
from flask import Flask, request, jsonify
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import BackEnd.GlobalInfo.ResponseMessages as ResponseMessage
import BackEnd.GlobalInfo.Keys as ColabsKey

app = Flask(__name__)

# Conexión a la base de datos
uri = "mongodb+srv://mimi:oaOKqX0tvwe8d7u2@cluster0.rkxwz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

if ColabsKey.dbconn is None:
    client = MongoClient(uri, server_api=ServerApi('1'))
    ColabsKey.dbconn = client[ColabsKey.strDBConnection]
    dbUsers = ColabsKey.dbconn['usuario']
    dbSchedules = ColabsKey.dbconn["aspersores"]
    dbValves = ColabsKey.dbconn["valvula"]

# Registrar un nuevo usuario
@app.route('/api/users', methods=['POST'])
def register_user():
    data = request.get_json()
    user = data.get('usuario')
    password = data.get('contraseña')

    try:
        print("Inserción de datos de usuario")
        dbUsers.insert_one({"usuario": user, "contraseña": password})
        objResponse = ResponseMessage.succ200.copy()
        objResponse['Estatus_Guardado'] = True
        return jsonify(objResponse)
    except Exception as e:
        objResponse = ResponseMessage.err500
        objResponse["Estatus_Guardado"] = False
        return jsonify(objResponse, e)

# Autenticación de usuario
@app.route('/api/auth', methods=['POST'])
def authenticate_user():
    data = request.get_json()
    user = data.get('usuario')
    password = data.get('contraseña')

    try:
        print("Comprobación de credenciales")
        objQuery = dbUsers.find_one({"usuario": user, "contraseña": password})
        if objQuery:
            objResponse = ResponseMessage.succ200.copy()
            objResponse['Estatus_Acreditado'] = True
            objResponse['user_id'] = str(objQuery.get('_id'))
            return jsonify(objResponse)
        else:
            objResponse = ResponseMessage.err401
            objResponse["Estatus_Acreditado"] = False
            return jsonify(objResponse)
    except Exception as e:
        objResponse = ResponseMessage.err500
        objResponse["Estatus_Acreditado"] = False
        return jsonify(objResponse, e)

# Registrar un nuevo horario de riego
@app.route('/api/schedules', methods=['POST'])
def register_schedule():
    data = request.get_json()
    user_id = data.get('usuario_id')
    day = data.get('dia')
    time = data.get('hora')
    valve_status = data.get('estadoValvula')

    try:
        print("Inserción de datos de horario de riego")
        dbSchedules.insert_one({"usuario_id": ObjectId(user_id), "dia": day, "hora": time, "estadoValvula": valve_status})
        objResponse = ResponseMessage.succ200.copy()
        objResponse['Estatus_Guardado'] = True
        return jsonify(objResponse)
    except Exception as e:
        objResponse = ResponseMessage.err500
        objResponse["Estatus_Guardado"] = False
        return jsonify(objResponse, e)

# Obtener el estado de la válvula
@app.route('/api/valves/<id>', methods=['GET'])
def get_valve_state(id):
    try:
        print("Obtención del estado de la válvula")
        objQuery = dbValves.find_one({"_id": ObjectId(id)})
        valve_status = objQuery.get('estadoValvula')
        objResponse = ResponseMessage.succ200.copy()
        objResponse['estadoValvula'] = valve_status
        return jsonify(objResponse)
    except Exception as e:
        objResponse = ResponseMessage.err500
        objResponse["Estatus_Acreditado"] = False
        return jsonify(objResponse, e)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
