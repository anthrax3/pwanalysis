
import logging

from settings import CONSTANTS, MODES

logger = logging.getLogger(__name__)


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

    def get_pw_block(self):

        raw_lines = []
        with open(self.filepath, 'r') as f:
            eof = False
            while not eof:

                for i in range(CONSTANTS.BLOCK_SIZE):
                    line = f.readline()
                    if line:
                        raw_lines.append(line)
                    else:
                        eof = True
                        break

                parsed_lines = self._parse_block(raw_lines)
                raw_lines = []
                yield parsed_lines



