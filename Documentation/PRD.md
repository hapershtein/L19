# Product Requirements Document (PRD)
## Gmail Agent System - Automated Email Processing and Repository Analysis

**Version:** 1.0
**Date:** November 2025
**Status:** Production Ready
**Project Type:** Educational/Enterprise Automation Tool

---

## Executive Summary

The Gmail Agent System is an integrated multi-agent platform that automates the complete workflow of retrieving emails from Gmail, analyzing GitHub repositories, generating personalized feedback messages, and creating draft responses. The system is designed for educational institutions, code review teams, and organizations that need to process and respond to repository submissions at scale.

### Key Metrics
- **4 Core Agents** working in coordinated pipeline
- **Processes 100+ repositories** in single execution
- **5 concurrent operations** for parallel repository cloning
- **4 feedback styles** based on code quality grades
- **Rotating logs** with 10MB files, 5 backups
- **74+ logging statements** across all agents

---

## 1. Product Overview

### 1.1 Product Vision

To provide a fully automated, intelligent system that transforms email-based repository submissions into actionable, personalized feedback with minimal human intervention, while maintaining comprehensive logging and monitoring capabilities.

### 1.2 Target Users

**Primary Users:**
- **Teaching Assistants** - Grading student code submissions
- **Course Instructors** - Managing programming assignments
- **Code Review Teams** - Evaluating multiple repositories
- **Engineering Managers** - Assessing team code quality

**Secondary Users:**
- **Students** - Receiving automated feedback
- **Developers** - Getting code quality assessments
- **Open Source Maintainers** - Reviewing contributions

### 1.3 Core Value Proposition

- **Time Savings**: Automates 90% of repetitive grading/review tasks
- **Consistency**: Applies uniform evaluation criteria
- **Scalability**: Handles hundreds of submissions simultaneously
- **Personality**: Provides engaging, memorable feedback
- **Transparency**: Complete audit trail via comprehensive logging

---

## 2. Functional Requirements

### 2.1 Gmail Agent (Email Retrieval)

**Purpose:** Retrieve emails from Gmail based on search criteria and extract GitHub repository URLs.

**Requirements:**

**FR-GA-001: Authentication**
- SHALL support OAuth 2.0 authentication with Gmail API
- SHALL use `gmail.readonly` scope
- SHALL save authentication token for reuse
- SHALL support both browser and console authentication flows
- SHALL automatically fallback to console auth in WSL/headless environments

**FR-GA-002: Email Search**
- SHALL support full Gmail search syntax
- SHALL support all Gmail operators (from, to, subject, has:attachment, etc.)
- SHALL retrieve up to configurable max results (default: 100)
- SHALL handle pagination for large result sets
- SHALL extract message ID, timestamp, subject, sender

**FR-GA-003: URL Extraction**
- SHALL extract first GitHub URL from email body
- SHALL support both plain text and HTML email bodies
- SHALL filter to only https://github.com URLs
- SHALL handle nested MIME parts recursively
- SHALL return empty string if no URL found

**FR-GA-004: Excel Export**
- SHALL export to Excel format (.xlsx)
- SHALL include columns: ID, TimeStamp, Subject, Search Criteria, github Repo URL
- SHALL format headers with blue background
- SHALL auto-adjust column widths
- SHALL preserve UTF-8 encoding

**FR-GA-005: Error Handling**
- SHALL handle API rate limits gracefully
- SHALL provide clear error messages
- SHALL log all errors with full context
- SHALL continue on individual email failures

### 2.2 Analyze Repos Agent (Repository Analysis)

**Purpose:** Clone GitHub repositories and analyze code metrics including modularity.

**Requirements:**

**FR-AR-001: Repository Cloning**
- SHALL clone repositories using git shallow clone (--depth 1)
- SHALL support concurrent cloning with semaphore limit (default: 5)
- SHALL clone to configurable temporary directory
- SHALL organize by repository ID
- SHALL handle clone failures without stopping pipeline
- SHALL support both public and authenticated repository access

