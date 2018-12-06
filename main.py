####################################
# Name: Nicasio Ng
# Section: H
# AndrewID: jianengn
# Mentor: Kusha
####################################

## MAIN GAME FILE ##

# Citations: 112 Course Website for Tkinter starter code
# http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

# Images: I don't own any of the images used, except the title on the startscreen.

####################################
# import modules/libraries
####################################

from tkinter import *
import pyautogui
import math
import random
import copy
import shelve
from PIL import Image
from PIL import ImageTk

####################################
# import my code in another file
####################################

from Map import Map

####################################
# core animation code
####################################

def init(data):
    # OVERALL
    data.gameState = "startscreen"
    
    # MAP
    data.map = Map("Player1") 
    data.map.randomMapGeneration()
    
    # Simulate player2
    data.map2 = Map("Player2") 
    data.map2.randomMapGeneration()

    
    # for images to follow mouse movement (hardcoded based on Map.py)
    data.smallBoxWidth = 800/22 
    data.smallBoxHeight = 534/22
    
    # IMAGES
    # start screen
    data.imageLogo = PhotoImage(file="title.png")
    # play: stats
    data.imageClose = PhotoImage(file="close.png")
    data.imageGraph = PhotoImage(file="graph2.png")
    # play: objects (to load into Map.py)
    data.imagePower = PhotoImage(file="wind.png")
    data.imageWater = PhotoImage(file="water.png")
    data.imageTree = PhotoImage(file="tree.png")
    data.imageConstruction = PhotoImage(file='construction3.png')
    im1 = Image.open("apartment.png")
    im1.thumbnail((45,45))
    data.imageApartment = ImageTk.PhotoImage(im1)
    im2 = Image.open("cabin2.png")
    im2.thumbnail((35,35))
    data.imageCabin = ImageTk.PhotoImage(im2)
    im3 = Image.open("store2.png")
    im3.thumbnail((35,35))
    data.imageStore = ImageTk.PhotoImage(im3)
    im4 = Image.open("industry2.png")
    im4.thumbnail((35,35))
    data.imageIndustry = ImageTk.PhotoImage(im4)
    im5 = Image.open("bulldoze.png")
    im5.thumbnail((25,25))
    data.imageDemolish = ImageTk.PhotoImage(im5)
    
    # GAME DATA
    data.temporaryValue = False # refreshes at timerFired 
    data.timer = 0
    data.imageCurrent = None # holder for next image, intialize at None
    data.colorGrid = None
    data.menuCurrent = None
    data.currentButton = None
    # stats shown (stored here in main.py)
    data.calendar = 1
    # stats stored in Map.py: Population Budget MonthlyExpense MonthlyIncome
    
    # object data
    data.constructionCost = {'imagePower':100,'imageWater':50,'imageTree':20, 'ZoningResidential':0,'ZoningCommercial':0,'ZoningIndustrial':0}
    data.monthlyCost = {'imagePower':10,'imageWater':5,'imageTree':2,'ZoningResidential':0,'ZoningCommercial':0,'ZoningIndustrial':0}

    # USER INTERFACE 
    # coordinates (start screen)
    data.coordinatesStart = [(data.width/2-100,data.height/2,data.width/2+100,data.height/2+50,'start'),(data.width/2-100,data.height/2 +70,data.width/2+100,data.height/2+50+70,'load')]
    # coordinates (play game)
    # build -- click to build
    data.coordinatesBuild = [(10,10,90,30,"imagePower"),(10,40,90,60,"imageWater"),(10,70,90,90,"imageTree"),(10,100,90,120,'imageDemolish')]
    # direct function -- settings/anything that does not involve building/no menu
    data.coordinatesDirectFunction = [(790,115,860,140,'save')]
    # non-build -- intermediate button, click to expand menu
    # x1,y1,x2,y2,'button name',5=menu length,6=menu item count,
    # 7='item 1 imagefile',8='item 1 color',9='item 1 text', then repeat
    data.coordinatesNonBuild = [(10,100,90,120,"zoning",200,3,"ZoningResidential","olivedrab","Residential","imageTree",'lightblue','Commerical',"ZoningIndustrial",'yellow','Industrial')]
    # stats -- to show graphs etc
    data.statsCategory = ['budget','monthly expense','population']
    x1,y1 = (120,640)
    width,height,xSpacing,ySpacing = (80,20,20,10)
    data.coordinatesStats = []
    for num in range(len(data.statsCategory)):
        data.coordinatesStats += [((x1+num*(width+xSpacing),y1+num*(height+ySpacing),x1+num*(width+xSpacing),y1+num*(width+xSpacing)))]
    data.coordinatesStats = [(120,640,200,660,'budget'),(220,640,340,660,'monthly expense'),(360,640,480,660,'population')]
    
    # AUTOMATIC CALCULATION FOR MENU
    # menu coordinates (for bottom bar)
    data.menuBgAbove = {}
    for coordinate in data.coordinatesStats:
        key = coordinate[4]
        data.menuBgAbove[key] = (coordinate[0],450,coordinate[0]+280,450+200)
    # menu coordinates (for left bar)
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
                data.menuOptionChecker[key] += [(rx1,ry1,rx2,ry2,data.menuBgSide[key][5+(num*3)],data.menuBgSide[key][6+(num*3)])] # coordinates of rectangle, image, color
            else:
                data.menuOptionChecker[key] = [(rx1,ry1,rx2,ry2,data.menuBgSide[key][5+(num*3)],data.menuBgSide[key][6+(num*3)])]
    
    

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
                print (button[4])
                if button[4] == 'load':
                    saveGameShelfFile = shelve.open('savedGames')
                    if 'mapGridContent' in saveGameShelfFile:
                        data.map.gridContent = saveGameShelfFile['mapGridContent']
                        data.map2.gridContent = saveGameShelfFile['mapGridContent']
                        data.map.stats = saveGameShelfFile['mapStats']
                        data.map2.stats = saveGameShelfFile['mapStats']
                        data.map.snapshot = saveGameShelfFile['mapSnapshot']
                        data.map2.snapshot = saveGameShelfFile['mapSnapshot']



                        print ('loaded')
                    else:
                        print('error')
    
    elif data.gameState == "play" or data.gameState == 'play2':
        # need to check for budget requirements.
        
        # check for button click (direct functionalities)
        for button in data.coordinatesDirectFunction:
            if checkButtonClick(event.x,event.y,button,data):
                if button[4] == 'save':
                    saveGameShelfFile = shelve.open('savedGames')
                    saveGameShelfFile['mapGridContent'] = data.map.gridContent
                    saveGameShelfFile['map2GridContent'] = data.map2.gridContent
                    saveGameShelfFile['mapStats'] = data.map.stats
                    saveGameShelfFile['map2Stats'] = data.map2.stats
                    saveGameShelfFile['mapSnapshot'] = data.map.snapshot
                    saveGameShelfFile['map2Snapshot'] = data.map2.snapshot

                    print ('game saved')
                elif button[4] == 'demolish':
                    data.imageCurrent = button[4]
                        
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
                        data.colorGrid = coordinate[5]
            
            # checks if 'close' button in menu option is clicked = close menu
            if checkButtonClick(event.x,event.y,(data.menuCurrent[2]-12,data.menuCurrent[1]+2,data.menuCurrent[2]-2,data.menuCurrent[1]+14),data):
                data.menuCurrent = None
                data.currentButton = None
    
        # check for grid click only if there is an existing imagecurrent
        # link to Map Class OOP
        if data.imageCurrent != None:
            if data.gameState == 'play':
                data.temporaryValue = data.map.mousePressAction(event.x,event.y,data.imageCurrent,data.colorGrid)
            elif data.gameState == 'play2':
                data.temporaryValue = data.map2.mousePressAction(event.x,event.y,data.imageCurrent,data.colorGrid)

            if data.temporaryValue == True:
                cost = data.constructionCost[data.imageCurrent]
                if data.gameState == 'play':
                    data.map.stats['budget'] -= cost
                    data.map.stats['monthly expense'] += data.monthlyCost[data.imageCurrent]
                elif data.gameState == 'play2':
                    data.map2.stats['budget'] -= cost
                    data.map2.stats['monthly expense'] += data.monthlyCost[data.imageCurrent]


def keyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym == "Up":
        print ('start \n \n \n')
        print (data.map.stats)
        print ('end \n \n \n')
    if event.keysym == "Down":
        print ('start \n \n \n')
        print (data.map.snapshot)
        print ('end \n \n \n')

    if event.keysym == 'Left':
        print (data.currentButton)
    if event.keysym == 'a':
        print (data.colorGrid)
    if event.keysym == 'b':
        # pollution heat map
        for key in data.map.gridContent.keys():
            pollution = data.map.gridContent[key]['pollution']
            if pollution >= 45: data.map.gridContent[key]['temp'] = 'darkred'
            elif 30 <= pollution < 45: data.map.gridContent[key]['temp'] = 'red'
            elif 20 <= pollution < 30: data.map.gridContent[key]['temp'] = 'darkorange'
            elif 10 <= pollution < 20: data.map.gridContent[key]['temp'] = 'yellow'
            elif 0 <= pollution < 10: data.map.gridContent[key]['temp'] = 'springgreen'
    if event.keysym == '2':
        data.gameState = "play2"
        data.imageCurrent = None
    if event.keysym == '1':
        data.gameState = "play"
        data.imageCurrent = None


    pass



def timerFired(data):
    if data.gameState == 'play' or data.gameState == 'play2':
        data.mouseX, data.mouseY = pyautogui.position()
        data.timer += 1
        data.temporaryValue = False
        data.map.statsRefresh()
        data.map2.statsRefresh()
        if data.timer % 10 == 0: #100
            data.calendar += 1
            # if data.gameState == 'play':
            data.map.desirabilityConstruction()
            data.map.constructionStatus()
            data.map.pollutionSpread()
            data.map.stats['budget'] -= data.map.stats['monthly expense']
            data.map.updateSnapshot(data.calendar)

            # if data.gameState == 'play2':
            data.map2.desirabilityConstruction()
            data.map2.constructionStatus()
            data.map2.pollutionSpread()
            data.map2.stats['budget'] -= data.map2.stats['monthly expense']
            data.map2.updateSnapshot(data.calendar)



