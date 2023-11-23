class Item:
    def __init__(self, nome, tipo, intensidade):
        self.nome = nome
        self.tipo = tipo
        self.intensidade = intensidade

    def __str__(self):
        return f"{self.nome} - Intensidade: {self.intensidade}"