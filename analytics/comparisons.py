
from analytics.base import AnalysisModuleTemplate


class ComparisonAnalyzer(AnalysisModuleTemplate):

    def analyze_userpass(self, dataset):
        return ['comp']

    def analyze_pass(self, dataset):
        return ['comp']