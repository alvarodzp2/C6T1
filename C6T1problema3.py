#librerias

from dataclasses import dataclass, field

@dataclass
class SensorData:
    distancia_frontal: float   # metros al obstaculo mas cercano al frente
    distancia_lateral: float   # metros al obstaculo lateral
    congestion:        float   # porcentaje de congestion del tramo (0-100)


@dataclass
class Nodo:
    nombre:   str
    vecinos:  dict = field(default_factory=dict)  # {nombre_nodo: distancia_km}


@dataclass
class Vehiculo:
    nombre:         str
    velocidad:      float = 0.0   # km/h
    estado:         str   = "detenido"
    ruta_actual:    list  = field(default_factory=list)
    log_energia:    list  = field(default_factory=list)

#funcion quesimula la lectura; en hardware real se conectaria al driver del sensor
def leer_sensores(vehiculo: Vehiculo) -> SensorData:
    print(f"\n  -- Sensores de {vehiculo.nombre} --")
    dist_f = leer_float("  Distancia frontal al obstaculo (m, 0=libre): ", minimo=0)
    dist_l = leer_float("  Distancia lateral al obstaculo (m, 0=libre): ", minimo=0)
    cong   = leer_float("  Congestion del tramo actual (0-100%%): ", minimo=0, maximo=100)
    return SensorData(dist_f, dist_l, cong)

# funcion que calcula la ruta optima con Dijkstra y actualiza el vehiculo modifica vehiculo.ruta_actual — efecto de lado explicito
def calcular_ruta_optima(vehiculo: Vehiculo, grafo: dict[str, Nodo],
                          origen: str, destino: str) -> None:
    # distancias iniciales: infinito para todos excepto origen
    distancias = {n: float("inf") for n in grafo}
    distancias[origen] = 0
    previo     = {n: None for n in grafo}
    pendientes = set(grafo.keys())

    while pendientes:
        # nodo con menor distancia conocida
        actual = min(pendientes, key=lambda n: distancias[n])
        if distancias[actual] == float("inf"):
            break
        pendientes.remove(actual)
        if actual == destino:
            break
        for vecino, peso in grafo[actual].vecinos.items():
            nueva = distancias[actual] + peso
            if nueva < distancias[vecino]:
                distancias[vecino] = nueva
                previo[vecino]     = actual

    # reconstruye el camino
    camino = []
    nodo   = destino
    while nodo:
        camino.append(nodo)
        nodo = previo[nodo]
    camino.reverse()

    vehiculo.ruta_actual = camino if camino[0] == origen else []
    dist_total = distancias[destino]
    print(f"\n  Ruta optima: {' -> '.join(vehiculo.ruta_actual)}")
    print(f"  Distancia total: {dist_total:.2f} km")

#funcion apra detectar obstaulos
def detectar_obstaculo(sensores: SensorData, umbral_frenado: float,
                        umbral_desvio: float) -> str:
    if sensores.distancia_frontal == 0 and sensores.distancia_lateral == 0:
        return "libre"
    if sensores.distancia_frontal > 0 and sensores.distancia_frontal <= umbral_frenado:
        return "frenar"
    if sensores.distancia_lateral > 0 and sensores.distancia_lateral <= umbral_desvio:
        return "desviar"
    return "libre"


# funcion aora ajustar la veliocidad segun trafico y obstaculo

def ajustar_velocidad(vehiculo: Vehiculo, sensores: SensorData,
                       accion: str, vel_max: float) -> None:
    # reduccion por congestion: a 100% de congestion la velocidad baja 80%
    factor_trafico = 1 - (sensores.congestion / 100) * 0.8

    if accion == "frenar":
        vehiculo.velocidad = 0.0
        vehiculo.estado    = "detenido por obstaculo"
    elif accion == "desviar":
        vehiculo.velocidad = vel_max * factor_trafico * 0.5   # mitad de velocidad al desviar
        vehiculo.estado    = "desviando"
    else:
        vehiculo.velocidad = vel_max * factor_trafico
        vehiculo.estado    = "en movimiento"

    vehiculo.log_energia.append(round(vehiculo.velocidad, 2))
    print(f"\n  Estado    : {vehiculo.estado}")
    print(f"  Velocidad : {vehiculo.velocidad:.2f} km/h")


def leer_float(msg: str, minimo: float = None, maximo: float = None) -> float:
    while True:
        try:
            v = float(input(msg))
            if minimo is not None and v < minimo:
                print(f"  Minimo: {minimo}"); continue
            if maximo is not None and v > maximo:
                print(f"  Maximo: {maximo}"); continue
            return v
        except: print("  Valor invalido.")

def leer_int(msg: str, minimo: int = 1) -> int:
    while True:
        try:
            v = int(input(msg))
            if v >= minimo: return v
            print(f"  Minimo: {minimo}")
        except: print("  Valor invalido.")


def construir_grafo() -> dict[str, Nodo]:
    n = leer_int("\nCantidad de nodos (puntos de entrega): ")
    nodos = {}
    nombres = []
    for i in range(n):
        nombre = input(f"  Nombre del nodo {i+1}: ").strip() or f"N{i+1}"
        nodos[nombre] = Nodo(nombre)
        nombres.append(nombre)

    print(f"\n  Nodos disponibles: {nombres}")
    e = leer_int("Cantidad de conexiones (aristas): ", minimo=1)
    for _ in range(e):
        print(f"  Nodos disponibles: {nombres}")
        a    = input("  Desde: ").strip()
        b    = input("  Hasta: ").strip()
        dist = leer_float("  Distancia (km): ", minimo=0.1)
        if a in nodos and b in nodos:
            nodos[a].vecinos[b] = dist
            nodos[b].vecinos[a] = dist  # grafo no dirigido
        else:
            print("  Nodo no encontrado, conexion ignorada.")
    return nodos

#programa
if __name__ == "__main__":
    print("sistema de navegacion vehiculo")

    nombre_v = input("\nNombre del vehiculo: ").strip() or "VAuto-1"
    vel_max  = leer_float("Velocidad maxima (km/h): ", minimo=1)

    grafo  = construir_grafo()
    nodos  = list(grafo.keys())

    print(f"\n  Nodos: {nodos}")
    origen  = input("Nodo de origen : ").strip()
    destino = input("Nodo de destino: ").strip()

    umbral_frenado = leer_float("\nDistancia minima frontal para frenar (m): ", minimo=0.1)
    umbral_desvio  = leer_float("Distancia minima lateral para desviar (m): ", minimo=0.1)

    vehiculo = Vehiculo(nombre_v)

    # flujo principal
    print(f"iniciod e ismulacion")

    calcular_ruta_optima(vehiculo, grafo, origen, destino)   # procedimiento

    sensores = leer_sensores(vehiculo)                        # funcion
    accion   = detectar_obstaculo(sensores,                   # funcion
                                   umbral_frenado, umbral_desvio)
    print(f"  Accion detectada: {accion}")

    ajustar_velocidad(vehiculo, sensores, accion, vel_max)   # procedimiento

    # resumen
    print(f"  RESUMEN  |  {vehiculo.nombre}")
    print(f"  Ruta     : {' -> '.join(vehiculo.ruta_actual)}")
    print(f"  Estado   : {vehiculo.estado}")
    print(f"  Velocidad: {vehiculo.velocidad:.2f} km/h")
    print(f"  Log vel. : {vehiculo.log_energia}")