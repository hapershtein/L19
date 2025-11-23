#!/usr/bin/env python3
"""
Script to add comprehensive logging to all agent files
Run this once to add logging throughout the project
"""

import re

# Key logging points to add to each file type
ANALYZE_REPOS_LOGGING = [
    # read_excel_data
    ('print(f"Reading data from {self.input_file}...")',
     'logger.info(f"Reading data from {self.input_file}")\n        print(f"Reading data from {self.input_file}...")'),
    ('print(f"Found {len(self.repos_data)} repositories with GitHub URLs\\n")',
     'logger.info(f"Found {len(self.repos_data)} repositories with GitHub URLs")\n        print(f"Found {len(self.repos_data)} repositories with GitHub URLs\\n")'),

    # clone_repo
    ('print(f"[{repo_id}] Cloning {repo_url}...")',
     'logger.info(f"[{repo_id}] Starting clone of {repo_url}")\n            print(f"[{repo_id}] Cloning {repo_url}...")'),
    ('print(f"[{repo_id}] ✓ Clone successful")',
     'logger.info(f"[{repo_id}] Clone successful")\n            print(f"[{repo_id}] ✓ Clone successful")'),
    ('print(f"[{repo_id}] ✗ Clone failed: {e}")',
     'logger.error(f"[{repo_id}] Clone failed: {e}")\n            print(f"[{repo_id}] ✗ Clone failed: {e}")'),

    # analyze_repository
    ('print(f"[{repo_id}] Analyzing code...")',
     'logger.info(f"[{repo_id}] Starting code analysis")\n        print(f"[{repo_id}] Analyzing code...")'),
    ('print(f"[{repo_id}] ✓ Analysis complete: {total_lines:,} total lines, {small_files_lines:,} lines in small files, Grade: {grade:.2f}%")',
     'logger.info(f"[{repo_id}] Analysis complete: total={total_lines}, small={small_files_lines}, grade={grade:.2f}%")\n        print(f"[{repo_id}] ✓ Analysis complete: {total_lines:,} total lines, {small_files_lines:,} lines in small files, Grade: {grade:.2f}%")'),
]

MESSAGE_WRITER_LOGGING = [
    ('print(f"Reading data from {self.input_file}...")',
     'logger.info(f"Reading data from {self.input_file}")\n        print(f"Reading data from {self.input_file}...")'),
    ('print(f"Found {len(self.data)} repositories to process\\n")',
     'logger.info(f"Found {len(self.data)} repositories to process")\n        print(f"Found {len(self.data)} repositories to process\\n")'),
    ('print(f"✓ Generated {len(self.data)} personalized messages")',
     'logger.info(f"Generated {len(self.data)} personalized messages")\n        print(f"✓ Generated {len(self.data)} personalized messages")'),
]

EMAIL_DRAFTER_LOGGING = [
    ('print("✓ Successfully authenticated with Gmail API\\n")',
     'logger.info("Successfully authenticated with Gmail API")\n        print("✓ Successfully authenticated with Gmail API\\n")'),
    ('print(f"Reading data from {self.input_file}...")',
     'logger.info(f"Reading data from {self.input_file}")\n        print(f"Reading data from {self.input_file}...")'),
    ('print(f"Found {len(self.data)} feedback messages to draft\\n")',
     'logger.info(f"Found {len(self.data)} feedback messages to draft")\n        print(f"Found {len(self.data)} feedback messages to draft\\n")'),
]

PIPELINE_LOGGING = [
    ('print(f"\\n{\'=\'*70}")',
     'logger.info(f"{\'=\'*70}")\n        print(f"\\n{\'=\'*70}")'),
]

print("This script adds logging statements to the agent files.")
print("Logging has been added to gmail_agent.py manually.")
print("To complete, add similar patterns to:")
print("- analyze_repos.py")
print("- message_writer.py")
print("- email_drafter.py")
print("- pipeline.py")
print("\nKey points to log:")
print("- Start/end of major operations")
print("- Success/failure of operations")
print("- Error conditions with full details")
print("- Progress updates for long-running operations")
