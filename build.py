#!/usr/bin/env python3
"""
Hunt Club — build.

Hace dos cosas:

1. Sella la versión del service worker con un hash del contenido, para que al
   publicar un cambio los móviles que ya tengan la app se traigan lo nuevo.
2. Genera dist/hunt-club.html: la app entera en un solo archivo, con las
   imágenes incrustadas. Es la versión que se pasa por WhatsApp o se abre
   desde Archivos sin servidor de por medio.

    python3 build.py
"""
import base64, hashlib, pathlib, re, sys

RAIZ = pathlib.Path(__file__).parent
DIST = RAIZ / "dist"
AMBIENTES = ["villa", "casa", "monasterio", "cuartel", "cortijo", "tren", "antartida", "orbital"]


def assets():
    for n in AMBIENTES:
        yield f"assets/amb-{n}.webp"
        yield f"assets/tab-{n}.webp"
    yield "assets/icon.webp"


def comprueba():
    faltan = [p for p in list(assets()) + ["index.html", "sw.js", "manifest.webmanifest"]
              if not (RAIZ / p).exists()]
    if faltan:
        sys.exit("Faltan archivos:\n  " + "\n  ".join(faltan))


def sella_sw(html: str) -> str:
    """La versión de la caché sale del contenido: si nada cambia, no se invalida."""
    h = hashlib.sha256(html.encode())
    for p in assets():
        h.update((RAIZ / p).read_bytes())
    version = h.hexdigest()[:10]

    sw = RAIZ / "sw.js"
    texto = sw.read_text()
    nuevo = re.sub(r"const VERSION = '[^']*';", f"const VERSION = '{version}';", texto)
    if nuevo != texto:
        sw.write_text(nuevo)
        print(f"  sw.js sellado con la versión {version}")
    else:
        print(f"  sw.js ya estaba en la versión {version}")
    return version


def un_solo_archivo(html: str) -> str:
    """Mete imágenes y manifiesto dentro del HTML y quita el service worker."""
    def dato(ruta: str) -> str:
        return "data:image/webp;base64," + base64.b64encode((RAIZ / ruta).read_bytes()).decode()

    for n in AMBIENTES:
        html = html.replace(f"'assets/amb-{n}.webp'", f"'{dato(f'assets/amb-{n}.webp')}'")
        html = html.replace(f"'assets/tab-{n}.webp'", f"'{dato(f'assets/tab-{n}.webp')}'")
    html = html.replace('"assets/icon.webp"', f'"{dato("assets/icon.webp")}"')

    # sin servidor no hay ni manifiesto ni service worker que valgan
    html = html.replace('<link rel="manifest" href="manifest.webmanifest">\n', "")
    html = re.sub(
        r"/\* -+ se guarda en el móvil[^*]*-+ \*/\n"
        r"if\('serviceWorker'[^\n]*\n[^\n]*\n\n", "", html)

    sueltas = re.findall(r"assets/[\w.-]+\.webp", html)
    if sueltas:
        sys.exit("Quedan rutas sin incrustar: " + ", ".join(sorted(set(sueltas))))
    return html


def main():
    comprueba()
    html = (RAIZ / "index.html").read_text()

    print("Sellando el service worker…")
    sella_sw(html)

    print("Generando el archivo único…")
    DIST.mkdir(exist_ok=True)
    salida = DIST / "hunt-club.html"
    salida.write_text(un_solo_archivo(html))
    print(f"  {salida.relative_to(RAIZ)} · {round(salida.stat().st_size / 1024)} KB")
    print("\nListo. Para publicar: sube el repo y activa GitHub Pages sobre la rama principal.")


if __name__ == "__main__":
    main()
