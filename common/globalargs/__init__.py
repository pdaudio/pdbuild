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

        # workspace directory
        self.workspace = cmdvalue.Value(
            identifier   = "general.workspace",
            description  = "Set workspace path. By default the workspace is set to the parent directory of the module where the build script is invoked.",
            category     = self.generalCategory,
            defaultValue = defaultWorkspacePath,
            expected     = False,
            unique       = True
        )

        self.workspace_Argument = cmdarg.StringArgument(
            self.workspace,
            "workspace",
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

        ctx.addValue( self.workspace )
        ctx.addArgument( self.workspace_Argument )
        
        ctx.addValue( self.librarianmode )
        ctx.addArgument( self.librarianmode_Argument )
        
        ctx.addValue( self.librariansearch )
        ctx.addArgument( self.librariansearch_Argument )
