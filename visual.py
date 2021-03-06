def main():
  # Standard Library
  import os, sys, argparse, platform
  # Project files
  import textification, vid2text, pencil, config, support, readOutFiles, interactions, imageEdit, fileReader, listener
  '''
  File that takes in user input + applies defaults when needed from config. Read README.md
  '''
  parser = argparse.ArgumentParser(description='Convert applicable file formats into color text.')
  parser.add_argument('-o', metavar='outfile', type=str, dest='outfile', help='Specify where the output will go. By default, this is the infile with the extention renamed to \'.txt\'')
  parser.add_argument('-c', metavar='bounds', type=int, dest='coords', nargs=2, help='Manually define the image bounds for x and y.\nBy default, this is your window size.')
  parser.add_argument('-p', metavar='pixel chars', type=str, dest='pixels',help='Specify what character(s) pixels are from. default is '+config.pixels)
  parser.add_argument('-l', metavar='color level', type=int, dest='level', help='Specify the level of color to use. [NOTE: Some terminals do not support higher values.] | 0: No color | 1: 8 colors | 2:256 colors | 3: 8^3 colors/truecolor')
  parser.add_argument('-b', metavar='background color', type=tuple, dest='back', help='Change the background color of the image. Default is white.')
  parser.add_argument('-t', metavar='type', type=str, dest='type', help='Specify file type manually, in case the program cannot.')
  parser.add_argument('--start', metavar='start frame', type=int, dest='start', help='Specify the frame to start in with a video.')
  parser.add_argument('--crop',type=int,nargs=4,help="Crop the image before processing. Eg. --crop x1 y1 x2 y2")
  parser.add_argument('-m', action='store_true', help='When enabled, converts the image at its original resolution. This will not fit in a terminal!')
  parser.add_argument('-r', action='store_true', help='When enabled, resizes the image to the specified bounds instead of scaling it down to them.')
  parser.add_argument('-s', action='store_true', help='When enabled, saturates the image. This may fix resultant images being desaturated from a terminal background.')
  parser.add_argument('--loop', action='store_true', help='When enabled, loops a video.')
  parser.add_argument('--optimize', type=int, help='A value of 0 = no optimization. Otherwise, values 0-256 group colors as similar or less similar than the value used.')
  parser.add_argument('--silent', action='store_true', help='Disable the progress bar.')
  parser.add_argument('--noimg', action='store_true', help='Disable writing to stdout.')
  parser.add_argument('--data', action='store_true', help='Print out image metadata..')
  parser.add_argument('--fastplay', action='store_true', help='Ignore the framerate read in the metadata, instead opting to play the video as fast as possible.')
  parser.add_argument('--noinput', action='store_true', help='Disable user input. Helpful when you don\'t want the listener thread active.')
  parser.add_argument('--size', action='store_true', help='Utility option to print the image size and exit.')
  parser.add_argument('-i',action='store_true', help='Interact with an image besides just printing it.')
  parser.add_argument('--read',action='store_true', help='Read a textified image instead of converting one. You may need to specify the pixels used.')
  parser.add_argument('infile', type=str, help='File to convert and its path, starting from the directory this file is located in.')
  parser.add_argument('--noheightlimit',action='store_true',help='Remove restrictions on the Y-Value for an image.')
  args = parser.parse_args()

  # Get the os
  args.os = platform.system() # "Linux", "Darwin" (Mac/Apple), "Windows"

  # Read textified image, exit
  if args.read: readOutFiles.readFile(args.infile,args.pixels); sys.exit(0)

  # Remove FPS cap read from videos
  if args.fastplay: args.nofpslimit = True
  else: args.nofpslimit = False

  # Provide information to the user on request
  if args.size: print('Size:',fileReader.handleImage(args.infile).size); sys.exit(0)
  if args.data: print('Size:',fileReader.getData(args.infile)); sys.exit(0)

  # Choose a cropped region of user specification
  if args.crop != None: imageEdit.crop(args)

  # Images can be uncapped on a y-level usually on user request and still be readable with scrolling
  # For best results, zoom terminal out fully before executing for high res image in terminal.
  if args.coords  == None: args.coords  = pencil.getBounds()
  if args.noheightlimit:   args.coords  = (args.coords[0],99999)

  removeWhenDone = False
  if args.outfile == None: 
    args.outfile = args.infile[:args.infile.rfind('.')] + '.txt'
    removeWhenDone = True
  
  if args.pixels  == None: args.pixels  = config.pixels
  if args.level   == None: args.level   = support.getSupport(args.os); print(f"{args.level}")
  if args.start   == None: args.start   = 0
  if args.optimize == None: args.optimize = 0

  # Adjust the pixel ratio based on how many pixels are in args.pixels
  args.pixelRatio = (config.pixelRatio[0]/len(args.pixels),config.pixelRatio[1])

  # Textify the image at a size of the original resolution, not the terminal
  if args.m: args.coords = fileReader.handleImage(args.infile).size
  print(args.coords)

  # Get image format
  format = (args.infile.split('.'))
  format = format[len(format)-1]
  if args.type == None:
    if format == 'gif': args.type = 'video'
    else: args.type = 'image'

  # Using image type and other args, do the stuff (finally, sheesh)
  if args.type == 'image':
      if args.i: # Interactive image viewing mode
        if args.noinput != True: listener.thread.start()
        interactions.imageSession(args)
        sys.exit(0)

      # Classic image printing mode
      image = textification.image_to_ASCII(args)
      pencil.writeToFile(image,args.outfile)
      if args.noimg == True: sys.exit(0)
      readOutFiles.readFile(args.outfile,args.pixels)
      if removeWhenDone: os.remove(args.outfile)

  # Video player
  elif args.type == 'video':
    if args.noinput != True: listener.thread.start()
    if args.loop:
      while True:
        vid2text.playVideo(args)
    vid2text.playVideo(args)

if __name__ == '__main__':
  main()