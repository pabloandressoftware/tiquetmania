# Tiquetmania · pruebas de rendimiento con JMeter y GitHub Actions

Taller de Automatización de Pruebas 2026-2. Es un monorepo: la API, el plan de JMeter y el pipeline viven juntos.
Cada cambio se prueba con exactamente el commit que se sube.

```
tiquetmania/
├── api/
│   └── ticketmania_simple.py              API de compra de boletas (la de la profesora, sin cambios)
├── pruebas/
│   ├── jmeter/                            EJERCICIO 1: despliegue (lo ejecuta el pipeline)
│   │   ├── Ticketmania.jmx
│   │   └── datos.csv                      misma carpeta que el .jmx (ruta relativa)
│   └── experimentacion/                   EJERCICIO 2: "¿Qué pasaría si...?" (solo local, el pipeline no lo corre)
│       ├── Experimentacion.jmx
│       ├── datos.csv
│       ├── resultados/                    reportes de cada escenario (1.ª corrida)
│       ├── resultados_repeticion/         2.ª corrida: resumen, CPU y memoria (sin los reportes HTML)
│       ├── repeticion_comparacion.json    comparación de las dos corridas
│       └── entrega/                       Informe en Word y PDF, presentación en PowerPoint y PDF (entrega del ejercicio 2)
├── scripts/                               generar_planes.py, correr_experimentos.py, comparar_repeticiones.py, generar_informe.py
├── .github/workflows/pipeline.yml         el pipeline (GitHub solo lo lee en la raíz)
└── README.md
```

## 1. Cómo correr todo en tu computador

Requisitos: Python 3.8+, Java 17+ y JMeter 5.6.3.

```bash
python3 api/ticketmania_simple.py                 # terminal 1: la API queda en http://127.0.0.1:8080

cd pruebas/jmeter                                 # terminal 2: siempre desde esta carpeta
jmeter -n -t Ticketmania.jmx -l resultados.jtl -e -o reporte
# abre reporte/index.html
```

Para ver o editar el plan: `jmeter -t pruebas/jmeter/Ticketmania.jmx`.

## 2. El plan `Ticketmania.jmx`

| Elemento | Configuración |
|---|---|
| Gestor de Cookies HTTP | a nivel del plan (la API no usa cookies, pero la guía lo incluye en el árbol) |
| Configuración del CSV Data Set | `datos.csv` (ruta relativa) · variables `tarifa,cantidad` · primera línea como nombres · reciclar en EOF |
| Valores por defecto de la petición HTTP | `127.0.0.1` · puerto `8080` |
| Grupo de Hilos `Seleccion de tarifa y Pago` | **200 hilos · subida 300 s · bucle 1** (200 usuarios entran en 5 minutos) |
| Temporizador Aleatorio Uniforme | desplazamiento 500 ms + aleatorio hasta 1000 ms (pausas de 500 a 1500 ms) |
| `Tarifas` | GET `/api/tarifas` |
| `SeleccionTarifaYCantidad` | POST `/api/seleccion` con `{"tarifa":"${tarifa}","cantidad":${cantidad}}` · Gestor de Cabecera (Accept y Content-Type JSON) · **JSON Extractor** `reserva` → `num_reserva` (por defecto `num_reserva_not_found`) |
| `Debug Sampler` | deshabilitado: solo se usa para verificar el extractor, no para medir |
| `Pago` | POST `/api/pago` con `{"reserva":"${num_reserva}"}` · Gestor de Cabecera · **JSON Assertion**: `$.estado` = `APROBADO` |
| Reporte resumen | listener para la interfaz gráfica |

No se incluyen los listeners de plugins (Transactions per Second, PerfMon) porque el pipeline no tiene los plugins instalados y el plan no cargaría. Ver "Local vs nube" más abajo.

## 3. El pipeline (`.github/workflows/pipeline.yml`)

Corre con cada `push` a `main` y a mano desde Actions (`workflow_dispatch`).

| Paso | Qué hace |
|---|---|
| Descargar el repositorio | `actions/checkout` |
| Java 17 | `actions/setup-java` (JMeter 5.6.3 lo necesita; la máquina viene vacía) |
| JMeter 5.6.3 | descarga el `.tgz` de Apache, **verifica el checksum SHA-512**, lo descomprime y agrega `bin` al `PATH` con `$GITHUB_PATH` |
| Levantar la API | `python3 api/ticketmania_simple.py` en segundo plano y un bucle que espera a que `/api/salud` responda (máximo 30 s, si no, falla) |
| Ejecutar JMeter | modo no-GUI **desde `pruebas/jmeter/`** (ahí está `datos.csv`): `jmeter -n -t Ticketmania.jmx -l resultados.jtl -e -o reporte` |
| Decidir | JMeter termina "bien" aunque una petición responda mal. Este paso lee el `.jtl` y, si hay peticiones fallidas (o ninguna), termina en rojo |
| Subir el reporte | artefacto `reporte-rendimiento` con `if: always()`: se sube aunque la prueba haya fallado |

