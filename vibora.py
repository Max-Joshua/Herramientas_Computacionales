"""
Modified version of "snake" game. (Taken from freegames.com)
by:
Joshua Amaya
José Derbez
Alejandro Fernandez
"""

import math
from turtle import *
from random import randrange
from random import shuffle
from freegames import square, vector

food = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)
colors = ["green", "blue", "yellow", "grey", "black"]
shuffle(colors)

gameSpood = 100 # a speed variable that will get changed later

def change(x, y):
    "Change snake direction."
    aim.x = x
    aim.y = y

def inside(head):
    "Return True if head inside boundaries."
    return -200 < head.x < 200 and -200 < head.y < 200

def move():
    "Move snake forward one segment."
    head = snake[-1].copy()
    head.move(aim)

    if not inside(head): # if not inside the playing field 
        if not -200 < head.x < 200: # on x
            head = vector(-head.x, head.y) # tp head to other side
        if not -200 < head.y < 200: # on y
            head = vector(head.x, -head.y) # tp head to other side

    if head in snake:
        square(head.x, head.y, 9, 'red')
        update()
        return

    snake.append(head)

    if head == food:
        print('Snake:', len(snake))
        food.x = randrange(-15, 15) * 10
        food.y = randrange(-15, 15) * 10
    else:
        snake.pop(0)

    clear()

    for body in snake:
        square(body.x, body.y, 9, colors[0])

    square(food.x, food.y, 9, colors[1])
    update()
    # calculate speed to go fater when more food is present:
    gameSpood = 100 - math.log(len(snake), 1.1)
    ontimer(move, int(gameSpood))

setup(420, 420, 370, 0)
hideturtle()
tracer(False)
listen()
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')
move()
done()
