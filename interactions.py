import textification, sys, os, pencil, imageEdit, listener, config, fileReader

def p(t,e=config.newln):
    pencil.write(t,e)

def writeImage(image,args,coords):
    newImg = fileReader.handleImage(image)
    newImg = newImg.crop(coords)
    args.infile = newImg
    newImg = textification.image_to_ASCII(args)
    pencil.write(newImg)
    pencil.write(f"Quit: {config.quit.upper()} | Shift view: {config.move} | Zoom: {config.zoom} |")
    pencil.write(f"Coords: {coords} | Save: {config.save} |")

def saveImage(image,args,coords):
    newImg = fileReader.handleImage(image)
    newImg = imageEdit.zoom(newImg,coords)
    args.infile = newImg
    fileNum = 0
    while True:
        padding = "0"*(5-len(str(fileNum)))
        outFile = f"{config.saved}{padding}{fileNum}"
        try:
            with open(outFile+'.png','x'):
                break
        except Exception:
            fileNum += 1
            continue
    txtImg = textification.image_to_ASCII(args)
    newImg.save(outFile+'.png')
    pencil.writeToFile(txtImg,outFile+'.txt',False)
    pencil.write(f"Wrote to {outFile}.png and {outFile}.txt!")

def isUsable(userInput):
    # Don't redraw or anything if it's not a character that does stuff
    usable = (*config.move,*config.zoom,config.quit,config.save)
    for i in usable:
        if i == userInput:
            return True
    if userInput != '': p("Invalid Input.")
    return False

def zoomImg(c,z,change,mC):
    mW = mC[2] - mC[0]
    mH = mC[3] - mC[1]
    sX = (mW * z) // 2
    sY = (mH * z) // 2
    print(sX,sY)
    nC = (c[0]+sX,c[1]+sY,c[2]-sX,c[3]-sY)
    return nC

    #
    #width  = maxCoords[2] - maxCoords[0]
    #height = maxCoords[3] - maxCoords[1]
    #p(f"{width},{height}")
    #shiftX, shiftY = (width*zoom)/2, (height*zoom)/2
    #newCoords =  (coords[0]+shiftX,coords[1]+shiftY,coords[2]-shiftX,coords[3]-shiftY)
    ## Sanity check
    #if change > 0: # zooming in
    #    if (coords[2] - coords[0] <= 5) or (coords[3] - coords[1] <= 5): return coords
    #if change < 0: # zooming out
    #    if (newCoords[0] < maxCoords[0]) or (newCoords[1] < maxCoords[1]): return coords
    #    if (newCoords[2] > maxCoords[2]) or (newCoords[3] > maxCoords[3]): return coords
    #return newCoords

def translate(coords,x,y):
    return (coords[0]+x,coords[1]+y,coords[2]+x,coords[3]+y)

def doShift(coords,shiftX,shiftY):
    # take coordinates and the direction to shift
    # return new coordinates shifted by a fractional amount of the width or height
    # (x1,y1,x2,y2)
    # for diagonals add two directions to string dir
    width  = coords[2] - coords[0]
    height = coords[3] - coords[1]
    #x,y = 0,0
    #if 'up'    in dir: y *= height * config.moveScale * -1
    #if 'down'  in dir: y *= height * config.moveScale
    #if 'left'  in dir: x *= width  * config.moveScale * -1
    #if 'right' in dir: x *= width  * config.moveScale
    x = shiftX * width  * config.moveScale
    y = shiftY * height * config.moveScale
    p(f"Before: {coords} | After: {translate(coords,x,y)}")
    return translate(coords,x,y)


def updateShift(x,y,userInput):
    if 'up'    in userInput: y -= 1
    if 'down'  in userInput: y += 1
    if 'left'  in userInput: x -= 1
    if 'right' in userInput: x += 1
    return x, y

def handleInput(userInput):
    direction, zoom, save = False, 0, False
    # Check for save
    if userInput == config.save:
        save = True
    # Check for move
    for i in range(len(config.move)):
        if userInput == config.move[i]:
            direction = config.moveDirs[i]
            break
    # Check for zoom
    for i,_ in enumerate(config.zoom):
        if userInput == config.zoom[i]:
            if   config.zoomDirs[i] == '+': zoom = config.zoomScale
            elif config.zoomDirs[i] == '-': zoom = config.zoomScale * -1
            break
    return direction, zoom, save

def clamp(n,minn,maxn):
    return max(min(maxn,n),minn)

def mixCoords(coords1,coords2):
    mixed = []
    mixed.append([coords1[i]+coords2[i] for i in range(len(coords1))])
    return mixed

def imageSession(args):
    w,h = fileReader.getImageSize(args.infile)
    zoom = 0
    coords = (0,0,w,h)
    shiftX, shiftY = 0,0
    ##### Write once, run (melos)
    writeImage(args.infile,args,coords)
    customArgs = args
    originalFile = args.infile
    while True:
        userInput = listener.getInput()
        # Ignore bad inputs, break when input thread dies
        if userInput is None: continue
        if isUsable(userInput) == False: continue
        if listener.thread.is_alive() == False or userInput == 'q': break
        ### Setup #
        newCoords = coords
        direction, zoomAdd, save = handleInput(userInput)
        ### Manip #
        zoom += zoomAdd
        zoom = clamp(zoom,0,1)
        if direction != False: shiftX, shiftY = updateShift(shiftX,shiftY,direction)
        newCoords = doShift(newCoords,shiftX,shiftY)
        newCoords = zoomImg(newCoords,zoom,zoomAdd,coords)
        if save: saveImage(originalFile,customArgs,newCoords)
        ### Write #
        writeImage(originalFile,customArgs,newCoords)

