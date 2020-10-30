"""
thieves' hole redeem is a plataformer game, where magic and bad guys collide!
Have fun going through different dungeos to save your loved one.

thieves' hole redeem by Alejandro Fernandez del Valle Herrera, Joshua Rubén Amaya Camilo and José Emilio Derbez Safie 
is licensed under CC BY 4.0. To view a copy of this license, visit https://creativecommons.org/licenses/by/4.0 
"""

import pyglet, os, json, random



#  /$$    /$$                    /$$           /$$       /$$                    
# | $$   | $$                   |__/          | $$      | $$                    
# | $$   | $$ /$$$$$$   /$$$$$$  /$$  /$$$$$$ | $$$$$$$ | $$  /$$$$$$   /$$$$$$$
# |  $$ / $$/|____  $$ /$$__  $$| $$ |____  $$| $$__  $$| $$ /$$__  $$ /$$_____/
#  \  $$ $$/  /$$$$$$$| $$  \__/| $$  /$$$$$$$| $$  \ $$| $$| $$$$$$$$|  $$$$$$ 
#   \  $$$/  /$$__  $$| $$      | $$ /$$__  $$| $$  | $$| $$| $$_____/ \____  $$
#    \  $/  |  $$$$$$$| $$      | $$|  $$$$$$$| $$$$$$$/| $$|  $$$$$$$ /$$$$$$$/
#     \_/    \_______/|__/      |__/ \_______/|_______/ |__/ \_______/|_______/ 

width = 1500
height = 800

mana = 5

window = pyglet.window.Window(1500, 800, resizable=False, vsync=True)

drawGroup0 = pyglet.graphics.OrderedGroup(0)
drawGroup1 = pyglet.graphics.OrderedGroup(1)
drawGroup2 = pyglet.graphics.OrderedGroup(2)

mainBatch = pyglet.graphics.Batch()
bkgBatch = pyglet.graphics.Batch()
bkgBatch1 = pyglet.graphics.Batch()
projectileBatch = pyglet.graphics.Batch()

objects = []

projectiles = []

plataforms = []

def gameStarter():
    '''
    Creates al the fundamental things in the level. 

    Checks JSON file, to create and load the current level.
    '''
    print("starting game!")
    global objects, plataforms, drawGroup0,drawGroup1,drawGroup2, mainBatch, bkgBatch, bkgBatch1, mana

    # reset pyglet batches for optimazation
    drawGroup0 = pyglet.graphics.OrderedGroup(0)
    drawGroup1 = pyglet.graphics.OrderedGroup(1)
    drawGroup2 = pyglet.graphics.OrderedGroup(2)

    mainBatch = pyglet.graphics.Batch()
    bkgBatch = pyglet.graphics.Batch()
    bkgBatch1 = pyglet.graphics.Batch()

    # reset game objects
    objects = []
    plataforms = []

    mana = 5

    # load JSON file
    with open('game/information.json') as file:
        info = json.load(file)

    objects.append(object(images.imgDict['Protagonist'], mainBatch, info['player']['x'], info['player']['y'])) # create player


    # create enemies
    for enemy in info['levels'][info['player']['currentlvl']]['enemies']:
        if enemy['type'] == 0: # nice
            objects.append(object(images.imgDict['Enemie0'], mainBatch, enemy['x'], enemy['y'], enemy["HP"]))
        elif enemy['type'] == 1:
            objects.append(object(images.imgDict['Enemie1'], mainBatch, enemy['x'], enemy['y'], enemy["HP"]))

    # create plataforms
    for plataform in info['levels'][info['player']['currentlvl']]['objects']:
        plataforms.append(staticObject(plataform['x'], plataform['y'], plataform['width'], plataform['height'], images.imgDict['Platform'], images.imgDict['Platform_rocks']))

    # start monser AI
    for monster in objects[1:]:
        monster.moveMonster()

#  /$$$$$$                                            
# |_  $$_/                                            
#   | $$   /$$$$$$/$$$$   /$$$$$$   /$$$$$$   /$$$$$$ 
#   | $$  | $$_  $$_  $$ |____  $$ /$$__  $$ /$$__  $$
#   | $$  | $$ \ $$ \ $$  /$$$$$$$| $$  \ $$| $$$$$$$$
#   | $$  | $$ | $$ | $$ /$$__  $$| $$  | $$| $$_____/
#  /$$$$$$| $$ | $$ | $$|  $$$$$$$|  $$$$$$$|  $$$$$$$
# |______/|__/ |__/ |__/ \_______/ \____  $$ \_______/
#                                  /$$  \ $$          
#                                 |  $$$$$$/          
#                                  \______/           


