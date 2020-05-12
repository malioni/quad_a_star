import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from a_star import *

class animation:

    def __init__(self, obstacles, fow, start, goal):
        self.flagInit = True
        self.fig, self.ax = plt.subplots()
        self.fow = fow
        self.handle = []
        self.obs_handle = []
        self.drawObstacles(obstacles)
        plt.axis([0.,10.,0.,10.])
        plt.ion()

    def drawObstacles(self,obstacles):

        for i in range(len(obstacles)):
            if self.flagInit:
                self.obs_handle.append(mpatches.Rectangle(xy=(obstacles[i][0],obstacles[i][1]),width=obstacles[i][2],height=obstacles[i][3],fill=True,fc='orange'))
                self.ax.add_patch(self.obs_handle[0])
            else:
                self.obs_handle[0].set_xy((obstacles[i][0],obstacles[i][1]))

    def drawEverything(self,point,path):
        self.drawObject(point)
        self.drawFrame(point)
        self.drawPath(point,path)
        plt.pause(0.001)

        if self.flagInit:
            self.flagInit = False

    def drawFrame(self,point):
        x = point[0] - self.fow/2.
        y = point[1] - self.fow/2.
        xy = (x,y)

        if self.flagInit:
            self.handle.append(mpatches.Rectangle(xy,self.fow,self.fow,fill=False,ec='black',lw = 0.1))
            self.ax.add_patch(self.handle[1])
        else:
            self.handle[1].set_xy(xy)

    def drawPath(self,path):
        x_list = []
        y_list = []

        for i in path:
            x_list.append(path[i][0])
            y_list.append(path[i][1])

        plt.scatter(x_list,y_list,s=10)

    def drawObject(self,point):
        xy = (point[0],point[1])

        if self.flagInit:
            self.handle.append(mpatches.Circle(xy,radius = 0.3,fill=True,ec='blue'))
            self.ax.add_patch(self.handle[0])
        else:
            self.handle[0].set_xy(xy)

start = [0.5,0.5]
goal = [10.,10.]
step = 0.1
fow = 1.
obstacles = [[5.,5.,2.,2.],[7.,7.,1.,1.]]


pic = animation(obstacles=obstacles,fow=fow,start=start,goal=goal)
a_star = AStarSearch(start=start,goal=goal,step=step,obstacles=[])

current = start

while current != goal:
    path, cost_so_far, current = a_star.update()
    pic.drawEverything(current,path)
    plt.pause(0.001)

plt.show()
plt.waitforbuttonpress()
plt.close()

