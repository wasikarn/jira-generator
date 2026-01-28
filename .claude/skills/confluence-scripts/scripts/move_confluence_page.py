#!/usr/bin/env python3
"""
Move Confluence Page to a new parent

This script moves a Confluence page to be a child of another page
without modifying the page content.

Example usage:
    python move_confluence_page.py --page-id 144244902 --parent-id 153518083
    python move_confluence_page.py --page-id 144244902 --parent-id 153518083 --dry-run
"""

import urllib.request
import urllib.error
import json
import base64
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
    """Get Confluence page details"""
    url = f"{CONFLUENCE_URL}/rest/api/content/{page_id}?expand=ancestors,version"

    req = urllib.request.Request(url)
    req.add_header("Authorization", get_auth_header())
    req.add_header("Content-Type", "application/json")

    with urllib.request.urlopen(req, context=ssl_context) as response:
        return json.loads(response.read().decode())

def move_page(page_id, parent_id):
    """
    Move a page to be a child of another page

    Uses the move API: POST /wiki/rest/api/content/{id}/move/{position}/{targetId}
    position can be: append, prepend, before, after
    """
    url = f"{CONFLUENCE_URL}/rest/api/content/{page_id}/move/append/{parent_id}"

    req = urllib.request.Request(url, method="PUT")
    req.add_header("Authorization", get_auth_header())
    req.add_header("Content-Type", "application/json")
    req.data = b'{}'  # Empty body required

    with urllib.request.urlopen(req, context=ssl_context) as response:
        return json.loads(response.read().decode())

def main():
    parser = argparse.ArgumentParser(
        description='Move Confluence page to a new parent',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Move page to be child of another page
  python move_confluence_page.py --page-id 144244902 --parent-id 153518083

  # Dry run (preview only)
  python move_confluence_page.py --page-id 144244902 --parent-id 153518083 --dry-run

  # Batch move multiple pages
  python move_confluence_page.py --page-ids 144244902,144015541,144015575 --parent-id 153518083
        """
    )

    parser.add_argument('--page-id', help='Single page ID to move')
    parser.add_argument('--page-ids', help='Comma-separated list of page IDs to move')
    parser.add_argument('--parent-id', required=True, help='Target parent page ID')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying')

    args = parser.parse_args()

    # Get list of pages to move
    if args.page_ids:
        page_ids = [p.strip() for p in args.page_ids.split(',')]
    elif args.page_id:
        page_ids = [args.page_id]
    else:
        print("Error: Specify --page-id or --page-ids")
        return 1

    # Get parent page info
    try:
        parent = get_page(args.parent_id)
        print(f"\n📁 Target Parent: {parent['title']} (ID: {args.parent_id})")
    except Exception as e:
        print(f"❌ Error getting parent page: {e}")
        return 1

    print(f"\n{'='*60}")
    print(f"Moving {len(page_ids)} page(s) to parent: {parent['title']}")
    print('='*60)

    success_count = 0
    fail_count = 0

    for page_id in page_ids:
        try:
            # Get page info
            page = get_page(page_id)
            title = page['title']
            current_parent = page.get('ancestors', [{}])[-1].get('title', 'Root') if page.get('ancestors') else 'Root'

            print(f"\n📄 {title}")
            print(f"   ID: {page_id}")
            print(f"   Current parent: {current_parent}")
            print(f"   → New parent: {parent['title']}")

            if args.dry_run:
                print("   🔍 DRY RUN - no changes applied")
                success_count += 1
                continue

            # Move the page
            result = move_page(page_id, args.parent_id)
            print(f"   ✅ Moved successfully")
            success_count += 1

        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            print(f"   ❌ HTTP Error: {e.code} - {e.reason}")
            print(f"      Details: {error_body[:200]}")
            fail_count += 1
        except Exception as e:
            print(f"   ❌ Error: {e}")
            fail_count += 1

    print(f"\n{'='*60}")
    print(f"Summary: {success_count} succeeded, {fail_count} failed")
    print('='*60)

    return 0 if fail_count == 0 else 1

if __name__ == "__main__":
    exit(main())
