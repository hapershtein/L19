# Message Writer Agent

A Python agent that generates personalized feedback messages based on code modularity grades using distinctive communication styles inspired by four public figures.

## Features

- Reads repository analysis data with modularity grades from Excel
- Generates personalized feedback messages based on grade ranges
- Uses four distinctive communication styles:
  - **Donald Trump** (90-100%): Congratulatory, superlative-heavy
  - **Benjamin Netanyahu** (70-89%): Analytical, evidence-based positive feedback
  - **Shahar Hason** (50-69%): Humorous, encouraging improvement messages
  - **Dudi Amsalem** (<50%): Brutally honest, direct, demanding improvement
- Exports enhanced Excel file with feedback column
- Text wrapping and formatting for readability

## Requirements

- Python 3.7 or higher
- openpyxl package (already in requirements.txt)

## Usage

### Basic Usage

```bash
python message_writer.py --input Output_23.xlsx
```

This will:
1. Read analysis data from `Output_23.xlsx`
2. Generate personalized messages for each repository based on grade
3. Export to `Output_34.xlsx` with new "Feedback Message" column

### Command-Line Options

- `--input`: Input Excel file with grades (default: `Output_23.xlsx`)
- `--output`: Output Excel file with messages (default: `Output_34.xlsx`)

### Examples

#### Use custom input/output files

```bash
python message_writer.py --input analyzed_repos.xlsx --output feedback_repos.xlsx
```

#### Process specific analysis file

```bash
python message_writer.py --input student_analysis.xlsx --output student_feedback.xlsx
```

## Input File Format

The input Excel file must contain these columns:

- **ID** - Unique identifier
- **TimeStamp** - Timestamp
- **Subject** - Email subject
- **Search Criteria** - Search query used
- **github Repo URL** - GitHub repository URL
- **Total Lines** - Total lines of code
- **Lines in Small Files** - Lines in files below threshold
- **Grade (%)** - Modularity percentage (REQUIRED for message generation)

## Output File Format

The output file contains all input columns plus:

- **Feedback Message** - Personalized feedback based on grade

Column is configured with text wrapping for better readability.

## Message Styles by Grade

### 90-100%: Donald Trump Style (Congratulations!)

**Characteristics:**
- Superlatives (INCREDIBLE, TREMENDOUS, BEST)
- Emphatic capitals
- Short, punchy sentences
- "Believe me", "Nobody does it better"
- Victory and winning language

**Example:**
> INCREDIBLE! Absolutely INCREDIBLE! This code is 95.5% modular - that's TREMENDOUS!
> Nobody writes code this good. Nobody. This is THE BEST. Beautiful, clean, modular -
> just perfect. This developer is a WINNER!

### 70-89%: Benjamin Netanyahu Style (Positive Feedback)

**Characteristics:**
- Evidence-based language
- Historical references
- "Let me be clear", "The data speaks for itself"
- Measured, professorial tone
- Forward-looking encouragement

**Example:**
> Let me be clear: achieving 78.3% modularity demonstrates solid technical capability.
> The evidence shows a well-structured codebase with thoughtful organization. This level
> of modular design reflects an understanding of best practices and maintainability.
> Well done.

### 50-69%: Shahar Hason Style (Needs Improvement)

**Characteristics:**
- Hebrew phrases mixed in
- Humorous comparisons
- Encouraging and light-hearted
- Emojis for tone
- "You got this!" mentality
- Relatable analogies

**Example:**
> אז... 62.7% modularity. לא רע, לא רע בכלל! (Not bad at all!) But listen, we can do
> better here, right? Think of it like hummus - better in small containers than one huge
> bucket! 😊 You're on the right track, my friend. Keep going! 💪

### 0-49%: Dudi Amsalem Style (Brutally Honest)

**Characteristics:**
- Direct and confrontational
- Hebrew interjections
- Urgent, demanding tone
- Strong warnings
- No sugar-coating
- "This is unacceptable!" approach

**Example:**
> תקשיב טוב (Listen well) - 42.3% modularity?! זה לא מקובל! (This is unacceptable!)
> What is this? Giant files, no organization! די כבר! (Enough already!) Break these
> files down! This needs MAJOR improvement. NOW. לא מחר! (Not tomorrow!) NOW! ⚠️

## How It Works

### 1. Read Analysis Data

Loads the Excel file with repository analysis and grades:

```python
writer = MessageWriter(input_file='Output_23.xlsx')
data = writer.read_excel_data()
```

### 2. Generate Messages

For each repository, determines appropriate style based on grade:

- Grade >= 90: Trump style (congratulations)
- Grade 70-89: Netanyahu style (positive)
- Grade 50-69: Hason style (improvement needed)
- Grade < 50: Amsalem style (brutally honest)

