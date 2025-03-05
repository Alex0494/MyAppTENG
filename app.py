from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

load_dotenv()

app = Flask(__name__)

admin=os.getenv("admin")
admin=json.loads(admin) if admin else {}
cred = credentials.Certificate(admin)
firebase_admin.initialize_app(cred)

# Inicializar Firebase con Firestore
# cred = credentials.Certificate("myappprueba-firebase.json")
# firebase_admin.initialize_app(cred)
# firebase_admin.initialize_app(cred, {
#     'databaseURL': "https://mitest-2d566-default-rtdb.firebaseio.com/"
# })

db = firestore.client() # Cliente de Firestore
TENG_ref = db.collection('TENG')    # Referencia a la colección TENG

@app.route('/')
def hello():
    return "hello world"

@app.route('/sensor', methods=['POST'])
def receive_sensor_data(): # recibir_datos_sensor
    try:
        data = request.get_json()
        
        # Añadir timestamp del servidor
        data['server_timestamp'] = datetime.now().isoformat()
        
        # Guardar en Firestore
        # doc_ref = TENG_ref.document()  # Crea un nuevo documento con ID automático
        # doc_ref.set(data)

        TENG_ref.add(data)  # Crea un documento con ID automático y establece los datos en una operación

        
        return jsonify({
            'status': 'success',
            'message': 'Datos guardados correctamente',
            'data': data
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)


# GET Obtener objeto , Leer datos
# POST Crear objeto, escribir datos
# PUT Actualizar objeto, escribir CAMBIOS
# DELETE Eliminar objeto