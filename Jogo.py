import random
import os
from Aventureiro import Aventureiro
from Tesouro import Tesouro
from Item import Item
from Monstro import Monstro
from Chefao import Chefao


def limpar_console():
    os.system('cls' if os.name == 'nt' else 'clear')


class Jogo:
    def __init__(self):
        self.aventureiro = Aventureiro(input("Digite o nome do aventureiro: "))
        self.tesouro = Tesouro(self.gerar_posicao_aleatoria())

    def gerar_posicao_aleatoria(self):
        posicao = [random.randint(0, 9), random.randint(0, 9)]
        # Fazendo a verificação para que a posição do tesouro não seja a mesma, inicialmente, do aventureiro
        while posicao == self.aventureiro.posicao:
            posicao = [random.randint(0, 9), random.randint(0, 9)]
        return posicao

    def iniciar_jogo(self):
        limpar_console()
        print("Bem-vindo à Caça ao Tesouro!")
        while self.aventureiro.esta_vivo():
            self.exibir_mapa()
            acao = input("\nEscolha sua ação (W, A, S, D, I, T, Q): ")
            self.realizar_acao(acao)

            if self.aventureiro.posicao == self.tesouro.posicao:

                print("Parabéns! Você encontrou o tesouro e venceu o jogo!")
                break

        print("Fim de jogo. Obrigado por jogar!")

    def exibir_mapa(self):
        print()
        for i in range(10):
            for j in range(10):
                if [i, j] == self.aventureiro.posicao:
                    print("@", end=" ")
                elif [i, j] == self.tesouro.posicao:
                    print("X", end=" ")
                else:
                    print("-", end=" ")
            print()

    def realizar_acao(self, acao):
        if acao.lower() in ["w", "a", "s", "d"]:
            movimento_valido = self.aventureiro.mover(acao)
            efeito = self.verificar_efeito_movimento()
            if movimento_valido != -1:
                print("\nVocê se moveu.")
                if efeito == "item":
                    self.encontrar_item()
                elif efeito == "monstro":
                    self.encontrar_monstro()
                elif efeito == "chefao":
                    self.encontrar_chefao()
            else:
                print("\nMovimento inválido!")
        elif acao.lower() == "i":
            escolha_item = None
            while escolha_item is None:
                self.mostrar_itens()
                escolha_item = input("Escolha o número do item que deseja usar (ou pressione Enter para voltar): ")
                if escolha_item:
                    try:
                        indice_item = int(escolha_item) - 1
                        if 0 <= indice_item < len(self.aventureiro.mochila):
                            item_escolhido = self.aventureiro.mochila[indice_item]
                            self.aventureiro.usar_item(item_escolhido)
                        else:
                            print("Por favor, insira um número novamente.")
                            escolha_item = None
                    except ValueError:
                        print("Por favor, insira um número válido.")
                        escolha_item = None
        elif acao.lower() == "t":
            self.mostrar_atributos()
        elif acao.lower() == "q":
            print("Você desistiu da busca pelo tesouro.")
            self.aventureiro.vida_atual = 0
        else:
            print("Por favor, insira um valor válido.")

    def verificar_efeito_movimento(self):
        chance = random.randint(1, 100)
        if chance <= 40:
            return "nada"
        elif 40 < chance <= 60:
            return "item"
        elif 60 < chance <= 100:
            chance_chefao = random.randint(1, 100)
            distancia_ao_tesouro = self.aventureiro.calcular_distancia(self.tesouro.posicao)
            if chance_chefao <= 80 and distancia_ao_tesouro <= 3:
                return "chefao"
            else:
                return "monstro"

    def encontrar_chefao(self):
        chefao = Chefao()
        print("\n| Combate com o Chefão |\n")
        print(f"Um chefão apareceu com Força: {chefao.forca}, Defesa: {chefao.defesa}, Vida: {chefao.vida}!")
        self.realizar_combate(chefao)
        if not chefao.esta_vivo():
            chefao.dar_recompensa(self.aventureiro)

    def encontrar_item(self):
        chance_item = random.randint(1, 100)

        if chance_item <= 10:
            nome_item = "Poção de força"
            intensidade = 1
        elif 10 < chance_item <= 15:
            nome_item = "Poção de força"
            intensidade = 2
        elif 15 < chance_item <= 65:
            nome_item = "Poção de vida"
            intensidade = 1
        elif 65 < chance_item <= 95:
            nome_item = "Poção de vida"
            intensidade = 2
        elif 95 < chance_item <= 100:
            nome_item = "Poção de defesa"
            intensidade = 1

        item = Item(nome_item, "Vida" if "vida" in nome_item.lower() else "Força" if "força" in nome_item.lower() else "Defesa", intensidade)
        self.aventureiro.coletar_item(item)
        print(f"Você encontrou um item! {nome_item} de intensidade {intensidade} foi adicionado à sua mochila!")

    def encontrar_monstro(self):
        monstro = Monstro()
        print("\n| Combate |\n")
        print(f"Um monstro apareceu com Força: {monstro.forca}, Defesa: {monstro.defesa}, Vida: {monstro.vida}!")
        self.realizar_combate(monstro)

    def realizar_combate(self, monstro):
        while self.aventureiro.esta_vivo() and monstro.esta_vivo():
            if self.aventureiro.esta_vivo():
                # Vez do aventureiro atacar
                dano_aventureiro = self.aventureiro.atacar()
                # Vez do monstro defender
                monstro.defender(dano_aventureiro)
                print(f"-> Você atacou o monstro causando {dano_aventureiro} de dano. Vida do monstro: {monstro.vida}")

            if monstro.esta_vivo():
                # Vez do monstro atacar
                dano_monstro = monstro.atacar()
                # Vez do aventureiro defender
                self.aventureiro.defender(dano_monstro)
                print(f"-> O monstro atacou você causando {dano_monstro} de dano. Sua vida: {self.aventureiro.vida_atual}")

        if not self.aventureiro.esta_vivo():
            print("\nVocê foi derrotado pelo monstro.")
        else:
            print("\nVocê derrotou o monstro!")

    def mostrar_itens(self):
        print("\n| Itens na mochila |")
        itens = self.aventureiro.ver_mochila()
        if itens:
            for i, item in enumerate(itens):
                print(f"{i + 1}. {item}")
        else:
            print("Sua mochila está vazia.")
        print()

    def mostrar_atributos(self):
        print(f"\nAtributos do aventureiro {self.aventureiro.nome}:")
        print(f"Força: {self.aventureiro.forca}")
        print(f"Defesa: {self.aventureiro.defesa}")
        print(f"Vida Atual: {self.aventureiro.vida_atual}")
        print(f"Vida Máxima: {self.aventureiro.vida_maxima}\n")


jogo = Jogo()
jogo.iniciar_jogo()
