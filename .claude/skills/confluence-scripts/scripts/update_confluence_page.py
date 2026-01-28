#!/usr/bin/env python3
"""
Generic Confluence Page Updater using REST API
Used for updating page content with find/replace operations

Example usage:
    python update_confluence_page.py --page-id 154730498 --find "5 นาที" --replace "3 นาที"
    python update_confluence_page.py --page-id 154730498 --find "300" --replace "180" --dry-run
"""

import urllib.request
import urllib.error
import json
import base64
import re
import ssl
import argparse
from pathlib import Path

# Create SSL context that doesn't verify certificates (for macOS)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Load credentials from .env file
def load_credentials():
    """Load Atlassian credentials from ~/.config/atlassian/.env"""
    env_path = Path.home() / ".config/atlassian/.env"
    creds = {}
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                creds[key] = value
    return creds

creds = load_credentials()
CONFLUENCE_URL = creds['CONFLUENCE_URL']
USERNAME = creds['CONFLUENCE_USERNAME']
API_TOKEN = creds['CONFLUENCE_API_TOKEN']

def get_auth_header():
    """Create Basic Auth header"""
    auth_string = f"{USERNAME}:{API_TOKEN}"
    auth_bytes = base64.b64encode(auth_string.encode()).decode()
    return f"Basic {auth_bytes}"

def get_page(page_id):
    """Get Confluence page content"""
    url = f"{CONFLUENCE_URL}/rest/api/content/{page_id}?expand=body.storage,version"

    req = urllib.request.Request(url)
    req.add_header("Authorization", get_auth_header())
    req.add_header("Content-Type", "application/json")

    with urllib.request.urlopen(req, context=ssl_context) as response:
        return json.loads(response.read().decode())

def update_page(page_id, title, content, version):
    """Update Confluence page content"""
    url = f"{CONFLUENCE_URL}/rest/api/content/{page_id}"

    data = {
        "id": page_id,
        "type": "page",
        "title": title,
        "body": {
            "storage": {
                "value": content,
                "representation": "storage"
            }
        },
        "version": {
            "number": version + 1
        }
    }

    req = urllib.request.Request(url, method="PUT")
    req.add_header("Authorization", get_auth_header())
    req.add_header("Content-Type", "application/json")
    req.data = json.dumps(data).encode()

    with urllib.request.urlopen(req, context=ssl_context) as response:
        return json.loads(response.read().decode())

def find_and_replace(content, find_text, replace_text, use_regex=False):
    """
    Find and replace text in content
    Returns: (new_content, count)
    """
    if use_regex:
        pattern = re.compile(find_text)
        new_content, count = pattern.subn(replace_text, content)
    else:
        count = content.count(find_text)
        new_content = content.replace(find_text, replace_text)

    return new_content, count

def process_page(page_id, replacements, dry_run=False):
    """
    Process a single page with multiple find/replace operations

    Args:
        page_id: Confluence page ID
        replacements: List of (find, replace, use_regex) tuples
        dry_run: If True, only show what would be changed
    """
    print(f"\n{'='*60}")
    print(f"Processing page ID: {page_id}")
    print('='*60)

    try:
        # Get current page
        page = get_page(page_id)
        title = page['title']
        current_content = page['body']['storage']['value']
        version = page['version']['number']

        print(f"Title: {title}")
        print(f"Current version: {version}")

        # Apply all replacements
        new_content = current_content
        total_changes = 0

        for find_text, replace_text, use_regex in replacements:
            new_content, count = find_and_replace(new_content, find_text, replace_text, use_regex)
            if count > 0:
                print(f"  '{find_text}' → '{replace_text}': {count} replacement(s)")
                total_changes += count

        if total_changes == 0:
            print("No matches found - no changes needed")
            return False

        print(f"Total changes: {total_changes}")

        if dry_run:
            print("🔍 DRY RUN - no changes applied")
            return True

        # Update page
        result = update_page(page_id, title, new_content, version)
        print(f"✅ Updated to version {result['version']['number']}")

        return True

    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        error_body = e.read().decode()
        print(f"Details: {error_body[:500]}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Update Confluence page content with find/replace operations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Simple text replacement
  python update_confluence_page.py --page-id 154730498 --find "5 นาที" --replace "3 นาที"

  # Multiple replacements
  python update_confluence_page.py --page-id 154730498 \\
    --find "5 minutes" --replace "3 minutes" \\
    --find "300" --replace "180"

  # Dry run (preview changes)
  python update_confluence_page.py --page-id 154730498 --find "old" --replace "new" --dry-run

  # Regex replacement
  python update_confluence_page.py --page-id 154730498 --find "v\\d+\\.\\d+" --replace "v2.0" --regex
        """
    )

    parser.add_argument('--page-id', required=True, help='Confluence page ID')
    parser.add_argument('--find', action='append', required=True, help='Text to find (can specify multiple)')
    parser.add_argument('--replace', action='append', required=True, help='Replacement text (must match --find count)')
    parser.add_argument('--regex', action='store_true', help='Treat find patterns as regex')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying')

    args = parser.parse_args()

    if len(args.find) != len(args.replace):
        print("Error: Number of --find and --replace arguments must match")
        return 1

    # Build replacements list
    replacements = [(f, r, args.regex) for f, r in zip(args.find, args.replace)]

    # Process page
    success = process_page(args.page_id, replacements, args.dry_run)

    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
