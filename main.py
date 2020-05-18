"""Módulo para o o cálculo do problema da mochila empregado Algoritmo Genético."""
from os import path
from time import time
import random
import csv
from copy import deepcopy


class Inventario():
    """Classe para ler arquivos do tipo CSV com o inventário/lista de itens disponíveis
    para combinar ao longo do problema da mochila."""

    def __init__(self, arquivo):
        """Método inicializador da classe.

        Parameters:
            arquivo(str): Nome do arquivo. Deve estar na mesma pasta do arquivo Python (*.py).

        """
        self.itens = arquivo

    @property
    def itens(self):
        """Método GET do campo que armazena os itens do inventário/lista.

        Returns:
            list(): Lista de itens dentro do inventário.

        """
        return self.__itens

    @itens.setter
    def itens(self, arquivo):
        """Método SET do campo que armazena os itens do inventário/lista.

        Parameters:
            arquivo(str): Nome do arquivo que possui a lista de itens a ser carregado neste campo.
                          Deve estar na mesma pasta do arquivo Python (*.py).

        """
        endereco = path.dirname(path.abspath(__file__))
        endereco_arquivo = path.join(endereco, arquivo)
        if arquivo is None:
            raise ValueError(
                "Arquivo com a descrição dos itens do inventário não informado!")
        itens = list()
        with open(endereco_arquivo, newline='') as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                [index, peso, valor] = row
                item = Item(index, peso, valor)
                itens.append(item)
        self.__itens = itens

    def __getitem__(self, index):
        return self.__itens[index]

    def __len__(self):
        return len(self.itens)

class Item():
    def __init__(self, index, peso, valor):
        self.index = int(index)
        self.peso = int(peso)
        self.valor = int(valor)

class Mochila():

    def __init__(self, composicao=None, nascimento=None):
        self.composicao = composicao
        self.fitness = None
        self.nascimento = nascimento

    @property
    def nascimento(self):
        return self.__nascimento

    @nascimento.setter
    def nascimento(self, nascimento):
        if nascimento is None:
            nascimento = 0
        self.__nascimento = nascimento

    @property
    def composicao(self):
        return self.__composicao

    @composicao.setter
    def composicao(self, composicao):
        # Valor semente para randômicos.
        random.seed(int(round(time() * 1000)))
        if composicao is None:
            composicao = [random.randint(0, 1)
                          for x in range(0, len(INVENTARIO))]
        self.__composicao = composicao
        fitness = self.__calcular_fitness()
        while fitness > (1+LIMIAR) * CAPACIDADE:
            elemento = random.randint(0, len(INVENTARIO)-1)
            composicao[elemento] = 0
            self.__composicao = composicao
            fitness = self.__calcular_fitness()

    @property
    def fitness(self):
        return self.__fitness

    @fitness.setter
    def fitness(self, valor=None):
        if valor is None:
            valor = self.__calcular_fitness()
        self.__fitness = valor

    def mutacionar(self):
        """
        Changes a random element of the permutation array from 0 -> 1 or from 1 -> 0.
        """
        # Valor semente para randômicos.
        random.seed(int(round(time() * 1000)))
        elemento = random.randint(0, len(self.composicao)-1)
        if self.__composicao[elemento] == 1:
            self.__composicao[elemento] = 0
        else:
            self.__composicao[elemento] = 1

    def __calcular_fitness(self):
        valor_total = 0
        peso_total = 0
        index = 0
        for i in self.__composicao:
            if index >= len(INVENTARIO):
                break
            if i == 1:
                valor_total += INVENTARIO[index].valor
                peso_total += INVENTARIO[index].peso
            index += 1
        return valor_total
        # Caso queira desconsiderar mochilas com peso superior à capacidade máxima,
        # inclua esta parte do código.
        # if peso_total > CAPACIDADE:
        #     return 0
        # else:
        #     return valor_total

    def __str__(self):
        return f"Fitness:{self.fitness}, Composição:{str(self.composicao)}"

    def __len__(self):
        return len(self.composicao)

    def __getitem__(self, index):
        return self.__composicao[index]

class Geracao():
    def __init__(self, evolucao=None, populacao=None):
        self.populacao = populacao
        self.evolucao = evolucao

    def __str__(self):
        return f"Geração {self.evolucao} com {len(self.populacao)} indivíduos."

    @property
    def evolucao(self):
        return self.__evolucao

    @evolucao.setter
    def evolucao(self, evolucao):
        if evolucao is None:
            evolucao = 0
        self.__evolucao = evolucao

    @property
    def populacao(self):
        return self.__populacao

    @populacao.setter
    def populacao(self, populacao):
        if populacao is None:
            populacao = [Mochila() for m in range(0, TAM_POP)]
        self.__populacao = sorted(
            populacao, key=lambda x: x.fitness, reverse=True)

    def evoluir(self):

        # Valor semente para randômicos.
        random.seed(int(round(time() * 1000)))

        tamanho_cruzamento = int(TAXA_REPRODUCAO*len(self.populacao))
        if tamanho_cruzamento % 2 > 0:
            tamanho_cruzamento += 1

        # Reprodução...
        ninhada = []
        elementos = deepcopy(self.populacao)
        while (len(ninhada)*2) < tamanho_cruzamento:
            # Seleção dos reprodutores pelo método da roleta.
            [gene1, elementos] = self.roleta(elementos)
            [gene2, elementos] = self.roleta(elementos)
            half = int(len(gene1)/2)
            # from start to half from father, from half to end from mother
            composicao = gene1[:half] + gene2[half:]
            resultado = type(gene1)(composicao=composicao,
                                    nascimento=(self.evolucao+1))

            if TAXA_MUTACAO > random.random():
                resultado.mutacionar()
            ninhada.append(resultado)

        nova_populacao = sorted(ninhada + self.populacao,
                                key=lambda x: x.fitness, reverse=True)
        geracao = Geracao(
            populacao=nova_populacao[:TAM_POP], evolucao=self.evolucao+1)
        return geracao

    def roleta(self, elementos):
        # Valor semente para randômicos.
        random.seed(int(round(time() * 1000)))
        abs_total = sum(m.fitness for m in elementos)
        perc_alvo = random.random()
        perc_atual = 0
        for elem in elementos:
            perc_atual += (elem.fitness/abs_total)
            if perc_atual > perc_alvo:
                elementos.remove(elem)
                return [elem, elementos]

# Capacidade da mochila, em kg.
CAPACIDADE = 120
# Limiar para primeira geração
LIMIAR = 0.05
# Tamanho máximo da população.
TAM_POP = 50
# Probabilidade de mutação.
TAXA_MUTACAO = 0.05
# Taxa de rerodução entre membro de uma geração.
TAXA_REPRODUCAO = 0.5
# Número máximo de gerações.
MAX_GERACOES = 500 * TAM_POP
# Leitura dos objetos que são possíveis colocar na mochila.
INVENTARIO = Inventario("dados.csv")

def main():
    # Instanciação do vetor repositório das gerações.
    geracoes = [None] * MAX_GERACOES
    # Criação da primeira geracao e população inicial.
    geracao = Geracao()
    # Atribui a primeira geração ao vetor de gerações como sendo a geração inicial.
    geracoes[geracao.evolucao] = geracao
    # Iteração até o número máximo de gerações.
    for geracao in geracoes:
        print(geracao)
        for mochila in geracao.populacao:
            print(mochila)
        # Evolui a geraçao (reprodução e mutação)
        geracao = geracao.evoluir()
        # Inclui a nova geração ao vetor de gerações.
        geracoes[geracao.evolucao] = geracao

if __name__ == "__main__":
    main()
