#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Classes import *

if __name__ == "__main__":
    # Definir número de missionários
    Busca.N_MISS = (int)(raw_input("Número de missionários: "))

    # Definir número de canibais.
    Busca.N_CAN = (int)(raw_input("Número de canibais: "))

    # Definir quantas pessoas cabem no barco.
    Busca.TAM_BARCO = (int)(raw_input("Tamanho do barco (em número de pessoas que podem ser carregadas por vez): "))

    # Definir margem inicial onde se encontra o barco.
    Busca.MARGEM_INICIAL = (raw_input("Margem inicial onde missionários, canibais e o barco se encontram (Esquerda ou Direita): "))

    busca = Busca()
    plano = busca.buscaEmLargura().mostrarPlanoResultante()

    print "Plano resultante (sequência de operadores para o resultado):"
    for operador in plano:
        print operador
