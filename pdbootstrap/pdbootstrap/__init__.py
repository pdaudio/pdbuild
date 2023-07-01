import sys, os
from .cmdline import parser, exceptions
from .globalargs import GlobalArgs
from .log import format




# pd build bootstrap already initialized=
initialized = False


# path of module invoking the build script
initialModulePath = None


# pd build workspace path
workspacePath = None




# setup command line parser for global build arguments
def setupCommandlineParser( ctx: parser.ParserRegistry ):
    global initialModulePath
    assert initialModulePath != None, "init needs to be called before calling setupCommandlineParser"
    globalArgs = GlobalArgs( os.path.dirname( initialModulePath ) )
    globalArgs.addToParser( ctx )




# load and setup pd build system
def init( buildModuleFile: str, requiredVersion: str ):

    # global states of pd build system
    global initialized
    global initialModulePath
    global workspacePath

    # already initialized?
    if( initialized == False ):
        initialized = True

        # setup initial module path
        if initialModulePath == None:
            initialModulePath = os.path.dirname( buildModuleFile )

        # setup argument parser
        ctx = parser.ParserRegistry()
        setupCommandlineParser( ctx )

        # parse global command line arguments
        parsedArgs = None
        try:
            parsedArgs = parser.Parser.parse( ctx, ignoreUnknown = True )
        except exceptions.CmdLineException as e:
            print( "invalid command line argument: " + str( e ) )
            print( "run with commandline argument '--general-help' for more informations." )
            sys.exit( 1 )

        # TODO: do not emit parsed settings
        for key in parsedArgs.valueKeys():
            print( key + " = " + str( parsedArgs.resolve( key ) ) )

        # show global command line help and exit?
        if( parsedArgs.resolve( "general.help" ) == True ):
            ctx.printHelp()
            fmt = format.Formatter()
            fmt.write( "" )
            fmt.write( "For build dependent help run with flag '--build-help'." )
            fmt.write( "Note: this will checkout all required dependencies in order to render help within the context of the project to build." )
            sys.exit( 0 )

        # setup workspace path
        workspacePath = parsedArgs.resolve( "general.workspace" )

        # initialize bootstrap librarian
        # TODO:

        # TODO: setup pdbuild
        # load pdbuild library
        # initialize pd build librarian
        # initialize pd build command line arguments

        # TODO: checkout or accept ( add to search path ) pdbuild module
        print( "CONTINUE" )
