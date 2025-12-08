# Enhanced Visualization Feature with Matplotlib & Seaborn

## Overview
The Results tracking system now generates beautiful, professional charts using **Matplotlib** and **Seaborn** libraries, creating visual graphs that are embedded in the Results.md file.

## New Features

### Professional Charts
- **Horizontal Bar Charts** - For email counts, repository metrics
- **Pie Charts** - For distribution and proportions
- **Histograms with KDE** - For grade distributions
- **Stacked Bar Charts** - For success/failure comparisons
- **Color-coded Charts** - Using Seaborn's color palettes

### Chart Types by Agent

#### 1. Gmail Search Agent
- **Horizontal Bar Chart**: Emails retrieved per search
- Colors from Seaborn's "husl" palette
- Value labels on each bar

#### 2. Repository Analyzer Agent
- **Histogram + KDE**: Grade distribution with density curve
- **Pie Chart**: Grade category proportions
- **Horizontal Bar Chart**: Top 5 repositories
- Color gradients from "RdYlGn" (Red-Yellow-Green)
- Grade boundary lines at 90%, 70%, 50%

#### 3. Message Writer Agent
- **Horizontal Bar Chart**: Message style distribution
- **Pie Chart**: Message style proportions
- Custom colors for each style

#### 4. Email Drafter Agent
- **Stacked Bar Chart**: Success vs Failed drafts
- Green for success, red for failures
- Value labels inside bars

## Installation

Install visualization dependencies:

```bash
pip install -r requirements_viz.txt
```

Or install individually:
```bash
pip install matplotlib seaborn numpy
```

## File Structure

```
results_tracker/
├── __init__.py
├── tracker.py (93 lines)
├── visualizations.py (30 lines) - Text charts
├── chart_generator.py (67 lines) - Horizontal bars
├── chart_generator2.py (106 lines) - Pie & stacked charts
├── chart_generator3.py (106 lines) - Advanced charts
├── gmail_tracker.py (68 lines)
├── repo_tracker.py (106 lines)
├── message_tracker.py (86 lines)
└── email_tracker.py (57 lines)

Results_Charts/ (auto-generated)
├── gmail_search_results.png
├── repo_grade_distribution.png
├── repo_grade_pie.png
├── repo_top5.png
├── message_styles_bar.png
├── message_styles_pie.png
└── email_drafts.png
```

## Chart Specifications

### Design Choices
- **DPI**: 150 for high-quality output
- **Style**: Seaborn's "whitegrid" theme
- **Palette**: "husl" for diverse colors
- **Figure Sizes**: Dynamically adjusted based on data
- **Fonts**: Bold titles and labels

### Color Schemes
- **Gmail/Messages**: Seaborn "husl" palette
- **Repository Grades**: "RdYlGn" (traffic light colors)
- **Success/Failure**: Green (#2ecc71) / Red (#e74c3c)

## Results.md Integration

Charts are embedded using markdown image syntax:
```markdown
![Chart Title](Results_Charts/chart_name.png)
```

### Collapsible Text Versions
Text-based charts are still available in collapsible sections:
```markdown
<details>
<summary>Text Version</summary>

```
Text chart here
```
</details>
```

## Example Output

### Gmail Search Results
```markdown
### Emails Retrieved per Search

![Emails Retrieved per Search](Results_Charts/gmail_search_results.png)

<details>
<summary>Text Version</summary>
...text chart...
</details>
```

### Repository Grade Distribution
```markdown
### Grade Distribution

![Grade Distribution](Results_Charts/repo_grade_distribution.png)

![Grade Categories](Results_Charts/repo_grade_pie.png)
```

## Chart Details

### Histogram with KDE (Repository Grades)
- X-axis: Grade percentage (0-100%)
- Y-axis: Number of repositories
- KDE curve: Shows probability density
- Vertical lines: Grade boundaries (90%, 70%, 50%)
- Legend: Color-coded categories

### Pie Charts
- Auto-percentages on wedges
- Color-coded segments
- White bold text for readability
- Clockwise from top (startangle=90)

### Horizontal Bar Charts
- Left-aligned labels
- Right-side value labels
- Proportional bar widths
- Grid for easy reading

### Stacked Bar Charts
- Green (success) + Red (failure)
- Value labels centered in bars
- Total height shows combined count
- Legend for clarity

## Benefits

### Over Text Charts
✅ **Visual Appeal**: Professional, publication-ready charts
✅ **Color Coding**: Immediate visual feedback
✅ **Patterns**: Easier to spot trends and outliers
✅ **Presentation**: Ready for reports and presentations
✅ **Accessibility**: Both visual and text versions available

### Technical Benefits
✅ **High Resolution**: 150 DPI for sharp images
✅ **Non-interactive**: Runs in background without GUI
✅ **Automatic**: Generated during pipeline execution
✅ **Modular**: Easy to add new chart types
✅ **Customizable**: Seaborn themes and palettes

## Usage

No changes needed! Simply run:
```bash
python pipeline.py --config config.json
```

Charts are automatically:
1. Generated during execution
2. Saved to Results_Charts/
3. Embedded in Results.md
4. Displayed when Results.md is shown

## Viewing Results

### In Terminal
Text versions are shown when Results.md is displayed

### In Browser/Editor
Open Results.md in:
- GitHub (charts render automatically)
- VS Code (with markdown preview)
- Any markdown viewer
- Web browser

## Performance

Chart generation adds minimal overhead:
- ~0.1-0.5 seconds per chart
- Non-blocking (sequential generation)
- Automatic cleanup of old charts

## Customization

### Changing Colors
Edit chart_generator files:
```python
colors = sns.color_palette("your_palette", n)
```

### Changing Sizes
Modify figsize in chart methods:
```python
fig, ax = plt.subplots(figsize=(width, height))
```

### Adding Chart Types
1. Add method to appropriate chart_generator file
2. Call from tracker module
3. Embed in Results.md

## Troubleshooting

### Charts Not Displaying
- Ensure matplotlib & seaborn are installed
- Check Results_Charts/ directory exists
- Verify file paths in Results.md

### ImportError
```bash
pip install matplotlib seaborn numpy
```

### Low Quality Charts
- Increase DPI in chart_generator files
- Adjust figure size for more space

## Line Count Summary

All files remain under 150 lines:
```
chart_generator.py:    67 lines ✅
chart_generator2.py:  106 lines ✅
chart_generator3.py:  106 lines ✅
gmail_tracker.py:      68 lines ✅
repo_tracker.py:      106 lines ✅
message_tracker.py:    86 lines ✅
email_tracker.py:      57 lines ✅
```

## Next Steps

Future enhancements:
- Interactive HTML charts with Plotly
- Real-time chart updates
- Chart comparison across runs
- Export to PDF with all charts
- Dashboard with all metrics

---

**Status**: COMPLETE ✅
**All files under 150 lines** ✅
**Professional visualizations** ✅
**Fully integrated** ✅
