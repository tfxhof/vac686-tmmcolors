import json
import os

from flask import Flask, send_file, jsonify
from flask_restx import Resource, Api, reqparse

from src.calculo_color.calculo_color import calcula_rgb
from src.calculo_color.lee_fichero import leer_fichero

app = Flask(__name__)
api = Api(app)
json_directory = os.path.join(os.path.dirname(__file__), '..', '..', 'documents')


@api.route('/getMateriales/')
class obtenerMateriales(Resource):
    def get(self):
        ruta_json = os.path.join(os.path.dirname(__file__), '..', '..', 'documents', 'diccionario.json')
        if os.path.exists(ruta_json):
            return send_file(ruta_json, mimetype='application/json')


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
                return jsonify(objeto["nombre"])
            else:
                # Si el objeto no existe, se retorna un mensaje de error con código 404
                return {'error': 'Objeto no encontrado'}, 404


        else:
            # Si el archivo no existe, retorna un mensaje de error
            return {'error': 'Archivo JSON no encontrado'}, 404


parser = reqparse.RequestParser()

parser.add_argument('materiales', type=str, help='Lista de materiales separados por comas')
parser.add_argument('grosores', type=str, help='Lista de grosores separados por comas')



@api.route('/getColors')
class getColors(Resource):
    def get(self):
        # Analizar los argumentos de la URL
        args = parser.parse_args()
        # Extraer la lista de materiales y dividirla en una lista
        materiales_param = args['materiales']
        materiales = materiales_param.split(',') if materiales_param else []

        grosores_param = args['grosores']
        grosores = []

        if grosores_param:
            grosores_list = grosores_param.split(',')
            for g in grosores_list:
                try:
                    grosores.append(float(g))
                except ValueError:
                    return jsonify({'error': f'El grosor "{g}" no es un número válido'})

        if len(materiales) < 2:
            return jsonify({'error': 'Se requieren al menos dos materiales'})

        material1 = materiales[0]
        material2 = materiales[1]

        grosor1 = grosores[0]
        grosor2 = grosores[1]
        grosor3 = grosores[2]

        si_n_fn = leer_fichero(material1)
        au_n_fn = leer_fichero(material2)
        air_n_fn = lambda wavelength: 1

        n_fn_list = [air_n_fn, si_n_fn, au_n_fn, air_n_fn]
        th_0 = 0
        d_list = [grosor1, grosor2, grosor3, grosor1]
        rgb_values = calcula_rgb(n_fn_list, d_list, th_0)
        rgb_values_list = rgb_values.tolist()

        # Crear un resultado con las variables individuales
        resultado = {
            'material1': material1,
            'material2': material2,
            'resultado': rgb_values_list
        }
        return jsonify(resultado)


if __name__ == '__main__':
    app.run(debug=True)
