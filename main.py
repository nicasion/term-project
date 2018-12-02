####################################
# Name: Nicasio Ng
# Section: H
# AndrewID: jianengn
# Mentor: Kusha
####################################

## MAIN GAME FILE ##

# Citations: 112 Course Website for Tkinter starter code
# http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

from tkinter import *
import pyautogui
import math
import random
import PIL

from Map import Map

####################################
# core animation code
####################################

def init(data):
    data.gameState = "startscreen"
    
    # initialize map
    data.map = Map("Player1") 
    
    # for images to follow mouse movement (calculation)
    data.smallBoxWidth = 800/22 
    data.smallBoxHeight = 534/22
    
    # images
    data.imageCurrent = None # holder for next image, intialize at None

    data.imageLogo = PhotoImage(file="title.png")
    data.imagePower = PhotoImage(file="wind.png")
    data.imageWater = PhotoImage(file="water.png")
    data.imageTree = PhotoImage(file="tree.png")
    data.imageConstruction = PhotoImage(file='construction3.png')
    data.imageClose = PhotoImage(file="close.png")
    data.imageGraph = PhotoImage(file="graph2.png")
    
    # General game data to keep track of
    data.population = 0
    data.budget = 10000
    data.timer = 0
    data.calendar = 1
    data.monthlyExpense = 0
    data.monthlyIncome = 0
    
    data.temporaryValue = False # refreshes at timerFired
    
    # Specific Data
    data.constructionCost = {'imagePower':100,'imageWater':50,'imageTree':20, 'zoning':0}
    data.monthlyCost = {'imagePower':10,'imageWater':5,'imageTree':2,'zoning':0}
    
    
    # sequence in dictionary[key] = budget,monthlyExpense,population
    data.snapshot = {1:[10000,0,0]}
    
    
    # UI coordinates (start screen)
    data.coordinatesStart = [(data.width/2-100,data.height/2,data.width/2+100,data.height/2+50)]
    
    # UI coordinates (play game): Build,NonBuild,Stats (BUTTONS)
    data.coordinatesBuild = [(10,10,90,30,"imagePower"),(10,40,90,60,"imageWater"),(10,70,90,90,"imageTree")]
    
    # MAIN ADD AREA!!!
    data.coordinatesNonBuild = [(10,100,90,120,"zoning",200,3,None,"limegreen","Residential","imageTree",'lightblue','Commerical',None,'yellow','Industrial')]
    # 5th pos = length, 6th pos = count of object, 7th = "imagefile", 8th = color of layer, 9th = text, 10th = repeat 7th for next set...
    data.coordinatesStats = [(120,660,200,680,'budget'),(220,660,340,680,'monthlyExpense')]
        
    # Coordinates for Menu
    data.menuBgAbove = {}
    for coordinate in data.coordinatesStats:
        key = coordinate[4]
        data.menuBgAbove[key] = (coordinate[0],450,coordinate[0]+280,450+200)
    
    data.menuBgSide = {}
    for coordinate in data.coordinatesNonBuild:
        key = coordinate[4]
        data.menuBgSide[key] = (110,coordinate[1]-coordinate[5]/2,110+200,coordinate[1]+coordinate[5]/2,coordinate[6])
        cycle = int((len(coordinate) - 7)/3)
        for i in range(cycle):
            data.menuBgSide[key] += (coordinate[7+(i*3)],coordinate[8+(i*3)],coordinate[9+(i*3)])

    # update menuOptionChecker!!! based on data in non-build)
    data.menuOptionChecker = {}
    for key in data.menuBgSide.keys():
        count = data.menuBgSide[key][4]
        for num in range(count):
            rx1 = data.menuBgSide[key][0]+15
            ry1 = data.menuBgSide[key][1]+15+(num*(15+50))
            rx2 = data.menuBgSide[key][0]+15+50
            ry2 = data.menuBgSide[key][1]+(num+1)*(15+50)
            if key in data.menuOptionChecker.keys():
                data.menuOptionChecker[key] += [(rx1,ry1,rx2,ry2,data.menuBgSide[key][5+(num*3)])]
            else:
                data.menuOptionChecker[key] = [(rx1,ry1,rx2,ry2,data.menuBgSide[key][5+(num*3)])]
    
    data.menuCurrent = None
    data.currentButton = None
    

# to check if clicked on button (for UI)
def checkButtonClick(clickX,clickY,buttonCoordinates,data):
    if buttonCoordinates[0] <= clickX <= buttonCoordinates[2] and \
        buttonCoordinates[1] <= clickY <= buttonCoordinates[3]:
        return True
    return False

