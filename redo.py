from PIL import Image

def format(file): # redo format
  file = color(file)
  return file

def color(file):  # redo color
  #with Image.open(file) as img:
  return file.convert('RGB')