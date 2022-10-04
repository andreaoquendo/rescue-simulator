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

    def updateMatrix(self, before, after, cost, didMove):
        """Define o estado inicial.
        @param cost: para atualizar a matrix.
        @param row, col: linha e coluna do estado inicial."""
        if didMove == True and (self.matrix[after.row][after.col] == None or self.matrix[after.row][after.col] > cost+self.matrix[before.row][before.col]):
            self.matrix[after.row][after.col] = cost+self.matrix[before.row][before.col]
        elif didMove == False:
            self.matrix[after.row][after.col] = -1
    
    def isItTimeToGoBackHome(self, timeLeft, cost, current):
        if self.matrix[current.row][current.col] + cost - timeLeft >= 0:
            return True
        return False

    #MUDAR, VERIFICAR APENAS DURANTE A EXECUÇÃO
    def setWallsFile(self, walls):
        return

        # row = 0
        # col = 0
        # for i in walls:
        #     col = 0
        #     for j in i:
        #         if j == 1:
        #             self.walls.append((row, col))
        #         col += 1
        #     row += 1
       
        
    

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

        # aux = (current.row, current.col)
        # if self.movement[aux] == None:
        #     self.movement[aux] = []
        
        # len(self.movement[aux])

        while True:
            rand = randint(0, 7)
            movDirection = possibilities[rand]
            f = self.isVisitado(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])
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


    # def do(self):
    #     """
    #     Método utilizado para o polimorfismo dos planos

    #     Retorna o movimento e o estado do plano (False = nao concluido, True = Concluido)
    #     """
        
    #     nextMove = self.move()
    #     return (nextMove[1], self.goalPos == State(nextMove[0][0], nextMove[0][1]))   