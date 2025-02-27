#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_url(url, user_agent):
    """
    Lanza un comando curl para verificar si la URL está activa (UP)
    o inactiva (DOWN), y mide el tiempo de respuesta.
    Retorna (url, 'UP'/'DOWN', tiempo_respuesta).
    """
    cmd = [
        'curl',
        '-A', user_agent,       # User-Agent de Chrome
        '-s',                   # modo silencioso
        '-o', '/dev/null',      # no mostrar el body
        '-w', '%{time_total}',  # muestra el tiempo total de la transferencia
        '-m', '10',             # timeout de 10 segundos
        url
    ]
    
    try:
        resultado = subprocess.run(cmd, capture_output=True, text=True)
        tiempo_respuesta = resultado.stdout.strip()
        
        # returncode=0 => se completó la petición (puede no ser HTTP 200, pero sí hay respuesta).
        if resultado.returncode == 0:
            status = "UP"
        else:
            status = "DOWN"
            tiempo_respuesta = "TIMEOUT"
    except Exception:
        status = "DOWN"
        tiempo_respuesta = "0.000"

    return (url, status, tiempo_respuesta)

def main():
    parser = argparse.ArgumentParser(
        description='Verifica si los sitios web de una lista están activos o inactivos y mide el tiempo de respuesta.'
    )
    parser.add_argument('-l', '--lista', required=True, help='Archivo con la lista de URLs.')
    parser.add_argument('-o', '--out', required=True, help='Archivo de salida con los resultados.')
    args = parser.parse_args()

    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/58.0.3029.110 Safari/537.36"
    )

    # 1. Leer las URLs del archivo
    with open(args.lista, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]

    results = []

    # 2. Lanza peticiones en paralelo
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_url, url, user_agent) for url in urls]

        # 3. Mostrar resultados en tiempo real
        for future in as_completed(futures):
            url, status, tiempo = future.result()
            print(f"{url} {status} {tiempo}")
            results.append((url, status, tiempo))

    # 4. Ordenar resultados: primero DOWN, luego UP
    #    Usamos una clave que ponga DOWN como False (0) y UP como True (1) para que DOWN aparezca antes.
    results_sorted = sorted(results, key=lambda x: x[1] != 'DOWN')

    # (Opcional) Mostrar en consola la lista final ordenada:
    # print("\n--- RESULTADOS ORDENADOS (DOWN primero) ---")
    # for url, status, tiempo in results_sorted:
    #     print(f"{url} {status} {tiempo}")

    # 5. Guardar en archivo de salida
    with open(args.out, 'w', encoding='utf-8') as out_file:
        for url, status, tiempo in results_sorted:
            out_file.write(f"{url} {status} {tiempo}\n")

if __name__ == '__main__':
    main()
