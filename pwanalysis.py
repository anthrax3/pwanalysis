
import argparse
import logging
import time

from settings import MODES, CONSTANTS
from analytics.base import AnalysisEngine
from engine.resultsmanagement import ResultsManager


logger = logging.getLogger(__name__)
if CONSTANTS.DEBUG:
    logging.basicConfig(format='%(asctime)s - %(levelname)s:%(message)s', level=logging.DEBUG)
else:
    logging.basicConfig(format='%(asctime)s - %(levelname)s:%(message)s', level=logging.WARNING)
fh = logging.FileHandler(CONSTANTS.LOGFILE)
fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s:%(message)s'))
logger.addHandler(fh)


class Engine(object):

    mode = None
    filepath = None
    block_size = None

    analyzer = None
    results_manager = None
    # results = {}

    def __init__(self, mode, filepath, block_size=None):
        self.mode = mode
        self.filepath = filepath

        if block_size:
            self.block_size = block_size
        else:
            self.block_size = CONSTANTS.BLOCK_SIZE

    def run(self):
        from preprocessing.parsing import PWDumpParser
        pw_parser = PWDumpParser(filepath=self.filepath, mode=self.mode)

        self.analyzer = AnalysisEngine(mode=self.mode)
        self.results_manager = ResultsManager(keys=self.analyzer.get_loaded_modules())

        print('Starting Analysis Engine...')

        start_time = time.time()
        counter = 1
        for block in pw_parser.get_pw_block(self.block_size):
            block_start = time.time()
            print('Executing block (size=%s) number %s. ' % (self.block_size, counter), end='')
            r = self.analyzer.run_analysis_modules(block, results_manager=self.results_manager)
            self.results_manager.add_result(r)
            counter += 1
            print('Block Evaluation Time: %s' % (time.time() - block_start))

        self.results_manager.print_top_ngrams()

        print('Total Program Execution Time: %s' % (time.time() - start_time))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--userpass',
        help='A file that contains the usernames and passwords (in the standard <user>:<pass> format) on each line')
    parser.add_argument(
        '--pw',
        help='A file that contains a password on each line')
    parser.add_argument(
        '-v',
        '--verbose',
        help='Verbose output mode',
        action='store_true')
    parser.add_argument(
        '--block',
        type=int,
        help='Block (chunk) size to read from file at a time (for memory optimization) (Default: %s)' %
             CONSTANTS.BLOCK_SIZE
    )

    args = parser.parse_args()

    if not (args.userpass or args.pw):
        parser.error('Either the --userpass or --pw flag must be used')

    if args.verbose:
        logging.basicConfig(format='%(asctime)s - %(levelname)s:%(message)s', level=logging.INFO)

    engine = None
    if args.userpass:
        engine = Engine(mode=MODES.MODE_USERPASS, filepath=args.userpass, block_size=args.block)
    if args.pw:
        engine = Engine(mode=MODES.MODE_PASSWORD, filepath=args.pw, block_size=args.block)

    if engine:
        engine.run()
    else:
        parser.error('An unknown input error has occurred.')