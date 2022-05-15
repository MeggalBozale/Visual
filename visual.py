def main():
  # Standard Library
  import os, sys, argparse
  # Project files
  import textification, vid2text, pencil, config, support, readOutFiles, interactions, imageEdit, fileReader, listener

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
  parser.add_argument('--read',action='store_true', help='Read a textified image instead of converting one.')
  parser.add_argument('infile', type=str, help='File to convert and its path, starting from the directory this file is located in.')
  args = parser.parse_args()

  if args.read: 
    pencil.readFromFile(args.infile)
    sys.exit(0)

  if args.fastplay: args.nofpslimit = True
  else: args.nofpslimit = False

  if args.size: print('Size:',fileReader.handleImage(args.infile).size); sys.exit(0)
  if args.data: print('Size:',fileReader.getData(args.infile)); sys.exit(0)

  if args.crop != None: imageEdit.crop(args)

  if args.outfile == None: args.outfile = args.infile[:args.infile.rfind('.')] + '.txt'
  if args.coords  == None: args.coords  = pencil.getBounds()
  if args.pixels  == None: args.pixels  = config.pixels
  if args.level   == None: args.level   = support.getSupport()
  if args.type    == None: args.type    = 'image'
  if args.start   == None: args.start   = 0
  if args.optimize == None: args.optimize = 4

  args.pixelRatio = (config.pixelRatio[0]/len(args.pixels),config.pixelRatio[1])

  if args.m: args.coords = fileReader.handleImage(args.infile).size
  print(args.coords)


  format = (args.infile.split('.'))
  format = format[len(format)-1]
  if format == 'gif': args.type = 'video'

  if args.type == 'image':

      if args.i:
        if args.noinput != True: listener.thread.start()
        interactions.imageSession(args)
        sys.exit(0)

      image = textification.image_to_ASCII(args)
      pencil.writeToFile(image,args.outfile)
      if args.noimg == False:
        pencil.write(image,'')

  elif args.type == 'video':
    if args.noinput != True: listener.thread.start()
    if args.loop:
      while True:
        vid2text.playVideo(args)
    vid2text.playVideo(args)

if __name__ == '__main__':
  main()