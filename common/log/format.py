from typing import List, Union, Tuple




class TextWarpSettings:
    def __init__(
            self,
            firstLinePrefix: str = None,
            firstBreakPrefix: str = None,
            followLinePrefix: str = None,
            followBreakPrefix: str = None
        ):
        """
        Settings for text warping
        """
        self.firstLinePrefix     = str( firstLinePrefix ) if firstLinePrefix != None else ""
        self.firstBreakPrefix    = str( firstBreakPrefix ) if firstBreakPrefix != None else "  "
        self.followLinePrefix    = str( followLinePrefix ) if followLinePrefix != None else ""
        self.followBreakPrefix   = str( followBreakPrefix ) if followBreakPrefix != None else "  "
        # TODO: add to construtor parameters
        self.spaceChars          = " "
        self.splitChars          = ",.:;?!"


    def maxIndent( self ) -> int:
        """
        Returns the maximum indent for formatting
        """
        return max( 
            len( self.firstLinePrefix ),
            len( self.firstBreakPrefix ),
            len( self.followLinePrefix ),
            len( self.followBreakPrefix ),
        )


    def indent( self, prefix: str ) -> 'TextWarpSettings':
        """
        Returns a copy of the text warp settings with identation
        """
        indent = ""
        if indent != None:
            indent = str( prefix )
        return TextWarpSettings(
            indent + self.firstLinePrefix,
            indent + self.firstBreakPrefix,
            indent + self.followLinePrefix,
            indent + self.followBreakPrefix
        )



class _TextWarp:
    def __init__(
            self,
            maximumWidth: int,
            textWarpSettings: TextWarpSettings
        ):
            """
            Auto warp text block
            """
            self.maximumWidth        = maximumWidth
            self.textWarpSettings    = textWarpSettings if textWarpSettings != None else TextWarpSettings()
            self.processingFirstLine = True
            self.lines               = []

            # TODO: assert we got at least one char per output line


    def _addLine( self, line: str ):
        """
        Adds a single line of text
        """
        breakMode        = False
        lineBegin        = True
        lineBuffer       = ""
        consumeSpace     = False
        lineHasNoDataYet = True
        while( True ):
            # consume space at front of line?
            if consumeSpace and lineBegin:
                if line[0:1] in self.textWarpSettings.spaceChars:
                    line = line[1:]
            consumeSpace = False

            # find line prefix
            if lineBegin:
                if breakMode:
                    lineBuffer += self.textWarpSettings.firstBreakPrefix if self.processingFirstLine else self.textWarpSettings.followBreakPrefix
                else:
                    lineBuffer += self.textWarpSettings.firstLinePrefix if self.processingFirstLine else self.textWarpSettings.followLinePrefix
                lineBegin        = False
                lineHasNoDataYet = True

            # content fits into output line buffer?
            t = lineBuffer + line
            if len( t ) <= self.maximumWidth:
                self.lines.append( t )
                self.processingFirstLine = False
                return         

            # split before space char and want to consume it?
            t = ""
            for cIndex in range( len( line ) ):
                c = line[ cIndex ]
                if( c in self.textWarpSettings.spaceChars ):
                    if( cIndex == 0 ):
                        t += c
                    else:
                        consumeSpace = True
                        break
                else:
                    t += c
            if len( lineBuffer + t ) <= self.maximumWidth:
                line = line[ len( t ) : ]
                lineBuffer += t
                lineHasNoDataYet = False
                continue

            # split after separator char, consuming next space?
            t = ""
            for cIndex in range( len( line ) ):
                c = line[ cIndex ]
                if( c in self.textWarpSettings.splitChars ):
                    t += c
                    consumeSpace = True
                    break
                else:
                    t += c
            if len( lineBuffer + t ) <= self.maximumWidth:
                line = line[ len( t ) : ]
                lineBuffer += t
                lineHasNoDataYet = False
                continue

            # no preferred split point found, split inbetween
            if lineHasNoDataYet:
                maxChars = self.maximumWidth - len( lineBuffer )
                lineBuffer += line[0:maxChars]
                line = line[maxChars:]

            # append rest of line
            self.lines.append( lineBuffer )
            lineHasNoDataYet = False
            breakMode        = True
            lineBegin        = True
            lineBuffer       = ""


    def addLine( self, text: str ):
        """
        Adds a one or more lines of text
        """
        # convert to string?
        if not isinstance( text, str ):
            text = str( text )

        # remove "\r"
        text = text.replace( '\r', '' )

        # treat "\t" as space
        text = text.replace( '\t', ' ' )

        # process multi line string?
        lines = text.split( "\n" )
        if( len( lines ) > 1 ):
            for line in lines:
                self._addLine( line )
        
        # process a single line
        else:
            self._addLine( text )


    def getFormatted( self ) -> List[ str ]:
        """
        Returns a list of lines after formatting
        """
        return self.lines




