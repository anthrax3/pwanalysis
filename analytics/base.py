
from settings import MODES, FUNCTIONS
from Exceptions import PWAnalysisException


class AnalysisModuleTemplate(object):

    def run(self, dataset):
        return []


class AnalysisEngine(object):

    mode = None
    modules = {}

    def __init__(self, mode):
        if mode in MODES.ALL_MODES:
            self.mode = mode
        else:
            raise PWAnalysisException('Invalid mode specified.')

        # Dynamically load modules from settings
        modules = []
        if mode == MODES.MODE_PASSWORD:
            modules = FUNCTIONS.PASSWORD_MODULES
        if mode == MODES.MODE_USERPASS:
            modules = FUNCTIONS.USER_PASS_MODULES

        for m, path in FUNCTIONS.MODULES.items():
            if m in modules:
                self.modules[m] = __import__(path)

    def run_analysis_modules(self):
        pass







