# Analyze Repos Agent

A Python agent that reads GitHub repository URLs from an Excel file, clones them in parallel, analyzes code metrics, and generates a detailed report.

## Features

- Reads GitHub URLs from Excel input file
- **Async parallel cloning** - Clones up to 5 repositories simultaneously for optimal performance
- Analyzes code metrics:
  - Total lines of code across entire repository
  - Lines of code in small files (< 150 lines)
  - Grade calculation (total lines / small files lines)
- Exports results to Excel with formatted output
- Progress tracking and detailed status reporting
- Automatic cleanup of temporary files
- Error handling for failed clones or missing URLs

## Requirements

- Python 3.7 or higher
- Git installed and available in PATH
- openpyxl package (already in requirements.txt)

## Installation

The required packages are already in `requirements.txt`. If you haven't installed them:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python analyze_repos.py --input Output_12.xlsx
```

This will:
1. Read GitHub URLs from `Output_12.xlsx`
2. Clone repositories to `TempFiles/` directory (parallel, up to 5 at once)
3. Analyze each repository's code metrics
4. Generate `Output_23.xlsx` with results
5. Clean up temporary files

### Command-Line Options

- `--input`: Input Excel file path (default: `Output_12.xlsx`)
- `--output`: Output Excel file path (default: `Output_23.xlsx`)
- `--temp-dir`: Directory for cloned repos (default: `TempFiles`)
- `--no-cleanup`: Keep cloned repositories after analysis

### Examples

#### Use custom input/output files

```bash
python analyze_repos.py --input my_repos.xlsx --output analysis_results.xlsx
```

#### Keep cloned repositories for manual inspection

```bash
python analyze_repos.py --input Output_12.xlsx --no-cleanup
```

#### Use custom temporary directory

```bash
python analyze_repos.py --input Output_12.xlsx --temp-dir MyRepos
```

## Input File Format

The input Excel file must contain these columns:

- **ID** - Unique identifier for each repository
- **TimeStamp** - Timestamp of the email
- **Subject** - Email subject
- **Search Criteria** - Search query used
- **github Repo URL** - GitHub repository URL (must start with `https://github.com`)

Example:
| ID | TimeStamp | Subject | Search Criteria | github Repo URL |
|----|-----------|---------|-----------------|-----------------|
| 12345 | 2024-11-19 | Repo submission | label:EmailTesting | https://github.com/user/repo |

## Output File Format

The output Excel file contains all input columns plus three new analysis columns:

1. **ID** - Original ID from input
2. **TimeStamp** - Original timestamp
3. **Subject** - Original subject
4. **Search Criteria** - Original search criteria
5. **github Repo URL** - Original GitHub URL
6. **Total Lines** - Total lines of code in entire repository
7. **Lines in Small Files (<150)** - Lines in files with fewer than 150 lines
8. **Grade** - Calculated as: Total Lines ÷ Lines in Small Files

### Grade Interpretation

- **Higher grade** = More code in larger files (more complex/consolidated codebase)
- **Lower grade** = More code distributed in small files (more modular codebase)
- **Grade of 1.0** = All code is in small files
- **Grade > 2.0** = Significant amount of code in larger files

## How It Works

### 1. Parallel Cloning

The agent uses Python's `asyncio` to clone up to 5 repositories simultaneously:

```
[repo1] Cloning https://github.com/user/repo1...
[repo2] Cloning https://github.com/user/repo2...
[repo3] Cloning https://github.com/user/repo3...
[repo4] Cloning https://github.com/user/repo4...
[repo5] Cloning https://github.com/user/repo5...
```

Each repository is cloned with `--depth 1` for faster downloads (shallow clone).

### 2. Repository Storage

Each repository is cloned to a unique folder based on its ID:

```
TempFiles/
├── 12345/          # Repository with ID 12345
├── 12346/          # Repository with ID 12346
└── 12347/          # Repository with ID 12347
```

### 3. Code Analysis

