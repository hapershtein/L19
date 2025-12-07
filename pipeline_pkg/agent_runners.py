"""
Agent runner functions for pipeline
"""
import os
import asyncio
from repo_analyzer import RepoAnalyzer
from message_writer_pkg import MessageWriter
from email_drafter_pkg import EmailDrafter


class AgentRunners:
    """Run different agents in the pipeline"""

    @staticmethod
    async def analyze_repositories(analyze_config):
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

    @staticmethod
    def generate_messages(message_config):
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

    @staticmethod
    def draft_emails(draft_config):
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
