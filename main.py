from random import randint, random
from math import ceil

TAMANHO_MAX = int(80)
melhor = [0,0,0,0,0,0,0]
countMelhor = 0

def main(): #{
    # Tabela usada na sala
    # Tabela onde cada coluna é: tamanho, valor, probabilidade e probabilidade acumulada
    tabela = [[10, 15, 0.2, 0.2], [40, 90, 0.2, 0.4], [20, 50, 0.2, 0.6], [32, 40, 0.2, 0.8], [8, 12, 0.2, 1.0]]
    newPop = gerarPop(5, tabela)

    # duas últimas colunas são tamanho e por último valor/fitness
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
    fitness = 0
    for i in range(0,5):
        if int(individuo[i]) == 1:
            fitness += int(tabela[i][1])
    return fitness
#}

def separaGrupos(populacao, tabela): #{
    individuos = populacao
    individuos.sort(key=keyValor1, reverse=True)

    global countMelhor
    countMelhor += 1
    print(f' count melhor1: {countMelhor}')
    if melhor[6] < individuos[0][6]:
        melhor.clear()
        melhor.append(individuos[0])
        print(f'melhor: {melhor}')
        countMelhor = 0


    meio = ceil(len(populacao)/2)
    chancePai = random()*100
    chanceMae = random()*100
    totalPai = 0
    totalMae = 0
    probPais = []
    probMaes = []

    for i in range(0, len(individuos)):
        if (i < meio):
            totalPai += individuos[i][6]
        else:
            totalMae += individuos[i][6]

    for i in range(0, len(individuos)):
        prob = 0
        probInd = []
        if (i < meio):
            prob = individuos[i][6] * 100 / totalPai
            probInd.append(prob)
            probInd.append(i)
            probPais.append(probInd)
        else:
            prob = individuos[i][6] * 100 / totalMae
            probInd.append(prob)
            probInd.append(i)
            probMaes.append(probInd)
    probPais.sort(key=keyValor2, reverse=True)
    probMaes.sort(key=keyValor2, reverse=True)

    ##########################################################################################
    ## SÓ PRA TESTAR, APAGAR ISSO DEPOIS #####################################################
    ##########################################################################################
    # duas últimas colunas são tamanho e por último valor
    print('ordenado:')
    for i in range(0, (len(individuos))):
        print(f'{individuos[i][0:5]}\ttamanho: {individuos[i][5]}\tvalor: {individuos[i][6]}')
    print('probPais:')
    for i in range(0, len(probPais)):
        print(probPais[i])
    print('probMaes:')
    for i in range(0, len(probMaes)):
        print(probMaes[i])
    ##########################################################################################
    # Pai = individuos[probPais[0][1]]
    # mae = individuos[probMaes[0][1]]

    # Agora dá pra saber quem são o posicaoPai e a mãe, tem que fazer o cruzamento

    for i in range(0,len(probPais)):
        if (i == 0):
            posicaoPai = probPais[i]
        else:
            if(chancePai < probPais[i][0]) and (probPais[i][0] > posicaoPai[0]):
                posicaoPai = probPais[i]
    for i in range(0,len(probMaes)):
        if (i == 0):
            posicaoMae = probMaes[i]
        else:
            if(chanceMae < probMaes[i][0]) and (probMaes[i][0] > posicaoMae[0]):
                posicaoMae = probMaes[i]

    print(f'posição pai: {posicaoPai[1]}')
    print(f'posição individuos em posição pais: {individuos[posicaoPai[1]]}')

    # chamar função de cruzamento
    cruzamento(individuos, posicaoPai, posicaoMae, tabela)
    populacao = individuos

    ##########################################################################################
    ## SÓ PRA TESTAR, APAGAR ISSO DEPOIS #####################################################
    ##########################################################################################
    # duas últimas colunas são tamanho e por último valor
    print('pós cruzamento (incompleta a função ainda):')
    for i in range(0, (len(individuos))):
        print(f'{individuos[i][0:5]}\ttamanho: {individuos[i][5]}\tvalor: {individuos[i][6]}')
    ##########################################################################################
#}

def cruzamento(individuos, posicaoPai, posicaoMae, tabela): #{
    pai = individuos[posicaoPai[1]]
    mae = individuos[posicaoMae[1]]
    pai.pop(6)
    pai.pop(5)
    print(f'pai antes: {pai}')

    global countMelhor
    countMelhor += 10
    print(f'countMelhor em cruzamento: {countMelhor}')

    individuos.pop(posicaoMae[1])
    individuos.pop(posicaoPai[1])
    sussa = False
    while sussa != True:
        filho1 = pai
        filho2 = mae
        cromMudar = randint(1,4) # porque se for o 0 ninguém muda e se for 5 muda tudo dos dois, ou seja, ninguém muda
        for i in range(0,cromMudar):
            aux = filho1[i]
            filho1[i] = filho2[i]
            filho2[i] = aux
        if (verificarTamanho(filho1, tabela) < TAMANHO_MAX) and (verificarTamanho(filho2, tabela) < TAMANHO_MAX):
            if (verificarTamanho(filho1, tabela) > 0) and (verificarTamanho(filho2,tabela) > 0):
                chanceMutar1 = random()
                chanceMutar2 = random()
                if chanceMutar1 <= 0.05:
                    # mutação filho1
                    print()
                if chanceMutar2 <= 0.05:
                    # mutação filho2
                    print()
                filho1.append(verificarTamanho(filho1, tabela))
                filho1.append(verificarFitness(filho1, tabela))
                filho2.append(verificarTamanho(filho2, tabela))
                filho2.append(verificarFitness(filho2, tabela))
                sussa = True
                print(f'filho com novo tamanho e novo fitness: {filho1}')

    individuos.append(filho1)
    individuos.append(filho2)
#}

def mutacao(filho): #{
    print()
#}

def keyValor1(objeto):
    #isso apenas precisa para fazer o sort, pois pega qual parte do objeto vai ser baseado o sort
    return objeto[6]

def keyValor2(objeto):
    #isso apenas precisa para fazer o sort, pois pega qual parte do objeto vai ser baseado o sort
    return objeto[0]

if(__name__ == "__main__"): #{
    main()
#}
