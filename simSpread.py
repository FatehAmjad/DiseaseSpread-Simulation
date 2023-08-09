# simSpread.py - Illustrates the spread of a disease through the population.
# Developed by: Fateh Amjad
# GitHub: www.github.com/FatehAmjad

import numpy as np
import matplotlib.pyplot as plt
import random
import sys

''' Creating a code to generate data either automatically, or manually through user input, by implementing a parameter sweep driver script to run the
simulation with varying parameters '''

if len(sys.argv) < 5:
    print('\nArguement values entered are too less! System sets default values to: POPINIT = 100 , INFECTEDINIT = 5, totalAirports = 5\n'
            'Hint: Give own arguement values using "Python3 simSpread.py <PopulationValue> <InfectedNumber> <neighbourhoodName> <Airports>')
    POPINIT = 100
    INFECTEDINIT = 5
    neighbourhood = None            # The following if-else statement does this: IF the user does not input any parameter values, #
    totalAirports = 5               # The terminal would notify the user that the system will now make use of its default parameter values #
else:                               # which are populationNumber = 100, InfectedPeople = 5, neighbourhoodSet = none (The user WILL BE ASKED AND HAS TO choose #
    arguement = sys.argv            # A neighbourhood amongst moore or von neumann to proceed further in the simulation, and the no.of total airports between transfers = 5 #
    POPINIT = int(arguement[1])
    INFECTEDINIT = int(arguement[2])
    neighbourhood = arguement[3] if arguement [3] in ["moore", "von-neumann"] else None
    totalAirports = int(arguement[4])

COLMAX = 15                
ROWMAX = 10
NUM_STEPS = 10                     # These are the pre-defined variable values that would be used in later functions below #
Rows_range = 9
Columns_range = 11


def distributePop(grid, numpeep): # Creates a grid with a list of zeros 
    num_r, num_c = grid.shape  # Defines 15 columns and 10 rows based on COLMAX and ROWMAX

    for i in range(numpeep):
        rpos = Rows_range
        cpos = Columns_range
        
                                          # Creating a barrier for restricting the spread of disease #
                            
        while rpos == Rows_range or cpos == Columns_range:                                                           
            rpos = random.randint(0, num_r-1)                   
            cpos = random.randint(0, num_c-1)                  
            
        grid[rpos, cpos] += 1
        #print("Adding 1 to (", rpos, ",", cpos,")")  # The distributePop function creates a grid with 15 columns, and 10 rows based on the pre-defined variables #
                                                      # COLMAX = 15, and ROWMAX = 10. The conditional loops create a barrier on the simulation plot that is shown, #
                                                      # Of the disease, acting as a boundary for the simulation values; The people move randomly accross the grid/map #
                                                      # Since random values are assigned using the random.randint function, and whenever the values are output,  #
                                                      # They would always be below number 9 and 11 in order to prevent the spread of the disease #

def showGrid(grid):
    num_r, num_c = grid.shape
#    for row in range(num_r-1, -1, -1):            
    for row in range(num_r):                           # Prints the grid on the terminal; 10 rows and 15 columns. #
        for col in range(num_c):
            print(grid[row,col], end=" ")
        print()

'''The buildScatter function uses values of the grid arguement, which are the no.of rows and columns defined, and uses the if condition to print the new grid values after 
the people have moved , whilst the FOR loops are Considered to be true. *Need to flip rows to have [0,0] at top left, axes are opposite way in plot y=row  '''

def buildScatter(grid):                         
    x_values = []
    y_values = []
    count_values = []
    num_r, num_c = grid.shape
    for row in range(num_r):                        
        for col in range(num_c):                    
            if grid[row,col] > 0:                               
                y_values.append(-row)                                           
                x_values.append(col)   # x=col 
                count_values.append(grid[row,col]*100) # size
#                print("Value at (", row, ",", col, ") is ", grid[row, col])    
    return(x_values, y_values, count_values)                

