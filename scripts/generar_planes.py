#!/usr/bin/env python3
"""Genera los dos planes de JMeter del taller.

  pruebas/jmeter/Ticketmania.jmx                  plan del despliegue (200 usuarios en 5 min)
  pruebas/experimentacion/Experimentacion.jmx     plan parametrizable para las 10 preguntas

Los .jmx son XML y se pueden abrir y editar en la interfaz de JMeter. Este script solo
evita escribir a mano el mismo XML varias veces. Uso:  python3 scripts/generar_planes.py
"""
import os
from xml.sax.saxutils import escape

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def s(nombre, valor):
    return f'<stringProp name="{nombre}">{escape(str(valor))}</stringProp>'


def b(nombre, valor):
    return f'<boolProp name="{nombre}">{"true" if valor else "false"}</boolProp>'


def arbol(elemento, hijos=""):
    """Un elemento de JMeter va seguido de su <hashTree> con los elementos que contiene."""
    return f"{elemento}\n<hashTree>\n{hijos}</hashTree>\n"


def hoja(elemento):
    return f"{elemento}\n<hashTree/>\n"


# ---------------------------------------------------------------- elementos
def csv(archivo, variables):
    return hoja(
        f'<CSVDataSet guiclass="TestBeanGUI" testclass="CSVDataSet" testname="Configuración del CSV Data Set" enabled="true">'
        f'{s("filename", archivo)}{s("fileEncoding", "UTF-8")}{s("variableNames", variables)}'
        f'{b("ignoreFirstLine", True)}{s("delimiter", ",")}{b("quotedData", False)}'
        f'{b("recycle", True)}{b("stopThread", False)}{s("shareMode", "shareMode.all")}</CSVDataSet>'
    )


def valores_por_defecto(host, puerto):
    return hoja(
        '<ConfigTestElement guiclass="HttpDefaultsGui" testclass="ConfigTestElement" '
        'testname="Valores por Defecto para Petición HTTP" enabled="true">'
        '<elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" '
        'testclass="Arguments" testname="Variables definidas por el usuario" enabled="true">'
        '<collectionProp name="Arguments.arguments"/></elementProp>'
        f'{s("HTTPSampler.domain", host)}{s("HTTPSampler.port", puerto)}{s("HTTPSampler.protocol", "http")}'
        '</ConfigTestElement>'
    )


def cabeceras():
    fila = lambda n, v: (f'<elementProp name="" elementType="Header">{s("Header.name", n)}{s("Header.value", v)}</elementProp>')
    return hoja(
        '<HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="Gestor de Cabecera HTTP" enabled="true">'
        f'<collectionProp name="HeaderManager.headers">{fila("Accept", "application/json")}'
        f'{fila("Content-Type", "application/json")}</collectionProp></HeaderManager>'
    )


def peticion(nombre, metodo, ruta, cuerpo=None, hijos="", habilitado=True):
    if cuerpo is None:
        args = '<elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="Variables definidas por el usuario" enabled="true"><collectionProp name="Arguments.arguments"/></elementProp>'
        raw = ""
    else:
        args = ('<elementProp name="HTTPsampler.Arguments" elementType="Arguments"><collectionProp name="Arguments.arguments">'
                '<elementProp name="" elementType="HTTPArgument">' + b("HTTPArgument.always_encode", False) +
                s("Argument.value", cuerpo) + s("Argument.metadata", "=") + '</elementProp></collectionProp></elementProp>')
        raw = b("HTTPSampler.postBodyRaw", True)
    el = (f'<HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="{escape(nombre)}" '
          f'enabled="{"true" if habilitado else "false"}">{raw}{args}{s("HTTPSampler.path", ruta)}{s("HTTPSampler.method", metodo)}'
          f'{b("HTTPSampler.follow_redirects", True)}{b("HTTPSampler.use_keepalive", True)}</HTTPSamplerProxy>')
    return arbol(el, hijos)


def extractor_json(variable, ruta, defecto):
    return hoja(
        '<JSONPostProcessor guiclass="JSONPostProcessorGui" testclass="JSONPostProcessor" testname="Json Extractor" enabled="true">'
        f'{s("JSONPostProcessor.referenceNames", variable)}{s("JSONPostProcessor.jsonPathExprs", ruta)}'
        f'{s("JSONPostProcessor.match_numbers", "1")}{s("JSONPostProcessor.defaultValues", defecto)}</JSONPostProcessor>'
    )


def asercion_json(nombre, ruta, esperado):
    """Comprueba que la ruta exista y que su valor sea el esperado ('Additionally assert value')."""
    return hoja(
        f'<JSONPathAssertion guiclass="JSONPathAssertionGui" testclass="JSONPathAssertion" testname="{escape(nombre)}" enabled="true">'
        f'{s("JSON_PATH", ruta)}{s("EXPECTED_VALUE", esperado)}{b("JSONVALIDATION", True)}{b("EXPECT_NULL", False)}'
        f'{b("INVERT", False)}{b("ISREGEX", False)}</JSONPathAssertion>'
    )


