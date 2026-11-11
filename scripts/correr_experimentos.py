#!/usr/bin/env python3
"""Corre los escenarios del taller de experimentación ("¿Qué pasaría si...?").

Para cada escenario: levanta la API limpia, mide CPU y memoria del equipo cada segundo,
ejecuta pruebas/experimentacion/Experimentacion.jmx en modo no-GUI con las propiedades del
escenario y deja en pruebas/experimentacion/resultados/<id>/ :
    resultados.jtl   respuestas crudas de JMeter
    reporte/         reporte HTML de JMeter (abrir index.html)
    recursos.csv     CPU y memoria por segundo (equipo completo, JMeter y API por separado)
    resumen.json     métricas ya calculadas (las usa el informe)

Uso:
    export JMETER_HOME=/ruta/a/apache-jmeter-5.6.3
    python3 scripts/correr_experimentos.py            # todos
    python3 scripts/correr_experimentos.py q1-20 q1-500
    python3 scripts/correr_experimentos.py --lista    # ver los escenarios
Si una carpeta de resultados ya existe, el escenario se salta (bórrala tú para repetirlo).
"""
import csv
import json
import os
import statistics
import subprocess
import sys
import threading
import time

import psutil

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
EXP = os.path.join(RAIZ, "pruebas", "experimentacion")
PUERTO = 8080

# id -> propiedades de JMeter (-J). Todo lo que no se nombra usa el valor por defecto del plan:
# usuarios=20, rampup=1 s, iteraciones=1, flujo=completo, timer 500 ms + hasta 1000 ms, sync=false.
# Los escenarios por tiempo usan iteraciones=-1 (repetir) y duracion=<segundos>.
T = {"duracion": 60, "iteraciones": -1}
ESCENARIOS = {
    # P1 - 20 vs 500 usuarios
    "q1-20":   dict(T, usuarios=20, rampup=10),
    "q1-500":  dict(T, usuarios=500, rampup=10),
    # P2 - ramp-up de 1 s vs 60 s
    "q2-rampup-1s":  dict(usuarios=200, rampup=1, duracion=90, iteraciones=-1),
    "q2-rampup-60s": dict(usuarios=200, rampup=60, duracion=90, iteraciones=-1),
    # P3 - con y sin temporizadores
    "q3-con-timer": dict(T, usuarios=100, rampup=10),
    "q3-sin-timer": dict(T, usuarios=100, rampup=10, timer_const=0, timer_rand=0),
    # P4 - escalones 50 -> 100 -> 250 -> 500 (cada escalón dura 30 s; temporizador corto para empujar la carga)
    "q4-escalones": dict(usuarios=50, rampup=5, duracion=120, iteraciones=-1, timer_const=50, timer_rand=100,
                         esc2=50, esc2_retraso=30, esc2_duracion=90,
                         esc3=150, esc3_retraso=60, esc3_duracion=60,
                         esc4=250, esc4_retraso=90, esc4_duracion=30, esc_rampup=5),
    # P5 - 1 minuto vs 10 minutos
    "q5-1min":  dict(usuarios=100, rampup=10, duracion=60, iteraciones=-1),
    "q5-10min": dict(usuarios=100, rampup=10, duracion=600, iteraciones=-1),
    # P6 - solo lectura (tarifas) vs crea reservas (seleccion), misma carga
    "q6-tarifas":   dict(T, usuarios=200, rampup=10, flujo="tarifas", timer_const=100, timer_rand=200),
    "q6-seleccion": dict(T, usuarios=200, rampup=10, flujo="seleccion", timer_const=100, timer_rand=200),
    # P7 - 500 usuarios crean reservas a la vez (sin pausas)
    "q7-500-reservas": dict(usuarios=500, rampup=1, iteraciones=10, flujo="seleccion", timer_const=0, timer_rand=0),
    # P8 - temporizador sincronizado vs llegada distribuida (una sola petición por usuario)
    "q8-sincronizado": dict(usuarios=500, rampup=5, iteraciones=1, flujo="seleccion", timer_const=0, timer_rand=0,
                            sync="true", sync_grupo=500),
    "q8-distribuido":  dict(usuarios=500, rampup=10, iteraciones=1, flujo="seleccion", timer_const=0, timer_rand=0),
    # P9 - totales bajo carga (+ control negativo con un CSV de totales equivocados)
    "q9-totales":  dict(usuarios=200, rampup=10, duracion=60, iteraciones=-1, timer_const=100, timer_rand=200),
    "q9-control-negativo": dict(usuarios=20, rampup=1, iteraciones=2, timer_const=0, timer_rand=0,
                                csv=os.path.join(EXP, "datos_totales_incorrectos.csv")),
    # P10 - 500 usuarios sostenidos mirando CPU y memoria
    "q10-500": dict(usuarios=500, rampup=30, duracion=180, iteraciones=-1),
    # P10 (extra) - los mismos 500 usuarios pero con pausas cortas, para llevar la API al límite
    "q10-500-presion": dict(usuarios=500, rampup=30, duracion=180, iteraciones=-1, timer_const=50, timer_rand=100),
}


