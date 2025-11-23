# Gmail Agent - Email Retrieval and Export Tool

A Python agent system that connects to Gmail, retrieves emails based on search criteria, extracts GitHub repository URLs, and optionally clones and analyzes the repositories with code metrics.

## Features

**Gmail Agent:**
- OAuth 2.0 authentication with Gmail API
- Flexible email search using Gmail's search syntax
- Export emails to Excel with formatted columns
- Automatic GitHub URL extraction from email bodies
- Command-line interface for easy automation
- Supports pagination for large result sets

**Analyze Repos Agent:**
- Async parallel repository cloning (up to 5 concurrent)
- Code metrics analysis (total lines, small files, modularity grade)
- Automatic cleanup of temporary files
- Progress tracking and error handling
- Integrates seamlessly with Gmail Agent pipeline

**Message Writer Agent:**
- Generates personalized feedback messages based on modularity grades
- Four distinctive communication styles based on grade ranges
- Trump style (90-100%): Congratulatory and enthusiastic
- Netanyahu style (70-89%): Professional and evidence-based
- Shahar Hason style (50-69%): Humorous and encouraging
- Dudi Amsalem style (<50%): Brutally honest and direct
- Exports enhanced Excel with feedback column

**Email Drafter Agent:**
- Creates Gmail draft messages from feedback messages
- Automatic subject line generation: "Feedback message to [ID]"
- OAuth 2.0 authentication with Gmail API
- Batch processing of multiple feedback messages
- Drafts stored in Gmail Drafts folder for review before sending
- Integrates seamlessly with complete pipeline

## Features Summary

- **Comprehensive Logging**: All operations logged to rotating files in `Logs/` folder
- **Automatic Log Rotation**: 10MB per file, 5 backups, prevents disk space issues
- **Detailed Error Tracking**: Full exception traces for debugging
- **Session Tracking**: Unique session IDs for each execution

## Requirements

- Python 3.7 or higher
- Git installed and available in PATH (for repository analysis)
- Google Cloud Project with Gmail API enabled
- OAuth 2.0 credentials from Google Cloud Console

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Google Cloud Project

#### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Note your project name/ID

#### Step 2: Enable Gmail API

1. In the Cloud Console, go to **APIs & Services** > **Library**
2. Search for "Gmail API"
3. Click on "Gmail API" and click **Enable**

#### Step 3: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth client ID**
3. If prompted, configure the OAuth consent screen:
   - Choose **External** user type (unless you have a Google Workspace)
   - Fill in the required fields (App name, user support email, developer email)
   - Add your email as a test user in the "Test users" section
   - Click **Save and Continue** through the scopes and summary
4. Back in Credentials, click **Create Credentials** > **OAuth client ID**
5. Select **Desktop app** as the application type
6. Name it (e.g., "Gmail Agent")
7. Click **Create**

#### Step 4: Download Credentials

1. After creating the OAuth client ID, click the download icon (⬇)
2. Save the file as `credentials.json` in the same directory as `gmail_agent.py`

## Usage

There are two ways to use the Gmail Agent:

1. **Single Search Mode** - Run one search at a time via command line
2. **Pipeline Mode** - Execute multiple searches from a JSON configuration file

### Single Search Mode

#### Basic Usage

```bash
python gmail_agent.py --query "your search criteria"
```

#### Command-Line Options

- `--query` (required): Gmail search query
- `--output`: Output Excel file path (default: `gmail_export.xlsx`)
- `--max`: Maximum number of emails to retrieve (default: 100)
- `--credentials`: Path to OAuth credentials file (default: `credentials.json`)

### Examples

#### Search for emails from a specific sender

```bash
python gmail_agent.py --query "from:example@gmail.com" --output from_example.xlsx
```

#### Search for emails with specific subject

```bash
python gmail_agent.py --query "subject:invoice" --max 50
```

#### Search for unread emails

```bash
python gmail_agent.py --query "is:unread"
```

#### Search with date range

```bash
python gmail_agent.py --query "after:2024/01/01 before:2024/12/31"
```

#### Complex search query

```bash
python gmail_agent.py --query "from:boss@company.com after:2024/01/01 has:attachment"
```

