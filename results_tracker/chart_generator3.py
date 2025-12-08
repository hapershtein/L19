"""
Advanced chart types for results tracking
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


class ChartGenerator3:
    """Advanced chart generation methods"""

    CHARTS_DIR = "Results_Charts"

    @classmethod
    def ensure_charts_dir(cls):
        """Create charts directory if it doesn't exist"""
        if not os.path.exists(cls.CHARTS_DIR):
            os.makedirs(cls.CHARTS_DIR)

    @classmethod
    def create_grade_distribution(cls, analyzed_repos, title, filename):
        """
        Create a histogram for grade distribution

        Args:
            analyzed_repos: List of analyzed repository dictionaries
            title: Chart title
            filename: Output filename

        Returns:
            Path to saved chart
        """
        cls.ensure_charts_dir()

        grades = [repo['grade'] for repo in analyzed_repos]

        fig, ax = plt.subplots(figsize=(12, 6))

        # Create histogram with KDE
        sns.histplot(grades, bins=20, kde=True, color='#3498db', ax=ax, stat='count')

        # Add vertical lines for grade boundaries
        ax.axvline(90, color='#2ecc71', linestyle='--', linewidth=2, label='Excellent (90%)')
        ax.axvline(70, color='#f39c12', linestyle='--', linewidth=2, label='Good (70%)')
        ax.axvline(50, color='#e74c3c', linestyle='--', linewidth=2, label='Fair (50%)')

        ax.set_xlabel('Grade (%)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Repositories', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        filepath = os.path.join(cls.CHARTS_DIR, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()

        return filepath

    @classmethod
    def create_top_repos_chart(cls, top_repos, title, filename):
        """
        Create a horizontal bar chart for top repositories

        Args:
            top_repos: List of top repository dictionaries
            title: Chart title
            filename: Output filename

        Returns:
            Path to saved chart
        """
        cls.ensure_charts_dir()

        fig, ax = plt.subplots(figsize=(12, max(6, len(top_repos) * 0.7)))

        repo_ids = [repo['id'] for repo in top_repos]
        grades = [repo['grade'] for repo in top_repos]

        colors = sns.color_palette("RdYlGn", len(top_repos))[::-1]
        bars = ax.barh(repo_ids, grades, color=colors)

        # Add grade labels
        for bar, grade in zip(bars, grades):
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height()/2,
                   f'{grade:.2f}%', ha='left', va='center',
                   fontsize=11, fontweight='bold')

        ax.set_xlabel('Grade (%)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Repository ID', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlim(0, 105)
        ax.grid(True, alpha=0.3, axis='x')

        plt.tight_layout()

        filepath = os.path.join(cls.CHARTS_DIR, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()

        return filepath
