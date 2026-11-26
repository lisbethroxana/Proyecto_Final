import html
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs


# Catalogo de productos y precios
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


def pesos(valor):
    return "$" + format(valor, ",").replace(",", ".")


def crear_pagina(titulo, contenido):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(titulo)} - CRUNCH & GO</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #fff7ed;
            margin: 0;
            padding: 30px 15px;
            color: #333;
        }}
        .contenedor {{
            max-width: 650px;
            margin: 30px auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 3px 12px rgba(0,0,0,0.12);
        }}
        h1 {{
            color: #d35400;
            text-align: center;
        }}
        .detalle {{
            padding: 12px 0;
            border-bottom: 1px solid #eee;
        }}
        .total {{
            font-size: 24px;
            font-weight: bold;
            color: #d35400;
            margin-top: 20px;
        }}
        .volver {{
            display: inline-block;
            margin-top: 25px;
            padding: 12px 20px;
            background: #d35400;
            color: white;
            text-decoration: none;
            border-radius: 6px;
        }}
        .mensaje {{
            background: #fff0df;
            padding: 12px;
            border-radius: 6px;
        }}
    </style>
</head>
<body>
    <main class="contenedor">
        {contenido}
        <a class="volver" href="/">Volver a CRUNCH & GO</a>
    </main>
</body>
</html>"""


class handler(BaseHTTPRequestHandler):

    def enviar_html(self, contenido, estado=200):
        pagina = crear_pagina("Resultado del pedido", contenido)
        datos = pagina.encode("utf-8")

        self.send_response(estado)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)

    def do_GET(self):
        contenido = """
        <h1>🍔 CRUNCH & GO</h1>
        <p class="mensaje">
            Para calcular tu pedido, regresa al menú y completa
            el formulario de la calculadora.
        </p>
        """
        self.enviar_html(contenido)

    def do_POST(self):

        try:
            longitud = int(self.headers.get("Content-Length", 0))
            cuerpo = self.rfile.read(longitud).decode("utf-8")
            formulario = parse_qs(cuerpo)

            productos_seleccionados = formulario.get("productos", [])
            metodo_pago = formulario.get("pago", ["Efectivo"])[0]

            if not productos_seleccionados:
                raise ValueError("Debes seleccionar al menos un producto.")

            metodos_validos = [
                "Efectivo",
                "Nequi",
                "Daviplata",
                "Transferencia",
                "Tarjeta"
            ]

            if metodo_pago not in metodos_validos:
                raise ValueError("El método de pago seleccionado no es válido.")

            total = 0
            resumen = ""

            for producto_id in productos_seleccionados:

                if producto_id not in PRODUCTOS:
                    raise ValueError("Uno de los productos seleccionados no es válido.")

                nombre_campo = "cantidad_" + producto_id
                cantidad_texto = formulario.get(nombre_campo, ["1"])[0]

                try:
                    cantidad = int(cantidad_texto)
                except ValueError:
                    raise ValueError("Las cantidades deben ser números enteros.")

                if cantidad < 1 or cantidad > 99:
                    raise ValueError("Cada cantidad debe estar entre 1 y 99.")

                producto = PRODUCTOS[producto_id]
                subtotal = producto["precio"] * cantidad
                total += subtotal

                resumen += f"""
                <div class="detalle">
                    <strong>{html.escape(producto["nombre"])}</strong><br>
                    Cantidad: {cantidad}<br>
                    Precio unitario: {pesos(producto["precio"])}<br>
                    Subtotal: {pesos(subtotal)}
                </div>
                """

            contenido = f"""
            <h1>🍔 ¡Tu pedido está listo!</h1>

            <p>Este es el resumen de tu pedido en CRUNCH & GO:</p>

            {resumen}

            <div class="detalle">
                <strong>Método de pago:</strong>
                {html.escape(metodo_pago)}
            </div>

            <p class="total">Total a pagar: {pesos(total)}</p>

            <p class="mensaje">
                Gracias por elegir CRUNCH & GO.
                ¡Esperamos que disfrutes tu pedido!
            </p>
            """

            self.enviar_html(contenido)

        except ValueError as error:
            contenido = f"""
            <h1>No pudimos calcular tu pedido</h1>
            <p class="mensaje">{html.escape(str(error))}</p>
            """
            self.enviar_html(contenido, 400)

        except Exception:
            contenido = """
            <h1>Ocurrió un inconveniente</h1>
            <p class="mensaje">
                No fue posible procesar el pedido.
                Regresa al formulario e inténtalo nuevamente.
            </p>
            """
            self.enviar_html(contenido, 500)