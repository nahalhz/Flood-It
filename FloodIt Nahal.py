#########################################################################################################
## File Name: FloodIt-Nahal.py                                                                         ##
## Author: Nahal H.                                                                                    ##                                                                               ##
## Modules Used: pygame, string, time, Controls                                                        ##
#########################################################################################################

#----------------#
#    IMPORTS     #
#----------------#
import pygame
pygame.init()
import string
import time
import math
import random
from Controls import Grid
from Controls import Label
from Controls import Button
from Controls import ComboBox
#----------------#
#   CONSTANTS    #
#----------------#
RED   = (255,0,0)
GREEN = (0,255,0)
BLUE  = (0,0,255)
GREY = (230,230,230)
BLACK = (0,0,0)
PURPLE = (102, 0, 102)
WHITE = (255,255,255)
PINK = (255, 51, 204)
ORANGE = (255, 102, 0)
YELLOW = (255, 255, 0)
MINT = (0, 204, 153)

colorsLst = [RED,GREEN,BLUE,PURPLE,PINK,ORANGE,YELLOW,MINT] #list of colours available for the gamegrid


#----------------------------------------------------------------------------------------------------------------------------------#
#                                            GAME GRID CLASS                                                                       #
#----------------------------------------------------------------------------------------------------------------------------------#
class Gamegrid(Grid):
    def __init__ (self, r, rows, columns, colorLst, gap=0,border=True, borderColor=(0,0,0), borderWidth=2,visible=True):
        Grid.__init__(self, r, rows, columns, gap=gap, border=border,visible = visible )
       
        self.border = border
        self.colorList = colorLst
        self.borderColor = borderColor
        self.cellsColor = self.cellColor()
        self.numMoves = self.loadnumMoves() 
        self.score = self.loadScore()

    def cellColor(self):
        colorOrder = []
        for c in self.cells:
            randColor = random.choice(self.colorList) # a list of random colours
            colorOrder.append(randColor)
        return colorOrder
    def loadnumMoves(self):   # determine how many moves are allowed according to size of grid and number of colours used
        numMoves = round(math.sqrt(self.rows * self.columns * len(self.colorList)))
        if numMoves > self.rows*self.columns:
            return self.rows * self.columns -1
        else:
            return numMoves-4 #increase difficulty
    def loadScore(self):  # load score displayer label as a list(first element is the one we manipulate to increase score) 
        x2 = self.x + 15
        y2 = self.y + 370
        score =[]
        score1 =Label('0',(self.x-20,y2,300,30), align='center',textColor=(0,0,0),fontSize=30)
        numMoves = "/" + str(self.numMoves)
        score2 = Label(numMoves,(x2,y2,300,30), align='center',textColor=(0,0,0),fontSize=30)
        score.append(score1)
        score.append(score2)
        return score
    def draw(self,win):
        if self.border:
            pygame.draw.rect(win,self.colour,self.rect,20)
##            if self.rows > 10:
##                pygame.draw.rect(win,(0,0,0),(self.x-20,self.y-20,self.width,self.height))    
        for i,rec in enumerate(self.cells):
            pygame.draw.rect(win,self.cellsColor[i],rec)
        for scr in self.score:
            scr.draw(win)
        

    def floodIt(self, cell, oldClr, newClr): # flood it recursive method
        if self.cellsColor[cell] != oldClr: # base case: if all neighbouring cells are tirned to thenew colour
            return
        self.cellsColor[cell] = newClr
        sCells = self.surroundingCells(cell) # call neighbouringCell method of grid(parent class)
        for n in sCells:
            self.floodIt(n, oldClr, newClr)

    def filledGrid(self): # check to see if grid is filled with one colour
        true = 0
        for i,clr in enumerate(self.cellsColor):
            if self.cellsColor[0] == self.cellsColor[i]:
                true += 1
        return true == len(self.cellsColor)
                
        
#----------------#
#   FUNCTIONS    #
#----------------#
def redraw_game_window(win,controls,winGame,loseGame,startGame,Instext,rowCols):
    win.fill(WHITE)
    if winGame == True:
        winSurface = pygame.font.SysFont("arial", 30).render('You win!',True,(0,0,0))
        win.blit(winSurface,((290,500)))
    elif loseGame == True:
         loseSurface = pygame.font.SysFont("arial", 30).render('You lose!',True,(0,0,0))
         win.blit(loseSurface,((290,500)))
    if not startGame:
        Instext.draw(win)
    if rowCols > 10:
        pygame.draw.rect(win,(0,0,0),(160,90,300,300))
    for control in controls:
        control.draw(win)
    pygame.display.update()
