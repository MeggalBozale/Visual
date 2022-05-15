def color_isApprox(color1,color2,maxDiff):
  # If 2 colors are similar enough, return true
  # Helps pair up colors that otherwise would be separate
  # When our eyes can't tell
  diff = 0
  if len(color1) != len(color2): return False
  for i in range(3): diff += color1[i] - color2[i]
  if abs(diff) < maxDiff: return True
  return False