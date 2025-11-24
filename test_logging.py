#!/usr/bin/env python3
"""
Test script to verify logging is working correctly for all agents
"""

import os
import sys
from logger_config import LoggerConfig

def test_logging():
    """Test that logging infrastructure is working"""

    print("Testing Logging System")
    print("=" * 70)

    # Create Logs directory if it doesn't exist
    if not os.path.exists('Logs'):
        os.makedirs('Logs')
        print("✓ Created Logs/ directory")
    else:
        print("✓ Logs/ directory exists")

    # Test each agent's logger
    agents = ['gmail_agent', 'analyze_repos', 'message_writer', 'email_drafter', 'pipeline']

    for agent in agents:
        logger = LoggerConfig.setup_logger(agent)
        logger.info(f"Test log entry for {agent}")

        log_file = f'Logs/{agent}.log'
        if os.path.exists(log_file):
            print(f"✓ {agent}: Log file created successfully")

            # Check if test entry was written
            with open(log_file, 'r') as f:
                content = f.read()
                if 'Test log entry' in content:
                    print(f"  ✓ Log entry written successfully")
                else:
                    print(f"  ✗ Log entry not found in file")
        else:
            print(f"✗ {agent}: Log file NOT created")

    # Test pipeline logger
    print("\nTesting Pipeline Logger...")
    pipeline_logger = LoggerConfig.setup_pipeline_logger()
    pipeline_logger.info("Test pipeline log entry")

    if os.path.exists('Logs/pipeline_execution.log'):
        print("✓ Pipeline log file created successfully")
        with open('Logs/pipeline_execution.log', 'r') as f:
            content = f.read()
            if 'Test pipeline log entry' in content:
                print("  ✓ Pipeline log entry written successfully")
            else:
                print("  ✗ Pipeline log entry not found")
    else:
        print("✗ Pipeline log file NOT created")

    # List all log files
    print("\n" + "=" * 70)
    print("Log Files Created:")
    print("=" * 70)
    if os.path.exists('Logs'):
        log_files = [f for f in os.listdir('Logs') if f.endswith('.log')]
        for log_file in sorted(log_files):
            file_path = os.path.join('Logs', log_file)
            size = os.path.getsize(file_path)
            print(f"  {log_file}: {size} bytes")

        if not log_files:
            print("  No log files found")
    else:
        print("  Logs/ directory does not exist")

    print("\n" + "=" * 70)
    print("✓ Logging system test complete")
    print("=" * 70)
    print("\nTo view logs:")
    print("  tail -n 50 Logs/gmail_agent.log")
    print("  tail -f Logs/pipeline_execution.log")
    print("  grep 'ERROR' Logs/*.log")

if __name__ == '__main__':
    test_logging()
