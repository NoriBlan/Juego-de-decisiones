import tkinter as tk
from tkinter import messagebox
import time

# Importaciones de los módulos del juego
from personaje import Personaje
from objeto_magico import ObjetoMagico
from mision import Mision
from npc import NPC
from escenario import Escenario
from historia import Historia
from enemigo import Enemigo

class InterfazJuego:
    """
    Clase principal para la interfaz gráfica del juego de aventura de texto.
    """
    def __init__(self, ventana_maestra):
        self.ventana_maestra = ventana_maestra
        ventana_maestra.title("Aventura de Texto")
        ventana_maestra.geometry("800x600")

        # Variables de estado del juego
        self.jugador = None
        self.historia = None
        self.indice_escenario_actual = 0
        self.linea_transicion_actual = 0
        self.enemigo_actual = None

        self.crear_widgets()
        self.mostrar_seleccion_personaje()

    def crear_widgets(self):
        self.area_texto = tk.Text(self.ventana_maestra, wrap="word", width=70, height=20, font=("Arial", 12))
        self.area_texto.pack(pady=10)
        self.area_texto.config(state="disabled")

        self.marco_info_combate = tk.Frame(self.ventana_maestra)
        self.etiqueta_salud_jugador = tk.Label(self.marco_info_combate, text="", font=("Arial", 10, "bold"), fg="blue")
        self.etiqueta_salud_jugador.pack(side=tk.LEFT, padx=10)
        self.etiqueta_salud_enemigo = tk.Label(self.marco_info_combate, text="", font=("Arial", 10, "bold"), fg="red")
        self.etiqueta_salud_enemigo.pack(side=tk.RIGHT, padx=10)

        self.marco_entrada = tk.Frame(self.ventana_maestra)
        self.marco_entrada.pack(pady=5)
        self.etiqueta_entrada = tk.Label(self.marco_entrada, text="", font=("Arial", 10))
        self.etiqueta_entrada.pack(side=tk.LEFT)
        self.campo_entrada = tk.Entry(self.marco_entrada, width=30, font=("Arial", 10))
        self.campo_entrada.pack(side=tk.LEFT, padx=5)
        self.boton_enviar = tk.Button(self.marco_entrada, text="Aceptar", command=self.procesar_entrada)
        self.boton_enviar.pack(side=tk.LEFT)

        self.marco_opciones = tk.Frame(self.ventana_maestra)
        self.marco_opciones.pack(pady=10)

    def limpiar_area_texto(self):
        self.area_texto.config(state="normal")
        self.area_texto.delete('1.0', tk.END)
        self.area_texto.config(state="disabled")

    def anadir_texto(self, texto):
        self.area_texto.config(state="normal")
        self.area_texto.insert(tk.END, texto + "\n")
        self.area_texto.see(tk.END)
        self.area_texto.config(state="disabled")

    def limpiar_opciones(self):
        for widget in self.marco_opciones.winfo_children():
            widget.destroy()

    def actualizar_info_combate(self):
        if self.jugador:
            self.etiqueta_salud_jugador.config(text=f"{self.jugador.nombre}: {self.jugador.salud} HP")
        if self.enemigo_actual:
            self.etiqueta_salud_enemigo.config(text=f"{self.enemigo_actual.nombre}: {self.enemigo_actual.salud} HP")

    def mostrar_seleccion_personaje(self):
        self.limpiar_area_texto()
        self.anadir_texto("👤 Elige tu clase:\n")
        clases = {
            "orco": {"salud": 140, "fuerza": 25}, "elfo": {"salud": 90, "fuerza": 18},
            "mago": {"salud": 80, "fuerza": 30}, "humano": {"salud": 110, "fuerza": 20},
            "enano": {"salud": 120, "fuerza": 22}
        }
        self.clases_personaje = clases
        for i, clase in enumerate(clases.keys(), 1):
            stats = clases[clase]
            self.anadir_texto(f"{i}. {clase.capitalize()} - Salud: {stats['salud']}, Fuerza: {stats['fuerza']}\n")
            boton = tk.Button(self.marco_opciones, text=f"{i}. {clase.capitalize()}", command=lambda c=clase: self.seleccionar_clase(c))
            boton.pack(side=tk.LEFT, padx=5)
        self.campo_entrada.pack_forget()
        self.boton_enviar.pack_forget()

    def seleccionar_clase(self, clase_elegida):
        self.limpiar_opciones()
        self.clase_elegida = clase_elegida
        self.limpiar_area_texto()
        self.anadir_texto(f"Has elegido ser un {clase_elegida.capitalize()}.\n")
        self.preguntar_genero()

    def preguntar_genero(self):
        self.limpiar_area_texto()
        self.anadir_texto("¿Eres hombre o mujer?\n")
        boton_hombre = tk.Button(self.marco_opciones, text="Hombre", command=lambda: self.establecer_genero("hombre"))
        boton_hombre.pack(side=tk.LEFT, padx=5)
        boton_mujer = tk.Button(self.marco_opciones, text="Mujer", command=lambda: self.establecer_genero("mujer"))
        boton_mujer.pack(side=tk.LEFT, padx=5)

    def establecer_genero(self, genero):
        self.limpiar_opciones()
        self.genero = genero.capitalize()
        self.limpiar_area_texto()
        self.anadir_texto(f"Has elegido ser {self.genero}.\n")
        self.preguntar_nombre()

    def preguntar_nombre(self):
        self.limpiar_area_texto()
        self.etiqueta_entrada.config(text="¿Cuál es tu nombre?:")
        self.campo_entrada.pack(side=tk.LEFT, padx=5)
        self.boton_enviar.pack(side=tk.LEFT)
        self.boton_enviar.config(command=self.crear_personaje)

    def crear_personaje(self):
        nombre = self.campo_entrada.get().strip()
        if not nombre:
            messagebox.showerror("Error", "Por favor, ingresa tu nombre.")
            return
        stats = self.clases_personaje[self.clase_elegida]
        self.jugador = Personaje(nombre, self.genero, self.clase_elegida, stats["salud"], stats["fuerza"])
        self.limpiar_area_texto()
        self.anadir_texto(f"\n¡Has elegido ser {self.jugador.nombre}, un(a) {self.jugador.raza.capitalize()} {self.jugador.genero}!\n")
        self.campo_entrada.pack_forget()
        self.etiqueta_entrada.pack_forget()
        self.boton_enviar.pack_forget()
        self.configurar_datos_juego()
        self.iniciar_aventura()

    def configurar_datos_juego(self):
        self.pocion = ObjetoMagico("Poción de Vida", "Cura 30 HP", "cura", 30)
        self.amuleto = ObjetoMagico("Amuleto de Poder", "Aumenta fuerza", "fuerza", 10)
        self.piedra_destino = ObjetoMagico("Piedra del Destino", "Objeto misterioso", "nulo", 0)
        self.espada_legendaria = ObjetoMagico("Espada Legendaria", "Gran daño", "fuerza", 50)
        self.armadura_dragon = ObjetoMagico("Armadura de Dragón", "Gran defensa", "salud", 70)

        self.mision_bosque = Mision("El secreto del bosque", "Explora la cabaña misteriosa.")
        self.mision_mina = Mision("Cristales perdidos", "Recupera el cristal de la mina maldita.")

        self.anciano = NPC("Anciano del Bosque", "Desde detrás de una raíz gigante cubierta de musgo...", "¿Tú... podrías ayudar a revelarlo?", self.mision_bosque)
        self.minero = NPC("Miner@ Fantasma", "Mientras exploras las ruinas de la mina...", "El cristal maldito en las profundidades debe ser recuperado...", self.mision_mina)

        self.goblin = Enemigo("Goblin", 40, 10, self.amuleto) 
        self.ogro = Enemigo("Ogro", 100, 20, self.armadura_dragon) 

        self.bosque = Escenario("Bosque Encantado", "Los árboles susurran y el ambiente es pesado.", {
            "explorar": {"descripcion": "Explorar la vieja cabaña.", "consecuencia": "Encuentras el mapa del bosque y un objeto mágico.", "accion": lambda: (self.jugador.agregar_objeto(self.piedra_destino), self.mision_bosque.completar())},
            "descansar": {"descripcion": "Descansar bajo un árbol.", "consecuencia": "Recuperas salud.", "accion": lambda: setattr(self.jugador, 'salud', self.jugador.salud + 10)},
            "cueva oscura": {
                "descripcion": "Adentrarse en una cueva oscura.", "consecuencia": "Un goblin te embosca!",
                # --- CAMBIO 1: AÑADIR MARCADOR ---
                "es_combate": True,
                "accion": lambda: self.iniciar_combate(self.goblin, accion_exito_combate=lambda: self.jugador.agregar_objeto(self.goblin.recompensa), accion_derrota_combate=lambda: self.anadir_texto("Te retiras de la cueva sin el amuleto."))
            },
            "usar piedra del destino": {"descripcion": "Usas la Piedra del Destino para revelar un camino oculto.", "consecuencia": "Descubres una biblioteca mágica escondida en el bosque.", "accion": lambda: self.anadir_texto("📘 Encuentras conocimientos olvidados. Sabiduría desbloqueada.")}
        }, npc=self.anciano)

        self.mina = Escenario("Mina Abandonada", "La oscuridad y el eco te envuelven.", {
            "buscar": {"descripcion": "Buscar el cristal maldito.", "consecuencia": "Encuentras el cristal y lo recuperas.", "accion": lambda: (self.jugador.agregar_objeto(self.pocion), self.mision_mina.completar())},
            "huir": {"descripcion": "Salir corriendo de la mina.", "consecuencia": "Escapas sano y salvo, pero sin el cristal.", "accion": lambda: self.anadir_texto("Decides que la aventura puede esperar.")},
            "enfrentar al ogro": {
                "descripcion": "Investigar un rugido profundo.", "consecuencia": "Un imponente ogro bloquea tu camino!",
                # --- CAMBIO 1: AÑADIR MARCADOR ---
                "es_combate": True,
                "accion": lambda: self.iniciar_combate(self.ogro, accion_exito_combate=lambda: self.jugador.agregar_objeto(self.ogro.recompensa), accion_derrota_combate=lambda: self.anadir_texto("No puedes obtener la armadura sin derrotar al ogro."))
            }
        }, npc=self.minero)

        self.aldea = Escenario("Aldea tranquila", "El pueblo parece pacífico, pero algo no está bien.", {
            "hablar": {"descripcion": "Hablar con los aldeanos.", "consecuencia": "Obtienes información sobre las misiones y el bosque.", "accion": lambda: self.anadir_texto("Los aldeanos te cuentan historias antiguas y consejos.")},
            "descansar": {"descripcion": "Descansar en la taberna.", "consecuencia": "Recuperas energías y salud.", "accion": lambda: setattr(self.jugador, 'salud', min(self.jugador.salud + 20, 100))}
        })

        self.historia = Historia(self.jugador)
        self.historia.agregar_escenario(self.bosque)
        self.historia.agregar_escenario(self.mina)
        self.historia.agregar_escenario(self.aldea)

    def iniciar_aventura(self):
        self.limpiar_area_texto()
        self.anadir_texto("\n🌟 Comienza tu aventura, valiente.\n")
        self.ventana_maestra.after(2000, self.mostrar_escenario_actual)

    def mostrar_escenario_actual(self):
        if self.indice_escenario_actual < len(self.historia.escenarios):
            escenario = self.historia.escenarios[self.indice_escenario_actual]
            self.linea_transicion_actual = 0
            self.narrar_transicion_paso_a_paso(escenario)
        else:
            self.finalizar_juego()

    def narrar_transicion_paso_a_paso(self, escenario):
        transiciones = {
            "Bosque Encantado": ["🌲 Caminas entre árboles altos y retorcidos...", "🍃 Las hojas crujen bajo tus pasos...", "Llegas al Bosque Encantado."],
            "Mina Abandonada": ["⛏️ Sigues un sendero olvidado...", "💨 El aire se vuelve más denso...", "Has llegado a la entrada de la Mina Abandonada."],
            "Aldea tranquila": ["🏘️ Las casas pequeñas aparecen a lo lejos...", "👀 Los ojos curiosos de algunos aldeanos te siguen...", "Ahora estás en la Aldea tranquila."]
        }
        lineas = transiciones.get(escenario.nombre, [f"Te diriges a {escenario.nombre}..."])
        if self.linea_transicion_actual == 0:
            self.limpiar_area_texto()
        if self.linea_transicion_actual < len(lineas):
            self.anadir_texto(lineas[self.linea_transicion_actual])
            self.linea_transicion_actual += 1
            self.ventana_maestra.after(2000, lambda: self.narrar_transicion_paso_a_paso(escenario))
        else:
            self.anadir_texto(f"\n📍 {escenario.nombre}\n{escenario.descripcion}\n")
            if escenario.npc:
                self.ventana_maestra.after(1500, lambda: self.manejar_interaccion_npc(escenario.npc, escenario))
            else:
                self.ventana_maestra.after(1500, lambda: self.mostrar_opciones_escenario(escenario))

    def manejar_interaccion_npc(self, npc, escenario):
        self.anadir_texto(f"\n❗ Sientes una presencia cerca...\n")
        self.ventana_maestra.after(1500, lambda: self.anadir_texto(npc.introduccion))
        self.ventana_maestra.after(3000, lambda: self.anadir_texto(f"\n¿Quieres hablar con {npc.nombre}?"))
        self.limpiar_opciones()
        self.ventana_maestra.after(3500, lambda: self._mostrar_botones_npc(npc, escenario))

    def _mostrar_botones_npc(self, npc, escenario):
        boton_si = tk.Button(self.marco_opciones, text="Sí", command=lambda: self.decision_interaccion_npc(npc, escenario, True))
        boton_si.pack(side=tk.LEFT, padx=5)
        boton_no = tk.Button(self.marco_opciones, text="No", command=lambda: self.decision_interaccion_npc(npc, escenario, False))
        boton_no.pack(side=tk.LEFT, padx=5)

    def decision_interaccion_npc(self, npc, escenario, decision):
        self.limpiar_opciones()
        self.limpiar_area_texto()
        if decision:
            self.anadir_texto(f"\n🧓 {npc.nombre} aparece...\n")
            self.ventana_maestra.after(1000, lambda: self.anadir_texto(npc.introduccion))
            self.ventana_maestra.after(2500, lambda: self.anadir_texto(f"\n{npc.nombre}: {npc.mensaje}\n"))
            self.ventana_maestra.after(4000, lambda: self.anadir_texto(f"\n{npc.nombre} te observa con atención, {self.jugador.nombre}.\n"))
            if npc.mision and not npc.mision.completada:
                self.ventana_maestra.after(5500, lambda: self.anadir_texto("¿Aceptar misión?"))
                self.ventana_maestra.after(6000, lambda: self._mostrar_botones_aceptar_mision(npc, escenario))
            else:
                self.ventana_maestra.after(5500, lambda: self.mostrar_opciones_escenario(escenario))
        else:
            self.anadir_texto(f"\nIgnoras a {npc.nombre} y sigues tu camino.\n")
            self.ventana_maestra.after(2000, lambda: self.mostrar_opciones_escenario(escenario))

    def _mostrar_botones_aceptar_mision(self, npc, escenario):
        boton_aceptar = tk.Button(self.marco_opciones, text="Sí", command=lambda: self.aceptar_mision(npc, escenario, True))
        boton_aceptar.pack(side=tk.LEFT, padx=5)
        boton_rechazar = tk.Button(self.marco_opciones, text="No", command=lambda: self.aceptar_mision(npc, escenario, False))
        boton_rechazar.pack(side=tk.LEFT, padx=5)

    def aceptar_mision(self, npc, escenario, decision):
        self.limpiar_opciones()
        self.limpiar_area_texto()
        if decision:
            self.jugador.misiones.append(npc.mision)
            self.anadir_texto(f"\n📜 Has aceptado la misión: {npc.mision.titulo}\n")
        else:
            self.anadir_texto(f"\n{npc.nombre} asiente lentamente y desaparece entre los árboles...\n")
        self.ventana_maestra.after(2000, lambda: self.mostrar_opciones_escenario(escenario))

    def mostrar_opciones_escenario(self, escenario):
        self.anadir_texto("\n🔎 Opciones disponibles:\n")
        self.limpiar_opciones()
        for clave, valor in escenario.opciones.items():
            self.anadir_texto(f"- {clave}: {valor['descripcion']}\n")
            boton = tk.Button(self.marco_opciones, text=clave.capitalize(), command=lambda c=clave: self.procesar_decision_escenario(escenario, c))
            boton.pack(side=tk.LEFT, padx=5)

    # --- CAMBIO 2: LÓGICA CORREGIDA ---
    def procesar_decision_escenario(self, escenario, clave_decision):
        self.limpiar_opciones()
        resultado_opcion = escenario.tomar_decision(clave_decision)

        if resultado_opcion:
            # Usamos el método .get() para buscar el marcador. Si no existe, devuelve False.
            es_combate = resultado_opcion.get("es_combate", False)
            accion = resultado_opcion.get("accion")

            if es_combate:
                # Si es un combate, muestra la consecuencia y luego llama a la acción (iniciar_combate)
                self.limpiar_area_texto()
                self.anadir_texto(f"\n➡️ {resultado_opcion['consecuencia']}\n")
                if accion:
                    self.ventana_maestra.after(1500, accion)
                # NO se avanza de escenario aquí. La lógica del combate se hará cargo.
            else:
                # Si NO es un combate, es una acción normal.
                self.limpiar_area_texto()
                self.anadir_texto(f"\n➡️ {resultado_opcion['consecuencia']}\n")
                if accion:
                    accion()
                
                # Ahora sí, se avanza de escenario de forma segura.
                self.anadir_texto("\n...Continuando la aventura...\n")
                self.indice_escenario_actual += 1
                self.ventana_maestra.after(2500, self.mostrar_escenario_actual)
        else:
            self.anadir_texto("❌ Opción inválida. Por favor elige una de las opciones disponibles.\n")
            self.ventana_maestra.after(1500, lambda: self.mostrar_opciones_escenario(escenario))

    def iniciar_combate(self, enemigo, accion_exito_combate=None, accion_derrota_combate=None):
        self.enemigo_actual = Enemigo(enemigo.nombre, enemigo.salud, enemigo.fuerza, enemigo.recompensa)
        self.accion_exito_combate = accion_exito_combate
        self.accion_derrota_combate = accion_derrota_combate
        self.limpiar_area_texto()
        self.limpiar_opciones()
        self.marco_info_combate.pack(pady=5)
        self.actualizar_info_combate()
        self.anadir_texto(f"¡Un {self.enemigo_actual.nombre} salvaje aparece!\n")
        self.ventana_maestra.after(1500, self.mostrar_opciones_combate)

    def mostrar_opciones_combate(self):
        self.limpiar_opciones()
        self.actualizar_info_combate()
        self.anadir_texto("\nElige tu acción:")
        boton_atacar = tk.Button(self.marco_opciones, text="Atacar", command=self.turno_combate)
        boton_atacar.pack(side=tk.LEFT, padx=5)
        boton_huir = tk.Button(self.marco_opciones, text="Huir", command=self.huir_combate)
        boton_huir.pack(side=tk.LEFT, padx=5)

    def turno_combate(self):
        if not self.enemigo_actual: return
        self.limpiar_opciones()
        self.limpiar_area_texto()
        self.anadir_texto(f"¡{self.jugador.nombre} ataca a {self.enemigo_actual.nombre}!")
        self.jugador.atacar(self.enemigo_actual)
        self.actualizar_info_combate()
        self.anadir_texto(f"El {self.enemigo_actual.nombre} ahora tiene {max(0, self.enemigo_actual.salud)} HP.\n")
        if self.enemigo_actual.esta_derrotado():
            self.ventana_maestra.after(1500, lambda: self.combate_terminado(True))
        else:
            self.ventana_maestra.after(2000, self.turno_enemigo)

    def turno_enemigo(self):
        if not self.enemigo_actual: return
        self.anadir_texto(f"¡El {self.enemigo_actual.nombre} te ataca!")
        self.enemigo_actual.atacar(self.jugador)
        self.actualizar_info_combate()
        self.anadir_texto(f"Tu salud actual: {max(0, self.jugador.salud)} HP.\n")
        if self.jugador.salud <= 0:
            self.ventana_maestra.after(1500, lambda: self.combate_terminado(False))
        else:
            self.ventana_maestra.after(2000, self.mostrar_opciones_combate)

    def huir_combate(self):
        self.marco_info_combate.pack_forget()
        self.limpiar_opciones()
        self.limpiar_area_texto()
        self.anadir_texto("Logras escapar del combate...\n")
        if self.accion_derrota_combate:
            self.accion_derrota_combate()
        self.ventana_maestra.after(2000, self.restaurar_estado_juego)

    def combate_terminado(self, victoria):
        self.marco_info_combate.pack_forget()
        self.limpiar_opciones()
        self.limpiar_area_texto()
        if victoria:
            self.anadir_texto(f"¡Has derrotado al {self.enemigo_actual.nombre}!\n")
            if self.enemigo_actual.recompensa and isinstance(self.enemigo_actual.recompensa, ObjetoMagico):
                self.jugador.agregar_objeto(self.enemigo_actual.recompensa)
                self.anadir_texto(f"Obtienes: ¡{self.enemigo_actual.recompensa.nombre}!\n")
            if self.accion_exito_combate: self.accion_exito_combate()
            self.enemigo_actual = None
            self.ventana_maestra.after(2500, self.restaurar_estado_juego)
        else:
            self.anadir_texto(f"¡Has sido derrotado por el {self.enemigo_actual.nombre}!\n")
            if self.accion_derrota_combate: self.accion_derrota_combate()
            messagebox.showinfo("Fin del Juego", "¡Has caído en combate! Fin de la aventura.")
            self.ventana_maestra.quit()

    def restaurar_estado_juego(self):
        if self.jugador.salud > 0:
            self.anadir_texto("\n...Continuando la aventura...\n")
            self.indice_escenario_actual += 1
            self.ventana_maestra.after(2000, self.mostrar_escenario_actual)
        else:
            self.finalizar_juego()

    def procesar_entrada(self): pass

    def finalizar_juego(self):
        self.limpiar_area_texto()
        self.anadir_texto("\n🏁 Fin de tu historia. Misiones completadas:\n")
        for mision in self.jugador.misiones:
            self.anadir_texto(mision.mostrar())
        self.limpiar_opciones()
        self.ventana_maestra.after(3000, lambda: messagebox.showinfo("Fin del Juego", "¡Gracias por jugar!"))
        self.ventana_maestra.after(3500, self.ventana_maestra.quit)

if __name__ == "__main__":
    raiz = tk.Tk()
    interfaz_juego = InterfazJuego(raiz)
    raiz.mainloop()