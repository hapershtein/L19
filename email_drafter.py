#!/usr/bin/env python3
"""
Email Drafter Agent
Creates Gmail draft messages for feedback from analyzed repositories
"""
import sys
import argparse
from email_drafter_pkg import EmailDrafter
from logger_config import LoggerConfig

logger = LoggerConfig.setup_logger('email_drafter')


def main():
    session_id = LoggerConfig.get_session_id()
    logger.info("=" * 70)
    logger.info(f"Email Drafter session started - Session ID: {session_id}")
    logger.info("=" * 70)

    parser = argparse.ArgumentParser(
        description='Create Gmail draft messages from feedback messages',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create drafts from default file
  python email_drafter.py

  # Use custom input file
  python email_drafter.py --input feedback_repos.xlsx

  # Use custom credentials
  python email_drafter.py --credentials my_credentials.json
        """
    )

    parser.add_argument(
        '--input',
        default='Output_34.xlsx',
        help='Input Excel file with feedback messages (default: Output_34.xlsx)'
    )

    parser.add_argument(
        '--credentials',
        default='credentials.json',
        help='Path to OAuth 2.0 credentials file (default: credentials.json)'
    )

    args = parser.parse_args()

    drafter = EmailDrafter(
        input_file=args.input,
        credentials_file=args.credentials
    )

    try:
        drafter.run()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