def plotGrids(Igrid, Ugrid):
    num_r, num_c = Igrid.shape
    Ix, Iy, Icount = buildScatter(Igrid)
    plt.scatter(Ix, Iy, s=Icount, c="r", alpha=0.5)
    Ux, Uy, Ucount = buildScatter(Ugrid)
    plt.scatter(Ux, Uy, s=Ucount, c="g", alpha=0.5)
    plt.axhline(Columns_range)                        # The axhline function is used to draw a horizontal line on the scatter, acting as a boundary line to restrict #    
    plt.axhline(Rows_range)                           # The exceeding of values beyond this range. # 
    plt.xlim = (-1, num_c)
    plt.ylim = (-1, num_r)
    plt.show()


def movePeeps(cur, next, r, c):
    #print("Pos (", r, ",", c, ") has ", cur[r,c], " people")
    num_r, num_c = cur.shape
    
    global neighbourhood

    for peep in range(cur[r,c]):
        if neighbourhood == "moore":
            # Moore neighbourhood code: If the user input is "moore", the below code defines how the peeps move within the map (Can move North, South, East, West, NorthEast, 
            #NorthWest, SouthEast and SouthWest)
            rMove = random.randint(-1,1)
            cMove = random.randint(-1,1)

        elif neighbourhood == "von-neumann":
            # Von Neumann neighbourhood code: If the user input is "von neumann", the below code defines how the peeps move within the map (Can only move North, South, East, West)
            vonMovement = random.randint(-1, 1)
            vonDirection = random.randint(0, 1)

            if vonDirection == 0:
                rMove = vonMovement
                cMove = 0
            if vonDirection == 1:
                rMove = 0
                cMove = vonMovement

         #print("Move from (", r, ",", c, ") to (", r+rMove, "," , c+cMove, ")")
        if (r + rMove) > (num_r-1) or (r + rMove) < 0:
            rMove = 0
        if (c + cMove) > (num_c-1) or (c + cMove) < 0:
            cMove = 0
        next[r + rMove, c + cMove] +=1
     #    print("          (", r, ",", c, ") to (", r+rMove, "," , c+cMove, ")")


                # Creating a method that sets neighbourhood according to the user input #

def findingNeighbourhood():
    default_neighbourhood = ["moore", "von-neumann"]
    
    global neighbourhood                                                                      
    
    while not neighbourhood:
        neighbourhood_entered = input("\nPlease enter a neighbourhood to set (moore or von-neumann): \n")
        if neighbourhood_entered.lower() in default_neighbourhood:
            neighbourhood = neighbourhood_entered
            print(f"Your neighbourhood has been set to : {neighbourhood_entered.title()}")
        else:
            print("The neighbourhood entered is invalid")

#find neighbourhood
findingNeighbourhood()                     # The findingNeighbourhood function is called to allow user to input a neighbourhood they want to choose amongst #
                                           # The moore and Von Neumann neighbourhoods. As per as the user input, the grid movement of people within it would change #
                                           # Wherein if the neighbourhood "von neumann" is prompted, the people can move up, down, left or right. If the "moore" #
                                           # Neighbourhood is selected, the users can move up, down, left, right, or even diagonally. If NO NEIGHBOURHOOD is entered, #
                                           # The simulation would not proceed. #
                                            
def infect(becameInfected, notInfected, r, c, prob):
#    print("Pos (", r, ",", c, ") has ", becameInfected[r,c], " becameInfected people and ", notInfected[r,c], " well people")
    prob = prob * becameInfected[r,c]
    if prob:
        for peep in range(notInfected[r,c]):
            if random.random() < prob:                        
                becameInfected[r, c] +=1            # Creates a function to calculate the no.of people that have been infected or are uninfected #
                notInfected[r, c] -=1
                print(">>> Infection Detected (", r, ",", c, ")")
                
                
                # Adding additional behaviour of death and recovery #

