from EnvironmentObject import EnvironmentObject

class Obstacle(EnvironmentObject):
    
    #Static Variable - Class members
    dictionaryOfObstacles = dict()
        
    def __init__(self,width,height,color,image,grid):
        EnvironmentObject.__init__(self,width,height,color,image,grid)
        #Already initialized at a random position by superclass
        Obstacle.dictionaryOfObstacles[(self.gridX,self.gridY)] = self