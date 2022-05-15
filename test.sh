for i in 1 2 4 8 16 32 64 128 256 512 1024
do
  python3.8 printASCII.py --silent --optimize=$i -o "optimized.txt" ./images/pixelMountains.png
  stat "optimized.txt" | grep -i 'size' >> test.txt
  rm "optimized.txt"
done