def death(becameInfected, r, c, prob): 
    for peep in range(becameInfected[r,c]):
        if random.random() < prob:
            becameInfected[r, c] -= 1
            print(f">>> Infection death ({r}, {c})")
    return becameInfected
                                                                # The functions death and reecovery are used to provide additional behaviour of individuals #
                                                                # Who have recovered, or died from the infection, if at all infected, otherwise are still categorized as #
                                                                # Individuals who are uninfected by the disease. #
def recovery(becameInfected, notInfected, r, c, prob): 
    for peep in range(becameInfected[r,c]):
        if random.random() < prob:
            notInfected[r, c] +=1
            becameInfected[r, c] -=1
            print(f">>> Recovered from infection ({r}, {c})")
    return becameInfected, notInfected

           # Creating an airport to allow the movement of people along long distances #
            
def airport(no_rows, no_cols, no_airports):
    rows, columns = Rows_range*np.ones(no_airports), Columns_range*np.ones(no_airports)
    while (Rows_range in rows) or (Columns_range in columns):
        rows, columns = np.random.randint(no_rows, size=no_airports), np.random.randint(no_cols, size=no_airports)
    airports = np.c_[rows, columns]
    return airports
                                                                # The airport function #selects a random number output from the list, but ensure that the size is smaller #
                                                                # than the value of no_airports variable; if true, the person is transferred from the currentAirport to the #
                                                                # nextAirport using the transferPeople function #
def transferPeople(cur, next, r, c):
    currentAirport = np.array([r,c])
    for peep in range(cur[r,c]):
        nextAirport = currentAirport
        while (nextAirport == currentAirport).all():
            nextAirport = random.choice(airports)
        cur[r,c] -= 1
        next[nextAirport[0], nextAirport[1]] += 1
        print(f">>> Transferring person from {currentAirport} airport to {nextAirport} airport.")
    return next

world = np.zeros((ROWMAX, COLMAX), dtype=int)  # Change np.int to int
infected = np.zeros((ROWMAX, COLMAX), dtype=int)  # Change np.int to int
uninfected = np.zeros((ROWMAX, COLMAX), dtype=int) 
airports = airport(ROWMAX, COLMAX, totalAirports)

distributePop(infected, INFECTEDINIT) # = 5
distributePop(uninfected, POPINIT) # = 100


#print(world)
#print()
showGrid(infected)
print()
showGrid(uninfected)

plotGrids(infected, uninfected)
for timestep in range(NUM_STEPS):
    print("\n###################### TIMESTEP", timestep, "#####################\n")
    infected2 = np.zeros((ROWMAX, COLMAX), dtype=int)
    uninfected2 = np.zeros((ROWMAX, COLMAX), dtype=int)
    for row in range(ROWMAX):
        for col in range(COLMAX):

            infect(infected, uninfected, row, col, 0.5) # Calls the method for calculating the infected ratio
            death(infected, row, col, 0.5) # Calls the method for calculating the death ratio
            recovery(infected, uninfected, row, col, 0.3) # Calls the method for calculating the recovery ratio

            if ([row, col] == airports).all(axis = 1).any() and \
                    random.random() < 0.4 and \
                    len(airports) > 1:
                transferPeople(infected, infected2, row, col)
                transferPeople(uninfected, uninfected2, row, col)

            movePeeps(infected, infected2, row, col)
            movePeeps(uninfected, uninfected2, row, col)

    infected = infected2
    uninfected = uninfected2
    plotGrids(infected, uninfected)
    print("Infected")
    showGrid(infected)
    print("Uninfected")
    showGrid(uninfected)


            # Using print command to output additional information regarding the statistics of the simulation #
    print("                                                 <<< Statistics >>>                                                                       ")
    print("Total population: ", POPINIT)
    print("Total no.of uninfected people: ", uninfected.sum().sum())
    print("Total no.of infected people: ", infected.sum().sum())
    print("Total no.of deaths: ", POPINIT+INFECTEDINIT-uninfected.sum().sum()-infected.sum().sum())

print("\n                                       ----- End of Disease-Spread-Simulation -----                                                   \n")
              

