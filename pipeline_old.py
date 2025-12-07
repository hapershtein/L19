#!/usr/bin/env python3
"""
Gmail Agent Pipeline - Execute multiple searches from JSON configuration
"""
import json
import os
import sys
import argparse
import asyncio
from datetime import datetime
from gmail_agent import GmailAgent

from logger_config import LoggerConfig

# Setup logger
logger = LoggerConfig.setup_logger('pipeline')

from analyze_repos import RepoAnalyzer
from message_writer import MessageWriter
from email_drafter import EmailDrafter


class GmailPipeline:
    """Pipeline to execute multiple Gmail searches from configuration"""

    def __init__(self, config_file):
        """
        Initialize the pipeline

        Args:
            config_file: Path to JSON configuration file
        """
        self.config_file = config_file
        self.config = None
        self.agent = None
        self.results = []

    def load_config(self):
        logger.info(f"Loading configuration from {self.config_file}")
        """Load and validate JSON configuration"""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Configuration file '{self.config_file}' not found.")

        with open(self.config_file, 'r') as f:
            self.config = json.load(f)

        # Validate configuration structure
        if 'searches' not in self.config:
            raise ValueError("Configuration must contain 'searches' array")

        if not isinstance(self.config['searches'], list):
            raise ValueError("'searches' must be an array")

        if len(self.config['searches']) == 0:
            raise ValueError("'searches' array cannot be empty")

        # Validate each search configuration
        for i, search in enumerate(self.config['searches']):
            if 'query' not in search:
                raise ValueError(f"Search #{i+1} is missing required 'query' field")

        print(f"Loaded configuration with {len(self.config['searches'])} search(es)")
        return self.config

    def validate_search(self, search, index):
        """
        Validate a single search configuration

        Args:
            search: Search configuration dictionary
            index: Index of the search in the config

        Returns:
            Dictionary with validated and default values
        """
        # Set defaults
        validated = {
            'name': search.get('name', f'Search {index + 1}'),
            'query': search['query'],
            'output': search.get('output', f'search_{index + 1}.xlsx'),
            'max_results': search.get('max_results', 100)
        }

        # Validate max_results
        if not isinstance(validated['max_results'], int) or validated['max_results'] < 1:
            print(f"Warning: Invalid max_results for '{validated['name']}', using default 100")
            validated['max_results'] = 100

        return validated

    def run(self, skip_on_error=False):
        session_id = LoggerConfig.get_session_id()
        logger.info(f"{"="*70}")
        logger.info(f"Pipeline execution started - Session ID: {session_id}")
        logger.info(f"{"="*70}")
        """
        Execute all searches in the pipeline

        Args:
            skip_on_error: If True, continue to next search on error. If False, stop on first error.

        Returns:
            List of result dictionaries
        """
        # Load configuration
        self.load_config()

        # Get credentials file
        credentials_file = self.config.get('credentials_file', 'credentials.json')

        # Initialize agent
        print(f"\nInitializing Gmail Agent...")
        self.agent = GmailAgent(credentials_file=credentials_file)
        self.agent.authenticate()

        # Execute each search
        print(f"\n{'='*70}")
        print(f"Starting pipeline execution")
        print(f"{'='*70}\n")

        total_searches = len(self.config['searches'])
        successful = 0
        failed = 0

        for i, search_config in enumerate(self.config['searches'], 1):
            try:
                # Validate search configuration
                search = self.validate_search(search_config, i - 1)

                print(f"\n[{i}/{total_searches}] {search['name']}")
                print(f"{'─'*70}")
                print(f"Query: {search['query']}")
                print(f"Output: {search['output']}")
                print(f"Max Results: {search['max_results']}")

                # Execute search
                start_time = datetime.now()
                emails = self.agent.search_emails(
                    query=search['query'],
                    max_results=search['max_results']
                )

                # Export to Excel
                if emails:
                    self.agent.export_to_excel(emails, output_file=search['output'])
                    end_time = datetime.now()
                    duration = (end_time - start_time).total_seconds()

                    result = {
                        'name': search['name'],
                        'query': search['query'],
                        'output': search['output'],
                        'count': len(emails),
                        'duration': duration,
                        'status': 'success'
                    }

                    print(f"✓ Success: {len(emails)} emails exported to {search['output']}")
                    print(f"  Duration: {duration:.2f}s")
                    successful += 1
                else:
                    result = {
                        'name': search['name'],
                        'query': search['query'],
                        'output': search['output'],
                        'count': 0,
                        'duration': 0,
                        'status': 'no_results'
                    }
                    print(f"ℹ No emails found")
                    successful += 1

                self.results.append(result)

            except Exception as e:
                result = {
                    'name': search.get('name', f'Search {i}'),
                    'query': search.get('query', 'N/A'),
                    'output': search.get('output', 'N/A'),
                    'count': 0,
                    'duration': 0,
                    'status': 'error',
                    'error': str(e)
                }
                self.results.append(result)

                print(f"✗ Error: {e}")
                failed += 1

                if not skip_on_error:
                    print(f"\nStopping pipeline due to error.")
                    break
                else:
                    print(f"Continuing to next search...")

        # Print summary
        print(f"\n{'='*70}")
        print(f"Pipeline Execution Summary")
        print(f"{'='*70}")
        print(f"Total Searches: {total_searches}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")

        # Print detailed results
        print(f"\nDetailed Results:")
        for result in self.results:
            status_symbol = '✓' if result['status'] == 'success' else 'ℹ' if result['status'] == 'no_results' else '✗'
            print(f"  {status_symbol} {result['name']}: {result['count']} emails")
            if result['status'] == 'error':
                print(f"    Error: {result['error']}")

        total_emails = sum(r['count'] for r in self.results)
        print(f"\nTotal Emails Retrieved: {total_emails}")

        return self.results

    def generate_report(self, output_file='pipeline_report.json'):
        """
        Generate a JSON report of pipeline execution

        Args:
            output_file: Path to output JSON report file
        """
        if not self.results:
            print("No results to report. Run the pipeline first.")
            return

        report = {
            'timestamp': datetime.now().isoformat(),
            'config_file': self.config_file,
            'total_searches': len(self.results),
            'successful': sum(1 for r in self.results if r['status'] == 'success'),
            'failed': sum(1 for r in self.results if r['status'] == 'error'),
            'no_results': sum(1 for r in self.results if r['status'] == 'no_results'),
            'total_emails': sum(r['count'] for r in self.results),
            'searches': self.results
        }

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\nReport saved to {output_file}")

    async def analyze_repositories(self, analyze_config):
        """
        Run repository analysis on output files

        Args:
            analyze_config: Configuration for repository analysis

        Returns:
            Analysis results
        """
        print(f"\n{'='*70}")
        print(f"Starting Repository Analysis")
        print(f"{'='*70}\n")

        input_file = analyze_config.get('input_file')
        output_file = analyze_config.get('output_file', 'Output_23.xlsx')
        temp_dir = analyze_config.get('temp_dir', 'TempFiles')
        cleanup = analyze_config.get('cleanup', True)
        small_file_threshold = analyze_config.get('small_file_threshold', 150)

        if not input_file:
            print("Error: 'input_file' not specified in analyze_repos configuration")
            return None

        if not os.path.exists(input_file):
            print(f"Warning: Input file '{input_file}' not found. Skipping repository analysis.")
            return None

        try:
            analyzer = RepoAnalyzer(
                input_file=input_file,
                output_file=output_file,
                temp_dir=temp_dir,
                small_file_threshold=small_file_threshold
            )

            results = await analyzer.run(cleanup=cleanup)
            return results

        except Exception as e:
            print(f"Error during repository analysis: {e}")
            import traceback
            traceback.print_exc()
            return None

    def generate_messages(self, message_config):
        """
        Run message generation on analyzed repositories

        Args:
            message_config: Configuration for message generation

        Returns:
            Message generation results
        """
        print(f"\n{'='*70}")
        print(f"Starting Message Generation")
        print(f"{'='*70}\n")

        input_file = message_config.get('input_file')
        output_file = message_config.get('output_file', 'Output_34.xlsx')

        if not input_file:
            print("Error: 'input_file' not specified in generate_messages configuration")
            return None

        if not os.path.exists(input_file):
            print(f"Warning: Input file '{input_file}' not found. Skipping message generation.")
            return None

        try:
            writer = MessageWriter(
                input_file=input_file,
                output_file=output_file
            )

            results = writer.run()
            return results

        except Exception as e:
            print(f"Error during message generation: {e}")
            import traceback
            traceback.print_exc()
            return None

    def draft_emails(self, draft_config):
        """
        Create Gmail draft messages from feedback

        Args:
            draft_config: Configuration for email drafting

        Returns:
            Draft creation results
        """
        print(f"\n{'='*70}")
        print(f"Starting Email Draft Creation")
        print(f"{'='*70}\n")

        input_file = draft_config.get('input_file')
        credentials_file = draft_config.get('credentials_file', 'credentials.json')

        if not input_file:
            print("Error: 'input_file' not specified in draft_emails configuration")
            return None

        if not os.path.exists(input_file):
            print(f"Warning: Input file '{input_file}' not found. Skipping email drafting.")
            return None

        try:
            drafter = EmailDrafter(
                input_file=input_file,
                credentials_file=credentials_file
            )

            results = drafter.run()
            return results

        except Exception as e:
            print(f"Error during email drafting: {e}")
            import traceback
            traceback.print_exc()
            return None


async def async_main(args):
    """Async main function to support repository analysis"""
    try:
        # Create and run pipeline
        pipeline = GmailPipeline(config_file=args.config)
        pipeline.run(skip_on_error=args.skip_on_error)

        # Generate report if requested
        if args.report:
            pipeline.generate_report(output_file=args.report)

        # Run repository analysis if configured
        if pipeline.config and 'analyze_repos' in pipeline.config:
            await pipeline.analyze_repositories(pipeline.config['analyze_repos'])

        # Run message generation if configured
        if pipeline.config and 'generate_messages' in pipeline.config:
            pipeline.generate_messages(pipeline.config['generate_messages'])

        # Create email drafts if configured
        if pipeline.config and 'draft_emails' in pipeline.config:
            pipeline.draft_emails(pipeline.config['draft_emails'])

        # Exit with appropriate code
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

    # Run async main to support repository analysis
    asyncio.run(async_main(args))


if __name__ == '__main__':
    main()
