#
# general settings of the build system
#




from ..cmdline import cmdarg
from ..cmdline import cmdvalue
from ..cmdline import parser




class GlobalArgs:
    def __init__( self, defaultWorkspacePath: str ):
        """
        Global commandline arguments used by pd build.
        """

        # general category
        self.generalCategory = "General build settings:"

        # show general help?
        self.generalHelp = cmdvalue.Value(
            identifier   = "general.help",
            description  = "Show help for general command line arguments.",
            category     = self.generalCategory,
            defaultValue = False,
            unique       = False,
            expected     = False
        )

        self.generalHelp_Argument = cmdarg.FlagArgument(
            self.generalHelp,
            "help"
        )

        # directory of module where the build script is invoked
        self.initialModule = cmdvalue.Value(
            identifier   = "general.initialmodule-dir",
            description  = "Directory of initial module where the build script was invoked.",
            category     = self.generalCategory,
            defaultValue = None,
            expected     = False,
            unique       = True
        )

        # directory of module where the build script is invoked
        self.localRepos = cmdvalue.Value(
            identifier   = "general.localrepos-dir",
            description  = "Directory where local repositories are located.",
            category     = self.generalCategory,
            defaultValue = None,
            expected     = False,
            unique       = True
        )

        # workspace directory
        self.workspace = cmdvalue.Value(
            identifier   = "general.workspace-dir",
            description  = "Set workspace path. By default the workspace is set to the parent directory of the module where the build script is invoked with /.workspace appended.",
            category     = self.generalCategory,
            defaultValue = defaultWorkspacePath + '/.workspace',
            expected     = False,
            unique       = True
        )

        self.workspace_Argument = cmdarg.StringArgument(
            self.workspace,
            "workspace-dir",
            "<dir>"
        )

        # build log directory
        self.buildlogPath = cmdvalue.Value(
            identifier   = "general.buildlog-dir",
            description  = "Set build log path. By default the build log is set to '${workspace-dir}/.buildlog'.",
            category     = self.generalCategory,
            expected     = False,
            unique       = True
        )

        self.buildlogPath_Argument = cmdarg.StringArgument(
            self.buildlogPath,
            "buildlog-dir",
            "<dir>"
        )

        # fetched directory
        self.fetchedPath = cmdvalue.Value(
            identifier   = "general.fetched-dir",
            description  = "Set path to fetch dependencies. By default the build log is set to '${workspace-dir}/.fetched'.",
            category     = self.generalCategory,
            expected     = False,
            unique       = True
        )

        self.fetchedPath_Argument = cmdarg.StringArgument(
            self.fetchedPath,
            "fetch-dir",
            "<dir>"
        )

        # cache directory
        self.cachePath = cmdvalue.Value(
            identifier   = "general.cache-dir",
            description  = "Set path of cache. By default the build log is set to '${workspace-dir}/.cache'.",
            category     = self.generalCategory,
            expected     = False,
            unique       = True
        )

        self.cachePath_Argument = cmdarg.StringArgument(
            self.cachePath,
            "cache-dir",
            "<dir>"
        )

        # librarian mode
        self.librarianmode = cmdvalue.Value(
            identifier   = "general.librarian.mode",
            description  = "Mode of librarian, controls the check out strategie of dependencies.",
            category     = self.generalCategory,
            defaultValue = "update",
            expected     = False,
            unique       = True,
            options      =
            [
                cmdvalue.Option( "none",   "do not fetch dependent repositories." ),
                cmdvalue.Option( "fetch",  "fetch only missing dependencies." ),
                cmdvalue.Option( "update", "update dependent repositories if no local changes are present." ),
                cmdvalue.Option( "force",  "update dependent repositories, stash local changes if present." ),
                cmdvalue.Option( "asis",   "ignore version constraints on local repositories, only fetch other dependencies." )
            ]
        )

        self.librarianmode_Argument = cmdarg.StringArgument(
            self.librarianmode,
            "librarian-mode",
            "<mode>",
        )

        # librarian search paths
        self.librariansearch = cmdvalue.ListValue(
            identifier   = "general.librarian.origins",
            description  = "Search paths of librarian, list of URLs to search for dependencies.\n" +
                           "A paths needs to be a URL to a git repository in the format: <scheme>:<scheme-specific-part>/${module}<suffix> -> i.e. https://github.com/xyz/${module}.git\n" +
                           "${module} will be replaced by the name of the dependent module.\n"
                           "When the value starts with '=' the search list will be overwritten,\n" +
                           "when the value starts with '+' it will be prepended to the search list,\n" + 
                           "otherwise the entry will be appended to the repo search list.",
            category     = self.generalCategory,
            initialValue = [ 'https://github.com/pdaudio/${module}' ],
            expected     = False
        )

        self.librariansearch_Argument = cmdarg.StringArgument(
            self.librariansearch,
            "librarian-origins",
            "<URL>",
        )


    def addToParser( self, ctx: parser.ParserRegistry ):
        """
        Add parameters to commandline parser registry
        """
        ctx.addValue( self.generalHelp )
        ctx.addArgument( self.generalHelp_Argument )

        ctx.addValue( self.initialModule )
        ctx.addValue( self.localRepos )

        ctx.addValue( self.workspace )
        ctx.addArgument( self.workspace_Argument )

        ctx.addValue( self.buildlogPath )
        ctx.addArgument( self.buildlogPath_Argument )

        ctx.addValue( self.fetchedPath )
        ctx.addArgument( self.fetchedPath_Argument )

        ctx.addValue( self.cachePath )
        ctx.addArgument( self.cachePath_Argument )
        
        ctx.addValue( self.librarianmode )
        ctx.addArgument( self.librarianmode_Argument )
        
        ctx.addValue( self.librariansearch )
        ctx.addArgument( self.librariansearch_Argument )
