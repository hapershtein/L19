# Quick Start Guide

## Complete Integrated Pipeline

Run the entire workflow with one command:

```bash
python pipeline.py --config config.json
```

This will:
1. Retrieve emails from Gmail matching your search criteria
2. Extract GitHub URLs from email bodies
3. Clone all repositories in parallel
4. Analyze code metrics (lines, small files, grade)
5. Generate two Excel reports

## Files Generated

- `Output_12.xlsx` - Gmail search results with GitHub URLs
- `Output_23.xlsx` - Repository analysis with code metrics

## Configuration Example

Edit `config.json`:

```json
{
  "credentials_file": "credentials.json",
  "searches": [
    {
      "name": "Student Submissions",
      "query": "label:EmailTesting",
      "output": "Output_12.xlsx",
      "max_results": 50
    }
  ],
  "analyze_repos": {
    "input_file": "Output_12.xlsx",
    "output_file": "Output_23.xlsx",
    "temp_dir": "TempFiles",
    "cleanup": true
  }
}
```

## First Time Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Google Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable Gmail API
3. Create OAuth 2.0 credentials (Desktop app)
4. Download as `credentials.json`

### 3. Run Pipeline

```bash
python pipeline.py --config config.json
```

On first run, it will open a browser for Google authentication.

## Individual Agents

### Gmail Agent Only

```bash
python gmail_agent.py --query "label:EmailTesting" --output my_emails.xlsx
```

### Repository Analysis Only

```bash
python analyze_repos.py --input Output_12.xlsx --output analyzed.xlsx
```

## Output Columns

### Output_12.xlsx (Gmail Results)
- ID
- TimeStamp
- Subject
- Search Criteria
- github Repo URL

### Output_23.xlsx (Repository Analysis)
- All columns from Output_12.xlsx, plus:
- **Total Lines** - Total lines in repository
- **Lines in Small Files (<150)** - Lines in files with < 150 lines
- **Grade** - Total Lines ÷ Small Files Lines

## Grade Interpretation

- **Grade < 1.5** - Very modular codebase (mostly small files)
- **Grade 1.5-2.5** - Balanced code distribution
- **Grade > 2.5** - More code in larger files (complex/consolidated)

## Common Use Cases

### Grade Student Assignments

```json
{
  "searches": [
    {
      "name": "Homework Submissions",
      "query": "subject:homework has:attachment",
      "output": "submissions.xlsx"
    }
  ],
  "analyze_repos": {
    "input_file": "submissions.xlsx",
    "output_file": "graded.xlsx"
  }
}
```

### Track Team Repositories

```json
{
  "searches": [
    {
      "name": "Team Updates",
      "query": "from:team@company.com newer_than:7d",
      "output": "team_repos.xlsx"
    }
  ],
  "analyze_repos": {
    "input_file": "team_repos.xlsx",
    "output_file": "team_analysis.xlsx"
  }
}
```

### Monitor Open Source Contributions

```json
{
  "searches": [
    {
      "name": "PR Notifications",
      "query": "from:notifications@github.com subject:pull request",
      "output": "prs.xlsx"
    }
  ],
  "analyze_repos": {
    "input_file": "prs.xlsx",
    "output_file": "pr_analysis.xlsx"
  }
}
```

## Troubleshooting

### "No module named 'google'"

```bash
pip install -r requirements.txt
```

### "Git is not recognized"

Install Git from [git-scm.com](https://git-scm.com/)

### Browser won't open (WSL)

The script automatically falls back to console authentication. Just copy/paste the URL.

### "No URL" for some repositories

Some emails may not contain GitHub URLs. These will be marked as "N/A" in the analysis.

## Advanced Options

### Skip repository cleanup

```json
"analyze_repos": {
  "cleanup": false
}
```

Repositories will remain in `TempFiles/` for inspection.

### Custom concurrent clone limit

Edit `analyze_repos.py` line 28:

```python
self.semaphore = asyncio.Semaphore(10)  # Increase from 5 to 10
```

### Change small file threshold

Edit `analyze_repos.py` line 188:

```python
if line_count < 200:  # Change from 150 to 200
```

## Documentation

- `README.md` - Complete documentation
- `ANALYZE_REPOS_README.md` - Repository analysis details
- `config.json.example` - Configuration examples

## Support

For issues with:
- Gmail API: [Gmail API Docs](https://developers.google.com/gmail/api)
- Git operations: Check `git --version`
- Python packages: Check `pip list`
