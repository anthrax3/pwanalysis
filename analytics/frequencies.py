from itertools import chain
from analytics.base import AnalysisModuleTemplate


class FreqAnalyzer(AnalysisModuleTemplate):

    def analyze_userpass(self, dataset):
        """
        Run all analytics on a user-pass dataset
        :param dataset:
        :return: dictionary of various results
        """

        users, passes = self._gen_wordlist_from_userpass(dataset)

        user_ngram_freqs = self._n_gram_freq(users)
        pass_ngram_freqs = self._n_gram_freq(passes)

        return {
            'user_ngram_freqs': user_ngram_freqs,
            'pass_ngram_freqs': pass_ngram_freqs,
        }

    def analyze_pass(self, dataset):
        return {}

    def _gen_wordlist_from_userpass(self, userpass_dataset):
        """
        Take a user-pass dataset and split it into two wordlists, a user and password word list
        Remove any extensions from emails on the usernames (the '@' and anything after it)
        :param userpass_dataset:
        :return: user wordlist, pass wordlist
        """
        user_wordlist = [str(user)[0:str(user).index('@')] for user, pw in userpass_dataset]
        pass_wordlist = [str(pw) for user, pw in userpass_dataset]

        return user_wordlist, pass_wordlist

    def _n_gram_freq(self, word_list, existing_ngrams=None):
        """
        generate the ngram frequencies based on the given wordlist.
        :param word_list: list of strings (words)
        :param existing_ngrams: dictionary of existing ngrams to add these results to. Default uses a new one.
        :return: ngram dictionary of frequencies of each ngram (key)
        """

        if existing_ngrams:
            ngram_freqs = existing_ngrams
        else:
            ngram_freqs = {}

        for word in word_list:
            word_ngrams = self._gen_ngrams(word)

            for ng in word_ngrams:
                ng_count = ngram_freqs.get(ng, 0)
                ng_count += 1
                ngram_freqs[ng] = ng_count

        return ngram_freqs

    def _gen_ngrams(self, word):
        """
        Generate ngrams for a given word
        :param word: string
        :return: list of ngrams for the given word
        """

        ngrams = []
        tmp = list(word)
        for n in range(1, len(tmp)):
            ngrams.append([''.join(a) for a in list(zip(*[tmp[i:] for i in range(n)]))])

        return list(chain.from_iterable(ngrams))

