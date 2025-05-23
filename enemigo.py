import time

class Enemigo:
    def __init__(self, nombre, salud, fuerza, recompensa=None):
        self.nombre = nombre
        self.salud = salud
        self.fuerza = fuerza
        self.recompensa = recompensa # Objeto o mensaje de recompensa al ser derrotado

    def recibir_danio(self, cantidad):
        """
        Reduce la salud del enemigo al recibir daño.
        """
        self.salud -= cantidad
        # print(f"El {self.nombre} ha recibido {cantidad} de daño. Salud restante: {self.salud}")

    def atacar(self, objetivo):
        """
        El enemigo ataca a un objetivo (personaje).
        """
        # print(f"El {self.nombre} ataca a {objetivo.nombre}!")
        objetivo.recibir_danio(self.fuerza)

    def esta_derrotado(self):
        """
        Verifica si el enemigo ha sido derrotado.
        """
        return self.salud <= 0