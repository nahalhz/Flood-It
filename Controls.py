#Controls BY NAHAL H>\.
#########################################################################################################
## File Name: Controls.py                                                                         ##
## Author: Nahal H.                                                                                    ##
## Date: May 19 2020                                                                                   ##
## Modules Used: pygame, string, time                                                                  ##
## Description:  This programs contains Grid, Menu, Label, button, Textbox, and ComboBox classes       ##
## which have methods and attributes that helps us built them and modify each based on the ability     ##
## and function that we want each of the objects derived from the clsses to have. There are also       ##
## examples of class inheritance(: menu is a child class of grid and button is a child class of label) ##
## and class composition (: button objects are made in menu class and we use menu, textbox, label      ##
## classes to create the comboBox objects.) Using the classes we make objects which we can modify based##
## on the methods and attributes in the classes(Ex: ComboBox can be either simple or not).             ##
## Input: User inputs text in texboxes and can choose options on comboboxes to cause changes to the    ##
## program's visuals.                                                                                  ##
#########################################################################################################

#----------------#
#    IMPORTS     #
#----------------#
import pygame
pygame.init()
import string
import time

#----------------#
#   CONSTANTS    #
#----------------#
RED   = (255,0,0)
GREEN = (0,255,0)
BLUE  = (0,0,255)
GREY = (230,230,230)
BLACK = (0,0,0)
PURPLE = (200,0,200)
PINK = (255, 51, 204)
ORANGE = (255, 102, 0)

DF_fontType = "calibri"
DF_fontSize = 14

#--------GRID CLASS -----------------------------------------------------------------------------------------------------
class Grid(object):

    def __init__ (self, r, rows, columns, gap=0, border=False, colour = (0,0,0),visible = True, simple=True ):
        self.x = r[0]
        self.y = r[1]
        self.width = r[2]
        self.height = r[3]
        self.rect = r
        self.colour = colour
        self.rows = rows
        self.columns = columns
        self.gap = gap
        self.border = border
        self.cellWidth = (self.width - (gap * (columns - 1 + int(border) * 2))) // columns
        self.cellHeight = (self.height - (gap * (rows - 1 + int(border) * 2))) // rows
        #print(self.cellWidth, self.cellHeight)
        self.cells = self.loadCells()
        self.txtboxCells = self.loadTextbox()
        self.visible = visible
        self.simple = simple

    def loadCells(self):
        cellRects = []
        cellY = self.y + int(self.border) * self.gap
        for r in range(self.rows):
            cellX = self.x + int(self.border) * self.gap
            for c in range(self.columns):
                 cellRect = (cellX,cellY,self.cellWidth,self.cellHeight)
                 cellRects.append(cellRect)
                 cellX += self.gap + self.cellWidth
            cellY += self.gap + self.cellHeight
        return cellRects

    def loadTextbox(self):
        txtboxCells = []
        for rec in self.cells:
             txtboxCell = TextBox(rec,txtColor=(0,0,0),fillColor=GREY)
             txtboxCells.append(txtboxCell)
        return txtboxCells
        

    def draw(self,win):
        if self.border:
            pygame.draw.rect(win,self.colour,self.rect,1)
        for i,rec in enumerate(self.cells):
            if self.simple:
                pygame.draw.rect(win,self.colour,rec,1)
            else:
                self.txtboxCells[i].draw(win)
            
            

    def getCellIndex(self,mp):
        for i,rec in enumerate(self.cells):
            if pygame.Rect(rec).collidepoint(mp):
                return i
        return -1

    def surroundingCells(self, i):
        neighbourCells = []
        a = i + 1
        if a < (self.rows*self.columns):
             if a % self.columns != 0:
                neighbourCells.append(a)
        b = i - 1
        if i % self.columns != 0:
            neighbourCells.append(b)
        c = i + self.columns
        if c < (self.rows*self.columns):
            neighbourCells.append(c)
        d = i - self.columns
        if d >= 0:
            neighbourCells.append(d)
        neighbourCells.sort()
        return neighbourCells
        
    def update(self,event):
        if not self.simple:
            for txtbox in self.txtboxCells:
                txtbox.update(event)