Si cualquier paso falla, los siguientes se omiten y el job queda en rojo. La excepción es subir el reporte, que corre siempre.

### Lista de verificación de la guía

- [x] Monorepo con `api/`, `pruebas/` y `.github/workflows/`
- [x] Plan con ruta `datos.csv` y 200 hilos, junto con el CSV en `pruebas/jmeter/`
- [x] Java 17 y JMeter 5.6.3 instalados en la máquina virtual
- [x] API levantada en 8080 y espera a `/api/salud`
- [x] Ejecución no-GUI con reporte HTML
- [x] Reporte subido con condición "siempre"
- [x] El job se detiene y queda en rojo si un paso falla

### Resultado de la ejecución

Corrida en GitHub Actions: **verde** (https://github.com/pabloandressoftware/tiquetmania/actions/runs/43103869356).

- Los 7 pasos terminaron en `success`, en unos 6 minutos.
- JMeter: **600 peticiones** (200 usuarios × 3), **0 fallidas**, media de 1 ms y máximo de 38 ms.
- El reporte quedó como artefacto `reporte-rendimiento` (~1 MB).
- La primera corrida (disparada por el push) se quedó atascada en cola por un problema de GitHub y no se pudo cancelar. La de arriba se lanzó a mano con `workflow_dispatch`.

### Local vs nube

| Aspecto | Mi computador | Pipeline |
|---|---|---|
| Máquina | la mía, con la API y JMeter juntos | máquina nueva de GitHub, compartida |
| PerfMon (CPU y memoria) | disponible con ServerAgent | no disponible |
| Comparar ejecuciones | válido si cambio una sola variable | varía entre ejecuciones |

La nube sirve para comprobar que la prueba corre de principio a fin, no para medir la capacidad de la API.
### Criterio de aceptación

La guía v3 dice que los criterios no son obligatorios, pero que si se proponen deben tener métrica, valor de referencia y carga. El del pipeline es:

| Métrica | Valor esperado | Carga |
|---|---|---|
| % Error | 0 % (ninguna petición fallida) | 200 usuarios, subida de 300 s, 1 vuelta (600 peticiones) |

El paso "Decidir" del pipeline lo aplica: si hay una sola petición fallida, el job queda en rojo.

## 4. Ejercicio 2: experimentación "¿Qué pasaría si...?"

`pruebas/experimentacion/Experimentacion.jmx` es un solo plan que se configura con propiedades (`-Jusuarios=500 -Jrampup=10 ...`).
`scripts/correr_experimentos.py` corre los 18 escenarios de las 10 preguntas, mide CPU y memoria cada segundo y guarda un reporte HTML por escenario en `pruebas/experimentacion/resultados/`.
Las respuestas, gráficas y capturas están en `pruebas/experimentacion/entrega/`: `Informe_Experimentacion.docx` (y `.pdf`) y `Presentacion_Experimentacion.pptx` (y `.pdf`).

```bash
export JMETER_HOME=/ruta/a/apache-jmeter-5.6.3
python3 scripts/correr_experimentos.py --lista            # ver escenarios
python3 scripts/correr_experimentos.py q1-20 q1-500       # correr algunos
```

### Repetición de los escenarios

Cada escenario se corrió dos veces (17 de 18; la prueba de 10 minutos de la pregunta 5 solo una).
La segunda corrida se guarda con `CARPETA_RESULTADOS=resultados_repeticion python3 scripts/correr_experimentos.py ...` y se compara con `python3 scripts/comparar_repeticiones.py`.

- **16 de 17** repiten la misma conclusión. Con carga normal los números casi no cambian y el error es 0 %.
- **Pregunta 7:** los 33 errores de la primera corrida no aparecieron en la segunda (0 de 5 000). La respuesta del informe dice "a veces".
- **Pregunta 8:** el escenario sincronizado tuvo 16,6 % de errores la primera vez y 41 % la segunda; el distribuido, 0 % las dos veces.
- La segunda corrida se hizo con contenedores de Docker de otro proyecto en reposo; el CPU medio del equipo fue parecido al de la primera.

El pipeline **no** ejecuta este plan.
