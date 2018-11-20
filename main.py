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
import math


####################################
# OOP
####################################

# class WaterPlant(object):
#     dotCount = 0
# 
#     # Model
#     def __init__(self, x, y):
#         Dot.dotCount += 1
#         self.x = x
#         self.y = y
#         self.r = random.randint(20,50)
#         self.fill = random.choice(["pink","orange","yellow","green",
#                                    "cyan","purple"])
#         self.clickCount = 0
# 
#     # View
#     def draw(self, canvas):
#         canvas.create_oval(self.x-self.r, self.y-self.r,
#                            self.x+self.r, self.y+self.r,
#                            fill=self.fill)
#         canvas.create_text(self.x, self.y, text=str(self.clickCount))
# 
#     # Controller
#     def containsPoint(self, x, y):
#         d = ((self.x - x)**2 + (self.y - y)**2)**0.5
#         return (d <= self.r)
# 
# class MovingDot(Dot):
#     # Model
#     def __init__(self, x, y):
#         super().__init__(x, y)
#         self.speed = 5 # default initial speed
# 
#     # Controller
#     def move(self, data):
#         self.x += self.speed
#         if (self.x > data.width):
#             self.x = 0    
#     


####################################
# core animation code
####################################

def init(data):
    # load data.xyz as appropriate
    
    # main map
    height = 534
    width = 800
    data.mapX1 = 150
    data.mapY1 = height/2 + 20
    data.mapX2 = data.mapX1 + width/2
    data.mapY2 = data.mapY1 + height/2
    data.mapX3 = data.mapX1 + width
    data.mapY3 = data.mapY1
    data.mapX4 = data.mapX2
    data.mapY4 = data.mapY2 - height
    
    # for the drawing of grids on the main map
    data.lst = []
    smallBoxHeight = height/22
    smallBoxWidth = width/22
    for j in range(22):
        startX1 = data.mapX1 + j*smallBoxWidth/2
        startY1 = data.mapY1 + j*smallBoxHeight/2
        for i in range(22):
            x1 = startX1 + i*smallBoxWidth/2
            y1 = startY1 - i*smallBoxHeight/2
            x2 = x1 + smallBoxWidth/2
            y2 = y1 + smallBoxHeight/2
            x3 = x1 + (smallBoxWidth)
            y3 = y1
            x4 = x2
            y4 = y2 - smallBoxHeight
            data.lst += [[x1,y1,x2,y2,x3,y3,x4,y4,"None",(j,i)]]
    
    # other data to keep track of
    data.population = 0
    data.budget = 100000
    data.timer = 0
    data.click = False
    data.clickedLst = []
    data.coordinatesUI = [(10,10,90,30),(10,40,90,60),(10,70,90,90),(10,100,90,120)]


    # images
    data.imagePower = PhotoImage(file="wind.png")
    data.imageWater = PhotoImage(file="water.png")
    data.imageTree = PhotoImage(file="tree.png")


# returns true if clicked within boundaries of a specified grid (slanted)
def checkGridClick(clickX,clickY,gridCoordinates,data):
    x1 = gridCoordinates[0]
    y1 = gridCoordinates[1]
    x2 = gridCoordinates[2]
    y2 = gridCoordinates[3]
    x3 = gridCoordinates[4]
    y3 = gridCoordinates[5]
    x4 = gridCoordinates[6]
    y4 = gridCoordinates[7]
    
    # quadrant 2
    if (x1 <= clickX <= x4) and (y4 <= clickY <= y1):
        gradientSide = (y4-y1)/(x4-x1)
        boundaryY = gradientSide*(clickX-x1) + y1
        if clickY < boundaryY: return False
        return True
    
    # quadrant 3
    elif (x1 <= clickX <= x2) and (y1 <= clickY <= y2):
        gradientSide = (y2-y1)/(x2-x1)
        boundaryY = gradientSide*(clickX-x1) + y1
        if clickY > boundaryY: return False
        return True
    
    # quadrant 4    
    elif (x2 <= clickX <= x3) and (y3 <= clickY <= y2):
        gradientSide = (y2-y3)/(x2-x3)
        boundaryY = gradientSide*(clickX-x2) + y2
        if clickY > boundaryY: return False
        return True
    
    # quadrant 1
    elif (x4 <= clickX <= x3) and (y4 <= clickY <= y3):
        gradientSide = (y2-y3)/(x2-x3)
        boundaryY = gradientSide*(clickX-x2) + y2
        if clickY < boundaryY: return False
        return True