def redrawAll(canvas, data):
    # for start screen
    if data.gameState == 'startscreen':
        canvas.create_image(data.width/6,data.height/4,anchor=NW, image=data.imageLogo)
        canvas.create_rectangle(data.width/2-100,data.height/2,data.width/2+100,data.height/2+50,fill="yellow")
        canvas.create_text(data.width/2-50,data.height/2+13,text="Start Game",anchor=NW,font="Arial 20")
        canvas.create_rectangle(data.width/2-100,data.height/2+70,data.width/2+100,data.height/2+50+70,fill="yellow")
        canvas.create_text(data.width/2-50,data.height/2+13+70,text="Load Game",anchor=NW,font="Arial 20")



    # for actual gameplay
    if data.gameState == "play" or data.gameState == 'play2':
        # draws the map... from Map.py
        if data.gameState == 'play': 
            data.map.draw(canvas) 
        elif data.gameState == 'play2': 
            data.map2.draw(canvas) 
        
        # UI (right corner)
        canvas.create_rectangle(790,15,860,40,fill="white") # box for 'day'
        canvas.create_text(800,20,text="Day %s"%(str(data.calendar)),anchor=NW)
        if data.gameState == 'play': 
            canvas.create_text(790,50,text="Budget = %d"%(data.map.stats['budget']),anchor=NW)
            canvas.create_text(790,70,text="Population = %d"%(data.map.stats['population']),anchor=NW)
            canvas.create_text(790,90,text="Monthly Expense = %d"%(data.map.stats['monthly expense']),anchor=NW)
            canvas.create_text(790,150,text="Water Supply = %d"%(data.map.stats['water']),anchor=NW)
            canvas.create_text(790,170,text="Jobs = %d"%(data.map.stats['jobs']),anchor=NW)        
        elif data.gameState == 'play2': 
            canvas.create_text(790,50,text="Budget = %d"%(data.map2.stats['budget']),anchor=NW)
            canvas.create_text(790,70,text="Population = %d"%(data.map2.stats['population']),anchor=NW)
            canvas.create_text(790,90,text="Monthly Expense = %d"%(data.map2.stats['monthly expense']),anchor=NW)
            canvas.create_text(790,150,text="Water Supply = %d"%(data.map2.stats['water']),anchor=NW)
            canvas.create_text(790,170,text="Jobs = %d"%(data.map2.stats['jobs']),anchor=NW)


        
        # temp position- save button
        canvas.create_rectangle(790,115,860,140,fill="white")

            
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
        canvas.create_rectangle(0,630,data.width,data.height,fill="grey",
            outline='grey')
        for rectangle in data.coordinatesStats:
            canvas.create_rectangle(rectangle[0],rectangle[1],rectangle[2],
                rectangle[3],fill='white')
            canvas.create_text((rectangle[0]+rectangle[2])/2,rectangle[1]+3,text=rectangle[4],anchor=N)
        
        
        
        # hardcoded adjustments for specific images for following of mouse movement
        # this must be also updated along with the one stored in Map.py
        def drawImageCalibrated(input,x1,y1): 
            if input == None: pass
            elif input == "imagePower":
                # canvas.create_image(x1,y1+4,anchor=SW, image=data.imagePower)
                # canvas.create_image(x1,y1+8,anchor=SW, image=data.imageApartment)
                # canvas.create_image(x1+3,y1+11,anchor=SW, image=data.imageCabin) 
                # canvas.create_image(x1+1,y1+11,anchor=SW, image=data.imageStore) 
                # canvas.create_image(x1+1,y1+11,anchor=SW, image=data.imageIndustry)
                # canvas.create_image(x1+5,y1+11,anchor=SW, image=data.imageDemolish)  
                canvas.create_image(x1+1,y1+11,anchor=SW, image=data.imageTest) 

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
                color = 'orange'
                if data.colorGrid != None:
                    color = data.colorGrid
                canvas.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4,fill=color)
                try:
                    drawImageCalibrated(data.imageCurrent,x1,y1)
                except:
                    pass

        
        # menu BG (and menu options;for non-build only)
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
                # if data.currentButton == "budget": pos = 0
                # elif data.currentButton == "monthly Expense": pos = 1
                # elif data.currentButton == "population": pos = 2
                
                # plot graph
                plotGraphData = []
                if data.gameState == 'play': snapshot = data.map.snapshot
                elif data.gameState == 'play2': snapshot = data.map2.snapshot
                for key in snapshot.keys():
                    dataPoint = snapshot[key][data.currentButton]
                    plotGraphData += [dataPoint]
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