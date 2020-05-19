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
    """Classe que representa cada item de uma mochila ou do inventário."""

    def __init__(self, index, peso, valor):
        """Método inicializador da classe.

        Parameters:
            index (int): Valor para indicar a referência do item.
            peso (int): Valor do peso do item.
            valor (int): Representaćão do valor monetário do item.
        """

        self.index = int(index)
        self.peso = int(peso)
        self.valor = int(valor)

class Mochila():
    """Classe que representa cada item de uma mochila ou do inventário."""

    def __init__(self, composicao=None, nascimento=None):
        """Método inicializador da classe.

        Parameters:
            composicao (list): Lista com a composicao de itens da mochila.
            nascimento (int): Referência para indicar em qual geracão a mochila foi criada.
        """
        self.nascimento = nascimento
        self.composicao = composicao
        self.fitness = None
        self.peso = None

    @property
    def nascimento(self):
        """Método tipo GET do parâmetro nascimento.

        Returns:
            int: Referência para indicar em qual geracão a mochila foi criada.
        """

        return self.__nascimento

    @nascimento.setter
    def nascimento(self, nascimento):
        """Método tipo SET do parâmetro nascimento.

        Parameters:
            nascimento (int): Referência para indicar em qual geracão a mochila foi criada.
        """
        if nascimento is None:
            nascimento = 0
        self.__nascimento = nascimento

    @property
    def composicao(self):
        """Método tipo GET do parâmetro composićão.

        Returns:
            list: Lista com a composicao de itens da mochila.
        """
        return self.__composicao

    @composicao.setter
    def composicao(self, composicao):
        """Método tipo SET do parâmetro composićão.

        Parameters:
            composicao (list): Lista com a composicao de itens da mochila.
        """
        if composicao is None:
            # Valor semente para randômicos.
            random.seed(int(round(time() * 1000)))
            composicao = [random.randint(0, 1) for x in range(0, len(INVENTARIO))]
        self.__composicao = composicao

    @property
    def fitness(self):
        """Método tipo GET do parâmetro fitness.

        Returns:
            double: Valor com a indicacão do valor de fitness da Mochila.
        """

        return self.__fitness

    @fitness.setter
    def fitness(self, fitness=None):
        """Método tipo SET do parâmetro fitness.

        Parameters:
            fitness (double): Valor com a indicacão do valor de fitness da Mochila.
        """

        if fitness is None:
            fitness = self.__calcular_fitness()
        self.__fitness = fitness

    @property
    def peso(self):
        """Método tipo GET do parâmetro peso.

        Returns:
            double: Valor com a indicacão do valor de peso da Mochila.
        """

        return self.__peso

    @peso.setter
    def peso(self, peso=None):
        """Método tipo SET do parâmetro peso.

        Parameters:
            valor (double): Valor com a indicacão do valor depeso da Mochila.
        """

        if peso is None:
            peso = self.__calcular_peso()
        self.__peso = peso

    def mutacionar(self):
        """Método que muda o valor de um elemento aleatório de 0 para 1 ou vice-versa."""

        # Valor semente para randômicos.
        random.seed(int(round(time() * 1000)))
        elemento = random.randint(0, len(self.composicao)-1)
        if self.__composicao[elemento] == 1:
            self.__composicao[elemento] = 0
        else:
            self.__composicao[elemento] = 1

    def __calcular_fitness(self):
        valor_total = 0
        for i in range(len(self.__composicao)):
            valor_total += INVENTARIO[i].valor * self.composicao[i]
        return valor_total

    def __calcular_peso(self):
        peso_total = 0
        for i in range(len(self.__composicao)):
            peso_total += INVENTARIO[i].peso * self.composicao[i]
        return peso_total

    def __str__(self):
        return f"Fitness:{self.fitness} Peso: {self.peso}, Composição:{str(self.composicao)}"

    def __len__(self):
        return len(self.composicao)

    def __getitem__(self, index):
        return self.__composicao[index]

    def reparar(self):
        """ Método para realizar a reparação do objeto caso este supere a capacidade máxima."""
        peso = self.peso
        while peso > CAPACIDADE:
            item_id = random.randint(0, len(INVENTARIO)-1)
            self.composicao[item_id] = 0
            peso = self.__calcular_peso()
        self.fitness = self.__calcular_fitness()
        self.peso = self.__calcular_peso()

    def penalizar(self):
        """ Método para realizar a penalização do objeto caso este supere a capacidade máxima."""
        if self.peso > CAPACIDADE:
            self.fitness = int((CAPACIDADE * self.fitness)/self.peso)

