# Generate a lot of colors.
import config, pick256, pickLow, pickMono, pencil

def genColors(level):
    colorSquare = ''
    rgb = [0,0,0]
    bounds = pencil.getBounds()
    rgbadd = [1,1,1]
    blocks = '[]'#config.pixels
    colorPotential = bounds[0]*bounds[1] # how many colors we can show
    print(f"Color level: {level}")
    for y in range(bounds[1]):
        for x in range(int(bounds[0]/len(blocks))):
            if level == 4: colorSquare += f"{config.escapeChr}[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m{blocks}"
            elif level == 3: colorSquare += pick256.color  ((*rgb,),blocks,end='')
            elif level == 2: colorSquare += pickLow.color16((*rgb,),blocks,end='')
            elif level == 1: colorSquare += pickLow.color8 ((*rgb,),blocks,end='')
            elif level == 0: colorSquare += pickMono.color ((*rgb,),blocks)
            
            rgb[0] += 8
            if rgb[0] >= 255: rgb[0] = 0; rgb[1] += 8
            if rgb[1] >= 255: rgb[1] = 0; rgb[2] += 8
        colorSquare += config.newln
    return colorSquare + config.resetColor
        #colors,text,end=config.resetColor,back=False,mode=8

# For users to see their first 16 colors, and adjust accordingly
#def gen16():
#    for i in range(8):


def main():
    print(genColors(4))
    #for i in range(5):
    #    print(genColors(4-i))

if __name__ == '__main__':
  main()