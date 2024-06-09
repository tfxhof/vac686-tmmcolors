import json
import os
from importlib.resources import Resource

from flask import jsonify, send_file

from src.calculo_color.lee_fichero import leer_fichero
from src.rest.api import api


def saludar(nombre):
    """Función que saluda a una persona."""
    print(f"{nombre}!")


def main():
    """Función principal del programa."""
    print("¡Bienvenido al programa!")

    # Solicitar al usuario que ingrese su nombre
    nombre = leer_fichero("si")

    # Llamar a la función para saludar
    saludar(nombre)

    print("¡Gracias por usar este programa!")


# Verificar si este script se está ejecutando directamente
if __name__ == "__main__":
    # Llamar a la función principal
    main()


@api.route('/materiales/')
class obtenerMateriales(Resource):
    def get(self):
        ruta_json = os.path.join(os.path.dirname(__file__), '..', '..', 'documents', 'catalogo.json')
        if os.path.exists(ruta_json):
            return send_file(ruta_json, mimetype='application/json')


        else:
            # Si el archivo no existe, retorna un mensaje de error
            return {'error': 'Archivo JSON no encontrado'}, 404
@api.route('/materiales/<int:objeto_id>')
class ObtenerMaterialPorID(Resource):
    def get(self, objeto_id):
        print(1)
        ruta_json = os.path.join(os.path.dirname(__file__), '..', '..', 'documents', 'catalogo.json')
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


@api.route('/materiales/nombre/<int:objeto_id>/')
class ObtenerNombredeMaterialPorID(Resource):
    def get(self, objeto_id):
        print(1)
        ruta_json = os.path.join(os.path.dirname(__file__), '..', '..', 'documents', 'catalogo.json')
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
