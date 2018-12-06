####################################
# map.py
####################################

from tkinter import *

import pyautogui
import math
import random
from PIL import Image
from PIL import ImageTk

####################################
# OOP for Map
####################################

class Map(object):

    def __init__(self,playerName):        
        # main map             
        self.height = 534
        self.width = 800
        self.mapX1 = 150
        self.mapY1 = self.height/2 + 50
        self.mapX2 = self.mapX1 + self.width/2
        self.mapY2 = self.mapY1 + self.height/2
        self.mapX3 = self.mapX1 + self.width
        self.mapY3 = self.mapY1
        self.mapX4 = self.mapX2
        self.mapY4 = self.mapY2 - self.height
        
        # initialize grid contents to be None, incl coordinates
        self.gridContent = {}
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
                self.gridContent[(j,i)] = {'content':None,'coordinates':(x1,y1,x2,y2,x3,y3,x4,y4),'color':None,'pollution':0,'population':0}
        
        # requirements
        self.requirements = {'imageApartment':{'power consumption':100,'water consumption':100,'polluting':3,'population':100},'imageStore':{'power consumption':100,'water consumption':100,'polluting':3,'jobs':10},'imageIndustry':{'power consumption':200,'water consumption':200,'polluting':30,'jobs':60}}
        
        # stats
        self.stats = {'population':0,'jobs':0, 'water':0, 'power':0}
        
        # images
        self.imagePower = PhotoImage(file="wind.png")
        self.imageWater = PhotoImage(file="water.png")
        self.imageTree = PhotoImage(file="tree.png")
        self.imageConstruction = PhotoImage(file="construction3.png")
        
        im1 = Image.open("apartment.png")
        im1.thumbnail((45,45))
        self.imageApartment = ImageTk.PhotoImage(im1)
        
        im2 = Image.open("cabin2.png")
        im2.thumbnail((35,35))
        self.imageCabin = ImageTk.PhotoImage(im2)
        
        im3 = Image.open("store2.png")
        im3.thumbnail((35,35))
        self.imageStore = ImageTk.PhotoImage(im3)
        
        im4 = Image.open("industry2.png")
        im4.thumbnail((35,35))
        self.imageIndustry = ImageTk.PhotoImage(im4)
    
    # returns a list of adjacent cells
    def adjacentCellGenerator(currentCell):
        x = currentCell[0]
        y = currentCell[1]
        lst = [(x,y+1),(x,y-1),(x-1,y),(x+1,y),(x+1,y+1),(x-1,y-1),(x+1,y-1),(x-1,y+1)]
        for item in lst:
            if not (0<=item[0]<=21 and 0<=item[1]<=21):
                position = lst.index(item)
                lst.pop(position)
        return lst
    
    def randomMapGeneration(self):
        randomNum = random.randint(6,15)
        randomNum2 = random.randint(0,1)
        for key in self.gridContent.keys():
            if randomNum <= key[randomNum2] < randomNum+4 :
                self.gridContent[key]['color'] = 'blue'
                self.gridContent[key]['content'] = 'river'
                continue
            randomChance = random.uniform(0,1)
            if randomChance >= 0.85:
                self.gridContent[key]['content'] = 'imageTree'
                adjacentCells = Map.adjacentCellGenerator(key)
                print(adjacentCells)
                for cell in adjacentCells:
                    randomChance = random.uniform(0,1)
                    if randomChance >= 0.70:
                        try:
                            if self.gridContent[cell]['content'] == None:
                                self.gridContent[cell]['content'] = 'imageTree'
                        except:
                            pass
        for key in self.gridContent.keys():
            if self.gridContent[key]['content'] == 'imageTree':
                self.gridContent[key]['color'] == 'forestgreen'
            

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
    def mousePressAction(self,clickX,clickY,imageCurrent,color):
        for key in self.gridContent.keys():
                gridCoordinates = self.gridContent[key]['coordinates']
                if Map.checkGridClick(clickX,clickY,gridCoordinates):
                    if self.gridContent[key]['content']==None:
                        self.gridContent[key]['content']= imageCurrent
                        # get coordinates of matching grid (at [9][0] and [9][1])
                        # replace data as imageCurrent
                        self.gridContent[key]['color'] = color
                        return True
                    elif self.gridContent[key]['content']!=None: pass 
                    # if something is occupied already
        return False
    
    # updates to stats during construction phase
    def updateStatsConstructionPhase(self,current,key):
        self.gridContent[key]['power'] = 0 - self.requirements[current]['power consumption']
        self.gridContent[key]['water'] = 0 - self.requirements[current]['water consumption']
        
    # desirable city 
    def desirabilityConstruction(self):
        for key in self.gridContent.keys():
            if self.gridContent[key]['content'] == None:
                continue
            elif self.gridContent[key]['content'] == "ZoningResidential":
                x = 100 - self.gridContent[key]['pollution'] # current score
                probability = (100/(1+math.e**(9-0.1*x)))
                # visualize at https://www.desmos.com/calculator/kn9tpwdan5
                randomGenerator = random.uniform(0,100)
                # if randomGenerator value is lower than probability, it will spawn
                if randomGenerator <= probability:
                    self.gridContent[key]['content'] = "imageConstruction"
                    self.gridContent[key]['constructing'] = ["imageApartment",3]
                    # 3 days for construction to be done
                    current = self.gridContent[key]['constructing'][0]
                    Map.updateStatsConstructionPhase(self,current,key)
            elif self.gridContent[key]['content'] == "ZoningCommercial":
                x = 100 - self.gridContent[key]['pollution'] # current score
                probability = (100/(1+math.e**(7-0.1*x)))
                randomGenerator = random.uniform(0,100)
                # if randomGenerator value is lower than probability, it will spawn
                if randomGenerator <= probability:
                    self.gridContent[key]['content'] = "imageConstruction"
                    self.gridContent[key]['constructing'] = ["imageStore",3]
                    # 3 days for construction to be done
                    current = self.gridContent[key]['constructing'][0]
                    Map.updateStatsConstructionPhase(self,current,key)
            elif self.gridContent[key]['content'] == "ZoningIndustrial":
                x = 100 - self.gridContent[key]['pollution'] # current score
                probability = (100/(1+math.e**(5-0.1*x)))
                randomGenerator = random.uniform(0,100)
                # if randomGenerator value is lower than probability, it will spawn
                if randomGenerator <= probability:
                    self.gridContent[key]['content'] = "imageConstruction"
                    self.gridContent[key]['constructing'] = ["imageIndustry",3]
                    # 3 days for construction to be done
                    current = self.gridContent[key]['constructing'][0]
                    Map.updateStatsConstructionPhase(self,current,key)
            

    # when construction days are reached, show completed house and update values
    def constructionStatus(self):
        for key in self.gridContent.keys():
            if self.gridContent[key]['content'] == 'imageConstruction':
                if self.gridContent[key]['constructing'][1] >= 1:
                    self.gridContent[key]['constructing'][1] -= 1
                elif self.gridContent[key]['constructing'][1] == 0:
                    self.gridContent[key]['content'] = self.gridContent[key]['constructing'][0]
                    del self.gridContent[key]['constructing']
                    current = self.gridContent[key]['content']
                    if 'population' in self.requirements[current].keys():
                        self.gridContent[key]['population'] = self.requirements[current]['population']
                    if 'polluting' in self.requirements[current].keys():
                        self.gridContent[key]['pollution'] = self.requirements[current]['polluting']
                    if 'jobs' in self.requirements[current].keys():
                        self.gridContent[key]['jobs'] = self.requirements[current]['jobs']
                     
    
    # refreshes and consolidates stats
    def statsRefresh(self):
        self.stats = {'population':0,'jobs':0, 'water':0, 'power':0}
        for key in self.gridContent.keys():
            currentGrid = self.gridContent[key]
            for statLabel in self.stats:
                self.stats[statLabel] += currentGrid.get(statLabel,0)
    
    # spread of pollution, based on random wind direction
    def pollutionSpread(self):
        randomValue = random.randint(0,3)
        direction = ["N",'S','E','W'][randomValue]
        for key in self.gridContent.keys():
            if (self.gridContent[key]['pollution'] >0 and 'pollution updated' not in self.gridContent[key].keys()) or ('pollution updated' in self.gridContent[key].keys() and self.gridContent[key]['pollution updated'][1]>0):
                pollutionValue = self.gridContent[key]['pollution']
                if 'pollution updated' in self.gridContent[key].keys() and self.gridContent[key]['pollution updated'][1]>0:
                    pollutionValue = self.gridContent[key]['pollution updated'][1]
                if direction == 'N': newKey = (key[0]-1,key[1])
                elif direction == 'S': newKey = (key[0]+1,key[1])
                elif direction == 'E': newKey = (key[0],key[1]+1)
                elif direction == 'W': newKey = (key[0],key[1]-1)
                # in case key is out of bounds
                try:
                    if self.gridContent[newKey]['pollution'] < pollutionValue:
                        self.gridContent[newKey]['pollution updated'] = (True, self.gridContent[newKey]['pollution']) # captures original value of pollution before spread
                        self.gridContent[newKey]['pollution'] = (self.gridContent[newKey]['pollution'] + pollutionValue)/2
                except: pass
        for key in self.gridContent.keys():
            if 'pollution updated' in self.gridContent[key].keys():
                del self.gridContent[key]['pollution updated']
            if self.gridContent[key]['content'] == 'imageApartment':
                self.gridContent[key]['pollution'] += 30
            elif self.gridContent[key]['content'] == None:
                self.gridContent[key]['pollution'] *= 0.7
                

    
    def draw(self,canvas):        
        # map
        canvas.create_polygon(self.mapX1,self.mapY1,self.mapX2,self.mapY2,
            self.mapX3,self.mapY3,self.mapX4,self.mapY4,fill="forestgreen")
        
        # draw borders of grids
        for key in self.gridContent.keys():
            grid = self.gridContent[key]
            if 'temp' in grid.keys(): 
                color = grid['temp']
            else: 
                if grid['color'] == None: color = "limegreen"
                else: color = grid['color']
            canvas.create_polygon(grid['coordinates'][0],grid['coordinates'][1],grid['coordinates'][2],grid['coordinates'][3],grid['coordinates'][4],grid['coordinates'][5],grid['coordinates'][6],grid['coordinates'][7],fill=color,outline="black",width = 2)
            
        
        # hardcoded adjustments for specific images
        def drawImageCalibrated(input,x1,y1):
            if input == None: pass
            elif input == "imagePower":
                canvas.create_image(x1,y1+4,anchor=SW, image=self.imagePower)
            elif input == "imageWater":
                canvas.create_image(x1+3,y1+9,anchor=SW, image=self.imageWater)
            elif input == "imageTree":
                canvas.create_image(x1+7,y1+2,anchor=SW, image=self.imageTree)
            elif input == "imageConstruction":
                canvas.create_image(x1+3,y1+8,anchor=SW, image=self.imageConstruction)
            elif input == "imageApartment":
                canvas.create_image(x1,y1+8,anchor=SW, image=self.imageApartment)
            elif input == "imageStore":
                canvas.create_image(x1+1,y1+11,anchor=SW, image=self.imageStore) 
            elif input == "imageIndustry":
                canvas.create_image(x1+1,y1+11,anchor=SW, image=self.imageIndustry)
            elif input == 'zoning':
                x2 = x1 + self.smallBoxWidth/2
                y2 = y1 + self.smallBoxHeight/2
                x3 = x1 + (self.smallBoxWidth)
                y3 = y1
                x4 = x2
                y4 = y2 - self.smallBoxHeight
                canvas.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4,fill='red')
                
        # to draw out objects for grid content
        for key in self.gridContent.keys():
            currentGrid = self.gridContent[key]['content']
            x1 = self.gridContent[key]['coordinates'][0]
            y1 = self.gridContent[key]['coordinates'][1]
            try:
                drawImageCalibrated(currentGrid,x1,y1)
            except:
                pass
