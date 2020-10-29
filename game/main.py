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
    sprite = pyglet.sprite.Sprite
    def __init__(self, x : float, y : float, sprite : pyglet.sprite.Sprite):
        self.x = x
        self.y = y
        self.sprite = sprite

images = imagesLoader()

@window.event
def on_draw():
    window.clear()
    images.spriteDict['test'].draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == 97: # if pressed the A key
        print("a is pressed!")

    if symbol == 119: # if pressed the W key
        print("W is pressed!")

    if symbol == 100: # if pressed the D key
        print("D is pressed!")

    if symbol == 115: # if pressed the S key
        print("S is pressed!")

pyglet.app.run()