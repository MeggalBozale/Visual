def color(color,text):
    # Take a color and decide if it will be black or white (pixel or space)
    brightness = color[0]+color[1]+color[2]
    if brightness > (255*3)/4:
        return text
    else:
        return ' '*len(text)