### 3. Export Enhanced File

Creates new Excel file with all original columns plus Feedback Message column.

### 4. Summary Report

Displays statistics:

```
Message Generation Summary
======================================================================
Total Repositories: 15

Messages by Style:
  Trump (90-100%):     3 - Congratulations
  Netanyahu (70-89%):  5 - Positive Feedback
  Hason (50-69%):      4 - Needs Improvement
  Amsalem (<50%):      3 - Brutally Honest
```

## Example Output

### Console Output

```
Reading data from Output_23.xlsx...
Found 10 repositories to process

======================================================================
Generating Personalized Messages
======================================================================

[1/10] 12345 - Grade: 95.30% - Style: Trump (Congratulations)
[2/10] 12346 - Grade: 78.50% - Style: Netanyahu (Positive)
[3/10] 12347 - Grade: 62.10% - Style: Hason (Improvement)
[4/10] 12348 - Grade: 42.80% - Style: Amsalem (Brutally Honest)
...

✓ Generated 10 personalized messages

Exporting results to Output_34.xlsx...
✓ Successfully exported to Output_34.xlsx

======================================================================
Message Generation Summary
======================================================================
Total Repositories: 10

Messages by Style:
  Trump (90-100%):     2 - Congratulations
  Netanyahu (70-89%):  3 - Positive Feedback
  Hason (50-69%):      3 - Needs Improvement
  Amsalem (<50%):      2 - Brutally Honest
```

## Integration with Pipeline

The message writer integrates seamlessly with the complete pipeline:

```json
{
  "searches": [ /* email searches */ ],
  "analyze_repos": { /* repo analysis */ },
  "generate_messages": {
    "input_file": "Output_23.xlsx",
    "output_file": "Output_34.xlsx"
  }
}
```

Full pipeline execution:
1. Gmail Agent retrieves emails → `Output_12.xlsx`
2. Analyze Repos clones and analyzes → `Output_23.xlsx`
3. Message Writer generates feedback → `Output_34.xlsx`

## Use Cases

### Student Assignment Grading

```bash
# Generate feedback for student submissions
python message_writer.py --input student_repos.xlsx --output student_feedback.xlsx
```

- Excellent students get Trump's enthusiastic congratulations
- Good students get Netanyahu's professional positive feedback
- Struggling students get Hason's encouraging but firm guidance
- Poor submissions get Amsalem's wake-up call

### Code Review Feedback

- Automated personalized feedback for repository quality
- Different tones for different quality levels
- Engaging and memorable messages

### Team Morale Management

- Celebrate great work with enthusiasm (Trump)
- Acknowledge solid work professionally (Netanyahu)
- Encourage improvement humorously (Hason)
- Address serious issues directly (Amsalem)

## Message Rotation

Each style has multiple message templates that rotate based on the repository ID hash, ensuring variety even for repositories with similar grades.

## Customization

### Modify Grade Thresholds

Edit `generate_message()` method in `message_writer.py`:

```python
if grade >= 95:  # Change from 90 to 95
    return self.generate_trump_message(repo_data)
```

### Add New Message Templates

Add messages to the respective style methods:

```python
def generate_trump_message(self, repo_data):
    messages = [
        # Existing messages...
        "Your new message here...",
    ]
```

### Change Message Styles

Replace or modify the style methods to change tone, language, or approach.

## Character Encoding

The agent properly handles:
- Hebrew characters (UTF-8)
- Emojis
- Special characters
- Mixed language content

## Error Handling

The agent handles:
- Missing input files
- Missing required columns
- Invalid grade values (treats as 0.0)
- Empty rows
- Various grade formats (numeric, string with %)

## Performance

- Fast processing (no external API calls)
- Efficient Excel I/O with openpyxl
- Handles hundreds of repositories easily

## Limitations

- Requires Grade (%) column in input
- Messages are in English with Hebrew phrases
- Fixed grade thresholds (customizable via code)
- No machine learning (template-based)

## Ethical Considerations

The message styles are:
- Inspired by public communication patterns
- Used for educational and motivational purposes
- Not endorsements of any political figures
- Intended to be engaging and memorable
- Should be used appropriately for context

## Troubleshooting

### "Required column not found"

Ensure input file has all required columns, especially "Grade (%)" or a column containing "Grade".

### Messages are too harsh/soft

Adjust grade thresholds or modify message templates in the respective methods.

### Hebrew characters display incorrectly

Ensure your terminal/system supports UTF-8 encoding. Excel should handle it properly.

### No messages generated

Check that grade values are valid numbers in the input file.

## License

This project is open source and available for personal and educational use.

## Disclaimer

Message styles are analytical interpretations of public communication patterns for
educational and engagement purposes. They are not political endorsements or criticisms.
