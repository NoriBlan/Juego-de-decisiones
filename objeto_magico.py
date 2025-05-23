class ObjetoMagico:
    def __init__(self, nombre, efecto, tipo, valor):
        self.nombre = nombre
        self.efecto = efecto
        self.tipo = tipo
        self.valor = valor

    def usar(self, personaje):
        if self.tipo == "cura":
            personaje.salud += self.valor
            print(f"{personaje.nombre} usó {self.nombre} y recupera {self.valor} de salud.")
        elif self.tipo == "fuerza":
            personaje.fuerza += self.valor
            print(f"{personaje.nombre} se siente más fuerte gracias a {self.nombre}! (+{self.valor} fuerza)")
        else:
            print(f"{self.nombre} no tiene un efecto claro...")