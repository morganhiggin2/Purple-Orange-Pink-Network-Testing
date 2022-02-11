from re import X
from PIL import Image
import numpy
import math
import matplotlib.pyplot as plot
#convert image of black pixels to array of points

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def __str__(self):
        return ("[" + str(self.x) + ", " + str(self.y) + "]")
    
    def __repr__(self):
        return self.__str__()

def getPoints():
    img = Image.open("data/points.png")
    numpyArray = numpy.asarray(img)
    
    height = numpyArray.shape[0]
    width = numpyArray.shape[1]
    
    points = []
    
    element = None
    
    for y in range(height):
        for x in range(width):
            element = numpyArray[y][x]
            if (element[0] == 0 & element[1] == 0 & element[2] == 0):
                points += [Point(x, y)]
    
    return ([points, width, height])
    
#these next methods are for the algorithm

#parameters for algorithm

people_per_group = 5
    
class Group(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.count = 1
    
    def addPoint(self, x, y):
        #recompute average group location
        self.x = (self.x * float(self.count) + float(x)) / (float(self.count) + 1.0)
        self.y = (self.y * float(self.count) + float(y)) / (float(self.count) + 1.0)
        
        #increment count
        self.count += 1
        
    def merge(self, group):
        #recompute average group location
        self.x = (self.x * float(self.count) + float(group.x) * float(group.count)) / (float(self.count) + float(group.count))
        self.y = (self.y * float(self.count) + float(group.y) * float(group.count)) / (float(self.count) + float(group.count))
        
        #increment count
        self.count += group.count
    
    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def __str__(self):
        return ("[" + str(self.x) + ", " + str(self.y) + "]")
    
    def __repr__(self):
        return self.__str__()
    
def algorithm(points, width, height):
    #for the google maps screen, radius is max of the dimensions
    #get all in the radius
    #get rid of any outside of the google maps screen
    #then perform algorithm
    
    #have max number before it cuts out, or max radius
    
    r_factor = min(5.0, (3.0/8.0) * math.log2(len(points) / 5.0) + 2.0)
    
    R = math.sqrt((width/2)**2 + (height/2)**2)
    r = float(R) / float(r_factor)
    #r = R / math.sqrt(float(len(points)) / float(people_per_group))
    
    groups = []
    closest = None
    distance = 0.0
    
    for point in points:
        
        closest = None
        distance = width + height
        
        for group in groups:
            
            if (group.distance(point) < distance):
                closest = group
                distance = group.distance(point)
        
        #if point within r of a group
        if (closest != None and distance < r):
            #choose closest group
            #join group
            closest.addPoint(point.x, point.y)
        #else
        else:
            #make a new group
            groups += [Group(point.x, point.y)]
    
    mergedGroups = []        
    #for each group, group close ones together
    
    fig, axis = plot.subplots(2, sharex=True, sharey=True)
    drawPoints(points, width, height, axis[0])
    #drawGroups(groups, width, height, axis[1])
    
    #for each group in groups list
    for group in groups:
        #get closest group
        closest = None
        distance = width + height
        
        for mergeGroup in mergedGroups:
            if (mergeGroup.distance(group) < distance):
                closest = mergeGroup
                distance = mergeGroup.distance(group)
                
        #if there is a closest group and it is in range
        if (closest != None and distance < r):
            #merge the two groups together
            closest.merge(group)
            
            #add combined group to merged groups list
            mergedGroups += [closest]
        else:
            #add original group to list since it is not close to anything else
            mergedGroups += [group]
    
    finalGroups = []
        
    #remove any merged groups with one people
    for mergeGroup in mergedGroups:
        if (mergeGroup.count > 1):
            finalGroups += [mergeGroup]
    
    drawMergedGroups(finalGroups, width, height, axis[1])
    plot.show()
        
def drawMergedGroups(groups, width, height, axis):
    xs = []
    ys = []
    
    for group in groups:
        xs += [group.x]
        ys += [group.y]
        axis.text(group.x, group.y, s=str(group.count), horizontalalignment='right')
    
    axis.scatter(xs, ys, color="red")
    axis.axis(xmin = 0, xmax=width, ymin=0, ymax=height)
        
def drawGroups(groups, width, height, axis):
    xs = []
    ys = []
    
    for group in groups:
        xs += [group.x]
        ys += [group.y]
        axis.text(group.x, group.y, s=str(group.count), horizontalalignment='right')
    
    axis.scatter(xs, ys, color="red")
    axis.axis(xmin = 0, xmax=width, ymin=0, ymax=height)

def drawPoints(points, width, height, axis):
    xs = []
    ys = []
    
    
    for point in points:
        xs += [point.x]
        ys += [point.y]
    
    axis.scatter(xs, ys)
    axis.axis(xmin = 0, xmax=width, ymin=0, ymax=height)

def plotRGraph():
    ys1 = [32, 12.5, 8.2, 1.6, 1.3]
    ys2 = [30.1, 11.5, 7.7, 1.41, 1.07]
    xs = [800, 200, 100, 10, 5]
    
    funcX = numpy.arange(1, max(xs), 2)
    #funcY = 0.9 * numpy.log(0.6 * funcX)
    funcY = (32/800) * funcX
    
    plot.scatter(xs, ys1, color="black")
    plot.scatter(xs, ys2, color="green")
    plot.plot(funcX, funcY, color="blue")
    plot.show()
    
'''xs = numpy.array([5, 10, 100, 200, 800])
ys = numpy.array([1.07, 1.41, 7.7, 11.5, 30.1])

a, b, c = numpy.polyfit(xs, ys, 2)

funcYs = a*xs*xs + b*xs + c

print(funcYs)

plot.scatter(xs, ys, color="black")
plot.plot(xs, funcYs, color="blue")
plot.show()'''

vals = getPoints()  
print(len(vals[0]))
algorithm(vals[0], vals[1], vals[2])

plotRGraph()
