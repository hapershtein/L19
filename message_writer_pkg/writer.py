"""
Message Writer main class
"""
import sys
from logger_config import LoggerConfig
from .excel_handler import ExcelHandler
from .message_generators import MessageGenerators

logger = LoggerConfig.setup_logger('message_writer')


class MessageWriter:
    """Agent to generate personalized feedback messages based on grades"""

    def __init__(self, input_file='Output_23.xlsx', output_file='Output_34.xlsx'):
        """
        Initialize the Message Writer

        Args:
            input_file: Path to input Excel file with grades
            output_file: Path to output Excel file with messages
        """
        self.input_file = input_file
        self.output_file = output_file
        self.data = []

    def read_excel_data(self):
        """Read data from input Excel file"""
        self.data = ExcelHandler.read_input_file(self.input_file)
        return self.data

    def process_all(self):
        """
        Process all repositories and generate messages

        Returns:
            List of processed data with messages
        """
        self.data = self.read_excel_data()

        print(f"\n{'='*70}")
        print(f"Generating Personalized Messages")
        print(f"{'='*70}\n")

        for i, repo in enumerate(self.data, 1):
            grade = repo['grade']
            message = MessageGenerators.generate_message(repo)
            repo['message'] = message

            if grade >= 90:
                style = "Trump (Congratulations)"
            elif grade >= 70:
                style = "Netanyahu (Positive)"
            elif grade >= 50:
                style = "Hason (Improvement)"
            else:
                style = "Amsalem (Brutally Honest)"

            print(f"[{i}/{len(self.data)}] {repo['id']} - Grade: {grade:.2f}% - Style: {style}")

        print(f"\n✓ Generated {len(self.data)} personalized messages")
        return self.data

    def export_to_excel(self):
        """Export data with messages to Excel file"""
        if not self.data:
            print("No data to export. Run process_all() first.")
            return

        ExcelHandler.export_results(self.data, self.output_file)

    def run(self):
        """
        Run the complete message writing pipeline

        Returns:
            List of processed data with messages
        """
        try:
            self.process_all()
            self.export_to_excel()
            self.print_summary()

            return self.data

        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    def print_summary(self):
        """Print summary of message generation"""
        print(f"\n{'='*70}")
        print(f"Message Generation Summary")
        print(f"{'='*70}")

        trump_count = sum(1 for r in self.data if r['grade'] >= 90)
        netanyahu_count = sum(1 for r in self.data if 70 <= r['grade'] < 90)
        hason_count = sum(1 for r in self.data if 50 <= r['grade'] < 70)
        amsalem_count = sum(1 for r in self.data if r['grade'] < 50)

        print(f"Total Repositories: {len(self.data)}")
        print(f"\nMessages by Style:")
        print(f"  Trump (90-100%):     {trump_count} - Congratulations")
        print(f"  Netanyahu (70-89%):  {netanyahu_count} - Positive Feedback")
        print(f"  Hason (50-69%):      {hason_count} - Needs Improvement")
        print(f"  Amsalem (<50%):      {amsalem_count} - Brutally Honest")
