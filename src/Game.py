import pygame
from Grid import Grid
from Food import Food
from Obstacle import Obstacle
from Predator import Predator
from PreyAdult import PreyAdult
from PreyOffspring import PreyOffspring
import time

# Define some colors
BLACK = (0, 0, 0)
WHITE = (240, 220, 106)
GREEN = (80, 240, 56)
CYAN = (54, 134, 156)
LIGHT_BLUE = (200, 200, 255)
RED = (79, 46, 15)
BLUE = (0, 0, 255)
ORANGE = (232, 84, 80)

# Define images for animats
lion = pygame.image.load("images/lion.png")
deerA = pygame.image.load("images/deerA.png")
deerO = pygame.image.load("images/deerO.png")
lion = pygame.transform.scale(lion,(40,40))
deerA = pygame.transform.scale(deerA,(40,40))
deerO = pygame.transform.scale(deerO,(40,40))

# initialize the game engine
pygame.init()
pygame.display.set_caption("My Game") 
clock = pygame.time.Clock()

numberOfCellsInColumnsOrRows = 20
margin = 5
done = False

widthOfCell = 30
heightOfCell = 30
sizeOfCell = 30

numberOfPreyAdults = 10
numberOfPreyOffsprings = 5
numberOfPredators = 4
numberOfFoodObjects = 10
numberOfObstacles = 3

sizeCalculation = widthOfCell * numberOfCellsInColumnsOrRows + (margin * (numberOfCellsInColumnsOrRows + 1))
size = (sizeCalculation, sizeCalculation)

screen = pygame.display.set_mode(size)

# Environment Agents/Objects
grid = Grid(numberOfCellsInColumnsOrRows, numberOfCellsInColumnsOrRows, sizeOfCell, screen, margin, pygame)
# Always init obstacles before everything else, because you don't want food being init'd on top of obstacle 
[Obstacle(widthOfCell, heightOfCell, BLACK,"", grid) for i in range(0, numberOfObstacles)]
[Predator(widthOfCell, heightOfCell,"", lion, grid) for i in range(0, numberOfPredators)]
[PreyAdult(widthOfCell, heightOfCell,"", deerA, grid) for i in range(0, numberOfPreyAdults)]
[PreyOffspring(widthOfCell, heightOfCell,"", deerO, grid) for i in range(0, numberOfPreyOffsprings)]
[Food(widthOfCell, heightOfCell, ORANGE,"", grid) for i in range(0, numberOfFoodObjects)]

# Reference to all animat agents in the environment
# environmentAgents = []
# [environmentAgents.append(predator) for predator in predators]
# [environmentAgents.append(prey) for singular_prey in prey]

def resetGridReferences():
    for cellRow in grid.cellMatrix:
        for cell in cellRow:
            cell.prey = []
            cell.predators = []
            cell.obstacles = []
            cell.foods = []