**FR-AR-002: Code Analysis**
- SHALL count total lines of code across all files
- SHALL identify files below configurable threshold (default: 150 lines)
- SHALL count lines in small files
- SHALL calculate modularity grade: (small_files_lines / total_lines) * 100
- SHALL skip binary files, images, and non-code files
- SHALL handle empty repositories

**FR-AR-003: Excel Processing**
- SHALL read input Excel with GitHub URLs
- SHALL preserve all original columns
- SHALL add columns: Total Lines, Lines in Small Files (<N), Grade (%)
- SHALL export to new Excel file
- SHALL maintain data integrity

**FR-AR-004: Resource Management**
- SHALL support optional cleanup of cloned repositories
- SHALL handle cleanup failures gracefully
- SHALL free disk space after analysis
- SHALL support no-cleanup mode for inspection

### 2.3 Message Writer Agent (Feedback Generation)

**Purpose:** Generate personalized feedback messages based on code quality grades using distinctive communication styles.

**Requirements:**

**FR-MW-001: Message Generation**
- SHALL generate messages based on grade thresholds:
  - 90-100%: Trump style (congratulatory, superlative-heavy)
  - 70-89%: Netanyahu style (analytical, evidence-based)
  - 50-69%: Shahar Hason style (humorous, encouraging, Hebrew/English mix)
  - <50%: Dudi Amsalem style (brutally honest, direct, Hebrew/English)
- SHALL rotate through multiple message templates per style
- SHALL use hash-based selection for variety
- SHALL support UTF-8 for Hebrew characters and emojis

**FR-MW-002: Style Characteristics**

**Trump Style (90-100%):**
- SHALL use superlatives (INCREDIBLE, TREMENDOUS, BEST)
- SHALL use emphatic capitals
- SHALL use short, punchy sentences
- SHALL reference winning and success

**Netanyahu Style (70-89%):**
- SHALL use evidence-based language
- SHALL reference data and metrics
- SHALL use measured, professional tone
- SHALL provide forward-looking encouragement

**Shahar Hason Style (50-69%):**
- SHALL mix Hebrew phrases with English
- SHALL use humor and light-hearted comparisons
- SHALL use emojis appropriately
- SHALL encourage improvement positively

**Dudi Amsalem Style (<50%):**
- SHALL be direct and confrontational
- SHALL use Hebrew interjections
- SHALL demand immediate improvement
- SHALL provide urgent, warning-based feedback

**FR-MW-003: Excel Processing**
- SHALL read Grade (%) column from input
- SHALL add Feedback Message column
- SHALL enable text wrapping (width: 100)
- SHALL preserve all original columns
- SHALL handle missing or invalid grades

**FR-MW-004: Statistics**
- SHALL report message counts by style
- SHALL display summary statistics
- SHALL log generation progress

### 2.4 Email Drafter Agent (Draft Creation)

**Purpose:** Create Gmail draft messages from feedback for manual review and sending.

**Requirements:**

**FR-ED-001: Authentication**
- SHALL use separate token file (token_drafter.pickle)
- SHALL use `gmail.compose` scope
- SHALL support OAuth 2.0 flow
- SHALL handle authentication errors clearly

**FR-ED-002: Draft Creation**
- SHALL create draft for each feedback message
- SHALL format subject as: "Feedback message to [ID]"
- SHALL use feedback as email body
- SHALL support optional subject prefix
- SHALL NOT send emails automatically
- SHALL store drafts in Gmail Drafts folder

**FR-ED-003: Batch Processing**
- SHALL process multiple feedback messages
- SHALL track success/failure per draft
- SHALL continue on individual failures
- SHALL report summary statistics

**FR-ED-004: Error Handling**
- SHALL handle API errors gracefully
- SHALL log detailed error information
- SHALL handle rate limits
- SHALL provide actionable error messages

### 2.5 Pipeline (Orchestration)

**Purpose:** Coordinate all agents in a unified workflow from configuration.

**Requirements:**

**FR-PL-001: Configuration**
- SHALL load JSON configuration file
- SHALL validate configuration structure
- SHALL support multiple search configurations
- SHALL support optional agent stages
- SHALL provide clear validation errors

