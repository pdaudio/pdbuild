from multiprocessing.dummy import Value
import sys


from typing import List
from . import cmdarg
from . import cmdvalue
from . import exceptions
from ..log import format



# registry of parser items
class ParserRegistry:
    def __init__( self ):
        """
        register parser values and arguments
        """
        self.values = {}
        self.arguments = []
        self.data = None


    def addValue( self, value: cmdvalue.Value ):
        """
        Add value to parser
        """
        vKey = value.getIdentifier()
        if vKey in self.values:
            # already registered
            pass
        else:
            # need to register value
            self.values[ vKey ] = value


    def addArgument( self, arg: cmdarg.Argument ):
        """
        Add a command to the commandline parser
        """
        # TODO: check not registering twice
        # TODO: check if referred value is known
        self.arguments.append( arg )


    def valueKeys( self ) -> List[ str ]:
        """
        Returns the keys of all known values
        """
        keys = []
        for value in self.values:
            keys.append( value )
        return keys


    def get( self, valueIdent: str ) -> cmdvalue.Value:
        """
        Returns a value by identifier
        """
        if valueIdent in self.values:
            return self.values[ valueIdent ]
        return None


    def overwrite( self, valueIdent: str, value ) -> None:
        """
        Sets a value by identifier
        """
        r = self.get( valueIdent )
        if r != None:
            r.overwrite( value )
        else:
            raise KeyError( "command line key " + valueIdent + " is unknown" )


    def resolve( self, valueIdent: str ):
        """
        Resolves default or value by key
        """
        r = self.get( valueIdent )
        if r != None:
            return r.get()
        return None


    def isSet( self, valueIdent: str ):
        """
        Check if key is set
        """
        r = self.get( valueIdent )
        if r != None:
            return r.isSet()
        return None


    def createContext( self ):
        """
        Create parser context
        """
        copy = ParserRegistry()
        copy.values = self.values
        copy.arguments = self.arguments
        copy.data = {}
        for vKey in self.values:
            value = self.values[ vKey ]
            copy.data[ value.getIdentifier() ] = value.create()
        return copy


    def _formatCommands( self, value: cmdvalue.Value, cmds: list ):
        """
        Print comands to modify a single value
        """
        s = ""
        for c in cmds:
            if s != "":
                s += ", "
            s += "--" + c.getCommand()
            argDesc = c.getArgumentDescription()
            if not( argDesc in( None, "" ) ):
                s += " " + argDesc
        return s


    def _formatDescription( self, value: cmdvalue.Value ):
        """
        Format description text for command line help
        """
        return value.getDescription()


    def printHelp( self, maxWidth: int = 80 ):
        """
        Print help for commandline
        """
        # console formatter
        fmtDefault = format.TextWarpSettings()
        fmtKey = format.TextWarpSettings().indent( "  " )
        fmtValue = format.TextWarpSettings().indent( "  " )
        formatter = format.Formatter(
            maxWidth,
            fmtDefault,
            fmtKey,
            fmtValue,
            leftWeight = 0.4,
            rightWeight = 0.6
        )

        # collect categories to print, collect parse command by value
        categoryOrder = []
        categories = {}
        for vk in self.values:
            v = self.values[ vk ]
            if v.getCategory() in categories:
                categories[ v.getCategory() ].append( v )
            else:
                categoryOrder.append( v.getCategory() )
                categories[ v.getCategory() ] = [ v ]

        # collect arguments by value binding
        cmdsByValue = {}
        for arg in self.arguments:
            valBinding = arg.getValueBinding()
            if valBinding in cmdsByValue:
                cmdsByValue[ valBinding ].append( arg )
            else:
                cmdsByValue[ valBinding ] = [ arg ]

        # iterate categories and print
        firstCategory = True
        for cIndex in categoryOrder:
            categoryWritten = False
            isFirstValue = True

            # process category
            category = categories[ cIndex ]
            for value in category:
                # find arguments to set option
                cmds = cmdsByValue[ value.getIdentifier() ] if value.getIdentifier() in cmdsByValue else []

                if len( cmds ) > 0:
                    # need to write category?
                    if firstCategory == True:
                        formatter.write( "" )
                    firstCategory = False
                    if categoryWritten == False:
                        formatter.write( cIndex )
                        categoryWritten = True

                    # format value text
                    if isFirstValue == False:
                        formatter.write( "" )
                    isFirstValue = False
                    cmdText = self._formatCommands( value, cmds )
                    descText = self._formatDescription( value )
                    formatter.write( ( cmdText, descText ) )




# command line parser
class Parser:
    def __init__(
            self,
            grammar: ParserRegistry,
            args: List[ str ]
        ):
        """
        Creates a new command line parser
        """
        self.grammar = grammar
        self.context = grammar.createContext()
        self.args = args


    @staticmethod
    def parse(
            grammar: ParserRegistry,
            args: List[ str ] = None,
            ignoreUnknown: bool = False
        ) -> ParserRegistry:
        """
        Parse command line
        """
        p = Parser( grammar, args if args != None else sys.argv[1:] )
        return p._parse( ignoreUnknown )


    def _parseCommand( self, cmd: str, index: int, args: List[ str ] ):
        """
        Parse single command
        """
        # find command to parse
        cmdInstance = None
        for arg in self.grammar.arguments:
            if arg.getCommand() == cmd:
                cmdInstance = arg
                break

        # abort if command is not found
        if cmdInstance == None:
            return False

        # find associated value
        valueInstance = None
        if cmdInstance.getValueBinding() in self.grammar.values:
            valueInstance = self.grammar.values[ cmdInstance.getValueBinding() ]

        # assert value instance is present
        assert valueInstance != None, "can not find value attached to --" + cmdInstance.getCommand()

        # parse command
        cmdInstance.parse( cmdarg._ParsedValues( valueInstance, index, self.args, args ) )
        return True


    def _generateValueMissingException( self, value: Value ):
        """
        Generate value missing exception
        """
        commands = []
        for cmd in self.grammar.arguments:
            if( cmd.getValueBinding() == value.getIdentifier() ):
                commands.append( cmd )
        raise exceptions.CmdLineMissingCommand( None, self.args, commands )


    def _parse( self, ignoreUnknown: bool ) -> ParserRegistry:
        """
        Parse command line
        """
        # process each argument
        argIndex = 0
        unknownFound = False 
        unknownCommandIndex = None
        while argIndex < len( self.args ):
            arg = self.args[argIndex]
            if arg.startswith( "--" ):
                # found command, extract argument list and parse
                cmd = arg[2:]
                argList = []
                argCounter = 1
                while( ( argIndex + argCounter ) < len ( self.args ) ):
                    a = self.args[ argIndex + argCounter ]
                    if a.startswith( "--" ):
                        break
                    argList.append( a )
                    argCounter += 1
                if( self._parseCommand( cmd, argIndex, argList ) == False ):
                    unknownFound = True
                    if unknownCommandIndex == None:
                        unknownCommandIndex = argIndex
                argIndex += argCounter
            else:
                # found argument, not allowed before a command was found
                raise exceptions.CmdLineNoArgumentExpected( argIndex, self.args )

        # check if command line parameter is missing?
        for vKey in self.context.values:
            v = self.context.values[ vKey ]
            if v.expected:
                if not v.isSet():
                    raise self._generateValueMissingException( v )

        # check for unknown command line options?
        if unknownFound:
            if ignoreUnknown != True:
                raise exceptions.CmdLineUnknownCommand( unknownCommandIndex, self.args )

        # return parsed context
        return self.context
