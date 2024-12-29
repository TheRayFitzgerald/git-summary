#!/usr/bin/env python3
from datetime import datetime, timedelta
import subprocess
import json
import os
import argparse


def get_commits_for_day(date):
    """Get commits for a specific day."""
    start_date = date.strftime("%Y-%m-%d 00:00:00")
    end_date = (date + timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")

    git_log = subprocess.run(
        [
            "git",
            "log",
            f'--since="{start_date}"',
            f'--until="{end_date}"',
            "--pretty=format:%H|||%s|||%at",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    return [
        commit.split("|||") for commit in git_log.stdout.strip().split("\n") if commit
    ]


def get_commit_changes(commit_hash):
    """Get the actual file changes for a commit."""
    diff = subprocess.run(
        [
            "git",
            "show",
            '--pretty=format:""',
            "--patch",
            commit_hash,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    return diff.stdout.strip()


def format_commit_data(commits):
    """Format commit data into a structured format."""
    formatted_commits = []

    for commit_hash, message, timestamp in commits:
        changes = get_commit_changes(commit_hash)
        commit_data = {
            "hash": commit_hash,
            "message": message,
            "timestamp": datetime.fromtimestamp(int(timestamp)).isoformat(),
            "changes": changes,
        }
        formatted_commits.append(commit_data)

    return formatted_commits


def generate_summary(commits):
    """Generate a summary using OpenAI API via curl."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "Error: OPENAI_API_KEY environment variable not set"

    messages = [
        {
            "role": "system",
            "content": "You are a technical writer creating a changelog summary.",
        },
        {
            "role": "user",
            "content": f"""Analyze these git commits and create a concise changelog summary.
            Focus on the key changes and their impact. Format the response as a markdown list.

            Commit data:
            {json.dumps(commits, indent=2)}
            """,
        },
    ]

    curl_data = {"model": "gpt-4o-mini", "messages": messages}

    try:
        curl_process = subprocess.run(
            [
                "curl",
                "https://api.openai.com/v1/chat/completions",
                "-H",
                "Content-Type: application/json",
                "-H",
                f"Authorization: Bearer {api_key}",
                "-d",
                json.dumps(curl_data),
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        response = json.loads(curl_process.stdout)
        return response["choices"][0]["message"]["content"]
    except subprocess.CalledProcessError as e:
        return f"Error executing curl command: {str(e)}"
    except json.JSONDecodeError as e:
        return f"Error parsing API response: {str(e)}"
    except Exception as e:
        return f"Error generating summary: {str(e)}"


def main():
    parser = argparse.ArgumentParser(description="Generate git commit summaries")
    parser.add_argument(
        "--days",
        type=int,
        default=1,
        help="Number of days to analyze (default: 1)",
    )
    args = parser.parse_args()

    if not os.path.exists(".git"):
        print("Error: Not a git repository")
        return

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    for day_offset in range(args.days):
        target_date = today - timedelta(days=day_offset)
        commits = get_commits_for_day(target_date)
        
        if not commits:
            print(f"\nNo commits found for {target_date.date()}")
            continue
            
        print(f"\nChangelog Summary for {target_date.date()}:\n")
        formatted_commits = format_commit_data(commits)
        summary = generate_summary(formatted_commits)
        print(summary)
        print("\n" + "-" * 50)  # Separator between days


if __name__ == "__main__":
    main()
