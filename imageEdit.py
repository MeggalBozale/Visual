from logging import raiseExceptions
import textification, os, pencil, fileReader

def crop(args):
  newfile = fileReader.handleImage(args.infile)
  newfile = newfile.crop(tuple(args.crop))
  if (args.infile).rfind('/') != -1: args.infile = args.infile[:args.infile.rfind('/')+1:]+'cropped_' + args.infile[args.infile.rfind('/')+1::]
  else: args.infile = 'cropped_'+args.infile
  if os.path.exists(args.infile): 
    if pencil.getBool("Cropped file exists. Overwrite?"):
      newfile.save(args.infile)
    else: return
  newfile.save(args.infile)

def zoom(image,coords):
    imageObj = fileReader.handleImage(image)
    #maxSize = imageObj.size
    #if coords[2] > maxSize[0] or coords[3] > maxSize[1]: pencil.write("Zoom out of bounds."); a=0/0
    imageObj = imageObj.crop(coords)
    return imageObj