"""
Visualization utilities for results tracking
"""


class Visualizations:
    """Create text-based visualizations"""

    @staticmethod
    def create_bar_chart(label, value, max_value, bar_width=50):
        """
        Create a text-based bar chart

        Args:
            label: Label for the bar
            value: Current value
            max_value: Maximum value for scaling
            bar_width: Width of the bar in characters

        Returns:
            String representation of the bar
        """
        if max_value == 0:
            filled = 0
        else:
            filled = int((value / max_value) * bar_width)

        empty = bar_width - filled
        bar = '█' * filled + '░' * empty
        return f"{label:<25} |{bar}| {value}"
