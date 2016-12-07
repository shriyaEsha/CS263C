import PreyAdult
import PreyOffspring
import qlearn_mod_random as qlearn
from AnimatObject import Animat
from Food import Food
from Obstacle import Obstacle
from Actions import Actions

class Predator(Animat):
    
    dictionaryOfPredators = dict()
    
    def __init__(self,width,height,color,image,grid):
        Animat.__init__(self, width, height, color,image, grid)
        self.ai = qlearn.QLearn(actions=range(Actions.directions),alpha=0.1, gamma=0.9, epsilon=0.1)
        Predator.dictionaryOfPredators[(self.gridX,self.gridY)] = self;
                        
    def getNeighborGridCoordinates(self):
        positionsOfNeighborGrids = []
        lookAroundDistance = 2        
        for i in range (-lookAroundDistance,lookAroundDistance + 1):
            for j in range (-lookAroundDistance,lookAroundDistance + 1):
                if((abs(i) + abs(j) <= lookAroundDistance) and (not (i==0 and j==0))):
                    neighborPosition = (self.gridX + i, self.gridY + j)
                    if(self.isWithinBounds(neighborPosition[0],neighborPosition[1])):
                        positionsOfNeighborGrids.append(neighborPosition)
        return positionsOfNeighborGrids
    
    def getPreyAdultPositionsInNeighborhood(self):
        neighborGrids = self.getNeighborGridCoordinates()
        preyPositionsInNeighborhood = []
        for neighborGrid in neighborGrids:
            if(PreyAdult.PreyAdult.dictionaryOfPreyAdults.has_key(neighborGrid)):
                preyPositionsInNeighborhood.append(neighborGrid)
        return preyPositionsInNeighborhood
    
    def getPreyOffspringPositionsInNeighborhood(self):
        neighborGrids = self.getNeighborGridCoordinates()
        offspringPositionsInNeighborhood = []
        for neighborGrid in neighborGrids:
            if(PreyOffspring.PreyOffspring.dictionaryOfOffsprings.has_key(neighborGrid)):
                offspringPositionsInNeighborhood.append(neighborGrid)
        return offspringPositionsInNeighborhood    
    
    def getAveragePreyAdultOffspringDistance(self):
        preyAdultPositionsInNeighborhood = self.getPreyAdultPositionsInNeighborhood()
        preyOffspringPositionsInNeighborhood = self.getPreyOffspringPositionsInNeighborhood()
        preyAdultPositionsInNeighborhood.sort()
        preyOffspringPositionsInNeighborhood.sort()
        totalPrey = len(preyAdultPositionsInNeighborhood) + len(preyOffspringPositionsInNeighborhood)
        # calculate distance between adults and offspring
        dist = 0
        import math
        for (p1,p2) in zip(preyAdultPositionsInNeighborhood,preyOffspringPositionsInNeighborhood):
            dist += math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        if totalPrey > 0:
            return round(dist/totalPrey,1)
        else:
            return 0

    def update(self):
        state = self.calculateState()
        reward = -1
        
        #Check if the animat has been eaten by any of the predators
        if (self.gridX,self.gridY) in self.previousPositionTuples:
            reward += -20
        
        # preyAdult in neighbourhood means less reward
        # if self.hasPreyAdultInNeighborhood():
        #     reward += 30
        
        # preyOffspring in neighbourhood means more reward
        # if self.hasPreyOffspringInNeighborhood():
        #     reward += 40

        # reduce reward proportional to average distance between preyAdult and preyOffspring
        # reward += -2 * (self.getAveragePreyAdultOffspringDistance() * self.lenPreyAdultInNeighborhood())

        # add reward proportional to no of nearby predators
        # reward += 5 * self.getPredatorsInNeighborhood()

        if(self.isEatingPreyAdult() or self.isEatingPreyOffspring()):
            #PreyAdult re-spawns itself randomly, if it gets eaten
            self.fed += 1
            reward += 50            
                
        if(self.lastState is not None):
            self.ai.learn(self.lastState,self.lastAction,reward,state)
            
        state = self.calculateState()
        action = self.ai.chooseAction(state)
        self.lastState = state
        self.lastAction = action            
        self.setPrevious2Positions()
        self.performAction(action)
        self.drawGameObjectAtCurrentPosition()
    
    def calculateState(self):
        def stateValueForNeighbor(neighborCellCoordinates):
            if self.isCellOnAnyPreyAdult(neighborCellCoordinates):
                return 3
            elif self.isCellOnAnyFood(neighborCellCoordinates):
                return 2
            elif self.isCellOnAnyObstacle(neighborCellCoordinates):
                return 1
            else:
                return 0
        return tuple([stateValueForNeighbor(neighborCellCoordinates) for neighborCellCoordinates in self.getNeighborGridCoordinates()])    
    
    def getPredatorsInNeighborhood(self):
        neighborGrids = self.getNeighborGridCoordinates()
        predatorPositionsInNeighborhood = []
        for neighborGrid in neighborGrids:
            if(self.dictionaryOfPredators.has_key(neighborGrid)):
                predatorPositionsInNeighborhood.append(neighborGrid)
        return len(predatorPositionsInNeighborhood)
    
    def hasPreyAdultInNeighborhood(self):
        preyAdultInNeighborHood = self.getPreyAdultPositionsInNeighborhood()
        if(len(preyAdultInNeighborHood) > 0):
            return True
        return False
    def lenPreyAdultInNeighborhood(self):
        preyAdultInNeighborHood = self.getPreyAdultPositionsInNeighborhood()
        return len(preyAdultInNeighborHood)
    
    def hasPreyOffspringInNeighborhood(self):
        preyOffspringInNeighborHood = self.getPreyOffspringPositionsInNeighborhood()
        if(len(preyOffspringInNeighborHood) > 0):
            return True
        return False
    
    def isEatingPreyAdult(self):
        return self.isCellOnAnyPreyAdult((self.gridX,self.gridY))
    
    def isEatingPreyOffspring(self):
        return self.isCellOnAnyPreyOffspring((self.gridX,self.gridY))
        
    def isCellOnAnyPreyAdult(self,gridCoordinatesOfCell):
        preyAdultKeys = PreyAdult.PreyAdult.dictionaryOfPreyAdults.keys() #Keys are tuples and Values are references to the actual prey object
        for preyAdultPosition in preyAdultKeys:
            if(gridCoordinatesOfCell == preyAdultPosition):
                return True
        return False
    
    def isCellOnAnyPreyOffspring(self,gridCoordinatesOfCell):
        preyOffspringKeys = PreyOffspring.PreyOffspring.dictionaryOfOffsprings.keys() #Keys are tuples and Values are references to the actual prey object
        for preyOffspringPosition in preyOffspringKeys:
            if(gridCoordinatesOfCell == preyOffspringPosition):
                return True
        return False
    
    def isCellOnAnyFood(self,gridCoordinatesForCell):
        if(Food.dictionaryOfFoodObjects.has_key(gridCoordinatesForCell)):            
            return True
        return False
    
    def isCellOnAnyObstacle(self,gridCoordinatesForCell):
        if(Obstacle.dictionaryOfObstacles.has_key(gridCoordinatesForCell)):            
            return True
        return False
    
    #TODO: Requires massive change for multiple Predators
    def move(self, directionX, directionY):
        oldXPosition = self.gridX
        oldYPosition = self.gridY        
        nextXPosition = self.gridX + directionX
        nextYPosition = self.gridY + directionY
        if(self.isMovementPossible(nextXPosition, nextYPosition)):
            #If prey is in new position     
            if(not Predator.dictionaryOfPredators.has_key((nextXPosition,nextYPosition))):
                #Another PreyAdult is not on the next Position, so valid movement
                Animat.move(self, directionX, directionY)
                Predator.dictionaryOfPredators.pop((oldXPosition,oldYPosition))
                Predator.dictionaryOfPredators[(self.gridX,self.gridY)] = self;    