def checkButtonClick(clickX,clickY,buttonCoordinates,data):
    if buttonCoordinates[0] <= clickX <= buttonCoordinates[2] and buttonCoordinates[1] <= clickY <= buttonCoordinates[3]:
        return True
    return False

def mousePressed(event, data):
    # use event.x and event.y
    
    # check for grid
    for grid in data.lst:
        if checkGridClick(event.x,event.y,grid,data):
            grid[8] = "Tree"
            data.click = True
            data.clickedLst += [grid[9]]
    
    # check for buttons
    for button in data.coordinatesUI:
        if checkButtonClick(event.x,event.y,button,data):
            data.click = "Button"
            

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    data.timer += 1

    pass





def redrawAll(canvas, data):
    # draw in canvas
    
    # map
    canvas.create_polygon(data.mapX1,data.mapY1,data.mapX2,data.mapY2,data.mapX3,data.mapY3,data.mapX4,data.mapY4,fill="limegreen")
    
    # text labels
    canvas.create_text(800,20,text="Population = %d"%(data.population),anchor=NW)
    canvas.create_text(800,40,text="Budget = %d"%(data.budget),anchor=NW)
    canvas.create_text(800,60,text="Click = %s"%(str(data.click)),anchor=NW)
    
    # UI
    canvas.create_rectangle(200,600,data.width,data.height,fill="lightgrey",outline='lightgrey')
    
    canvas.create_rectangle(0,0,100,data.height,fill='lightgrey',outline='lightgrey')
    
    for rectangle in data.coordinatesUI:
        canvas.create_rectangle(rectangle[0],rectangle[1],rectangle[2],rectangle[3],fill='white')
        
    # canvas.create_rectangle(10,10,90,30,fill='white')
    canvas.create_text(30,13,text="Power",anchor=NW)
    
    # canvas.create_rectangle(10,40,90,60,fill='white')
    canvas.create_text(30,43,text="Water",anchor=NW)
    
    # canvas.create_rectangle(10,70,90,90,fill='white')
    canvas.create_text(28,73,text="Nature",anchor=NW)
    
    # canvas.create_rectangle(10,100,90,120,fill='white')
    canvas.create_text(28,103,text="Zoning",anchor=NW)




    for smallBox in data.lst:
        if smallBox[8] == "None":
            color = "limegreen"
        elif smallBox[8] == "Building":
            color = 'grey'
        else:
            color = 'limegreen'
            # color = smallBox[8]

        canvas.create_polygon(smallBox[0],smallBox[1],smallBox[2],smallBox[3],smallBox[4],smallBox[5],smallBox[6],smallBox[7],fill=color,outline="black",width = 2,activefill="red")
        # if smallBox[8] == "Power":
        #     canvas.create_image(smallBox[0],smallBox[1]+4,anchor=SW, image=data.imagePower)
        # elif smallBox[8] == "Water":
        #     canvas.create_image(smallBox[0]+3,smallBox[1]+9,anchor=SW, image=data.imageWater)
        # elif smallBox[8] == "Tree":
        #     canvas.create_image(smallBox[0]+7,smallBox[1]+2,anchor=SW, image=data.imageTree)
    
    for clickedGrid in data.clickedLst:
        j = clickedGrid[0]
        i = clickedGrid[1]
        number = j*22 + i
        x1 = data.lst[number][0]
        y1 = data.lst[number][1]
        canvas.create_image(x1+7,y1+2,anchor=SW,image=data.imageTree)
        
        


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
    data.timerDelay = 100 # milliseconds
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