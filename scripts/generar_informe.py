#!/usr/bin/env python3
"""Arma el informe del taller de experimentación (Word) a partir de pruebas/experimentacion/resultados/.

Requiere:  pip install matplotlib python-docx   y Google Chrome (para las capturas de los reportes).
Uso:       python3 scripts/generar_informe.py
Salida:    pruebas/experimentacion/Informe_Experimentacion.docx  (+ pruebas/experimentacion/informe_img/*.png)
"""
import csv
import json
import os
import subprocess

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt, RGBColor

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
EXP = os.path.join(RAIZ, "pruebas", "experimentacion")
RES = os.path.join(EXP, "resultados")
IMG = os.path.join(EXP, "informe_img")
os.makedirs(IMG, exist_ok=True)

AZUL, ROJO, VERDE, GRIS = "#2563eb", "#dc2626", "#16a34a", "#6b7280"
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.alpha": .25})


# ------------------------------------------------------------------ datos
def resumen(i):
    return json.load(open(os.path.join(RES, i, "resumen.json")))


def jtl(i):
    """Filas del .jtl con tiempos relativos (s) al primer envío."""
    filas = list(csv.DictReader(open(os.path.join(RES, i, "resultados.jtl"), encoding="utf-8")))
    t0 = min(int(f["timeStamp"]) for f in filas)
    for f in filas:
        f["t"] = (int(f["timeStamp"]) - t0) / 1000
        f["ms"] = int(f["elapsed"])
        f["ok"] = f["success"] == "true"
    return filas


def recursos(i):
    return list(csv.DictReader(open(os.path.join(RES, i, "recursos.csv"))))


