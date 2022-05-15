# Generate a lot of colors.
import config, pick256, pickLow, pickMono


def genColors(level):
    colorSquare = ''
    rgb = [0,85,170]
    size = 20
    rgbadd = [1,1,1]
    print(f"Color level: {level}")
    for i in range(size):
        for j in range(size):
            if level == 4: colorSquare += f"{config.escapeChr}[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m[]"
            elif level == 3: colorSquare += pick256.color((*rgb,),'[]',False,'')
            elif level == 2: colorSquare += pickLow.color16((*rgb,),'[]',end='')
            elif level == 1: colorSquare += pickLow.color8((*rgb,),'[]',end='')
            elif level == 0: colorSquare += pickMono.color((*rgb,),'[]')
            for i in range(3):
                if rgb[i] >= 255: rgbadd[i] = -1
                if rgb[i] <=   0: rgbadd[i] =  1
                rgb[i] += rgbadd[i]
        colorSquare += config.newln
    return colorSquare + config.resetColor
        #colors,text,end=config.resetColor,back=False,mode=8

def main():
    for i in range(5):
        print(genColors(5-i))

if __name__ == '__main__':
  main()