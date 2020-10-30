import pyglet, os, json, random

width = 1500
height = 800

window = pyglet.window.Window(1500, 800, resizable=False, vsync=True)

drawGroup0 = pyglet.graphics.OrderedGroup(0)
drawGroup1 = pyglet.graphics.OrderedGroup(1)
drawGroup2 = pyglet.graphics.OrderedGroup(2)

mainBatch = pyglet.graphics.Batch()
bkgBatch = pyglet.graphics.Batch()
bkgBatch1 = pyglet.graphics.Batch()

objects = []

plataforms = []

def gameStarter():
    print("starting game!")
    global objects, plataforms, drawGroup0,drawGroup1,drawGroup2, mainBatch, bkgBatch, bkgBatch1

    drawGroup0 = pyglet.graphics.OrderedGroup(0)
    drawGroup1 = pyglet.graphics.OrderedGroup(1)
    drawGroup2 = pyglet.graphics.OrderedGroup(2)

    mainBatch = pyglet.graphics.Batch()
    bkgBatch = pyglet.graphics.Batch()
    bkgBatch1 = pyglet.graphics.Batch()

    objects = []
    plataforms = []

    with open('game/information.json') as file:
        info = json.load(file)

    objects.append(object(images.imgDict['Protagonist'], mainBatch, info['player']['x'], info['player']['y']))

    for enemy in info['levels'][info['player']['currentlvl']]['enemies']:
        if enemy['type'] == 0:
            objects.append(object(images.imgDict['Enemie0'], mainBatch, enemy['x'], enemy['y'], enemy["HP"]))
        elif enemy['type'] == 1:
            objects.append(object(images.imgDict['Enemie1'], mainBatch, enemy['x'], enemy['y'], enemy["HP"]))

    for plataform in info['levels'][info['player']['currentlvl']]['objects']:
        plataforms.append(staticObject(plataform['x'], plataform['y'], plataform['width'], plataform['height'], images.imgDict['Platform'], images.imgDict['Platform_rocks']))

    for monster in objects[1:]:
        monster.moveMonster()

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
            #self.spriteDict[file[:-4]] = pyglet.sprite.Sprite(img = self.imgDict[file[:-4]], batch = mainBatch)
        print('images loaded')

class object:
    x = 0
    y = 0
    xVel = 0
    yVel = 0
    xAxcel = 0
    yAxcel = 0
    drag = 10
    gravityActive = True
    canJump = False

    width = 0
    height = 0

    HP = 100
    def __init__( self, spriteImg, batch, x : float = 0, y : float = 0, HP : int = 100):
        self.x = x
        self.y = y
        self.sprite = pyglet.sprite.Sprite(img = spriteImg, batch = batch)
        self.HP = HP

        self.width = self.sprite.width
        self.height = self.sprite.height

    def calculateNextPoint(self):
        self.xVel += self.xAxcel * physiscDeltaTime - self.xVel / self.drag
        self.yVel += self.yAxcel * physiscDeltaTime - self.yVel / self.drag
        self.x += self.xVel * physiscDeltaTime
        self.y += self.yVel * physiscDeltaTime

        if self.xVel > 0:
            look = 1
            offset = 0
        else:
            look = -1
            offset = self.sprite.width

        self.sprite.x = self.x + offset
        self.sprite.y = self.y
        self.sprite.update(scale_x = look)

    def moveMonster(self, dx = None):
        self.xVel = random.randint(-500,500)
        self.yVel = random.randint(100,800)
        pyglet.clock.schedule_once(self.moveMonster, random.randint(2,10))
    
    def checkCollisions(self):
        activateGravity = False
        if self.x < 0:
            self.x = 0
            self.xVel = 0
            self.xAxcel = 0
        elif self.x > width - self.sprite.width:
            self.x = width - self.sprite.width
            self.xVel = 0
            self.xAxcel = 0
        
        if self.y < 0:
            self.y = 0
            self.yVel = 0
            self.yAxcel = 0
            activateGravity = True
        elif self.y <= 0:
            activateGravity = True
        elif self.y > height - self.sprite.height:
            self.y = height - self.sprite.height
            self.yVel = 0
            self.yAxcel = 0

        for plataform in plataforms:
            if plataform.x - self.sprite.width < self.x < plataform.x + plataform.width:
                if plataform.y - self.sprite.height < self.y < plataform.y + plataform.height:
                    # chech best way to throw the player to
                    offsetRenderer = 5
                    if plataform.x - self.sprite.width  + offsetRenderer <= self.x <= plataform.x + plataform.width - 20:
                        if plataform.y + plataform.height - 2 > self.y > plataform.y:
                            self.y = plataform.y + plataform.height - 1
                            self.yAxcel = 0
                            self.yVel = 0
                            activateGravity = True
                        elif self.y < plataform.y:
                            self.y = plataform.y - self.sprite.height
                            self.yAxcel = 0
                            self.yVel = 0
                        
                        if plataform.y + plataform.height >= self.y > plataform.y:
                            activateGravity = True

                    if plataform.y - self.sprite.height  + offsetRenderer <= self.y <= plataform.y + plataform.height - offsetRenderer:
                        activateGravity = True
                        if self.x + self.sprite.width / 2 < plataform.x + plataform.width / 2:
                            self.x -= offsetRenderer - 1
                            self.xVel = 0
                            self.xAxcel = 0
                        else:
                            self.x += offsetRenderer - 1
                            self.xVel = 0
                            self.xAxcel = 0

        if activateGravity:
            self.canJump = True
            self.gravityActive = False
        else:
            self.gravityActive = True

    def checkCollisionWithList(self, list, action):
        for object in list:
            if object.x - self.sprite.width < self.x < object.x + object.width:
                if object.y - self.sprite.height < self.y < object.y + object.height:
                    action()

