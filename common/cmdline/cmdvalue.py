from typing import List




# option of command value
class Option:
    def __init__( self, option: str, description ):
        """
        Create a new option for OptionValue
        """
        self.option      = option
        self.description = description
        pass




# value of command parameter
class Value:
    def __init__(
            self,
            identifier: str,
            description: str,
            category: str,
            defaultValue = None,

            # validate settings
            expected: bool = False,
            unique: bool = True,

            # optional list of valid options
            options: List[ Option ] = None
        ):
        """
        Creates a new value factory for a command line
        """
        self.identifier  = identifier
        self.description = description
        self.category = category
        self._isSet = False
        self._data = None
        self._default = defaultValue
        self._defaultNode = None

        # validation flags
        self.expected = expected
        self.unqiue = unique

        # optional list of options
        self.options = options


    def create( self ):
        """
        Creates a storage item for a commandline value
        """
        n = type( self )( identifier = self.identifier, description = self.description, category = self.category )
        n._defaultNode = self
        return n


    def getCategory( self ):
        """
        Returns the category of this value
        """
        return self.category


    def get( self ):
        """
        Get value
        """
        if( self.isSet() == False ):
            return self.getDefault()
        return self._data


    def isSet( self ):
        """
        Returns true when set by parser
        """
        return self._isSet


    def getDefault( self ):
        """
        Returns the default value of this commandline parameter
        """
        if( self._defaultNode != None ):
            return self._defaultNode.getDefault()
        return self._default

    
    def setDefault( self, override: bool, data ):
        """
        Sets the default value of this command line parameter
        """
        if( override == True ) and ( self._defaultNode != None ):
            self._defaultNode._default = data
        else:
            self._default = data
            self._defaultNode = None


    def onParse( self, data ):
        """
        Sets the value of this command line parameter
        """
        self._data = data
        self._isSet = True


    def getIdentifier( self ):
        """
        Return identifier
        """
        return self.identifier


    def getOptions( self ) -> List[ Option ]:
        """
        Returns a list of accepted options or None when all values are accepted
        """
        return self.options


    def _formatOptionDescriptions( self ):
        """
        Format description of options
        """
        result = ""
        for opt in self.options:
            result += "\n" + opt.option + ": " + opt.description
        return result


    def getDescription( self ):
        """
        Return description
        """
        if( self.options != None ):
            return self.description + "\n" + self._formatOptionDescriptions()
        else:
            return self.description

    


# list value of command parameter
class ListValue( Value ):
    def __init__(
            self,
            identifier: str,
            description: str,
            category: str,
            initialValue = [],

            # validate settings
            expected: bool = False,
        ):
        """
        Creates a new list value factory for a command line
        """
        super().__init__(

            identifier = identifier,
            description = description,
            category = category,
            defaultValue = [] + initialValue,
            expected = expected,
            unique = False
        )
        self._data = [] + initialValue


    def onParse( self, data ):
        """
        Sets the value of this command line parameter
        """
        # insert entry into list
        dStr = str( data )
        if( dStr == "=" ):
            self._data = []
        elif( dStr.startswith( "=" ) ):
            self._data = [ dStr[1:] ]
        elif( dStr.startswith( "+" ) ):
            self._data = [ dStr[1:] ] + self._data
        else:
            self._data.append( dStr )

        # value is set from command line
        self._isSet = True
