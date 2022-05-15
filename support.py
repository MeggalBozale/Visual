# For trying to determine the colors this terminal uses.
'''
https://unix.stackexchange.com/questions/172548/how-to-determine-the-current-color-of-the-console-output
'''

import sys, config, colorTest

def getSupport(operatingSystem):
    if operatingSystem == 'Linux':
        firstTimeSetup()
    elif operatingSystem == 'Windows':
        firstTimeSetup()
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
    return 4 # this is a fallback in case something goes absolutely, horribly wrong (not uncommon)

def firstTimeSetup():
    colorFile = 'colorlevel_save.txt'
    try:
        with open(colorFile,'x') as file:
            pass
    except:
        with open(colorFile,'r') as file:
            contents = file.read()
            print(contents)
            return
    print("No color level detected in colorlevel_save.txt!")
    print("It is likely the file was either deleted or made empty.")
    print("Sets of testing colors will be printed out and you will determine if they are colored correctly.")
    print(colorTest.genColors(4))
    print("Do those colors look to change on a smooth gradient?")
    if input("(Y/N): ").lower() == 'y':
        print("Setting color level to 4.")
        with open(colorFile,'w') as file:
            file.write('4')
        return
    print("Ok. How about these?")
    