**FR-PL-002: Execution Flow**
- SHALL execute agents in sequence:
  1. Gmail Agent (email retrieval)
  2. Analyze Repos Agent (code analysis)
  3. Message Writer Agent (feedback generation)
  4. Email Drafter Agent (draft creation)
- SHALL skip optional stages if not configured
- SHALL support skip-on-error mode
- SHALL support stop-on-error mode

**FR-PL-003: Progress Reporting**
- SHALL display progress for each stage
- SHALL show success/failure counts
- SHALL show timing information
- SHALL generate optional JSON report

**FR-PL-004: Report Generation**
- SHALL generate JSON execution report
- SHALL include timestamp, counts, durations
- SHALL include per-search results
- SHALL support custom report filenames

---

## 3. Non-Functional Requirements

### 3.1 Performance

**NFR-PERF-001: Throughput**
- SHALL process at least 50 emails per minute
- SHALL clone 5 repositories concurrently
- SHALL analyze 10 repositories per minute
- SHALL create 20 drafts per minute

**NFR-PERF-002: Resource Usage**
- SHALL limit concurrent git operations to 5
- SHALL use shallow clones to minimize disk usage
- SHALL clean up temporary files after analysis
- SHALL rotate logs to prevent unlimited growth

**NFR-PERF-003: Scalability**
- SHALL handle up to 500 emails per execution
- SHALL handle up to 1000 repositories per analysis
- SHALL support repositories up to 100MB
- SHALL handle files up to 10,000 lines

### 3.2 Reliability

**NFR-REL-001: Error Recovery**
- SHALL continue pipeline on individual agent failures
- SHALL provide detailed error context
- SHALL log all errors for troubleshooting
- SHALL maintain data integrity on failures

**NFR-REL-002: Data Integrity**
- SHALL preserve all input data in outputs
- SHALL validate Excel file structure
- SHALL handle corrupt Excel files gracefully
- SHALL use UTF-8 encoding throughout

**NFR-REL-003: Token Management**
- SHALL refresh expired tokens automatically
- SHALL handle token revocation gracefully
- SHALL separate tokens by scope requirements
- SHALL prompt for re-authentication when needed

### 3.3 Usability

**NFR-USE-001: Command Line Interface**
- SHALL provide clear command-line arguments
- SHALL provide help documentation (--help)
- SHALL show progress during execution
- SHALL use colored/formatted output for readability

**NFR-USE-002: Configuration**
- SHALL use JSON for configuration (human-readable)
- SHALL provide example configuration files
- SHALL validate configuration on load
- SHALL provide clear error messages for invalid config

**NFR-USE-003: Documentation**
- SHALL provide README with setup instructions
- SHALL provide agent-specific documentation
- SHALL provide quick start guide
- SHALL provide troubleshooting guide
- SHALL document all configuration options

### 3.4 Security

**NFR-SEC-001: Credentials Management**
- SHALL NOT store passwords in code
- SHALL use OAuth 2.0 for authentication
- SHALL store tokens securely
- SHALL exclude credentials from version control
- SHALL use read-only scope where possible

**NFR-SEC-002: Data Privacy**
- SHALL NOT log email content bodies
- SHALL NOT log passwords or tokens
- SHALL NOT transmit data to third parties
- SHALL respect Gmail API terms of service

**NFR-SEC-003: API Permissions**
- SHALL request minimum necessary scopes
- SHALL separate scopes by agent (readonly vs compose)
- SHALL NOT send emails without user review
- SHALL create drafts only (no auto-send)

### 3.5 Logging and Monitoring

**NFR-LOG-001: Comprehensive Logging**
- SHALL log all major operations (start/end)
- SHALL log all errors with full stack traces
- SHALL log progress for long operations
- SHALL use structured logging format

**NFR-LOG-002: Log Rotation**
- SHALL rotate logs at 10MB per file
- SHALL keep 5 backup log files
- SHALL prevent unlimited disk usage
- SHALL support manual log cleanup

**NFR-LOG-003: Log Levels**
- SHALL support DEBUG, INFO, WARNING, ERROR levels
- SHALL log DEBUG+ to files
- SHALL log WARNING+ to console
- SHALL provide session IDs for tracing