class Geracao():
    """ Classe que representa o objeto de uma geraćão inteira de elementos do tipo mochila."""

    def __init__(self, identificador=None, populacao=None):
        self.populacao = populacao
        self.identificador = identificador

    def __str__(self):
        return f"Geração {self.identificador} com {len(self.populacao)} indivíduos."

    @property
    def identificador(self):
        """Método tipo GET do parâmetro evolucão.

        Returns:
            int: Valor com a indicacão de qual número de evolucão esta geracão pertence.
        """
        return self.__evolucao

    @identificador.setter
    def identificador(self, evolucao):
        """Método tipo SET do parâmetro evolucão.

        Parameters:
            evolucao (int): Valor com a indicacão de qual número de evolucão esta geracão pertence.
        """
        if evolucao is None:
            evolucao = 0
        self.__evolucao = evolucao

    @property
    def populacao(self):
        """Método tipo GET do parâmetro populacão.

        Returns:
            list: Lista com os elementos que pertencem a esta geracão.
        """
        return self.__populacao

    @populacao.setter
    def populacao(self, populacao):
        """Método tipo SET do parâmetro populacão.

        Parameters:
            populacao (list): Lista com os elementos que pertencem a esta geracão.
        """
        if populacao is None:
            populacao = [Mochila() for m in range(0, NP)]
        self.__populacao = sorted(
            populacao, key=lambda x: x.fitness, reverse=True)

    def evoluir(self, metodo):
        """
        Método que realiza a evolucão dos elementos que compõe uma geracão.
        A evolucão é composta pela reproducão e mutacão de elementos.
        """

        # Valor semente para randômicos.
        random.seed(int(round(time() * 1000)))

        # Define o tamanho do cruzamento com base na probabilidade Crossover.
        tamanho_cruzamento = int(PC*len(self.populacao))
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
            # Primeira metada será do Gene1 e a outra metade do Gene2.
            composicao = gene1[:half] + gene2[half:]
            resultado = type(gene1)(composicao=composicao,
                                    nascimento=(self.identificador+1))
            # Mutacão...
            if PM > random.random():
                resultado.mutacionar()
            ninhada.append(resultado)


        nova_pop = ninhada + self.populacao
        # Cfe item 3.1.a, as etapas de reparação/penalização ocorrem após a geração dos
        # filhos e antes da seleção dos sobrevimentes para a próxima geração
        # Definir penalizacão ou reparacão.
        if metodo == "r":
            for elemento in nova_pop:
                elemento.reparar()
        elif metodo == "p":
            for elemento in nova_pop:
                elemento.penalizar()
        else:
            raise ValueError("Método para refinamento da próxima geração não definido.")

        nova_pop_ordenada = sorted(nova_pop, key=lambda x: x.fitness, reverse=True)
        nova_geracao = Geracao(populacao=nova_pop_ordenada[:NP], identificador=self.identificador+1)
        return nova_geracao

    def roleta(self, elementos):
        """ Método da roleta para uma série de elementos de uma geracão.

        Parameters:
            elementos (list): lista de elementos que serão sorteados pelo método da roleta.

        Returns:
            list: lista composta de elemento selecionado e lsita com o
                 resto dos elementos não selecionados.
        """
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

# Probabilidade de mutação.
PM = 0.05
# Probabilidade de Crossover/reprodução entre membros de uma geração.
PC = 0.5
# Tamanho máximo da população.
NP = 50
# Capacidade da mochila, em kg.
CAPACIDADE = 120
# Número máximo de gerações.
MAX_GERACOES = 500 * NP
# Leitura dos objetos que são possíveis colocar na mochila.
INVENTARIO = Inventario("dados.csv")

if __name__ == "__main__":
    # Instanciação do vetor repositório das gerações.
    geracoes = [None] * MAX_GERACOES
    # Criação da primeira geracao e população inicial.
    geracao = Geracao()
    # Atribui a primeira geração ao vetor de gerações como sendo a geração inicial.
    geracoes[geracao.identificador] = geracao
    # Iteração até o número máximo de gerações.
    for geracao in geracoes:
        print(geracao)
        for mochila in geracao.populacao:
            print(mochila)
        # Evolui a geraçao (reprodução e mutação)
        geracao = geracao.evoluir("p")
        # Inclui a nova geração ao vetor de gerações.
        geracoes[geracao.identificador] = geracao
