#!/usr/bin/env python3
# graphhopper_directions_es.py
"""
Script de geolocalización (GraphHopper)
- Interacción en español
- Números con 2 decimales
- Salir con 's' o 'salir'
- Imprime narrativa del viaje
Requiere: pip install requests
"""

import requests
import sys
import time

# --- CONFIGURACIÓN ---
API_KEY = "55d39773-ebf1-49c6-8809-cce30c732304"   
GEOCODE_URL = "https://graphhopper.com/api/1/geocode"
ROUTE_URL = "https://graphhopper.com/api/1/route"
# ---------------------

def format_num(n):
    """Formatea número a 2 decimales. Si falla, devuelve string"""
    try:
        return f"{float(n):.2f}"
    except Exception:
        return str(n)

def es_coordenada(texto):
    """Detecta si el texto es 'lat,lon' numérico"""
    try:
        parts = [p.strip() for p in texto.split(",")]
        if len(parts) != 2:
            return False
        float(parts[0]); float(parts[1])
        return True
    except Exception:
        return False

def geocode(direccion):
    """Convierte una dirección a 'lat,lon' usando la API de geocoding de GraphHopper.
       Devuelve string 'lat,lon' o lanza excepción si falla."""
    params = {"q": direccion, "key": API_KEY, "locale": "es"}
    r = requests.get(GEOCODE_URL, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    hits = data.get("hits", [])
    if not hits:
        raise ValueError("No se encontró la dirección ingresada.")
    # Tomamos la primera coincidencia
    lat = hits[0]["point"]["lat"]
    lon = hits[0]["point"]["lon"]
    return f"{lat},{lon}"

def obtener_ruta(origen_pt, destino_pt):
    """Llama al endpoint de route. origin_pt y destino_pt son 'lat,lon' strings."""
    params = [
        ("point", origen_pt),
        ("point", destino_pt),
        ("vehicle", "car"),
        ("locale", "es"),
        ("calc_points", "true"),
        ("instructions", "true"),
        ("key", API_KEY)
    ]
    r = requests.get(ROUTE_URL, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def mostrar_resumen_por_path(ruta):
    """Imprime resumen y narrativa (instrucciones) en español con 2 decimales."""
    if not ruta or "paths" not in ruta or not ruta["paths"]:
        print("No se ha recibido una ruta válida.")
        return

    path = ruta["paths"][0]
    distancia_m = path.get("distance", 0)            # en metros
    tiempo_ms = path.get("time", 0)                  # en milisegundos

    print("\n=== Resumen del viaje ===")
    print(f" Distancia: {format_num(distancia_m/1000)} km")
    print(f" Duración estimada: {format_num(tiempo_ms/1000/60)} minutos")  # ms -> min

    # Instrucciones paso a paso (narrativa)
    instructions = path.get("instructions", [])
    if instructions:
        print("\nInstrucciones (narrativa del viaje):")
        for idx, instr in enumerate(instructions, start=1):
            text = instr.get("text", "").strip()
            dist = instr.get("distance", 0)
            time_ms = instr.get("time", 0)
            # Algunos textos vienen ya en español si locale=es
            print(f" {idx}. {text} | Dist: {format_num(dist)} m | Tiempo: {format_num(time_ms/1000)} s")
    else:
        print(" No hay instrucciones detalladas disponibles.")

def pedir_entrada(prompt):
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nSaliendo...")
        sys.exit(0)

def main():
    print("=== Planificador de rutas (GraphHopper) ===")
    print("Ingrese 's' o 'salir' en cualquier momento para terminar.")
    # Verificación básica de API_KEY
    if not API_KEY or API_KEY == "TU_GRAPHHOPPER_API_KEY":
        print("ATENCIÓN: no has definido API_KEY en el script. Edita el archivo y agrega tu token.")
        return

    while True:
        origen = pedir_entrada("\nIngrese origen (lat,lon o dirección): ")
        if origen.lower() in ("s","salir"):
            print("Saliendo. ¡Buen viaje!")
            break

        destino = pedir_entrada("Ingrese destino (lat,lon o dirección): ")
        if destino.lower() in ("s","salir"):
            print("Saliendo. ¡Buen viaje!")
            break

        # Resolver origen a lat,lon si es necesario
        try:
            if es_coordenada(origen):
                origen_pt = origen
            else:
                print("Buscando coordenadas del origen...")
                origen_pt = geocode(origen)
                print(f"Origen resuelto a: {origen_pt}")

            if es_coordenada(destino):
                destino_pt = destino
            else:
                print("Buscando coordenadas del destino...")
                destino_pt = geocode(destino)
                print(f"Destino resuelto a: {destino_pt}")

            print("Consultando GraphHopper...")
            ruta = obtener_ruta(origen_pt, destino_pt)
            mostrar_resumen_por_path(ruta)

        except requests.HTTPError as he:
            status = he.response.status_code if he.response is not None else "N/A"
            print(f"Error HTTP al consultar GraphHopper: {status}")
            try:
                print("Respuesta:", he.response.text)
            except Exception:
                pass
        except Exception as e:
            print("Ocurrió un error:", str(e))
        # pequeña pausa antes del siguiente ciclo
        time.sleep(0.2)

if __name__ == "__main__":
    main()