# function to find size of the new grid based on the option clicked on the comboBox
def findSize(s):  
    if len(s) == 3: # check for one digit number
        num = int(s[0])
    else:
        num = int(s[:2])
    return num
    
#------------------------------#
#  INITIALIZATION + MAIN LOOP  #
#------------------------------#
def main():
    # GAME DISPLAY SETUP #
    win = pygame.display.set_mode((640,640)) 
    pygame.display.set_caption('Flood-It Game by Nahal H.')
    # VARIABLE INITIALIZATION #
    sizeLst = ['2x2','6x6','10x10','14x14','18x18','22x22']
    colorNumLst = ['3','4','5','6','7','8']
    winGame = False
    loseGame = False
    startGame = False
    resetBtnIndex = -1
    rowCols = 6
    clrs = 4
    inPlay = True
    # OBJECTS #
    titleLabel= Label("Flood-It", (0,20,640,30), align='center',textColor=(244,194,194),fontSize=70)
    mainGrid = Gamegrid((170,100,300,300),rowCols,rowCols,colorsLst[:clrs])
    changeSize = ComboBox((170, 430,100,30), "Size",sizeLst , True)
    colorNum = ComboBox((290,430,100,30), "Colors",colorNumLst, True)
    #set default values for the size of the grid#
    colorNum.textBox.text = colorNumLst[1]
    changeSize.textBox.text = sizeLst[1]
    resetBtn =Button("New Game",(410,430,80,30),color=(217,244,237))
    Instext = Label("Click the cells. Fill the board with the same colour.", (170,520,300,20), align='center',textColor=(0,0,0),fontSize=15)
    
    controls = [titleLabel,mainGrid,changeSize,colorNum,resetBtn] #list of the objects

    # MAIN LOOP STARTS HERE #
    while inPlay:
        redraw_game_window(win,controls,winGame,loseGame,startGame,Instext,rowCols)
        pygame.time.delay(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inPlay = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inPlay = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickPos = pygame.mouse.get_pos()
                gridBtnIndex = mainGrid.getCellIndex(clickPos)  
                if gridBtnIndex != -1:
                    startGame = True  # Instructions disappear from window
                    if mainGrid.cellsColor[0] == mainGrid.cellsColor[gridBtnIndex]: # if you click on same colour, flood it won't happen + score not added
                        print('same colour')
                    else:
                        mainGrid.floodIt(0,mainGrid.cellsColor[0],mainGrid.cellsColor[gridBtnIndex]) #flood it
                        mainGrid.score[0].text = str(int(mainGrid.score[0].text) + 1) # add score
                    filledgrid = mainGrid.filledGrid() # checks to see if grid is filled with same colour or not
                    if filledgrid and int(mainGrid.score[0].text) <= mainGrid.numMoves:   # check if game is won
                        winGame = True
                    elif not filledgrid and int(mainGrid.score[0].text) >= mainGrid.numMoves:  # check if game is lost
                        loseGame = True
                changeSizeIndex = changeSize.menu.getCellIndex(clickPos)
                if changeSizeIndex != -1:
                    rowCols = findSize(sizeLst[changeSizeIndex]) # calls findsize function to find the number of rows and columns for the new grid
                colorNumIndex = colorNum.menu.getCellIndex(clickPos)
                if colorNumIndex != -1:
                    clrs =int(findSize(colorNumLst[colorNumIndex])) # find the number of colours for the new grid
                resetBtnIndex = resetBtn.isOver(clickPos)
                print(resetBtnIndex)
                if resetBtnIndex == 1:
                    controls.pop(1) #old main Grid is removed 
                    mainGrid = Gamegrid((170,100,300,300),rowCols,rowCols,colorsLst[:clrs])
                    controls.insert(1,mainGrid) # new Grid is added 
                    winGame = False
                    loseGame = False    # game is reset 
            if event.type == pygame.MOUSEBUTTONUP:
                pass
            if event.type == pygame.MOUSEMOTION:
                mp = pygame.mouse.get_pos()
            changeSize.update(event)
            colorNum.update(event)
        
    pygame.quit()

if __name__ == "__main__":
    main()
