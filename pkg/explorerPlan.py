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

    def updateCurrentState(self, state):
         self.currentState = state

    def updateMatrix(self, previous, expected, moveCost, didMove):
        """Define o estado inicial.
        @param cost: para atualizar a matrix.
        @param row, col: linha e coluna do estado inicial."""
        if didMove == True and (self.matrix[expected.row][expected.col] == None or self.matrix[expected.row][expected.col] > moveCost+self.matrix[previous.row][previous.col]):
            self.matrix[expected.row][expected.col] = moveCost+self.matrix[previous.row][previous.col]
        elif didMove == False:
            self.walls.append((expected.row, expected.col))
            print('MAMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIN')
            if expected.row < 0 or expected.col < 0:
                return
            self.matrix[expected.row][expected.col] = -1     
    
    def isItTimeToGoBackHome(self, timeLeft, cost):
        """Retorna se é momento de fazer o caminho de volta:
        @param timeLeft
        """
        if cost == None:
            return False
        if self.matrix[self.currentState.row][self.currentState.col] + cost - timeLeft >= 0:
            return True
        return False

    def setVictimsFile(self, current, vitals):
        """ Faz um update do arquivo de vítimas:
        @param current:
        @pram vitals:
        """    
        return
    

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

        while True:
            rand = randint(0, 7)
            movDirection = possibilities[rand]
            f = self.isVisitado(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])
            p = self.isParede(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])
            if p == True:
                continue
            chances = randint(0, 100)
            if f == True:
                if chances <= 10:
                    state = State(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])
                    break
            else:
                if chances <= 90:
                    state = State(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])
                    break
                

        return movDirection, state

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
        result = self.moveToNextPosition()

        # while not self.isPossibleToMove(result[1]):
        #     result = self.moveToNextPosition()

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
        low = self.matrix[self.currentState.row][self.currentState.col]
        row = self.currentState.row
        col = self.currentState.col
        for i in range(-1,2):
            for j in range(-1,2):
                if self.currentState.row + i < 0 or self.currentState.col + j < 0 or self.matrix[self.currentState.row + i][self.currentState.col + j] == None:
                    continue
                if self.matrix[self.currentState.row + i][self.currentState.col + j] < low and self.matrix[self.currentState.row + i][self.currentState.col + j] != -1:
                    low = self.matrix[self.currentState.row + i][self.currentState.col + j]
                    row = self.currentState.row + i
                    col = self.currentState.col + j
        return (row - self.currentState.row, col - self.currentState.col)

    # def do(self):
    #     """
    #     Método utilizado para o polimorfismo dos planos

    #     Retorna o movimento e o estado do plano (False = nao concluido, True = Concluido)
    #     """
        
    #     nextMove = self.move()
    #     return (nextMove[1], self.goalPos == State(nextMove[0][0], nextMove[0][1]))   