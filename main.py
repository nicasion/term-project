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
    
    # other data to keep track of
    data.population = 0
    data.budget = 100000
    data.timer = 0
    data.click = False
    data.clickedLst = []
    
    # UI coordinates
    data.coordinatesStart = [(data.width/2-100,data.height/2,data.width/2+100,data.height/2+50)]
    data.coordinatesUI = [(10,10,90,30,"imagePower"),(10,40,90,60,"imageWater"),(10,70,90,90,"imageTree"),(10,100,90,120,"Zoning")]

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
                data.click = "Button"
                data.imageCurrent = button[4]
        
        # check for grid click
        if data.imageCurrent != None:
            data.map.mousePressAction(event.x,event.y,data.imageCurrent)
            # data.imageCurrent = None

def keyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym == "Up":
        print (data.map.gridContent)
    pass

def timerFired(data):
    data.mouseX, data.mouseY = pyautogui.position()
    data.timer += 1
    pass

def redrawAll(canvas, data):
    if data.gameState == 'startscreen':
        canvas.create_image(data.width/6,data.height/4,anchor=NW, image=data.imageLogo)
        canvas.create_rectangle(data.width/2-100,data.height/2,data.width/2+100,data.height/2+50,fill="yellow")
        canvas.create_text(data.width/2-50,data.height/2+13,text="Start Game",anchor=NW,font="Arial 20")
    
    if data.gameState == "play":
        # draw in canvas
        data.map.draw(canvas)
        
        # text labels
        canvas.create_text(800,20,text="Population = %d"%(data.population),anchor=NW)
        canvas.create_text(800,40,text="Budget = %d"%(data.budget),anchor=NW)
        canvas.create_text(800,60,text="Click = %s"%(str(data.click)),anchor=NW)
            
        # UI
        canvas.create_rectangle(0,650,data.width,data.height,fill="grey",
            outline='grey')
        
        canvas.create_rectangle(0,0,100,data.height,fill='lightgrey',
            outline='lightgrey')
        
        for rectangle in data.coordinatesUI:
            canvas.create_rectangle(rectangle[0],rectangle[1],rectangle[2],
                rectangle[3],fill='white',activefill="yellow")
            
        canvas.create_text(30,13,text="Power",anchor=NW)
        canvas.create_text(30,43,text="Water",anchor=NW)
        canvas.create_text(28,73,text="Nature",anchor=NW)
        canvas.create_text(28,103,text="Zoning",anchor=NW)
        
        # hardcoded adjustments for specific images
        def drawImageCalibrated(input,x1,y1): 
            if input == None: pass
            elif input == "imagePower":
                canvas.create_image(x1,y1+4,anchor=SW, image=data.imagePower)
            elif input == "imageWater":
                canvas.create_image(x1+3,y1+9,anchor=SW, image=data.imageWater)
            elif input == "imageTree":
                canvas.create_image(x1+7,y1+2,anchor=SW, image=data.imageTree)
                
        # follows mouse movement
        if data.imageCurrent != None:
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