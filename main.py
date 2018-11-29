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
    data.imageLogo = PhotoImage(file="title.png")
    data.imageCurrent = None # holder for next image, intialize at None
    data.imagePower = PhotoImage(file="wind.png")
    data.imageWater = PhotoImage(file="water.png")
    data.imageTree = PhotoImage(file="tree.png")
    data.imageConstruction = PhotoImage(file='construction3.png')
    data.imageClose = PhotoImage(file="close.png")
    data.imageGraph = PhotoImage(file="graph2.png")

    
    # other data to keep track of
    data.population = 0
    data.budget = 10000
    data.timer = 0
    data.click = False
    data.clickedLst = []
    data.calendar = 1
    data.temporaryValue = False
    
    # UI coordinates
    data.coordinatesStart = [(data.width/2-100,data.height/2,data.width/2+100,data.height/2+50)]
    data.coordinatesUI = [(10,10,90,30,"imagePower"),(10,40,90,60,"imageWater"),(10,70,90,90,"imageTree"),(10,100,90,120,"zoning")]
    data.coordinatesNonBuild = [(120,660,200,680,'budget'),(220,660,340,680,'monthlyExpense')]
    data.menuBg = {'budget':(120,450,400,650),'monthlyExpense':(220,450,500,650)}
    data.menuCurrent = None
    data.currentButton = None
    
    # Specific Data
    data.constructionCost = {'imagePower':100,'imageWater':50,'imageTree':20, 'zoning':0}
    data.monthlyCost = {'imagePower':10,'imageWater':5,'imageTree':2,'zoning':0}
    
    data.monthlyExpense = 0
    data.monthlyIncome = 0
    
    # sequence in dictionary[key] = budget,monthlyExpense,population
    data.snapshot = {1:[10000,0,0]}
    

# to check if clicked on button (for UI)
def checkButtonClick(clickX,clickY,buttonCoordinates,data):
    if buttonCoordinates[0] <= clickX <= buttonCoordinates[2] and \
        buttonCoordinates[1] <= clickY <= buttonCoordinates[3]:
        return True
    return False

def mousePressed(event, data):
    if data.gameState == "startscreen":
        for button in data.coordinatesStart:
            if checkButtonClick(event.x,event.y,button,data):
                data.gameState = 'play'
    
    elif data.gameState == "play":
        # check for button click
        for button in data.coordinatesUI:
            if checkButtonClick(event.x,event.y,button,data):
                data.imageCurrent = button[4]
        
        for button in data.coordinatesNonBuild:
            if checkButtonClick(event.x,event.y,button,data):
                data.imageCurrent = None
                data.currentButton = button[4]
                data.menuCurrent = data.menuBg[data.currentButton]
        
        if data.menuCurrent != None:
            if checkButtonClick(event.x,event.y,(data.menuCurrent[2]-12,data.menuCurrent[1]+2,data.menuCurrent[2]-2,data.menuCurrent[1]+14),data):
                data.menuCurrent = None


        # check for grid click
        if data.imageCurrent != None:
            data.temporaryValue = data.map.mousePressAction(event.x,event.y,data.imageCurrent)
            if data.temporaryValue == True:
                cost = data.constructionCost[data.imageCurrent]
                data.budget -= cost
                data.monthlyExpense += data.monthlyCost[data.imageCurrent]
                
            # data.imageCurrent = None

def keyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym == "Up":
        print (data.map.gridContent)
    if event.keysym == "Down":
        print (data.snapshot)
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
    if data.gameState == 'startscreen':
        canvas.create_image(data.width/6,data.height/4,anchor=NW, image=data.imageLogo)
        canvas.create_rectangle(data.width/2-100,data.height/2,data.width/2+100,data.height/2+50,fill="yellow")
        canvas.create_text(data.width/2-50,data.height/2+13,text="Start Game",anchor=NW,font="Arial 20")
    
    if data.gameState == "play":
        # draw in canvas
        data.map.draw(canvas)
        
        canvas.create_rectangle(790,15,860,40,fill="white") 
        
        # text labels
        canvas.create_text(790,70,text="Population = %d"%(data.population),anchor=NW)
        canvas.create_text(790,50,text="Budget = %d"%(data.budget),anchor=NW)
        canvas.create_text(790,90,text="Monthly Expense = %d"%(data.monthlyExpense),anchor=NW)

        canvas.create_text(800,20,text="Day %s"%(str(data.calendar)),anchor=NW)
            
        # UI
        canvas.create_rectangle(0,650,data.width,data.height,fill="grey",
            outline='grey')
        canvas.create_rectangle(0,0,100,data.height,fill='lightgrey',
            outline='lightgrey')
        
        for rectangle in data.coordinatesUI:
            canvas.create_rectangle(rectangle[0],rectangle[1],rectangle[2],
                rectangle[3],fill='white')
        for rectangle in data.coordinatesNonBuild:
            canvas.create_rectangle(rectangle[0],rectangle[1],rectangle[2],
                rectangle[3],fill='white')
        
        # menu BG
        if data.menuCurrent != None:
            canvas.create_rectangle(data.menuCurrent[0],data.menuCurrent[1],data.menuCurrent[2],data.menuCurrent[3],fill="lightgrey")
            canvas.create_image(data.menuCurrent[2]-2,data.menuCurrent[1]+2,anchor=NE, image=data.imageClose)
            canvas.create_image(data.menuCurrent[2]-19,data.menuCurrent[1]+8,anchor=NE, image=data.imageGraph)
            canvas.create_text(data.menuCurrent[0]+34,data.menuCurrent[1]+4,text=data.currentButton,anchor=NW)
            canvas.create_text(data.menuCurrent[2]-44,data.menuCurrent[3],text="time",anchor=SE)

                        
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
                
                    
            
        canvas.create_text(30,13,text="Power",anchor=NW)
        canvas.create_text(30,43,text="Water",anchor=NW)
        canvas.create_text(28,73,text="Nature",anchor=NW)
        canvas.create_text(28,103,text="Zoning",anchor=NW)
        
        canvas.create_text(137,663,text="Budget",anchor=NW)
        canvas.create_text(227,663,text="Monthly Expense",anchor=NW)


        
        # hardcoded adjustments for specific images
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