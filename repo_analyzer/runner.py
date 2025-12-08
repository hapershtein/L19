"""
Repository analysis runner
"""
import os
import shutil
from .excel_handler import ExcelHandler


class AnalysisRunner:
    """Run complete repository analysis pipeline"""

    @staticmethod
    async def run_analysis(analyzer, cleanup=True):
        """
        Run the complete analysis pipeline

        Args:
            analyzer: RepoAnalyzer instance
            cleanup: Whether to remove cloned repositories after analysis

        Returns:
            List of analyzed repository data
        """
        repos_data = analyzer.read_excel_data()
        repos_data = await analyzer.clone_all_repos(repos_data)
        repos_data = analyzer.analyze_all_repos(repos_data)

        ExcelHandler.export_results(
            repos_data,
            analyzer.output_file,
            analyzer.small_file_threshold
        )

        if cleanup and os.path.exists(analyzer.temp_dir):
            shutil.rmtree(analyzer.temp_dir)

        return repos_data
