# Gmail Agent - Email Retrieval and Export Tool

A Python agent that connects to Gmail, retrieves emails based on search criteria, and exports them to Excel format.

## Features

- OAuth 2.0 authentication with Gmail API
- Flexible email search using Gmail's search syntax
- Export emails to Excel with formatted columns
- Command-line interface for easy automation
- Supports pagination for large result sets

## Requirements

- Python 3.7 or higher
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

Pipeline mode allows you to execute multiple searches in sequence using a JSON configuration file. This is ideal for:
- Running scheduled email exports
- Batch processing multiple search criteria
- Automating recurring email retrieval tasks
- Generating multiple reports at once

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
  ]
}
```

#### Configuration Fields

Each search in the configuration supports:

- **name** (optional): Descriptive name for the search (defaults to "Search N")
- **query** (required): Gmail search query string
- **output** (optional): Output Excel filename (defaults to "search_N.xlsx")
- **max_results** (optional): Maximum emails to retrieve (defaults to 100)

Global configuration:

- **credentials_file** (optional): Path to OAuth credentials (defaults to "credentials.json")

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

The Excel file contains the following columns:

1. **ID** - Unique Gmail message ID
2. **TimeStamp** - Date and time the email was received
3. **Subject** - Email subject line
4. **Search Criteria** - The search query used to retrieve this email
5. **Repo URL** - The first URL found in the email body (useful for tracking links to repositories, documents, or resources)

The Excel file includes:
- Formatted headers with blue background
- Auto-adjusted column widths
- Professional styling
- Automatic URL extraction from email body content

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

## Security Notes

- **Keep `credentials.json` secure** - This file contains your OAuth client credentials
- **Keep `token.pickle` secure** - This file contains your access token
- **Never commit these files to version control** - Add them to `.gitignore`
- The agent only requests **read-only** access to your Gmail

## Adding to .gitignore

Create a `.gitignore` file to prevent sensitive files from being committed:

```
credentials.json
token.pickle
*.xlsx
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
