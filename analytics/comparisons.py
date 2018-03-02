
from analytics.base import AnalysisModuleTemplate


class ComparisonAnalyzer(AnalysisModuleTemplate):

    def analyze_userpass(self, dataset, results_manager=None):
        return {}

    def analyze_pass(self, dataset, results_manager=None):
        return {}