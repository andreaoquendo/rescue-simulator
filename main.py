import sys
import os
import time

## Importa as classes que serao usadas
sys.path.append(os.path.join("pkg"))
from model import Model
from agentRnd import AgentRnd
from pkg.agentSavior import AgentSavior


## Metodo utilizado para permitir que o usuario construa o labirindo clicando em cima
def buildMaze(model):
    model.drawToBuild()
    step = model.getStep()
    while step == "build":
        model.drawToBuild()
        step = model.getStep()
    ## Atualiza o labirinto
    model.updateMaze()

def main():
    # Lê arquivo config.txt
    arq = open(os.path.join("config_data","ambiente.txt"),"r")
    configDict = {} 
    for line in arq:
        ## O formato de cada linha é:var=valor
        ## As variáveis são 
        ##  maxLin, maxCol que definem o tamanho do labirinto
        ## Tv e Ts: tempo limite para vasculhar e tempo para salvar
        ## Bv e Bs: bateria inicial disponível ao agente vasculhador e ao socorrista
        ## Ks :capacidade de carregar suprimentos em número de pacotes (somente para o ag. socorrista)

        values = line.split(" ")
        if values[0] == "Vitimas" or values[0] == "Parede" or values[0] == "Base":
            continue
        configDict[values[0]] = int(values[1])

    print("dicionario config: ", configDict)

    # Cria o ambiente (modelo) = Labirinto com suas paredes
    mesh = "square"

    ## nome do arquivo de configuracao do ambiente - deve estar na pasta <proj>/config_data
    loadMaze = "ambiente"

    model = Model(configDict["XMax"], configDict["YMax"], mesh, loadMaze)
    buildMaze(model)

    model.maze.board.posAgent
    model.maze.board.posGoal
    # Define a posição inicial do agente no ambiente - corresponde ao estado inicial
    model.setAgentPos(model.maze.board.posAgent[0],model.maze.board.posAgent[1])
    model.setGoalPos(model.maze.board.posGoal[0],model.maze.board.posGoal[1])  
    model.draw()

    # Cria um agente
    agentE = AgentRnd(model,configDict)

    ## Ciclo de raciocínio do agente
    aux = agentE.deliberate()
    while aux != -1:
        if aux == 0:
            return
        model.draw()
        #time.sleep(0.1) # para dar tempo de visualizar as movimentacoes do agente no labirinto
        aux = agentE.deliberate()

    agentE.yeahItsTimeToGoBackHome()
    while agentE.yeahItsTimeToGoBackHome() != -1:
        model.draw()
        #time.sleep(0.1) # para dar tempo de visualizar as movimentacoes do agente no labirinto
    model.draw()

    agentS = AgentSavior(model,configDict)
    info = agentE.giveInformantion()
    agentS.receiveInformation(info[0], info[1]) 

    ## Ciclo de raciocínio do agente
    aux = agentS.deliberate()
    while aux != -1:
        if aux == 0:
            return
        model.draw()
        time.sleep(0.1) # para dar tempo de visualizar as movimentacoes do agente no labirinto
        aux = agentS.deliberate()

    # agentS.yeahItsTimeToGoBackHome()
    # while agentS.yeahItsTimeToGoBackHome() != -1:
    #     model.draw()
    #     time.sleep(0.1) # para dar tempo de visualizar as movimentacoes do agente no labirinto
    # model.draw()     
        
if __name__ == '__main__':
    main()
