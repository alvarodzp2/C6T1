# C6T1 - Implementacion de Funciones y Procedimientos para la Resolucion de Problemas Reales

**Tema:** 4.1 Introduccion a la modularidad | 4.2 Creacion y uso de funciones simples  
**Lenguaje:** Python 3.12  

---

## Estructura del repositorio

```
/
├── problema1_edificio.py
├── problema2_inventario.py
├── problema3_vehiculo_autonomo.py
├── problema4_fabrica.py
├── problema5_riego.py
└── README.md
```

---

## Problema 1: Control de Temperatura en un Edificio Inteligente

**Archivo:** `problema1_edificio.py`

El sistema simula el control climatico de un edificio con multiples zonas. Cada zona tiene su propio sensor, calcula su temperatura optima y recibe senales de ajuste.

### Funciones y su rol

| Funcion / Procedimiento | Tipo | Descripcion |
|---|---|---|
| `leer_sensor_temperatura()` | Funcion | Simula la lectura del sensor de temperatura de una zona. Retorna un float con variacion aleatoria. No modifica estado. |
| `calcular_temperatura_optima()` | Funcion | Calcula la temperatura ideal combinando hora del dia, ocupacion y temperatura exterior. Retorna un float. No modifica estado. |
| `enviar_senal_ajuste()` | Procedimiento | Decide la accion (CALEFACCION / REFRIGERACION / MANTENER) y modifica `zona.temperatura_actual`. Efecto de lado explicito. |
| `registrar_consumo()` | Funcion | Acumula el consumo en kWh y agrega un registro al historial de la zona. |
| `generar_reporte_consumo()` | Funcion | Recorre todas las zonas y muestra consumo total y promedio por ciclo. |

### Impacto en rendimiento

Separar `calcular_temperatura_optima()` de `enviar_senal_ajuste()` permite recalcular el objetivo sin activar el hardware. Esto evita ciclos de ajuste innecesarios cuando la diferencia es menor a 0.5 C. `registrar_consumo()` usa una lista como acumulador de O(1) por insercion, lo que mantiene el historial sin costo significativo incluso con muchos ciclos simulados.

---

## Problema 2: Gestion de Inventario en un Almacen

**Archivo:** `problema2_inventario.py`

Sistema interactivo de inventario con menu de consola. Registra entradas y salidas, calcula niveles optimos y genera alertas automaticas.

### Funciones y su rol

| Funcion / Procedimiento | Tipo | Descripcion |
|---|---|---|
| `registrar_entrada()` | Funcion | Incrementa el stock del producto y registra el movimiento con fecha automatica. |
| `registrar_salida()` | Funcion | Valida disponibilidad, decrementa el stock y dispara una alerta inmediata si cae bajo el minimo. |
| `calcular_nivel_optimo()` | Procedimiento | Calcula el punto medio entre stock minimo y maximo y muestra cuanto hay que pedir. Modifica la salida pero no el objeto. |
| `generar_alertas()` | Funcion | Recorre todos los productos y clasifica cada uno como SIN STOCK, BAJO, EXCESO o NORMAL. Retorna el conteo de alertas. |

### Impacto en rendimiento

Separar `registrar_entrada()` y `registrar_salida()` en dos funciones independientes permite validar stock disponible unicamente en la salida, sin ejecutar esa logica en entradas. `generar_alertas()` hace un unico recorrido O(N) sobre todos los productos, lo que escala linealmente con el tamano del inventario.

---

## Problema 3: Sistema de Navegacion para un Vehiculo Autonomo

**Archivo:** `problema3_vehiculo_autonomo.py`

Sistema que planifica la ruta optima entre nodos usando Dijkstra, lee datos de sensores y ajusta la velocidad segun obstaculos y congestion.

### Funciones y su rol

| Funcion / Procedimiento | Tipo | Descripcion |
|---|---|---|
| `leer_sensores()` | Funcion | Solicita distancias frontal y lateral al obstaculo y el porcentaje de congestion. Retorna un objeto `SensorData`. No modifica nada. |
| `calcular_ruta_optima()` | Procedimiento | Ejecuta Dijkstra sobre el grafo y escribe el camino resultante en `vehiculo.ruta_actual`. Efecto de lado explicito. |
| `detectar_obstaculo()` | Funcion | Compara las distancias del sensor contra los umbrales definidos por el usuario. Retorna la accion recomendada: `"frenar"`, `"desviar"` o `"libre"`. |
| `ajustar_velocidad()` | Procedimiento | Calcula la velocidad resultante aplicando el factor de trafico y la accion del sensor. Modifica `vehiculo.velocidad` y `vehiculo.estado`. |

