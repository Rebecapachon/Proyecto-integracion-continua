"""Servicio HTTP sencillo que expone las existencias del pedido de ejemplo."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def cargar_existencias():
    ruta = Path(os.getenv("ARCHIVO_PEDIDO", "examples/pedido.json"))
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    return datos["existencias"]


class InventarioHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            respuesta = {"estado": "ok"}
            estado = 200
        elif self.path == "/existencias":
            respuesta = cargar_existencias()
            estado = 200
        else:
            respuesta = {"error": "Ruta no encontrada"}
            estado = 404

        cuerpo = json.dumps(respuesta, ensure_ascii=False).encode("utf-8")
        self.send_response(estado)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)


if __name__ == "__main__":
    puerto = int(os.getenv("PUERTO_INVENTARIO", "8000"))
    servidor = ThreadingHTTPServer(("0.0.0.0", puerto), InventarioHandler)
    print(f"Servicio de inventario activo en el puerto {puerto}", flush=True)
    servidor.serve_forever()
