
import argparse
import logging

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

    def __init__(self, mode, filepath):
        self.mode = mode
        self.filepath = filepath

    def run(self):
        from preprocessing.parsing import PWDumpParser
        pw_parser = PWDumpParser(filepath=self.filepath)

        analyzer = AnalysisEngine(mode=self.mode)

        for block in pw_parser.get_pw_block():
            print(analyzer.run_analysis_modules(block))



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