class Formatter:
    def __init__(
            self,
            maxWidth = None,
            defaultWarpSettings: TextWarpSettings = None,
            tableWarpSettingsLeft: TextWarpSettings = None,
            tableWarpSettingsRight: TextWarpSettings = None,
            leftWeight = 1.0,
            rightWeight = 1.0
        ):
        """
        Formatter for printing to the command line
        """
        # TODO:
        self.maxWidth               = maxWidth if maxWidth is not None else 80
        self.defaultWarpSettings    = defaultWarpSettings if defaultWarpSettings != None else TextWarpSettings()
        self.tableWarpSettingsLeft  = tableWarpSettingsLeft if tableWarpSettingsLeft != None else TextWarpSettings()
        self.tableWarpSettingsRight = tableWarpSettingsRight if tableWarpSettingsRight != None else TextWarpSettings()
        self.leftWeight             = leftWeight
        self.rightWeight            = rightWeight
        self.indentStack            = []

        pass


    def _write( self, line: str ):
        """
        Write formatted line to console
        """
        print( line )


    def _getIndent( self ):
        """
        Returns the indent as string
        """
        s = ""
        for indent in self.indentStack:
            s += indent
        return s


    def _writeLine( self, text: str ):
        """
        Write a single line
        """
        indent = self._getIndent()
        maxWidth = self.maxWidth - len( indent )
        warp = _TextWarp( maxWidth, self.defaultWarpSettings )
        warp.addLine( text )
        for line in warp.getFormatted():
            self._write( indent + line )


    def _writeTable( self, left: str, right: str ):
        """
        Write a table entry
        """
        fw = None
        indent = self._getIndent()

        # distribute space
        if self.maxWidth != None:
            i1 = self.tableWarpSettingsLeft.maxIndent()
            i2 = self.tableWarpSettingsRight.maxIndent()
            maxWidth = self.maxWidth - ( len( indent ) + i1 + i2 )
            if maxWidth < 1:
                maxWidth = 1
            wm = self.leftWeight + self.rightWeight
            w1 = int( maxWidth * ( self.leftWeight / wm ) )
            w2 = maxWidth - w1
            if w1 < 1:
                w1 = 1
            if w2 < 1:
                w2 = 1
            f1 = _TextWarp( w1 + i1, self.tableWarpSettingsLeft )
            f2 = _TextWarp( w2 + i2, self.tableWarpSettingsLeft )
            fw = w1 + i1
        else:
            f1 = _TextWarp( None, self.tableWarpSettingsLeft )
            f2 = _TextWarp( None, self.tableWarpSettingsLeft )

        # format table
        f1.addLine( str( left ) )
        f2.addLine( str( right ) )
        s1 = f1.getFormatted()
        s2 = f2.getFormatted()

        # check for longest line of left column
        if fw == None:
            fw = 0
            for l in s1:
                if len( l ) > fw:
                    fw = len( l )

        # print formatted table
        for lidx in range( max( len( s1 ), len( s2 ) ) ):
            sl1 = s1[lidx] if lidx < len( s1 ) else ""
            sl2 = s2[lidx] if lidx < len( s2 ) else ""
            sl1p = sl1 + " " * ( fw - len( sl1 ) )
            self._write( indent + sl1p + sl2 )


    def _writeTuple( self, list ):
        """
        Write a table entry from tuple
        """
        if len( list ) != 2:
            return False
        self._writeTable( list[0], list[1] )
        return True


    def pushIndent( self, indent: str ):
        """
        Push indentation
        """
        if indent == None:
            self.indentStack.append( "" )
        else:
            self.indentStack.append( str( indent ) )


    def popIndent( self ):
        """
        Pop indentation
        """
        if len( self.indentStack ) > 0:
            self.indentStack.pop()


    def newSection( self ):
        """
        Begin new text section
        """
        # TODO:


    def write(
            self,
            content: Union[ str, Tuple[ str, str ] ]
        ):
        """
        Write text lines or a table
        """
        if content != None:
            if isinstance( content, ( tuple, list ) ):
                if self._writeTuple( content ) == True:
                    return
            self._writeLine( str( content ) )