# MOUSE
def mousePressed(event, data):
    if data.gameState == "startscreen":
        for button in data.coordinatesStart:
            if checkButtonClick(event.x,event.y,button,data):
                data.gameState = 'play'
    
    elif data.gameState == "play":
        # check for button click (build menu)
        for button in data.coordinatesBuild:
            if checkButtonClick(event.x,event.y,button,data):
                # if button is clicked, store button info in imagecurrent
                data.imageCurrent = button[4]
    
        # check for button click (non-build menu)
        for button in data.coordinatesNonBuild:
            if checkButtonClick(event.x,event.y,button,data):
                data.imageCurrent = None
                # if button is clicked, store button info in currentbutton
                data.currentButton = button[4]
                data.menuCurrent = data.menuBgSide[button[4]]

        # check for button click (stats menu)
        for button in data.coordinatesStats:
            if checkButtonClick(event.x,event.y,button,data):
                data.imageCurrent = None
                # if button is clicked, store button info in currentbutton
                data.currentButton = button[4]
                data.menuCurrent = data.menuBgAbove[button[4]]
        
        if data.menuCurrent != None:
            # check for clicks on menu options only when specific menu is open
            # for build menu only (not for stat)
            if data.currentButton in data.menuOptionChecker.keys():
                for coordinate in data.menuOptionChecker[data.currentButton]:
                    if checkButtonClick(event.x,event.y,coordinate,data):
                        data.imageCurrent = coordinate[4]
            
            # checks if 'close' button in menu option is clicked = close menu
            if checkButtonClick(event.x,event.y,(data.menuCurrent[2]-12,data.menuCurrent[1]+2,data.menuCurrent[2]-2,data.menuCurrent[1]+14),data):
                data.menuCurrent = None
                data.currentButton = None
            
            

        # check for grid click only if there is an existing imagecurrent
        if data.imageCurrent != None:
            data.temporaryValue = data.map.mousePressAction(event.x,event.y,data.imageCurrent)
            if data.temporaryValue == True:
                cost = data.constructionCost[data.imageCurrent]
                data.budget -= cost
                data.monthlyExpense += data.monthlyCost[data.imageCurrent]


def keyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym == "Up":
        print (data.map.gridContent)
    if event.keysym == "Down":
        print (data.snapshot)
    if event.keysym == 'Left':
        print (data.currentButton)
    pass



def timerFired(data):
    if data.gameState == 'play':
        data.mouseX, data.mouseY = pyautogui.position()
        data.timer += 1
        data.temporaryValue = False
        if data.timer % 100 == 0:
            data.calendar += 1
            data.budget -= data.monthlyExpense
            data.snapshot[data.calendar] = [data.budget,data.monthlyExpense,data.population]



