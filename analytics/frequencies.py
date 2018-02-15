
from analytics.base import AnalysisModuleTemplate


class FreqAnalyzer(AnalysisModuleTemplate):

    def analyze_userpass(self, dataset):
        return ['freq']

    def analyze_pass(self, dataset):
        return ['freq']

