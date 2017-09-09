import random, pprint, pygame
from framework.node import Node
from framework.director import Director
from pygame.locals import *

def find(father, x):
    if father[x] != x:
        father[x] = find(father, father[x])
    return father[x]


def combine(father, x, y):
    x = find(father, x)
    y = find(father, y)
    if x != y:
        father[x] = y


class MazeImp:
    def __init__(self):
        self.__data = []

    def generate_kruskal(self, size):
        father = [row * size[1] + col for row in range(size[0]) for col in range(size[1])]
        maze = [1] * (size[0] * size[1])
        walls = []
        for row in range(1, size[0] - 1, 2):
            for col in range(1, size[1] - 1, 2):
                if row >= 3:
                    walls.append((row, col, row - 2, col))
                if row <= size[0] - 4:
                    walls.append((row, col, row + 2, col))
                if col >= 3:
                    walls.append((row, col, row, col - 2))
                if col <= size[1] - 4:
                    walls.append((row, col, row, col + 2))
        random.shuffle(walls)
        for wall in walls:
            u = (wall[0], wall[1])
            uid = u[0] * size[1] + u[1]
            v = (wall[2], wall[3])
            vid = v[0] * size[1] + v[1]
            maze[uid] = 0
            maze[vid] = 0
            if find(father, uid) != find(father, vid):
                maze[(wall[0] + wall[2]) // 2 * size[1] + (wall[1] + wall[3]) // 2] = 0
                combine(father, uid, vid)
        return maze

    def simple_generate(self, size, start=(0, 0), end=None):
        if end is None:
            end = (size[0] - 1, size[1] - 1)
        data = []
        for row in range(size[0]):
            rowdata = []
            for col in range(size[1]):
                if (row, col) == start or (row, col) == end:
                    rowdata.append(0)
                else:
                    rowdata.append(random.randint(0, 1))
            data.append(rowdata)
        return data

    def check(self, data, start=(0, 0), end=None):
        size = (len(data), len(data[0]))
        if end is None:
            end = (size[0] - 1, size[1] - 1)
        inq = {}
        q = []
        q.append(start)
        inq[start] = True
        while len(q) > 0:
            cur = q.pop(0)
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nxt = (cur[0] + offset[0], cur[1] + offset[1])
                if nxt[0] < 0 or nxt[0] >= size[0] or nxt[1] < 0 or nxt[1] >= size[1]:
                    continue
                if nxt == end: return True
                if data[nxt[0]][nxt[1]] != 1 and (nxt not in inq):
                    inq[nxt] = True
                    q.append(nxt)
        return False


class Maze(Node):
    def init(self):
        self.imp = MazeImp()
        self.maze_size = (9, 11)
        self.data = self.imp.generate_kruskal(self.maze_size)
        self.end = (self.maze_size[0] - 2, self.maze_size[1] - 2)
        for row in range(self.maze_size[0]):
            for col in range(self.maze_size[1]):
                print(self.data[row * self.maze_size[1] + col], end=" ")
            print()
        self.tile_images = {}
        self.tile_images[1] = pygame.image.load("wall.png").convert_alpha()
        self.tile_images[0] = pygame.Surface((75, 75)).convert_alpha()
        size = self.maze_size
        width = 75
        height = 75
        self.image = pygame.Surface(Director.instance().resolution)
        for row in range(size[0]):
            for col in range(size[1]):
                self.image.blit(self.tile_images[self.data[row * size[1] + col]],
                          Rect(col * width, row * height, width, height))


if __name__ == "__main__":
    imp = MazeImp()
    size = (11, 11)
    maze = imp.generate_kruskal(size)
    for row in range(size[0]):
        for col in range(size[1]):
            print(maze[row * size[1] + col], end=" ")
        print()
