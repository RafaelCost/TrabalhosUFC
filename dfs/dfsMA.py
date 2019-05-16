import time
import numpy as np

def dfs(graph, state, maxVariables, e):
    stack = [e]
    time = 1
    lenGraph = len(graph)
    
    for l in range(lenGraph):
        
        if state[l][0] == 0:
            while len(stack) > 0:
                n = stack.pop()
                if state[n][0] == 0:
                    state[n][1] = time
                    state[n][0] = 1
                    time += 1

                stack.append(n)
                contTotal = 0
                contNoWhite = 0
                
                for j in range(0,lenGraph):
                    if graph[n][j] == 1:
                        contTotal +=1
                        if state[j][0] == 0:
                            stack.append(j)
                            break 
                        else:
                            contNoWhite+=1
                            
                if contTotal == contNoWhite:
                    stack.pop()    
                    state[n][0] = 2
                    state[n][2] = time
                    time+=1 
                
                
        if state[maxVariable[l][1]][0] != 2:
            stack.append(maxVariable[l][1])

    return state   

name = ['\Grafo1_1000_12','\Grafo1_1000_31','\Grafo1_1000_59','\Grafo1_1000_83',
        '\Grafo2_2000_12','\Grafo2_2000_31','\Grafo2_2000_59','\Grafo2_2000_83',
        '\Grafo3_3000_12','\Grafo3_3000_31','\Grafo3_3000_59','\Grafo3_3000_83',
        '\Grafo4_4000_12','\Grafo4_4000_31','\Grafo4_4000_59','\Grafo4_4000_83',
        '\Grafo5_5000_12','\Grafo5_5000_31','\Grafo5_5000_59','\Grafo5_5000_83',
        '\Grafo6_10000_12','\Grafo6_10000_31','\Grafo6_10000_59']

for y in name:
    print("")
    print("Inicializando o arquivo . . .")
    iniL = time.time()
    end = 'trabTestes'+y+'.txt'
    text = open(end,'r').readlines()
    length = int(text[0].split(' ')[0])
    text = text[2:]


    graph = []
    for p in range(length):
        graph.append(0)
        graph[p]=[]
        for i in range(length):
            graph[p].append(0)

    adjMatrix = graph

    
    maxVariable=[]
    for j in range(length):
        maxVariable.append(0)
        maxVariable[j] = []
        for i in range(2):
            maxVariable[j].append(0)

    def startAdj(x):
        for p in range(len(x)):
            pos = x[p].split(' ')
            
            if int(pos[0]) != int(pos[1]):
                adjMatrix[int(pos[0])][int(pos[1])] = 1
            maxVariable[int(pos[0])][0] += 1
            maxVariable[int(pos[1])][0] += 1     
            maxVariable[int(pos[0])][1] = int(pos[0])
            maxVariable[int(pos[1])][1] = int(pos[1]) 


    startAdj(text)
    maxVariable.sort(reverse=True)
    m =maxVariable[0][1]

    state=[]
    for j in range(length):
        state.append(0)
        state[j] = []
        for i in range(3):
            state[j].append(0)


    fimL = time.time()
    print("")
    print("Tempo de Leitura:", fimL-iniL)
    print("")
    print("Vertice Inicial:",m)
    print()
    print("Inicializando a busca no grafo "+y+' . . .')

    iniE = time.time()
    k = dfs(adjMatrix, state, maxVariable, m)
    fimE = time.time()

    print("")
    print("Busca finalizada no grafo "+y+' . . .')
    print("")
    print("Tempo da Busca no grafo "+y+': ',fimE-iniE)
    print()

    arq = open('resultados\Matriz de Adjacencia'+y+'.txt', 'w')
    arq.write("Tempo de Leitura: "+str(fimL-iniL))
    arq.writelines("\n")
    arq.writelines("\n")
    arq.writelines("Vertice Inicial: "+str(m))
    arq.writelines("\n")
    arq.writelines("\n")
    arq.writelines("Tempo da Busca: "+str(fimE-iniE))
    arq.writelines("\n")
    arq.writelines("\n")
    print("")
    print("")
  
    for p in range(len(k)):
        arq.writelines(str(p)+": ("+str(k[p][1])+"/"+str(k[p][2])+")")
        arq.writelines("\n")