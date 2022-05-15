# stdlib

# stuff
from tqdm import trange
#import PIL
from PIL import Image, ImageEnhance
# mine
import support, pencil, config, optimize, fileReader

def resizeImg(image,newSize):
  with Image.open(image) as img:
    newImg = img.resize(newSize,5)
  return newImg

def saturateImg(image,newImage,factor=1.5):
  with Image.open(image) as img:
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(factor)
    img.save(newImage)
    return img

def reduce2fit(image,max,pixRatio=(1,1)):
  imgFull = fileReader.handleImage(image)
  w,h = imgFull.size
  factor = 1
  max = (max[0]*pixRatio[0],max[1]*pixRatio[1])
  while w/factor > max[0] or h/factor > max[1]:
    factor += 1
  return imgFull.reduce(factor)

def image_to_ASCII(args):
  ##### Handle args
  functArgs = args
  if functArgs.level == None: functArgs = support.getSupport()
  if functArgs.s: 
    newImage = config.tmp+'saturated.png'
    imageObj = saturateImg(functArgs.infile,newImage)
    functArgs.infile = newImage
  if functArgs.m == False:
    if functArgs.r: imageObj = resizeImg(functArgs.infile,functArgs.coords)
    else: imageObj = reduce2fit(functArgs.infile,functArgs.coords,functArgs.pixelRatio)
  else: imageObj = fileReader.handleImage(functArgs.infile)
  ##### Setup
  pixels = imageObj.load()
  w,h = imageObj.size
  image = ""
  oldColor = ()
  ##### Convert
  if functArgs.silent: iterable = range(h)
  else: iterable = trange(h)
  for y in iterable:
    for x in range(w):
      color = pixels[x,y]
      if functArgs.optimize > 0:
        if optimize.color_isApprox(color,oldColor,functArgs.optimize):
          image += functArgs.pixels
          continue
      oldPix = pencil.color(color,functArgs.pixels,functArgs.level,'',False)
      image += oldPix
      oldColor = color
    image += config.newln
  return image + config.resetColor