import sys
import random

class point:
  def __init__(self, num, x, y):
    self.num = num
    self.x = x
    self.y = y

  def dist(self, other):
    return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** .5

  def __str__(self):
    return "[" + str(self.x) + ", " + str(self.y) + "]"

class path:
  def __init__(self, size):
    self.size = size
    self.order = []
    self.l = 0
    self.fitness = "placeholder"


class cities:
  def __init__(self):
    self.size = "placeholder"
    self.min = "placeholder"
    self.optimal = "placeholder"
    self.points = []
    self.distances = []
    self.label = sys.argv[1]
    self.numPaths = "placeholder"
    self.numGenerations = "placeholder"
    self.mutation = "placeholder"
    self.paths = []
    self.wheel = []
    self.pairs = []
    self.shortest = "placeholder"
    self.shortestLength = "placeholder"
    self.initEverything()


  def initEverything(self):
    file = open("points.csv", "r")
    lines = file.readlines()
    cline = 0
    for i in range(len(lines)):
      if lines[i][:len(self.label)] == self.label:
        cline = i
        break
    clines = lines[cline:cline + 4]
    for i in range(4):
      clines[i] = clines[i].replace("\n", "").split(",")
    self.size = len(clines[1])
    self.min = float(clines[0][1])
    for i in range(self.size):
      p = point(i, int(clines[1][i]), int(clines[2][i]))
      self.points.append(p)
    self.initOptimal(clines[3])
    self.initDistances()
    self.initOtherStuff()
    self.paths = self.genNRandomPaths(self.numPaths)

  def initOptimal(self, ord):
    p = path(self.size)
    for i in ord: p.order.append(int(i))
    p.l = self.min
    self.optimal = p

  def initDistances(self):
    for i in range(self.size):
      self.distances.append([])
      for x in range(self.size):
        if x <= i: self.distances[i].append(0)
        else: self.distances[i].append(self.points[i].dist(self.points[x]))

  def initOtherStuff(self):
    self.numPaths = 300
    self.numGenerations = 10000
    self.mutation = .05
    self.wheel = [0] * self.numPaths
    self.shortest = self.genRandomPath()
    self.shortestLength = self.shortest.l

  def dist(self, p1, p2):
    if p1 > p2: return self.distances[p2][p1]
    else: return self.distances[p1][p2]

  def calcPathLength(self, path):
    path.l = 0
    for i in range(path.size - 1):
      path.l += self.dist(path.order[i], path.order[i + 1])
    path.l += self.dist(path.order[0], path.order[-1])
    path.fitness = (1.0 / path.l) ** 6
      #print(self.dist(path.order[i], path.order[i + 1]))

  def genRandomPath(self):
    p = path(self.size)
    temp = []
    for i in range(self.size): temp.append(i)
    while (len(temp) > 0):
      current = random.choice(temp)
      temp.remove(current)
      p.order.append(current)
    self.calcPathLength(p)
    return p

  def genNRandomPaths(self, n):
    paths = []
    for i in range(n):
      paths.append(self.genRandomPath())
    return paths

  def genRandomPaths(self):
    shortest = self.genRandomPath()
    current = None
    while True:
      if shortest.l <= self.optimal.l: return shortest
      current = self.genRandomPath()
      if current.l < shortest.l:
        shortest = current
        print(shortest.l)

  def calcFitnesses(self):
    smallest = self.paths[0].fitness
    for i in range(1, self.numPaths):
      if self.paths[i].fitness < smallest: smallest = self.paths[i].fitness
    factor = 1.0 / smallest
    for i in range(self.numPaths): self.paths[i].fitness = int(self.paths[i].fitness * factor)

  def modWheel(self):
    total = 0
    for i in range(self.numPaths):
      total += self.paths[i].fitness
      self.wheel[i] = total

  def selectRandom(self):
    n = random.randint(0, self.wheel[-1] - 1)
    if n < self.wheel[0]: return 0
    for i in range(len(self.wheel)):
      if self.wheel[i] <= n and n < self.wheel[i + 1]: return i + 1
    return "error"

  def selectNotN(self, n):
    while True:
      possible = self.selectRandom()
      if possible != n: return possible

  def selectPairs(self):
    self.pairs = []
    for i in range(self.numPaths):
      father = self.selectRandom()
      mother = self.selectNotN(father)
      pair = [father, mother]
      self.pairs.append(pair)
    # ary = []
    # for i in range(self.numPaths): ary.append(0)
    # for i in range(self.numPaths):
    #   ary[pairs[i][0]] += 1
    #   ary[pairs[i][1]] += 1

  def mate(self):
    tempPaths = []
    for pair in self.pairs:
      first,second = self.paths[pair[0]].order,self.paths[pair[1]].order
      numCities = random.randint(0, int(self.size * .8))
      idx = random.randint(0, self.size - numCities)
      temp = [-500] * idx + first[idx:idx + numCities]
      temp += [-500] * (self.size - numCities - idx)
      secondIdx = idx + numCities
      tempIdx = idx + numCities
      if tempIdx == len(temp):
        tempIdx = 0
        secondIdx = 0
      while temp[tempIdx] == -500:
        if second[secondIdx] not in temp:
          temp[tempIdx] = second[secondIdx]
          if tempIdx != len(temp) - 1: tempIdx += 1
          else: tempIdx = 0
          if secondIdx != len(second) - 1: secondIdx += 1
          else: secondIdx = 0
        else:
          if secondIdx != len(second) - 1: secondIdx += 1
          else: secondIdx = 0
      p = path(self.size)
      p.order = temp
      self.calcPathLength(p)
      tempPaths.append(p)
    self.paths = tempPaths

  def mutate(self):
    for p in range(len(self.paths)):
      mutate = random.random()
      if mutate < self.mutation:
        idx1 = random.randint(0, self.size - 1)
        idx2 = random.randint(0, self.size - 1)
        self.paths[p].order[idx1],self.paths[p].order[idx2] = self.paths[p].order[idx2],self.paths[p].order[idx1]

  def findBest(self):
    newShortest = False
    for i in range(self.size):
      if self.paths[i].l < self.shortestLength:
        self.shortest = self.paths[i]
        self.shortestLength = self.shortest.l
        newShortest = True
    if newShortest: print(self.shortestLength)

  def cycle(self):
    self.calcFitnesses()
    self.modWheel()
    self.selectPairs()
    self.mate()
    self.mutate()
    self.findBest()

  def run(self):
    for i in range(self.numGenerations): self.cycle()


c = cities()
c.run()
print(c.shortest.order)
# for i in range(len(c.paths)): print(c.paths[i].fitness)
# print(c.wheel)
#print(c.genRandomPaths())
#possible fitness function:
#(1/x)^n * whatever is needed to get smallest value to one
#n will be small integer (2-4)
