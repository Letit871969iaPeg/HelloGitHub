#!/usr/bin/env python3
"""Fetch GitHub issues and extract project submissions for HelloGitHub content generation."""

import os
import json
import re
from typing import Optional
import requests

GITHUB_API_URL = "https://api.github.com"
REPO_OWNER = os.getenv("REPO_OWNER", "521xueweihan")
REPO_NAME = os.getenv("REPO_NAME", "HelloGitHub")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


def get_issues(label: Optional[str] = None, state: str = "open", per_page: int = 30) -> list:
    """Fetch issues from the GitHub repository.

    Args:
        label: Filter issues by label name.
        state: Issue state ('open', 'closed', or 'all').
        per_page: Number of issues per page (max 100).

    Returns:
        List of issue objects from the GitHub API.
    """
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    params = {"state": state, "per_page": per_page}
    if label:
        params["labels"] = label

    response = requests.get(url, headers=HEADERS, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def parse_submission(issue: dict) -> Optional[dict]:
    """Parse a project submission from an issue body.

    Expects the issue body to follow the submit-cn.yaml or submit-en.yaml template.

    Args:
        issue: A GitHub issue object.

    Returns:
        Parsed submission dict or None if parsing fails.
    """
    body = issue.get("body", "") or ""
    submission = {
        "issue_number": issue.get("number"),
        "title": issue.get("title", ""),
        "author": issue.get("user", {}).get("login", ""),
    }

    # Extract fields using markdown heading patterns from the issue template
    field_patterns = {
        "project_name": r"###\s*项目名称[\s\S]*?\n([^\n#]+)",
        "project_url": r"###\s*项目地址[\s\S]*?\n([^\n#]+)",
        "project_description": r"###\s*项目描述[\s\S]*?\n([^\n#]+(?:\n(?!#)[^\n]+)*)",
        "category": r"###\s*项目分类[\s\S]*?\n([^\n#]+)",
        "language": r"###\s*编程语言[\s\S]*?\n([^\n#]+)",
    }

    for field, pattern in field_patterns.items():
        match = re.search(pattern, body, re.MULTILINE)
        if match:
            submission[field] = match.group(1).strip()
        else:
            submission[field] = None

    # Validate required fields
    if not submission.get("project_url"):
        return None

    return submission


def fetch_and_save_submissions(output_path: str = "data/submissions.json", label: str = "待收录") -> list:
    """Fetch submissions from issues and save them to a JSON file.

    Args:
        output_path: Path to save the submissions JSON file.
        label: GitHub label used to filter submission issues.

    Returns:
        List of parsed submission dicts.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"Fetching issues with label '{label}' from {REPO_OWNER}/{REPO_NAME}...")
    issues = get_issues(label=label, state="open")
    print(f"Found {len(issues)} issues.")

    submissions = []
    for issue in issues:
        parsed = parse_submission(issue)
        if parsed:
            submissions.append(parsed)
            print(f"  Parsed #{parsed['issue_number']}: {parsed.get('project_name', 'Unknown')}")
        else:
            print(f"  Skipped #{issue.get('number')}: could not parse submission.")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(submissions, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(submissions)} submissions to {output_path}")
    return submissions


if __name__ == "__main__":
    fetch_and_save_submissions()