**NFR-LOG-004: Log Organization**
- SHALL create separate log per agent
- SHALL create unified pipeline log
- SHALL organize logs in Logs/ directory
- SHALL use UTF-8 encoding for international characters

### 3.6 Maintainability

**NFR-MAIN-001: Code Quality**
- SHALL use modular, object-oriented design
- SHALL provide clear function/method documentation
- SHALL use meaningful variable names
- SHALL follow Python PEP 8 style guidelines

**NFR-MAIN-002: Testing**
- SHALL provide test scripts for verification
- SHALL support dry-run modes
- SHALL validate inputs before processing
- SHALL provide example configurations

**NFR-MAIN-003: Extensibility**
- SHALL support custom message styles (via code modification)
- SHALL support configurable thresholds
- SHALL support additional Excel columns
- SHALL support new Gmail search operators

---

## 4. System Architecture

### 4.1 Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         Pipeline                            │
│                    (Orchestration Layer)                    │
└─────────────────────────────────────────────────────────────┘
           │              │              │              │
           ▼              ▼              ▼              ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │  Gmail   │    │ Analyze  │    │ Message  │    │  Email   │
    │  Agent   │──▶│  Repos    │──▶│  Writer  │──▶│ Drafter  │
    └──────────┘    └──────────┘    └──────────┘    └──────────┘
         │              │                │               │
         ▼              ▼                ▼               ▼
    Output_12       Output_23        Output_34         Gmail
      .xlsx           .xlsx            .xlsx           Drafts
