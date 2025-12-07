#!/usr/bin/env python3
"""
Gmail Agent Pipeline - Execute multiple searches from JSON configuration
"""
import sys
import asyncio
import argparse
from pipeline_pkg import GmailPipeline


async def async_main(args):
    """Async main function to support repository analysis"""
    try:
        pipeline = GmailPipeline(config_file=args.config)
        pipeline.run(skip_on_error=args.skip_on_error)

        if args.report:
            pipeline.generate_report(output_file=args.report)

        if pipeline.config and 'analyze_repos' in pipeline.config:
            await pipeline.analyze_repositories(pipeline.config['analyze_repos'])

        if pipeline.config and 'generate_messages' in pipeline.config:
            pipeline.generate_messages(pipeline.config['generate_messages'])

        if pipeline.config and 'draft_emails' in pipeline.config:
            pipeline.draft_emails(pipeline.config['draft_emails'])

        failed = sum(1 for r in pipeline.results if r['status'] == 'error')
        sys.exit(1 if failed > 0 else 0)

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n\nPipeline interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Main function to run the pipeline"""
    parser = argparse.ArgumentParser(
        description='Gmail Agent Pipeline - Execute multiple searches from JSON configuration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example config.json structure:
{
  "credentials_file": "credentials.json",
  "searches": [
    {
      "name": "Unread Emails",
      "query": "is:unread",
      "output": "unread_emails.xlsx",
      "max_results": 50
    },
    {
      "name": "Important Emails",
      "query": "is:important",
      "output": "important_emails.xlsx",
      "max_results": 100
    }
  ]
}

Usage:
  python pipeline.py --config config.json
  python pipeline.py --config config.json --skip-on-error
  python pipeline.py --config config.json --report results.json
        """
    )

    parser.add_argument(
        '--config',
        type=str,
        default='config.json',
        help='Path to JSON configuration file (default: config.json)'
    )

    parser.add_argument(
        '--skip-on-error',
        action='store_true',
        help='Continue to next search if an error occurs (default: stop on error)'
    )

    parser.add_argument(
        '--report',
        type=str,
        help='Generate a JSON report of the pipeline execution'
    )

    args = parser.parse_args()

    asyncio.run(async_main(args))


if __name__ == '__main__':
    main()