#--------MENU CLASS -----------------------------------------------------------------------------------------------------
class Menu(Grid):
    def __init__ (self, r, rows, columns, text, gap=0,  border=True, colour=(255,255,255), textColor=(0,0,0), borderColor=(0,0,0), borderWidth=2, mouseOverColor=(255,0,0), fontType='arialrounded', fontSize=12, align='center',visible=True):
        #Grid.__init__(self, r, rows, columns, gap=0, border=True, colour = (255,255,255),visible = True)
        Grid.__init__(self, r, rows, columns, gap=gap, border=border, colour = colour,visible = visible )     # <=== I changed to this Reason: now the defaults com from the line above so if they were to change you only hve to change one thing, its a small thing

        self.textColor = textColor
        self.text = text
        self.align = align
        self.textColor = textColor
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.fontSize=fontSize
        self.fontType=fontType
        self.font = pygame.font.SysFont(fontType, fontSize)
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.mouseOverColor = mouseOverColor
        self.buttons = self.loadButtons()     

    def loadButtons(self):

        buttonLst = []
        for i,rec in enumerate(self.cells):
            newBtn = Button(self.text[i],rec,self.colour,self.textColor,self.borderColor,1,self.mouseOverColor,self.fontType,self.fontSize,self.align,True)
            # <=== I've put literal values for borderwidth(1), align(center), and because you don't pass these parameters into the Menu __init__ method
            # and they are needed to create your menu buttons.  I put visible at True, because if the Menu has a visible property of False then the buttons will not be drawn anyways so best to just leave tehm as visible.
            # Also used self.colour for the button color but not sure that that is what you mean it to be.  Your menu class needs to know both the menu colors and the button colors
            # another similiar example is there is a border for both the menu and the buttons.  So you need a border width parameter for both.  Since we are in the menu class I would just call this one borderWidth and call the other one borderWidthButton or something like that
            buttonLst.append(newBtn)
        return buttonLst


    def draw(self,win):
        if self.visible:
            if self.border:
                pygame.draw.rect(win,self.borderColor,self.rect,self.borderWidth)   
            for btn in self.buttons:
                btn.draw(win)

    def isOver(self,mp):
        if self.visible:
            for btn in self.buttons:
                return pygame.Rect(btn[0]).collidepoint(mp)

    def changebtnColour(self,i,clr):
        self.buttons[i].color = clr

#--------LABEL CONTROL -----------------------------------------------------------------------------------------------------

class Label(object):

    itemData = None
    backColor = None   # I've put this here because 99.9% of the time we want the back color to be transparent

    def __init__(self,text,rect,align='left',textColor=(0,0,0),borderColor=(0,0,0),borderWidth=0,fontSize = 15,fontType = 'arialrounded',visible=True):
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        self.rect = rect
        self.text = text
        self.align = align
        self.textColor = textColor
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.fontSize=fontSize
        self.fontType=fontType
        self.font = pygame.font.SysFont(fontType, fontSize)
        self.visible = visible

    def draw(self,win):
        gap = 0
        if self.visible == True:
            if self.borderWidth > 0:
                #draw border rectangle
                pygame.draw.rect(win,self.borderColor,self.rect,self.borderWidth)
            #draw text
            txtSurface = self.font.render(self.text,True,self.textColor,self.backColor)
            win.blit(txtSurface,self.alignText(txtSurface))

    def setFont(self,fontType,fontSize):
        self.fontSize = fSize
        self.fontType = fType
        self.font = pygame.font.SysFont(fontType, fontSize)

    def setFontSize(self,fSize):
        self.fontSize = fSize
        self.font = pygame.font.SysFont(self.fontType, fSize)

    def setFontType(self,fType):
        self.fontType = fType
        self.font = pygame.font.SysFont(fType, self.fontSize)

    def alignText(self,txtSurf):  # assumes vertical alignment of center for all
        y = self.y + (self.height - txtSurf.get_height()) // 2
        if self.align == 'left':
            x = self.x + self.borderWidth + 1
        elif self.align == 'right':
            x = self.x + (self.width - txtSurf.get_width() - self.borderWidth - 1)
        elif self.align == 'center':
            x = self.x + (self.width - txtSurf.get_width()) // 2
        return (x,y)

