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
        
        pass

    def recibir_danio(self, cantidad):
        self.salud -= cantidad
       

    def atacar(self, enemigo):
       
        enemigo.recibir_danio(self.fuerza)

    def usar_objeto(self, objeto):
        objeto.usar(self) # El uso del objeto ya podría imprimir su efecto si lo deseas

    def agregar_objeto(self, objeto):
        self.inventario.append(objeto)
