
import logging

from settings import MODES, FUNCTIONS, CONSTANTS
from Exceptions import PWAnalysisException

logger = logging.getLogger(__name__)
if CONSTANTS.DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.WARNING)
fh = logging.FileHandler(CONSTANTS.LOGFILE)
logger.addHandler(fh)


class AnalysisModuleTemplate(object):

    def run(self, dataset, mode):
        results = []

        if mode == MODES.MODE_USERPASS:
            results = self.analyze_userpass(dataset)

        elif mode == MODES.MODE_PASSWORD:
            results = self.analyze_pass(dataset)

        return results

    def analyze_userpass(self, dataset):
        return {}

    def analyze_pass(self, dataset):
        return {}


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
                try:
                    self.modules[m] = self.import_modules(path)
                except ImportError:
                    logger.error('Unable to load module: %s, Continuing without it.' % path)

    def import_modules(self, name):
        components = str(name).split('.')
        clazz = components[-1]
        mod = __import__('.'.join(components[:-1]), globals(), locals(), [components[-1]], 0)
        return getattr(mod, clazz)()

    def run_analysis_modules(self, dataset):
        """
        Run all registered analysis modules on the given dataset.
        A registered analysis module is one that is successfully loaded for execution using the dynamic loader
        :param dataset:
        :return:
        """

        result_set = {}

        for name, module in self.modules.items():
            results = module.run(dataset, self.mode)
            result_set[name] = results

        return result_set







