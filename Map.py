####################################
# map.py
####################################

from tkinter import *

import pyautogui
import math

####################################
# OOP for Map
####################################

class Map(object):

    def __init__(self,playerName):        
        # main map             
        self.height = 534
        self.width = 800
        self.mapX1 = 150
        self.mapY1 = self.height/2 + 20
        self.mapX2 = self.mapX1 + self.width/2
        self.mapY2 = self.mapY1 + self.height/2
        self.mapX3 = self.mapX1 + self.width
        self.mapY3 = self.mapY1
        self.mapX4 = self.mapX2
        self.mapY4 = self.mapY2 - self.height
        
        # for the drawing of grids on the main map
        self.lst = []
        self.smallBoxHeight = self.height/22
        self.smallBoxWidth = self.width/22
        for j in range(22):
            startX1 = self.mapX1 + j*self.smallBoxWidth/2
            startY1 = self.mapY1 + j*self.smallBoxHeight/2
            for i in range(22):
                x1 = startX1 + i*self.smallBoxWidth/2
                y1 = startY1 - i*self.smallBoxHeight/2
                x2 = x1 + self.smallBoxWidth/2
                y2 = y1 + self.smallBoxHeight/2
                x3 = x1 + (self.smallBoxWidth)
                y3 = y1
                x4 = x2
                y4 = y2 - self.smallBoxHeight
                self.lst += [[x1,y1,x2,y2,x3,y3,x4,y4,"None",(j,i)]]
        
        # initialize grid contents to be None
        self.gridContent = []
        for j in range(22):
            self.gridContent += [[]]
            for i in range(22):
                self.gridContent[j] += [None]
        
        # images
        self.imagePower = PhotoImage(file="wind.png")
        self.imageWater = PhotoImage(file="water.png")
        self.imageTree = PhotoImage(file="tree.png")

    # returns true if clicked within boundaries of a specified grid (slanted)
    def checkGridClick(clickX,clickY,gridCoordinates):
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
    
    # to call from mouse pressed in main game file 
    def mousePressAction(self,clickX,clickY,imageCurrent):
        for gridCoordinates in self.lst:
            if Map.checkGridClick(clickX,clickY,gridCoordinates):
                self.gridContent[gridCoordinates[9][0]][gridCoordinates[9][1]] = imageCurrent
                # get coordinates of matching grid
                # replace data as imageCurrent
    
    def draw(self,canvas):        
        # map
        canvas.create_polygon(self.mapX1,self.mapY1,self.mapX2,self.mapY2,
            self.mapX3,self.mapY3,self.mapX4,self.mapY4,fill="forestgreen")
        
        # draw borders of grids
        for smallBox in self.lst:
            if smallBox[8] == "None":
                color = "forestgreen"
            else:
                color = smallBox[8]
            canvas.create_polygon(smallBox[0],smallBox[1],smallBox[2],smallBox[3],smallBox[4],smallBox[5],smallBox[6],smallBox[7],fill=color,outline="black",width = 2)
        
        # hardcoded adjustments for specific images
        def drawImageCalibrated(input,x1,y1):
            if input == None: pass
            elif input == "imagePower":
                canvas.create_image(x1,y1+4,anchor=SW, image=self.imagePower)
            elif input == "imageWater":
                canvas.create_image(x1+3,y1+9,anchor=SW, image=self.imageWater)
            elif input == "imageTree":
                canvas.create_image(x1+7,y1+2,anchor=SW, image=self.imageTree)
                
        # to draw out objects for grid content
        for row in range(len(self.gridContent)):
            for col in range(len(self.gridContent[row])):
                currentGrid = self.gridContent[row][col]
                x1 = self.lst[row*22+col][0]
                y1 = self.lst[row*22+col][1]
                drawImageCalibrated(currentGrid,x1,y1)