"""
Additional chart types for results tracking
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


class ChartGenerator2:
    """Additional chart generation methods"""

    CHARTS_DIR = "Results_Charts"

    @classmethod
    def ensure_charts_dir(cls):
        """Create charts directory if it doesn't exist"""
        if not os.path.exists(cls.CHARTS_DIR):
            os.makedirs(cls.CHARTS_DIR)

    @classmethod
    def create_pie_chart(cls, labels, values, title, filename):
        """
        Create a pie chart

        Args:
            labels: List of labels
            values: List of values
            title: Chart title
            filename: Output filename

        Returns:
            Path to saved chart
        """
        cls.ensure_charts_dir()

        fig, ax = plt.subplots(figsize=(10, 8))

        colors = sns.color_palette("husl", len(labels))
        wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%',
                                           colors=colors, startangle=90,
                                           textprops={'fontsize': 11, 'fontweight': 'bold'})

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(12)

        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)

        plt.tight_layout()

        filepath = os.path.join(cls.CHARTS_DIR, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()

        return filepath

    @classmethod
    def create_stacked_bar_chart(cls, categories, success, failed, title, filename):
        """
        Create a stacked bar chart for success/failure

        Args:
            categories: List of category names
            success: List of success counts
            failed: List of failure counts
            title: Chart title
            filename: Output filename

        Returns:
            Path to saved chart
        """
        cls.ensure_charts_dir()

        fig, ax = plt.subplots(figsize=(10, 6))

        x = np.arange(len(categories))
        width = 0.6

        bars1 = ax.bar(x, success, width, label='Success', color='#2ecc71')
        bars2 = ax.bar(x, failed, width, bottom=success, label='Failed', color='#e74c3c')

        ax.set_ylabel('Count', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha='right')
        ax.legend()

        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2., bar.get_y() + height/2.,
                           f'{int(height)}', ha='center', va='center',
                           fontweight='bold', color='white', fontsize=10)

        plt.tight_layout()

        filepath = os.path.join(cls.CHARTS_DIR, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()

        return filepath