class imagesLoader:
    spriteDict = {}
    def __init__(self):
        
        """Cretes a image dictionary ready to be used in pyglet. 

        ONLY .png FILES ARE SUPPORTED"""
        print('loading images')
        self.imgDict = {}
        files = []
        for root, dirs, foundFiles in os.walk("game/img", topdown=False):
            for name in foundFiles:
                if name.endswith('.png'):
                    files.append(name)

        for file in files:
            self.imgDict[file[:-4]] = pyglet.image.load('game/img/' + file)
            #self.spriteDict[file[:-4]] = pyglet.sprite.Sprite(img = self.imgDict[file[:-4]], batch = mainBatch)
        print('images loaded')



#   /$$$$$$  /$$                                                /$$                                  
#  /$$__  $$| $$                                               | $$                                  
# | $$  \__/| $$$$$$$   /$$$$$$   /$$$$$$  /$$$$$$   /$$$$$$$ /$$$$$$    /$$$$$$   /$$$$$$   /$$$$$$$
# | $$      | $$__  $$ |____  $$ /$$__  $$|____  $$ /$$_____/|_  $$_/   /$$__  $$ /$$__  $$ /$$_____/
# | $$      | $$  \ $$  /$$$$$$$| $$  \__/ /$$$$$$$| $$        | $$    | $$$$$$$$| $$  \__/|  $$$$$$ 
# | $$    $$| $$  | $$ /$$__  $$| $$      /$$__  $$| $$        | $$ /$$| $$_____/| $$       \____  $$
# |  $$$$$$/| $$  | $$|  $$$$$$$| $$     |  $$$$$$$|  $$$$$$$  |  $$$$/|  $$$$$$$| $$       /$$$$$$$/
#  \______/ |__/  |__/ \_______/|__/      \_______/ \_______/   \___/   \_______/|__/      |_______/ 


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
    def __init__( self, spriteImg, batch, x : float = 0, y : float = 0, HP : int = 4):
        """
        creates and mantains a desired character, with the spriteImg as the sprite, it creates the sprite inside.

        x and y coordinates are used for placement in world, and HP is for hitpoints
        """
        self.x = x
        self.y = y
        self.sprite = pyglet.sprite.Sprite(img = spriteImg, batch = batch)
        self.HP = HP

        self.width = self.sprite.width
        self.height = self.sprite.height

    def calculateNextPoint(self):
        """
        Does the math for all the necesary gravity and more calculations
        """
        # calculate velocity
        self.xVel += self.xAxcel * physiscDeltaTime - self.xVel / self.drag 
        self.yVel += self.yAxcel * physiscDeltaTime - self.yVel / self.drag

        # calculate position based on previios pos and current vel
        self.x += self.xVel * physiscDeltaTime
        self.y += self.yVel * physiscDeltaTime

        # make the player look the way it should
        if self.xVel > 0:
            look = 1
            offset = 0
        else:
            look = -1
            offset = self.sprite.width

        # make the player be inside colliders
        self.sprite.x = self.x + offset
        self.sprite.y = self.y
        self.sprite.update(scale_x = look)

    def moveMonster(self, dx = None):
        """
        simple monster AI, reapeats itself untill it dies
        """
        self.xVel = random.randint(-500,500)
        self.yVel = random.randint(100,800)
        pyglet.clock.schedule_once(self.moveMonster, random.randint(2,10))
    
    def checkCollisions(self):
        """
        make sure the player does not fall of the world!
        """
        activateGravity = False # deactivates gravity if is within boundaries

        # check if inside world
        # on X
        if self.x < 0:
            self.x = 0
            self.xVel = 0
            self.xAxcel = 0
        elif self.x > width - self.sprite.width:
            self.x = width - self.sprite.width
            self.xVel = 0
            self.xAxcel = 0
        
        # on Y
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

        # check if colliding with plataform, xirst on X coordinates, then on Y
        for plataform in plataforms:
            if plataform.x - self.sprite.width < self.x < plataform.x + plataform.width:
                if plataform.y - self.sprite.height < self.y < plataform.y + plataform.height:
                    # chech best way to throw the player to
                    offsetRenderer = 5

                    # throw player up or down if withing boundaries
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

                    # throw player left or right if withing boundaries
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

        if activateGravity: # if the gravioty is deactivated or not
            self.canJump = True
            self.gravityActive = False
        else:
            self.gravityActive = True

    def checkCollisionWithList(self, list, action): 
        """
        check specified collisions and take action if colided
        """
        for object in list:
            if object.x - self.sprite.width < self.x < object.x + object.width:
                if object.y - self.sprite.height < self.y < object.y + object.height:
                    action()

    def removeHitpoints(self, amount):
        """
        remove amount of HP, if HP is 0, destroy self, with sprite
        """
        self.HP -= amount

        if self.HP == 0:
            self.destroy()
    
    def destroy(self):
        """
        destroy handler, makes sure all objects are eliminated
        """
        global mana
        self.sprite.delete()
        objects.pop(objects.index(self))
        mana = 5



