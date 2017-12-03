from PIL import Image

## HugeBMP manages an uncompressed BMP file with 24 bits per pixel.
#  Management of image data is handled diretly in the file.
#    
class HugeBMP:

    ## Creates byte data to write them in the file.
    #
    def __getBytes( self, value, size ):
        res = ""
        for i in range(0,size):
            res = res+chr((value>>i*8)&255)
        return res
    
    ## Returnes the size of the file header.
    #
    def __getHeaderSize( self ):
        return 14
    
    ## Returns the size of the Bitmap information header
    #
    def __getInfoSize( self ):
        return 40
    
    ## Returns the size of the pixel data block.
    #
    def __getPixelDataSize( self ):
        w = self.__bitmapHeader["width"]
        h = self.__bitmapHeader["height"]
        f = self.__getRowFiller()
        return f+w*h*3
    
    ## Recalculates headerinformation that could change
    #  while working with the class.
    #
    def __recalculateMetaData(self):
        self.__fileHeader["size"]   = self.__getHeaderSize() + self.__getInfoSize() + self.__getPixelDataSize()
        self.__fileHeader["offset"] = self.__getHeaderSize() + self.__getInfoSize()
        self.__bitmapHeader["size"] = self.__getInfoSize()
    
    ## Calculates the number of bytes to fill each row in the Pixeldata block.
    #
    def __getRowFiller(self):
        w = self.__bitmapHeader["width"]
        tmp0 = 4
        tmp = (w*3)%tmp0
        if tmp > 0:
            tmp = tmp0-tmp    
        return tmp
    
    ##
    #
    def __init__( self, fileName, width = 100, height = 100 ):
        
        # fileheader
        fh = {}
        # 2 - signature
        fh["signature"] = "BM"
        # 4 - filesize in bytes
        fh["size"] = 0
        # 2 - reserved
        fh["res0"] = 0
        # 2 - reserved
        fh["res1"] = 0
        # 4 - offset of pixeldata
        fh["offset"] = 0

        self.__fileHeader = fh
        
        # bitmapheader
        bh = {}
        # 4 - headersize
        bh["size"] = 0
        # 4 - image width
        bh["width"] = width
        # 4 - image height 
        bh["height"] = height
        # 2 - number of color planes
        bh["numColPlanes"] = 1
        # 2 - depths bpp
        bh["bpp"] = 24
        # 4 - compression
        bh["compression"] = 0
        # 4 - size of comp data
        bh["dataSize"] = 0
        # 4 - horicontal resolution
        bh["hRes"] = 0
        # 4 - vertical resolution
        bh["vRes"] = 0
        # 4 - palette size
        bh["palSize"] = 0
        # 4 - important colors
        bh["impColors"] = 0
        
        self.__bitmapHeader = bh
        
        self.__workingPos = [0,0]
        self.__recalculateMetaData()
        self.__file = open( fileName, "w+" )
        self.__writeFileHeader()
        self.__writeInfoBlock()
        self.__createDataBlock(255,0,255)
        self.setPos(0,0)
    
    ## Writes the file header.
    #
    def __writeFileHeader(self):
        f = self.__file
        h = self.__fileHeader
        
        f.seek(0)
        f.write( h["signature"] )
        f.write( self.__getBytes( h["size"], 4)  )
        f.write( self.__getBytes( h["res0"], 2)  )
        f.write( self.__getBytes( h["res1"], 2)  )
        f.write( self.__getBytes( h["offset"], 4)  )
    
    ## Writes the Bitmap information block.
    #
    def __writeInfoBlock(self):
        
        f = self.__file
        h = self.__bitmapHeader
        
        f.seek( self.__getHeaderSize() )
        f.write( self.__getBytes( h["size"], 4)  )
        f.write( self.__getBytes( h["width"], 4)  )
        f.write( self.__getBytes( -h["height"], 4)  )
        f.write( self.__getBytes( h["numColPlanes"], 2)  )
        f.write( self.__getBytes( h["bpp"], 2)  )
        f.write( self.__getBytes( h["compression"], 4)  )
        f.write( self.__getBytes( h["dataSize"], 4)  )
        f.write( self.__getBytes( h["hRes"], 4)  )
        f.write( self.__getBytes( h["vRes"], 4)  )
        f.write( self.__getBytes( h["palSize"], 4)  )
        f.write( self.__getBytes( h["impColors"], 4)  )
    
    ## Writes the pixel data block to create the file.
    #
    def __createDataBlock(self, red = 255, green = 0, blue = 255):
        f = self.__file
        w = self.__bitmapHeader["width"]
        h = self.__bitmapHeader["height"]
        filler = self.__getRowFiller()
        f.seek( self.__fileHeader["offset"] )
        for i in range(0, h):
            for j in range(0, w):
                f.write( chr(blue) )
                f.write( chr(green) )
                f.write( chr(red) )
            for j in range(0, filler):
                f.write( chr(0) )
    
    ## Sets the file pointer to the position
    #  of the given coordinates.
    #
    def setPos(self,x,y):
        f = self.__file
        w = self.__bitmapHeader["width"]
        h = self.__bitmapHeader["height"]
        filler = self.__getRowFiller()

        if x > w or y > h:
            return False
        
        self.__workingPos = [x,y]
        f.seek( self.__fileHeader["offset"] + (w*3+filler)*y + x*3 )
        return True
    
    ## Writes a pixel value to the current position and moves the
    #  pointer to the next pixel. If the end of a row is reached.
    #  the pointer is moved to the first pixel in the next row.
    def writeColor( self, red, green, blue ):
        wp = self.__workingPos
        w = self.__bitmapHeader["width"]
        
        f = self.__file
        f.write( chr(blue) )
        f.write( chr(green) )
        f.write( chr(red) )
        
        wp[0] = wp[0]+1
        if wp[0] > w:
            self.setPos( 0, wp[1]+1 )

    ## Sets the color value of the given pixel.
    #
    def setPixel(self,x,y,red,green,blue):
        if not self.setPos(x,y):
            return False
            
        self.writeColor(red,green,blue)
        return True
    
    ## Pastes an Image at the defined area.
    #
    def paste( self, img, box):
    
        w = self.__bitmapHeader["width"]
        h = self.__bitmapHeader["height"]
        
        if len(box) == 2:
            box = box+(box[0]+img.size[0], box[1]+img.size[1])
        
        mb = ( 
            # left border - must be >= 0 and <= bmp.width
            max( 0, min(box[0],w) ),
            # upper border - must be >= 0 and <= bmp.height
            max( 0, min(box[1],h) ),
            # right border - must be <= img.width and must respect right border of bmp
            min( w, box[2] ),
            # right border - must be <= img.height and must respect down border of bmp
            min( h, box[3] )
        )
        
        for y in range( mb[1], mb[3] ):
            self.setPos( mb[0],y )
            for x in range(mb[0], mb[2]):
                # This line shouldn't be necassary
                # but the seems to be a bug.
                self.setPos( x,y )
                
                c = img.getpixel( (x-mb[0], y-mb[1]) )
                self.writeColor(c[0],c[1],c[2])

    ## Closes the image file.
    #                
    def close(self):
        self.__file.close()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        