#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""@package Classes
Documentação para o módulo de classes.
"""

## Classe que define um nó do espaço de busca.
#
# Mais informações abaixo.
class Nodo:
    ## Construtor:
    # @brief Inicialização dos parâmetros associados aos nodos (estado, referência ao nodo pai e operador que o gerou).
    # @param estado Estado do nodo.
    # @param pai Referência ao nodo pai.
    # @param operador Operador que gerou o nodo.
    def __init__(self, estado, pai=None, operador=None):
        self.estado = estado
        self.pai = pai
        self.operador = operador

    ## @var self.estado
    # @brief Estado do nodo atual.

    ## @var self.pai
    # @brief Referência ao nodo que gerou o atual.

    ## @var self.operador
    # @brief Operador que gerou o nodo atual.

    ## Aplicar o operador <M,C>, onde 0 < (M + C) < TAM_BARCO.
    # M: representa o número de missionários a serem transportados no barco.
    # C: representa o número de canibais a serem transportados no barco.
    # @param self Referência ao nodo.
    # @param operador Operador que produz novo nodo.
    # @param possiveisOperadores Lista de operadores que podem ser utilizados na função sucessor.
    # @return Retorna nodo gerado a partir de um operador.
    def funcSucessor(self, operador, possiveisOperadores):
        novoEstado = self.transportar(self.estado, operador)
        novoNodo = Nodo(novoEstado, self, operador)

        return novoNodo

    ## Gerar nodos filhos de um determinado nodo com uso da função sucessor.
    # @param self Referência ao nodo.
    # @return Retorna todos nodos com estados gerados a partir dos possíveis operadores.
    def gerarEstados(self):
        possiveisOperadores = self.definirOpValidos(self.estado)

        return [self.funcSucessor(operadorAtual, possiveisOperadores)
                for operadorAtual in possiveisOperadores]

    ## Mostrar operadores que realizaram o objetivo.
    # @param self Referência ao nodo.
    # @return Retorna a sequência de operadores usados para atingir o estado objetivo.
    def mostrarPlanoResultante(self):
        return [node.operador for node in self.caminho()[1:]]

    ## Lista de referências ao caminho que levou ao objetivo.
    # @param self Referência ao nodo.
    # @return Retorna a lista de referências de trás pra frente (dos estados objetivo ao inicial).
    def caminho(self):
        nodo, caminho_de_nodos = self, []
        while nodo:
            caminho_de_nodos.append(nodo)
            nodo = nodo.pai
        return list(reversed(caminho_de_nodos))

    ## Método que verifica se o estado atual é o estado objetivo.
    # @param self Referência ao nodo.
    # @param estado Estado a ser comparado com estado objetivo.
    # @param sObjetivo Estado referência (objetivo).
    # @return Retorna 'True' se e somente se, todos os itens da tupla 'estado' forem iguais ao da tupla 'sObjetivo'.
    def testeDeObjetivo(self, estado, sObjetivo):
        if all(itemDoEstadoAtual == itemDoEstadoObjetivo for (itemDoEstadoAtual, itemDoEstadoObjetivo) in zip(estado, sObjetivo)):
            return True
        else:
            return False

    ## Método que gera um estado com base em um operador. Isso simula um transporte de x missionários e y canibais para a outra margem.
    # @param self Referência ao nodo.
    # @param estado Estado de partida para realizar o transporte das pessoas.
    # @param opAtual Operador que define quantos missionários e quantos canibais serão levados no barco.
    # @return Retorna estado gerado a partir do transporte das pessoas.
    def transportar(self, estado, opAtual):
        margens = self.obterMargens(estado, opAtual)
        ME = margens[0]
        MD = margens[1]
        novaMargem = margens[2]

        novoEstado = (ME, MD, novaMargem)
        return novoEstado

    ## Método que verifica a quantia de pessoas em cada margem do rio.
    # @param self Referência ao nodo.
    # @param margens Configuração de cada margem, isto é, quantos missionários e canibais há em cada uma.
    # @return Retorna 'False' caso haja mais canibais que missionários em alguma das margens.
    # Retorna 'True' caso as margens sejam válidas.
    def verificarMargens(self, margens):
        me = margens[0]
        md = margens[1]

        missionariosNaDireita = md[0]
        canibaisNaDireita = md[1]

        missionariosNaEsquerda = me[0]
        canibaisNaEsquerda = me[1]

        if (missionariosNaDireita > 0):
            if (missionariosNaDireita < canibaisNaDireita):
                return False # INVÁLIDO!

        if (missionariosNaEsquerda > 0):
            if (missionariosNaEsquerda < canibaisNaEsquerda):
                return False # INVÁLIDO!

        return True # VÁLIDO!

    ## Método que seleciona apenas operadores válidos.
    # @param self Referência ao nodo.
    # @param estado Estado necessário para verificação de operadores válidos.
    # @return Retorna lista de possíveis operadores.
    def definirOpValidos(self, estado):
        margemAtual = (estado[2])

        if margemAtual == "MargemDireita":
            indiceMargem = 1
        else:
            indiceMargem = 0

        numMissionarios = estado[indiceMargem][0]
        numCanibais = estado[indiceMargem][1]

        operadores = self.opIniciais()
        possiveisOperadores = self.testarTransporte(operadores, numMissionarios, numCanibais)

        """ A segunda bateria de testes valida os operadores quanto a:
        - O uso deste operador gera uma margem onde numCanibais > numMissionarios ?
        - Se sim, este estado será descartado
        - Caso contrário, ele será um possível operador. """
        possiveisOperadores = self.testarOperadores(possiveisOperadores, estado)

        return possiveisOperadores

    ## Método que simula a ação de um operador, verificando se o seu uso gera numCanibais > numMissionarios em alguma das margens.
    # @param self Referência ao nodo.
    # @param operadores Lista de operadores a serem testados.
    # @param estado Estado Estado a ser testado.
    # @return Lista de operadores validados no primeiro teste.
    def testarOperadores(self, operadores, estado):
        for opAtual in operadores[:]:
            if (self.transporteGeraMaisCanibaisQueMissionarios(opAtual, estado) == True):
                operadores.remove(opAtual)

        return operadores

    ## Método especialista que avalia se o uso do operador causa a situação inválida: numCanibais > numMissionarios.
    # @param self Referência ao nodo.
    # @param opAtual Operador a ser testado.
    # @param estado Estado que contém as configurações das margens.
    # @return Retorna 'False' caso o uso do operador não causar a morte dos missionários (numCanibais > numMissionarios).
    # Retorna 'True' caso houver morte.
    def transporteGeraMaisCanibaisQueMissionarios(self, opAtual, estado):
        margens = self.obterMargens(estado, opAtual)

        if self.verificarMargens(margens) == True:
            return False
        else:
            return True

    ## Definição das configurações das margens a partir do uso de um operador.
    # @param self Referência ao nodo.
    # @param estado Estado que contém as configurações das margens.
    # @param opAtual Operador a ser testado.
    # @return Configurações das margens com o uso de opAtual.
    def obterMargens(self, estado, opAtual):
        configBarco = opAtual
        numMissionariosTransportados = configBarco[0]
        numCanibaisTransportados = configBarco[1]

        # Variáveis responsáveis pelo número de pessoas na margem esquerda
        missionariosNaMargemEsquerda = estado[0][0]
        canibaisNaMargemEsquerda = estado[0][1]

        # Variáveis responsáveis pelo número de pessoas na margem direita
        missionariosNaMargemDireita = estado[1][0]
        canibaisNaMargemDireita = estado[1][1]

        # Faz o transporte de fato (leva as pessoas e também alterna o lado do barco)
        if estado[2] == "MargemEsquerda":
            missionariosNaMargemEsquerda -= numMissionariosTransportados
            canibaisNaMargemEsquerda -= numCanibaisTransportados

            missionariosNaMargemDireita += numMissionariosTransportados
            canibaisNaMargemDireita += numCanibaisTransportados

            novaMargem = "MargemDireita"
        else:
            missionariosNaMargemEsquerda += numMissionariosTransportados
            canibaisNaMargemEsquerda += numCanibaisTransportados

            missionariosNaMargemDireita -= numMissionariosTransportados
            canibaisNaMargemDireita -= numCanibaisTransportados

            novaMargem = "MargemEsquerda"

        MD = [missionariosNaMargemDireita, canibaisNaMargemDireita]
        ME = [missionariosNaMargemEsquerda, canibaisNaMargemEsquerda]

        margens = (ME, MD, novaMargem)
        return margens

    ## Método que gera operadores iniciais com base no estado inicial.
    # @param self Referência ao nodo.
    # @return Lista que contém todos os operadores (válidos e inválidos), dados o número de pessoas e tamanho do barco.
    def opIniciais(self):
        operadores = []

        for numMissAtual in range(0, Busca.N_MISS+1):
            for  numCaniAtual in range(0, Busca.N_CAN+1):
                # Ignorar operadores
                numPessoasNoBarco = numMissAtual + numCaniAtual
                if (numPessoasNoBarco == 0):
                    break
                if (numPessoasNoBarco > Busca.TAM_BARCO):
                    break
                # Supondo que se: numMissAtual < numCaniAtual (tem mais canibais que missionários no barco) então isso será um estado inválido
                if (numMissAtual > 0) and (numCaniAtual > numMissAtual):
                    break

                else:
                    opAtual = (numMissAtual, numCaniAtual)
                    operadores.append(opAtual)

        for i in range (1, Busca.TAM_BARCO+1):
            opAtual = (0,i)
            operadores.append(opAtual)

        return operadores

    ## Método especialista em verificar se o transporte das pessoas é inválido, ou seja, transportar N+1 canibais de uma margem onde há apenas N canibais, por exemplo.
    # @param self Referência ao nodo.
    # @param operadores Lista de operadores a serem validados.
    # @param numMissAtual Indica o número de missionários na margem onde o barco se encontra.
    # @param numCaniAtual Indica o número de canibais na margem onde o barco se encontra.
    # @return Lista de operadores que foram validados neste teste.
    def testarTransporte(self, operadores, numMissAtual, numCaniAtual):
        for opAtual in operadores[:]:
            if (opAtual[0] > numMissAtual) or (opAtual[1] > numCaniAtual):
                operadores.remove(opAtual)

        return operadores

## Implementação de fila FIFO necessária para realizar busca em largura.
#
# Mais informações abaixo.
class FilaFIFO:
    ## Construtor:
    # @brief Inicialização das variáveis fila e referência ao início da fila.
    # @param self Referência à fila
    def __init__(self):
        self.fila = []
        self.inicio = 0

    ## @var self.fila
    # @brief Lista utilizada para implementar a fila.

    ## @var self.inicio
    # @brief Referência ao membro inicial da fila.

    ## Método responsável por adicionar à fila nodos filhos de um determinado nó.
    # @param self Referência à fila.
    # @param items Itens a serem incluídos na lista.
    def expandir(self, items):
        for item in items:
            print "Operador: " + str(item.operador) + " - " + "Estado: " + str(item.estado)
            self.append(item)

    ## Inclusão de itens individuais à fila.
    # @param self Referência à fila.
    # @param item Item a ser incluído na lista.
    def append(self, item):
        self.fila.append(item)

    ## Tirar item da fila. Como é FIFO, o primeiro a entrar sai primeiro.
    # @param self Referência à fila.
    def pop(self):
        itemRemover = self.fila[self.inicio]
        self.inicio += 1

        return itemRemover

## Classe que implementa busca em largura com uso de fila FIFO.
#
# Mais informações abaixo.
class Busca:
    ## Construtor:
    # @brief Inicialização das variáveis necessárias para a busca (estados inicial e final, fila FIFO e nodo inicial).
    # @param self Referência a busca
    def __init__(self):
        self.estadoInicial = self.setEstadoInicial()
        self.estadoObjetivo = self.setEstadoObjetivo()
        self.fila = FilaFIFO()
        self.nodoInicial = Nodo(self.estadoInicial)

    ## @var self.estadoInicial
    # @brief Configuração inicial do problema.

    ## @var self.estadoObjetivo
    # @brief Configuração objetivo do problema.

    ## @var self.fila
    # @brief Fila FIFO.

    ## @var self.nodoInicial
    # @brief Nodo inicial da busca.

    ## Número de missionários.
    # @brief É uma entrada do programa.
    N_MISS = 3

    ## Número de canibais.
    # @brief É uma entrada do programa.
    N_CAN = 3

    ## Quantas pessoas cabem no barco.
    # @brief É uma entrada do programa.
    TAM_BARCO = 2

    ## Margem inicial onde se encontra o barco.
    # @brief É uma entrada do programa.
    MARGEM_INICIAL = "Esquerda"

    @classmethod
    ## Definição do parâmetro 'MARGEM_INICIAL', responsável por definir onde se encontram os missionários, canibais e o barco.
    # @param cls Referência à classe Busca.
    def checkMargemInicial(cls):

        if "Esquerda" in Busca.MARGEM_INICIAL or "esquerda" in Busca.MARGEM_INICIAL:
            Busca.MARGEM_INICIAL = "MargemEsquerda"
        elif "Direita" in Busca.MARGEM_INICIAL or "direita" in Busca.MARGEM_INICIAL:
            Busca.MARGEM_INICIAL = "MargemDireita"
        else:
            print "A margem inicial inserida é inválida. Portanto, MargemEsquerda será assumida."
            Busca.MARGEM_INICIAL = "MargemEsquerda"

    @classmethod
    ## Definição da margem final com base na margem inicial.
    # @param cls Referência à classe Busca.
    # @return Retorna a margem do estado objetivo.
    def margemFinal(cls):
        if (Busca.MARGEM_INICIAL == "MargemEsquerda"):
            return "MargemDireita"
        else:
            return "MargemEsquerda"

    ## Definição do estado inicial, tendo como base a margem inicial.
    # @param self Referência à busca.
    # @return Retorna a configuração do estado inicial.
    def setEstadoInicial(self):
        Busca.checkMargemInicial()

        if Busca.MARGEM_INICIAL == "MargemEsquerda":
            return ([Busca.N_MISS, Busca.N_CAN], [0,0], Busca.MARGEM_INICIAL)
        else:
            return ([0,0], [Busca.N_MISS, Busca.N_CAN], Busca.MARGEM_INICIAL)

    ## Definição do estado objetivo, tendo como base a margem inicial.
    # @param self Referência ao objeto busca.
    # @return Retorna a configuração do estado objetivo.
    def setEstadoObjetivo(self):
        if Busca.MARGEM_INICIAL == "MargemEsquerda":
            return ([0,0], [Busca.N_MISS, Busca.N_CAN], "MargemDireita")
        else:
            return ([Busca.N_MISS, Busca.N_CAN], [0,0], "MargemEsquerda")

    ## Implementação da busca em largura.
    # @param self Referência ao objeto busca.
    def buscaEmLargura(self):
        # Define nodo inicial
        self.fila.append(self.nodoInicial)

        while self.fila:
            nodoAtual = self.fila.pop()

            # ~DEBUG
            print "\nEstado sendo visitado: "
            print nodoAtual.estado

            if nodoAtual.testeDeObjetivo(nodoAtual.estado, self.estadoObjetivo) == True:
                print "Estado final encontrado!"
                return nodoAtual

            else:
                print "Estados gerados: "
                self.fila.expandir(nodoAtual.gerarEstados())

        return None
