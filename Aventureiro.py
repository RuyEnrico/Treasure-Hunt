import random


class Aventureiro:
    def __init__(self, nome):
        self.nome = nome
        self.forca = random.randint(10, 18)
        self.defesa = random.randint(10, 18)
        self.vida_maxima = random.randint(100, 120)
        self.vida_atual = self.vida_maxima
        self.mochila = []
        self.posicao = [0, 0]

    def atacar(self):
        return self.forca + random.randint(1, 6)

    def defender(self, dano):
        self.vida_atual -= max(0, dano - self.defesa)
        if self.vida_atual < 0:
            self.vida_atual = 0

    def mover(self, direcao):
        if direcao.lower() == "w" and self.posicao[0] > 0:
            self.posicao[0] -= 1
        elif direcao.lower() == "a" and self.posicao[1] > 0:
            self.posicao[1] -= 1
        elif direcao.lower() == "s" and self.posicao[0] < 9:
            self.posicao[0] += 1
        elif direcao.lower() == "d" and self.posicao[1] < 9:
            self.posicao[1] += 1
        else:
            return -1

    def coletar_item(self, item):
        self.mochila.append(item)

    def usar_item(self, item_escolhido):
        if item_escolhido.tipo == "Vida" and self.vida_atual == self.vida_maxima:
            print("Sua vida já está no máximo. Não é possível usar a poção de vida.")
            return

        if item_escolhido in self.mochila:
            if item_escolhido.tipo == "Vida":
                self.vida_atual += 20 * item_escolhido.intensidade
                if self.vida_atual > self.vida_maxima:
                    self.vida_atual = self.vida_maxima
            elif item_escolhido.tipo == "Força":
                self.forca += item_escolhido.intensidade
            elif item_escolhido.tipo == "Defesa":
                self.defesa += item_escolhido.intensidade

            self.mochila.remove(item_escolhido)
        else:
            print(f"Item {item_escolhido} não encontrado na mochila.")

    def ver_mochila(self):
        return [item for item in self.mochila]

    def esta_vivo(self):
        return self.vida_atual > 0
    
    def calcular_distancia(self, outra_posicao):
        return abs(self.posicao[0] - outra_posicao[0]) + abs(self.posicao[1] - outra_posicao[1])
