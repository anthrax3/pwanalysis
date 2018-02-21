
class CONSTANTS:
    DEBUG = True
    LOGFILE = 'resources/pwanalysis.log'

    # Input File constants
    BLOCK_SIZE = 1000
    DELIM = ":"


class FUNCTIONS:
    """
    This class handles all modules for the password analysis tool.

    To add a module:
        1. Create a name (Ex: FREQ_ANALYSIS = 'Frequency Analysis')
        2. Add your named variable to the module list that it applies to (Ex: USER_PASS_MODULES, etc.)
        3. Add your module name and path to the MODULES dictionary

    Modules must inherit from the analytics.base.AnalysisModuleTemplate class and overwrite the two methods within.

    """

    FREQ_ANALYSIS = 'Frequency Analysis'
    USER_PASS_COMP = 'Username Password Comparison'

    # Modules to be executed on a user-password dataset
    USER_PASS_MODULES = (
        FREQ_ANALYSIS,
        USER_PASS_COMP,
    )

    # Modules to be executed on a password list dataset
    PASSWORD_MODULES = (
        FREQ_ANALYSIS,
    )

    # Associated modules and their paths (Add your module name and path
    MODULES = {
        FREQ_ANALYSIS: 'analytics.frequencies.FreqAnalyzer',
        USER_PASS_COMP: 'analytics.comparisons.ComparisonAnalyzer',
    }


class MODES:
    MODE_USERPASS = 'userpass'
    MODE_PASSWORD = 'password'

    ALL_MODES = (
        MODE_USERPASS,
        MODE_PASSWORD,
    )
