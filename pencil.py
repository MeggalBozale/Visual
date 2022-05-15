# stdlib
#import getch
import os, pickMono, pickLow, pick256, pick24bit, config

def color(rgb,text,support,end=config.resetColor,background = False):
  if   support == 4: return pick24bit.color(rgb,text,      end,background)
  elif support == 3: return   pick256.color(rgb,text,False,end,background)
  elif support == 2: return   pickLow.color(rgb,text,      end,background,16)
  elif support == 1: return   pickLow.color(rgb,text,      end,background, 8)
  else:              return  pickMono.print(rgb,text)

def write(input,end=config.newln):
  os.system("printf \'" + input + end + "\'")

def writeColor(rgb,text,support,end=config.newln,background=False):
  text = color(rgb,text,support,end,background)
  os.system("printf \'"+text+end+"\'")

def getInt(query,min,max,complain="Out of bounds."):
  while True:
    get = int(input(query))
    if get > max or get < min:
      write(complain)
      write("Clamp is ({}-{}). Try again...".format(min,max))
      continue
    return get

def getBool(query,yes='Y',no='N',complain="Invalid option."):
  while True:
    write(f"{query}\n({yes}/{no})")
    get = input('').lower()
    if get == yes.lower():
      return True
    elif get == no.lower():
      return False
    else:
      write(complain)
      write("Valid options are {} and {}.".format(yes,no))
      continue


def clear(extraLines):
    size = getBounds()
    write(config.lnup*extraLines,end=config.returnLeft)
    for y in range(size[1]+4):
        write(' '*size[0],config.newln)
    write(config.lnup*size[1],end=config.returnLeft)

def getBounds():
  # Get the bounds of the terminal at any given moment
  y, x = os.popen('stty size', 'r').read().split()
  return int(x),int(y)

def writeToFile(text,file,safety=True):
  try: 
    f = open(file,'x')
    f.write(text)
    f.close()
  except: 
    if safety: confirm = getBool("Output file for %s exists. Overwrite?" % file)
    else: confirm = True # Outside of videos safety should really be on. I mean it!
    write(config.lnup*2,'')
    if confirm:
      f = open(file,'w')
      f.write(text)
      f.close()
    else:
      confirm = getBool("Cancelling overwrite. Would you like to specify a new path for this file?")
      if confirm:
        writeToFile(text,input("New file path: "))

def readFromFile(file):
  f = open(file)
  contents = f.read()
  os.system('echo -em \''+contents+'\'')
  #write(contents,'')
  f.close()