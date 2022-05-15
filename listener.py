import threading, config

# Classes not mine
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()
class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        ch = ''
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()
getch = _Getch()

def inputHandler():
  while True:
    if thread.userInput == config.quit: break
    if thread.isDone: break
    thread.userInput = getch()

def getInput():
    retVal = thread.userInput
    thread.userInput = ''
    return retVal

def endListen(): 
    thread.isDone = True

thread = threading.Thread(name='listener',target=inputHandler)
thread.userInput = ''
thread.isDone = False