def worldUpdate(showDisplay):
                        
    screen.fill(GREEN)    
    grid.drawGrid(WHITE)               
        
    resetGridReferences()
        
    foodKeys = Food.dictionaryOfFoodObjects.keys()
    if(len(foodKeys) < 1):
        foods = [Food(widthOfCell, heightOfCell, ORANGE,"", grid) for i in range(0, numberOfFoodObjects)]
    for foodObjectPosition in foodKeys:
        food = Food.dictionaryOfFoodObjects[foodObjectPosition]
        food.update()
        grid.cellMatrix[food.gridX][food.gridY].food = food
        food.createFoodGradientsInNeighbors(3)
        food.gradientsCreated = True
        
    obstacleKeys = Obstacle.dictionaryOfObstacles.keys()
    for obstaclePosition in obstacleKeys:
        obstacle = Obstacle.dictionaryOfObstacles[obstaclePosition]        
        obstacle.update()
        grid.cellMatrix[obstacle.gridX][obstacle.gridY].obstacle = obstacle
    
    predatorKeys = Predator.dictionaryOfPredators.keys()
    for predatorPosition in predatorKeys:
        predator = Predator.dictionaryOfPredators[predatorPosition]
        predator.update()
        grid.cellMatrix[predator.gridX][predator.gridY].predator = predator
    
    preyAdultKeys = PreyAdult.dictionaryOfPreyAdults.keys()
    for preyAdultPosition in preyAdultKeys:
        singularAdultPrey = PreyAdult.dictionaryOfPreyAdults[preyAdultPosition]        
        grid.cellMatrix[singularAdultPrey.gridX][singularAdultPrey.gridY].preyAdult = singularAdultPrey
        singularAdultPrey.update()       
        
    offspringKeys = PreyOffspring.dictionaryOfOffsprings.keys()
    for preyOffspringPosition in offspringKeys:
        singular_preyoffspring = PreyOffspring.dictionaryOfOffsprings[preyOffspringPosition]        
        grid.cellMatrix[singular_preyoffspring.gridX][singular_preyoffspring.gridY].offspring = singular_preyoffspring
        singular_preyoffspring.update()    
    
    if(showDisplay):
        pygame.display.update()
        clock.tick(5)       

worldAge = 0

# create file for plotting graphs
liveness_fileA = open('livenessA.txt','a')
prot = open('prot.txt','a')
dfile = open('dfile.txt','a')
# liveness_fileO = open('livenessO.txt','a')
group_file = open('group.txt','a')

endAge = worldAge + 10000
while not done and worldAge < endAge:
    # --- Main event loop      
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True            
    
    grid.shouldDrawScreen = True  
    worldUpdate(grid.shouldDrawScreen)
    tot_eaten = 0
    tot_prot = 0
    avg_dist = 0
    avg_grp_size = 0
    if worldAge % 1000 == 0:
        # create file for plotting graphs
        liveness_fileA = open('livenessA.txt','a')
        dfile = open('dfile.txt','a')
        prot = open('prot.txt','a')
        # liveness_fileO = open('livenessO.txt','a')
        group_file = open('group.txt','a')

        preyAdultKeys = PreyAdult.dictionaryOfPreyAdults.keys()
        for preyAdultPosition in preyAdultKeys:
            singular_prey = PreyAdult.dictionaryOfPreyAdults[preyAdultPosition]                                
            print "{:d}, e: {:0.2f}, W: {:d}, L: {:d}, CP: {:d}"\
                .format(worldAge, singular_prey.ai.epsilon, singular_prey.fed, singular_prey.eaten, singular_prey.offspringsProtected)
            # find average group size
            avg_grp_size += len(singular_prey.getPreyAdultPositionsInNeighborhood())
            # write to file here
            tot_eaten += (singular_prey.eaten)
            tot_prot += (singular_prey.offspringsProtected)
            avg_dist += singular_prey.avg_distance

            singular_prey.eaten = 0
            singular_prey.fed = 0
            singular_prey.offspringsProtected = 0
        if avg_grp_size > len(PreyAdult.dictionaryOfPreyAdults.keys()):
            avg_grp_size /= len(PreyAdult.dictionaryOfPreyAdults.keys())
        else:
            avg_grp_size = 1
        avg_dist /= len(PreyAdult.dictionaryOfPreyAdults.keys())

        prot.write(str(worldAge)+','+str(tot_prot)+'\n')
        dfile.write(str(worldAge)+','+str(avg_dist)+'\n')
        group_file.write(str(worldAge)+','+str(avg_grp_size)+'\n')
        liveness_fileA.write(str(worldAge)+','+str(tot_eaten)+'\n')
        liveness_fileA.close()
        prot.close()
        dfile.close()
        group_file.close()
        print 'grp: '+str(avg_grp_size)+" tot: "+str(tot_eaten)
    worldAge += 1
    print worldAge
    
while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True   
    
    grid.shouldDrawScreen = True    
    worldUpdate(grid.shouldDrawScreen)


pygame.quit()
