# Logging System Documentation

The Gmail Agent System includes comprehensive logging throughout all agents to help with debugging, monitoring, and auditing.

## Overview

All agents use a centralized logging configuration that:
- Creates rotating log files (max 10MB per file, keeps 5 backups)
- Logs to both files and console
- Uses UTF-8 encoding for proper character support (Hebrew, emojis, etc.)
- Organizes logs in a dedicated `Logs/` folder
- Provides detailed timestamps and context for all operations

## Log Files Location

All log files are stored in the `Logs/` directory:

```
Logs/
├── gmail_agent.log          - Gmail email retrieval operations
├── gmail_agent.log.1        - Rotated backup (older logs)
├── gmail_agent.log.2        - Rotated backup
├── analyze_repos.log        - Repository cloning and analysis
├── message_writer.log       - Feedback message generation
├── email_drafter.log        - Gmail draft creation
└── pipeline_execution.log   - Complete pipeline runs (all agents)
```

## Log Rotation

Logs automatically rotate when they reach 10MB:
- Maximum size per log file: 10MB
- Number of backup files kept: 5
- Total maximum disk space per agent: ~50MB
- Old logs are automatically cleaned up

## Log Levels

The system uses standard Python logging levels:

### File Logs (All levels)
- **DEBUG**: Detailed information for diagnosing problems
  - API calls, parameter values, step-by-step operations
  - Example: `"Processing message 5/20, ID: 1234567"`

- **INFO**: General informational messages
  - Start/end of operations, progress updates, success messages
  - Example: `"Successfully retrieved 15 emails"`

- **WARNING**: Warning messages for non-critical issues
  - Fallback behaviors, recoverable errors
  - Example: `"Browser authentication failed, falling back to console"`

- **ERROR**: Error messages for serious problems
  - Failed operations, exceptions
  - Example: `"Clone failed for repository: https://github.com/user/repo"`

### Console Output (WARNING and above)
- Console only shows WARNING and ERROR messages
- Reduces noise while keeping critical information visible
- Full details always available in log files

## What Gets Logged

### Gmail Agent (`gmail_agent.log`)
- Authentication flow (token loading, refresh, new auth)
- Email search queries and results
- Message retrieval progress (every 10 messages)
- URL extraction results
- Excel export operations
- API errors and exceptions

### Analyze Repos (`analyze_repos.log`)
- Repository cloning operations (start, success, failure)
- Code analysis for each repository
- Line counting and file metrics
- Grade calculations
- Parallel operation coordination
- Excel import/export operations

### Message Writer (`message_writer.log`)
- Input file reading
- Message generation for each repository
- Style selection based on grades
- Excel export operations
- Summary statistics

### Email Drafter (`email_drafter.log`)
- Gmail API authentication
- Draft creation for each message
- Success/failure per draft
- API errors and rate limits

### Pipeline (`pipeline_execution.log`)
- Complete pipeline execution flow
- Each agent's execution
- Configuration loading
- Report generation
- Overall success/failure status

## Reading Log Files

### View Recent Logs

```bash
# View last 50 lines of gmail agent log
tail -n 50 Logs/gmail_agent.log

# View last 100 lines of pipeline log
tail -n 100 Logs/pipeline_execution.log

# Follow log file in real-time
tail -f Logs/pipeline_execution.log
```

### Search Logs

```bash
# Search for errors
grep "ERROR" Logs/gmail_agent.log

# Search for specific repository
grep "12345" Logs/analyze_repos.log

# Search for failed operations
grep -i "failed" Logs/*.log

# Count errors per log file
grep -c "ERROR" Logs/*.log
```

### View Logs by Date/Time

```bash
# View logs from specific date
grep "2025-01-23" Logs/pipeline_execution.log

# View logs from specific hour
grep "2025-01-23 14:" Logs/gmail_agent.log
```

## Log Format

### File Log Format

```
YYYY-MM-DD HH:MM:SS - module_name - LEVEL - function_name:line_number - message
```

Example:
```
2025-01-23 14:32:15 - gmail_agent - INFO - search_emails:166 - Starting email search with query: 'label:EmailTesting', max_results: 50
2025-01-23 14:32:16 - gmail_agent - INFO - search_emails:182 - API returned 15 message IDs
2025-01-23 14:32:18 - gmail_agent - INFO - search_emails:240 - Successfully retrieved all 15 emails
```

### Session Identification

Each execution starts with a session ID:
```
======================================================================
Gmail Agent session started - Session ID: 20250123_143215
Parameters: query='label:EmailTesting', max=50, output='Output_12.xlsx'
======================================================================
```

## Using Logs for Troubleshooting

### Common Scenarios

#### 1. Email Search Returns No Results

Check logs:
```bash
grep "No messages found" Logs/gmail_agent.log
grep "API returned" Logs/gmail_agent.log | tail -n 5
```

#### 2. Repository Clone Failures

Check logs:
```bash
grep "Clone failed" Logs/analyze_repos.log
grep "ERROR" Logs/analyze_repos.log | tail -n 10
```

