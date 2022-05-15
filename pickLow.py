'''
64 bits!
32 bits.
16 bits.
8 BITS.
4 BITS
2 BITS
ONE BIT
HALF BIT
QUARTER BIT
THE WRIST GAME
'''
import config

def color(colors,text,end=config.resetColor,back=False,mode=8):
  line = getTuple(colors,mode) # mode should be 8 or 16, 16 if a terminal support light colored stuff
  if line == False:
    line = getBestFit(colors,mode)
  # Formatted as \x1b[ (foreground 38, background 48) ; 5 (256 colors) ; line number m
  if back: back = 4
  else: back = 3
  return "{}[{}{}m{}{}".format(config.escapeChr,back,line,text,end)

def getTuple(colorTuple,mode):
  # Obtain the line number of a given color in case our desired one is in stock, otherwise return False
  cfgColors = config.colors[0:mode]
  for i in range(len(cfgColors)):
    if cfgColors[i] == colorTuple:
      return i
  return False

def getBestFit(colorTuple,mode):
  # If our desired color is not in our list, this gets the closest match
  cfgColors = config.colors[0:mode]
  closest, line = 999, 0
  for n,tuple in enumerate(cfgColors):
    diff = getDiff(colorTuple,tuple)
    if diff < closest:
      closest, line = diff, n
  return line

def getDiff(tuple1,tuple2):
  # Get how different the sum of two color tuples are.
  # Used to see how different a given color is from our target color.
  diff = 0
  for i in range(3):
    diff += abs(tuple1[i] - tuple2[i])
  return diff