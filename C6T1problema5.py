#librerias 
from dataclasses import dataclass, field
#clases

@dataclass
class Seccion:
    nombre:         str
    humedad:        float = 0.0   # porcentaje actual 0-100
    agua_asignada:  float = 0.0   # litros calculados
    valvula_abierta: bool = False
    historial:      list  = field(default_factory=list)


@dataclass
class Cultivo:
    nombre:          str
    humedad_minima:  float   # humedad minima que necesita el cultivo
    humedad_maxima:  float   # humedad maxima tolerable


@dataclass
class Campo:
    nombre:    str
    secciones: list = field(default_factory=list)


# funcion que lee humedad del suelo por seccion desde consola 
def leer_sensores_humedad(secciones: list[Seccion]) -> dict[str, float]:
    print("\n  -- Lectura de sensores de humedad --")
    lecturas = {}
    for s in secciones:
        h = leer_float(f"  Humedad actual en {s.nombre} (0-100%%): ", 0, 100)
        lecturas[s.nombre] = h
    return lecturas

# fucnion que  consulta prevision meteorologica ingresada por el usuario
def consultar_prevision_meteorologica() -> dict:
    print("\n  -- Prevision meteorologica --")
    lluvia    = leer_float("  Lluvia prevista (mm): ", 0)
    temp      = leer_float("  Temperatura prevista (C): ")
    humedad_a = leer_float("  Humedad ambiental prevista (0-100%%): ", 0, 100)
    return {
        "lluvia_mm"  : lluvia,
        "temperatura": temp,
        "humedad_amb": humedad_a,
    }

# funcion que calcula la cantidad optima de riego y actualiza cada seccion modifica seccion.humedad y seccion.agua_asignada — efecto de lado explicito
def calcular_riego_optimo(campo: Campo, lecturas: dict[str, float],
                           prevision: dict, cultivo: Cultivo,
                           litros_por_punto: float) -> None:
    print(f"\n  -- Calculo de riego optimo | {campo.nombre} --")
    for s in campo.secciones:
        humedad_actual = lecturas[s.nombre]
        s.humedad      = humedad_actual

        # la lluvia prevista aporta humedad; se reduce la necesidad de riego
        aporte_lluvia  = prevision["lluvia_mm"] * 0.5   # factor de absorcion del suelo
        humedad_efectiva = min(100.0, humedad_actual + aporte_lluvia)

        if humedad_efectiva >= cultivo.humedad_minima:
            s.agua_asignada = 0.0
            motivo = "humedad suficiente"
        elif humedad_efectiva >= cultivo.humedad_maxima:
            s.agua_asignada = 0.0
            motivo = "humedad en rango optimo"
        else:
            deficit         = cultivo.humedad_minima - humedad_efectiva
            s.agua_asignada = round(deficit * litros_por_punto, 2)
            motivo          = f"deficit de {deficit:.1f}%"

        s.historial.append({
            "humedad"       : humedad_efectiva,
            "agua_asignada" : s.agua_asignada,
        })
        print(f"  {s.nombre:<14}: {s.agua_asignada:>7.2f} L  ({motivo})")


#funcion quedetermina el estado de cada valvula segun el agua asignada
def controlar_valvulas(secciones: list[Seccion]) -> dict[str, str]:
    acciones = {}
    for s in secciones:
        if s.agua_asignada > 0:
            acciones[s.nombre] = "abrir"
        else:
            acciones[s.nombre] = "cerrar"
    return acciones


def aplicar_valvulas(campo: Campo, acciones: dict[str, str]) -> None:
    print(f"\n  -- Control de valvulas --")
    for s in campo.secciones:
        s.valvula_abierta = acciones[s.nombre] == "abrir"
        estado = "ABIERTA" if s.valvula_abierta else "CERRADA"
        print(f"  Valvula {s.nombre:<14}: {estado}  ({s.agua_asignada:.2f} L)")
#ingreso de datos por usuario
def leer_float(msg: str, minimo: float = None, maximo: float = None) -> float:
    while True:
        try:
            v = float(input(msg))
            if minimo is not None and v < minimo:
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

# inicio del sisema
if __name__ == "__main__":
    print("  SISTEMA DE RIEGO AUTOMATIZADO")

    nombre_campo = input("\nNombre del campo: ").strip() or "Campo-1"
    n            = leer_int("Cantidad de secciones: ")

    secciones = []
    for i in range(1, n + 1):
        nombre = input(f"  Nombre seccion {i}: ").strip() or f"Seccion-{i}"
        secciones.append(Seccion(nombre))

    print("\n  -- Datos del cultivo --")
    nombre_c  = input("  Nombre del cultivo: ").strip() or "Cultivo"
    hum_min   = leer_float("  Humedad minima requerida (0-100%%): ", 0, 100)
    hum_max   = leer_float("  Humedad maxima tolerable (0-100%%): ", 0, 100)
    lit_punto = leer_float("  Litros necesarios por punto de deficit: ", 0.1)

    cultivo = Cultivo(nombre_c, hum_min, hum_max)
    campo   = Campo(nombre_campo, secciones)

    # flujo principal
    print(f"simulacion| {campo.nombre}")

    lecturas  = leer_sensores_humedad(campo.secciones)          # funcion
    prevision = consultar_prevision_meteorologica()             # funcion
    calcular_riego_optimo(campo, lecturas, prevision,           # procedimiento
                           cultivo, lit_punto)
    acciones  = controlar_valvulas(campo.secciones)             # funcion
    aplicar_valvulas(campo, acciones)                           # procedimiento

    # resumen
    total_agua = sum(s.agua_asignada for s in campo.secciones)
    print(f"resumen final")
    print(f"  Campo    : {campo.nombre}")
    print(f"  Cultivo  : {cultivo.nombre}  "
          f"(humedad optima {cultivo.humedad_minima}% - {cultivo.humedad_maxima}%)")
    print(f"  Agua total asignada: {total_agua:.2f} L")
    abiertas = sum(1 for s in campo.secciones if s.valvula_abierta)
    print(f"  Valvulas abiertas  : {abiertas} / {len(campo.secciones)}")