#### 3. Authentication Issues

Check logs:
```bash
grep -i "auth" Logs/gmail_agent.log | tail -n 20
grep "token" Logs/email_drafter.log | tail -n 10
```

#### 4. Pipeline Failures

Check logs:
```bash
tail -n 100 Logs/pipeline_execution.log
grep "ERROR" Logs/pipeline_execution.log
```

### Exception Details

When exceptions occur, logs include:
- Exception type and message
- Full stack trace
- Context (which operation was being performed)
- Input parameters

Example:
```
2025-01-23 14:35:22 - analyze_repos - ERROR - clone_repo:85 - [12345] Clone failed: Repository not found
2025-01-23 14:35:22 - analyze_repos - ERROR - clone_repo:86 - Exception in clone_repo: GitCommandError: ...
2025-01-23 14:35:22 - analyze_repos - ERROR - Full traceback:
Traceback (most recent call last):
  File "/path/to/analyze_repos.py", line 82, in clone_repo
    ...
```

## Log Management

### Automatic Cleanup

The system includes automatic log cleanup functionality:

```python
from logger_config import LoggerConfig

# Clean up logs older than 30 days
removed = LoggerConfig.cleanup_old_logs(log_dir='Logs', days_to_keep=30)
print(f"Removed {removed} old log files")
```

### Manual Cleanup

```bash
# Remove all logs older than 30 days
find Logs/ -name "*.log*" -mtime +30 -delete

# Remove all logs
rm -rf Logs/*.log*

# Remove specific agent logs
rm Logs/gmail_agent.log*
```

### Disk Space Management

Monitor log disk usage:
```bash
# Check total size of Logs directory
du -sh Logs/

# Check size per log file
du -h Logs/*.log | sort -h
```

## Integration with Monitoring Tools

### Centralized Logging

Logs can be forwarded to centralized logging systems:
- Splunk
- ELK Stack (Elasticsearch, Logstash, Kibana)
- CloudWatch
- Datadog

### Log Aggregation

Use tools like `filebeat` or `fluentd` to collect and forward logs.

### Alerts

Set up alerts based on log patterns:
- ERROR count exceeds threshold
- Specific error messages
- Performance degradation

## Configuration

### Changing Log Levels

Edit `logger_config.py` to change default levels:

```python
# For more verbose file logs
file_handler.setLevel(logging.DEBUG)  # Already default

# For more console output
console_handler.setLevel(logging.INFO)  # Change from WARNING
```

### Changing Log Rotation

Edit `logger_config.py`:

```python
# Larger files before rotation
max_bytes=20*1024*1024  # 20MB instead of 10MB

# Keep more backups
backup_count=10  # 10 backups instead of 5
```

### Custom Log Directory

```python
logger = LoggerConfig.setup_logger('my_module', log_dir='CustomLogs')
```

## Best Practices

### For Users

1. **Check logs when errors occur** - Logs contain detailed error information
2. **Include logs in bug reports** - Attach relevant log snippets
3. **Monitor disk space** - Logs can grow over time
4. **Archive important logs** - Save logs before cleanup if needed

### For Developers

1. **Log at appropriate levels**
   - DEBUG: Detailed diagnostic info
   - INFO: Normal operation progress
   - WARNING: Unexpected but handled situations
   - ERROR: Failures and exceptions

2. **Include context in log messages**
   - Include IDs, filenames, counts
   - Example: `f"Processing repository {repo_id}: {repo_url}"`

3. **Log exceptions properly**
   - Use `LoggerConfig.log_exception()` for full tracebacks
   - Include operation context

4. **Avoid sensitive data in logs**
   - Don't log passwords, tokens, or API keys
   - Truncate long strings if needed

## Performance Impact

Logging has minimal performance impact:
- File I/O is buffered
- DEBUG logs to file don't slow down console output
- Async operations not blocked by logging
- Log rotation happens automatically in background

## Privacy and Security

### What's NOT Logged

- OAuth tokens and credentials
- Email message bodies (only metadata)
- User passwords
- API keys

### What IS Logged

- File paths and names
- Repository URLs (public information)
- Email subjects and IDs
- Timestamps and counts
- Error messages and stack traces

### Securing Log Files

```bash
# Restrict log directory permissions
chmod 700 Logs/

# Restrict log file permissions
chmod 600 Logs/*.log
```

## Troubleshooting Logging Issues

### Logs Not Being Created

Check:
1. `Logs/` directory exists and is writable
2. No permission errors
3. Logger is properly initialized

### Logs Too Large

Solutions:
1. Reduce `max_bytes` in `logger_config.py`
2. Reduce `backup_count`
3. Run cleanup more frequently
4. Change log level to INFO instead of DEBUG

### Missing Log Entries

Check:
1. Log level configuration
2. Console vs file handler levels
3. Logger name matches module

## Support

For logging-related issues:
1. Check this documentation
2. Review log configuration in `logger_config.py`
3. Check file permissions on Logs/ directory
4. See main README.md for general troubleshooting
