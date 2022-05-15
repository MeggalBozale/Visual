
# Where you want stuff to go.
#stem = "./images/"
#out  = "./text/"
#tmp  = "./tmp/"
#saved = "./saved/"
#palettes = "./palettes/"

stem = '.'
out  = '.'
tmp  = '.'
saved = '.'
palettes = './palettes/'

# Provides the palette for 256 color mode
file256 = palettes+"256.txt"

#May provide automatic switching from Linux to Windows/Mac codes later.
lnup       = "\x1b[F" 
newln      = "\n\r"    # For prints where we need to make extra sure we are ALL the way to the left.
returnLeft = '\r'
resetColor = "\x1b[0m"

# Interactive session controls
move = ('w','a','s','d')
moveScale = 0.01 # How far you move by w/h * scale. (eg. 0.1 = 1/10th of the image at a time.)
moveDirs = ('up','left','down','right')


# Enable the following for numpad movement:
'''
move = (7,8,9,4,6,1,2,3)
moveScale = 0.1
moveDirs = ('upleft','up','upright','left','right','downleft','down','downright')
'''

# Warn mac users that I don't use mac and thus dont care
warnMacOS = True

zoom = ('i','o')
zoomDirs = ('+','-')
zoomScale = 0.05 # added to zoom level. 

save = '='
quit = 'q'

# Misc
pixels = '██' # █
escapeChr = '\x1b'
pixelRatio = (1,1) # x per y
listen = True # listen to keyboard inputs

colors = [ # Many terminals change the first 16 colors. Adjust this to your liking! (TODO: automatically detect colors in this range)
(  0,  0,  0), # 1-8 (Standard)
(255,  0,  0),
(  0,255,  0),
(255,255,  0),
(  0,  0,255),
(255,  0,255),
(  0,255,255),
(200,200,255),

(128,128,128), # 9-16 (Light)
(255,128,128),
(128,255,128),
(255,255,128),
(128,128,255),
(128,255,255),
(255,255,255)]