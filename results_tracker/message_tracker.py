"""
Message writer results tracking
"""
from .visualizations import Visualizations
from .chart_generator import ChartGenerator
from .chart_generator2 import ChartGenerator2


class MessageTracker:
    """Track message writer agent results"""

    @staticmethod
    def add_results(f, data):
        """
        Add message generation results to file

        Args:
            f: File handle
            data: List of repository data with messages
        """
        f.write("## Message Writer Agent\n\n")
        f.write("### Feedback Message Generation\n\n")

        if not data:
            f.write("*No messages generated*\n\n")
            return

        trump_count = sum(1 for r in data if r['grade'] >= 90)
        netanyahu_count = sum(1 for r in data if 70 <= r['grade'] < 90)
        hason_count = sum(1 for r in data if 50 <= r['grade'] < 70)
        amsalem_count = sum(1 for r in data if r['grade'] < 50)

        f.write(f"- **Total Messages Generated:** {len(data)}\n\n")

        f.write("### Message Styles Distribution\n\n")

        # Create visual charts
        labels = ["Trump\n(Congratulations)", "Netanyahu\n(Positive)", "Hason\n(Improvement)", "Amsalem\n(Critical)"]
        counts = [trump_count, netanyahu_count, hason_count, amsalem_count]

        # Bar chart
        bar_path = ChartGenerator.create_horizontal_bar_chart(
            labels, counts,
            "Message Style Distribution",
            "message_styles_bar.png"
        )
        f.write(f"![Message Styles Distribution]({bar_path})\n\n")

        # Pie chart
        pie_labels = []
        pie_counts = []
        for label, count in zip(labels, counts):
            if count > 0:
                pie_labels.append(label.replace('\n', ' '))
                pie_counts.append(count)

        if pie_labels:
            pie_path = ChartGenerator2.create_pie_chart(
                pie_labels, pie_counts,
                "Message Style Proportion",
                "message_styles_pie.png"
            )
            f.write(f"![Message Style Proportion]({pie_path})\n\n")

        # Text version
        f.write("<details>\n<summary>Text Version</summary>\n\n```\n")
        styles = [
            ("Trump (Congratulations)", trump_count),
            ("Netanyahu (Positive)   ", netanyahu_count),
            ("Hason (Improvement)    ", hason_count),
            ("Amsalem (Critical)     ", amsalem_count)
        ]
        max_count = max(count for _, count in styles)
        for label, count in styles:
            f.write(Visualizations.create_bar_chart(label, count, max_count) + "\n")
        f.write("```\n</details>\n\n")

        f.write("### Message Statistics by Style\n\n")
        f.write("| Style | Grade Range | Count | Percentage |\n")
        f.write("|-------|-------------|-------|------------|\n")
        f.write(f"| Trump (Congratulations) | 90-100% | {trump_count} | {(trump_count/len(data)*100):.1f}% |\n")
        f.write(f"| Netanyahu (Positive) | 70-89% | {netanyahu_count} | {(netanyahu_count/len(data)*100):.1f}% |\n")
        f.write(f"| Hason (Improvement) | 50-69% | {hason_count} | {(hason_count/len(data)*100):.1f}% |\n")
        f.write(f"| Amsalem (Critical) | 0-49% | {amsalem_count} | {(amsalem_count/len(data)*100):.1f}% |\n")

        f.write("\n---\n\n")
