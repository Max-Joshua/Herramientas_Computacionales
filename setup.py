import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if sys.version_info[0] >= 3 and sys.version_info[1] >= 8 or sys.version_info[0] > 3:
    print('python version meets minimum requirements')
else:
    print('python version 3.8+ is requiered. please install it at: https://www.python.org/ to proceed.')
    exit()

try:
    import pyglet
    print('All software requirements are met, not runing any extra procceses.')
    doTheExit = True
except:
    print("Not all software requirements met!")
    doTheExit = False

if doTheExit:
    exit()

if not input('Would you like to continue with auto installation? (y/n) ') == 'y':
    print('exiting...')
    exit()

print('testing for pyglet')

try:
    import pyglet
    print('pyglet is installed!')

except:
    print("pyglet is not installed, installing...")
    install('pyglet')
