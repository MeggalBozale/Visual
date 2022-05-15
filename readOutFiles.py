# made for reading ASCII images
import os

def readFile(inFile,pixel):
    with open(inFile) as file:
        for line in file:
            if (pixel in line) == False:
                line = '' # some lines are basically empty but dont give a heck about size
            os.system(f"printf '{line}'")