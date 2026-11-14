"""Cliente que consulta el inventario en el otro contenedor y calcula el pedido."""
import json
import os
import sys
from pathlib import Path
from urllib.request import urlopen

from pedido import calcular_total


def main():
    ruta = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("examples/pedido.json")
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    url = os.getenv("INVENTARIO_URL", "http://inventario:8000/existencias")

    with urlopen(url, timeout=5) as respuesta:
        existencias = json.loads(respuesta.read().decode("utf-8"))

    print(f"Inventario consultado en el servicio remoto: {url}")
    resultado = calcular_total(datos["pedido"], existencias)
    resultado["total"] += 1
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