#### Search for emails with attachments

```bash
python gmail_agent.py --query "has:attachment filename:pdf"
```

### Gmail Search Operators

The agent supports all Gmail search operators:

- `from:` - Emails from a specific sender (e.g., `from:user@example.com`)
- `to:` - Emails to a specific recipient (e.g., `to:user@example.com`)
- `subject:` - Emails with specific subject text (e.g., `subject:meeting`)
- `has:attachment` - Emails with attachments
- `filename:` - Emails with specific attachment types (e.g., `filename:pdf`)
- `is:unread` - Unread emails
- `is:read` - Read emails
- `is:starred` - Starred emails
- `is:important` - Important emails
- `after:` - Emails after a date (e.g., `after:2024/01/01`)
- `before:` - Emails before a date (e.g., `before:2024/12/31`)
- `older_than:` - Emails older than a time period (e.g., `older_than:1y`)
- `newer_than:` - Emails newer than a time period (e.g., `newer_than:7d`)
- `label:` - Emails with a specific label (e.g., `label:work`)
- `category:` - Emails in a category (e.g., `category:social`)

You can combine multiple operators with spaces (AND logic):
```bash
python gmail_agent.py --query "from:client@example.com after:2024/01/01 has:attachment"
```

### Pipeline Mode

Pipeline mode allows you to execute multiple searches in sequence using a JSON configuration file, and optionally analyze GitHub repositories found in the emails. This is ideal for:
- Running scheduled email exports
- Batch processing multiple search criteria
- Automating recurring email retrieval tasks
- Generating multiple reports at once
- **Analyzing GitHub repositories from email links (integrated repo analysis)**

#### Creating a Configuration File

Create a `config.json` file with your search configurations:

```json
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
      "name": "Important with Attachments",
      "query": "is:important has:attachment",
      "output": "important_attachments.xlsx",
      "max_results": 100
    },
    {
      "name": "Last Week from Boss",
      "query": "from:boss@company.com newer_than:7d",
      "output": "boss_emails_week.xlsx",
      "max_results": 50
    }
  ],
  "analyze_repos": {
    "input_file": "boss_emails_week.xlsx",
    "output_file": "analyzed_repos.xlsx",
    "temp_dir": "TempFiles",
    "cleanup": true
  }
}
```

#### Configuration Fields

**Search Configuration:**

Each search in the configuration supports:

- **name** (optional): Descriptive name for the search (defaults to "Search N")
- **query** (required): Gmail search query string
- **output** (optional): Output Excel filename (defaults to "search_N.xlsx")
- **max_results** (optional): Maximum emails to retrieve (defaults to 100)

**Global Configuration:**

- **credentials_file** (optional): Path to OAuth credentials (defaults to "credentials.json")

**Repository Analysis (Optional):**

Add an `analyze_repos` section to automatically analyze GitHub repositories from one of your output files:

- **input_file** (required): Excel file with GitHub URLs to analyze (should match one of your search outputs)
- **output_file** (optional): Output file for analysis results (defaults to "Output_23.xlsx")
- **temp_dir** (optional): Directory for cloning repos (defaults to "TempFiles")
- **cleanup** (optional): Remove cloned repos after analysis (defaults to true)

#### Running the Pipeline

Execute all searches in your configuration:

```bash
python pipeline.py --config config.json
```

#### Pipeline Options

- `--config`: Path to JSON configuration file (default: `config.json`)
- `--skip-on-error`: Continue to next search if one fails (default: stop on first error)
- `--report`: Generate a JSON report of the execution results

#### Pipeline Examples

```bash
# Run with default config.json
python pipeline.py

# Use custom configuration file
python pipeline.py --config my_searches.json

# Continue on errors and generate report
python pipeline.py --config config.json --skip-on-error --report results.json
```

#### Pipeline Output

The pipeline will display progress for each search:

