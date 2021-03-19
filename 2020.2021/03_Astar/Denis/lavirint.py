import copy
# S - ulazak
# X - ne mozemo tuda, prepreka
# F - izlaz
# . - mozemo, 1
# # - mozemo, 2
# G = {
# (i,j) -> [((k,l), w)]
#}
class Maze:
    def __init__(self, maze_matrix):
        self.start, self.finish, self.adjacency_list = self.convert_to_graph(maze_matrix)
        self.maze_matrix = maze_matrix

    def __str__(self):
        return str(self.adjacency_list)

    def convert_to_graph(self, maze_matrix):
        adjacency_list = {}
        start = None
        finish = None

        n = len(maze_matrix)
        m = len(maze_matrix[0])

        for i in range(n):
            for j in range(m):
                v = (i, j)
                neighbors = []

                if maze_matrix[i][j] != 'X':
                    if maze_matrix[i][j] == 'S':
                        start = v
                    if maze_matrix[i][j] == 'F':
                        finish = v
                    if i > 0:
                        if maze_matrix[i-1][j] != 'X':
                            w = (i-1,j)
                            if maze_matrix[i-1][j] == "#":
                                weight = 2
                            else:
                                weight = 1
                            neighbors.append((w, weight))
                    if i < n - 1:
                        if maze_matrix[i+1][j] != 'X':
                            w = (i+1, j)
                            if maze_matrix[i+1][j] == '#':
                                wei = 2
                            else:
                                wei = 1

                            neighbors.append((w, wei))
                    if j > 0:
                        if maze_matrix[i][j-1] != 'X':
                            w = (i, j-1)
                            if maze_matrix[i][j-1] == '#':
                                wei = 2

                            else:
                                wei = 1
                            neighbors.append((w, wei))
                    if j < m - 1:
                        if maze_matrix[i][j+1] != 'X':
                            w = (i, j+1)
                            if maze_matrix[i][j+1] == '#':
                                wei = 2
                            else:
                                wei = 1
                            neighbors.append((w, wei))
                adjacency_list[v] = neighbors
        return start, finish, adjacency_list

    def h(self, v_cords):
        v_x1 = int(v_cords[0])
        v_y1 = int(v_cords[1])

        finish_x1 = int(self.finish[0])
        finish_y1 = int(self.finish[1])

        return abs(v_x1 - finish_x1) + abs(v_y1 - finish_y1)

    def astar(self, start, stop):
        open_list = set([start])
        closed_list = set([])

        g = {}
        g[start] = 0

        parents = {}
        parents[start] = None


        while len(open_list) > 0:
            n = None
            for v in open_list:
                if n==None or g[v] + self.h(v) < g[n] + self.h(n):
                    n = v
            if n == None:
                return None
            if n == stop:
                path = []
                path.append(stop)
                tmp = parents[stop]
                while tmp != None:
                    path.append(tmp)
                    tmp = parents[tmp]

                path.reverse()
                return path
            for m, weight in self.adjacency_list[n]:
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m is closed_list:
                            closed_list.remove(m)
                            open_list.add(m)
            open_list.remove(n)
            closed_list.add(n)
        return None


    def solve(self):
        graph_path = self.astar(self.start, self.finish)
        if graph_path == None:
            print("No solution!")
            return self.maze_matrix
        else:
            print("Found solution!")
            solved_matrix = copy.deepcopy(self.maze_matrix)
            path = []
            for v_cords in graph_path:
                v_x1 = int(v_cords[0])
                v_x2 = int(v_cords[1])
                if solved_matrix[v_x1][v_x2] != 'S' and solved_matrix[v_x1][v_x2] != 'F':
                    solved_matrix[v_x1][v_x2] = '*'
                path.append((v_x1, v_x2))
            return (path, solved_matrix)
def main():
    maze_matrix =   [['S', '#', '#'],
                     ['.', 'X', '.'],
                     ['.', '#', 'F']]
    maze = Maze(maze_matrix)
    path, matrix = maze.solve()
    for row in matrix:
        print(row)

    maze_matrix =   [['S', '#','.', '.', 'X', '#', '#','.'],
                     ['.', 'X','#', '.', 'X', '#', '#', '.'],
                     ['.', '.','.', '.', '.', '#', 'X', '.'],
                     ['.', 'X','X', '#', 'X', '.', 'X', '.'],
                     ['#', '.','.', '.', 'X', '.', 'X', '.'],
                     ['.', 'X','#', '#', '.', '#', '.', '.'],
                     ['.', '#','.', '.', 'X', '.', '#', '.'],
                     ['.', '#','.', '.', 'X', '#', '#', 'F']]
    maze = Maze(maze_matrix)
    path, matrix = maze.solve()
    for row in matrix:
        print(row)
if __name__== "__main__":
    main()
