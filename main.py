from random import randint
from math import ceil

TAMANHO_MAX = int(80)

def main(): #{
    # Tabela usada na sala
    # Tabela onde cada coluna é: tamanho, valor, probabilidade e probabilidade acumulada
    tabela = [[10, 15, 0.2, 0.2], [40, 90, 0.2, 0.4], [20, 50, 0.2, 0.6], [32, 40, 0.2, 0.8], [8, 12, 0.2, 1.0]]
    newPop = gerarPop(5, tabela)


    # duas últimas colunas são tamanho e por último valor
    for i in range(0,(len(newPop))):
        print(f'{newPop[i][0:5]}\ttamanho: {newPop[i][5]}\tvalor: {newPop[i][6]}')

    separaGrupos(newPop, tabela)
#}

def gerarPop(numInd, tabela):#{
    newPop = []
    count = 0
    while count < numInd:
        peso = 0
        newInd = []
        for c in range(0, 5):
            aux = randint(0, 1)
            newInd.append(aux)
        tamanho = verificarTamanho(newInd, tabela)
        valor = verificarFitness(newInd, tabela)
        newInd.append(tamanho)
        newInd.append(valor)
        if (tamanho <= TAMANHO_MAX) and (tamanho != 0):
            newPop.append(newInd)
            count += 1
    return newPop
#}

def verificarTamanho(individuo, tabela): #{
    tamanho = 0
    for i in range(0,5):
        if int(individuo[i]) == 1:
            tamanho += int(tabela[i][0])
    return tamanho
#}

def verificarFitness(individuo, tabela): #{
    tamanho = 0
    for i in range(0,5):
        if int(individuo[i]) == 1:
            tamanho += int(tabela[i][1])
    return tamanho
#}

def separaGrupos(populacao, tabela): #{
    individuos = populacao
    individuos.sort(key=keyValor, reverse=True)

    ##########################################################################################
    ## SÓ PRA TESTAR, APAGAR ISSO DEPOIS #####################################################
    ##########################################################################################
    print('pop sorted')
    for i in range(0,5):
        print(f'{individuos[i][0:5]}\ttamanho: {individuos[i][5]}\tvalor: {individuos[i][6]}')
    ##########################################################################################



#}

def keyValor(objeto):
    #isso apenas precisa para fazer o sort, pois pega qual parte do objeto vai ser baseado o sort
    return objeto[6]

if(__name__ == "__main__"): #{
    main()
#}
