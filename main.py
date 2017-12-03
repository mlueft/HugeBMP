from PIL import Image
import HugeBMP

bmp = HugeBMP.fileBMP( "d:\\programming\\python\\fileBMP\\out1.bmp", 2000, 2000)

img = Image.open( "d:\\programming\\python\\fileBMP\\test.png" )

pos = (0,0)
#bmp.paste( img,( pos[0], pos[1], pos[0]+img.size[0], pos[1]+img.size[1] ) )
bmp.paste( img, (0,0) )
bmp.paste( img, (50,30) )
bmp.paste( img, (100,300) )
bmp.paste( img, (1900,0) )
bmp.close()
