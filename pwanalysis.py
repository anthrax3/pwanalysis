
import argparse
import logging

from collections import Counter

from settings import MODES, CONSTANTS
from analytics.base import AnalysisEngine


logger = logging.getLogger(__name__)
if CONSTANTS.DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.WARNING)
fh = logging.FileHandler(CONSTANTS.LOGFILE)
logger.addHandler(fh)


class Engine(object):

    mode = None
    filepath = None

    analyzer = None
    results = {}

    def __init__(self, mode, filepath):
        self.mode = mode
        self.filepath = filepath

    def run(self):
        from preprocessing.parsing import PWDumpParser
        pw_parser = PWDumpParser(filepath=self.filepath, mode=self.mode)

        self.analyzer = AnalysisEngine(mode=self.mode)

        for block in pw_parser.get_pw_block():
            r = self.analyzer.run_analysis_modules(block)
            self._merge_results(r)
            # print('Block Results: %s' % r)

        # print('Ledger: %s' % (self.results, ))
        self._print_top_ngrams()

    def _merge_results(self, new_results):
        """
        Iterates through loaded modules (names are keys in results) and adds the results to the general results ledger.
        Each module has multiple results dicts from their various analytics functions

        Example:
            keys = ['module1', 'module2']

            results {
                'module1': {
                    'analytics1': {...}
                    'analytics2': {...}
                    ...
                },
                'module2': {
                    ...
                },
                ...
            }

        NOTE: This method allows for combination of results from files that are too large to store im memory.

        :param new_results:
        :return:
        """
        keys = self.analyzer.get_loaded_modules()

        for key in keys:
            ledger_mod_results = self.results.get(key, None)
            new_mod_results = new_results.get(key, {})
            if not ledger_mod_results:
                self.results[key] = new_mod_results
                continue

            # Add each new result set from the associated analytics function to the ledger
            for analytics_func, analytics_dict in new_mod_results.items():
                self.results[key][analytics_func] = dict(Counter(self.results[key][analytics_func]) +
                                                         Counter(analytics_dict))

    def _print_top_ngrams(self):

        max_len = len(sorted(self.results['Frequency Analysis']['pass_ngram_freqs'].keys(), key=lambda x: -len(x))[0])
        for i in range(1, max_len+1):
            tmp = {k: v for k, v in self.results['Frequency Analysis']['pass_ngram_freqs'].items() if len(k) == i}
            print('%2d: %s' % (i, sorted(tmp.items(), key=lambda x: -x[1])))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--userpass",
        help="A file that contains the usernames and passwords (in the standard <user>:<pass> format) on each line")
    parser.add_argument(
        "--pw",
        help="A file that contains a password on each line")

    args = parser.parse_args()

    if not (args.userpass or args.pw):
        parser.error('Either the --userpass or --pw flag must be used')

    engine = None
    if args.userpass:
        engine = Engine(mode=MODES.MODE_USERPASS, filepath=args.userpass)
    if args.pw:
        engine = Engine(mode=MODES.MODE_PASSWORD, filepath=args.pw)

    if engine:
        engine.run()
    else:
        parser.error('An unknown input error has occurred.')