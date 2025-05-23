import time

class NPC:
    def __init__(self, nombre, introduccion, mensaje, mision=None):
        self.nombre = nombre
        self.introduccion = introduccion
        self.mensaje = mensaje
        self.mision = mision

    def interactuar(self, jugador):
        print(f"\n🧓 {self.nombre} aparece...\n")
        time.sleep(2)
        print(self.introduccion)
        time.sleep(2)
        print(f"\n{self.nombre}: {self.mensaje}")
        time.sleep(2)
        print(f"\n{self.nombre} te observa con atención, {jugador.nombre}.")
        time.sleep(1)

        if self.mision and not self.mision.completada:
            while True:
                decision = input("¿Aceptar misión? (sí/no): ").strip().lower()
                if decision == "sí":
                    jugador.misiones.append(self.mision)
                    print(f"\n📜 Has aceptado la misión: {self.mision.titulo}")
                    time.sleep(1.5)
                    break
                elif decision == "no":
                    print(f"\n{self.nombre} asiente lentamente y desaparece entre los árboles...")
                    time.sleep(2)
                    break
                else:
                    print("Por favor, responde con 'sí' o 'no'.")