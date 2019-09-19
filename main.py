from random import randint, random
from math import ceil

TAMANHO_MAX = int(80)
melhor = [0, 0, 0, 0, 0, 0, 0]
countMelhor = 0


def main():  # {
    # Tabela usada na sala
    # Tabela onde cada coluna é: tamanho, valor, probabilidade e probabilidade acumulada
    tabela = [[10, 15, 0.2, 0.2],
              [40, 90, 0.2, 0.4],
              [20, 50, 0.2, 0.6],
              [32, 40, 0.2, 0.8],
              [8, 12, 0.2, 1.0]]
    newPop = gerarPop(5, tabela)

    rodaAlgoritmoGenetico(newPop, tabela)
# }

def rodaAlgoritmoGenetico(populacao, tabela):  # {
    epoca = 0
    global countMelhor

    while (epoca < 100):
        individuos = separaGrupos(populacao, tabela)
        populacao = individuos
        epoca += 1
        if countMelhor > 15:
            break
    print('\n' * 50)
    print(f'quantas vezes o melhor não muda: {countMelhor}')
    print(f'qtd de epocas: {epoca}')
    print(f'Melhor resultado: {melhor}')
# }

def gerarPop(numInd, tabela):  # {
    newPop = []
    count = 0
    while count < numInd:
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
# }

def verificarTamanho(individuo, tabela):  # {
    tamanho = 0
    for i in range(0, 5):
        if individuo[i] == 1:
            tamanho += int(tabela[i][0])
    return tamanho
# }

def verificarFitness(individuo, tabela):  # {
    fitness = 0

    for i in range(0, 5):
        if individuo[i] == 1:
            fitness += int(tabela[i][1])
    return fitness
# }

def separaGrupos(populacao, tabela):  # {
    individuos = populacao

    individuos.sort(key=keyValor1, reverse=True)

    global melhor
    global countMelhor
    countMelhor += 1

    if individuos[0][6] > melhor[6]:
        melhor = individuos[0].copy()
        #print('melhor {}'.format(melhor[6]))
        countMelhor = 0

    meio = ceil(len(individuos) / 2)
    chancePai = random() * 100
    chanceMae = random() * 100
    totalPai = 0
    totalMae = 0
    probPais = []
    probMaes = []

    for i in range(0, len(individuos)):
        if (i < meio):
            # totalPai += individuos[i][6]
            totalPai = totalPai + verificarFitness(individuos[i], tabela)
        else:
            # totalMae += individuos[i][6]
            totalMae = totalMae + verificarFitness(individuos[i], tabela)

    for i in range(0, len(populacao)):
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

    for i in range(0, len(probPais)):
        if (i == 0):
            posicaoPai = probPais[i]
        else:
            if (chancePai < probPais[i][0]) and (probPais[i][0] > posicaoPai[0]):
                posicaoPai = probPais[i]
    for i in range(0, len(probMaes)):
        if (i == 0):
            posicaoMae = probMaes[i]
        else:
            if (chanceMae < probMaes[i][0]) and (probMaes[i][0] > posicaoMae[0]):
                posicaoMae = probMaes[i]

    individuos = cruzamento(individuos, posicaoPai, posicaoMae, tabela)
    return individuos
# }

def cruzamento(individuos, posicaoPai, posicaoMae, tabela):  # {
    pai = individuos[posicaoPai[1]]
    mae = individuos[posicaoMae[1]]
    pai.pop(6)
    mae.pop(6)
    pai.pop(5)
    mae.pop(5)

    global countMelhor

    individuos.pop(posicaoMae[1])
    individuos.pop(posicaoPai[1])

    sussa = False
    while sussa != True:
        filho1 = pai
        filho2 = mae
        cromMudar = randint(1, 4)  # porque se for o 0 ninguém muda e se for 5 muda tudo dos dois, ou seja, ninguém muda
        for i in range(0, cromMudar):
            aux = filho1[i]
            filho1[i] = filho2[i]
            filho2[i] = aux
        if (verificarTamanho(filho1, tabela) < TAMANHO_MAX) and (verificarTamanho(filho2, tabela) < TAMANHO_MAX):
            if (verificarTamanho(filho1, tabela) > 0) and (verificarTamanho(filho2, tabela) > 0):
                chanceMutar1 = random()
                chanceMutar2 = random()
                if chanceMutar1 <= 0.05:
                    filho1 = mutacao(filho1, tabela)
                if chanceMutar2 <= 0.05:
                    filho2 = mutacao(filho2, tabela)
                filho1.append(verificarTamanho(filho1, tabela))
                filho1.append(verificarFitness(filho1, tabela))
                filho2.append(verificarTamanho(filho2, tabela))
                filho2.append(verificarFitness(filho2, tabela))
                sussa = True

    individuos.append(filho1)
    individuos.append(filho2)

    return individuos


# }

def mutacao(filho, tabela):  # {
    tudoCerto = False
    while tudoCerto != True:
        individuo = filho
        cromMudar = randint(0, 4)
        if individuo[cromMudar] == 0:
            individuo[cromMudar] = 1
        else:
            individuo[cromMudar] = 0
        novoTamanho = verificarTamanho(filho, tabela)
        if (novoTamanho <= TAMANHO_MAX) and (novoTamanho != 0):
            tudoCerto = True
    return individuo
# }

def keyValor1(objeto):
    # isso apenas precisa para fazer o sort, pois pega qual parte do objeto vai ser baseado o sort
    return objeto[6]


def keyValor2(objeto):
    # isso apenas precisa para fazer o sort, pois pega qual parte do objeto vai ser baseado o sort
    return objeto[0]


if (__name__ == "__main__"):  # {
    main()
# }





