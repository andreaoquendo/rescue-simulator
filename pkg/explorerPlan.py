import os
from pickle import TRUE
from random import randint
from state import State

class ExplorerPlan:
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
        self.matrix = [[None for j in range(100)]for i in range(100)] # MUDAR: Não façam isso em casa
        self.matrix[initialState.row][initialState.col] = 0.0
        self.file = ''
        self.victims = {}

        self.actionsDFS = {}
        self.result = {}
        self.untried = {}
        self.unbacktracked = {}
        self.unbackbacktracked = {}
        self.previousDirection = "nop"

    def updateCurrentState(self, state):
        """Faz o upload do current state dentro do plano.
        """
        self.currentState = state

    def updateMatrix(self, previous, expected, moveCost, didMove):
        """Define o estado inicial.
        @param cost: para atualizar a matrix.
        @param row, col: linha e coluna do estado inicial."""
        if didMove == 1 and (self.matrix[expected.row][expected.col] == None or self.matrix[expected.row][expected.col] > moveCost+self.matrix[previous.row][previous.col]):
            self.matrix[expected.row][expected.col] = moveCost+self.matrix[previous.row][previous.col]
        elif didMove == -1:
            self.walls.append((expected.row, expected.col))
            if expected.row < 0 or expected.col < 0:
                return
            self.matrix[expected.row][expected.col] = -1
        else:
            return    
    
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
        """ Faz um update do arquivo de vítimas:
        @param current:
        @pram vitals:
        """    
        print('MAAAAAAAAAAAAAAAAAAAAAAAAAAAAE O FORNINHOOOOOOOOOOOOOOOOOOOOOOOOO')
        print(vitals[0])
        self.victims[vitals[0][0]] = self.currentState
        vitals[0] = [str(x) for x in vitals[0]]
        line = ','.join(vitals[0]) + '\n'
        self.file += line

    def saveVictimsFile(self):
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

        # Partimos primeiro das opções não tentadas primeiro
        # Não esquecer de reservar o result depois
        # No unbacktracked ele precisa saber qual foi o previous state
        while len(self.untried[curr_pos]) > 0 :
            print('untried: ', self.untried[curr_pos])
            if self.previousDirection == "nop" or self.untried[curr_pos][-1] == oppositeDirection[self.previousDirection] or len(self.untried[curr_pos]) <= 1:
                movDirection = self.untried[curr_pos].pop()
            else:
                aux = self.untried[curr_pos].pop()
                movDirection = self.untried[curr_pos].pop()
                self.untried[curr_pos].append(aux)
                
            state = State(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])
            self.previousDirection = movDirection
            if(self.isParede(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])):
                print('parede is possibilities', possibilities)
                r_possibilities = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]
                self.result[curr_pos][r_possibilities.index(movDirection)] = self.currentState
            elif self.isVisitado(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1]) and len(self.untried[curr_pos]) > 1:
                r_possibilities = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]
                self.result[curr_pos][r_possibilities.index(movDirection)] = state  
                self.unbacktracked[curr_pos].append(movDirection)
            else:
                return movDirection, state

        # No unbacktracked só queremos saber qual foi a ação que levou ela a fazer o que fez
        if len(self.unbacktracked[curr_pos]) > 0:
            print('unbacktrack', self.unbacktracked[curr_pos])
            
            movDirection = self.unbacktracked[curr_pos][0]
            self.unbackbacktracked[curr_pos].append(movDirection)
            self.unbacktracked[curr_pos].remove(self.unbacktracked[curr_pos][0])
        
            state = State(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])
            self.previousDirection = movDirection
            return movDirection, state
        
        print('cheguei', self.unbackbacktracked[curr_pos])
        if  len(self.unbackbacktracked[curr_pos]) > 0:
            print('cheguei', self.unbackbacktracked[curr_pos])
            movDirection = self.unbackbacktracked[curr_pos].pop()
            state = State(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])
            return movDirection, state

        print('enviando none')

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
