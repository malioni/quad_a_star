import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

class Graph:
    def __init__(self, current, obstacles = [], field_view=1.):
        self.edges = {}
        self.obstacles = obstacles
        self.current = current
        self.field_of_view = field_view
        self.update_field_of_view()

    def neighbors(self,point,step):
        neighbors_list = []

        for dim in range(len(point)):
            temp = point
            print(point)
            point[dim] += step
            print(point)
            print(temp)
            if point not in self.obstacles:
                neighbors_list.append(temp)
            temp2 = point
            temp2[dim] -= step
            if temp2 not in self.obstacles:
                neighbors_list.append(temp2)

        print(neighbors_list)

        return neighbors_list

    def borders(self,point):
        for coord in range(len(point)):
            if point[coord] == self.edges[coord][0] or point[coord] == self.edges[coord][1]:
                return True
        return False

    def update_obstacles(self,obstacles):
        for coord in range(len(obstacles)):
            self.obstacles.append(obstacles[coord])

    def update_field_of_view(self):
        for dim in range(len(self.current)):
            self.edges[dim] = [self.current[dim]-self.field_of_view,self.current[dim]+self.field_of_view]

class AStarSearch:
    def __init__(self, start, goal,obstacles,step=0.1):
        self.cost_so_far = {}
        self.came_from = {}
        self.goal = goal
        self.start = start
        self.step = step
        self.current = start
        self.graph = Graph(current = self.current,obstacles=obstacles)
        self.came_from[str(self.current)] = None
        self.cost_so_far[str(self.current)] = 0.

    def update(self):
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
                new_cost = self.cost_so_far[str(current)] + self.step
                # print("here")
                # print(str(next_point) not in cost_so_far)
                # print(new_cost < cost_so_far[str(next_point)])
                # print(cost_so_far)
                # print(next_point)
                if str(next_point) not in cost_so_far or new_cost < cost_so_far[str(next_point)]:
                    print("here 2")
                    cost_so_far[str(next_point)] = new_cost
                    priority = new_cost + self.heuristic(next_point)
                    frontier.put(next_point, priority)
                    came_from[str(next_point)] = current

        path = self.reconstruct_path(came_from,self.current,current)
        print(path)
        self.current = path[1]
        self.graph.current = self.current
        self.cost_so_far[str(self.current)] = cost_so_far[str(self.current)]
        self.came_from[str(self.current)] = came_from[str(self.current)]
        self.graph.update_field_of_view()

        return path, cost_so_far, self.current

    def heuristic(self,point):
        distance = 0.
        for i in range(len(point)):
            distance += abs(self.goal[i]-point[i])
        return distance

    def reconstruct_path(self,came_from,start,goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path

    def get_results(self):
        path = self.reconstruct_path(self.came_from,self.start,self.goal)
        return path
