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
        plt.axis([0,100,0,100])
        plt.ion()

    def drawObstacles(self,obstacles):

        for i in range(len(obstacles)):
            if self.flagInit:
                self.obs_handle.append(mpatches.Rectangle(xy=(obstacles[i][0],obstacles[i][1]),width=obstacles[i][2],height=obstacles[i][3],fill=True,fc='orange'))
                self.ax.add_patch(self.obs_handle[i])
            else:
                self.obs_handle[i].set_xy((obstacles[i][0],obstacles[i][1]))

    def drawEverything(self,point,path):
        self.drawObject(point)
        self.drawFrame(point)
        self.drawPath(path)
        plt.pause(0.001)

        if self.flagInit:
            self.flagInit = False

    def drawFrame(self,point):
        x = point[0] - self.fow
        y = point[1] - self.fow
        xy = (x,y)

        if self.flagInit:
            self.handle.append(mpatches.Rectangle(xy,2*self.fow,2*self.fow,fill=False,ec='black',lw = 1))
            self.ax.add_patch(self.handle[1])
        else:
            self.handle[1].set_xy(xy)

    def drawPath(self,path):
        x_list = []
        y_list = []

        for i in path:
            x_list.append(i[0])
            y_list.append(i[1])

        plt.scatter(x_list,y_list,s=10)

    def drawObject(self,point):
        xy = (point[0]-0.5,point[1]-0.5)

        if self.flagInit:
            self.handle.append(mpatches.Rectangle(xy,height = 1,width=1,fill=True,ec='blue'))
            self.ax.add_patch(self.handle[0])
        else:
            self.handle[0].set_xy(xy)

start = [1,1,1]
goal = [80,80,80]
step = 1
fow = 10
#obstacles = [[20,20,30,30],[60,60,10,10]]
#obstacles = []

a_obstacles = []
x_coord = 20
while x_coord <= 50:
    y_coord = 20
    while y_coord <= 50:
        z_coord = 20
        while z_coord <= 50:
            a_obstacles.append([x_coord,y_coord,z_coord])
            z_coord +=1
        y_coord += 1
    x_coord += 1

x_coord = 60
while x_coord <= 70:
    y_coord = 60
    while y_coord <= 70:
        z_coord = 60
        while z_coord <= 70:
            a_obstacles.append([x_coord,y_coord,z_coord])
            z_coord += 1
        y_coord += 1
    x_coord += 1

#pic = animation(obstacles=obstacles,fow=fow,start=start,goal=goal)
a_star = AStarSearch(start=start,goal=goal,step=step,obstacles=a_obstacles,fow=fow)

current = start

while current != goal:
    path, cost_so_far, current = a_star.update()
    print(current)
    # pic.drawEverything(current,path)
    # plt.pause(0.01)
# plt.figure(1)

path = a_star.get_results()

# x_list = []
# y_list = []
# z_list = []
#
# for i in path:
#     x_list.append(i[0])
#     y_list.append(i[1])
#     z_list.append(i[2])
#
# plt.subplot(311)
# plt.scatter(x_list,y_list,s=10)
# plt.subplot(312)
# plt.scatter(x_list,z_list,s=10)
# plt.subplot(313)
# plt.scatter(y_list,z_list,s=10)
#
# plt.show()
# plt.pause(10)
