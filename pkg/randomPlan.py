from random import randint
from state import State

class RandomPlan:
    def __init__(self, maxRows, maxColumns, goal, initialState, name = "none", mesh = "square"):
        """
        Define as variaveis necessárias para a utilização do random plan por um unico agente.
        """
        self.walls = []
        self.knownWalls = []
        self.maxRows = maxRows
        self.maxColumns = maxColumns
        self.initialState = initialState
        self.currentState = initialState
        self.goalPos = goal
        self.actions = []
        self.visStates = []
        self.visStatesCnt = []

    
    def setWalls(self, walls):
        row = 0
        col = 0
        for i in walls:
            col = 0
            for j in i:
                if j == 1:
                    self.walls.append((row, col))
                col += 1
            row += 1
       
        
    def updateCurrentState(self, state):
         self.currentState = state

    def isInside(self, toState):
        """Verifica se o agente nao vai sair do labirinto
        @param toState: instancia da classe State - um par (lin, col) - que aqui indica a posicao futura 
        @return: True quando é possivel ir do estado atual para o estado futuro """

        ## vai para fora do labirinto
        if (toState.col < 0 or toState.row < 0):
            return False

        if (toState.col >= self.maxColumns or toState.row >= self.maxRows):
            return False
        
        if len(self.walls) == 0:
            return True
  
        return True

    def hitWall(self, toState):
        """Verifica se eh possivel ir da posicao atual para o estado (lin, col) considerando 
        a posicao das paredes do labirinto e movimentos na diagonal
        @param toState: instancia da classe State - um par (lin, col) - que aqui indica a posicao futura 
        @return: True quando é possivel ir do estado atual para o estado futuro """

        
        ## vai para cima de uma parede
        if (toState.row, toState.col) in self.walls:
            self.knownWalls.append((toState.row,toState.col))
            if (toState.row,toState.col) not in self.visStates:
                self.visStates.append((toState.row,toState.col))
                self.visStatesCnt.append(1)
            else:
                i = self.visStates.index((toState.row,toState.col))
                self.visStatesCnt[i] += 1

            return True

        # vai na diagonal? Caso sim, nao pode ter paredes acima & dir. ou acima & esq. ou abaixo & dir. ou abaixo & esq.
        delta_row = toState.row - self.currentState.row
        delta_col = toState.col - self.currentState.col

        ## o movimento eh na diagonal
        if (delta_row !=0 and delta_col != 0):
            if (self.currentState.row + delta_row, self.currentState.col) in self.walls and (self.currentState.row, self.currentState.col + delta_col) in self.walls:
                self.knownWalls.append((self.currentState.row + delta_row, self.currentState.col))
                if (self.currentState.row + delta_row, self.currentState.col) not in self.visStates:
                    self.visStates.append((self.currentState.row + delta_row, self.currentState.col))
                    self.visStatesCnt.append(1)
                else:
                    i = self.visStates.index((self.currentState.row + delta_row, self.currentState.col))
                    self.visStatesCnt[i] += 1

                self.knownWalls.append((self.currentState.row, self.currentState.col + delta_col))
                if (self.currentState.row, self.currentState.col + delta_col) not in self.visStates:
                    self.visStates.append((self.currentState.row, self.currentState.col + delta_col))
                    self.visStatesCnt.append(1)
                else:
                    i = self.visStates.index((self.currentState.row, self.currentState.col + delta_col))
                    self.visStatesCnt[i] += 1

                return True
            
        
        return False

    def isVisited(self, toState):
        """Verifica se o estado já foi visitado
        @param toState: instancia da classe State - um par (lin, col) - que aqui indica a posicao futura 
        @return: True quando é possivel ir do estado atual para o estado futuro """

        
        ## vai para a proxima posicao
        if (toState.row, toState.col) in self.visStates:
            return False

        if len(self.visStates) == 0:
            return True
        
        return True

    def pickPossibilities(self):
        """Verifica os movimentos possiveis considerando os estados já visitados
        @param toState: instancia da classe State - um par (lin, col) - que aqui indica a posicao futura 
        @return: True quando é possivel ir do estado atual para o estado futuro """
        
        possibilities = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]

        movePos = { "N" : (-1, 0),
                    "S" : (1, 0),
                    "L" : (0, 1),
                    "O" : (0, -1),
                    "NE" : (-1, 1),
                    "NO" : (-1, -1),
                    "SE" : (1, 1),
                    "SO" : (1, -1),
                    "Hit": (0, 0)}

        done = False
        tries = 1
        while not done:

            for i in possibilities:

                movDirection = i
                state = State(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])                    
               
                if ((state.row, state.col) in self.visStates):
                    if self.visStatesCnt[self.visStates.index((state.row, state.col))] >= tries:
                        possibilities.remove(movDirection)
            
            if len(possibilities) == 0:
                tries += 1
                possibilities = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]
            else:
                done = True
        
        return possibilities   

    def randomizeNextPosition(self):
         """ Sorteia uma direcao e calcula a posicao futura do agente 
         @return: tupla contendo a acao (direcao) e o estado futuro resultante da movimentacao """
         
         movePos = { "N" : (-1, 0),
                    "S" : (1, 0),
                    "L" : (0, 1),
                    "O" : (0, -1),
                    "NE" : (-1, 1),
                    "NO" : (-1, -1),
                    "SE" : (1, 1),
                    "SO" : (1, -1),
                    "Hit": (0, 0)}


         possibilities = self.pickPossibilities()

         rand = randint(0, len(possibilities) - 1)

         movDirection = possibilities[rand]
         state = State(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])

         # Testa se bateu na parede 
         if(self.hitWall(state) == True):
            movDirection = "Hit"
            state = State(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])

        ## SALVAR STATE  E QUANTAS VEZES FOI VISITADO AQUII

         return movDirection, state


    def chooseAction(self):
        """ Escolhe o proximo movimento de forma aleatoria. 
        Eh a acao que vai ser executada pelo agente. 
        @return: tupla contendo a acao (direcao) e uma instância da classe State que representa a posição esperada após a execução
        """

        ## TESTA SE AINDA TEM TEMPO PRA PROCURAR (CALCULA O TEMPO PRA VOLTAR E DESCONTA DO TEMPO DISPONIVEL)

        ## Tenta encontrar um movimento possivel dentro do tabuleiro 
        result = self.randomizeNextPosition()

        # Testa se o proximo movimento esta dentro do labirinto
        while not (self.isInside(result[1])):
                result = self.randomizeNextPosition()
        
        if (result[1].row,result[1].col) not in self.visStates:
            self.visStates.append((result[1].row,result[1].col))
            self.visStatesCnt.append(1)
        else:
            i = self.visStates.index((result[1].row,result[1].col))
            self.visStatesCnt[i] += 1

        return result


    def do(self):
        """
        Método utilizado para o polimorfismo dos planos

        Retorna o movimento e o estado do plano (False = nao concluido, True = Concluido)
        """
        
        nextMove = self.move()
        return (nextMove[1], self.goalPos == State(nextMove[0][0], nextMove[0][1]))   
    
     


        
       
        
        
