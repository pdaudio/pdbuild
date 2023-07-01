from typing import List


class CmdLineException( Exception ):
    def __init__(
            self,
            what: str,
            argumentId: int,
            arguments: List[ str ]
        ):
        """
        Creates a new command line parse exception
        """
        super().__init__( what )
        self.what = what
        self.argumentId = argumentId
        self.arguments = arguments




class CmdLineNoArgumentExpected( CmdLineException ):
    def __init__(
            self,
            argumentId: int,
            arguments: List[ str ]
        ):
        """
        Creates a new argument not expected exception
        """
        super().__init__( "argument not expected", argumentId, arguments )


    def __str__( self ):
        argstr = self.arguments[ self.argumentId ]
        return "argument '" + argstr + "' @" + str( self.argumentId ) + " not expected"




class CmdLineUnknownCommand( CmdLineException ):
    def __init__(
            self,
            argumentId: int,
            arguments: List[ str ]
        ):
        """
        Creates an unkown argument exception
        """
        super().__init__( "command not found", argumentId, arguments )


    def __str__( self ):
        argstr = self.arguments[ self.argumentId ]
        return "command '" + argstr + "' @" + str( self.argumentId ) + " is unknown"




class CmdLineUnexpectedArgumentCount( CmdLineException ):
    def __init__(
            self,
            argumentId: int,
            arguments: List[ str ],
            command: str,
            expectedCount: int,
            gotCount: int
        ):
        """
        Creates an unexpected argument count exception
        """
        super().__init__( "unexpected argument count", argumentId, arguments )
        self.command = command
        self.expectedCount = expectedCount
        self.gotCount = gotCount


    def __str__( self ):
        return "command '--" + self.command + "' @" + str( self.argumentId ) + " expected " + str( self.expectedCount ) + " arguments but got " + str( self.gotCount )




class CmdLineCommandTwice( CmdLineException ):
    def __init__(
            self,
            argumentId: int,
            arguments: List[ str ],
            command: str
        ):
        """
        Creates a command issued twice exception
        """
        super().__init__( "command issued twice", argumentId, arguments )
        self.command = command


    def __str__( self ):
        return "command '--" + self.command + "' @" + str( self.argumentId ) + " can not be set twice"




class CmdLineMissingCommand( CmdLineException ):
    def __init__(
            self,
            argumentId: int,
            arguments: List[ str ],
            commands
        ):
        """
        Creates a command missing exception
        """
        super().__init__( "command missing", argumentId, arguments )
        self.commands = commands


    def __str__( self ):
        cmds = ""
        for cmd in self.commands:
            if cmds != "":
                cmds += ", "
            cmdStr = "--" + cmd.getCommand()
            cmdArgs = cmd.getArgumentDescription()
            if not ( cmdArgs in ( None, "" ) ):
                cmdStr += " " + cmdArgs
            cmds += cmdStr
        return "command '" + cmds + "' is expected to be set"




class CmdLineInvalidOption( CmdLineException ):
    def __init__(
            self,
            argumentId: int,
            arguments: List[ str ],
            command,
            optionValue
        ):
        """
        Creates an invalid commad option
        """
        super().__init__( "invalid option", argumentId, arguments )
        self.command = command
        self.optionValue = optionValue


    def __str__( self ):
        return "command '--" + self.command + "' has no option '" + str( self.optionValue ) + "'"