def redrawAll(canvas, data):
    # for start screen
    if data.gameState == 'startscreen':
        canvas.create_image(data.width/6,data.height/4,anchor=NW, image=data.imageLogo)
        canvas.create_rectangle(data.width/2-100,data.height/2,data.width/2+100,data.height/2+50,fill="yellow")
        canvas.create_text(data.width/2-50,data.height/2+13,text="Start Game",anchor=NW,font="Arial 20")
    
    # for actual gameplay
    if data.gameState == "play":
        data.map.draw(canvas) # draws the map... from Map.py
        
        # UI (right corner)
        canvas.create_rectangle(790,15,860,40,fill="white") # box for 'day'
        canvas.create_text(800,20,text="Day %s"%(str(data.calendar)),anchor=NW)
        canvas.create_text(790,50,text="Budget = %d"%(data.budget),anchor=NW)
        canvas.create_text(790,70,text="Population = %d"%(data.population),anchor=NW)
        canvas.create_text(790,90,text="Monthly Expense = %d"%(data.monthlyExpense),anchor=NW)
            
        # UI (build menu)
        canvas.create_rectangle(0,0,100,data.height,fill='lightgrey',
            outline='lightgrey')
        for rectangle in data.coordinatesBuild:
            canvas.create_rectangle(rectangle[0],rectangle[1],rectangle[2],
                rectangle[3],fill='white')
        canvas.create_text(30,13,text="Power",anchor=NW)
        canvas.create_text(30,43,text="Water",anchor=NW)
        canvas.create_text(28,73,text="Nature",anchor=NW)
        
        # UI (non-build menu)
        for rectangle in data.coordinatesNonBuild:
            canvas.create_rectangle(rectangle[0],rectangle[1],rectangle[2],
                rectangle[3],fill='white')
        canvas.create_text(28,103,text="Zoning",anchor=NW)

    
        # UI (stats/non-build menu)
        canvas.create_rectangle(0,650,data.width,data.height,fill="grey",
            outline='grey')
        for rectangle in data.coordinatesStats:
            canvas.create_rectangle(rectangle[0],rectangle[1],rectangle[2],
                rectangle[3],fill='white')
        
        
        canvas.create_text(137,663,text="Budget",anchor=NW)
        canvas.create_text(227,663,text="Monthly Expense",anchor=NW)
        
        
        
        
        # hardcoded adjustments for specific images for following of mouse movement
        # this must be also updated along with the one stored in Map.py
        def drawImageCalibrated(input,x1,y1): 
            if input == None: pass
            elif input == "imagePower":
                canvas.create_image(x1,y1+4,anchor=SW, image=data.imagePower)
            elif input == "imageWater":
                canvas.create_image(x1+3,y1+9,anchor=SW, image=data.imageWater)
            elif input == "imageTree":
                canvas.create_image(x1+7,y1+2,anchor=SW, image=data.imageTree)
            elif input == "imageConstruction":
                canvas.create_image(x1+3,y1+8,anchor=SW, image=data.imageConstruction)
                
        # follows mouse movement
        if data.imageCurrent != None:
            if not (data.mouseX <= 100 or data.mouseY >= 690):
            # when hovering over UI sidemenu, image that follows mouse movement disappears
                x1 = data.mouseX-6 - data.smallBoxWidth/2
                y1 = data.mouseY-51 
                x2 = x1 + data.smallBoxWidth/2
                y2 = y1 + data.smallBoxHeight/2
                x3 = x1 + data.smallBoxWidth
                y3 = y1
                x4 = x2
                y4 = y2 - data.smallBoxHeight
                canvas.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4,fill="orange")
                drawImageCalibrated(data.imageCurrent,x1,y1)

        
        # menu BG
        if data.menuCurrent != None:
            canvas.create_rectangle(data.menuCurrent[0],data.menuCurrent[1],data.menuCurrent[2],data.menuCurrent[3],fill="lightgrey")
            canvas.create_image(data.menuCurrent[2]-
2,data.menuCurrent[1]+2,anchor=NE, image=data.imageClose)
            # menu BG for non-build
            if data.currentButton in data.menuBgSide.keys():
                count = data.menuCurrent[4]
                for num in range(count):
                    rx1 = data.menuCurrent[0]+15
                    ry1 = data.menuCurrent[1]+15+(num*(15+50))
                    rx2 = data.menuCurrent[0]+15+50
                    ry2 = data.menuCurrent[1]+(num+1)*(15+50)
                    canvas.create_rectangle(rx1,ry1,rx2,ry2,fill='white')
                    
                    x1 = data.menuCurrent[0]+22
                    y1 = data.menuCurrent[1]+50+(num*(15+50))
                    x2 = x1 + data.smallBoxWidth/2
                    y2 = y1 + data.smallBoxHeight/2
                    x3 = x1 + data.smallBoxWidth
                    y3 = y1
                    x4 = x2
                    y4 = y2 - data.smallBoxHeight
                    canvas.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4,fill=data.menuCurrent[6+(num*3)])
                    if data.menuCurrent[5+(num*3)] != None:
                        drawImageCalibrated(data.menuCurrent[5+(num*3)],x1,y1)
                    canvas.create_text((rx2+data.menuCurrent[2])/2,ry1,text=data.menuCurrent[7+(num*3)],anchor=N)


            # menu BG for stats
            if data.currentButton in data.menuBgAbove.keys():
                canvas.create_image(data.menuCurrent[2]-19,data.menuCurrent[1]+8,anchor=NE, image=data.imageGraph)
                canvas.create_text(data.menuCurrent[0]+34,data.menuCurrent[1]+4,text=data.currentButton,anchor=NW)
                canvas.create_text(data.menuCurrent[2]-44,data.menuCurrent[3],text="time",anchor=SE)
            
            
                # retrieving from snapshot values, assign position for retrieval
                if data.currentButton == "budget": pos = 0
                elif data.currentButton == "monthlyExpense": pos = 1
                elif data.currentButton == "population": pos = 2
                
                # plot graph
                plotGraphData = []
                for dataPoint in data.snapshot.values():
                    plotGraphData += [dataPoint[pos]]
                maxValue = max(plotGraphData)
                minValue = min(plotGraphData)
                dataCount = len(plotGraphData)
                difference = maxValue - minValue
                horizontalSpacing = (data.menuCurrent[2]-data.menuCurrent[0]-28)/dataCount
                if difference == 0: difference = 1
                verticalSpacing = (data.menuCurrent[3]-data.menuCurrent[1]-48)/difference
                for x in range(len(plotGraphData)):
                    y = plotGraphData[x]
                    xPos = x*horizontalSpacing + 32 + data.menuCurrent[0]
                    yPos = (maxValue - y)*verticalSpacing + 20 + data.menuCurrent[1]
                    canvas.create_oval(xPos,yPos,xPos+5,yPos+5,fill='black')




####################################
# use the run function as-is
####################################

def run(width=300, height=300):

    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1000, 700)