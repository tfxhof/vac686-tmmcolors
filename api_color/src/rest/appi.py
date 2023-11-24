import os

from flask import Flask, send_file
from flask_restx import Resource, Api

app = Flask(__name__)
api = Api(app)


@api.route('/getMateriales/')
class obtenerMateriales(Resource):
    def get(self):
        ruta_json = os.path.join(os.path.dirname(__file__), '..', '..', 'documents', 'diccionario.json')
        if os.path.exists(ruta_json):
            return send_file(ruta_json, mimetype='application/json')
        else:
            # Si el archivo no existe, retorna un mensaje de error
            return {'error': 'Archivo JSON no encontrado'}, 404


if __name__ == '__main__':
    app.run(debug=True)
