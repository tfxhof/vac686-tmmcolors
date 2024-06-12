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

parser = reqparse.RequestParser()

parser.add_argument('materiales', type=str, help='Lista de materiales separados por comas')
parser.add_argument('grosores', type=str, help='Lista de grosores separados por comas')


@api.route('/materiales/label')
class obtenerNombreMateriales(Resource):
    def get(self):
        ruta_json = os.path.join(os.path.dirname(__file__), '..', '..', 'documents', 'catalogo.json')
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


@api.route('/colors/<materiales>/<grosores>')
class get_colors(Resource):
    def get(self, materiales, grosores=None):
        # Dividir la cadena de materiales en una lista
        materiales_list = materiales.split(',') if materiales else []

        if len(materiales_list) < 1:
            return jsonify({'error': 'Se requieren al menos dos materiales'})
        if len(materiales_list) > 50:
            return jsonify({'error': 'No s epueden anadir mas materiales'})
        primer_material = materiales_list.pop(0)

        # Crear una lista de funciones de índice de refracción para los materiales
        n_fn_list = [leer_fichero(material) for material in materiales_list]

        if primer_material.lower() == 'air':
            n_fn = lambda wavelength: 1
        else:
            try:
                valor_numerico = float(primer_material)
                n_fn = lambda wavelength: valor_numerico
            except ValueError:
                return jsonify({'error': 'El primer material no es válido'})

            # Calcular los valores RGB
        th_0 = 0
        if grosores is None or grosores == '':
            return jsonify({'error': 'You should add at least one layer.'})
        # Dividir la cadena de grosores en una lista de números
        grosores_str_list = grosores.split(',')
        grosores_list = []

        for g in grosores_str_list:
            try:
                grosor = float(g) if g != 'inf' else float('inf')
            except ValueError:
                return jsonify({'error': 'Thikness field must be a numeric value'})

            if grosor < 0:
                return jsonify({'error': 'Thikness value must be a number greater than 0'})

            grosores_list.append(grosor)

        # Verificar que haya al menos dos grosores

        # Calcular los valores RGB
        d_list = [float('inf')] + grosores_list + [float('inf')]  # Agregar infinito al final para el último material
        rgb_values = calcula_rgb([n_fn] + n_fn_list, d_list, th_0)
        rgb_values_list = rgb_values.tolist()

        # Crear un resultado con las variables individuales
        resultado = {
            'rgb': rgb_values_list
        }
        return jsonify(resultado)


api.add_resource(get_colors, '/colors/<string:materiales>/', '/colors/<string:materiales>/<string:grosores>')

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
