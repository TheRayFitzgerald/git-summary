#!/usr/bin/env python3
from datetime import datetime, timedelta
import subprocess
import json
from openai import OpenAI
import os


def get_recent_commits(hours=24):
    """Get commits from the last n hours."""
    since_date = (datetime.now() - timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")

    # Get commit hashes and messages
    git_log = subprocess.run(
        [
            "git",
            "log",
            f'--since="{since_date}"',
            "--pretty=format:%H|||%s|||%at",  # hash, message, timestamp
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
    # Get the files changed in this commit
    diff = subprocess.run(
        [
            "git",
            "show",
            '--pretty=format:""',  # No commit message
            "--patch",  # Show the actual changes
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
    """Generate a summary using OpenAI API."""
    client = OpenAI()

    # Format the prompt with structured commit data
    prompt = f"""Analyze these git commits and create a concise changelog summary.
Focus on the key changes and their impact. Format the response as a markdown list.

Commit data:
{json.dumps(commits, indent=2)}
"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a technical writer creating a changelog summary.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {str(e)}"


def main():
    # Ensure we're in a git repository
    if not os.path.exists(".git"):
        print("Error: Not a git repository")
        return

    # Get and format commit data
    recent_commits = get_recent_commits()
    if not recent_commits:
        print("No commits found in the last 24 hours")
        return

    formatted_commits = format_commit_data(recent_commits)

    # Generate and print summary
    summary = generate_summary(formatted_commits)
    print("\nChangelog Summary:\n")
    print(summary)


if __name__ == "__main__":
    main()
