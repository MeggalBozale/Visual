# For trying to determine the colors this terminal uses.
'''
https://unix.stackexchange.com/questions/172548/how-to-determine-the-current-color-of-the-console-output
'''

import sys, config, colorTest

def getSupport(operatingSystem):
    print(f"{operatingSystem}")
    if operatingSystem == 'Linux':
        return getColorLevel(config.colorFile)
    elif operatingSystem == 'Windows':
        return getColorLevel(config.colorFile)
    elif operatingSystem == 'Darwin':
        if config.warnMacOS:
            print("HEY!!!")
            print("I don't currently have the ability to bugtest MacOS.")
            print("The function I use to determine color support is going to return 24bit color (4).")
            print(f"If the program crashes during basic execution, please file an issue on {config.repo}.")
            input("Enter anything to confirm you understand. Disable mac warning in config to supress this output.")
        return 4
    elif operatingSystem == 'Java':
        print("Listen, I don't even know how you have a Java OS. Please tell me on the github repo VISUAL.")
        sys.exit(0)
    else:
        print("OS not recognized. Inserting snarky developer comment and exiting...")
        sys.exit(0)

def compare(level1,level2,colorFile):
    print("Do those color squares look different?")
    print(colorTest.genColors(level1))
    print(colorTest.genColors(level2))
    if input("(Y/N): ").lower() == 'y':
        print(f"Setting color level to {level1}.")
        with open(colorFile,'w') as file:
            file.write(str(level1))
        return

def getColorLevel(colorFile):
    try:
        with open(colorFile,'x') as file:
            pass
    except Exception:
        with open(colorFile,'r') as file:
            contents = file.read()
            if contents != '': return int(contents[0])
    firstTimeSetup(colorFile)

def firstTimeSetup(colorFile):
    print("No color level detected in colorlevel_save.txt!")
    print("It is likely the file was either deleted or made empty.")
    print("Sets of testing colors will be printed out and you will determine if they are colored correctly.")
    comparisons = ((4,3),(3,2),(2,1),(1,0))
    for i in comparisons: compare(i[0],i[1],colorFile)
    print("Setting color level to 0.")
    with open(colorFile,'w') as file:
        file.write('0')
    return
    