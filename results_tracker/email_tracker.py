"""
Email drafter results tracking
"""
from .visualizations import Visualizations
from .chart_generator2 import ChartGenerator2


class EmailTracker:
    """Track email drafter agent results"""

    @staticmethod
    def add_results(f, results):
        """
        Add email drafting results to file

        Args:
            f: File handle
            results: Dictionary with draft creation results
        """
        f.write("## Email Drafter Agent\n\n")
        f.write("### Gmail Draft Creation\n\n")

        if not results:
            f.write("*No drafts created*\n\n")
            return

        total = results.get('total', 0)
        success = results.get('success', 0)
        failed = results.get('failed', 0)

        f.write(f"- **Total Drafts Attempted:** {total}\n")
        f.write(f"- **Successfully Created:** {success}\n")
        f.write(f"- **Failed:** {failed}\n")

        if total > 0:
            success_rate = (success / total) * 100
            f.write(f"- **Success Rate:** {success_rate:.1f}%\n\n")

            f.write("### Draft Creation Results\n\n")

            # Create stacked bar chart
            chart_path = ChartGenerator2.create_stacked_bar_chart(
                ["Draft Creation"],
                [success],
                [failed],
                "Email Draft Creation Results",
                "email_drafts.png"
            )
            f.write(f"![Draft Creation Results]({chart_path})\n\n")

            # Text version
            f.write("<details>\n<summary>Text Version</summary>\n\n```\n")
            f.write(Visualizations.create_bar_chart("✓ Successful", success, total) + "\n")
            f.write(Visualizations.create_bar_chart("✗ Failed    ", failed, total) + "\n")
            f.write("```\n</details>\n\n")

        f.write("---\n\n")