### Impacto en rendimiento

Dijkstra en `calcular_ruta_optima()` corre en O(N²) con la implementacion de conjunto simple, adecuado para grafos de distribucion con decenas de nodos. `detectar_obstaculo()` es O(1) al ser una comparacion directa, lo que garantiza respuesta en tiempo real ante obstaculos. Separar deteccion de ajuste permite cambiar los umbrales sin tocar la logica de velocidad.

---

## Problema 4: Optimizacion de la Produccion en una Fabrica

**Archivo:** `problema4_fabrica.py`

Sistema que monitorea maquinas, programa mantenimiento preventivo, analiza rendimiento y distribuye la carga de produccion segun la demanda.

### Funciones y su rol

| Funcion / Procedimiento | Tipo | Descripcion |
|---|---|---|
| `monitorear_maquinas()` | Funcion | Recorre la lista de maquinas y retorna un listado de diccionarios con su estado actual. No modifica ningun objeto. |
| `planificar_mantenimiento()` | Procedimiento | Detecta maquinas que superaron su intervalo de horas, activa `en_mantenimiento`, reinicia horas y restaura eficiencia. Efecto de lado explicito. |
| `analizar_rendimiento()` | Funcion | Calcula eficiencia promedio, capacidad total activa y porcentaje de cobertura frente a la demanda. Retorna un diccionario de metricas. |
| `ajustar_programacion()` | Procedimiento | Distribuye la demanda entre maquinas activas proporcional a su eficiencia y actualiza `fabrica.programa`. |

### Impacto en rendimiento

`monitorear_maquinas()` y `analizar_rendimiento()` son funciones puras: se pueden llamar en cualquier momento sin riesgo de modificar el sistema. Esto permite mostrar el estado antes y despues del mantenimiento sin efectos secundarios. `planificar_mantenimiento()` concentra todos los efectos de lado en un solo lugar, facilitando el rastreo de cambios de estado.

---

## Problema 5: Sistema de Riego Automatizado para Agricultura

**Archivo:** `problema5_riego.py`

Sistema que combina lectura de sensores de humedad y prevision meteorologica para calcular cuanta agua necesita cada seccion del campo y controlar las valvulas.

### Funciones y su rol

| Funcion / Procedimiento | Tipo | Descripcion |
|---|---|---|
| `leer_sensores_humedad()` | Funcion | Solicita el nivel de humedad actual de cada seccion. Retorna un diccionario `{nombre: humedad}`. No modifica nada. |
| `consultar_prevision_meteorologica()` | Funcion | Solicita lluvia prevista, temperatura y humedad ambiental. Retorna un diccionario con las condiciones climaticas. |
| `calcular_riego_optimo()` | Procedimiento | Combina humedad actual con el aporte estimado de lluvia, calcula el deficit respecto al rango del cultivo y escribe `agua_asignada` en cada seccion. |
| `controlar_valvulas()` | Funcion | Evalua el agua asignada de cada seccion y retorna el diccionario de acciones `{nombre: "abrir"/"cerrar"}`. No modifica ningun objeto. |

### Impacto en rendimiento

Separar `leer_sensores_humedad()` y `consultar_prevision_meteorologica()` del calculo permite actualizar cualquiera de las dos fuentes de datos de forma independiente sin reejecutar el sistema completo. `calcular_riego_optimo()` concentra toda la logica de negocio en un procedimiento, lo que hace que cambiar la formula de riego no afecte la lectura de sensores ni el control de valvulas. `controlar_valvulas()` al ser una funcion pura puede ejecutarse multiples veces con los mismos datos sin efectos secundarios.

---

## Principios aplicados en todos los problemas

**Modularidad:** cada funcion realiza exactamente una tarea. Cambiar la logica de una no obliga a modificar las demas.

**Funciones vs procedimientos:** las funciones retornan valores sin modificar estado externo. Los procedimientos modifican objetos de forma explicita y no retornan valores utiles. Esta separacion hace predecible donde ocurren los cambios de estado.

**Reutilizabilidad:** las funciones de calculo (temperatura optima, estadisticas, deteccion de obstaculos) pueden usarse con cualquier fuente de datos sin modificacion.

**OOP:** cada dominio tiene sus propias clases con responsabilidades claras, evitando variables globales y facilitando la extension del sistema.
