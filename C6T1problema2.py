# librerias
import os
from datetime import datetime

# constantes
STOCK_MINIMO_DEFAULT = 10
STOCK_MAXIMO_DEFAULT = 100

# clase: representa un producto en el inventario
class Producto:

    def __init__(self, codigo: str, nombre: str, stock: int,
                 stock_minimo: int = STOCK_MINIMO_DEFAULT,
                 stock_maximo: int = STOCK_MAXIMO_DEFAULT):
        self.codigo       = codigo
        self.nombre       = nombre
        self.stock        = stock
        self.stock_minimo = stock_minimo
        self.stock_maximo = stock_maximo

    def __str__(self) -> str:
        return f"[{self.codigo}] {self.nombre}  (stock: {self.stock})"


# clase: registra cada movimiento con fecha automatica
class Movimiento:

    def __init__(self, codigo: str, tipo: str, cantidad: int, motivo: str):
        self.codigo   = codigo
        self.tipo     = tipo
        self.cantidad = cantidad
        self.motivo   = motivo
        self.fecha    = datetime.now().strftime("%Y-%m-%d %H:%M")

    def __str__(self) -> str:
        return (f"  {self.fecha}  {self.tipo:<8} "
                f"Cod:{self.codigo}  Cant:{self.cantidad:>4}  {self.motivo}")


# clase: logica principal del almacen
class Almacen:

    def __init__(self):
        self.productos:   dict[str, Producto] = {}
        self.movimientos: list[Movimiento]    = []

    # funcion 1: registrar entrada de productos
    def registrar_entrada(self, codigo: str, cantidad: int, motivo: str = "Reabastecimiento") -> None:
        producto = self._buscar_producto(codigo)
        if producto is None:
            return
        producto.stock += cantidad
        self.movimientos.append(Movimiento(codigo, "ENTRADA", cantidad, motivo))
        print(f"  Entrada registrada: +{cantidad}  ->  stock actual: {producto.stock}")

    # funcion 2: registrar salida de productos
    def registrar_salida(self, codigo: str, cantidad: int, motivo: str = "Venta") -> None:
        producto = self._buscar_producto(codigo)
        if producto is None:
            return
        if cantidad > producto.stock:
            print(f"  Stock insuficiente. Disponible: {producto.stock}  Solicitado: {cantidad}")
            return
        producto.stock -= cantidad
        self.movimientos.append(Movimiento(codigo, "SALIDA", cantidad, motivo))
        print(f"  Salida registrada:  -{cantidad}  ->  stock actual: {producto.stock}")
        self._alerta_inmediata(producto)

    # procedimiento 3: calcular nivel optimo de inventario
    def calcular_nivel_optimo(self, codigo: str) -> None:
        producto = self._buscar_producto(codigo)
        if producto is None:
            return
        optimo         = (producto.stock_minimo + producto.stock_maximo) // 2
        cantidad_pedir = max(0, optimo - producto.stock)

        print(f"\n  Nivel optimo - {producto.nombre}")
        print(f"    Stock actual    : {producto.stock}")
        print(f"    Stock minimo    : {producto.stock_minimo}")
        print(f"    Stock maximo    : {producto.stock_maximo}")
        print(f"    Nivel optimo    : {optimo}")
        print(f"    Unidades a pedir: {cantidad_pedir}")

    # funcion 4: generar alertas de reabastecimiento
    def generar_alertas(self) -> None:
        print("  ALERTAS DE REABASTECIMIENTO")
        alertas = 0
        for producto in self.productos.values():
            if producto.stock == 0:
                print(f"  [SIN STOCK]  {producto.nombre}  ->  pedir {producto.stock_maximo} unidades")
                alertas += 1
            elif producto.stock <= producto.stock_minimo:
                pedir = producto.stock_maximo - producto.stock
                print(f"  [BAJO]       {producto.nombre}  ->  pedir {pedir} unidades")
                alertas += 1
            elif producto.stock >= producto.stock_maximo:
                exceso = producto.stock - producto.stock_maximo
                print(f"  [EXCESO]     {producto.nombre}  ->  reducir {exceso} unidades")
                alertas += 1
        if alertas == 0:
            print("  Todos los productos en niveles normales.")

    # agrega un producto nuevo
    def agregar_producto(self, codigo: str, nombre: str, stock: int,
                         stock_minimo: int = STOCK_MINIMO_DEFAULT,
                         stock_maximo: int = STOCK_MAXIMO_DEFAULT) -> None:
        if codigo in self.productos:
            print(f"  El codigo {codigo} ya existe.")
            return
        self.productos[codigo] = Producto(codigo, nombre, stock, stock_minimo, stock_maximo)
        print(f"  Producto agregado: {self.productos[codigo]}")

    # muestra todos los productos con su estado
    def mostrar_inventario(self) -> None:
        print("inventario actual")
        if not self.productos:
            print("  Sin productos registrados.")
            return
        for p in self.productos.values():
            print(f"  {p.codigo:<8} {p.nombre:<25} Stock: {p.stock:>4}  [{self._estado(p)}]")

    # muestra historial de movimientos
    def mostrar_historial(self) -> None:
        print("historial de movimientos")
        if not self.movimientos:
            print("  Sin movimientos registrados.")
            return
        for mov in self.movimientos:
            print(mov)

    def _buscar_producto(self, codigo: str):
        producto = self.productos.get(codigo)
        if producto is None:
            print(f"  Codigo '{codigo}' no encontrado.")
        return producto

    def _alerta_inmediata(self, producto: Producto) -> None:
        if producto.stock <= producto.stock_minimo:
            print(f"  ALERTA: {producto.nombre} bajo en stock ({producto.stock} unidades)")

    def _estado(self, p: Producto) -> str:
        if p.stock == 0:              return "SIN STOCK"
        if p.stock <= p.stock_minimo: return "BAJO"
        if p.stock >= p.stock_maximo: return "EXCESO"
        return "NORMAL"


