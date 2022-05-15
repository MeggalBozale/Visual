# stdlib
import os, time
from time import sleep
# stuff
from PIL import ImageSequence
# mine
import support, pencil, config, textification, redo, listener, fileReader

def getFPS(curTime,oldTime,curFrame,oldFrame,oldFPS,interval=0):
    # Return the old values when we ran this function just recently
    if curTime < oldTime + interval: return oldFPS, oldTime, oldFrame
    curFPS = (curFrame-oldFrame) / (curTime-oldTime) # (Frames since last calc) / (Time since last calc)
    return curFPS, curTime, curFrame

def playVideo(args,constrainFPS=True,cls=False):
    if cls: os.system('clear')
    ##### Setup
    functArgs = args
    video = fileReader.handleImage(functArgs.infile)
    if args.nofpslimit == False: 
        print("Getting FPS. This may take a while for longer videos!",end=config.returnLeft)
        constrainFPS = fileReader.getFPS(video)
    else: constrainFPS = False
    ##### Main Loop
    frameNum, ourTime, ourFrame, ourFPS, extraLines = 0, 0, 0, constrainFPS, 0
    # add 1 to extraLines for every new newline you add after video rendering
    for frame in ImageSequence.Iterator(video):
        if listener.thread.is_alive() == False: break
        if (frameNum < functArgs.start): continue
        ourFPS, ourTime, ourFrame = getFPS(time.time(),ourTime,frameNum,ourFrame,ourFPS,0)
        #if ourFPS < constrainFPS: frameNum += 1; continue # TODO
        if constrainFPS:
            if ourFPS > constrainFPS: time.sleep((1/(constrainFPS-(time.time()-ourTime))))
        frame = redo.format(frame)
        functArgs.infile = frame; functArgs.silent = True
        renderFrame(functArgs,frameNum,ourFPS,constrainFPS)
        frameNum += 1
    listener.endListen()
    pencil.clear(extraLines)
    print("Press any key to exit...",end=config.returnLeft)

def renderFrame(args,frameNum,ourFPS,maxFPS):
    ASCIIvideo = textification.image_to_ASCII(args)
    pencil.write(ASCIIvideo,'')
    pencil.writeColor((0,128,255),(f"Frame: {frameNum} | FPS: {int(ourFPS)} | QUIT: {config.quit.upper()} | Max FPS: {maxFPS}") ,4,config.lnup)
    pencil.write(config.lnup*(ASCIIvideo.count(config.newln)+10),config.lnup)
    