#  /$$$$$$$                                               /$$     /$$ /$$          
# | $$__  $$                                             | $$    |__/| $$          
# | $$  \ $$ /$$$$$$   /$$$$$$  /$$  /$$$$$$   /$$$$$$$ /$$$$$$   /$$| $$  /$$$$$$ 
# | $$$$$$$//$$__  $$ /$$__  $$|__/ /$$__  $$ /$$_____/|_  $$_/  | $$| $$ /$$__  $$
# | $$____/| $$  \__/| $$  \ $$ /$$| $$$$$$$$| $$        | $$    | $$| $$| $$$$$$$$
# | $$     | $$      | $$  | $$| $$| $$_____/| $$        | $$ /$$| $$| $$| $$_____/
# | $$     | $$      |  $$$$$$/| $$|  $$$$$$$|  $$$$$$$  |  $$$$/| $$| $$|  $$$$$$$
# |__/     |__/       \______/ | $$ \_______/ \_______/   \___/  |__/|__/ \_______/
#                         /$$  | $$                                                
#                        |  $$$$$$/                                                
#                         \______/                                                 



class bullet:
    x = 0
    y = 0
    xVel = 500
    yVel = 0
    sprite = None
    def __init__(self, img, player : object, batch, looking: int):
        """
        starts the projectile in player position.
        looking has to be 1 or -1 to give direction
        """
        self.sprite = pyglet.sprite.Sprite(img = img, batch = batch)

        self.width = self.sprite.width
        self.height = self.sprite.height

        self.x = player.x + player.width / 2 
        self.y = player.y + player.height / 2 

        self.xVel *= looking
        self.sprite.x = self.x
        self.sprite.y = self.y

    def calculateCollisionsandNext(self, listToDestroy, otherList):
        # same as object's collision
        global physiscDeltaTime
        self.x += self.xVel * physiscDeltaTime
        self.sprite.x = self.x

        for object in listToDestroy:
            if object.x - self.sprite.width < self.x < object.x + object.width:
                if object.y - self.sprite.height < self.y < object.y + object.height:
                    object.removeHitpoints(1)
                    self.destroy()
                    break
        else:
            for object in otherList:
                if object.x - self.sprite.width < self.x < object.x + object.width:
                    if object.y - self.sprite.height < self.y < object.y + object.height:
                        self.destroy()
                        break
            else:
                if not (0 < self.x < width):
                    self.destroy()

    def destroy(self):
        # same as object's destroy
        self.sprite.delete()
        projectiles.pop(projectiles.index(self))



def killPlayer():
    objects[0].HP -= 1

    objects[0].xVel *= -5
    objects[0].yVel *= -5

    if objects[0].HP < 0:
        gameStarter()



#  /$$$$$$$  /$$             /$$                /$$$$$$                                 
# | $$__  $$| $$            | $$               /$$__  $$                                
# | $$  \ $$| $$  /$$$$$$  /$$$$$$    /$$$$$$ | $$  \__//$$$$$$   /$$$$$$  /$$$$$$/$$$$ 
# | $$$$$$$/| $$ |____  $$|_  $$_/   |____  $$| $$$$   /$$__  $$ /$$__  $$| $$_  $$_  $$
# | $$____/ | $$  /$$$$$$$  | $$      /$$$$$$$| $$_/  | $$  \ $$| $$  \__/| $$ \ $$ \ $$
# | $$      | $$ /$$__  $$  | $$ /$$ /$$__  $$| $$    | $$  | $$| $$      | $$ | $$ | $$
# | $$      | $$|  $$$$$$$  |  $$$$/|  $$$$$$$| $$    |  $$$$$$/| $$      | $$ | $$ | $$
# |__/      |__/ \_______/   \___/   \_______/|__/     \______/ |__/      |__/ |__/ |__/
                                                                                      
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



