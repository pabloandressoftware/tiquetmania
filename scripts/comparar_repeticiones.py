#!/usr/bin/env python3
"""Compara la corrida 1 (resultados/) con la corrida 2 (resultados_repeticion/) de cada escenario.

Escribe pruebas/experimentacion/repeticion_comparacion.json y imprime una tabla.
Criterio de "coincide": el rendimiento (peticiones/s) difiere menos del 15 %, la media
difiere menos de 1 ms o menos del 30 %, y el % de error difiere menos de 2 puntos.
El máximo no entra en el criterio: depende de una sola petición y varía mucho.
"""
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXP = os.path.join(RAIZ, "pruebas", "experimentacion")


def leer(carpeta, id_):
    ruta = os.path.join(EXP, carpeta, id_, "resumen.json")
    if not os.path.exists(ruta):
        return None
    return json.load(open(ruta, encoding="utf-8"))


def coincide(a, b):
    ta, tb = a["total"], b["total"]
    thr = abs(ta["throughput"] - tb["throughput"]) / max(ta["throughput"], 0.001) < 0.15
    dm = abs(ta["media_ms"] - tb["media_ms"])
    media = dm < 1 or dm / max(ta["media_ms"], 0.001) < 0.30
    err = abs(ta["error_pct"] - tb["error_pct"]) < 2
    return thr and media and err


def main():
    salida = []
    for id_ in sorted(os.listdir(os.path.join(EXP, "resultados"))):
        a, b = leer("resultados", id_), leer("resultados_repeticion", id_)
        if not a or not b:
            continue
        ta, tb = a["total"], b["total"]
        salida.append({"id": id_, "coincide": coincide(a, b),
                       "corrida1": {k: ta[k] for k in ("muestras", "media_ms", "p95_ms", "max_ms", "error_pct", "throughput")},
                       "corrida2": {k: tb[k] for k in ("muestras", "media_ms", "p95_ms", "max_ms", "error_pct", "throughput")}})
    json.dump(salida, open(os.path.join(EXP, "repeticion_comparacion.json"), "w"), indent=1, ensure_ascii=False)
    for s in salida:
        a, b = s["corrida1"], s["corrida2"]
        print(f'{s["id"]:22} media {a["media_ms"]:>7} / {b["media_ms"]:>7}  p95 {a["p95_ms"]:>6} / {b["p95_ms"]:>6}  '
              f'err {a["error_pct"]:>5} / {b["error_pct"]:>5}  thr {a["throughput"]:>7} / {b["throughput"]:>7}  {"OK" if s["coincide"] else "DIFERENTE"}')
    print(f'{sum(s["coincide"] for s in salida)} de {len(salida)} coinciden')


if __name__ == "__main__":
    main()