# ---------BUTTON CONTROL --------------------------------------------------------------------------------------------------

class Button(Label):

    itemData = None

    def __init__(self, text, rect, color=(255,255,255), textColor=(0,0,0), borderColor=(0,0,0), borderWidth=2, mouseOverColor=(255,0,0), fontType='arialrounded', fontSize=12, align='center', visible=True):
        Label.__init__(self,text,rect,textColor=textColor,fontSize=fontSize,fontType=fontType, align=align)
        self.color = color
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.mouseOverColor = mouseOverColor
        self.visible = visible
    def draw(self, win):
        if self.visible:
            mp = pygame.mouse.get_pos()
            mouseOver = self.isOver(mp)
            # note I'm drawing a large filled rectangle and then a smaller one inside of it  rather than an outline for the border as I don't like how the later method removes pixels in the corners
            if mouseOver:  # draw a thicker border.
                pygame.draw.rect(win,self.mouseOverColor,(self.x - self.borderWidth, self.y - self.borderWidth, self.width + self.borderWidth*2, self.height + self.borderWidth*2))   # drwws the borderColor
                pygame.draw.rect(win,self.color,(self.x + self.borderWidth,self.y+self.borderWidth,self.width - self.borderWidth*2,self.height - self.borderWidth*2))
                bText = self.font.render(self.text, True, self.mouseOverColor)
            else:  # draw a normal border
                pygame.draw.rect(win,self.borderColor,self.rect)
                pygame.draw.rect(win,self.color,(self.x + self.borderWidth,self.y+self.borderWidth,self.width - self.borderWidth*2,self.height - self.borderWidth*2))
                bText = self.font.render(self.text, True, self.textColor)
            xyPos = self.alignText(bText)
            win.blit(bText,xyPos)

    def isOver(self,mp):
        if self.visible:
            return pygame.Rect(self.rect).collidepoint(mp)

# ---------Textbox CONTROL --------------------------------------------------------------------------------------------------

