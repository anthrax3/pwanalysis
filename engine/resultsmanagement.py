
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

    def add_result(self, results):
        """
        Adds the given result dictionary to the result-set

        :param results: dictionary -- results
        :return:
        """

        for key in self.loaded_keys:
            ledger_mod_results = self.results.get(key, None)
            new_mod_results = results.get(key, {})
            if not ledger_mod_results:
                self.results[key] = new_mod_results
                continue

            # Add each new result set from the associated analytics function to the ledger
            for analytics_func, analytics_dict in new_mod_results.items():
                self.results[key][analytics_func] = dict(Counter(self.results[key][analytics_func]) +
                                                         Counter(analytics_dict))

    def print_top_ngrams(self):
        """
        Prints the top 10 ngrams for each size of ngram in the given dataset

        :return:
        """

        print('Calculating top ngrams...')
        max_len = len(sorted(self.results['Frequency Analysis']['pass_ngram_freqs'].keys(), key=lambda x: -len(x))[0])
        for i in range(1, max_len+1):
            tmp = {k: v for k, v in self.results['Frequency Analysis']['pass_ngram_freqs'].items() if len(k) == i}
            print('%2d: %s' % (i, sorted(tmp.items(), key=lambda x: -x[1])))