```
[1/3] Unread Emails
──────────────────────────────────────────────────────────────────────
Query: is:unread
Output: unread_emails.xlsx
Max Results: 50
Found 12 messages. Retrieving details...
✓ Success: 12 emails exported to unread_emails.xlsx
  Duration: 2.34s

[2/3] Important with Attachments
──────────────────────────────────────────────────────────────────────
Query: is:important has:attachment
Output: important_attachments.xlsx
Max Results: 100
Found 45 messages. Retrieving details...
✓ Success: 45 emails exported to important_attachments.xlsx
  Duration: 5.67s

======================================================================
Pipeline Execution Summary
======================================================================
Total Searches: 3
Successful: 3
Failed: 0

Total Emails Retrieved: 57
```

#### Generating Reports

Use the `--report` option to create a JSON report:

```bash
python pipeline.py --config config.json --report results.json
```

The report contains detailed execution results:

```json
{
  "timestamp": "2024-11-19T14:30:00.000000",
  "config_file": "config.json",
  "total_searches": 3,
  "successful": 3,
  "failed": 0,
  "no_results": 0,
  "total_emails": 57,
  "searches": [
    {
      "name": "Unread Emails",
      "query": "is:unread",
      "output": "unread_emails.xlsx",
      "count": 12,
      "duration": 2.34,
      "status": "success"
    }
  ]
}
```

#### Integrated Workflow Example

Here's a complete workflow that retrieves emails, analyzes repositories, generates personalized feedback, and creates draft emails:

```json
{
  "credentials_file": "credentials.json",
  "searches": [
    {
      "name": "Student Repo Submissions",
      "query": "label:EmailTesting",
      "output": "student_repos.xlsx",
      "max_results": 100
    }
  ],
  "analyze_repos": {
    "input_file": "student_repos.xlsx",
    "output_file": "graded_repos.xlsx",
    "temp_dir": "TempFiles",
    "cleanup": true
  },
  "generate_messages": {
    "input_file": "graded_repos.xlsx",
    "output_file": "feedback_repos.xlsx"
  },
  "draft_emails": {
    "input_file": "feedback_repos.xlsx",
    "credentials_file": "credentials.json"
  }
}
```

When you run this configuration:

1. **Gmail Agent** retrieves emails matching "label:EmailTesting"
2. Extracts GitHub URLs from email bodies
3. Exports to `student_repos.xlsx` with columns: ID, TimeStamp, Subject, Search Criteria, github Repo URL
4. **Analyze Repos Agent** automatically:
   - Clones each repository (parallel, up to 5 at once)
   - Counts total lines and lines in small files (<150 lines)
   - Calculates modularity grade (percentage of code in small files)
   - Exports to `graded_repos.xlsx` with additional columns: Total Lines, Lines in Small Files, Grade (%)
5. **Message Writer Agent** automatically:
   - Reads grades from analysis results
   - Generates personalized feedback based on grade:
     - 90-100%: Enthusiastic congratulations (Trump style)
     - 70-89%: Professional positive feedback (Netanyahu style)
     - 50-69%: Encouraging improvement message (Shahar Hason style)
     - Below 50%: Brutally honest critique (Dudi Amsalem style)
   - Exports to `feedback_repos.xlsx` with new "Feedback Message" column
6. **Email Drafter Agent** automatically:
   - Reads feedback messages from Excel
   - Authenticates with Gmail API
   - Creates draft messages in Gmail Drafts folder
   - Subject: "Feedback message to [ID]"
   - Body: Complete feedback message
   - Drafts ready for review and sending
7. Cleans up temporary files

**Output:**