def muestrear(proc_jmeter, proc_api, parar, ruta):
    """Escribe una fila por segundo con CPU y memoria."""
    psutil.cpu_percent(None)
    par_j, par_a = {}, {}

    def uso(p, cache):
        try:
            procs = [p] + p.children(recursive=True)
            cpu = mem = 0.0
            for q in procs:
                c = cache.setdefault(q.pid, q)
                cpu += c.cpu_percent(None)
                mem += c.memory_info().rss
            return cpu, mem / 2**20
        except psutil.Error:
            return 0.0, 0.0

    with open(ruta, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t_seg", "cpu_equipo_pct", "mem_equipo_pct", "mem_equipo_usada_mb", "cpu_jmeter_pct", "mem_jmeter_mb", "cpu_api_pct", "mem_api_mb"])
        t0 = time.time()
        while not parar.is_set():
            time.sleep(1)
            vm = psutil.virtual_memory()
            cj, mj = uso(proc_jmeter, par_j) if proc_jmeter else (0, 0)
            ca, ma = uso(proc_api, par_a)
            w.writerow([round(time.time() - t0), psutil.cpu_percent(None), vm.percent, round((vm.total - vm.available) / 2**20),
                        round(cj, 1), round(mj, 1), round(ca, 1), round(ma, 1)])
            f.flush()


def percentil(valores, p):
    v = sorted(valores)
    return v[min(len(v) - 1, int(len(v) * p / 100))] if v else 0


def resumir(carpeta):
    filas = list(csv.DictReader(open(os.path.join(carpeta, "resultados.jtl"), encoding="utf-8")))
    t0 = min(int(f["timeStamp"]) for f in filas)
    fin = max(int(f["timeStamp"]) + int(f["elapsed"]) for f in filas)
    dur = (fin - t0) / 1000

    def metricas(fs):
        e = [int(f["elapsed"]) for f in fs]
        if not e:
            return {}
        ini = min(int(f["timeStamp"]) for f in fs)
        fin_ = max(int(f["timeStamp"]) + int(f["elapsed"]) for f in fs)
        d = max((fin_ - ini) / 1000, 0.001)   # del primer envío a la última respuesta
        return {"muestras": len(fs), "media_ms": round(statistics.mean(e), 1), "p90_ms": percentil(e, 90), "p95_ms": percentil(e, 95),
                "p99_ms": percentil(e, 99), "max_ms": max(e), "error_pct": round(100 * sum(f["success"] != "true" for f in fs) / len(fs), 2),
                "throughput": round(len(fs) / d, 1)}

    etiquetas = sorted({f["label"] for f in filas})
    # serie en el tiempo: ventanas de 10 s
    ventana = 10
    cubos = {}
    for f in filas:
        cubos.setdefault((int(f["timeStamp"]) - t0) // 1000 // ventana, []).append(f)
    serie = []
    for k in sorted(cubos):
        fs = cubos[k]
        e = [int(x["elapsed"]) for x in fs]
        serie.append({"desde_s": k * ventana, "muestras": len(fs), "peticiones_por_s": round(len(fs) / ventana, 1),
                      "media_ms": round(statistics.mean(e), 1), "p95_ms": percentil(e, 95), "max_ms": max(e),
                      "errores": sum(x["success"] != "true" for x in fs), "hilos_activos": max(int(x["allThreads"]) for x in fs)})
    primeros = [f for f in filas if int(f["timeStamp"]) - t0 < 5000]
    resumen = {"duracion_s": round(dur, 1), "total": metricas(filas), "por_peticion": {l: metricas([f for f in filas if f["label"] == l]) for l in etiquetas},
               "primeros_5s": metricas(primeros), "hilos_max": max(int(f["allThreads"]) for f in filas), "serie_10s": serie,
               "codigos": {c: sum(f["responseCode"] == c for f in filas) for c in sorted({f["responseCode"] for f in filas})}}
    # recursos
    ruta = os.path.join(carpeta, "recursos.csv")
    if os.path.exists(ruta):
        r = list(csv.DictReader(open(ruta)))
        if r:
            col = lambda c: [float(x[c]) for x in r]
            resumen["recursos"] = {c: {"media": round(statistics.mean(col(c)), 1), "max": round(max(col(c)), 1)}
                                   for c in ("cpu_equipo_pct", "mem_equipo_pct", "mem_equipo_usada_mb", "cpu_jmeter_pct", "mem_jmeter_mb", "cpu_api_pct", "mem_api_mb")}
            resumen["recursos"]["mem_equipo_usada_mb"]["inicio"] = col("mem_equipo_usada_mb")[0]
            resumen["recursos"]["mem_equipo_usada_mb"]["fin"] = col("mem_equipo_usada_mb")[-1]
            resumen["recursos"]["mem_api_mb"]["inicio"] = col("mem_api_mb")[0]
            resumen["recursos"]["mem_api_mb"]["fin"] = col("mem_api_mb")[-1]
    with open(os.path.join(carpeta, "resumen.json"), "w") as f:
        json.dump(resumen, f, indent=1, ensure_ascii=False)
    return resumen


def correr(id_, props):
    carpeta = os.path.join(EXP, "resultados", id_)
    if os.path.exists(carpeta):
        print(f"[{id_}] ya existe resultados/{id_}, se salta")
        return
    os.makedirs(carpeta)
    jm_home = os.environ.get("JMETER_HOME", "")
    jmeter = os.path.join(jm_home, "bin", "jmeter") if jm_home else "jmeter"
    api = subprocess.Popen([sys.executable, "-I", os.path.join(RAIZ, "api", "ticketmania_simple.py")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.5)
    pj = {"host": "127.0.0.1", "puerto": PUERTO, "csv": os.path.join(EXP, "datos.csv"), **props}
    cmd = [jmeter, "-n", "-t", os.path.join(EXP, "Experimentacion.jmx"), "-l", os.path.join(carpeta, "resultados.jtl"),
           "-e", "-o", os.path.join(carpeta, "reporte"), "-j", os.path.join(carpeta, "jmeter.log")] + [f"-J{k}={v}" for k, v in pj.items()]
    print(f"[{id_}] {' '.join(f'{k}={v}' for k, v in props.items())}", flush=True)
    t0 = time.time()
    proc = subprocess.Popen(cmd, stdout=open(os.path.join(carpeta, "salida.txt"), "w"), stderr=subprocess.STDOUT)
    parar = threading.Event()
    hilo = threading.Thread(target=muestrear, args=(psutil.Process(proc.pid), psutil.Process(api.pid), parar, os.path.join(carpeta, "recursos.csv")))
    hilo.start()
    proc.wait()
    parar.set()
    hilo.join()
    api.terminate()
    api.wait()
    res = resumir(carpeta)
    t = res["total"]
    print(f"[{id_}] {time.time() - t0:.0f}s | {t['muestras']} muestras | media {t['media_ms']} ms | p95 {t['p95_ms']} | max {t['max_ms']} | "
          f"error {t['error_pct']}% | {t['throughput']}/s", flush=True)


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--lista" in args:
        for k, v in ESCENARIOS.items():
            print(k, v)
        sys.exit(0)
    for id_ in args or list(ESCENARIOS):
        correr(id_, ESCENARIOS[id_])
