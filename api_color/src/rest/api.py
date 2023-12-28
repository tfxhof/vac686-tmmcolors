import json
import os

from flask import Flask, send_file, jsonify
from flask_restx import Resource, Api, reqparse
from flask_cors import CORS


from src.calculo_color.calculo_color import calcula_rgb
from src.calculo_color.lee_fichero import leer_fichero

from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

app = Flask(__name__)
api = Api(app)
CORS(app)  # Habilita CORS para todas las rutas

json_directory = os.path.join(os.path.dirname(__file__), '..', '..', 'documents')


# Define el manejador de solicitudes HTTP
handler = SimpleHTTPRequestHandler



@api.route('/getMateriales/')
class obtenerMateriales(Resource):
    def get(self):
        ruta_json = os.path.join(os.path.dirname(__file__), '..', '..', 'documents', 'diccionario.json')
        if os.path.exists(ruta_json):
            return send_file(ruta_json, mimetype='application/json')


        else:
            # Si el archivo no existe, retorna un mensaje de error
            return {'error': 'Archivo JSON no encontrado'}, 404

@api.route('/getMateriales/label')
class obtenerNombreMateriales(Resource):
    def get(self):
        ruta_json = os.path.join(os.path.dirname(__file__), '..', '..', 'documents', 'diccionario.json')
        if os.path.exists(ruta_json):
            with open(ruta_json, 'r') as file:
                contenido = json.load(file)
                print("Contenido del archivo JSON:", contenido)  # Impresión para depuración

                if contenido:
                    # Obtener el primer elemento de la lista (índice 0)
                    nombres = [elemento["label"] for elemento in contenido]
                    return jsonify(nombres)



        else:
            # Si el archivo no existe, retorna un mensaje de error
            return {'error': 'Archivo JSON no encontrado'}, 404


@api.route('/getMateriales/<int:objeto_id>')
class ObtenerMaterialPorID(Resource):
    def get(self, objeto_id):
        print(1)
        ruta_json = os.path.join(os.path.dirname(__file__), '..', '..', 'documents', 'diccionario.json')
        if os.path.exists(ruta_json):
            with open(ruta_json, 'r') as json_file:
                data = json.load(json_file)

                objeto = next((item for item in data if item["id"] == objeto_id), None)
            if objeto:
                return objeto
            else:
                # Si el objeto no existe, se retorna un mensaje de error con código 404
                return {'error': 'Objeto no encontrado'}, 404


        else:
            # Si el archivo no existe, retorna un mensaje de error
            return {'error': 'Archivo JSON no encontrado'}, 404


@api.route('/getMateriales/nombre/<int:objeto_id>/')
class ObtenerNombredeMaterialPorID(Resource):
    def get(self, objeto_id):
        print(1)
        ruta_json = os.path.join(os.path.dirname(__file__), '..', '..', 'documents', 'diccionario.json')
        if os.path.exists(ruta_json):
            with open(ruta_json, 'r') as json_file:
                data = json.load(json_file)

                objeto = next((item for item in data if item["id"] == objeto_id), None)
            if objeto:
                return jsonify(objeto["label"])
            else:
                # Si el objeto no existe, se retorna un mensaje de error con código 404
                return {'error': 'Objeto no encontrado'}, 404


        else:
            # Si el archivo no existe, retorna un mensaje de error
            return {'error': 'Archivo JSON no encontrado'}, 404


parser = reqparse.RequestParser()

parser.add_argument('materiales', type=str, help='Lista de materiales separados por comas')
parser.add_argument('grosores', type=str, help='Lista de grosores separados por comas')





@api.route('/getColors/<materiales>/<grosores>')
class getColors(Resource):
    def get(self, materiales, grosores):
        # Dividir la cadena de materiales en una lista
        materiales_list = materiales.split(',') if materiales else []

        if len(materiales_list) < 2:
            return jsonify({'error': 'Se requieren al menos dos materiales'})

        # Crear una lista de funciones de índice de refracción para los materiales
        n_fn_list = [leer_fichero(material) for material in materiales_list]

        # Crear una función de índice de refracción para el aire
        air_n_fn = lambda wavelength: 1
        si_n_fn = leer_fichero('si')

        # Calcular los valores RGB
        th_0 = 0

        # Dividir la cadena de grosores en una lista de números
        grosores_list = [float(g) if g != 'inf' else float('inf') for g in grosores.split(',')]


        # Verificar que haya al menos dos grosores
        if len(grosores_list) < 2:
            return jsonify({'error': 'Se requieren al menos dos grosores'})

        # Calcular los valores RGB
        d_list = [float('inf')]+grosores_list + [float('inf')]  # Agregar infinito al final para el último material
        rgb_values = calcula_rgb([air_n_fn] + n_fn_list + [si_n_fn], d_list, th_0)
        rgb_values_list = rgb_values.tolist()

        # Crear un resultado con las variables individuales
        resultado = {
            'rgb': rgb_values_list
        }
        return jsonify(resultado)


if __name__ == '__main__':
    httpd = TCPServer(("", 8000), handler)
    print("Servidor en el puerto 8000")

    # Ejecuta Flask en segundo plano
    from threading import Thread

    thread = Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000})
    thread.daemon = True
    thread.start()

    # Inicia el servidor HTTP
    httpd.serve_forever()