```

### 4.2 Data Flow

1. **Input**: Gmail search query + configuration
2. **Stage 1**: Gmail Agent → Output_12.xlsx (emails + URLs)
3. **Stage 2**: Analyze Repos → Output_23.xlsx (metrics + grades)
4. **Stage 3**: Message Writer → Output_34.xlsx (+ feedback messages)
5. **Stage 4**: Email Drafter → Gmail Drafts (ready to send)

### 4.3 Technology Stack

- **Language**: Python 3.7+
- **Gmail API**: google-api-python-client
- **Excel**: openpyxl
- **Git**: subprocess + git CLI
- **Async**: asyncio for concurrent operations
- **Logging**: Python logging + RotatingFileHandler
- **Auth**: OAuth 2.0 via google-auth-oauthlib

---

## 5. User Workflows

### 5.1 Primary Workflow: Grade Student Assignments

**Actor:** Teaching Assistant

**Preconditions:**
- Students submitted repositories via email
- Gmail API credentials configured
- OAuth consent screen configured

**Steps:**
1. Configure search query in config.json (e.g., "label:homework")
2. Run pipeline: `python pipeline.py --config config.json`
3. Pipeline retrieves emails with repository links
4. Pipeline clones and analyzes each repository
5. Pipeline generates personalized feedback based on grades
6. Pipeline creates Gmail drafts for each student
7. TA reviews drafts in Gmail
8. TA customizes messages if needed
9. TA sends drafts to students

**Success Criteria:**
- All repositories analyzed successfully
- Grades calculated correctly
- Feedback messages generated in appropriate styles
- Drafts ready for review in Gmail Drafts

**Alternative Flows:**
- Some repositories fail to clone → Continue with others, log failures
- Some emails have no URL → Skip, log warning
- API rate limit hit → Back off, retry

### 5.2 Secondary Workflow: Code Review Automation

**Actor:** Engineering Manager

**Preconditions:**
- Team submits repositories via email or notification
- Manager wants quick quality assessment

**Steps:**
1. Configure search for team submissions
2. Run pipeline to analyze all repositories
3. Review grades in Output_23.xlsx
4. Filter for low-scoring repositories
5. Focus manual review on problem areas
6. Send automated feedback to high-scorers
7. Schedule 1-on-1 for low-scorers

---

## 6. Configuration Specification

### 6.1 Configuration File Format (JSON)

```json
{
  "credentials_file": "credentials.json",
  "searches": [
    {
      "name": "Search Name",
      "query": "Gmail search query",
      "output": "output_file.xlsx",
      "max_results": 100
    }
  ],
  "analyze_repos": {
    "input_file": "output_file.xlsx",
    "output_file": "analyzed.xlsx",
    "temp_dir": "TempFiles",
    "cleanup": true,
    "small_file_threshold": 150
  },
  "generate_messages": {
    "input_file": "analyzed.xlsx",
    "output_file": "with_feedback.xlsx"
  },
  "draft_emails": {
    "input_file": "with_feedback.xlsx",
    "credentials_file": "credentials.json"
  }
}
```

### 6.2 Configuration Parameters

**Global:**
- `credentials_file`: Path to OAuth credentials (default: credentials.json)

**Searches (array):**
- `name`: Descriptive name (optional)
- `query`: Gmail search query (required)
- `output`: Output filename (optional, defaults to search_N.xlsx)
- `max_results`: Max emails to retrieve (optional, default: 100)

**Analyze Repos (optional object):**
- `input_file`: Excel with GitHub URLs (required)
- `output_file`: Output filename (optional, default: Output_23.xlsx)
- `temp_dir`: Clone directory (optional, default: TempFiles)
- `cleanup`: Remove clones after (optional, default: true)
- `small_file_threshold`: Max lines for "small" (optional, default: 150)

**Generate Messages (optional object):**
- `input_file`: Excel with grades (required)
- `output_file`: Output filename (optional, default: Output_34.xlsx)

**Draft Emails (optional object):**
- `input_file`: Excel with feedback (required)
- `credentials_file`: OAuth credentials (optional, default: credentials.json)

---

## 7. Output Specifications

### 7.1 Output_12.xlsx (Gmail Agent Output)

**Columns:**
1. ID (Text) - Gmail message ID
2. TimeStamp (DateTime) - Email received timestamp
3. Subject (Text) - Email subject line
4. Search Criteria (Text) - Query used
5. github Repo URL (Text) - Extracted GitHub URL or empty

**Formatting:**
- Headers: Bold, blue background (#4472C4)
- Column widths: Auto-adjusted
- Encoding: UTF-8

### 7.2 Output_23.xlsx (Analyze Repos Output)

**Columns:** All from Output_12.xlsx plus:
6. Total Lines (Number) - Total lines in repository
7. Lines in Small Files (<N) (Number) - Lines in files below threshold
8. Grade (%) (Number) - Modularity percentage

**Calculations:**
- Grade = (Lines in Small Files / Total Lines) × 100
- Higher grade = more modular codebase

### 7.3 Output_34.xlsx (Message Writer Output)

**Columns:** All from Output_23.xlsx plus:
9. Feedback Message (Text, wrapped) - Personalized feedback

**Formatting:**
- Feedback Message column: Width 100, text wrapping enabled
- Vertical alignment: Top

### 7.4 Gmail Drafts (Email Drafter Output)

**Format:**
- Subject: "Feedback message to [ID]"
- Body: Complete feedback message (plain text)
- Recipients: Empty (to be filled by user)
- Status: Draft (not sent)

---

## 8. Success Metrics

### 8.1 Quantitative Metrics

- **Processing Speed**: 50+ emails/minute
- **Analysis Throughput**: 10+ repositories/minute
- **Success Rate**: >95% of operations succeed
- **Uptime**: System available when user runs it
- **Error Recovery**: <5% unrecoverable errors

### 8.2 Qualitative Metrics

- **User Satisfaction**: Feedback is engaging and helpful
- **Time Savings**: 90% reduction in manual grading time
- **Consistency**: All submissions evaluated with same criteria
- **Transparency**: Clear audit trail for all operations

---

## 9. Constraints and Assumptions

### 9.1 Constraints

- **Gmail API Quotas**: 250 units per second per user, 25,000 per day
- **Draft Creation**: 100 units per draft = ~250 drafts/day limit
- **Git Operations**: Dependent on network speed and repository size
- **Disk Space**: Temporary storage required for cloned repositories
- **Python Version**: Requires Python 3.7+

### 9.2 Assumptions

- Users have Gmail accounts
- Users can create Google Cloud projects
- Users can configure OAuth consent screens
- GitHub repositories are publicly accessible (or user has access)
- Git is installed and available in PATH
- Users have sufficient disk space for temporary clones

---

## 10. Dependencies

### 10.1 External Dependencies

**Python Packages:**
- google-auth-oauthlib (2.0.0+)
- google-auth-httplib2 (0.1.0+)
- google-api-python-client (2.0.0+)
- openpyxl (3.0.0+)
- python-dateutil (2.8.0+)

**System Dependencies:**
- Git (2.0+)
- Python (3.7+)
- Internet connection

**External Services:**
- Gmail API
- Google OAuth 2.0
- GitHub (for repository access)

### 10.2 Internal Dependencies

- Each agent depends on the output of the previous agent
- Pipeline coordinates all agents
- Logger configuration shared across all agents
- Configuration file required for pipeline

---

## 11. Future Enhancements

### 11.1 Planned Features (Not in Current Release)

**P1 - High Priority:**
- Email recipient extraction and auto-population in drafts
- Support for private repositories with SSH keys
- Configurable message templates via JSON (no code changes)
- Web dashboard for monitoring executions
- Support for additional email providers (Outlook, etc.)

**P2 - Medium Priority:**
- HTML email templates with styling
- Attachment support in drafts
- Scheduled pipeline execution (cron integration)
- Real-time progress bar for long operations
- Database storage for historical results

**P3 - Low Priority:**
- Machine learning for grade prediction
- Custom code quality rules beyond modularity
- Integration with GitHub API for direct repository access
- Slack/Teams notifications
- Multi-language support for feedback messages

### 11.2 Known Limitations

1. **Single Gmail Account**: Pipeline works with one Gmail account at a time
2. **Public Repositories**: Best support for public GitHub repositories
3. **Synchronous Pipeline**: Agents run sequentially, not in parallel
4. **Manual Sending**: Drafts must be manually reviewed and sent
5. **Fixed Styles**: Message styles hardcoded, require code changes to modify

---

## 12. Compliance and Legal

### 12.1 Data Privacy

- System processes email metadata and repository content
- No data transmitted to third parties except Gmail API and GitHub
- Users responsible for compliance with local data protection laws
- Suitable for FERPA compliance (educational records)

### 12.2 Terms of Service

- Must comply with Gmail API Terms of Service
- Must comply with GitHub Terms of Service
- OAuth consent screen must accurately describe application
- No automated mass mailing (drafts only, manual sending)

### 12.3 License

- Open source, available for personal and educational use
- No warranty provided
- User responsible for proper use and configuration

---

## 13. Support and Maintenance

### 13.1 Documentation

- README.md - Complete system documentation
- Agent-specific READMEs (4 files)
- LOGGING_README.md - Logging system documentation
- QUICK_START.md - Quick reference guide
- PROMPTS.md - Development history
- This PRD

### 13.2 Troubleshooting

- Comprehensive troubleshooting sections in each README
- Detailed error logging to Logs/ directory
- Test scripts for verification
- GitHub repository for issues (if applicable)

### 13.3 Updates

- Semantic versioning for releases
- Changelog for version history
- Migration guides for breaking changes
- Backward compatibility where possible

---

## 14. Glossary

- **Agent**: Independent module performing specific task (Gmail, Analyze, Message Writer, Email Drafter)
- **Pipeline**: Orchestration system coordinating all agents
- **Grade**: Code modularity percentage (0-100%)
- **Small File**: File with lines below threshold (default: 150)
- **Scope**: OAuth permission level (gmail.readonly, gmail.compose)
- **Token**: Saved authentication credential
- **Draft**: Unsent email message in Gmail
- **Repository**: Git repository on GitHub
- **Modularity**: Measure of code organization (higher = more small files)

---

## Appendix A: Configuration Examples

See `config.json.example` for comprehensive configuration examples.

## Appendix B: Error Codes

See agent-specific README files for detailed error documentation.

## Appendix C: API Reference

See inline code documentation and README files.

---

**Document History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11 | System | Initial PRD creation |

**Approval:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner | | | |
| Technical Lead | | | |
| Stakeholder | | | |
