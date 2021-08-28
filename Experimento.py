def le_grafo(path):
    conteudo = []
    grafo = []
    aux = []

    with open(path, 'r') as arquivo:
        for linha in arquivo.readlines():
            linha = linha.replace('\n', '')
            linha = linha.split(' ')
            for i in range(len(linha)):
                if '.' in linha[i]:
                    linha[i] = float(linha[i])
                else:
                    linha[i] = int(linha[i])
            conteudo.append(linha)

    n_vertices = int(conteudo[0][0])
    n_arestas = int(conteudo[0][1])

    conteudo.pop(0)

    grafo = conteudo[:]

    return n_vertices, n_arestas, grafo


''' Lista de Adjacências '''


# Salva apenas o nó, não a tupla (nó, peso)

def lista_adjacencia(n_vertices, n_arestas, grafo):
    lista_adj = []

    for no in range(n_vertices):
        lista_adj.append(list())

    for i in range(len(grafo)):
        no1 = int(grafo[i][0])
        no2 = int(grafo[i][1])
        peso = float(grafo[i][2])

        lista_adj[no1].append((no2, peso))
        lista_adj[no2].append((no1, peso))

    return lista_adj


def grafo_dic(grafo):
    dic = {}

    for i in range(len(grafo)):
        no1 = int(grafo[i][0])
        no2 = int(grafo[i][1])
        peso = float(grafo[i][2])

        dic[no1, no2] = peso
        dic[no2, no1] = peso

    return dic


def calc_custo(sol, dic):
    custo = 0

    custo += dic.get((sol[-1], sol[0]), 100000000)

    for i in range(len(sol) - 1):
        custo += dic.get((sol[i], sol[i + 1]), 100000000)

    return custo


def insere_fim_origem(sol):
    sol_aux = sol[:]
    sol_aux.append(sol[0])

    return sol_aux


def escreve_saida(custo, sol):
    with open('saida2.txt', 'a') as arquivo:
        arquivo.write(f'{custo}\n{sol}\n')
        arquivo.close()


def aleat(n_vertices, dic, tempo):
    import random
    import time

    t_inicio = time.time()
    t = 0

    sol = [x for x in range(n_vertices)]

    custo_ = float('inf')

    while t < tempo:

        random.shuffle(sol)
        custo = calc_custo(sol, dic)
        if custo < custo_:
            sol_ = sol[:]
            custo_ = custo

        t_final = time.time()
        t = t_final - t_inicio

    escreve_saida(custo_, insere_fim_origem(sol_))

    return custo_, insere_fim_origem(sol_)


def vizin(n_vertices, dic, lista_vizinhos, tempo):
    import random
    import time

    cont = 0

    t_inicio = time.time()
    t = 0
    sol = []
    sol_ = []
    custo_ = float('inf')

    while t < tempo:

        n_visitados = [x for x in range(n_vertices)]

        origem = random.randrange(0, n_vertices)
        sol.append(origem)
        n_visitados.remove(origem)
        vizinhos = lista_vizinhos[origem]

        while len(n_visitados) != 0:

            menor = float('inf')

            for i in range(len(vizinhos)):
                if vizinhos[i][1] < menor and vizinhos[i][0] in n_visitados:
                    menor = vizinhos[i][1]
                    vmp = vizinhos[i][0]

            sol.append(vmp)
            origem = vmp
            n_visitados.remove(vmp)

            vizinhos = lista_vizinhos[origem]

        custo = calc_custo(sol, dic)
        if custo < custo_:
            sol_ = sol.copy()
            custo_ = custo

        t_final = time.time()
        t = t_final - t_inicio

    escreve_saida(custo_, insere_fim_origem(sol_))

    return custo_, insere_fim_origem(sol_)


def two_opt(n_vertices, sol, dic, tempo):
    import time

    t_inicio = time.time()
    t = 0

    if len(sol) == n_vertices:
        sol = insere_fim_origem(sol)

    sol_ = sol[:]
    custo_ = calc_custo(sol[:len(sol) - 1], dic)

    while t < tempo:

        for i in range(1, len(sol) - 2):
            for j in range(i + 1, len(sol)):
                if j - i == 1:
                    continue
                sol_aux = sol.copy()
                sol[i:j] = sol[j - 1:i - 1:-1]
                custo = calc_custo(sol[:len(sol) - 1], dic)

                if custo < custo_:
                    custo_ = custo
                    sol_ = sol.copy()
                    sol_aux = sol_.copy()
                else:
                    sol = sol_aux.copy()

        t_final = time.time()
        t = t_final - t_inicio

    escreve_saida(custo_, sol_)

    return custo_, sol_


def resolve_pcv(dicionario, lista_vizinhos, tempo):
    import random

    # print(aleat(n_vertices, dicionario, tempo))
    print(vizin(n_vertices, dicionario, lista_vizinhos, tempo))
    sol = [x for x in range(n_vertices)]
    random.shuffle(sol)
    print(two_opt(n_vertices, sol, dicionario, tempo))


import random

files = ['teste.txt', 'a280.txt', 'ali535.txt', 'ch130.txt', 'fl1577.txt', 'gr666.txt']

for i in files:

    path = 'C:\\Users\\cesar\\PycharmProjects\\Aeds3\\' + i

    n_vertices, n_arestas, grafo = le_grafo(path)

    dicionario = grafo_dic(grafo)
    lista_vizinhos = lista_adjacencia(n_vertices, n_arestas, grafo)

    tempo = 60

    for _ in range(5):
        vizin(n_vertices, dicionario, lista_vizinhos, tempo)
        sol = [x for x in range(n_vertices)]
        random.shuffle(sol)
        two_opt(n_vertices, sol, dicionario, tempo)