```
Starting pipeline execution
──────────────────────────────────────────────────────────────────────
[1/1] Student Repo Submissions
Query: label:EmailTesting
Found 15 messages. Retrieving details...
✓ Success: 15 emails exported to student_repos.xlsx

Starting Repository Analysis
──────────────────────────────────────────────────────────────────────
[12345] Cloning https://github.com/student1/project...
[12346] Cloning https://github.com/student2/project...
[12345] ✓ Clone successful
[12345] Analyzing code...
[12345] ✓ Analysis complete: 3,421 total lines, 1,876 lines in small files, Grade: 54.84%

Analysis Summary
Total Repositories: 15
Successfully Analyzed: 14
Clone Failed: 1
Average Lines per Repo: 4,123

Starting Message Generation
──────────────────────────────────────────────────────────────────────
Reading data from graded_repos.xlsx...
Found 14 repositories to process

[1/14] 12345 - Grade: 95.30% - Style: Trump (Congratulations)
[2/14] 12346 - Grade: 78.50% - Style: Netanyahu (Positive)
[3/14] 12347 - Grade: 62.10% - Style: Hason (Improvement)
[4/14] 12348 - Grade: 42.80% - Style: Amsalem (Brutally Honest)
...

✓ Generated 14 personalized messages
✓ Successfully exported to feedback_repos.xlsx

Message Generation Summary
Total Repositories: 14
Messages by Style:
  Trump (90-100%):     2 - Congratulations
  Netanyahu (70-89%):  5 - Positive Feedback
  Hason (50-69%):      4 - Needs Improvement
  Amsalem (<50%):      3 - Brutally Honest

Starting Email Draft Creation
──────────────────────────────────────────────────────────────────────
✓ Successfully authenticated with Gmail API

Reading data from feedback_repos.xlsx...
Found 14 feedback messages to draft

[1/14] Creating draft for ID: 12345
  ✓ Draft created successfully (ID: r-1234567890)
[2/14] Creating draft for ID: 12346
  ✓ Draft created successfully (ID: r-1234567891)
...

Draft Creation Summary
Total Feedback Messages: 14
Drafts Created: 14
Failed: 0

✓ Drafts are available in your Gmail account under 'Drafts' folder
```

## First Run

On the first run, the script will authenticate with Google:

### Automatic Browser Authentication (Default)

1. Opens your default web browser automatically
2. Redirects to Google login page
3. Asks you to log in and grant permissions
4. Saves the authentication token as `token.pickle` for future use

### Console Authentication (Fallback for WSL/Headless)

If the browser can't be opened automatically (common in WSL or remote environments), the script will:

1. Display a URL in the console
2. Ask you to manually copy and paste it into your browser
3. After authorization, provide a code to paste back into the console
4. Save the authentication token as `token.pickle` for future use

The token is saved locally and will be reused on subsequent runs, so you won't need to authenticate every time.

## Output Format

### Gmail Agent Output (e.g., Output_12.xlsx)

The Excel file contains the following columns:

1. **ID** - Unique Gmail message ID
2. **TimeStamp** - Date and time the email was received
3. **Subject** - Email subject line
4. **Search Criteria** - The search query used to retrieve this email
5. **github Repo URL** - GitHub repository URLs extracted from email body

### Repository Analysis Output (e.g., Output_23.xlsx)

Includes all Gmail Agent columns plus:

6. **Total Lines** - Total lines of code in the repository
7. **Lines in Small Files (<150)** - Lines in files below threshold
8. **Grade (%)** - Modularity percentage (higher = more modular)

### Message Writer Output (e.g., Output_34.xlsx)

Includes all Repository Analysis columns plus:

9. **Feedback Message** - Personalized feedback based on grade:
   - 90-100%: Trump-style congratulations
   - 70-89%: Netanyahu-style positive feedback
   - 50-69%: Shahar Hason-style improvement guidance
   - Below 50%: Dudi Amsalem-style brutally honest critique

All Excel files include:
- Formatted headers with blue background
- Auto-adjusted column widths
- Professional styling
- Text wrapping for long messages

## Troubleshooting

### "Credentials file not found"

Make sure you've downloaded the `credentials.json` file from Google Cloud Console and placed it in the same directory as the script.

### "Access blocked: This app's request is invalid"

1. Go to Google Cloud Console > APIs & Services > OAuth consent screen
2. Make sure you've added your email as a test user
3. Ensure the Gmail API is enabled

### "Token has been expired or revoked"

Delete the `token.pickle` file and run the script again to re-authenticate:

```bash
rm token.pickle
python gmail_agent.py --query "your search"
```

### Rate Limits

The Gmail API has usage quotas. If you're retrieving large numbers of emails, you may hit rate limits. The default `--max` is set to 100 to stay within reasonable limits.

### "xdg-open: no method available for opening" (WSL/Linux)

