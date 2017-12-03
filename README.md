# HugeBMP
A Python class to create (huge) BMPs files without using the computers memory to keep image data. All operations are handled directly in the BMP file without having the bitmap data in memory.

This example shows how to set single pixels.
```
import HugeBMP
# Create a new BMP file
bmp = HugeBMP.HugeBMP( "d:\\temp\\out1.bmp", 2000, 2000)

# draw a white pixel
bmp.setPos(100,100)
bmp.setColor(255,255,255)

# Those two lines are equivalent to
# Internally setPixel calls setPos and setColor
bmp.setPixel(100,100,255,255,255)

bmp.close()
```

This exampel shows how to copy am Image to the bmp file.
```
from PIL import Image
import HugeBMP

# Create a new BMP file
bmp = HugeBMP.HugeBMP( "d:\\temp\\out1.bmp", 2000, 2000)

# Load a test image to paste it into the bmp
img = Image.open( "d:\\temp\\test.png" )

# paste the test image into the bmp
bmp.paste( img, (0,0) )
bmp.paste( img, (500,500) )

bmp.close()
```
