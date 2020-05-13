import heapq
from math import sqrt

class PriorityQueue:
    """
    Includes a list of items sorted by priority, lowest to highest.
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
    Includes the global view of the obstacles, as well as the field of view
    definition.
    """
    def __init__(self, current, obstacles = [], field_view=2):
        self.edges = {} # Edges of the field of view
        self.obstacles = obstacles # List of all coordinates in obstacles
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
        # FIXME: Unused?
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
        self.current = start #
        self.graph = Graph(current = self.current,obstacles=obstacles,field_view=fow)
        self.came_from[str(self.current)] = None
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
            current = frontier.get()

            if current == self.goal or self.graph.borders(point=current):
                break

            for next_point in self.graph.neighbors(point=current,step=self.step):
                new_cost = cost_so_far[str(current)] + 0.5*self.step # 0.5 is close to 1/sqrt(3), see heuristic
                if str(next_point) not in cost_so_far or new_cost < cost_so_far[str(next_point)]:
                    cost_so_far[str(next_point)] = new_cost
                    priority = new_cost + self.heuristic(next_point)
                    frontier.put(next_point, priority)
                    came_from[str(next_point)] = current

        path = self.reconstruct_path(came_from,self.current,current)
        self.current = path[1]
        self.graph.current = self.current
        self.cost_so_far[str(self.current)] = cost_so_far[str(self.current)]
        self.came_from[str(self.current)] = came_from[str(self.current)]
        self.graph.update_field_of_view()

        return path, cost_so_far, self.current

    def heuristic(self,point):
        """
        Finds the cost of getting from a point to the goal.
        """
        ### This implementation uses the actual distance to the goal, ignoring steps.
        ### Because the cost is reduced by being direct, the multiplier above exists.
        distance = 0.
        for i in range(len(point)):
            distance += (self.goal[i]-point[i])**2)
        return sqrt(distance)

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
        path = self.reconstruct_path(self.came_from,self.start,self.goal)
        return path
