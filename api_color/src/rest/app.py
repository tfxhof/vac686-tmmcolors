from flask import Flask, jsonify, request

app = Flask(__name__)

# Datos de ejemplo
elementos = [
    {"id": 1, "nombre": "Elemento 1"},
    {"id": 2, "nombre": "Elemento 2"},
]

# Endpoint para obtener todos los elementos
@app.route('/api/elementos', methods=['GET'])
def obtener_elementos():
    return jsonify({"elementos": elementos})

# Endpoint para obtener un elemento por ID
@app.route('/api/elementos/<int:elemento_id>', methods=['GET'])
def obtener_elemento(elemento_id):
    elemento = next((e for e in elementos if e["id"] == elemento_id), None)
    if elemento:
        return jsonify({"elemento": elemento})
    else:
        return jsonify({"mensaje": "Elemento no encontrado"}), 404

# Endpoint para agregar un nuevo elemento
@app.route('/api/elementos', methods=['POST'])
def agregar_elemento():
    nuevo_elemento = request.get_json()
    elementos.append(nuevo_elemento)
    return jsonify({"mensaje": "Elemento agregado correctamente"})

# Endpoint para actualizar un elemento por ID
@app.route('/api/elementos/<int:elemento_id>', methods=['PUT'])
def actualizar_elemento(elemento_id):
    elemento = next((e for e in elementos if e["id"] == elemento_id), None)
    if elemento:
        datos_actualizados = request.get_json()
        elemento.update(datos_actualizados)
        return jsonify({"mensaje": "Elemento actualizado correctamente"})
    else:
        return jsonify({"mensaje": "Elemento no encontrado"}), 404

# Endpoint para eliminar un elemento por ID
@app.route('/api/elementos/<int:elemento_id>', methods=['DELETE'])
def eliminar_elemento(elemento_id):
    global elementos
    elementos = [e for e in elementos if e["id"] != elemento_id]
    return jsonify({"mensaje": "Elemento eliminado correctamente"})

if __name__ == '__main__':
    app.run(debug=True)