This occurs when running in WSL or a headless environment where the browser can't be opened automatically. The script will automatically fall back to console authentication mode where you:

1. Copy the URL displayed in the terminal
2. Paste it into your browser (on Windows or any device)
3. Complete the authentication
4. Copy the authorization code from the browser
5. Paste it back into the terminal

No additional configuration is needed - the fallback happens automatically.

## Standalone Agent Usage

You can also run the agents independently, without the full pipeline:

### Standalone Repository Analysis

```bash
# Analyze repos from any Excel file with GitHub URLs
python analyze_repos.py --input Output_12.xlsx --output analyzed.xlsx

# Keep cloned repos for manual inspection
python analyze_repos.py --input repos.xlsx --no-cleanup

# Use custom temp directory
python analyze_repos.py --input repos.xlsx --temp-dir MyRepos
```

The input Excel file must have a column named "github Repo URL" containing GitHub repository URLs.

**Output includes:**
- All original columns from input file
- **Total Lines** - Total lines of code in entire repository
- **Lines in Small Files (<150)** - Lines in files with fewer than 150 lines
- **Grade (%)** - Percentage of code in small files (higher = more modular codebase)

See `ANALYZE_REPOS_README.md` for detailed documentation on the repository analysis agent.

### Standalone Message Writer

```bash
# Generate feedback messages from analyzed repos
python message_writer.py --input Output_23.xlsx --output feedback.xlsx

# Use custom input/output files
python message_writer.py --input student_analysis.xlsx --output student_feedback.xlsx
```

The input Excel file must have a "Grade (%)" column with modularity percentages.

**Output includes:**
- All original columns from input file
- **Feedback Message** - Personalized feedback based on grade (Trump/Netanyahu/Hason/Amsalem styles)

See `MESSAGE_WRITER_README.md` for detailed documentation on the message writer agent.

### Standalone Email Drafter

```bash
# Create Gmail drafts from feedback messages
python email_drafter.py --input Output_34.xlsx

# Use custom input file
python email_drafter.py --input student_feedback.xlsx

# Use custom credentials
python email_drafter.py --input feedback.xlsx --credentials my_creds.json
```

The input Excel file must have "ID" and "Feedback Message" columns.

**Creates:**
- Gmail draft messages in your Drafts folder
- Subject: "Feedback message to [ID]"
- Body: Complete feedback message
- Ready for review and sending

See `EMAIL_DRAFTER_README.md` for detailed documentation on the email drafter agent.

## Logging

All agents include comprehensive logging to help with debugging and monitoring:

- **Log Location**: `Logs/` directory
- **Log Files**:
  - `gmail_agent.log` - Email retrieval operations
  - `analyze_repos.log` - Repository analysis
  - `message_writer.log` - Message generation
  - `email_drafter.log` - Draft creation
  - `pipeline_execution.log` - Complete pipeline runs
- **Rotation**: Automatic rotation at 10MB, keeps 5 backups
- **Format**: Timestamped with module, level, and detailed context

See `LOGGING_README.md` for complete logging documentation.

### View Logs

```bash
# View recent logs
tail -n 50 Logs/gmail_agent.log

# Follow pipeline execution in real-time
tail -f Logs/pipeline_execution.log

# Search for errors
grep "ERROR" Logs/*.log
```

## Security Notes

- **Keep `credentials.json` secure** - This file contains your OAuth client credentials
- **Keep `token.pickle` secure** - This file contains your access token
- **Never commit these files to version control** - Add them to `.gitignore`
- **Log files may contain IDs and URLs** - Treat log files as sensitive
- The agent only requests **read-only** access to your Gmail

## Adding to .gitignore

Create a `.gitignore` file to prevent sensitive files from being committed:

```
credentials.json
token.pickle
*.xlsx
Logs/
*.log
__pycache__/
*.pyc
```

## License

This project is open source and available for personal and educational use.

## Support

For issues related to:
- **Gmail API**: Check [Gmail API documentation](https://developers.google.com/gmail/api)
- **Google Cloud setup**: Check [Google Cloud documentation](https://cloud.google.com/docs)
- **Python dependencies**: Check the respective package documentation
