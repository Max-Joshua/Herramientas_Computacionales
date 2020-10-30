"""
Modified version of "paint" game. (Taken from freegames.com)
by:
Joshua Amaya
José Derbez
Alejandro Fernandez
"""
from turtle import *
from freegames import vector
import math

def line(start, end):
    "Draw line from start to end."
    up()
    goto(start.x, start.y)
    down()
    goto(end.x, end.y)

def square(start, end):
    "Draw square from start to end."
    up()
    goto(start.x, start.y)
    down()
    begin_fill()

    for count in range(4):
        forward(end.x - start.x)
        left(90)

    end_fill()

def drawCircle(start, end):
    "Draw circle from start as centerpoint, to end as radious."

    radious = math.sqrt((start.x - end.x) ** 2 + (start.y - end.y) ** 2) # get the radious of the ball by using pythagoras theorum

    up() # stop drawing 
    goto(start.x, start.y - radious) # go to the point at the bottom of the circle, because turtle starts drawing there
    down()

    begin_fill() 

    circle(radious) # make the circle

    end_fill()

def rectangle(start, end):
    "Draw rectangle from start to end."
    up()
    goto(start.x, start.y)
    begin_fill()
    goto(end.x, end.y)
    
    begin_fill()
    
    for count in range(2):
        forward(end.x - start.x)
        left(90)
        forward(end.y - 2 * start.y)
        left(90)
    end_fill()
    
   

    end_fill()

def triangle(start, end):
    "Draw triangle from start to end."
    step = end.x - start.x
    up()
    goto(start.x, start.y)
    begin_fill()
    goto(end.x, end.y)
    goto(start.x + 2*step,start.y)
    goto(start.x, start.y)
    end_fill()

def tap(x, y):
    "Store starting point or draw shape."
    start = state['start']

    if start is None:
        state['start'] = vector(x, y)
    else:
        shape = state['shape']
        end = vector(x, y)
        shape(start, end)
        state['start'] = None

def store(key, value):
    "Store value in state at key."
    state[key] = value

state = {'start': None, 'shape': line}
setup(420, 420, 370, 0)
onscreenclick(tap)
listen()
onkey(undo, 'u')
onkey(lambda: color('black'), 'K')
onkey(lambda: color('white'), 'W')
onkey(lambda: color('green'), 'G')
onkey(lambda: color('blue'), 'B')
onkey(lambda: color('red'), 'R')
onkey(lambda: color('yellow'), 'Y')
onkey(lambda: store('shape', line), 'l')
onkey(lambda: store('shape', square), 's')
onkey(lambda: store('shape', drawCircle), 'c')
onkey(lambda: store('shape', rectangle), 'r')
onkey(lambda: store('shape', triangle), 't')
done()
