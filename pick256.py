'''
The 256 color palette sucks to comb through, so this file does it for you!
'''
import config

def color(colors,text,lazy=True,end=config.resetColor,back=False):
  ourLine = getTuple(colors)
  if ourLine == False:
    ourLine = getBestFit(colors,lazy)
  # Formatted as \x1b[ (foreground 38, background 48) ; 5 (256 colors) ; line number m
  zlvl = 38
  if back: zlvl = 48
  return "{}[{};5;{}m{}{}".format(config.escapeChr,zlvl,ourLine,text,end)

def getColorTuple(color):
  # Get decimal rgb values from a hex string (eg. #AAE0FF)
  if color[0] == '#': color = color[1::]
  return (int(color[0:2],16),int(color[2:4],16),int(color[4:6],16))

def getTuple(colorTuple):
  # Obtain the line number of a given color in case our desired one is in stock, otherwise return False
  file = open(config.file256)
  for r,line in enumerate(file):
    lineColor = getColorTuple(line)
    if lineColor == colorTuple:
      return r
  return False

def getBestFit(colorTuple,lazy=True,margin=30):
  # If our desired color is not in our list, this gets the closest match
  file = open(config.file256)
  closest,line = 999,0
  for i,list in enumerate(file):
    lineTuple = getColorTuple(list)
    diff = getDiff(colorTuple,lineTuple)
    if diff < closest:
      closest, line = diff, i
      if lazy: # Saves processing time
        if diff <= margin:
          return line
  return line

def getDiff(tuple1,tuple2):
  # Get how different the sum of two color tuples are.
  # Used to see how different a given color is from our target color.
  diff = 0
  for i in range(3):
    diff += abs(tuple1[i] - tuple2[i])
  return diff

def matches(list1,list2):
  # Check if two lists match
  for i in range(len(list1)):
    if list1[i] != list2[i]:
      return False
  return True