#  /$$$$$$$$                              /$$             
# | $$_____/                             | $$             
# | $$    /$$    /$$ /$$$$$$  /$$$$$$$  /$$$$$$   /$$$$$$$
# | $$$$$|  $$  /$$//$$__  $$| $$__  $$|_  $$_/  /$$_____/
# | $$__/ \  $$/$$/| $$$$$$$$| $$  \ $$  | $$   |  $$$$$$ 
# | $$     \  $$$/ | $$_____/| $$  | $$  | $$ /$$\____  $$
# | $$$$$$$$\  $/  |  $$$$$$$| $$  | $$  |  $$$$//$$$$$$$/
# |________/ \_/    \_______/|__/  |__/   \___/ |_______/ 


@window.event
def on_draw():
    # do all the draw procidures, from clearing all, to drawing all the objects
    global bkgBatch, mainBatch
    
    window.clear()

    for i in range(objects[0].HP + 1): # UwU
        hearts[i].draw()

    for i in range(mana):
        manaSprites[i].draw()

    bkgBatch1.draw()
    bkgBatch.draw()
    mainBatch.draw()
    projectileBatch.draw()


moveForce = 1000

@window.event
def on_key_press(symbol, modifiers):
    # event handlet
    global mana
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
        if mana > 0:
            projectiles.append(bullet(images.imgDict['Fire_Ball'], objects[0], projectileBatch, 1 if objects[0].xAxcel >= 0 else -1))
            mana -= 1

@window.event
def on_key_release(symbol, modifiers):
    # make sure player not keep walking right
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
    """
    Repitable action for physics jumps
    """
    objects[0].checkCollisionWithList(objects[1:], killPlayer)

    for object in projectiles:
        object.calculateCollisionsandNext(objects[1:], plataforms)
    
    for object in objects:
        if object.gravityActive:
            if object.yAxcel > maxGravity:
                object.yAxcel -= gravity

        object.checkCollisions()
        object.calculateNextPoint()



#   /$$$$$$   /$$                           /$$    
#  /$$__  $$ | $$                          | $$    
# | $$  \__//$$$$$$    /$$$$$$   /$$$$$$  /$$$$$$  
# |  $$$$$$|_  $$_/   |____  $$ /$$__  $$|_  $$_/  
#  \____  $$ | $$      /$$$$$$$| $$  \__/  | $$    
#  /$$  \ $$ | $$ /$$ /$$__  $$| $$        | $$ /$$
# |  $$$$$$/ |  $$$$/|  $$$$$$$| $$        |  $$$$/
#  \______/   \___/   \_______/|__/         \___/  
                                                 
# procidures to start game itself
images = imagesLoader()
hearts = [pyglet.sprite.Sprite(img = images.imgDict['Heart']), pyglet.sprite.Sprite(img = images.imgDict['Heart']), pyglet.sprite.Sprite(img = images.imgDict['Heart']), pyglet.sprite.Sprite(img = images.imgDict['Heart']), pyglet.sprite.Sprite(img = images.imgDict['Heart'])]

for i in range(len(hearts)):
    hearts[i].update(x= 20 * i + 25, y=height - 50, scale = 3)

manaSprites = [pyglet.sprite.Sprite(img = images.imgDict['ManaPoints']), pyglet.sprite.Sprite(img = images.imgDict['ManaPoints']), pyglet.sprite.Sprite(img = images.imgDict['ManaPoints']), pyglet.sprite.Sprite(img = images.imgDict['ManaPoints']), pyglet.sprite.Sprite(img = images.imgDict['ManaPoints'])]

for i in range(len(hearts)):
    manaSprites[i].update(x= 20 * i + 25, y=height - 100, scale = 1)

gameStarter()

pyglet.clock.schedule_interval(runPhysics, physiscDeltaTime)

pyglet.app.run()