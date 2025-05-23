import time

class Historia:
    def __init__(self, jugador):
        self.jugador = jugador
        self.escenarios = []

    def agregar_escenario(self, escenario):
        self.escenarios.append(escenario)

    def narrar_transicion(self, lugar):
        transiciones = {
            "Bosque Encantado": [
                "🌲 Caminas entre árboles altos y retorcidos...",
                "🍃 Las hojas crujen bajo tus pasos mientras el sol se filtra débilmente...",
                "Llegas al Bosque Encantado."
            ],
            "Mina Abandonada": [
                "⛏️ Sigues un sendero olvidado que te lleva hacia unas ruinas oscuras...",
                "💨 El aire se vuelve más denso, y el eco de tus pasos resuena en las rocas...",
                "Has llegado a la entrada de la Mina Abandonada."
            ],
            "Aldea tranquila": [
                "🏘️ Las casas pequeñas aparecen a lo lejos mientras cruzas un campo dorado...",
                "👀 Los ojos curiosos de algunos aldeanos te siguen desde las ventanas...",
                "Ahora estás en la Aldea tranquila."
            ]
        }

        if lugar in transiciones:
            for linea in transiciones[lugar]:
                print(linea)
                time.sleep(2)
        else:
            print(f"Te diriges a {lugar}...")
            time.sleep(1.5)

    def comenzar(self):
        print("\n🌟 Comienza tu aventura, valiente.")
        time.sleep(2)
        for escenario in self.escenarios:
            self.narrar_transicion(escenario.nombre)
            time.sleep(1)
            escenario.mostrar_info(self.jugador)
            if escenario.opciones:
                resultado = escenario.tomar_decision()
                if resultado:
                    print(f"\n➡️ {resultado['consecuencia']}")
                    time.sleep(2)
                    accion = resultado.get("accion")
                    if accion:
                        accion()
                    print("\n...Continuando la aventura...\n")
                    time.sleep(1.5)

        print("\n🏁 Fin de tu historia. Misiones completadas:")
        for m in self.jugador.misiones:
            m.mostrar()