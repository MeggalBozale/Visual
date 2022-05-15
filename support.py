# For determining the colors this terminal uses.
import platform, os

system = platform.system()

def getSupport():
  return 4 # i literally can't do this right now so when in doubt, maximum quality
  '''
    if system == "Linux":
        support = os.popen("echo $COLORTERM").read().strip()
        if support == "truecolor" or support == "24bit": return 3
        elif support == "256": return 2
        else: return 1
    elif system == "Windows":
        # it really really should just be 16 colors
        return 1
    elif system == "Darwin": # MacOS
        print("No mac support yet sorry maybe 'later'")
    else:
        print("Either something went wrong, or you're using an unsupported operating system.")
  '''