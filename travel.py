#from classes import point, path, cities
import random

def genRandomPath(length):
  p = path(length)
  temp = []
  for i in range(length): temp.append(i)
  while (len(temp) > 0):
    current = random.choice(temp)
    temp.remove(current)
    p.order.append(current)
  print(p.order)


ary1 = [1, 2, 3]
ary2 = ary1
ary1 = []
print(ary1)
print(ary2)
