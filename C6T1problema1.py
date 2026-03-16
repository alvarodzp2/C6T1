#librerias
import random
from datetime import datetime

# Clase Zona representa una zona individual del edificio (oficina, sala, laboratorio, etc.)

class Zona:
    def __init__(self, nombre: str, capacidad_maxima: int):
        """
        Inicializa una zona del edificio.
        """
        self.nombre = nombre
        self.capacidad_maxima = capacidad_maxima
        self.temperatura_actual = 22.0   # Temperatura inicial en grados Celsius
        self.ocupacion_actual = 0        # Personas presentes en este momento
        self.consumo_total_kwh = 0.0     # Acumulador de energia consumida
        self.historial_consumo = []      # Lista de registros (hora, consumo)

    def leer_sensor_temperatura(self) -> float:
        """
        Simula la lectura del sensor de temperatura de la zona.
        """
        variacion = random.uniform(-1.5, 1.5)
        temperatura_leida = round(self.temperatura_actual + variacion, 2)
        return temperatura_leida

    def actualizar_ocupacion(self, personas: int) -> None:
        """
        Actualiza el numero de personas presentes en la zona.
        """
        # Aseguramos que no supere la capacidad ni sea negativo
        self.ocupacion_actual = max(0, min(personas, self.capacidad_maxima))

    def calcular_temperatura_optima(self, hora: int, temperatura_exterior: float) -> float:
        """
        Calcula la temperatura ideal para la zona segun tres factores:
        la hora del dia, la ocupacion y el clima externo.
        """
        # Temperatura base segun horario laboral (8am a 6pm)
        if 8 <= hora <= 18:
            temp_base = 22.0
        else:
            # Fuera de horario se ahorra energia
            temp_base = 18.0

        # Ajuste por ocupacion: mas personas = mas calor corporal generado
        ajuste_ocupacion = -(self.ocupacion_actual * 0.3)

        # Ajuste por clima exterior: si supera 30 C afuera, enfriamos mas
        if temperatura_exterior > 30:
            ajuste_clima = -1.5
        elif temperatura_exterior < 10:
            ajuste_clima = 1.5
        else:
            ajuste_clima = 0.0

        temperatura_optima = temp_base + ajuste_ocupacion + ajuste_clima

        # Limites de seguridad: nunca menos de 16 ni mas de 28 grados
        temperatura_optima = max(16.0, min(28.0, temperatura_optima))

        return round(temperatura_optima, 2)

    def registrar_consumo(self, hora: int, kwh: float) -> None:
        """
        Registra el consumo de energia de esta zona en un momento dado.
        """
        self.consumo_total_kwh += kwh
        self.historial_consumo.append({
            "hora": hora,
            "kwh": round(kwh, 4)
        })

# Clase SistemaClimatico
class SistemaClimatico:
    def leer_temperatura_exterior(self) -> float:
        """
        Simula la lectura de la temperatura exterior del edificio.
        """
        return round(random.uniform(5.0, 40.0), 2)

# Clase Edificio

