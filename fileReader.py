import PIL
from PIL import Image
from PIL.ExifTags import TAGS

def handleImage(image):
    # If an image/imageobj passed in isn't an image obj, make it one
    if isinstance(image,str):
        return Image.open(image)
    else:
        return image

def getImageSize(image):
    # For main.py user input validation / addition option
    imageObj = handleImage(image)
    return imageObj.size

def getData(image):
    imageObj = handleImage(image)
    print(vars(imageObj))

def getFPS(image):
    """ Returns the average framerate of a PIL Image object """
    imageObj = handleImage(image)
    imageObj.seek(0)
    frames = duration = 0
    while True:
        try:
            frames += 1
            duration += imageObj.info['duration']
            imageObj.seek(imageObj.tell() + 1)
        except EOFError:
            return frames / duration * 1000

def getMetadata(image):
    imageObj = handleImage(image)
    exifData = imageObj.getexif()
    for tagID in exifData:
        tag = TAGS.get(tagID, tagID)
        data = exifData.get(tagID)
        if isinstance(data,bytes):
            data = data.decode()
        print(f"{tag:25}: {data}")
    return exifData
