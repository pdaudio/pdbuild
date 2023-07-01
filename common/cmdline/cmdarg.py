from typing import Union, List

from .cmdvalue import Value
from .exceptions import CmdLineUnexpectedArgumentCount, CmdLineCommandTwice, CmdLineInvalidOption



class _ParsedValues:
    def __init__(
            self,
            value: Value,
            argIndex: int,
            allArgs: List[ str ],
            args: List[ str ]
        ):
        """
        Values from parser
        """
        self.value = value
        self.argIndex = argIndex
        self.allArgs = allArgs
        self.args = args




class Argument:
    def __init__(
            self,
            valueBinding: Union[ str, Value ],
            command: str
        ):
        """
        Create a new parser argument
        """
        # bind command to it's value by logical name
        self.command = command
        self.valueBinding = valueBinding
        if isinstance( valueBinding, Value ):
            self.valueBinding = valueBinding.getIdentifier()


    def getCommand( self ):
        """
        Returns the command used to process this argument
        """
        return self.command


    def getValueBinding( self ):
        """
        Returns the logical name of the bound value
        """
        return self.valueBinding


    def getArgumentDescription( self ):
        """
        Prints the description of the expected arguments
        """
        return ""


    def _validate( self, ctx: _ParsedValues ):
        """
        Validate parameter usage
        """
        if ctx.value.unqiue:
            if( ctx.value.isSet() ):
                raise CmdLineCommandTwice( ctx.argIndex, ctx.allArgs, self.getCommand() )


    def _assertValueCount( self, ctx: _ParsedValues, count: int ):
        """
        Assert to have N values
        """
        if len( ctx.args ) != count:
            raise CmdLineUnexpectedArgumentCount( ctx.argIndex, ctx.allArgs, self.getCommand(), count, len( ctx.args ) )


    def parse( self, ctx: _ParsedValues ):
        """
        Parse from commandline
        """
        assert False, "To be implemented by base class"




class FlagArgument( Argument ):
    def __init__(
            self,
            valueBinding: Union[ str, Value ],
            command: str,
            data: bool = True
        ):
        """
        Create a new flag parser argument
        """
        super().__init__( valueBinding, command )
        self.data = data


    def parse( self, ctx: _ParsedValues ):
        self._validate( ctx )
        self._assertValueCount( ctx, 0 )
        ctx.value.onParse( self.data )



class StringArgument( Argument ):
    def __init__(
            self,
            valueBinding: Union[ str, Value ],
            command: str,
            argName: str
        ):
        """
        Create a new string parser argument
        """
        super().__init__( valueBinding, command )
        self.argName = argName


    def getArgumentDescription( self ):
        return self.argName


    def parse( self, ctx: _ParsedValues ):
        self._validate( ctx )
        self._assertValueCount( ctx, 1 )
        if( ctx.value.getOptions() != None ):
            optionFound = False
            for option in ctx.value.getOptions():
                if option.option == ctx.args[0]:
                    optionFound = True
                    break
            if( optionFound == False ):
                raise CmdLineInvalidOption( ctx.argIndex, ctx.allArgs, self.getCommand(), ctx.args[0] )
        ctx.value.onParse( ctx.args[0] )
