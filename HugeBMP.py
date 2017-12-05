from PIL import Image

## HugeBMP manages an uncompressed BMP file with 24 bits per pixel.
#  Management of image data is handled diretly in the file.
#    
class HugeBMP:

    class __BMP:
        
        def __init__(self, fileName, width = 100, height = 100 ):
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

            self.fileHeader = fh        
            self.bitmapInfoBlock = bh
            self.file = open( fileName, "w+" )
            self.workingPos = [0,0]
        
            self.recalculateMetaData()
            self.writeFileHeader()
            self.writeInfoBlock()
            self.createDataBlock(255, 0, 255 )
            self.setPos(0,0)
            
        ## Creates byte data to write them in the file.
        #
        def getBytes( self, value, size ):
            res = ""
            for i in range(0,size):
                res = res+chr((value>>i*8)&255)
            return res

        ## Returns the size of the file header.
        #
        def getHeaderSize( self ):
            return 14
        
        ## Returns the size of the Bitmap information header
        #
        def getInfoSize( self ):
            return 40
        
        ## Returns the size of the pixel data block.
        #
        def getPixelDataSize( self ):
            bib = self.bitmapInfoBlock
            
            w = bib["width"]
            h = bib["height"]
            f = self.getRowFiller( )
            return f+w*h*3
        
        ## Recalculates headerinformation that could change
        #  while working with the class.
        #
        def recalculateMetaData(self):
            
            bib = self.bitmapInfoBlock
            fh = self.fileHeader
            
            fh["size"]   = self.getHeaderSize() + self.getInfoSize() + self.getPixelDataSize()
            fh["offset"] = self.getHeaderSize() + self.getInfoSize()
            bib["size"] = self.getInfoSize()
        
        ## Calculates the number of bytes to fill each row in the Pixeldata block.
        #
        def getRowFiller(self):
            bib = self.bitmapInfoBlock
            w = bib["width"]
            tmp0 = 4
            tmp = (w*3)%tmp0
            if tmp > 0:
                tmp = tmp0-tmp    
            return tmp
        
        ## Writes the file header.
        #
        def writeFileHeader(self):
            f = self.file
            fh = self.fileHeader
            
            f.seek(0)
            f.write( fh["signature"] )
            f.write( self.getBytes( fh["size"], 4)  )
            f.write( self.getBytes( fh["res0"], 2)  )
            f.write( self.getBytes( fh["res1"], 2)  )
            f.write( self.getBytes( fh["offset"], 4)  )
        
        ## Writes the Bitmap information block.
        #
        def writeInfoBlock(self):
            f = self.file
            bib = self.bitmapInfoBlock
            
            f.seek( self.getHeaderSize() )
            f.write( self.getBytes( bib["size"], 4)  )
            f.write( self.getBytes( bib["width"], 4)  )
            f.write( self.getBytes( -bib["height"], 4)  )
            f.write( self.getBytes( bib["numColPlanes"], 2)  )
            f.write( self.getBytes( bib["bpp"], 2)  )
            f.write( self.getBytes( bib["compression"], 4)  )
            f.write( self.getBytes( bib["dataSize"], 4)  )
            f.write( self.getBytes( bib["hRes"], 4)  )
            f.write( self.getBytes( bib["vRes"], 4)  )
            f.write( self.getBytes( bib["palSize"], 4)  )
            f.write( self.getBytes( bib["impColors"], 4)  )
        
        ## Writes the pixel data block to create the file.
        #
        def createDataBlock(self, red = 255, green = 0, blue = 255):
            f = self.file
            bib = self.bitmapInfoBlock
            fh = self.fileHeader
            
            w = bib["width"]
            h = bib["height"]
            filler = self.getRowFiller()
            f.seek( fh["offset"] )
            
            # create first row to save time
            # At this point we could get a memory problem.
            line = ""
            for j in range(0, w):
                line = line + chr(blue)
                line = line + chr(green)
                line = line + chr(red)
            for j in range(0, filler):
                line = line + chr(0)
                
            for i in range(0, h):
                f.write( line )
        
        ## Sets the file pointer to the position
        #  of the given coordinates.
        #
        def setPos( self, x, y ):
            f = self.file
            bib = self.bitmapInfoBlock
            fh = self.fileHeader
            
            w = bib["width"]
            h = bib["height"]
            filler = self.getRowFiller()

            if x > w or y > h:
                return False
            
            self.workingPos = [x,y]
            f.seek( fh["offset"] + (w*3+filler)*y + x*3 )
            return True
    
    
    

    ##
    #
    def __init__( self, fileName, width = 100, height = 100 ):
        bmp = HugeBMP.__BMP( fileName, width, height )
        self.__bmp = bmp
        
    ## Writes a pixel value to the current position and moves the
    #  pointer to the next pixel. If the end of a row is reached.
    #  the pointer is moved to the first pixel in the next row.
    def setColor( self, red, green, blue ):
        
        bmp = self.__bmp
        bib = bmp.bitmapInfoBlock
        f = bmp.file
        wp = bmp.workingPos
        
        w = bib["width"]
        f.write( chr(blue) )
        f.write( chr(green) )
        f.write( chr(red) )
        
        wp[0] = wp[0]+1
        if wp[0] >= w:
            self.setPos( 0, wp[1]+1 )

    ## Sets the file pointer to the position
    #  of the given coordinates.
    #
    def setPos( self, x, y ):
        bmp = self.__bmp
        return bmp.setPos(x,y)
    
    ## Sets the color value of the given pixel.
    #
    def setPixel(self,x,y,red,green,blue):
        if not self.setPos(x,y):
            return False
            
        self.setColor(red,green,blue)
        return True
    
    ## Pastes an Image at the defined area.
    #
    def paste( self, img, targetPos):
        
        bmp = self.__bmp
        bib = bmp.bitmapInfoBlock
    
        w = bib["width"]
        h = bib["height"]
        
        if len(targetPos) == 2:
            targetPos = targetPos+(targetPos[0]+img.size[0], targetPos[1]+img.size[1])
        
        mb = ( 
            # left border - must be >= 0 and <= bmp.width
            max( 0, min(targetPos[0],w) ),
            # upper border - must be >= 0 and <= bmp.height
            max( 0, min(targetPos[1],h) ),
            # right border - must be <= img.width and must respect right border of bmp
            min( w, targetPos[2] ),
            # right border - must be <= img.height and must respect down border of bmp
            min( h, targetPos[3] )
        )

        sourceOffset = (
            min( 0, targetPos[0] ),
            min( 0, targetPos[1] ),
        )
        
        for y in range( mb[1], mb[3] ):
            bmp.setPos( mb[0],y )
            for x in range(mb[0], mb[2]):
                # This line shouldn't be necassary
                # but the seems to be a bug.
                bmp.setPos( x,y )
                
                c = img.getpixel( (x-mb[0]-sourceOffset[0], y-mb[1]-sourceOffset[1]) )
                self.setColor(c[0],c[1],c[2])

    ## Closes the image file.
    #                
    def close(self):
        bmp = self.__bmp
        f = bmp.file
        f.close()
        
