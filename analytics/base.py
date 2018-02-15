
from settings import MODES, FUNCTIONS
from Exceptions import PWAnalysisException


class AnalysisModuleTemplate(object):

    def run(self, dataset, mode):
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
            if m in modules and m not in self.modules:
                # self.modules[m] = __import__(path)
                self.modules[m] = self.import_modules(path)

    def import_modules(self, name):
        components = str(name).split('.')
        clazz = components[-1]
        mod = __import__('.'.join(components[:-1]), globals(), locals(), [components[-1]], 0)
        return getattr(mod, clazz)()

    def run_analysis_modules(self, dataset):
        result_set = {}

        for name, module in self.modules.items():
            results = module.run(dataset, self.mode)
            result_set[name] = results

        return result_set







