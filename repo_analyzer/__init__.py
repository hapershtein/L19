"""
Repository Analysis Package
"""
from .analyzer import RepoAnalyzer
from .excel_handler import ExcelHandler
from .runner import AnalysisRunner

# Add run method to RepoAnalyzer
async def _run(self, cleanup=True):
    return await AnalysisRunner.run_analysis(self, cleanup)

RepoAnalyzer.run = _run

__all__ = ['RepoAnalyzer', 'ExcelHandler', 'AnalysisRunner']
