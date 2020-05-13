"""
A* implementation
Based in code by Amit Patel, found at:
    https://www.redblobgames.com/pathfinding/a-star/implementation.html
"""

import heapq
from math import sqrt

class PriorityQueue:
    """
    Includes a list of items sorted by priority, lowest to highest.
    Wrapper for the heapq class.
    """
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

class Graph:
    """
    The graph as known by the quadrotor. All obstacle locations can either be added
    all at once or as they come into the quadrotors field of view without degrading
    performance.
    """
    def __init__(self, current, obstacles = [], field_view=2):
        self.edges = {} # Edges of the field of view
        self.obstacles = obstacles # List of all coordinates in known obstacles
            # TODO: Faster way to evaluate? Or way without global knowledge?
        self.current = current # Current position of the quadrotor
        self.field_of_view = field_view # Size of the field of view, in each direction from the quadrotor
        self.update_field_of_view()

    def neighbors(self,point,step):
        """
        Defines the neighbors adjacent to the current block, and doesn't add
        them if they are in the obstacles list.
        """
        #TODO: See if the aesthetic code works
        neighbors_list = []

        for dim in range(len(point)):
            temp = point.copy()
            temp[dim] += step
            if temp not in self.obstacles:
                neighbors_list.append(temp)
            temp = point.copy()
            temp[dim] -= step
            if temp not in self.obstacles:
                neighbors_list.append(temp)

        return neighbors_list

    def borders(self,point):
        """
        Determines if the current point is along one of the edges of the
        field of view.
        """
        for coord in range(len(point)):
            if point[coord] == self.edges[coord][0] or point[coord] == self.edges[coord][1]:
                return True
        return False

    def update_obstacles(self,obstacles):
        """
        Add obstacles to the self.obstacles list.
        """
        for coord in range(len(obstacles)):
            self.obstacles.append(obstacles[coord])

    def update_field_of_view(self):
        """
        Puts the field of view around the current quadrotor position.
        """
        for dim in range(len(self.current)):
            self.edges[dim] = [self.current[dim]-self.field_of_view,self.current[dim]+self.field_of_view]

class AStarSearch:
    """
    Conducts the search.
    """
    def __init__(self, start, goal,obstacles,step=1,fow=2):
        self.cost_so_far = {} # A dictionary of the minimum cost to each point explored
        self.came_from = {} # A dictionary of the point directly before each point explored
        self.goal = goal
        self.start = start
        self.step = step # Distance between points
        self.current = start
        self.graph = Graph(current = self.current,obstacles=obstacles,field_view=fow)
        self.came_from[str(self.current)] = None # As lists cannot be keys in dictionaries,
        # we convert them to strings. Can be replaced with a better method.
        self.cost_so_far[str(self.current)] = 0.

    def update(self):
        """
        Follows A* Implementation, using borders to stop searching.
        """
        frontier = PriorityQueue()
        frontier.put(self.current, 0)
        came_from = {}
        cost_so_far = {}
        came_from[str(self.current)] = self.came_from[str(self.current)]
        cost_so_far[str(self.current)] = self.cost_so_far[str(self.current)]

        while not frontier.empty():
            current = frontier.get() # Get next node with the lowest priority score

            if current == self.goal or self.graph.borders(point=current):
                break

            # Step through the available neighbors of the node
            for next_point in self.graph.neighbors(point=current,step=self.step):
                # Calculate the cost of moving to the next point.
                # For quadrotors the cost of moving to each node is the same 
                new_cost = cost_so_far[str(current)] + self.step
                if str(next_point) not in cost_so_far or new_cost < cost_so_far[str(next_point)]:
                    cost_so_far[str(next_point)] = new_cost
                    priority = new_cost + self.heuristic(next_point)
                    frontier.put(next_point, priority)
                    came_from[str(next_point)] = current

        path = self.reconstruct_path(came_from,self.current,current)
        self.current = path[1] # Take one step in the desired direction, first 
        # point in path is the current location
        self.graph.current = self.current # Update graph's knowledge of location
        self.cost_so_far[str(self.current)] = cost_so_far[str(self.current)]
        self.came_from[str(self.current)] = came_from[str(self.current)]
        self.graph.update_field_of_view()

        return path, cost_so_far, self.current

    def heuristic(self,point):
        """
        Finds the cost of getting from a point to the goal.
        """
        distance = 0.
        # Use actual distance, with a modifier.
        for i in range(len(point)):
            distance += (self.goal[i]-point[i])**2
        return sqrt(distance) * 2

    def reconstruct_path(self,came_from,start,goal):
        """
        Rebuilds the path from the goal to the start.
        """
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[str(current)]
        path.append(start)
        path.reverse()
        return path

    def get_results(self):
        """
        Used to reconstruct the final path after the goal has been reached
        """
        path = self.reconstruct_path(self.came_from,self.start,self.goal)
        return path
