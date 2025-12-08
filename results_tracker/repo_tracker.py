"""
Repository analysis results tracking
"""
from .visualizations import Visualizations
from .chart_generator import ChartGenerator
from .chart_generator2 import ChartGenerator2
from .chart_generator3 import ChartGenerator3


class RepoTracker:
    """Track repository analyzer agent results"""

    @staticmethod
    def add_results(f, repos_data):
        """
        Add repository analysis results to file

        Args:
            f: File handle
            repos_data: List of repository analysis dictionaries
        """
        f.write("## Repository Analyzer Agent\n\n")
        f.write("### Code Analysis Statistics\n\n")

        if not repos_data:
            f.write("*No repositories analyzed*\n\n")
            return

        analyzed = [r for r in repos_data if r['status'] == 'analyzed']
        failed = [r for r in repos_data if r['status'] == 'clone_failed']
        no_url = [r for r in repos_data if r['status'] == 'no_url']

        f.write(f"- **Total Repositories:** {len(repos_data)}\n")
        f.write(f"- **Successfully Analyzed:** {len(analyzed)}\n")
        f.write(f"- **Clone Failed:** {len(failed)}\n")
        f.write(f"- **No URL:** {len(no_url)}\n\n")

        if analyzed:
            avg_lines = sum(r['total_lines'] for r in analyzed) / len(analyzed)
            avg_grade = sum(r['grade'] for r in analyzed) / len(analyzed)
            f.write(f"- **Average Lines per Repo:** {int(avg_lines):,}\n")
            f.write(f"- **Average Grade:** {avg_grade:.2f}%\n\n")

            f.write("### Grade Distribution\n\n")

            # Create grade distribution histogram
            chart_path = ChartGenerator3.create_grade_distribution(
                analyzed,
                "Repository Grade Distribution",
                "repo_grade_distribution.png"
            )
            f.write(f"![Grade Distribution]({chart_path})\n\n")

            # Create pie chart for grade categories
            grade_ranges = [
                ("90-100% (Excellent)", 90, 100),
                ("70-89%  (Good)", 70, 89),
                ("50-69%  (Fair)", 50, 69),
                ("0-49%   (Poor)", 0, 49)
            ]

            labels = []
            counts = []
            for label, min_g, max_g in grade_ranges:
                count = sum(1 for r in analyzed if min_g <= r['grade'] <= max_g)
                if count > 0:
                    labels.append(label)
                    counts.append(count)

            if labels:
                pie_path = ChartGenerator2.create_pie_chart(
                    labels, counts,
                    "Grade Category Distribution",
                    "repo_grade_pie.png"
                )
                f.write(f"![Grade Categories]({pie_path})\n\n")

            # Text version
            f.write("<details>\n<summary>Text Version</summary>\n\n```\n")
            max_count = max(counts) if counts else 0
            for label, count in zip(labels, counts):
                f.write(Visualizations.create_bar_chart(label, count, max_count) + "\n")
            f.write("```\n</details>\n\n")

            f.write("### Top 5 Repositories by Grade\n\n")
            top_repos = sorted(analyzed, key=lambda x: x['grade'], reverse=True)[:5]

            # Create chart for top repos
            if top_repos:
                top_chart_path = ChartGenerator3.create_top_repos_chart(
                    top_repos,
                    "Top 5 Repositories by Grade",
                    "repo_top5.png"
                )
                f.write(f"![Top 5 Repositories]({top_chart_path})\n\n")

            f.write("| Rank | Repository ID | Grade | Total Lines | Small Files Lines |\n")
            f.write("|------|---------------|-------|-------------|-------------------|\n")

            for idx, repo in enumerate(top_repos, 1):
                medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
                f.write(f"| {medal} | {repo['id']} | {repo['grade']:.2f}% | {repo['total_lines']:,} | {repo['small_files_lines']:,} |\n")

            f.write("\n")

        f.write("---\n\n")
