#!/usr/bin/env python3
"""
Analyze Repos Agent - Clone GitHub repositories and analyze code metrics
"""
import os
import sys
import asyncio
import argparse
import shutil
from repo_analyzer import RepoAnalyzer, ExcelHandler
from logger_config import LoggerConfig

logger = LoggerConfig.setup_logger('analyze_repos')


class AnalysisRunner:
    """Runner for repository analysis with summary and cleanup"""

    def __init__(self, analyzer):
        """
        Initialize runner

        Args:
            analyzer: RepoAnalyzer instance
        """
        self.analyzer = analyzer

    async def run(self, cleanup=True):
        """
        Run the complete analysis pipeline

        Args:
            cleanup: Whether to remove cloned repositories after analysis

        Returns:
            List of analyzed repository data
        """
        try:
            repos_data = self.analyzer.read_excel_data()
            repos_data = await self.analyzer.clone_all_repos(repos_data)
            repos_data = self.analyzer.analyze_all_repos(repos_data)

            ExcelHandler.export_results(
                repos_data,
                self.analyzer.output_file,
                self.analyzer.small_file_threshold
            )

            self.print_summary(repos_data)

            if cleanup:
                self.cleanup_temp_files()

            return repos_data

        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    def print_summary(self, repos_data):
        """
        Print summary of analysis

        Args:
            repos_data: List of repository data dictionaries
        """
        print(f"\n{'='*70}")
        print(f"Analysis Summary")
        print(f"{'='*70}")

        total = len(repos_data)
        analyzed = sum(1 for r in repos_data if r['status'] == 'analyzed')
        failed = sum(1 for r in repos_data if r['status'] == 'clone_failed')
        no_url = sum(1 for r in repos_data if r['status'] == 'no_url')

        print(f"Total Repositories: {total}")
        print(f"Successfully Analyzed: {analyzed}")
        print(f"Clone Failed: {failed}")
        print(f"No URL: {no_url}")

        if analyzed > 0:
            total_lines_sum = sum(r['total_lines'] for r in repos_data if r['status'] == 'analyzed')
            avg_lines = total_lines_sum / analyzed
            print(f"\nAverage Lines per Repo: {int(avg_lines):,}")

    def cleanup_temp_files(self):
        """Remove temporary cloned repositories"""
        if os.path.exists(self.analyzer.temp_dir):
            print(f"\nCleaning up temporary files in {self.analyzer.temp_dir}...")
            shutil.rmtree(self.analyzer.temp_dir)
            print(f"✓ Cleanup complete")


async def main():
    session_id = LoggerConfig.get_session_id()
    logger.info(f"{"="*70}")
    logger.info(f"Analyze Repos session started - Session ID: {session_id}")
    logger.info(f"{"="*70}")

    parser = argparse.ArgumentParser(
        description='Analyze Repos Agent - Clone GitHub repositories and analyze code metrics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  python analyze_repos.py --input Output_12.xlsx
  python analyze_repos.py --input Output_12.xlsx --output custom_output.xlsx
  python analyze_repos.py --input Output_12.xlsx --no-cleanup
  python analyze_repos.py --input Output_12.xlsx --temp-dir MyRepos
        """
    )

    parser.add_argument('--input', type=str, default='Output_12.xlsx',
                        help='Input Excel file with GitHub URLs (default: Output_12.xlsx)')
    parser.add_argument('--output', type=str, default='Output_23.xlsx',
                        help='Output Excel file with analysis results (default: Output_23.xlsx)')
    parser.add_argument('--temp-dir', type=str, default='TempFiles',
                        help='Directory to store cloned repositories (default: TempFiles)')
    parser.add_argument('--no-cleanup', action='store_true',
                        help='Keep cloned repositories after analysis (default: cleanup)')
    parser.add_argument('--small-file-threshold', type=int, default=150,
                        help='Maximum line count for a file to be considered "small" (default: 150)')

    args = parser.parse_args()

    analyzer = RepoAnalyzer(
        input_file=args.input,
        output_file=args.output,
        temp_dir=args.temp_dir,
        small_file_threshold=args.small_file_threshold
    )

    runner = AnalysisRunner(analyzer)
    await runner.run(cleanup=not args.no_cleanup)


if __name__ == '__main__':
    asyncio.run(main())
