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
    """
    Setup the commandline parser
    """
    global initialModulePath
    assert initialModulePath != None, "init needs to be called before calling setupCommandlineParser"
    globalArgs = GlobalArgs( os.path.dirname( initialModulePath ) )
    globalArgs.addToParser( ctx )




def _createDirectory( path: str ):
    """
    Create a directory required to run on
    """
    os.makedirs( path, exist_ok = True )




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

        # setup initial module path
        parsedArgs.overwrite( "general.initialmodule-dir", initialModulePath )

        # setup local repository source path
        parsedArgs.overwrite( "general.localrepos-dir", os.path.dirname( initialModulePath ) )

        # setup absolute workspace path
        workspacePath = parsedArgs.resolve( "general.workspace-dir" )
        workspacePath = os.path.abspath( workspacePath )
        parsedArgs.overwrite( "general.workspace-dir", str( workspacePath ) )

        # setup buildlog dir
        buildlogDefaultDir = workspacePath + '/.buildlog'
        buildlogDir = parsedArgs.resolve( "general.buildlog-dir" ) if parsedArgs.isSet( "general.buildlog-dir" ) else buildlogDefaultDir
        buildlogDir = os.path.abspath( buildlogDir )
        parsedArgs.overwrite( "general.buildlog-dir", buildlogDir )

        # setup fetched dir
        fetchedDefaultDir = workspacePath + '/.fetched'
        fetchedDir = parsedArgs.resolve( "general.fetched-dir" ) if parsedArgs.isSet( "general.fetched-dir" ) else fetchedDefaultDir
        fetchedDir = os.path.abspath( fetchedDir )
        parsedArgs.overwrite( "general.fetched-dir", fetchedDir )

        # setup cache dir
        cacheDefaultDir = workspacePath + '/.cache'
        cacheDir = parsedArgs.resolve( "general.cache-dir" ) if parsedArgs.isSet( "general.cache-dir" ) else cacheDefaultDir
        cacheDir = os.path.abspath( cacheDir )
        parsedArgs.overwrite( "general.cache-dir", cacheDir )

        # create directories required to run the build script
        _createDirectory( workspacePath )
        _createDirectory( buildlogDir )
        _createDirectory( fetchedDir )
        _createDirectory( cacheDir )

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

        # initialize bootstrap librarian
        # TODO:

        # TODO: setup pdbuild
        # load pdbuild library
        # initialize pd build librarian
        # initialize pd build command line arguments

        # TODO: checkout or accept ( add to search path ) pdbuild module
        print( "CONTINUE" )
