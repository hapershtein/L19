#!/usr/bin/env python3
"""
Message Writer Agent - Generate personalized feedback messages based on code analysis grades
"""
import argparse
from message_writer_pkg import MessageWriter
from logger_config import LoggerConfig

logger = LoggerConfig.setup_logger('message_writer')


def main():
    """Main function to run the message writer"""
    session_id = LoggerConfig.get_session_id()
    logger.info(f"{'='*70}")
    logger.info(f"Message Writer session started - Session ID: {session_id}")
    logger.info(f"{'='*70}")

    parser = argparse.ArgumentParser(
        description='Message Writer Agent - Generate personalized feedback based on code grades',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  # Generate messages from Output_23.xlsx
  python message_writer.py --input Output_23.xlsx

  # Specify custom output file
  python message_writer.py --input Output_23.xlsx --output custom_messages.xlsx

Message Styles by Grade:
  90-100%:  Donald Trump style (Congratulations!)
  70-89%:   Benjamin Netanyahu style (Positive feedback)
  50-69%:   Shahar Hason style (Needs improvement, humorous)
  0-49%:    Dudi Amsalem style (Brutally honest, direct)
        """
    )

    parser.add_argument(
        '--input',
        type=str,
        default='Output_23.xlsx',
        help='Input Excel file with grades (default: Output_23.xlsx)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='Output_34.xlsx',
        help='Output Excel file with messages (default: Output_34.xlsx)'
    )

    args = parser.parse_args()

    writer = MessageWriter(
        input_file=args.input,
        output_file=args.output
    )

    writer.run()


if __name__ == '__main__':
    main()