class TextBox():

    clickTime = 0
    lastClick = 0

    def __init__(self, rect, txtColor=(0,0,0), fillColor=(255,255,255), borderColor=(105,105,105), borderWidth=2, fontType=DF_fontType,
                 fontSize=DF_fontSize,focusColor=(0,0,0),validKeys=string.printable,locked=False,visible=True):
        self.rect = rect
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        self.txtColor = txtColor
        self.fillColor = fillColor
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.fontType = fontType
        self.fontSize = fontSize
        self.hasFocus = False
        self.tabIndex = 0
        self.text = ''
        self.focusColor = focusColor
        self.validKeys = validKeys
        self.textSelected = False
        self.locked = locked
        self.visible = visible

    def isOver(self,mp):
        if self.visible:
            return pygame.Rect(self.rect).collidepoint(mp)

    def draw(self,win):
        if self.visible:
            xMargin = int(self.fontSize * .4)   # distance to indent text from the left & right border
            if self.hasFocus:
                pygame.draw.rect(win, self.focusColor, (self.x - self.borderWidth, self.y - self.borderWidth, self.width + self.borderWidth*2, self.height + self.borderWidth*2))
            else:
                pygame.draw.rect(win, self.borderColor, self.rect)
            pygame.draw.rect(win, self.fillColor,(self.x + self.borderWidth, self.y + self.borderWidth, self.width - self.borderWidth * 2, self.height - self.borderWidth * 2))
            blitX = self.x + self.borderWidth + xMargin
            if len(self.text) != 0:
                fontobject = pygame.font.SysFont(self.fontType, self.fontSize)
                if self.textSelected:
                    input_surface = fontobject.render(self.text, True, (255,255,255),(30,144,255))   # using white text and blue back for selected text,
                else:
                    input_surface = fontobject.render(self.text, True, self.txtColor)
                blitY = self.y + (self.height - input_surface.get_height()) // 2 + 1
                if blitX + input_surface.get_width() > self.x + self.width - (self.borderWidth + xMargin):
                    xOffSet = (blitX + input_surface.get_width()) - (self.x + self.width - (self.borderWidth + xMargin))
                    input_surface = input_surface.subsurface((xOffSet,0,input_surface.get_width()-xOffSet,input_surface.get_height()))
                win.blit(input_surface,(blitX,blitY))

    def update(self,event):
        if self.visible:
            if not self.locked:
                if self.hasFocus:
                    if event.type == pygame.KEYDOWN:
                        keyPressed = event.unicode
                        if keyPressed in self.validKeys:
                            self.text += keyPressed
                        elif event.key == pygame.K_BACKSPACE:
                            if self.textSelected:
                                self.text = ''
                                self.textSelected = False
                            else:
                                self.text = self.text[:-1]
                        elif event.key == pygame.K_RETURN:
                            self.hasFocus = False
                            return True  # will return True when enter pressed to signify completion of entering

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mp = pygame.mouse.get_pos()
                    if self.isOver(mp):
                        self.hasFocus = True
                        #print( time.time(), self.lastClick )
                        if time.time() - self.lastClick  < .4:  #0.4 seconds used to check for double click good?
                            # this is a double click
                            self.textSelected = True
                            self.lastClick = 0
                            #print('double click')
                        else:
                            self.lastClick = time.time()
                            self.textSelected = False
                    else:
                        self.hasFocus = False
        return False

# ---------Combobox CONTROL --------------------------------------------------------------------------------------------------

