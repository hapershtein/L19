"""
Gmail search results tracking
"""
from .visualizations import Visualizations
from .chart_generator import ChartGenerator


class GmailTracker:
    """Track Gmail search agent results"""

    @staticmethod
    def add_results(f, search_data):
        """
        Add Gmail search results to file

        Args:
            f: File handle
            search_data: List of search result dictionaries
        """
        f.write("## Gmail Search Agent\n\n")
        f.write("### Email Retrieval Statistics\n\n")

        if not search_data:
            f.write("*No searches performed*\n\n")
            return

        total_emails = sum(s['count'] for s in search_data)
        successful = sum(1 for s in search_data if s['status'] == 'success')
        failed = sum(1 for s in search_data if s['status'] == 'error')

        f.write(f"- **Total Searches:** {len(search_data)}\n")
        f.write(f"- **Successful:** {successful}\n")
        f.write(f"- **Failed:** {failed}\n")
        f.write(f"- **Total Emails Retrieved:** {total_emails}\n\n")

        f.write("### Emails Retrieved per Search\n\n")

        # Create visual chart
        labels = [f"{s['name'][:30]}" for s in search_data]
        values = [s['count'] for s in search_data]
        chart_path = ChartGenerator.create_horizontal_bar_chart(
            labels, values,
            "Emails Retrieved per Search",
            "gmail_search_results.png"
        )
        f.write(f"![Emails Retrieved per Search]({chart_path})\n\n")

        # Also include text version
        f.write("<details>\n<summary>Text Version</summary>\n\n```\n")
        max_count = max((s['count'] for s in search_data), default=0)

        for search in search_data:
            status_icon = "✓" if search['status'] == 'success' else "✗"
            label = f"{status_icon} {search['name'][:20]}"
            f.write(Visualizations.create_bar_chart(label, search['count'], max_count) + "\n")

        f.write("```\n</details>\n\n")

        f.write("### Search Details\n\n")
        f.write("| Search Name | Query | Status | Count | Output File |\n")
        f.write("|-------------|-------|--------|-------|-------------|\n")

        for search in search_data:
            status_icon = "✅" if search['status'] == 'success' else "❌"
            query_short = search['query'][:30] + "..." if len(search['query']) > 30 else search['query']
            f.write(f"| {search['name']} | `{query_short}` | {status_icon} | {search['count']} | {search['output']} |\n")

        f.write("\n---\n\n")
