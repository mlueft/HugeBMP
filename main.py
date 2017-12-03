from PIL import Image
import HugeBMP

# Create a new BMP file
bmp = HugeBMP.HugeBMP( "d:\\temp\\out1.bmp", 2000, 2000)

# Load a test image to paste it into the bmp
img = Image.open( "d:\\temp\\test.png" )

# paste the test image into the bmp
bmp.paste( img, (0,0) )

# paste the test image into the bmp
bmp.paste( img, (50,30) )

# paste the test image into the bmp
bmp.paste( img, (100,300) )

# paste the test image into the bmp
bmp.paste( img, (1900,0) )

# draw a white pixel
bmp.setPos(100,100)
bmp.setColor(255,255,255)

# Those two lines are equivalent to
# Internally setPixel calls setPos and setColor
bmp.setPixel(100,100,255,255,255)

# to write more pixel horizontally
# just call setPos at the beginning
bmp.setPos(100,102)
bmp.setColor(255,255,255)
bmp.setColor(255,255,255)
bmp.setColor(255,255,255)
bmp.setColor(255,255,255)

# if setColor reaches the end of a row
# it automatically jumps to the next line.
bmp.setPos(1998,2)
bmp.setColor(255,255,255)
bmp.setColor(255,255,255)
bmp.setColor(255,255,255)
bmp.setColor(255,255,255)

bmp.close()
