from HumanClass import Human
from time import sleep, time
import random

human = Human(0, 0, 0, 0)

while True:
    x = random.randint(-10, 10)
    y = random.randint(-10, 10)
    curtime = time()
    human.update(x, y, curtime)
    human.visualize()
    sleep(1)