def asercion_codigo(nombre, codigo):
    return hoja(
        f'<ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="{escape(nombre)}" enabled="true">'
        f'<collectionProp name="Asserion.test_strings">{s("1", codigo)}</collectionProp>{s("Assertion.custom_message", "")}'
        f'{s("Assertion.test_field", "Assertion.response_code")}{b("Assertion.assume_success", False)}'
        '<intProp name="Assertion.test_type">8</intProp></ResponseAssertion>'
    )


def temporizador_uniforme(constante, aleatorio):
    return hoja(
        '<UniformRandomTimer guiclass="UniformRandomTimerGui" testclass="UniformRandomTimer" '
        'testname="Temporizador Aleatorio Uniforme" enabled="true">'
        f'{s("ConstantTimer.delay", constante)}{s("RandomTimer.range", aleatorio)}</UniformRandomTimer>'
    )


def temporizador_sincronizado(grupo):
    return hoja(
        '<SyncTimer guiclass="TestBeanGUI" testclass="SyncTimer" testname="Temporizador sincronizado" enabled="true">'
        f'{s("groupSize", grupo)}<longProp name="timeoutInMs">0</longProp></SyncTimer>'
    )


def controlador_if(nombre, condicion, hijos):
    return arbol(
        f'<IfController guiclass="IfControllerPanel" testclass="IfController" testname="{escape(nombre)}" enabled="true">'
        f'{s("IfController.condition", condicion)}{b("IfController.evaluateAll", False)}{b("IfController.useExpression", True)}</IfController>',
        hijos)


def reporte_resumen():
    guardar = ("<time>true</time><latency>true</latency><timestamp>true</timestamp><success>true</success><label>true</label>"
               "<code>true</code><message>true</message><threadName>true</threadName><dataType>true</dataType><encoding>false</encoding>"
               "<assertions>true</assertions><subresults>true</subresults><responseData>false</responseData><samplerData>false</samplerData>"
               "<xml>false</xml><fieldNames>true</fieldNames><responseHeaders>false</responseHeaders><requestHeaders>false</requestHeaders>"
               "<responseDataOnError>false</responseDataOnError><saveAssertionResultsFailureMessage>true</saveAssertionResultsFailureMessage>"
               "<assertionsResultsToSave>0</assertionsResultsToSave><bytes>true</bytes><sentBytes>true</sentBytes><url>true</url>"
               "<threadCounts>true</threadCounts><idleTime>true</idleTime><connectTime>true</connectTime>")
    return hoja(
        '<ResultCollector guiclass="SummaryReport" testclass="ResultCollector" testname="Reporte resumen" enabled="true">'
        f'{b("ResultCollector.error_logging", False)}<objProp><name>saveConfig</name><value class="SampleSaveConfiguration">{guardar}</value></objProp>'
        f'{s("filename", "")}</ResultCollector>'
    )


def grupo_hilos(nombre, hilos, subida, bucle, hijos, duracion="", retraso="", planificador=False):
    el = (f'<ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="{escape(nombre)}" enabled="true">'
          f'{s("ThreadGroup.on_sample_error", "continue")}'
          '<elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" '
          'testclass="LoopController" testname="Controlador de bucle" enabled="true">'
          f'{b("LoopController.continue_forever", False)}{s("LoopController.loops", bucle)}'
          '</elementProp>'
          f'{s("ThreadGroup.num_threads", hilos)}{s("ThreadGroup.ramp_time", subida)}{b("ThreadGroup.scheduler", planificador)}'
          f'{s("ThreadGroup.duration", duracion)}{s("ThreadGroup.delay", retraso)}{b("ThreadGroup.same_user_on_next_iteration", True)}</ThreadGroup>')
    return arbol(el, hijos)


def plan(nombre, variables, hijos):
    args = "".join(
        f'<elementProp name="{k}" elementType="Argument">{s("Argument.name", k)}{s("Argument.value", v)}{s("Argument.metadata", "=")}</elementProp>'
        for k, v in variables.items())
    cabecera = ('<?xml version="1.0" encoding="UTF-8"?>\n<jmeterTestPlan version="1.2" properties="5.0" jmeter="5.6.3">\n<hashTree>\n')
    tp = (f'<TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="{escape(nombre)}" enabled="true">'
          f'{b("TestPlan.functional_mode", False)}{b("TestPlan.serialize_threadgroups", False)}'
          '<elementProp name="TestPlan.user_defined_variables" elementType="Arguments" guiclass="ArgumentsPanel" '
          f'testclass="Arguments" testname="Variables definidas por el usuario" enabled="true"><collectionProp name="Arguments.arguments">{args}</collectionProp></elementProp>'
          '</TestPlan>')
    return cabecera + arbol(tp, hijos) + "</hashTree>\n</jmeterTestPlan>\n"


