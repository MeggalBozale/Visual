# Use 24-bit colors, supported by many terminals by this point.
# Fairly straightforward with RGB!
import config

def color(rgb,text,end=config.resetColor,back=False):
    # Color code is formatted as \x1b[ (foreground 38, background 48) ; 2 (true color) ; red ; green ; blue m
  zlevel = 38
  if back:
    zlevel = 48
  return "{}[38;2;{};{};{}m{}{}".format(config.escapeChr,rgb[0],rgb[1],rgb[2],text,end)