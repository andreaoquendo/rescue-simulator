from cmath import exp
import os
from pickle import TRUE
from random import randint
from state import State

class SaviorPlan:
    def __init__(self, maxRows, maxColumns, goal, initialState, name = "none", mesh = "square"):
        """
        Define as variaveis necessárias para a utilização do random plan por um unico agente.
        """
        self.walls = []
        self.maxRows = maxRows
        self.maxColumns = maxColumns
        self.initialState = initialState
        self.currentState = initialState
        self.goalPos = goal
        self.actions = []
        self.movement = {}
        self.matrix = [[]]
        self.file = ''
        self.victims = {}
        self.nodes = []

        self.actionsDFS = {}
        self.result = {}
        self.untried = {}
        self.unbacktracked = {}
        self.unbackbacktracked = {}
        self.previousDirection = "nop"
        self.foi = False

    def setInformation(self, matrix, result):
        self.matrix = matrix
        self.result = result

    def createPlan(self, victimsPos):
        #Loop
            #Achar a vitima mais próxima
                #Verificar se dá tempo
                #Adicionar ela na lista (com o caminho até ela)
        self.goalPos = (victimsPos[1], victimsPos[2])
        print('VITIMA', (victimsPos[1], victimsPos[2]))
        self.nodes = []
        self.createNode((self.currentState.row, self.currentState.col), 0, (self.currentState.row, self.currentState.col), None)
        print('PRIMEIRO',self.nodes[0])
        self.pathList = self.findPath(self.nodes[0], (victimsPos[1],victimsPos[2])) #self.savingPath.append(data)
        path = self.createPath()
        print('CAMINHO', path)

        self.foi = True
        #self.savePath() #self.savingPath.append(data)            
        #chamar executePlan no agente    
        return path

    def executePlan(self):
        self.go() #execute path
        #self.saveVictim()

    def go(self):
        return

    def getClosestVictim(self):
        file = open(os.path.join(".", "vitimas_posicoes.txt"), "r")

        victimsPos = []
        for line in file:
            values = line.split(',')
            tup = (self.matrix[int(values[1])][int(values[2])],int(values[1]),int(values[2]))
            victimsPos.append(tup)
            
        victimsPos.sort()

        return victimsPos

    def createNode(self, posAtual, g, posVizinha, conexao):
        # Cria um node que guarda os valores da posição, G, H e a conexão
        posObjetivo = self.goalPos
        
        dif = (abs(posAtual[0] - posObjetivo[0]), abs(posAtual[1] - posObjetivo[1]))
        self.nodes.append((posAtual, self.getDistance(posAtual, posVizinha) + g, min(dif[0],dif[1])*1.5 + abs(dif[0] - dif[1]), conexao))

    def getDistance(self, posAtual, posVizinha):
        if posAtual == posVizinha: 
            return 0
        
        moveDirection = -1
        c = 0

        if posAtual[0] >= 0 and posAtual[1] >= 0:
            for i in range(0,8):
                if self.result[posAtual][i] != None:
                    redor = (self.result[posAtual][i].row, self.result[posAtual][i].col)
                    if redor == posVizinha:
                        moveDirection = i

        if moveDirection > 3:
            c = 1.5
        else:
            c = 1

        return c


    #retorna uma lista de nodes vizinhos
    def vizinhos(self, node):

        print('VIZINHOS DO',node[0])
        posAtual = node[0]
        g = node[1]
        vizinhos = []
        listaPos = []

        if posAtual[0] >= 0 and posAtual[1] >= 0:
            for i in range(0,8):
                if self.result[posAtual][i] != None:
                    redor = (self.result[posAtual][i].row, self.result[posAtual][i].col)
                    if redor != posAtual:
                        self.createNode(redor, g, posAtual, None)
                        listaPos.append(redor)

        for n in self.nodes:
            for pos in listaPos:
                if n[0] == pos:
                    vizinhos.append(n)

        return vizinhos

    #current é o node atual
    def findPath(self, start, goal):
        procurar = []
        procurar.append(start)
        processados = []

        while len(procurar) != 0:
            current = procurar[0]
            for node in procurar:
                if (node[1] + node[2]) < (current[1] + current[2]) or ((node[1] + node[2]) == (current[1] + current[2]) and node[2] < current[2]):
                    current = node

            print('ANTES', len(processados),len(procurar))
            processados.append(current)
            procurar.remove(current)
            print('DEPOIS', len(processados),len(procurar))

            if current[0] == goal:
                print('FOIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII')
                currentInPath = current
                path =[]
                while currentInPath != start:
                    path.append(currentInPath)
                    currentInPath = currentInPath[3]
                print(path)
                return path
            
            vizinhos = self.vizinhos(current)
            for vizinho in vizinhos:
                inProcessados = False
                inProcurar = False
                for procs in processados:
                    if vizinho[0] == procs[0] and vizinho[1] == procs[1]:
                        inProcessados = True

                if not inProcessados:
                    custoVizinho = current[1] + self.getDistance(current[0], vizinho[0])
                    for proc in procurar:
                        if vizinho[0] == proc[0] and vizinho[1] == proc[1]:
                            inProcurar = True
                    if not inProcurar or custoVizinho < vizinho[1]:
                        viz = list(vizinho)
                        viz[1] = custoVizinho
                        viz[3] = current
                        vizinho = tuple(viz)

                        if not inProcurar:
                            procurar.append(vizinho)  
                    

    def createPath(self):
        movePos = { 0 : "S" ,
                    1: "N" ,
                    2: "O" ,
                    3: "L",
                    4: "SO",
                    5: "SE",
                    6: "NO",
                    7: "NE"}
        path = []

        for node in self.pathList:
            current = node[0]
            next = node[3][0]
            #if current[0] >= 0 and current[1] >= 0:
            for i in range(0,8):
                if self.result[current][i] != None:
                    redor = (self.result[current][i].row, self.result[current][i].col)
                    if redor == next:
                        print('TRUE', redor, next)
                        path.append(movePos[i])

        return list(reversed(path))

    def updateCurrentState(self, state):
        """Faz o upload do current state dentro do plano.
        """
        self.currentState = state
    
    def getLowestCost(self, expected):
        possibilities = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]
        
        curr = (expected.row, expected.col)

        if curr not in self.result.keys():
            return 0, 0

        for i in range(0,8):
            if self.result[curr][i] != None:
                lowestPos = self.result[curr][i]
                moveDirection = possibilities[i]
                break

        for i in range(0,8):
            if not self.result[curr][i]:
                continue
            val = self.matrix[self.result[curr][i].row][self.result[curr][i].col]
            lowest = self.matrix[lowestPos.row][lowestPos.col]
            if self.result[curr][i] != self.currentState and val <= lowest:
                lowestPos = self.result[curr][i]
                moveDirection = possibilities[i]
        
        if moveDirection in ["NE", "NO", "SE", "SO"]:
            c = 1.5
        else:
            c = 1

        return c, lowest
    
    def isItTimeToGoBackHome(self, timeLeft, cost):
        """Retorna se é momento de fazer o caminho de volta:
        @param timeLeft
        """
        if cost == None:
            return False
        if self.matrix[self.currentState.row][self.currentState.col] + cost - timeLeft >= 0:
            return True
        return False

    def setVictimsFile(self, vitals):
        """ Adiciona vítima
        """    
        self.victims[vitals[0][0]] = self.currentState
        vitals[0] = [str(x) for x in vitals[0]]
        line = ','.join(vitals[0]) + '\n'
        self.file += line

    def saveVictimsFile(self):
        """ Salva o arquivo com os dados vitais de todas as vítimas
        """  
        arquivo = open(os.path.join(".", "vitimas_encontradas.txt"), "w")
        arquivo.writelines(self.file)
        arquivo.close()

        arquivo = open(os.path.join(".", "vitimas_posicoes.txt"), "w")
        f = [str(key) + ',' + str(val.row) + ',' + str(val.col) + '\n' for key, val in self.victims.items()]
        arquivo.writelines(f)
        arquivo.close()
    
    def letItDie(self, victimId):
        return victimId in self.victims.keys()

    #MUDAR, NÃO VAI MAIS SER RANDOM
    def moveToNextPosition(self):
        """ Sorteia uma direcao e calcula a posicao futura do agente 
        @return: tupla contendo a acao (direcao) e o estado futuro resultante da movimentacao """
        possibilities = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]
        movePos = { "N" : (-1, 0),
                    "S" : (1, 0),
                    "L" : (0, 1),
                    "O" : (0, -1),
                    "NE" : (-1, 1),
                    "NO" : (-1, -1),
                    "SE" : (1, 1),
                    "SO" : (1, -1)}

        acoes = []
        reservadas = []
        while True:
            rand = randint(0, 7)
            movDirection = possibilities[rand]
            if movDirection not in acoes:
                acoes.append(movDirection)
            print('OLHA AKI: ', acoes)
            print('OLHA AKI2: ', reservadas)

            f = self.isVisitado(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])
            p = self.isParede(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])
            if p == False:
                chances = randint(0, 100)
                if f == True:
                    if chances <= 10 or len(acoes) == 8:
                        state = State(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])
                        break
                    else:
                        reservadas.append(movDirection)
                else:
                    if chances <= 90 or len(acoes) == 8:
                        state = State(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])
                        break
                    else:
                        reservadas.append(movDirection)

            if len(acoes) == 8:
                if len(reservadas) == 0:
                    print('ESTOU PRESO')
                    return None
                else:
                    movDirection = reservadas.pop()
                    state = State(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])
                    break
            

        return movDirection, state

    def moveToNextPositionDFS(self):
        """ Sorteia uma direcao e calcula a posicao futura do agente 
        @return: tupla contendo a acao (direcao) e o estado futuro resultante da movimentacao """

        #Seta as primeiras variáveis
        possibilities = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]
        #Para que as primeiras ações a serem executadas sejam as de custo 1
        print('possibilities', possibilities)
        possibilities.reverse()
        

        movePos = { "N" : (-1, 0),
                    "S" : (1, 0),
                    "L" : (0, 1),
                    "O" : (0, -1),
                    "NE" : (-1, 1),
                    "NO" : (-1, -1),
                    "SE" : (1, 1),
                    "SO" : (1, -1)}
        
        oppositeDirection = { "N" : "S",
                    "S" : "N",
                    "L" :"O",
                    "O" : "L",
                    "NE" :"SO",
                    "NO" : "SE",
                    "SE" : "NO",
                    "SO" :"NE" }
        #Se é a primeira vez passando por aqui, ele recebe todas essas possíveis ações
        # Ele não tem nenhum resultado salvo
        # Todas as possibilidades estão como não tentadas
        # As ações que ele ainda não desfez está vazia, só deve ser preenchida ao entrar nela de alguma forma
        curr_pos = (self.currentState.row, self.currentState.col)
        if curr_pos not in self.untried.keys():
            self.result[curr_pos] = [None]*8
            self.untried[curr_pos] = possibilities
            self.unbacktracked[curr_pos] = []
            self.unbackbacktracked[curr_pos] = []

            if self.previousDirection !="nop":
                state = State(self.currentState.row - movePos[self.previousDirection][0], self.currentState.col - movePos[self.previousDirection][1])
                r_possibilities = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]
                self.result[curr_pos][r_possibilities.index(oppositeDirection[self.previousDirection])] = state

        # Partimos primeiro das opções não tentadas primeiro
        # Não esquecer de reservar o result depois
        # No unbacktracked ele precisa saber qual foi o previous state
        while len(self.untried[curr_pos]) > 0 :
            if self.previousDirection == "nop" or self.untried[curr_pos][-1] == oppositeDirection[self.previousDirection] or len(self.untried[curr_pos]) <= 1:
                movDirection = self.untried[curr_pos].pop()
            else:
                aux = self.untried[curr_pos].pop()
                movDirection = self.untried[curr_pos].pop()
                self.untried[curr_pos].append(aux)
                
            state = State(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])
            self.previousDirection = movDirection
            if(self.isParede(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])):
                r_possibilities = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]
                self.result[curr_pos][r_possibilities.index(movDirection)] = self.currentState
            elif self.isVisitado(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1]) and len(self.untried[curr_pos]) > 1 and movDirection in ["N", "S", "L", "O"]:
                r_possibilities = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]
                self.result[curr_pos][r_possibilities.index(movDirection)] = state  
                self.unbacktracked[curr_pos].append(movDirection)
            else: 
                return movDirection, state

        # No unbacktracked só queremos saber qual foi a ação que levou ela a fazer o que fez
        if len(self.unbacktracked[curr_pos]) > 0:
            
            movDirection = self.unbacktracked[curr_pos][0]
            self.unbackbacktracked[curr_pos].append(movDirection)
            self.unbacktracked[curr_pos].remove(self.unbacktracked[curr_pos][0])
        
            state = State(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])
            self.previousDirection = movDirection
            return movDirection, state
        
        if  len(self.unbackbacktracked[curr_pos]) > 0:
            movDirection = self.unbackbacktracked[curr_pos].pop()
            state = State(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])
            return movDirection, state


    def analyzePosition(self):
        """ Sorteia uma direcao e calcula a posicao futura do agente 
        @return: tupla contendo a acao (direcao) e o estado futuro resultante da movimentacao """

    

        #Seta as primeiras variáveis
        possibilities = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]
        #Para que as primeiras ações a serem executadas sejam as de custo 1
        possibilities.reverse()
    
        movePos = { "N" : (-1, 0),
                    "S" : (1, 0),
                    "L" : (0, 1),
                    "O" : (0, -1),
                    "NE" : (-1, 1),
                    "NO" : (-1, -1),
                    "SE" : (1, 1),
                    "SO" : (1, -1)}
        
        oppositeDirection = { "N" : "S",
                    "S" : "N",
                    "L" :"O",
                    "O" : "L",
                    "NE" :"SO",
                    "NO" : "SE",
                    "SE" : "NO",
                    "SO" :"NE" }
        #Se é a primeira vez passando por aqui, ele recebe todas essas possíveis ações
        # Ele não tem nenhum resultado salvo
        # Todas as possibilidades estão como não tentadas
        # As ações que ele ainda não desfez está vazia, só deve ser preenchida ao entrar nela de alguma forma
        curr_pos = (self.currentState.row, self.currentState.col)
        if curr_pos not in self.untried.keys():
            self.result[curr_pos] = [None]*8
            self.untried[curr_pos] = possibilities
            self.unbacktracked[curr_pos] = []
            self.unbackbacktracked[curr_pos] = []
            
            if self.previousDirection !="nop":
                state = State(self.currentState.row - movePos[self.previousDirection][0], self.currentState.col - movePos[self.previousDirection][1])
                r_possibilities = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]
                self.result[curr_pos][r_possibilities.index(oppositeDirection[self.previousDirection])] = state

    def setResultOfAction(self, previousState, previousAction):

        #Caso seja a primeira vez dele entrando aqui, não deve executar nada
        if previousAction == "nop":
            return

        possibilities = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]

        # O resultado da ação anterior me levou a esta 
        prev_pos = (previousState.row, previousState.col)
        curr_pos = (self.currentState.row, self.currentState.col)
        print('len self untried', len(self.untried[prev_pos]))
        self.result[prev_pos][possibilities.index(previousAction)] = self.currentState

        movePos = { "N" : (-1, 0),
                    "S" : (1, 0),
                    "L" : (0, 1),
                    "O" : (0, -1),
                    "NE" : (-1, 1),
                    "NO" : (-1, -1),
                    "SE" : (1, 1),
                    "SO" : (1, -1)}

        oppositeDirection = { "N" : "S",
                    "S" : "N",
                    "L" :"O",
                    "O" : "L",
                    "NE" :"SO",
                    "NO" : "SE",
                    "SE" : "NO",
                    "SO" :"NE" }

        # Queremos colocar o caminho de volta da ação anterior
        if previousState != self.currentState:
            print('prevAction', previousAction,  sep=' ', )
            print( 'opposite', oppositeDirection[previousAction])
            if previousAction not in self.unbacktracked[prev_pos]:
                self.unbacktracked[prev_pos].append(previousAction)
        
        if self.matrix[prev_pos[0] + movePos["NO"][0]][prev_pos[1]+ movePos["NO"][1]] and self.result[prev_pos][possibilities.index("N")] != None and self.result[prev_pos][possibilities.index("O")] != None:
            if "NO" in self.untried[prev_pos]:
                self.untried[prev_pos].remove("NO")
        if self.matrix[prev_pos[0] + movePos["NE"][0]][prev_pos[1]+ movePos["NE"][1]] and self.result[prev_pos][possibilities.index("N")] != None and self.result[prev_pos][possibilities.index("L")] != None:
            if "NE" in self.untried[prev_pos]:
                self.untried[prev_pos].remove("NE")
        if self.matrix[prev_pos[0] + movePos["SO"][0]][prev_pos[1]+ movePos["SO"][1]] and self.result[prev_pos][possibilities.index("S")] != None and self.result[prev_pos][possibilities.index("O")] != None:
            if "SO" in self.untried[prev_pos]:
                self.untried[prev_pos].remove("SO")
        if self.matrix[prev_pos[0] + movePos["SE"][0]][prev_pos[1]+ movePos["SE"][1]] and self.result[prev_pos][possibilities.index("S")] != None and self.result[prev_pos][possibilities.index("L")] != None:
            if "SE" in self.untried[prev_pos]:
                self.untried[prev_pos].remove("SE")

    def isParede(self, row, col):
        if (row, col) in self.walls:
            return True
        return False
    
    def isVisitado(self, row, col):
        if self.matrix[row][col] != None:
            return True
        return False

    #SÓ RETORNA QUANDO FAZ O MOVIMENTO, MAS TEM Q CONTAR MSM Q NÃO CONSEGUIR
    def chooseAction(self):
        """ Escolhe o proximo movimento de forma aleatoria. 
        Eh a acao que vai ser executada pelo agente. 
        @return: tupla contendo a acao (direcao) e uma instância da classe State que representa a posição esperada após a execução
        """

        ## Tenta encontrar um movimento possivel dentro do tabuleiro 
        result = self.moveToNextPositionDFS()

        return result

    def chooseReturnAction(self):
        movePos = { (-1, 0): "N" ,
                    (1, 0): "S" ,
                    (0, 1): "L" ,
                    (0, -1): "O",
                    (-1, 1): "NE",
                    (-1, -1): "NO",
                    (1, 1): "SE",
                    (1, -1): "SO"}
        
        pos = self.getLowestDirection()
        action = movePos[pos]
        state = State(self.currentState.row + pos[0], self.currentState.col + pos[1])
        return action, state

    def chooseReturnActionDFS(self):

        movePos = { "N" : (-1, 0),
                    "S" : (1, 0),
                    "L" : (0, 1),
                    "O" : (0, -1),
                    "NE" : (-1, 1),
                    "NO" : (-1, -1),
                    "SE" : (1, 1),
                    "SO" : (1, -1)}
        
        # Queremos encontrar qual direção é a que tem menor valor na matriz
        movDirection = self.getLowestDirectionDFS()
        state = State(self.currentState.row + movePos[movDirection][0], self.currentState.col +movePos[movDirection][1])
        return movDirection, state

    def getLowestDirectionDFS(self):
        possibilities = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]

        
        curr = (self.currentState.row, self.currentState.col)

        # Procura um ponto de comparação
        for i in range(0,8):
            if self.result[curr][i] != None:
                lowestPos = self.result[curr][i] #lowestPos => state
                moveDirection = possibilities[i]
                break
        
        # Atualiza o lowestPos de fato
        for i in range(0,8):
            if not self.result[curr][i]:
                continue
            val = self.matrix[self.result[curr][i].row][self.result[curr][i].col]
            lowest = self.matrix[lowestPos.row][lowestPos.col]
            if self.result[curr][i] != self.currentState and val <= lowest:
                lowestPos = self.result[curr][i]
                moveDirection = possibilities[i]

        return moveDirection

    def getLowestDirection(self):
        low = -10
        row = self.currentState.row
        col = self.currentState.col
        for i in range(-1,2):
            for j in range(-1,2):
                if self.currentState.row + i < 0 or self.currentState.col + j < 0 or self.matrix[self.currentState.row + i][self.currentState.col + j] == None:
                    continue
                print('Matrix na pos: ', self.currentState.row + i, self.currentState.col + j, '\nValor: ',self.matrix[self.currentState.row + i][self.currentState.col + j])
                if low < 0:
                    low = self.matrix[self.currentState.row + i][self.currentState.col + j]
                    row = self.currentState.row + i
                    col = self.currentState.col + j   
                elif self.matrix[self.currentState.row + i][self.currentState.col + j] < low and self.matrix[self.currentState.row + i][self.currentState.col + j] != -1:
                    low = self.matrix[self.currentState.row + i][self.currentState.col + j]
                    row = self.currentState.row + i
                    col = self.currentState.col + j
        
        return (row - self.currentState.row, col - self.currentState.col)

    def isPossibleToMoveDiagonal(self, to_row, to_col):
        from_row = self.currentState.row
        from_col = self.currentState.col

        row_dif = to_row - from_row
        col_dif = to_col - from_col

        if (row_dif !=0 and col_dif != 0):
            if (self.matrix[from_row + row_dif][from_col] == -1 or
                self.matrix[from_row][from_col + col_dif] == -1):
                return False
        
        return True