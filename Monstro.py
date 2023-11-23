import random


class Monstro:
    def __init__(self):
        self.forca = random.randint(5, 25)
        self.defesa = random.randint(5, 10)
        self.vida = random.randint(10, 100)

    def atacar(self):
        return self.forca

    def defender(self, dano):
        self.vida -= max(0, dano - self.defesa)
        if self.vida < 0:
            self.vida = 0

    def esta_vivo(self):
        return self.vida > 0