class ComboBox():
    def __init__(self, rect,labeltxt, txtLst, simple=True, txtColor=(0,0,0), fillColor=(255,255,255), borderColor=(105,105,105), borderWidth=2, fontType=DF_fontType,fontSize=DF_fontSize,focusColor=(0,0,0),visible=True,):
        self.rect = rect
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        self.txtColor = txtColor
        self.fillColor = fillColor
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.labeltxt = labeltxt
        self.txtLst = txtLst
        self.fontType = fontType
        self.fontSize = fontSize
        self.visible = visible
        self.label = self.loadLabel()
        self.textBox = self.loadtextBox()
        self.Dropbutton = self.loadDropbutton()
        self.menu = self.loadMenu()
        self.dropbtnclicked = False
        self.simple = simple
    def loadLabel(self):
        newY = self.y - 20
        label = Label(self.labeltxt+':', (self.x,newY,self.width,self.height))
        return label
    def loadtextBox(self):
        newW = self.width * 0.8
        txtBox = TextBox((self.x, self.y, newW, self.height), self.txtColor)
        return txtBox
    def loadDropbutton(self):
        newX = int(self.x + (self.width * 0.8))
        newW = int(self.width * 0.2)
        Dropbutton = Menu((newX, self.y, newW, int(self.height)),1,1,["\/"],2, True,(137,207,240))
        return Dropbutton
    def loadMenu(self):
        newW = self.width * 0.8
        rows = len(self.txtLst)
        newY = self.y + self.height
        newH = self.height * rows
        menu = Menu((self.x,newY,newW,newH),rows,1,self.txtLst,0, border=True)
        return menu

    def update(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mp = pygame.mouse.get_pos()
            dropbtnIndex = self.Dropbutton.getCellIndex(mp)
            if dropbtnIndex != -1:
                    self.dropbtnclicked = True
            menuBtnIndex = self.menu.getCellIndex(mp)
            if menuBtnIndex != -1:
                comboText = self.txtLst[menuBtnIndex]
                self.textBox.text = comboText
                self.dropbtnclicked = False  
        if not self.simple:
            self.textBox.update(event)
    def draw(self,win):
        if self.visible:
            comboBox = [self.label,self.textBox,self.Dropbutton]
            for obj in comboBox:
                obj.draw(win)
            if self.dropbtnclicked:
                self.menu.draw(win)
                



#-----------------------------------------#
#   VARIABLE AND OBJECT INITIALIZATION    #
#-----------------------------------------#

def redraw_game_window(win,controls,bckgroundColourIndex):
    win.fill(GREY)
    if bckgroundColourIndex == 0: #change background color based on what clour the user chooses
        win.fill(PURPLE)
    elif bckgroundColourIndex == 1:
        win.fill(RED)
    elif bckgroundColourIndex == 2:
        win.fill(BLUE)
    elif bckgroundColourIndex == 3:
        win.fill(ORANGE)
    for control in controls:
        control.draw(win)

    pygame.display.update()


def main():

    # create window
    win = pygame.display.set_mode((640,640))
    pygame.display.set_caption('Grid by Nahal H.')

    titleLabel= Label("Nahal's Controls", (0,40,640,30), align='center',textColor=(244,194,194),fontSize=70)
    
    gridtest = Grid((50,100,200,200),6,4,10,border=True,simple=False)
    menuTest = Menu((300,100,200,200),3,1,['text0','text1','text2'],10, border=True)   
    menuTest.changebtnColour(1,(137,207,240))                                                                                               
                                                                    
    testBtn = Button("Test Button",(50,325,150,50),color=(217,244,237))
    testBtn2 = Button("Test Button 2",(300,325,150,50),align='right',textColor=(0,0,255),borderWidth = 4,fontSize=20)
    testBtn2.setFontType('script')
    
    label1 = Label('Enter age:', (50,375,150,30))
    label2 = Label('Enter name:', (300,375,150,30))
   
    txtAge = TextBox((50,400,150,30), txtColor=(0,103,0), fillColor=(255,255,204))
    txtAge.validKeys = string.digits

    txtFirstName = TextBox((300,400,150,30), fillColor=(220,220,220))
    txtFirstName.hasFocus = True

    TestComboBox = ComboBox((50,500,150,30), "Favourite Color", ['Purple','Red','Blue','Orange'], True) #=> simple comboBox
    TestComboBox2 = ComboBox((300,500,150,30), "Favourite Sport", ['hockey','soccer','volleyball'], False)  #=> non simple comboBox

   
    controls = [titleLabel,gridtest,menuTest,testBtn,testBtn2,label1,label2,txtAge,txtFirstName,TestComboBox,TestComboBox2]

    inPlay = True
    bckgroundColourIndex = -1
    while inPlay:
        redraw_game_window(win,controls,bckgroundColourIndex)
        pygame.display.update()
        pygame.time.delay(20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inPlay = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inPlay = False
            #  SHOW ME THAT YOUR CONTROLS WORK, DON'T JUST PRINT THE MOUSE POSITION  - Example show me that you can determin what button you clicked on in your menu - hint: use your getCellIndex method
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickPos = pygame.mouse.get_pos()
                gridBtnIndex = gridtest.getCellIndex(clickPos)
                if gridBtnIndex != -1:
                    surroundingCells = gridtest.surroundingCells(gridBtnIndex)
                    print('you clicked on cell',gridBtnIndex,'. The surrounding cells are:',surroundingCells)
##                gridtest.x += 10                    #  <=== this line is working but the grid is not moving, can you figure out why
##                print(gridtest.x)                    # <===  I added this line to show that the x attribute is changing  - this problem demonstrates why allowing direct access to attributes withoug going thru a method is not always good.

                bckgroundColourIndex = TestComboBox.menu.getCellIndex(clickPos)
            if event.type == pygame.MOUSEBUTTONUP:
                #print('mouse up')
                pass
            if event.type == pygame.MOUSEMOTION:
                mp = pygame.mouse.get_pos()
            txtFirstName.update(event)
            txtAge.update(event)
            TestComboBox.update(event)
            TestComboBox2.update(event)
            gridtest.update(event)
    


    pygame.quit()

if __name__ == "__main__":
    main()
