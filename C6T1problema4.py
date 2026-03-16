#librerias
from dataclasses import dataclass, field
# clases

@dataclass
class Maquina:
    nombre:           str
    eficiencia:       float        # porcentaje 0-100
    horas_uso:        float        # horas acumuladas desde ultimo mantenimiento
    intervalo_mant:   float        # cada cuantas horas se requiere mantenimiento
    en_mantenimiento: bool  = False
    historial:        list  = field(default_factory=list)


@dataclass
class Fabrica:
    nombre:    str
    maquinas:  list = field(default_factory=list)
    programa:  list = field(default_factory=list)   # lista de tareas programadas

# funcion que monitorea el estado de las maquinas y retorna un resumen no modifica ningun objeto; solo lee y retorna informacion
def monitorear_maquinas(maquinas: list[Maquina]) -> list[dict]:
    estados = []
    for m in maquinas:
        estados.append({
            "nombre"         : m.nombre,
            "eficiencia"     : m.eficiencia,
            "horas_uso"      : m.horas_uso,
            "mantenimiento"  : m.en_mantenimiento,
            "necesita_mant"  : m.horas_uso >= m.intervalo_mant,
        })
    return estados

def planificar_mantenimiento(fabrica: Fabrica) -> None:
    print(f"\n  -- Mantenimiento preventivo | {fabrica.nombre} --")
    hubo = False
    for m in fabrica.maquinas:
        if m.horas_uso >= m.intervalo_mant:
            m.en_mantenimiento = True
            m.horas_uso        = 0.0      # reinicia contador tras programar mant.
            m.eficiencia       = min(100.0, m.eficiencia + 15.0)  # recupera eficiencia
            m.historial.append(f"Mantenimiento programado. Eficiencia -> {m.eficiencia:.1f}%")
            print(f"  {m.nombre}: mantenimiento programado. Eficiencia restaurada a {m.eficiencia:.1f}%")
            hubo = True
    if not hubo:
        print("  Ninguna maquina requiere mantenimiento en este momento.")

# fucnion que  analiza el rendimiento global de la produccion y retorna metricas
def analizar_rendimiento(maquinas: list[Maquina], demanda: float) -> dict:
    activas      = [m for m in maquinas if not m.en_mantenimiento]
    inactivas    = [m for m in maquinas if m.en_mantenimiento]
    efic_prom    = sum(m.eficiencia for m in activas) / len(activas) if activas else 0
    capacidad    = sum(m.eficiencia for m in activas)    # unidades ponderadas
    cobertura    = min(100.0, (capacidad / demanda * 100)) if demanda > 0 else 0

    return {
        "total_maquinas"  : len(maquinas),
        "activas"         : len(activas),
        "en_mantenimiento": len(inactivas),
        "eficiencia_prom" : round(efic_prom, 2),
        "capacidad_total" : round(capacidad, 2),
        "demanda"         : demanda,
        "cobertura_pct"   : round(cobertura, 2),
    }
# PROCEDIMIENTO: ajusta la programacion de produccion segun la demanda
# Modifica fabrica.programa — efecto de lado explicito
# ---------------------------------------------------------------------------
def ajustar_programacion(fabrica: Fabrica, demanda: float) -> None:
    fabrica.programa.clear()
    activas = [m for m in fabrica.maquinas if not m.en_mantenimiento]

    if not activas:
        print("\n  Sin maquinas activas para programar.")
        return

    # distribuye la demanda proporcionalmente a la eficiencia de cada maquina
    efic_total = sum(m.eficiencia for m in activas)
    print(f"\n  -- Programacion ajustada | demanda={demanda} unidades --")
    for m in activas:
        asignacion = round((m.eficiencia / efic_total) * demanda, 2)
        fabrica.programa.append({"maquina": m.nombre, "unidades": asignacion})
        print(f"  {m.nombre}: {asignacion} unidades  (eficiencia {m.eficiencia}%)")

#funcione spara que usuario ingrese datos
def leer_float(msg: str, minimo: float = 0.0, maximo: float = None) -> float:
    while True:
        try:
            v = float(input(msg))
            if v < minimo:
                print(f"  Minimo: {minimo}"); continue
            if maximo is not None and v > maximo:
                print(f"  Maximo: {maximo}"); continue
            return v
        except:
            print("  Valor invalido.")

def leer_int(msg: str, minimo: int = 1) -> int:
    while True:
        try:
            v = int(input(msg))
            if v >= minimo: return v
            print(f"  Minimo: {minimo}")
        except:
            print("  Valor invalido.")

#inicio del sistema
if __name__ == "__main__":
    print("  OPTIMIZACION DE PRODUCCION - FABRICA")

    nombre_f = input("\nNombre de la fabrica: ").strip() or "Fabrica-1"
    n        = leer_int("Cantidad de maquinas: ")

    maquinas = []
    for i in range(1, n + 1):
        print(f"\n  Maquina {i}")
        nombre  = input("  Nombre: ").strip() or f"M-{i}"
        efic    = leer_float("  Eficiencia actual (0-100): ", 0, 100)
        horas   = leer_float("  Horas de uso acumuladas: ", 0)
        interv  = leer_float("  Intervalo de mantenimiento (horas): ", 1)
        maquinas.append(Maquina(nombre, efic, horas, interv))

    demanda = leer_float("\nDemanda de produccion (unidades): ", minimo=1)

    fabrica = Fabrica(nombre_f, maquinas)

    # flujo principal
    print(f"  SIMULACION | {fabrica.nombre}")

    # 1. monitoreo
    estados = monitorear_maquinas(fabrica.maquinas)
    print(f"\n  -- Estado actual de maquinas --")
    print(f"  {'Nombre':<14} {'Efic%':>6} {'Horas':>7} {'Mant?':>6} {'Necesita':>9}")
    print("  " + "-" * 46)
    for e in estados:
        print(f"  {e['nombre']:<14} {e['eficiencia']:>6.1f} {e['horas_uso']:>7.1f}"
              f" {'SI' if e['mantenimiento'] else 'NO':>6}"
              f" {'SI' if e['necesita_mant'] else 'NO':>9}")

    # 2. mantenimiento preventivo
    planificar_mantenimiento(fabrica)

    # 3. analisis de rendimiento
    metricas = analizar_rendimiento(fabrica.maquinas, demanda)
    print(f"\n  -- Rendimiento --")
    for k, v in metricas.items():
        print(f"  {k:<20}: {v}")

    # 4. ajuste de programacion
    ajustar_programacion(fabrica, demanda)

    # resumen final
    print(f"  PROGRAMA FINAL DE PRODUCCION")
    for tarea in fabrica.programa:
        print(f"  {tarea['maquina']:<14} -> {tarea['unidades']} unidades")