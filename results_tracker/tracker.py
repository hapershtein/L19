"""
Results tracking and visualization for pipeline agents
"""
import os
from datetime import datetime
from .gmail_tracker import GmailTracker
from .repo_tracker import RepoTracker
from .message_tracker import MessageTracker
from .email_tracker import EmailTracker


class ResultsTracker:
    """Track and visualize agent activity in Results.md"""

    RESULTS_FILE = "Results.md"

    @staticmethod
    def initialize_results_file():
        """Initialize or reset the Results.md file"""
        with open(ResultsTracker.RESULTS_FILE, 'w', encoding='utf-8') as f:
            f.write("# Pipeline Execution Results\n\n")
            f.write(f"**Execution Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")

    @staticmethod
    def add_gmail_search_results(search_data):
        """
        Add Gmail search results to Results.md

        Args:
            search_data: List of search result dictionaries
        """
        with open(ResultsTracker.RESULTS_FILE, 'a', encoding='utf-8') as f:
            GmailTracker.add_results(f, search_data)

    @staticmethod
    def add_repo_analysis_results(repos_data):
        """
        Add repository analysis results to Results.md

        Args:
            repos_data: List of repository analysis dictionaries
        """
        with open(ResultsTracker.RESULTS_FILE, 'a', encoding='utf-8') as f:
            RepoTracker.add_results(f, repos_data)

    @staticmethod
    def add_message_writer_results(data):
        """
        Add message generation results to Results.md

        Args:
            data: List of repository data with messages
        """
        with open(ResultsTracker.RESULTS_FILE, 'a', encoding='utf-8') as f:
            MessageTracker.add_results(f, data)

    @staticmethod
    def add_email_drafter_results(results):
        """
        Add email drafting results to Results.md

        Args:
            results: Dictionary with draft creation results
        """
        with open(ResultsTracker.RESULTS_FILE, 'a', encoding='utf-8') as f:
            EmailTracker.add_results(f, results)

    @staticmethod
    def finalize_results():
        """Add footer to Results.md"""
        with open(ResultsTracker.RESULTS_FILE, 'a', encoding='utf-8') as f:
            f.write("## Summary\n\n")
            f.write(f"Pipeline execution completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("All results have been saved to their respective output files.\n")

    @staticmethod
    def display_results():
        """Display the contents of Results.md to console"""
        if os.path.exists(ResultsTracker.RESULTS_FILE):
            print("\n" + "="*70)
            print("RESULTS.MD CONTENTS")
            print("="*70 + "\n")

            with open(ResultsTracker.RESULTS_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
                print(content)

            print("\n" + "="*70)
            print(f"Full results saved to: {os.path.abspath(ResultsTracker.RESULTS_FILE)}")
            print("="*70 + "\n")
        else:
            print("Results.md file not found.")
