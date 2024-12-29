# Git Summary

A command-line tool that generates concise, AI-powered summaries of your recent git commits.

## Features

- Fetches git commits from the last 24 hours
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
./git_summary.py
```

The tool will:
1. Fetch all commits from the last 24 hours
2. Analyze the commits and their changes
3. Generate a concise summary using OpenAI's API
4. Output the summary in markdown format

## Example Output

```markdown
Changelog Summary:

- Implemented user authentication system with OAuth2
- Fixed critical bug in data processing pipeline
- Added new dashboard features for monitoring
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

## License

[MIT License](LICENSE) 