def killPlayer():
    print('player died!')
    gameStarter()

class staticObject:
    x = 0
    y = 0
    width = 0
    height = 0

    def __init__(self, x, y, width, height, spriteImg, secondarySpriteImg):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.sprites = [pyglet.sprite.Sprite(img = spriteImg, batch = bkgBatch)]
        self.bkgSprites = []
        scale = self.width / (self.width // self.sprites[0].width + 1) / self.sprites[0].width
        self.sprites[0].update(x=self.x, y=self.y + self.height - self.sprites[0].height,scale_x=scale)

        for i in range(1, self.width // self.sprites[0].width + 1):
            self.sprites.append(pyglet.sprite.Sprite(img = spriteImg, batch = bkgBatch))
            self.sprites[i].update(x=self.x + scale * self.sprites[0].width * i, y=self.y + self.height - self.sprites[0].height, scale_x = scale)

        if self.height // self.sprites[0].height > 0:
            for Y in range(0, self.height // self.sprites[0].height):
                for i in range(0, self.width // self.sprites[0].width + 1):
                    self.bkgSprites.append(pyglet.sprite.Sprite(img = secondarySpriteImg, batch = bkgBatch1, group = drawGroup2))
                    self.bkgSprites[i + Y * (self.height // self.sprites[0].height) ].update(x = self.x + scale * self.sprites[0].width * i, y = self.y - 5 , scale_x = scale)

@window.event
def on_draw():
    global bkgBatch, mainBatch
    window.clear()
    bkgBatch1.draw()
    bkgBatch.draw()
    mainBatch.draw()


moveForce = 1000

@window.event
def on_key_press(symbol, modifiers):
    if symbol == 97: # if pressed the A key
        objects[0].xAxcel -= moveForce
    if symbol == 119: # if pressed the W key
        if objects[0].canJump:
            objects[0].yAxcel = 2000
            objects[0].yVel = 500
            objects[0].canJump = False

    if symbol == 100: # if pressed the D key
        objects[0].xAxcel += moveForce

    if symbol == 115: # if pressed the S key
        print("S is pressed!")

@window.event
def on_key_release(symbol, modifiers):
    if symbol == 119: # if pressed the W key
        if objects[0].yAxcel > 0:
            objects[0].yAxcel = 0
    if symbol == 97: # if pressed the A key
        objects[0].xAxcel = 0

    if symbol == 100: # if pressed the D key
        objects[0].xAxcel = 0

gravity = 100
maxGravity = -10000
physiscDeltaTime = 0.02

def runPhysics(dx):

    objects[0].checkCollisionWithList(objects[1:], killPlayer)
    
    for object in objects:
        if object.gravityActive:
            if object.yAxcel > maxGravity:
                object.yAxcel -= gravity

        object.checkCollisions()
        object.calculateNextPoint()

images = imagesLoader()
gameStarter()

pyglet.clock.schedule_interval(runPhysics, physiscDeltaTime)

pyglet.app.run()