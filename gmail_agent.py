#!/usr/bin/env python3
"""
Gmail Agent - Retrieve and export emails to Excel
"""
import argparse
from gmail_agent_pkg import GmailAgent
from logger_config import LoggerConfig

logger = LoggerConfig.setup_logger('gmail_agent')


def main():
    """Main function to run the Gmail agent"""
    parser = argparse.ArgumentParser(
        description='Gmail Agent - Retrieve and export emails to Excel',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search for emails from a specific sender
  python gmail_agent.py --query "from:example@gmail.com" --output results.xlsx

  # Search for emails with specific subject
  python gmail_agent.py --query "subject:invoice" --max 50

  # Search for unread emails
  python gmail_agent.py --query "is:unread"

  # Complex search
  python gmail_agent.py --query "from:boss@company.com after:2024/01/01 has:attachment"
        """
    )

    parser.add_argument(
        '--query',
        type=str,
        required=True,
        help='Gmail search query (e.g., "from:example@gmail.com subject:invoice")'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='gmail_export.xlsx',
        help='Output Excel file path (default: gmail_export.xlsx)'
    )

    parser.add_argument(
        '--max',
        type=int,
        default=100,
        help='Maximum number of emails to retrieve (default: 100)'
    )

    parser.add_argument(
        '--credentials',
        type=str,
        default='credentials.json',
        help='Path to OAuth 2.0 credentials file (default: credentials.json)'
    )

    args = parser.parse_args()

    try:
        session_id = LoggerConfig.get_session_id()
        logger.info(f"{'='*70}")
        logger.info(f"Gmail Agent session started - Session ID: {session_id}")
        logger.info(f"Parameters: query='{args.query}', max={args.max}, output='{args.output}'")
        logger.info(f"{'='*70}")

        agent = GmailAgent(credentials_file=args.credentials)
        agent.authenticate()

        emails = agent.search_emails(args.query, max_results=args.max)

        if emails:
            agent.export_to_excel(emails, output_file=args.output)
            logger.info(f"Session completed successfully - {len(emails)} emails exported")
            print(f"\n✓ Complete! {len(emails)} emails exported to {args.output}")
        else:
            logger.info("Session completed - No emails found")
            print("\nNo emails found matching the search criteria.")

    except FileNotFoundError as e:
        logger.error(f"FileNotFoundError: {e}")
        print(f"\nError: {e}")
        print("\nPlease follow the setup instructions in README.md")
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        LoggerConfig.log_exception(logger, e, "main function")
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
