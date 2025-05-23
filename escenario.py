# Archivo: escenario.py

import time

class Escenario:
    def __init__(self, nombre, descripcion, opciones=None, npc=None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.opciones = opciones or {}
        self.npc = npc

    # El método mostrar_info ya no se usa en la GUI, se mantiene por si acaso
    def mostrar_info(self, jugador):
        print(f"\n📍 {self.nombre}\n{self.descripcion}")
        time.sleep(1)

        if self.npc:
            print(f"\n❗ Sientes una presencia cerca...\n")
            time.sleep(1)
            print(self.npc.introduccion)
            time.sleep(2)
          

        print("\n🔎 Opciones disponibles:")
        for clave, valor in self.opciones.items():
            print(f"- {clave}: {valor['descripcion']}")

    def tomar_decision(self, decision=None):
        """
        Toma una decisión en el escenario y devuelve la información de la consecuencia.
        """
        if decision is not None:
            if decision in self.opciones:
                return self.opciones[decision]
            else:
                return None
        else:
            # Modo consola: forzar decisión válida (no usado por la GUI)
            while True:
                decision = input("¿Qué quieres hacer?: ").strip().lower()
                if decision in self.opciones:
                    return self.opciones[decision]
                else:
                    print("❌ Opción inválida. Por favor elige una de las opciones disponibles.")
