import random


class Chefao:
    def __init__(self):
        self.forca = random.randint(22, 26)
        self.defesa = random.randint(1, 5)
        self.vida = random.randint(100, 130)
        
    def atacar(self):
        return self.forca

    def defender(self, dano):
        self.vida -= int(max(0, dano - self.defesa))
        if self.vida < 0:
            self.vida = 0

    # Quando o aventureiro derrota o chefao ele ganha uma recompensa de aumento de 25% de força
    def dar_recompensa(self, aventureiro):
        aventureiro.forca = int(aventureiro.forca * 1.25)

    def esta_vivo(self):
        return self.vida > 0

