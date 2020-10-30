"""
Modified version of "cannonball" game. (Taken from freegames.com)
by:
Joshua Amaya
José Derbez
Alejandro Fernandez
"""

from random import randrange
from turtle import *
from freegames import vector

ball = vector(-200, -200)
speed = vector(0, 0)
targets = []
score = 0 # we need to keep track of the score someway

def tap(x, y):
    "Respond to screen tap."
    if not inside(ball):
        ball.x = -199
        ball.y = -199
        speed.x = (x + 400) / 25
        speed.y = (y + 400) / 25

def inside(xy):
    "Return True if xy within screen."
    return -200 < xy.x < 200 and -200 < xy.y < 200

def draw():
    "Draw ball and targets."
    clear()

    for target in targets:
        goto(target.x, target.y)
        dot(20, 'blue')

    if inside(ball):
        goto(ball.x, ball.y)
        dot(6, 'red')

    update()

def move():
    "Move ball and targets."
    global score # make sure the variable is readable inside the function!
    if randrange(40) == 0:
        y = randrange(-150, 150)
        target = vector(200, y)
        targets.append(target)

    for target in targets:
        target.x -= 4

    if inside(ball):
        speed.y -= 0.8
        ball.move(speed)

    dupe = targets.copy()
    targets.clear()

    for target in dupe:
        if abs(target - ball) > 13:
            targets.append(target)
        else:
            # if the target is not drawn, it means that it was killed, so we sum one to score
            score += 1
            print(f'score: {score}')

    draw()

    for target in targets:
        if not inside(target):
           return



    ontimer(move, 50)

setup(420, 420, 370, 0)
hideturtle()
up()
tracer(False)
onscreenclick(tap)
move()
done()
