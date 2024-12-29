# Git Summary

A command-line tool that generates concise, AI-powered summaries of your recent git commits.

## Features

- Generates day-by-day summaries of git commits
- Supports analyzing multiple days of commit history
- Analyzes commit messages and changes
- Generates a human-readable changelog using OpenAI's GPT model
- Outputs the summary in markdown format

## Prerequisites

- Python 3.x
- Git repository
- OpenAI API key

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/git-summary.git
cd git-summary
```

2. Make the script executable:
```bash
chmod +x git_summary.py
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Usage

Run the script from within any git repository:

```bash
# Default: summarize last 24 hours
./git_summary.py

# Summarize the last 7 days
./git_summary.py --days 7
```

The tool will:
1. Process commits day by day for the specified time period
2. Analyze the commits and their changes for each day
3. Generate a concise summary using OpenAI's API
4. Output daily summaries in markdown format

## Example Output

```markdown
Changelog Summary for 2024-01-20:

- Implemented user authentication system with OAuth2
- Fixed critical bug in data processing pipeline
- Added new dashboard features for monitoring

--------------------------------------------------

Changelog Summary for 2024-01-19:

- Updated dependencies to latest versions
- Improved error handling in API endpoints
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

## License

[MIT License](LICENSE) 