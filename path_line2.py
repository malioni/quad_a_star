"""
==================
Animated Path Line
==================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

from test2 import path, goal

def gen_rand_points(num):
    """
    Generates a list of points for Testing
    """
    points = np.empty((num, 3))
    for index in range(num):
        points[index, :] = np.random.rand(3)
    return points

def gen_3d_path_segments(points):
    """
    Takes the total number of points, and returns the lines.
    """
    length = len(points)
    line_data = np.empty((3, length))
    for index in range(length):
        for i in range(3):
            line_data[i, index] = points[index][i]
    return line_data

def update_path(num, dataLines, lines):
    """
    Function called in FuncAnimation to draw the line.
    """
    for line, data in zip(lines, dataLines):
        # NOTE: there is no .set_data() for 3 dim data...
        line.set_data(data[0:2, :num])
        line.set_3d_properties(data[2, :num])

        # Visualize Field of View
        # line.set_marker("s")
        # line.set_markeredgewidth(20)
    return lines

def plot_cube(cube_definition):
    cube_definition_array = [
        np.array(list(item))
        for item in cube_definition
    ]

    points = []
    points += cube_definition_array
    vectors = [
        cube_definition_array[1] - cube_definition_array[0],
        cube_definition_array[2] - cube_definition_array[0],
        cube_definition_array[3] - cube_definition_array[0]
    ]

    points += [cube_definition_array[0] + vectors[0] + vectors[1]]
    points += [cube_definition_array[0] + vectors[0] + vectors[2]]
    points += [cube_definition_array[0] + vectors[1] + vectors[2]]
    points += [cube_definition_array[0] + vectors[0] + vectors[1] + vectors[2]]

    points = np.array(points)

    edges = [
        [points[0], points[3], points[5], points[1]],
        [points[1], points[5], points[7], points[4]],
        [points[4], points[2], points[6], points[7]],
        [points[2], points[6], points[3], points[0]],
        [points[0], points[2], points[4], points[1]],
        [points[3], points[6], points[7], points[5]]
    ]

    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')

    faces = Poly3DCollection(edges, linewidths=1, edgecolors='k')
    faces.set_facecolor((0,0,1,0.1))

    ax.add_collection3d(faces)

    # Plot the points themselves to force the scaling of the axes
    ax.scatter(points[:,0], points[:,1], points[:,2], s=0)

    # ax.set_aspect('equal')

obstacle1 = [(0,20,0), (0,20,100), (0,24,0), (50,20,0)]
obstacle2 = [(0,50,0), (80,50,0), (0,54,0), (0,50,50)]
obstacle3 = [(0, 80, 40), (80, 80, 40), (0,84, 40), (0, 80, 100)]

# data = [gen_3d_path_segments(([0, 0, 0], [1, 1, 1], [0.5, 1, 0.5]))]
# data = [gen_3d_path_segments(gen_rand_points(50))]
data = [gen_3d_path_segments(path)]

# Attaching 3D axis to the figure
fig = plt.figure()
ax = fig.add_subplot(projection="3d")

lines = [ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1])[0] for dat in data]

# Setting the axes properties
ax.set_xlim3d([0.0, 80.0])
ax.set_xlabel('X')

ax.set_ylim3d([0.0, 100.0])
ax.set_ylabel('Y')

ax.set_zlim3d([0.0, 100.0])
ax.set_zlabel('Z')

plot_cube(obstacle1)
plot_cube(obstacle2)
plot_cube(obstacle3)

[goal_x, goal_y, goal_z] = goal
ax.scatter(goal_x, goal_y, goal_z, marker='*', color='y')

# # Make data
# u = np.linspace(0, 2 * np.pi, 100)
# v = np.linspace(0, np.pi, 100)
# x = 2 * np.outer(np.cos(u), np.sin(v)) + goal_x
# y = 2 * np.outer(np.sin(u), np.sin(v)) + goal_y
# z = 2 * np.outer(np.ones(np.size(u)), np.cos(v)) + goal_z
#
# # Plot the surface
# ax.plot_surface(x, y, z, color='y')

# Creating the Animation object
path_ani = animation.FuncAnimation(
    fig, update_path, len(path)+30, fargs=(data, lines), interval=20)

plt.show()
