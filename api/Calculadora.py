
from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path

# 1. Ubicacion del proyecto
BASE_DIR = Path(__file__).resolve().parent

# 2. Crear la aplicacion Flask
app = Flask(__name__, static_folder=None)

# 3. Catalogo de productos y precios
PRODUCTOS = {
    "hamburguesa": {
        "nombre": "Hamburguesa Crunch",
        "precio": 18000
    },
    "perro": {
        "nombre": "Perro Explosivo",
        "precio": 14000
    },
    "salchipapa": {
        "nombre": "Salchipapa Suprema",
        "precio": 16000
    }
}


# 4. Mostrar la pagina principal
@app.get("/")
def inicio():
    return send_from_directory(BASE_DIR, "Index.html")


# 5. Buscar los archivos CSS
@app.get("/css/<path:archivo>")
def servir_css(archivo):
    return send_from_directory(BASE_DIR / "css", archivo)


# 6. Buscar las imagenes
@app.get("/IMG/<path:archivo>")
def servir_imagenes(archivo):
    return send_from_directory(BASE_DIR / "IMG", archivo)


# 7. Recibir y calcular el pedido
@app.post("/api/calcular")
def calcular_pedido():

    # 8. Recibir los datos enviados desde HTML
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({"error": "Datos incorrectos"}), 400

    # 9. Obtener los productos seleccionados
    items = datos.get("items")

    if not isinstance(items, list):
        return jsonify({"error": "Lista de productos incorrecta"}), 400

    # 10. Preparar el resumen y el total
    resumen = []
    total = 0

    # 11. Recorrer cada producto
    for item in items:

        if not isinstance(item, dict):
            return jsonify({"error": "Producto incorrecto"}), 400

        producto_id = item.get("id")
        cantidad = item.get("cantidad")

        # 12. Verificar que el producto exista
        if producto_id not in PRODUCTOS:
            return jsonify({"error": "Producto no valido"}), 400

        # 13. Validar la cantidad
        if isinstance(cantidad, bool) or not isinstance(cantidad, int):
            return jsonify({"error": "Cantidad incorrecta"}), 400

        if cantidad < 1 or cantidad > 99:
            return jsonify({"error": "Cantidad fuera de rango"}), 400

        # 14. Obtener los datos del producto
        producto = PRODUCTOS[producto_id]

        # 15. Calcular el subtotal
        subtotal = producto["precio"] * cantidad

        # 16. Acumular el total
        total += subtotal

        # 17. Guardar el producto en el resumen
        resumen.append({
            "id": producto_id,
            "nombre": producto["nombre"],
            "precio": producto["precio"],
            "cantidad": cantidad,
            "subtotal": subtotal
        })

    # 18. Enviar el resultado a HTML
    return jsonify({
        "productos": resumen,
        "total": total,
        "moneda": "COP"
    })


# 19. Iniciar el servidor
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