def guardar(ruta, contenido):
    ruta = os.path.normpath(os.path.join(RAIZ, ruta))
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    print("escrito", os.path.relpath(ruta, os.path.join(RAIZ)))


# ------------------------------------------------------------ plan despliegue
def plan_despliegue():
    flujo = (
        peticion("Tarifas", "GET", "/api/tarifas")
        + peticion("SeleccionTarifaYCantidad", "POST", "/api/seleccion", '{"tarifa":"${tarifa}","cantidad":${cantidad}}',
                   cabeceras() + extractor_json("num_reserva", "reserva", "num_reserva_not_found"))
        + peticion("Debug Sampler (solo para depurar)", "GET", "/api/salud", None, "", habilitado=False)
        + peticion("Pago", "POST", "/api/pago", '{"reserva":"${num_reserva}"}',
                   cabeceras() + asercion_json("JSON Assertion: estado = APROBADO", "$.estado", "APROBADO"))
        + temporizador_uniforme(500, 1000)
        + reporte_resumen()
    )
    cuerpo = (
        csv("datos.csv", "tarifa,cantidad")
        + valores_por_defecto("127.0.0.1", "8080")
        # 200 usuarios entran en 300 s (5 minutos); cada uno recorre el flujo 1 vez
        + grupo_hilos("Seleccion de tarifa y Pago", 200, 300, 1, flujo)
    )
    guardar("pruebas/jmeter/Ticketmania.jmx", plan("Ticketmania", {}, cuerpo))


# -------------------------------------------------------- plan experimentación
def plan_experimentacion():
    P = lambda n, d: f"${{__P({n},{d})}}"
    jexl = lambda expr: f"${{__jexl3({expr})}}"

    def seleccion(extra=""):
        return peticion("SeleccionTarifaYCantidad", "POST", "/api/seleccion", '{"tarifa":"${tarifa}","cantidad":${cantidad}}',
                        cabeceras() + extractor_json("num_reserva", "reserva", "num_reserva_not_found")
                        + asercion_codigo("Código 201", "201")
                        + asercion_json("Total = precio x cantidad", "$.total", "${total_esperado}") + extra)

    flujo = (
        controlador_if("Si el flujo incluye Tarifas", jexl('"${__P(flujo,completo)}" != "seleccion"'),
                       peticion("Tarifas", "GET", "/api/tarifas", None, asercion_codigo("Código 200", "200")))
        + controlador_if("Seleccion con temporizador sincronizado (si sync=true)", jexl('"${__P(flujo,completo)}" != "tarifas" && "${__P(sync,false)}" == "true"'),
                         seleccion(temporizador_sincronizado(P("sync_grupo", 0))))
        + controlador_if("Seleccion normal (si sync=false)", jexl('"${__P(flujo,completo)}" != "tarifas" && "${__P(sync,false)}" != "true"'),
                         seleccion())
        + controlador_if("Pago (solo en el flujo completo)", jexl('"${__P(flujo,completo)}" == "completo"'),
                         peticion("Pago", "POST", "/api/pago", '{"reserva":"${num_reserva}"}',
                                  cabeceras() + asercion_codigo("Código 200", "200")
                                  + asercion_json("estado = APROBADO", "$.estado", "APROBADO")
                                  + asercion_json("Total cobrado = precio x cantidad", "$.total", "${total_esperado}")))
        + temporizador_uniforme(P("timer_const", 500), P("timer_rand", 1000))
        + reporte_resumen()
    )

    # Grupo principal + 3 grupos opcionales para escalonar la carga (0 hilos = no corre)
    grupos = grupo_hilos("Usuarios (grupo principal)", P("usuarios", 20), P("rampup", 1), P("iteraciones", 1), flujo,
                         duracion=P("duracion", 3600), retraso="0", planificador=True)
    for k in (2, 3, 4):
        grupos += grupo_hilos(f"Escalon {k}: usuarios que se suman", P(f"esc{k}", 0), P("esc_rampup", 5), P("iteraciones", 1), flujo,
                              duracion=P(f"esc{k}_duracion", 3600), retraso=P(f"esc{k}_retraso", 0), planificador=True)

    cuerpo = (
        csv(P("csv", "datos.csv"), "tarifa,cantidad,total_esperado")
        + valores_por_defecto(P("host", "127.0.0.1"), P("puerto", 8080))
        + grupos
    )
    guardar("pruebas/experimentacion/Experimentacion.jmx", plan("Experimentacion Ticketmania", {}, cuerpo))


if __name__ == "__main__":
    plan_despliegue()
    plan_experimentacion()