For each cloned repository:
- Walks through all files (excluding `.git` directory)
- Counts lines in each file
- Tracks total lines across all files
- Tracks lines in files with < 150 lines
- Calculates grade metric

### 4. Output Generation

Results are exported to Excel with:
- All original columns from input file
- Three new metric columns
- Formatted headers with blue background
- Auto-adjusted column widths

### 5. Cleanup

By default, all cloned repositories are removed after analysis. Use `--no-cleanup` to keep them.

## Example Output

```
Reading data from Output_12.xlsx...
Found 10 repositories to analyze

======================================================================
Starting parallel repository cloning
======================================================================

[12345] Cloning https://github.com/user/repo1...
[12346] Cloning https://github.com/user/repo2...
[12347] Cloning https://github.com/user/repo3...
[12345] ✓ Clone successful
[12345] Analyzing code...
[12345] ✓ Analysis complete: 5,234 total lines, 1,876 lines in small files (<150 lines), Grade: 2.79
[12346] ✓ Clone successful
[12346] Analyzing code...
[12346] ✓ Analysis complete: 3,421 total lines, 2,105 lines in small files (<150 lines), Grade: 1.63

...

======================================================================
Analysis Summary
======================================================================
Total Repositories: 10
Successfully Analyzed: 8
Clone Failed: 1
No URL: 1

Average Lines per Repo: 4,327

Exporting results to Output_23.xlsx...
✓ Successfully exported to Output_23.xlsx

Cleaning up temporary files in TempFiles...
✓ Cleanup complete
```

## Performance

- **Parallel cloning**: Up to 5 repositories cloned simultaneously (configurable via `semaphore`)
- **Shallow clones**: Uses `--depth 1` for faster downloads
- **Efficient analysis**: Single-pass file system walk

For 10 repositories, typical execution time:
- Sequential cloning: ~5-10 minutes
- Parallel cloning: ~1-3 minutes

## Error Handling

The agent handles various error conditions:

- **No URL**: Skips repositories with empty GitHub URL column
- **Clone failures**: Reports failed clones but continues with other repositories
- **File read errors**: Ignores files that cannot be read (binary files, encoding issues)
- **Missing columns**: Validates required columns exist in input file

Failed repositories are marked as "N/A" in the output file.

## Troubleshooting

### "Git is not recognized"

Make sure Git is installed and available in your PATH:

```bash
git --version
```

If not installed, download from [git-scm.com](https://git-scm.com/)

### "Input file not found"

Ensure the input Excel file exists:

```bash
ls -la Output_12.xlsx
```

### "Permission denied" when cloning

Some repositories may be private or require authentication. The agent will skip these and mark them as "clone_failed".

### Analysis is slow

- The agent limits concurrent clones to 5 to avoid overwhelming your network
- Large repositories take longer to clone
- Use `--no-cleanup` to inspect which repos are taking longest

## Advanced Usage

### Modify Concurrent Clone Limit

Edit `analyze_repos.py` line 28:

```python
self.semaphore = asyncio.Semaphore(10)  # Increase to 10 concurrent clones
```

### Change "Small File" Threshold

Edit `analyze_repos.py` line 188:

```python
if line_count < 200:  # Change from 150 to 200
```

### Include Specific File Types Only

Modify the `analyze_repo` method to filter by file extension:

```python
# Only analyze Python files
if file.endswith('.py'):
    line_count = self.count_lines_in_file(file_path)
```

## Integration with Gmail Agent

This agent is designed to work with the Gmail Agent output:

```bash
# Step 1: Get repos from Gmail
python pipeline.py --config config.json

# Step 2: Analyze the repos (rename output file to Output_12.xlsx)
mv email_lTesting.xlsx Output_12.xlsx
python analyze_repos.py --input Output_12.xlsx
```

## Security Notes

- Cloned repositories are temporary and can be automatically deleted
- The agent only performs read operations on cloned code
- No code is executed from cloned repositories
- Use caution when keeping cloned repositories with `--no-cleanup`

## License

This project is open source and available for personal and educational use.
