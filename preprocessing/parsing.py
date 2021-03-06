
import logging

from settings import CONSTANTS, MODES

logger = logging.getLogger(__name__)
if CONSTANTS.DEBUG:
    logging.basicConfig(format='%(asctime)s - %(levelname)s:%(message)s', level=logging.DEBUG)
else:
    logging.basicConfig(format='%(asctime)s - %(levelname)s:%(message)s', level=logging.WARNING)
fh = logging.FileHandler(CONSTANTS.LOGFILE)
fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s:%(message)s'))
logger.addHandler(fh)


class PWDumpParser(object):

    filepath = None
    mode = None

    def __init__(self, filepath, mode):
        self.filepath = filepath
        self.mode = mode

    def _load_file(self, filepath):
        raise NotImplementedError()

    def _parse_block(self, block):
        """
        Flow:
            if overwrite==false, check if there is already a cached version of this password dump (hash)
                Will be the same name as the file but with a diff extension
                If yes, return the already-parsed dump

        :param block: list of unparsed usernames and passwords
        :return:
        """
        parsed_lines = []
        for line in block:
            try:
                line = str(line).strip()

                if self.mode == MODES.MODE_USERPASS:
                    line = line.split(CONSTANTS.DELIM)

                parsed_lines.append(line)

            except Exception:
                logging.warning('could not parse line: %s' % line)

        return parsed_lines

    def get_pw_block(self, size=None):

        block_size = size if size else CONSTANTS.BLOCK_SIZE

        raw_lines = []
        with open(self.filepath, 'r') as f:
            eof = False
            while not eof:

                for i in range(block_size):
                    try:
                        line = f.readline()
                        if line:
                            raw_lines.append(line)
                        else:
                            eof = True
                            break
                    except UnicodeDecodeError:
                        logger.error('Could not parse line. Skipping line.')

                parsed_lines = self._parse_block(raw_lines)
                raw_lines = []
                yield parsed_lines



