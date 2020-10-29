import pyglet, os

width = 1500
height = 800

window = pyglet.window.Window(1500, 800, resizable=False, vsync=True)

class imagesLoader:
    spriteDict = {}
    def __init__(self):
        self.imgDict = {}
        """Cretes a image dictionary ready to be used in pyglet. 

        ONLY .png FILES ARE SUPPORTED"""
        print('loading images')
        files = []
        for root, dirs, foundFiles in os.walk("game/img", topdown=False):
            for name in foundFiles:
                if name.endswith('.png'):
                    files.append(name)

        for file in files:
            self.imgDict[file[:-4]] = pyglet.image.load('game/img/' + file)
            self.spriteDict[file[:-4]] = pyglet.sprite.Sprite(img = self.imgDict[file[:-4]])
        print('images loaded')

class object:
    x = 0
    y = 0
    xVel = 0
    yVel = 0
    xAxcel = 0
    yAxcel = 0
    drag = 10
    def __init__( self, spriteImg, x : float = 0, y : float = 0):
        self.x = x
        self.y = y
        self.sprite = spriteImg

    def calculateNextPoint(self):
        self.xVel += self.xAxcel * physiscDeltaTime - self.xVel / self.drag
        self.yVel += self.yAxcel * physiscDeltaTime - self.yVel / self.drag
        self.x += self.xVel * physiscDeltaTime
        self.y += self.yVel * physiscDeltaTime
        self.sprite.x = self.x
        self.sprite.y = self.y

class staticObject:
    pass

images = imagesLoader()

objects = []

objects.append(object(images.spriteDict['test']))

@window.event
def on_draw():
    window.clear()
    for object in objects:
        object.sprite.draw()

moveForce = 500

@window.event
def on_key_press(symbol, modifiers):
    if symbol == 97: # if pressed the A key
        objects[0].xAxcel -= moveForce
    if symbol == 119: # if pressed the W key
        print("W is pressed!")

    if symbol == 100: # if pressed the D key
        objects[0].xAxcel += moveForce

    if symbol == 115: # if pressed the S key
        print("S is pressed!")

@window.event
def on_key_release(symbol, modifiers):
    if symbol == 97: # if pressed the A key
        objects[0].xAxcel = 0
    if symbol == 119: # if pressed the W key
        print("W is pressed!")

    if symbol == 100: # if pressed the D key
        objects[0].xAxcel = 0

    if symbol == 115: # if pressed the S key
        print("S is pressed!")

gravity = 5
physiscDeltaTime = 0.02

def runPhysics(dx):
    for object in objects:
        '''
        object.yAxcel -= gravity
        '''
        object.calculateNextPoint()

pyglet.clock.schedule_interval(runPhysics, physiscDeltaTime)

pyglet.app.run()