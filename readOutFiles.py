# made for reading ASCII images
import os, config

def readFile(inFile):
    file = open(inFile)
    for line in file:
        os.system(f"printf \"%s{line}\r\"")
    file.close()