class Edificio:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.zonas: list[Zona] = []
        self.sistema_climatico = SistemaClimatico()

    def agregar_zona(self, zona: Zona) -> None:
        """
        Registra una nueva zona dentro del edificio.
        """
        self.zonas.append(zona)

    def enviar_senal_ajuste(self, zona: Zona, temperatura_objetivo: float) -> None:
        diferencia = temperatura_objetivo - zona.temperatura_actual

        if abs(diferencia) < 0.5:
            # Si la diferencia es minima, no se activa el sistema
            accion = "MANTENER"
        elif diferencia > 0:
            accion = "CALEFACCION"
        else:
            accion = "REFRIGERACION"

        print(
            f"  [{zona.nombre}] Senal: {accion} | "
            f"Actual: {zona.temperatura_actual} C -> Objetivo: {temperatura_objetivo} C"
        )

        # Simulamos que el sistema ajusta la temperatura gradualmente (50% del camino)
        zona.temperatura_actual = round(
            zona.temperatura_actual + (diferencia * 0.5), 2
        )

    def calcular_consumo_ajuste(self, zona: Zona, temperatura_objetivo: float) -> float:
        """
        Estima el consumo energetico necesario para realizar el ajuste de temperatura.
        """
        diferencia = abs(temperatura_objetivo - zona.temperatura_actual)
        # Consumo base: 0.1 kWh por grado de diferencia, escala con el tamano de la zona
        factor_zona = zona.capacidad_maxima / 10
        consumo = diferencia * 0.1 * factor_zona
        return round(consumo, 4)

    def ejecutar_ciclo(self, hora: int) -> None:
        print(f"\n{'='*60}")
        print(f"Edificio: {self.nombre} | Hora: {hora:02d}:00")
        print(f"{'='*60}")

        temperatura_exterior = self.sistema_climatico.leer_temperatura_exterior()
        print(f"Temperatura exterior: {temperatura_exterior} C\n")

        for zona in self.zonas:
            # Simulamos ocupacion aleatoria segun hora del dia
            if 8 <= hora <= 18:
                ocupacion = random.randint(1, zona.capacidad_maxima)
            else:
                ocupacion = random.randint(0, max(1, zona.capacidad_maxima // 5))

            zona.actualizar_ocupacion(ocupacion)

            # Paso 1: leer el sensor de temperatura
            temp_sensor = zona.leer_sensor_temperatura()

            # Paso 2: calcular la temperatura optima
            temp_optima = zona.calcular_temperatura_optima(hora, temperatura_exterior)

            # Paso 3: calcular consumo estimado antes del ajuste
            consumo = self.calcular_consumo_ajuste(zona, temp_optima)

            # Paso 4: enviar senal de ajuste al HVAC
            self.enviar_senal_ajuste(zona, temp_optima)

            # Paso 5: registrar el consumo
            zona.registrar_consumo(hora, consumo)

            print(
                f"  Sensor: {temp_sensor} C | "
                f"Ocupacion: {zona.ocupacion_actual}/{zona.capacidad_maxima} | "
                f"Optima: {temp_optima} C | "
                f"Consumo: {consumo} kWh"
            )

    def generar_reporte_consumo(self) -> None:

        print(f"\n{'='*60}")
        print("reporte de l consumo energetico")
        print(f"Edificio: {self.nombre}")
        print(f"{'='*60}")

        consumo_edificio_total = 0.0

        for zona in self.zonas:
            ciclos = len(zona.historial_consumo)
            promedio = (
                zona.consumo_total_kwh / ciclos if ciclos > 0 else 0.0
            )
            consumo_edificio_total += zona.consumo_total_kwh

            print(f"\nZona: {zona.nombre}")
            print(f"  Ciclos registrados : {ciclos}")
            print(f"  Consumo total      : {round(zona.consumo_total_kwh, 4)} kWh")
            print(f"  Consumo promedio   : {round(promedio, 4)} kWh/ciclo")

        print(f"\nCONSUMO TOTAL DEL EDIFICIO: {round(consumo_edificio_total, 4)} kWh")
        print(f"{'='*60}")

# Programa principal
if __name__ == "__main__":
    # Crear el edificio
    edificio = Edificio("Torre Central")

    # Definir zonas con nombre y capacidad maxima de personas
    zonas_config = [
        ("Oficina A",      20),
        ("Sala Reuniones", 10),
        ("Laboratorio",    15),
        ("Recepcion",       8),
        ("Cafeteria",      30),
    ]

    for nombre, capacidad in zonas_config:
        edificio.agregar_zona(Zona(nombre, capacidad))

    # Simular varios ciclos a lo largo del dia
    horas_simuladas = [7, 9, 12, 15, 18, 21]

    for hora in horas_simuladas:
        edificio.ejecutar_ciclo(hora)

    # Mostrar reporte final de consumo
    edificio.generar_reporte_consumo()