def por_ventana(filas, ancho):
    """Agrupa filas en ventanas de `ancho` s -> lista (inicio, filas)."""
    g = {}
    for f in filas:
        g.setdefault(int(f["t"] // ancho), []).append(f)
    return [(k * ancho, g[k]) for k in sorted(g)]


def pct(v, p):
    v = sorted(v)
    return v[min(len(v) - 1, int(len(v) * p / 100))] if v else 0


def estable(i, hasta):
    """Rendimiento (peticiones/s) y media (ms) solo hasta `hasta` s, para que las respuestas rezagadas del final no distorsionen."""
    fs = [f for f in jtl(i) if f["t"] <= hasta]
    return len(fs) / hasta, sum(f["ms"] for f in fs) / len(fs)


def guardar(fig, nombre):
    ruta = os.path.join(IMG, nombre)
    fig.savefig(ruta, dpi=170, bbox_inches="tight")
    plt.close(fig)
    return ruta


# ---------------------------------------------------------------- gráficas
def fig_q1():
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
    for i, c, n in (("q1-20", AZUL, "20 usuarios"), ("q1-500", ROJO, "500 usuarios")):
        w = por_ventana(jtl(i), 5)
        ax[0].plot([a for a, _ in w], [len(f) / 5 for _, f in w], color=c, label=n, marker="o", ms=3)
        ax[1].plot([a for a, _ in w], [sum(x["ms"] for x in f) / len(f) for _, f in w], color=c, label=n, marker="o", ms=3)
    ax[0].set(title="Throughput (peticiones/s)", xlabel="segundos"); ax[1].set(title="Tiempo de respuesta medio (ms)", xlabel="segundos", ylim=(0, 6))
    ax[0].legend()
    return guardar(fig, "q1.png")


def fig_q2():
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
    for i, c, n in (("q2-rampup-1s", ROJO, "subida de 1 s"), ("q2-rampup-60s", AZUL, "subida de 60 s")):
        w = [(a, f) for a, f in por_ventana(jtl(i), 1) if a <= 30]
        ax[0].plot([a for a, _ in w], [max(x["ms"] for x in f) for _, f in w], color=c, label=n)
        ax[1].plot([a for a, _ in w], [len(f) for _, f in w], color=c, label=n)
    ax[0].set(title="Tiempo máximo por segundo (ms)", xlabel="segundos desde el inicio"); ax[1].set(title="Peticiones por segundo", xlabel="segundos desde el inicio")
    ax[0].legend()
    return guardar(fig, "q2.png")


def fig_q3():
    fig, ax = plt.subplots(1, 3, figsize=(9.5, 3))
    ids = ("q3-con-timer", "q3-sin-timer")
    tp = [estable(i, 60)[0] for i in ids]
    ax[0].bar(["con\ntemporizador", "sin\ntemporizador"], tp, color=[AZUL, ROJO]); ax[0].set_title("Throughput (peticiones/s)\nprimeros 60 s")
    ax[1].bar(["con", "sin"], [estable(i, 60)[1] for i in ids], color=[AZUL, ROJO]); ax[1].set_title("Tiempo medio (ms)\nprimeros 60 s")
    ax[2].bar(["con", "sin"], [resumen(i)["recursos"]["cpu_api_pct"]["max"] / 100 for i in ids], color=[AZUL, ROJO]); ax[2].set_title("Núcleos de CPU que usa la API\n(máximo)")
    for a, v in zip(ax, (tp, [estable(i, 60)[1] for i in ids], [resumen(i)["recursos"]["cpu_api_pct"]["max"] / 100 for i in ids])):
        for k, x in enumerate(v):
            a.text(k, x, f"{x:.1f}", ha="center", va="bottom")
    return guardar(fig, "q3.png")


def fig_q4():
    r = resumen("q4-escalones")["serie_10s"]
    fig, ax = plt.subplots(figsize=(9, 3.4))
    x = [s["desde_s"] for s in r]
    ax.bar(x, [s["peticiones_por_s"] for s in r], width=8, color=AZUL, align="edge", label="Throughput (peticiones/s)")
    ax.set(xlabel="segundos", ylabel="peticiones/s", ylim=(0, 2900))
    for k, (tm, u) in enumerate(((0, 50), (30, 100), (60, 250), (90, 500))):
        ax.axvline(tm, color=GRIS, ls="--", lw=.8); ax.text(tm + .5, ax.get_ylim()[1] * .97, f"{u} usuarios", va="top", fontsize=8)
    ax2 = ax.twinx(); ax2.grid(False)
    ax2.plot([a + 4 for a in x], [s["p95_ms"] for s in r], color=ROJO, marker="o", label="p95 (ms)")
    ax2.set_ylabel("p95 (ms)", color=ROJO)
    return guardar(fig, "q4.png")


def fig_q5():
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
    for i, c, n in (("q5-10min", AZUL, "10 minutos"), ("q5-1min", ROJO, "1 minuto")):
        w = por_ventana(jtl(i), 30 if i == "q5-10min" else 10)
        ax[0].plot([a / 60 for a, _ in w], [sum(x["ms"] for x in f) / len(f) for _, f in w], color=c, label=n, marker="o", ms=3)
        r = recursos(i)
        ax[1].plot([int(x["t_seg"]) / 60 for x in r], [float(x["mem_api_mb"]) for x in r], color=c, label=n)
    ax[0].set(title="Tiempo de respuesta medio (ms)", xlabel="minutos", ylim=(0, 6)); ax[0].legend()
    ax[1].set(title="Memoria de la API (MB)", xlabel="minutos", ylim=(0, 40))
    return guardar(fig, "q5.png")


def fig_q6():
    fig, ax = plt.subplots(1, 3, figsize=(9.5, 3))
    ids = (("q6-tarifas", "Tarifas", AZUL), ("q6-seleccion", "SeleccionTarifaYCantidad", ROJO))
    for a, (campo, tit) in zip(ax, (("media_ms", "Tiempo medio (ms)"), ("p99_ms", "p99 (ms)"), ("throughput", "Throughput (peticiones/s)"))):
        v = [resumen(i)["por_peticion"][l][campo] for i, l, _ in ids]
        a.bar(["Tarifas\n(lectura)", "Selección\n(crea reserva)"], v, color=[c for *_, c in ids]); a.set_title(tit)
        for k, x in enumerate(v):
            a.text(k, x, f"{x}", ha="center", va="bottom")
    return guardar(fig, "q6.png")


def fig_q7():
    f = jtl("q7-500-reservas")
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
    ax[0].hist([x["ms"] for x in f if x["ok"]], bins=[1, 2, 5, 10, 50, 100, 500, 1000, 2000, 5000, 10000, 120000], color=AZUL)
    ax[0].set_xscale("log"); ax[0].set(title="Tiempo de respuesta de las exitosas (ms)", xlabel="ms (escala log)", ylabel="peticiones")
    w = por_ventana(f, 5)
    ax[1].bar([a for a, _ in w], [sum(not x["ok"] for x in g) for _, g in w], width=4, color=ROJO, align="edge")
    ax[1].set(title="Peticiones fallidas (Connection reset)", xlabel="segundos", ylabel="fallidas por ventana de 5 s")
    return guardar(fig, "q7.png")


def fig_q8():
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
    for i, c, n in (("q8-sincronizado", ROJO, "sincronizado"), ("q8-distribuido", AZUL, "distribuido")):
        f = jtl(i)
        w = por_ventana(f, 1)
        d = -.2 if i == "q8-sincronizado" else .2
        ax[0].bar([a + d for a, _ in w], [len(g) for _, g in w], width=.4, color=c, label=n)
    ax[0].set(title="Peticiones ENVIADAS por segundo", xlabel="segundos", ylabel="peticiones"); ax[0].legend()
    nombres, p50, p95, mx = [], [], [], []
    for i, n in (("q8-sincronizado", "sincronizado"), ("q8-distribuido", "distribuido")):
        v = [x["ms"] for x in jtl(i) if x["ok"]]
        nombres.append(n); p50.append(pct(v, 50)); p95.append(pct(v, 95)); mx.append(max(v))
    xs = range(2)
    ax[1].bar([k - .27 for k in xs], p50, .27, label="mediana", color=VERDE); ax[1].bar(xs, p95, .27, label="p95", color=AZUL); ax[1].bar([k + .27 for k in xs], mx, .27, label="máximo", color=ROJO)
    ax[1].set_xticks(list(xs)); ax[1].set_xticklabels(nombres); ax[1].set_yscale("log"); ax[1].set(title="Tiempo de respuesta de las exitosas (ms, log)"); ax[1].legend()
    return guardar(fig, "q8.png")


def fig_q9():
    fig, ax = plt.subplots(figsize=(5.5, 3))
    datos = [("Bajo carga\n(CSV correcto)", resumen("q9-totales")["total"]["error_pct"]), ("Control negativo\n(2 de 4 filas mal)", resumen("q9-control-negativo")["total"]["error_pct"])]
    ax.bar([d[0] for d in datos], [d[1] for d in datos], color=[VERDE, ROJO])
    for k, (_, v) in enumerate(datos):
        ax.text(k, v, f"{v:.2f} %", ha="center", va="bottom")
    ax.set(title="% de peticiones que fallan la validación del total", ylim=(0, 40))
    return guardar(fig, "q9.png")


def fig_q10():
    fig, ax = plt.subplots(2, 2, figsize=(9.5, 5.4), sharex="col")
    for col, (i, tit) in enumerate((("q10-500", "500 usuarios, pausas normales"), ("q10-500-presion", "500 usuarios, pausas cortas"))):
        r = recursos(i)
        x = [int(a["t_seg"]) for a in r]
        ax[0][col].plot(x, [float(a["cpu_equipo_pct"]) for a in r], color=GRIS, label="equipo completo (% de 16 núcleos)")
        ax[0][col].plot(x, [float(a["cpu_api_pct"]) for a in r], color=ROJO, label="API (% de 1 núcleo)")
        ax[0][col].plot(x, [float(a["cpu_jmeter_pct"]) / 4 for a in r], color=AZUL, label="JMeter (% de 4 núcleos)")
        ax[0][col].set(title=tit, ylabel="CPU (%)"); ax[0][col].set_ylim(0, 160)
        w = por_ventana(jtl(i), 5)
        ax[1][col].plot([a for a, _ in w], [sum(g["ms"] for g in f) / len(f) for _, f in w], color=ROJO, label="media")
        ax[1][col].plot([a for a, _ in w], [pct([g["ms"] for g in f], 95) for _, f in w], color=AZUL, label="p95")
        ax[1][col].set(xlabel="segundos", ylabel="respuesta (ms)")
        if col == 1:
            ax[1][col].set_yscale("log")
        else:
            ax[1][col].set_ylim(0, 4)
    ax[0][0].legend(fontsize=7, loc="upper left"); ax[1][0].legend(fontsize=7)
    return guardar(fig, "q10.png")


def fig_q10_mem():
    fig, ax = plt.subplots(figsize=(7, 2.8))
    for i, c, n in (("q10-500", AZUL, "pausas normales"), ("q10-500-presion", ROJO, "pausas cortas")):
        r = recursos(i)
        ax.plot([int(a["t_seg"]) for a in r], [float(a["mem_jmeter_mb"]) for a in r], color=c, label=f"JMeter, {n}")
    ax.set(title="Memoria de JMeter (MB)", xlabel="segundos"); ax.legend(fontsize=7)
    return guardar(fig, "q10_mem.png")


def ficha(nombre, filas):
    """Tabla del escenario como imagen (hilos, subida, duración, temporizadores...)."""
    import textwrap
    filas = [[a, "\n".join(textwrap.wrap(v, 62, break_long_words=False, break_on_hyphens=False))] for a, v in filas]
    lineas = [max(1, v.count("\n") + 1) for _, v in filas]
    fig, ax = plt.subplots(figsize=(8.4, .3 * (sum(lineas) + 1) + .25))
    ax.axis("off")
    t = ax.table(cellText=filas, colLabels=["Parámetro", "Valor"], loc="center", cellLoc="left", colWidths=[.27, .73])
    t.auto_set_font_size(False); t.set_fontsize(8.5)
    total = sum(lineas) + 1
    for (r, c), cel in t.get_celld().items():
        cel.set_edgecolor("#d1d5db")
        cel.set_height(((1 if r == 0 else lineas[r - 1]) / total) * .98)
        if r == 0:
            cel.set_facecolor("#1e3a8a"); cel.get_text().set_color("white"); cel.get_text().set_weight("bold")
    return guardar(fig, f"ficha_{nombre}.png")


def captura_reporte(i, ancho=1400, alto=1250):
    """Captura de pantalla del reporte HTML de JMeter (index.html) con Chrome sin ventana."""
    destino = os.path.join(IMG, f"reporte_{i}.png")
    if not os.path.exists(destino):
        url = "file://" + os.path.join(RES, i, "reporte", "index.html")
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", f"--window-size={ancho},{alto}",
                        "--virtual-time-budget=8000", f"--screenshot={destino}", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    return destino


# ------------------------------------------------------------------- Word
def tabla(doc, encabezado, filas, anchos=None, tam=8.5):
    t = doc.add_table(rows=1, cols=len(encabezado))
    t.style = "Light Grid Accent 1"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for k, h in enumerate(encabezado):
        t.rows[0].cells[k].text = h
    for fila in filas:
        c = t.add_row().cells
        for k, v in enumerate(fila):
            c[k].text = str(v)
    for r in t.rows:
        for k, c in enumerate(r.cells):
            for p in c.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(tam)
            if anchos:
                c.width = Cm(anchos[k])
    doc.add_paragraph()
    return t


def parrafo(doc, texto, negrita_inicio=None, cursiva=False):
    p = doc.add_paragraph()
    if negrita_inicio:
        p.add_run(negrita_inicio).bold = True
    r = p.add_run(texto)
    r.italic = cursiva
    return p


def imagen(doc, ruta, pie, ancho=16):
    doc.add_picture(ruta, width=Cm(ancho))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = doc.add_paragraph(pie)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p.runs:
        r.italic = True; r.font.size = Pt(8); r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)


def fmt(x, d=1):
    return f"{x:,.{d}f}".replace(",", " ") if isinstance(x, float) else f"{x:,}".replace(",", " ")


def met_fila(i, nombre, hasta=None):
    r = resumen(i)["total"]
    thr = r["throughput"] if not hasta else round(estable(i, hasta)[0], 1)
    return [nombre, fmt(r["muestras"]), fmt(r["media_ms"]), fmt(r["p95_ms"]), fmt(r["p99_ms"]), fmt(r["max_ms"]), f'{r["error_pct"]:.2f} %', fmt(thr)]


ENC = ["Escenario", "Muestras", "Media (ms)", "p95 (ms)", "p99 (ms)", "Máx (ms)", "% Error", "Rendimiento (peticiones/s)"]
ANCHOS = [3.6, 1.6, 1.6, 1.4, 1.4, 1.8, 1.5, 2.6]


def pregunta(doc, num, categoria, enunciado, ficha_img, reportes, tablas, figuras, respuesta, limites):
    doc.add_heading(f"Pregunta {num} · {categoria}", level=1)
    parrafo(doc, enunciado, "¿Qué pasaría si... ", cursiva=True)
    doc.add_heading("Escenario", level=2)
    for r in ficha_img:
        imagen(doc, r[0], r[1], 12.5)
    doc.add_heading("Resultados observados", level=2)
    for enc, filas, anch in tablas:
        tabla(doc, enc, filas, anch)
    for ruta, pie in figuras:
        imagen(doc, ruta, pie, 16)
    for ruta, pie in reportes:
        imagen(doc, ruta, pie, 16)
    doc.add_heading("Mi respuesta", level=2)
    for t in respuesta:
        parrafo(doc, t)
    doc.add_heading("Qué no pude medir o qué cambió el resultado", level=2)
    for t in limites:
        doc.add_paragraph(t, style="List Bullet")
    doc.add_page_break()


def construir():
    R = resumen
    doc = Document()
    st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10.5)
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2.2); s.top_margin = s.bottom_margin = Cm(2)

    # ---------------- portada
    for _ in range(5):
        doc.add_paragraph()
    t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run("Taller de experimentación con JMeter\n“¿Qué pasaría si...?”"); r.bold = True; r.font.size = Pt(26); r.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
    t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t.add_run("API Tiquetmania · carga, estrés y concurrencia").font.size = Pt(14)
    for _ in range(3):
        doc.add_paragraph()
    t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t.add_run("Pablo Guzmán\nAutomatización de Pruebas 2026-2\nNoviembre de 2026").font.size = Pt(12)
    for _ in range(3):
        doc.add_paragraph()
    t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t.add_run("Repositorio: github.com/pabloandressoftware/tiquetmania").font.size = Pt(10)
    doc.add_page_break()

    # ---------------- cómo se hizo
    doc.add_heading("Cómo se hicieron las pruebas", level=1)
    parrafo(doc, "Las 10 preguntas se probaron con un solo archivo, pruebas/experimentacion/Experimentacion.jmx. No se modifica el plan del despliegue (pruebas/jmeter/Ticketmania.jmx). "
                 "El plan se configura con propiedades de JMeter (-Jusuarios, -Jrampup, -Jduracion, -Jflujo, -Jtimer_const, -Jsync...), así cada escenario es una ejecución distinta del mismo archivo. "
                 "Cada ejecución se hizo en modo no-GUI, con la API recién iniciada, y generó su reporte HTML.")
    doc.add_heading("Qué contiene el plan", level=2)
    for x in ("Configuración del CSV Data Set con datos.csv: 32 compras (tarifa, cantidad, total_esperado). El total esperado es precio × cantidad.",
              "Valores por defecto de la petición HTTP (127.0.0.1:8080) y Gestor de Cabecera con Accept y Content-Type JSON.",
              "Flujo: Tarifas (GET) → SeleccionTarifaYCantidad (POST, JSON Extractor de num_reserva) → Pago (POST). Un controlador If permite probar solo Tarifas, solo Selección o el flujo completo.",
              "Aserciones: código 201/200, estado APROBADO y total = precio × cantidad (JSON Assertion contra la columna total_esperado).",
              "Temporizador Aleatorio Uniforme (500 ms + hasta 1000 ms por defecto) y Temporizador sincronizado opcional (pregunta 8).",
              "Cuatro Grupos de Hilos: uno principal y tres de escalones que se suman con un retraso (pregunta 4). Un grupo con 0 hilos no corre."):
        doc.add_paragraph(x, style="List Bullet")
    doc.add_heading("Equipo y limitaciones generales", level=2)
    parrafo(doc, "Todo corrió en mi computador: Ubuntu Linux, 16 núcleos y 31 GB de RAM, Java 21, JMeter 5.6.3 y la API de la profesora (Python, un solo proceso). "
                 "JMeter y la API comparten el equipo, así que el resultado mide a los dos juntos. Esa es la principal limitación y aplica a todas las preguntas.", "Limitación: ")
    for x in ("Para CPU y memoria no usé PerfMon con ServerAgent. Escribí un muestreador propio (scripts/correr_experimentos.py, librería psutil) que anota CPU y memoria cada segundo del equipo completo, de JMeter y de la API. "
              "Mide lo mismo que PerfMon, pero no es el plugin que pide la guía.",
              "Para la pregunta 4 usé cuatro Grupos de Hilos estándar con retraso de inicio en lugar del Ultimate Thread Group, que es un plugin. El resultado es el mismo escalonado: 50, 100, 250 y 500 usuarios.",
              "Los valores son de una sola ejecución por escenario. Son una referencia, no un promedio de varias repeticiones.",
              "Las capturas de los reportes son del reporte HTML de JMeter. La captura del escenario es una tabla con los parámetros exactos de cada ejecución."):
        doc.add_paragraph(x, style="List Bullet")
    doc.add_heading("Resumen de los 18 escenarios", level=2)
    ids = [("q1-20", "P1 · 20 usuarios"), ("q1-500", "P1 · 500 usuarios"), ("q2-rampup-1s", "P2 · subida 1 s"), ("q2-rampup-60s", "P2 · subida 60 s"),
           ("q3-con-timer", "P3 · con temporizador"), ("q3-sin-timer", "P3 · sin temporizador"), ("q4-escalones", "P4 · escalones"), ("q5-1min", "P5 · 1 minuto"),
           ("q5-10min", "P5 · 10 minutos"), ("q6-tarifas", "P6 · /api/tarifas"), ("q6-seleccion", "P6 · /api/seleccion"), ("q7-500-reservas", "P7 · 500 reservas a la vez"),
           ("q8-sincronizado", "P8 · sincronizado"), ("q8-distribuido", "P8 · distribuido"), ("q9-totales", "P9 · totales bajo carga"), ("q9-control-negativo", "P9 · control negativo"),
           ("q10-500", "P10 · 500 usuarios"), ("q10-500-presion", "P10 · 500 con pausas cortas")]
    tabla(doc, ENC, [met_fila(i, n) for i, n in ids], ANCHOS, 7.5)
    parrafo(doc, "El rendimiento de esta tabla es peticiones ÷ tiempo desde el primer envío hasta la última respuesta. En los escenarios con respuestas muy lentas al final "
                 "(P3 sin temporizador, P4, P7, P8) esa cuenta se baja porque la prueba se alarga; en cada pregunta uso el rendimiento de los primeros 60 s cuando hace falta.", cursiva=True)
    doc.add_page_break()

    def f_(**kw):
        return [[k.replace("_", " "), str(v)] for k, v in kw.items()]

    # ------------------------------------------------------------ P1
    a, b = R("q1-20"), R("q1-500")
    pregunta(doc, 1, "Carga",
             "subo de 20 a 500 usuarios? ¿Cambia el throughput, el tiempo de respuesta o ambos?",
             [(ficha("q1", [["Hilos (usuarios)", "20 y 500 (dos ejecuciones)"], ["Periodo de subida", "10 s"], ["Duración", "60 s (bucle infinito, scheduler 60 s)"],
                            ["Temporizador", "Aleatorio Uniforme: 500 ms + hasta 1000 ms"], ["Flujo", "Tarifas → Selección → Pago"], ["Propiedades", "-Jusuarios=20|500 -Jrampup=10 -Jduracion=60 -Jiteraciones=-1"]]),
               "Configuración del escenario de la pregunta 1.")],
             [(captura_reporte("q1-500"), "Reporte HTML de JMeter, 500 usuarios.")],
             [(ENC, [met_fila("q1-20", "20 usuarios"), met_fila("q1-500", "500 usuarios")], ANCHOS)],
             [(fig_q1(), "Throughput y tiempo de respuesta cada 5 s. El throughput se multiplica por 25; el tiempo de respuesta no cambia.")],
             [f"Cambia el throughput y el tiempo de respuesta se mantiene. Con 20 usuarios la API completó unas {a['serie_10s'][2]['peticiones_por_s']:.0f} peticiones por segundo y con 500 usuarios unas {b['serie_10s'][2]['peticiones_por_s']:.0f}. "
              f"Son 25 veces más usuarios y casi 25 veces más peticiones. El tiempo medio de respuesta quedó en {a['total']['media_ms']} ms con 20 usuarios y {b['total']['media_ms']} ms con 500, y el p95 en {a['total']['p95_ms']} y {b['total']['p95_ms']} ms.",
              "Esto pasa porque 500 usuarios con pausas de 1 s casi no presionan a la API: ella puede con muchas más peticiones por segundo (la pregunta 4 muestra que aguanta unas 2 300). "
              f"El único cambio visible está en el máximo: con 500 usuarios hay unas pocas peticiones de cerca de 1 segundo ({b['total']['max_ms']} ms) mientras suben los usuarios. Esas pocas peticiones no mueven el promedio. "
              "Mi hipótesis es que son conexiones nuevas que el servidor no alcanzó a aceptar y se reintentaron al segundo, pero no lo comprobé."],
             ["Los dos escenarios usan pausas, así que la carga está controlada por los temporizadores. Sin pausas el resultado sería otro (pregunta 3).",
              "API y JMeter comparten el equipo: con 500 usuarios JMeter usó hasta 3,9 núcleos y la API apenas 0,5."])

    # ------------------------------------------------------------ P2
    f1, f2 = jtl("q2-rampup-1s"), jtl("q2-rampup-60s")
    lentas1 = sum(1 for x in f1 if x["t"] < 5 and x["ms"] > 500)
    lentas2 = sum(1 for x in f2 if x["t"] < 5 and x["ms"] > 500)
    pregunta(doc, 2, "Carga",
             "el ramp-up pasa de 1 segundo a 60 segundos? ¿Cambia el pico inicial del reporte?",
             [(ficha("q2", [["Hilos (usuarios)", "200"], ["Periodo de subida", "1 s y 60 s (dos ejecuciones)"], ["Duración", "90 s (bucle infinito)"],
                            ["Temporizador", "Aleatorio Uniforme: 500 ms + hasta 1000 ms"], ["Flujo", "Tarifas → Selección → Pago"], ["Propiedades", "-Jusuarios=200 -Jrampup=1|60 -Jduracion=90 -Jiteraciones=-1"]]),
               "Configuración del escenario de la pregunta 2.")],
             [(captura_reporte("q2-rampup-1s"), "Reporte de JMeter, subida de 1 s."), (captura_reporte("q2-rampup-60s"), "Reporte de JMeter, subida de 60 s.")],
             [(["Escenario", "Máx. en los primeros 5 s (ms)", "Peticiones > 500 ms en los primeros 5 s", "Media (ms)", "p95 (ms)", "Máx. total (ms)", "% Error"],
               [["Subida de 1 s", R("q2-rampup-1s")["primeros_5s"]["max_ms"], lentas1, R("q2-rampup-1s")["total"]["media_ms"], R("q2-rampup-1s")["total"]["p95_ms"], R("q2-rampup-1s")["total"]["max_ms"], "0.00 %"],
                ["Subida de 60 s", R("q2-rampup-60s")["primeros_5s"]["max_ms"], lentas2, R("q2-rampup-60s")["total"]["media_ms"], R("q2-rampup-60s")["total"]["p95_ms"], R("q2-rampup-60s")["total"]["max_ms"], "0.00 %"]], None)],
             [(fig_q2(), "Primeros 30 s. Con subida de 1 s el máximo salta a más de 1 s al inicio; con 60 s la carga sube de forma gradual.")],
             [f"Sí, cambia el pico inicial, pero es un pico de pocas peticiones. Con subida de 1 s los 200 usuarios llegan casi juntos: la carga sube de golpe a {R('q2-rampup-1s')['serie_10s'][0]['peticiones_por_s']:.0f} peticiones por segundo y en los primeros 5 segundos aparece un pico: {lentas1} petición{"es" if lentas1 != 1 else ""} de más de medio segundo "
              f"(la más lenta, {R('q2-rampup-1s')['primeros_5s']['max_ms']} ms). Con subida de 60 s la carga sube en rampa, de unas 21 a unas 190 peticiones por segundo, y el máximo de los primeros 5 s es de {R('q2-rampup-60s')['primeros_5s']['max_ms']} ms.",
              "Después de ese arranque los dos escenarios se comportan igual: media de 1,5 ms y p95 de 2 ms. La subida corta no hace que la API falle, solo hace visible el momento de arranque. "
              "Con subida larga ese pico desaparece, pero también tarda cerca de un minuto en llegar a la carga completa."],
             ["En el reporte el pico se ve en la gráfica de tiempos de respuesta en el tiempo, no en el promedio general.",
              "No sé exactamente qué causa el pico de 1 segundo (puede ser el reintento de conexiones nuevas). No lo medí con herramientas de red."])

    # ------------------------------------------------------------ P3
    tc, ts = estable("q3-con-timer", 60), estable("q3-sin-timer", 60)
    pregunta(doc, 3, "Carga",
             "quito los temporizadores? ¿Cuánto sube el throughput y qué significa eso para la prueba?",
             [(ficha("q3", [["Hilos (usuarios)", "100"], ["Periodo de subida", "10 s"], ["Duración", "60 s (bucle infinito)"],
                            ["Temporizador", "con: 500 ms + hasta 1000 ms / sin: 0 ms + 0 ms"], ["Flujo", "Tarifas → Selección → Pago"], ["Propiedades", "-Jusuarios=100 -Jrampup=10 -Jduracion=60 -Jtimer_const=0 -Jtimer_rand=0"]]),
               "Configuración del escenario de la pregunta 3.")],
             [(captura_reporte("q3-sin-timer"), "Reporte de JMeter sin temporizadores: los máximos llegan a más de 100 s.")],
             [(ENC, [met_fila("q3-con-timer", "Con temporizador"), met_fila("q3-sin-timer", "Sin temporizador", 60)], ANCHOS),
              (["Escenario (primeros 60 s)", "Rendimiento (peticiones/s)", "Media (ms)", "CPU máx. de la API (núcleos)"],
               [["Con temporizador", f"{tc[0]:.0f}", f"{tc[1]:.1f}", f"{R('q3-con-timer')['recursos']['cpu_api_pct']['max'] / 100:.2f}"],
                ["Sin temporizador", f"{ts[0]:.0f}", f"{ts[1]:.1f}", f"{R('q3-sin-timer')['recursos']['cpu_api_pct']['max'] / 100:.2f}"]], None)],
             [(fig_q3(), f"Sin temporizadores el throughput se multiplica por unas {ts[0] / tc[0]:.0f} y la API llega a usar más de un núcleo completo.")],
             [f"Sin temporizadores el throughput sube de unas {tc[0]:.0f} a unas {ts[0]:.0f} peticiones por segundo: unas {ts[0] / tc[0]:.0f} veces más con los mismos 100 usuarios. "
              f"El tiempo medio también sube (de {tc[1]:.1f} ms a {ts[1]:.0f} ms), el p99 pasa a {R('q3-sin-timer')['total']['p99_ms']} ms y el máximo llega a {R('q3-sin-timer')['total']['max_ms'] / 1000:.0f} segundos.",
              f"Lo que significa para la prueba: los temporizadores representan el tiempo que una persona real tarda en pensar entre un clic y el siguiente. Sin ellos, cada usuario virtual dispara una petición apenas termina la anterior, "
              f"y 100 usuarios generan la presión de unas {round(ts[0] / tc[0] * 100, -2):.0f} personas reales. Ya no es una prueba de carga normal, es una prueba de estrés: mide hasta dónde llega la API y no cómo la usarían los clientes.",
              "También se nota que la API empieza a saturarse: usa más de un núcleo (141 %), el tiempo de algunas peticiones se dispara y la prueba de 60 s terminó a los 124 s porque había respuestas pendientes."],
             ["Con temporizadores o sin ellos, ninguna petición falló: el límite aparece como demora, no como error.",
              "El rendimiento general del reporte (1 296 por segundo) está por debajo del real porque la prueba se alargó por las respuestas lentas del final. Por eso en la tabla uso los primeros 60 s.",
              "JMeter y la API compiten por el mismo equipo, así que parte de la demora puede venir de JMeter y no solo de la API."])

    # ------------------------------------------------------------ P4
    s4 = R("q4-escalones")["serie_10s"]
    pregunta(doc, 4, "Estrés",
             "escalono de 50 a 100, 250 y 500 usuarios? ¿En qué punto deja de crecer el throughput?",
             [(ficha("q4", [["Escalón 1 (desde 0 s)", "50 usuarios (subida 5 s)"], ["Escalón 2 (desde 30 s)", "+50 → 100 usuarios"], ["Escalón 3 (desde 60 s)", "+150 → 250 usuarios"],
                            ["Escalón 4 (desde 90 s)", "+250 → 500 usuarios"], ["Duración total", "120 s (cada escalón ~30 s)"], ["Temporizador", "50 ms + hasta 100 ms (corto, para empujar la carga)"],
                            ["Flujo", "Tarifas → Selección → Pago"], ["Propiedades", "-Jusuarios=50 -Jesc2=50 -Jesc2_retraso=30 -Jesc3=150 -Jesc3_retraso=60 -Jesc4=250 -Jesc4_retraso=90"]]),
               "Configuración del escenario de la pregunta 4: cuatro Grupos de Hilos con retraso de inicio.")],
             [(captura_reporte("q4-escalones"), "Reporte de JMeter del escenario escalonado.")],
             [(["Escalón (usuarios)", "Ventana", "Rendimiento (peticiones/s)", "Media (ms)", "p95 (ms)", "Máx. (ms)"],
               [[u, v, s4[k]["peticiones_por_s"], s4[k]["media_ms"], s4[k]["p95_ms"], s4[k]["max_ms"]] for u, v, k in ((50, "10–20 s", 1), (100, "40–50 s", 4), (250, "70–80 s", 7), (500, "100–110 s", 10))], None)],
             [(fig_q4(), "Throughput por ventana de 10 s (barras) y p95 (línea roja). El throughput se aplana entre 250 y 500 usuarios.")],
             [f"Deja de crecer entre 250 y 500 usuarios, cerca de las 2 300 peticiones por segundo. Con 50 usuarios el throughput fue de unas {s4[1]['peticiones_por_s']:.0f} por segundo, con 100 de unas {s4[4]['peticiones_por_s']:.0f}, con 250 de unas {s4[7]['peticiones_por_s']:.0f} "
              f"y con 500 de unas {sum(x['peticiones_por_s'] for x in s4[9:12]) / 3:.0f}. Pasar de 50 a 100 y de 100 a 250 usuarios casi duplicó el throughput cada vez. Pasar de 250 a 500 lo subió solo un {100 * (sum(x['peticiones_por_s'] for x in s4[9:12]) / 3 / s4[7]['peticiones_por_s'] - 1):.0f} %, aunque se duplicaron los usuarios.",
              f"Cuando el throughput se estanca, el tiempo de respuesta se rompe: el p95 pasa de 2 ms a más de 1 000 ms con 500 usuarios y el máximo llega a {R('q4-escalones')['total']['max_ms'] / 1000:.0f} segundos. "
              "Es la señal clásica de saturación: llegan más peticiones de las que la API puede atender, entonces se acumulan en fila. Con 250 usuarios ya se ve el comienzo (el promedio sube de 1 a 16 ms)."],
             ["Tampoco hubo errores: la saturación se ve como demora, no como fallas.",
              "El límite de unas 2 300 peticiones por segundo es del conjunto API y JMeter en mi equipo; la API es un solo proceso de Python, lo que probablemente limita este número. No probé otra máquina.",
              "Usé temporizadores cortos (50 a 150 ms). Con las pausas por defecto 500 usuarios solo generan unas 500 peticiones por segundo y la API no llegaría a saturarse."])

    # ------------------------------------------------------------ P5
    a, b = R("q5-1min"), R("q5-10min")
    s10 = b["serie_10s"]
    pregunta(doc, 5, "Estrés",
             "la prueba dura 10 minutos en lugar de 1? ¿El tiempo de respuesta se mantiene o sube con el tiempo?",
             [(ficha("q5", [["Hilos (usuarios)", "100"], ["Periodo de subida", "10 s"], ["Duración", "60 s y 600 s (dos ejecuciones)"], ["Temporizador", "Aleatorio Uniforme: 500 ms + hasta 1000 ms"],
                            ["Flujo", "Tarifas → Selección → Pago"], ["Propiedades", "-Jusuarios=100 -Jrampup=10 -Jduracion=60|600 -Jiteraciones=-1"]]),
               "Configuración del escenario de la pregunta 5.")],
             [(captura_reporte("q5-10min"), "Reporte de JMeter de la prueba de 10 minutos.")],
             [(ENC, [met_fila("q5-1min", "1 minuto"), met_fila("q5-10min", "10 minutos")], ANCHOS),
              (["Minuto", "1", "2", "3", "5", "7", "10"],
               [["Media (ms)"] + [round(sum(x["media_ms"] * x["muestras"] for x in s10 if m * 60 <= x["desde_s"] < (m + 1) * 60) / sum(x["muestras"] for x in s10 if m * 60 <= x["desde_s"] < (m + 1) * 60), 2) for m in (0, 1, 2, 4, 6, 9)],
                ["p95 (ms)"] + [max(x["p95_ms"] for x in s10 if m * 60 <= x["desde_s"] < (m + 1) * 60) for m in (0, 1, 2, 4, 6, 9)]], None)],
             [(fig_q5(), "Tiempo medio a lo largo de la prueba (izquierda) y memoria de la API (derecha).")],
             [f"Se mantiene. La media fue de {a['total']['media_ms']} ms en la prueba de 1 minuto y de {b['total']['media_ms']} ms en la de 10 minutos; el p95 fue de 2 ms en las dos. "
              "Minuto a minuto el tiempo se queda plano, sin tendencia a subir. Tampoco crece la memoria de la API: pasó de 22,3 a 22,7 MB en 10 minutos.",
              "Tiene sentido porque la carga es moderada (unas 100 peticiones por segundo) y cada reserva se borra al pagarse. No hay nada que se acumule. "
              "El único valor más alto está en los primeros segundos (máximo de 29 ms), cuando están arrancando los hilos."],
             ["Con esta carga 10 minutos no alcanzan para ver un problema. Para buscar fugas de memoria o degradación lenta haría falta una prueba más larga o con más carga.",
              "El caso contrario sí aparece en la pregunta 6: las reservas que no se pagan se acumulan en memoria."])

    # ------------------------------------------------------------ P6
    a, b = R("q6-tarifas"), R("q6-seleccion")
    ma, mb = a["por_peticion"]["Tarifas"], b["por_peticion"]["SeleccionTarifaYCantidad"]
    pregunta(doc, 6, "Estrés",
             "mido /api/tarifas (solo lectura) y /api/seleccion (crea reservas) con la misma carga? ¿Cuál cuesta más?",
             [(ficha("q6", [["Hilos (usuarios)", "200"], ["Periodo de subida", "10 s"], ["Duración", "60 s (bucle infinito)"], ["Temporizador", "100 ms + hasta 200 ms"],
                            ["Petición medida", "solo GET /api/tarifas, o solo POST /api/seleccion"], ["Propiedades", "-Jflujo=tarifas|seleccion -Jusuarios=200 -Jtimer_const=100 -Jtimer_rand=200"]]),
               "Configuración del escenario de la pregunta 6.")],
             [(captura_reporte("q6-seleccion"), "Reporte de JMeter de /api/seleccion.")],
             [(["Petición", "Muestras", "Media (ms)", "p95 (ms)", "p99 (ms)", "Máx (ms)", "Rendimiento (peticiones/s)", "Memoria de la API al final (MB)"],
               [["GET /api/tarifas", ma["muestras"], ma["media_ms"], ma["p95_ms"], ma["p99_ms"], ma["max_ms"], ma["throughput"], a["recursos"]["mem_api_mb"]["fin"]],
                ["POST /api/seleccion", mb["muestras"], mb["media_ms"], mb["p95_ms"], mb["p99_ms"], mb["max_ms"], mb["throughput"], b["recursos"]["mem_api_mb"]["fin"]]], None)],
             [(fig_q6(), "Costo (tiempo de respuesta) y rendimiento de las dos peticiones.")],
             [f"Cuesta más /api/seleccion, pero por muy poco. Su tiempo medio fue de {mb['media_ms']} ms contra {ma['media_ms']} ms de /api/tarifas, o sea unos {mb['media_ms'] - ma['media_ms']:.1f} ms más (cerca de un {100 * (mb['media_ms'] / ma['media_ms'] - 1):.0f} % más). "
              f"El p95 es igual (2 ms en las dos) y el rendimiento también (unas {ma['throughput']:.0f} peticiones por segundo), porque lo fijan los temporizadores y no la API.",
              f"Es lo esperado: /api/tarifas solo devuelve una lista fija, y /api/seleccion además valida los datos, genera un identificador y guarda la reserva en memoria. "
              f"Ese guardado tiene otro costo que no se ve en el tiempo: como en este escenario nadie paga, la memoria de la API pasó de {b['recursos']['mem_api_mb']['inicio']} a {b['recursos']['mem_api_mb']['fin']} MB con {mb['muestras']:,} reservas, y con /api/tarifas se quedó en {a['recursos']['mem_api_mb']['fin']} MB.".replace(",", " ")],
             ["Con el costo medido como tiempo de respuesta, la diferencia de 0,3 ms es pequeña y está cerca de lo que mi equipo puede distinguir. Con una carga más alta se vería mejor.",
              "El costo en memoria no es el que pide la guía (tiempo de respuesta), pero lo anoto porque es una diferencia real entre las dos peticiones."])

    # ------------------------------------------------------------ P7
    g = R("q7-500-reservas")
    f7 = jtl("q7-500-reservas")
    ok7 = [x["ms"] for x in f7 if x["ok"]]
    pregunta(doc, 7, "Concurrencia",
             "500 usuarios crean reservas al mismo tiempo? ¿Todas las respuestas son exitosas?",
             [(ficha("q7", [["Hilos (usuarios)", "500"], ["Periodo de subida", "1 s"], ["Bucle", "10 repeticiones por usuario (5 000 reservas)"], ["Temporizador", "ninguno (0 ms)"],
                            ["Petición", "solo POST /api/seleccion"], ["Aserciones", "código 201 y total = precio × cantidad"], ["Propiedades", "-Jflujo=seleccion -Jusuarios=500 -Jrampup=1 -Jiteraciones=10 -Jtimer_const=0 -Jtimer_rand=0"]]),
               "Configuración del escenario de la pregunta 7.")],
             [(captura_reporte("q7-500-reservas"), "Reporte de JMeter: aparecen errores y tiempos muy altos.")],
             [(ENC, [met_fila("q7-500-reservas", "500 reservas a la vez")], ANCHOS),
              (["Dato", "Valor"], [["Respuestas exitosas", f"{len(ok7)} de 5 000"], ["Respuestas fallidas", f"{len(f7) - len(ok7)} (todas: Non HTTP response code: java.net.SocketException / Connection reset)"],
                                   ["Mediana de las exitosas", f"{pct(ok7, 50)} ms"], ["p95 de las exitosas", f"{pct(ok7, 95)} ms"], ["Máximo", f"{max(x['ms'] for x in f7)} ms"]], [4, 12])],
             [(fig_q7(), "Distribución del tiempo de respuesta (izquierda) y errores en el tiempo (derecha).")],
             [f"No, no todas fueron exitosas. De 5 000 peticiones, {len(f7) - len(ok7)} ({g['total']['error_pct']} %) fallaron con “Connection reset”: el servidor cortó la conexión. Entre las que sí respondieron, la mayoría fue rápida (mediana de {pct(ok7, 50)} ms), "
              f"pero el p95 fue de {pct(ok7, 95) / 1000:.1f} segundos y hubo respuestas de más de 100 segundos.",
              "Lo importante es qué falló y qué no. Las reservas que se crearon fueron correctas: todas pasaron la validación de total (precio × cantidad) y devolvieron 201. Lo que no aguantó fue la llegada simultánea de conexiones: "
              "la API no alcanza a aceptarlas todas a la vez, unas esperan varios segundos y otras se rechazan. Mi hipótesis es que se llena la fila de conexiones pendientes del servidor, pero no lo comprobé con herramientas de red."],
             ["Que el tiempo total sea de casi 2 minutos con 5 000 peticiones sin pausas confirma que el problema es la llegada en bloque, no la cantidad.",
              "Un servidor real tendría una fila de conexiones más grande y quizá un balanceador. Esta API es un solo proceso de Python con la configuración básica."])

    # ------------------------------------------------------------ P8
    a, b = R("q8-sincronizado"), R("q8-distribuido")
    fa, fb = jtl("q8-sincronizado"), jtl("q8-distribuido")
    oka, okb = [x["ms"] for x in fa if x["ok"]], [x["ms"] for x in fb if x["ok"]]
    pregunta(doc, 8, "Concurrencia",
             "los usuarios disparan a la vez con el Temporizador sincronizado, frente a cuando llegan distribuidos?",
             [(ficha("q8", [["Hilos (usuarios)", "500, una sola petición cada uno (POST /api/seleccion)"], ["Sincronizado", "Temporizador sincronizado, grupo de 500; subida 5 s"],
                            ["Distribuido", "sin temporizador sincronizado; subida 10 s"], ["Temporizador aleatorio", "ninguno (0 ms)"],
                            ["Propiedades", "-Jsync=true -Jsync_grupo=500 -Jrampup=5  /  -Jrampup=10"]]),
               "Configuración del escenario de la pregunta 8.")],
             [(captura_reporte("q8-sincronizado"), "Reporte de JMeter, escenario sincronizado."), (captura_reporte("q8-distribuido"), "Reporte de JMeter, escenario distribuido.")],
             [(["Escenario", "Muestras", "Mediana ok (ms)", "p95 ok (ms)", "Máx. ok (ms)", "Fallidas", "% Error"],
               [["Sincronizado", 500, pct(oka, 50), pct(oka, 95), max(oka), len(fa) - len(oka), f"{a['total']['error_pct']} %"],
                ["Distribuido", 500, pct(okb, 50), pct(okb, 95), max(okb), len(fb) - len(okb), f"{b['total']['error_pct']} %"]], None)],
             [(fig_q8(), "Izquierda: peticiones enviadas por segundo. Derecha: tiempos de las peticiones exitosas (escala logarítmica).")],
             [f"Cambia mucho. Con el Temporizador sincronizado las 500 peticiones salen en el mismo segundo y la API no lo soporta bien: {len(fa) - len(oka)} fallaron ({a['total']['error_pct']} %) con “Connection reset”, "
              f"la mediana de las que sí respondieron fue de {pct(oka, 50) / 1000:.1f} s y el p95 de {pct(oka, 95) / 1000:.0f} s. "
              f"Cuando los mismos 500 usuarios llegan repartidos en 10 s (unos 50 por segundo), ninguna falló, la mediana fue de {pct(okb, 50)} ms y el p95 de {pct(okb, 95)} ms.",
              "La diferencia es lo que el temporizador sincronizado sirve para probar: un pico real de llegada simultánea, como cuando se abre la venta de boletas. "
              "La llegada distribuida es más suave y por eso esconde el problema. Si solo hubiera probado de forma distribuida, habría concluido que la API aguanta 500 usuarios sin errores."],
             ["La simulación de “al mismo tiempo” es aproximada: JMeter libera los hilos a la vez, pero llegan a la API con diferencias de milisegundos.",
              "Este escenario y el de la pregunta 7 se parecen. La diferencia es que aquí cada usuario hace una sola petición y en la 7 hace 10 seguidas."])

    # ------------------------------------------------------------ P9
    a, n = R("q9-totales"), R("q9-control-negativo")
    sel9 = a["por_peticion"]["SeleccionTarifaYCantidad"]["muestras"]
    pregunta(doc, 9, "Concurrencia",
             "el total cobrado no coincide con precio × cantidad bajo carga? ¿Cómo lo validarías con el CSV?",
             [(ficha("q9", [["Hilos (usuarios)", "200 (control negativo: 20)"], ["Periodo de subida", "10 s"], ["Duración", "60 s (bucle infinito)"], ["Temporizador", "100 ms + hasta 200 ms"],
                            ["CSV", "datos.csv con 3 columnas: tarifa, cantidad, total_esperado (precio × cantidad)"],
                            ["Validación", "JSON Assertion: $.total = ${total_esperado}, en Selección y en Pago"], ["Control negativo", "datos_totales_incorrectos.csv con 2 de 4 filas mal a propósito"]]),
               "Configuración del escenario de la pregunta 9.")],
             [(captura_reporte("q9-totales"), "Reporte de JMeter bajo carga: 0 % de error.")],
             [(ENC, [met_fila("q9-totales", "Bajo carga (CSV correcto)"), met_fila("q9-control-negativo", "Control negativo")], ANCHOS),
              (["Dato", "Valor"], [["Validaciones del total bajo carga", f"{sel9} en Selección + {a['por_peticion']['Pago']['muestras']} en Pago, todas correctas"],
                                   ["Control negativo", "40 de 120 peticiones fallan: justo las de las 2 filas con total equivocado (10 + 10 en Selección, 20 en Pago)"]], [5, 11])],
             [(fig_q9(), "La validación del total detecta los datos equivocados del control negativo y no falla bajo carga.")],
             [f"Bajo carga no se encontró ninguna diferencia. En {sel9} reservas y {a['por_peticion']['Pago']['muestras']} pagos con 200 usuarios simultáneos, el total fue siempre precio × cantidad. Ningún total quedó mezclado entre usuarios.",
              "Cómo lo validé con el CSV: agregué al CSV una tercera columna, total_esperado, con el precio de la tarifa por la cantidad (por ejemplo, vip × 4 = 1 400 000). En JMeter puse una JSON Assertion con la ruta $.total y el valor ${total_esperado}. "
              "Así cada usuario compara lo que le devolvió la API contra lo que correspondía a su propia fila, y la comprobación vale aunque muchos usuarios compren a la vez.",
              "Para estar seguro de que la validación sirve, hice un control negativo: un CSV con dos filas con el total mal a propósito. Fallaron exactamente 40 de las 120 peticiones: las de esas dos filas, tanto en Selección como en Pago. "
              "Si la aserción no funcionara, el escenario de carga habría dado 0 % de error igual."],
             ["La API de la profesora calcula el total con una multiplicación simple y sin estado compartido, así que no es sorprendente que no falle. Un error de concurrencia real aparecería con una API que reutilice datos entre peticiones.",
              "La validación solo mira los totales que responde la API; no comprueba que el valor guardado en la reserva sea el mismo (eso requeriría otro endpoint de consulta)."])

    # ------------------------------------------------------------ P10
    a, b = R("q10-500"), R("q10-500-presion")
    ra, rb = a["recursos"], b["recursos"]
    sb = b["serie_10s"]
    pregunta(doc, 10, "Recursos",
             "subo a 500 usuarios? ¿Cómo se comportan la memoria y la CPU durante la prueba? ¿Llegan a saturarse? ¿Cuánto cambia el tiempo de respuesta cuando eso pasa?",
             [(ficha("q10", [["Hilos (usuarios)", "500"], ["Periodo de subida", "30 s"], ["Duración", "180 s (bucle infinito)"], ["Temporizador", "normal: 500 ms + hasta 1000 ms / con presión: 50 ms + hasta 100 ms"],
                             ["Flujo", "Tarifas → Selección → Pago"], ["Monitoreo", "CPU y memoria cada 1 s (equipo, JMeter y API)"],
                             ["Propiedades", "-Jusuarios=500 -Jrampup=30 -Jduracion=180  (presión: -Jtimer_const=50 -Jtimer_rand=100)"]]),
               "Configuración del escenario de la pregunta 10.")],
             [(captura_reporte("q10-500-presion"), "Reporte de JMeter con 500 usuarios y pausas cortas.")],
             [(ENC, [met_fila("q10-500", "500 usuarios, pausas normales"), met_fila("q10-500-presion", "500 usuarios, pausas cortas")], ANCHOS),
              (["Recurso (máximo)", "Pausas normales", "Pausas cortas"],
               [["CPU del equipo (% de 16 núcleos)", ra["cpu_equipo_pct"]["max"], rb["cpu_equipo_pct"]["max"]], ["CPU de JMeter (núcleos)", round(ra["cpu_jmeter_pct"]["max"] / 100, 1), round(rb["cpu_jmeter_pct"]["max"] / 100, 1)],
                ["CPU de la API (núcleos)", round(ra["cpu_api_pct"]["max"] / 100, 2), round(rb["cpu_api_pct"]["max"] / 100, 2)], ["Memoria del equipo (%)", ra["mem_equipo_pct"]["max"], rb["mem_equipo_pct"]["max"]],
                ["Memoria de JMeter (MB)", ra["mem_jmeter_mb"]["max"], rb["mem_jmeter_mb"]["max"]], ["Memoria de la API (MB)", ra["mem_api_mb"]["max"], rb["mem_api_mb"]["max"]]], [7, 4, 4])],
             [(fig_q10(), "Arriba: CPU. Abajo: tiempo de respuesta. A la izquierda, pausas normales; a la derecha, pausas cortas."), (fig_q10_mem(), "Memoria que usa JMeter durante la prueba.")],
             [f"Con las pausas normales no se saturó nada. El equipo usó como máximo un {ra['cpu_equipo_pct']['max']:.0f} % de CPU, JMeter hasta {ra['cpu_jmeter_pct']['max'] / 100:.1f} núcleos y la API apenas {ra['cpu_api_pct']['max'] / 100:.1f}. La memoria de la API se quedó en {ra['mem_api_mb']['max']} MB y la de JMeter en cerca de 1 GB. "
              f"El tiempo de respuesta se mantuvo en {a['total']['media_ms']} ms de media.",
              f"Con pausas cortas, que sí empujan la carga a unas {sb[-1]['peticiones_por_s']:.0f} peticiones por segundo, la API llega a su límite: pasa de {ra['cpu_api_pct']['max'] / 100:.1f} a {rb['cpu_api_pct']['max'] / 100:.1f} núcleos, es decir, un poco más de un núcleo completo. "
              f"Ahí el tiempo de respuesta cambia mucho: la media sube de {a['total']['media_ms']} a {b['total']['media_ms']:.0f} ms (unas {b['total']['media_ms'] / a['total']['media_ms']:.0f} veces), el p95 pasa de {a['total']['p95_ms']} a {b['total']['p95_ms']} ms y el máximo llega a {b['total']['max_ms'] / 1000:.0f} segundos.",
              f"Lo más interesante es que el CPU total del equipo nunca se vio saturado (máximo {rb['cpu_equipo_pct']['max']:.0f} %). El cuello de botella fue el proceso de la API, que usa algo más de un núcleo, y no el equipo completo. "
              "Por eso no basta con mirar el CPU del equipo: hay que mirar el proceso que se está probando. La memoria no fue un problema en ninguno de los dos casos."],
             ["No usé PerfMon con ServerAgent; el muestreador propio mide CPU y memoria del equipo, de JMeter y de la API cada segundo, pero no mide red ni disco.",
              "Como JMeter y la API comparten el equipo, el CPU del equipo mezcla a los dos. Por eso los separé por proceso.",
              "El escenario de “pausas cortas” lo agregué yo para poder observar la saturación: con las pausas normales la API no llegaba a su límite con 500 usuarios."])

    # ------------------------------------------------------------ conclusiones
    doc.add_heading("Conclusiones", level=1)
    for x in ("Con carga normal (pausas de 0,5 a 1,5 s) la API aguanta 500 usuarios sin problemas: el tiempo de respuesta no cambia y no hay errores (preguntas 1, 5 y 10).",
              "La API se satura cerca de las 2 300 peticiones por segundo. Antes de ese punto el throughput crece con los usuarios; después se estanca y los tiempos se disparan (preguntas 3, 4 y 10).",
              "El límite que se encontró es el de un solo proceso de la API, no del equipo completo. El CPU del equipo se quedó por debajo del 55 % (pregunta 10).",
              "Lo que más daña a la API es la llegada simultánea de muchas conexiones: 500 usuarios al mismo tiempo produjeron errores de “Connection reset” (16,6 % en la pregunta 8 y 0,66 % en la 7), mientras que repartidos nunca fallaron (preguntas 7 y 8).",
              "La lógica de negocio es correcta bajo carga: el total siempre fue precio × cantidad (pregunta 9).",
              "Las pausas definen qué estoy midiendo: con temporizadores simulo personas, sin ellos mido el límite de la API (pregunta 3)."):
        doc.add_paragraph(x, style="List Bullet")
    doc.add_heading("Cómo reproducir", level=2)
    parrafo(doc, "python3 scripts/correr_experimentos.py (todos los escenarios) o con el nombre de uno, por ejemplo q4-escalones. Los reportes HTML quedan en pruebas/experimentacion/resultados/<escenario>/reporte/index.html.")
    ruta = os.path.join(EXP, "Informe_Experimentacion.docx")
    doc.save(ruta)
    print("guardado", os.path.relpath(ruta, RAIZ))


if __name__ == "__main__":
    construir()
