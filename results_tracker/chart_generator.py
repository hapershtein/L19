"""
Chart generation using matplotlib and seaborn
"""
import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set seaborn style
sns.set_theme(style="whitegrid")
sns.set_palette("husl")


class ChartGenerator:
    """Generate visual charts for results tracking"""

    CHARTS_DIR = "Results_Charts"

    @classmethod
    def ensure_charts_dir(cls):
        """Create charts directory if it doesn't exist"""
        if not os.path.exists(cls.CHARTS_DIR):
            os.makedirs(cls.CHARTS_DIR)

    @classmethod
    def create_horizontal_bar_chart(cls, labels, values, title, filename, max_value=None):
        """
        Create a horizontal bar chart

        Args:
            labels: List of labels for bars
            values: List of values for bars
            title: Chart title
            filename: Output filename (without path)
            max_value: Optional maximum value for x-axis

        Returns:
            Path to saved chart
        """
        cls.ensure_charts_dir()

        fig, ax = plt.subplots(figsize=(10, max(6, len(labels) * 0.5)))

        colors = sns.color_palette("husl", len(labels))
        bars = ax.barh(labels, values, color=colors)

        # Add value labels on bars
        for i, (bar, value) in enumerate(zip(bars, values)):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2,
                   f' {value}', ha='left', va='center', fontsize=10, fontweight='bold')

        ax.set_xlabel('Count', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)

        if max_value:
            ax.set_xlim(0, max_value * 1.1)

        plt.tight_layout()

        filepath = os.path.join(cls.CHARTS_DIR, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()

        return filepath
