# Archivo: personaje.py

class Personaje:
    def __init__(self, nombre, genero, raza, salud, fuerza):
        self.nombre = nombre
        self.genero = genero
        self.raza = raza
        self.salud = salud
        self.fuerza = fuerza
        self.inventario = []
        self.misiones = []

    def hablar(self, mensaje):
        # Esta función puede que ya no sea usada por la GUI, pero se mantiene.
        # print(f"{self.nombre} dice: {mensaje}")
        pass

    def recibir_danio(self, cantidad):
        self.salud -= cantidad
        # Eliminar o comentar el print si la GUI lo va a manejar
        # print(f"{self.nombre} ha recibido {cantidad} de daño. Salud restante: {self.salud}")

    def atacar(self, enemigo):
        # Eliminar o comentar el print si la GUI lo va a manejar
        # print(f"{self.nombre} ataca a {enemigo.nombre}")
        enemigo.recibir_danio(self.fuerza)

    def usar_objeto(self, objeto):
        objeto.usar(self) # El uso del objeto ya podría imprimir su efecto si lo deseas

    def agregar_objeto(self, objeto):
        self.inventario.append(objeto)
        # Eliminar o comentar el print si la GUI lo va a manejar
        # print(f"{self.nombre} ha obtenido {objeto.nombre}")