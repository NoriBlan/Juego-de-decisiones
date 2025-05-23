class Mision:
    def __init__(self, titulo, descripcion, completada=False):
        self.titulo = titulo
        self.descripcion = descripcion
        self.completada = completada

    def mostrar(self):
        """
        Retorna una cadena de texto formateada con el estado y los detalles de la misión.
        Esto es usado por la interfaz gráfica.
        """
        estado = "✅" if self.completada else "⏳"
        return f"{estado} {self.titulo}: {self.descripcion}" # Retorna la cadena en lugar de imprimirla

    def completar(self):
        """
        Marca la misión como completada.
        """
        self.completada = True
        pass
