#!/usr/bin/env python3
"""
Generate HelloGitHub monthly content markdown files.

This script helps automate the creation of new monthly issue files
for the HelloGitHub project, pulling project data from GitHub issues
and formatting them into the standard markdown template.

Usage:
    python scripts/generate_content.py --issue 102
    python scripts/generate_content.py --issue 102 --lang en
"""

import argparse
import os
import re
from datetime import datetime
from pathlib import Path

# Directory where content files are stored
CONTENT_DIR = Path(__file__).parent.parent / "content"

# Supported languages and their file suffixes
LANGUAGES = {
    "cn": "",
    "en": "_en",
}

# Category labels used in HelloGitHub issues
CATEGORIES = [
    "C 项目",
    "C# 项目",
    "C++ 项目",
    "Go 项目",
    "Java 项目",
    "JavaScript 项目",
    "Kotlin 项目",
    "Python 项目",
    "Rust 项目",
    "Swift 项目",
    "其它",
    "开源书籍",
]


def get_issue_number() -> int:
    """Determine the next issue number based on existing content files."""
    existing = sorted(CONTENT_DIR.glob("HelloGitHub*.md"))
    if not existing:
        return 1
    last_file = existing[-1].stem  # e.g. 'HelloGitHub101'
    match = re.search(r"(\d+)", last_file)
    if match:
        return int(match.group(1)) + 1
    return 1


def generate_header(issue_num: int) -> str:
    """Generate the markdown header for a new issue."""
    now = datetime.now()
    # Use %-m on Linux/Mac to avoid zero-padded month; falls back gracefully
    month_str = now.strftime("%Y 年 %m 月")
    return (
        f"# 《HelloGitHub》第 {issue_num} 期\n"
        f"> 兴趣是最好的老师，**HelloGitHub** 让你对开源感兴趣！\n"
        f"\n"
        f"<p align=\"center\">\n"
        f"    <img src='https://raw.githubusercontent.com/521xueweihan/img_logo/master/logo/cover.jpg' style=\"max-width:100%;\"/>\n"
        f"</p>\n"
        f"\n"
        f"## 目录\n"
        f"\n"
        f"点击右上角的 **「目录」** 图标打开目录，获得更好的阅读体验。\n"
        f"\n"
        f"![](https://raw.githubusercontent.com/521xueweihan/img_logo/master/logo/catalog.jpeg)\n"
        f"\n"
        f"**Tips**：如果遇到图片刷不出来的情况，[点击](https://hellogithub.com/periodical/volume/{issue_num:02d}) 换一种浏览方式。\n"
        f"\n"
        f"<p align=\"center\">\n"
        f"  <img src=\"https://github.com/521xueweihan/HelloGitHub/assets/1rc3w9c/2eda1e3f-b2b2-423f-b952-d3a3b2a3e0e9\" style=\"max-width:100%\" />\n"
        f"</p>\n"
        f"\n"
        f"---\n"
        f"\n"
    )


def generate_category_section(category: str) -> str:
    """Generate a placeholder section for a given category."""
    return f"### {category}\n\n"


def create_content_file(issue_num: int, lang: str = "cn") -> Path:
    """
    Create a new content markdown file for the given issue number.

    Args:
        issue_num: The issue number to generate.
        lang: Language code ('cn' or 'en'). Defaults to 'cn'.

    Returns:
        Path to the created file.

    Raises:
        ValueError: If an unsupported language code is provided.
    """
    if lang not in LANGUAGES:
        raise ValueError(f"Unsupported language '{lang}'. Choose from: {list(LANGUAGES.keys())}")

    suffix = LANGUAGES.get(lang, "")
    filename = CONTENT_DIR / f"HelloGitHub{issue_num:03d}{suffix}.md"

    if filename.exists():
        print(f"[!] File already exists: {