# clase: menu interactivo
class MenuAlmacen:

    def __init__(self):
        self.almacen = Almacen()

    def ejecutar(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        print(" sistema de inventario")

        while True:
            self._mostrar_menu()
            opcion = input("Opcion: ").strip()

            if   opcion == "1": self.almacen.mostrar_inventario()
            elif opcion == "2": self._flujo_agregar()
            elif opcion == "3": self._flujo_entrada()
            elif opcion == "4": self._flujo_salida()
            elif opcion == "5": self._flujo_optimo()
            elif opcion == "6": self.almacen.generar_alertas()
            elif opcion == "7": self.almacen.mostrar_historial()
            elif opcion == "0": print("\n  Sistema cerrado."); break
            else: print("  Opcion no valida.")

            input("\n  Presiona Enter para continuar...")
            os.system("cls" if os.name == "nt" else "clear")

    def _mostrar_menu(self) -> None:
        print("  1. Ver inventario")
        print("  2. Agregar producto")
        print("  3. Registrar entrada")
        print("  4. Registrar salida")
        print("  5. Calcular nivel optimo")
        print("  6. Generar alertas")
        print("  7. Ver historial")
        print("  0. Salir")

    def _flujo_agregar(self) -> None:
        print("\n  AGREGAR PRODUCTO")
        codigo = input("  Codigo: ").strip().upper()
        nombre = input("  Nombre: ").strip()
        stock  = self._pedir_entero("  Stock inicial: ", 0, 9999)
        smin   = self._pedir_entero("  Stock minimo : ", 0, 9999)
        smax   = self._pedir_entero("  Stock maximo : ", smin, 9999)
        self.almacen.agregar_producto(codigo, nombre, stock, smin, smax)

    def _flujo_entrada(self) -> None:
        print("\n  REGISTRAR ENTRADA")
        codigo   = input("  Codigo del producto: ").strip().upper()
        cantidad = self._pedir_entero("  Cantidad a ingresar: ", 1, 9999)
        motivo   = input("  Motivo (Enter = Reabastecimiento): ").strip()
        self.almacen.registrar_entrada(codigo, cantidad, motivo or "Reabastecimiento")

    def _flujo_salida(self) -> None:
        print("\n  REGISTRAR SALIDA")
        codigo   = input("  Codigo del producto: ").strip().upper()
        cantidad = self._pedir_entero("  Cantidad a retirar: ", 1, 9999)
        motivo   = input("  Motivo (Enter = Venta): ").strip()
        self.almacen.registrar_salida(codigo, cantidad, motivo or "Venta")

    def _flujo_optimo(self) -> None:
        print("\n  CALCULAR NIVEL OPTIMO")
        codigo = input("  Codigo del producto: ").strip().upper()
        self.almacen.calcular_nivel_optimo(codigo)

    def _pedir_entero(self, mensaje: str, minimo: int, maximo: int) -> int:
        while True:
            try:
                valor = int(input(mensaje))
                if minimo <= valor <= maximo:
                    return valor
                print(f"    Rango valido: {minimo} a {maximo}.")
            except ValueError:
                print("    Ingresa un numero entero.")


# entrada
if __name__ == "__main__":
    menu = MenuAlmacen()
    menu.ejecutar()