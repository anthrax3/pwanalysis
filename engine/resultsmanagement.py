
import statistics

from settings import FUNCTIONS

from collections import Counter


class ResultsManager(object):
    """
    Result storage class that can be passed between analysis modules and queried for stored results
    """

    results = None
    loaded_keys = None

    def __init__(self, results=None, keys=None):

        self.results = results if results else {}
        self.loaded_keys = keys if keys else []

    def add_result(self, source_results, dest_results=None):
        """
        Adds the given result dictionary to the result-set

        :param source_results: dictionary: results to be added to the destination result set
        :param dest_results: dictionary: results that the source results will be added to
                (if None, adds to self.results)
        :return:
        """

        if dest_results is None:
            dest_results = self.results

        for key in self.loaded_keys:
            ledger_mod_results = dest_results.get(key, None)
            new_mod_results = source_results.get(key, {})
            if not ledger_mod_results:
                dest_results[key] = new_mod_results
                continue

            # Add each new result set from the associated analytics function to the ledger
            for analytics_func, analytics_dict in new_mod_results.items():
                dest_results[key][analytics_func] = dict(Counter(dest_results[key][analytics_func]) +
                                                         Counter(analytics_dict))

        return dest_results

    def _calculate_meaningful_frequency_results(self):
        """
        Reduce the results based on simple statistical analysis.
        Remove any result that is less than the set threshold
        :return: pruned dictionary of meaningful results
        """

        pruned = {}
        if not self.results.get(FUNCTIONS.FREQ_ANALYSIS, None):
            return pruned

        max_len = len(sorted(self.results[FUNCTIONS.FREQ_ANALYSIS]['pass_ngram_freqs'].keys(),
                             key=lambda x: -len(x))[0])

        counts = self.results[FUNCTIONS.FREQ_ANALYSIS]['pass_ngram_freqs'].values()
        std_dev = statistics.stdev(counts)
        mean = statistics.mean(counts)
        threshold = max(1, mean)
        median = statistics.median(counts)
        mode = statistics.mode(counts)
        #
        # print('Mean: %s' % mean)
        # print('Std Dev: %s' % std_dev)
        # print('Thresh: %s' % threshold)
        # print('median: %s' % median)
        # print('mode: %s' % mode)
        # print('max: %s' % max(counts))
        # print('min: %s' % min(counts))

        for i in range(1, max_len+1):

            tmp = {
                FUNCTIONS.FREQ_ANALYSIS: {
                    'pass_ngram_freqs': {
                        k: v for k, v in self.results[FUNCTIONS.FREQ_ANALYSIS]['pass_ngram_freqs'].items()
                        if len(k) == i and int(v) > threshold}}}

            pruned = self.add_result(tmp, pruned)

        return pruned

    def print_top_ngrams(self):
        """
        Prints the top 10 ngrams for each size of ngram in the given dataset

        :return:
        """

        print('Calculating top ngrams...')

        pruned = self._calculate_meaningful_frequency_results()

        if not self.results.get(FUNCTIONS.FREQ_ANALYSIS, None):
            return

        max_len = len(sorted(pruned[FUNCTIONS.FREQ_ANALYSIS]['pass_ngram_freqs'].keys(),
                             key=lambda x: -len(x))[0])

        for i in range(1, max_len+1):
            tmp = {k: v for k, v in pruned[FUNCTIONS.FREQ_ANALYSIS]['pass_ngram_freqs'].items() if len(k) == i}
            print('%2d: %s' % (i, sorted(tmp.items(), key=lambda x: -x[1])[:20]))

