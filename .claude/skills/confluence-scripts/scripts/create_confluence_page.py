#!/usr/bin/env python3
"""
Create or Update Confluence Page with proper code block formatting

This script converts markdown to Confluence storage format with proper
<ac:structured-macro> tags for code blocks.

Example usage:
    # Create new page
    python create_confluence_page.py --space BEP --title "My Page" --content-file content.md

    # Create as child of parent page
    python create_confluence_page.py --space BEP --title "My Page" --parent-id 123456 --content-file content.md

    # Update existing page
    python create_confluence_page.py --page-id 123456 --content-file content.md

    # Update with inline content
    python create_confluence_page.py --page-id 123456 --content "# Hello World"
"""

import urllib.request
import urllib.error
import json
import base64
import re
import ssl
import argparse
import html
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
    url = f"{CONFLUENCE_URL}/rest/api/content/{page_id}?expand=body.storage,version,space"

    req = urllib.request.Request(url)
    req.add_header("Authorization", get_auth_header())
    req.add_header("Content-Type", "application/json")

    with urllib.request.urlopen(req, context=ssl_context) as response:
        return json.loads(response.read().decode())

def create_page(space_key, title, content, parent_id=None):
    """Create new Confluence page"""
    url = f"{CONFLUENCE_URL}/rest/api/content"

    data = {
        "type": "page",
        "title": title,
        "space": {"key": space_key},
        "body": {
            "storage": {
                "value": content,
                "representation": "storage"
            }
        }
    }

    if parent_id:
        data["ancestors"] = [{"id": str(parent_id)}]

    req = urllib.request.Request(url, method="POST")
    req.add_header("Authorization", get_auth_header())
    req.add_header("Content-Type", "application/json")
    req.data = json.dumps(data).encode()

    with urllib.request.urlopen(req, context=ssl_context) as response:
        return json.loads(response.read().decode())

def update_page(page_id, title, content, version):
    """Update existing Confluence page"""
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

def markdown_to_storage(markdown_content):
    """
    Convert markdown to Confluence storage format with proper code blocks

    This is a simplified converter that handles:
    - Headings (# ## ###)
    - Bold (**text**)
    - Italic (*text*)
    - Code blocks (```language)
    - Inline code (`code`)
    - Links [text](url)
    - Lists (- item)
    - Horizontal rules (---)
    - Tables
    - Blockquotes (>)
    """
    lines = markdown_content.split('\n')
    result = []
    in_code_block = False
    code_language = "text"
    code_content = []
    in_list = False
    in_table = False
    table_rows = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Code block start/end
        if line.startswith('```'):
            if not in_code_block:
                # Start code block
                in_code_block = True
                code_language = line[3:].strip() or "text"
                code_content = []
            else:
                # End code block
                in_code_block = False
                code_text = '\n'.join(code_content)
                result.append(create_code_macro(code_language, code_text))
            i += 1
            continue

        if in_code_block:
            code_content.append(line)
            i += 1
            continue

        # Table handling
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_rows = []
            # Skip separator row (|---|---|)
            if re.match(r'^\|[\s\-:|]+\|$', line.strip()):
                i += 1
                continue
            table_rows.append(line)
            i += 1
            continue
        elif in_table:
            # End of table
            in_table = False
            result.append(create_table(table_rows))
            table_rows = []
            # Don't increment i, process this line normally

        # Empty line
        if not line.strip():
            if in_list:
                in_list = False
                result.append('</ul>')
            result.append('')
            i += 1
            continue

        # Horizontal rule
        if line.strip() in ['---', '***', '___']:
            if in_list:
                in_list = False
                result.append('</ul>')
            result.append('<hr/>')
            i += 1
            continue

        # Headings
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading_match:
            if in_list:
                in_list = False
                result.append('</ul>')
            level = len(heading_match.group(1))
            text = convert_inline(heading_match.group(2))
            result.append(f'<h{level}>{text}</h{level}>')
            i += 1
            continue

        # Blockquote
        if line.startswith('>'):
            if in_list:
                in_list = False
                result.append('</ul>')
            quote_text = convert_inline(line[1:].strip())
            result.append(f'<blockquote><p>{quote_text}</p></blockquote>')
            i += 1
            continue

        # Unordered list
        list_match = re.match(r'^[\-\*]\s+(.+)$', line)
        if list_match:
            if not in_list:
                in_list = True
                result.append('<ul>')
            text = convert_inline(list_match.group(1))
            result.append(f'<li>{text}</li>')
            i += 1
            continue

        # Ordered list
        ordered_match = re.match(r'^\d+\.\s+(.+)$', line)
        if ordered_match:
            # For simplicity, treat as unordered
            if not in_list:
                in_list = True
                result.append('<ul>')
            text = convert_inline(ordered_match.group(1))
            result.append(f'<li>{text}</li>')
            i += 1
            continue

        # Regular paragraph
        if in_list:
            in_list = False
            result.append('</ul>')

        text = convert_inline(line)
        if text.strip():
            result.append(f'<p>{text}</p>')

        i += 1

    # Close any open elements
    if in_list:
        result.append('</ul>')
    if in_table and table_rows:
        result.append(create_table(table_rows))

    return '\n'.join(result)

def convert_inline(text):
    """Convert inline markdown elements"""
    # Escape HTML entities first (but not already-escaped ones)
    # text = html.escape(text)  # Skip this to allow HTML passthrough

    # Bold **text**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

    # Italic *text* (but not inside **)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)

    # Inline code `code`
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

    # Links [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)

    return text

def create_code_macro(language, content):
    """Create Confluence code macro"""
    # Map common language aliases
    lang_map = {
        'js': 'javascript',
        'ts': 'typescript',
        'py': 'python',
        'sh': 'bash',
        'shell': 'bash',
        'yml': 'yaml',
        '': 'text'
    }
    language = lang_map.get(language, language)

    return f'''<ac:structured-macro ac:name="code" ac:schema-version="1">
<ac:parameter ac:name="language">{language}</ac:parameter>
<ac:plain-text-body><![CDATA[{content}]]></ac:plain-text-body>
</ac:structured-macro>'''

def create_table(rows):
    """Create HTML table from markdown table rows"""
    if not rows:
        return ''

    result = ['<table>']

    for idx, row in enumerate(rows):
        cells = [c.strip() for c in row.split('|')[1:-1]]  # Remove empty first/last

        result.append('<tr>')
        for cell in cells:
            tag = 'th' if idx == 0 else 'td'
            cell_content = convert_inline(cell)
            result.append(f'<{tag}>{cell_content}</{tag}>')
        result.append('</tr>')

    result.append('</table>')
    return '\n'.join(result)

def main():
    parser = argparse.ArgumentParser(
        description='Create or update Confluence page with proper code formatting',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create new page
  python create_confluence_page.py --space BEP --title "API Spec" --content-file spec.md

  # Create as child page
  python create_confluence_page.py --space BEP --title "Sub Page" --parent-id 123456 --content-file content.md

  # Update existing page
  python create_confluence_page.py --page-id 123456 --content-file updated.md

  # Update with inline content
  python create_confluence_page.py --page-id 123456 --content "# Updated Title"

  # Dry run (preview storage format)
  python create_confluence_page.py --space BEP --title "Test" --content "# Hello" --dry-run
        """
    )

    # Create mode arguments
    parser.add_argument('--space', help='Space key for new page (e.g., BEP)')
    parser.add_argument('--title', help='Page title')
    parser.add_argument('--parent-id', help='Parent page ID for new page')

    # Update mode arguments
    parser.add_argument('--page-id', help='Page ID to update')

    # Content arguments
    parser.add_argument('--content', help='Markdown content (inline)')
    parser.add_argument('--content-file', help='Path to markdown file')

    # Options
    parser.add_argument('--dry-run', action='store_true', help='Preview without saving')

    args = parser.parse_args()

    # Validate arguments
    if args.page_id:
        # Update mode
        mode = 'update'
    elif args.space and args.title:
        # Create mode
        mode = 'create'
    else:
        print("Error: Specify either --page-id (update) or --space and --title (create)")
        return 1

    # Get content
    if args.content_file:
        with open(args.content_file, 'r') as f:
            markdown_content = f.read()
    elif args.content:
        markdown_content = args.content
    else:
        print("Error: Specify --content or --content-file")
        return 1

    # Convert markdown to storage format
    storage_content = markdown_to_storage(markdown_content)

    if args.dry_run:
        print("=" * 60)
        print("DRY RUN - Storage Format Preview:")
        print("=" * 60)
        print(storage_content)
        print("=" * 60)
        return 0

    try:
        if mode == 'create':
            print(f"Creating page: {args.title} in space {args.space}")
            result = create_page(args.space, args.title, storage_content, args.parent_id)
            print(f"✅ Created: {result['title']}")
            print(f"   ID: {result['id']}")
            print(f"   URL: {CONFLUENCE_URL}/pages/viewpage.action?pageId={result['id']}")

        else:  # update
            # Get current page info
            page = get_page(args.page_id)
            title = args.title or page['title']
            version = page['version']['number']

            print(f"Updating page: {title} (ID: {args.page_id})")
            print(f"Current version: {version}")

            result = update_page(args.page_id, title, storage_content, version)
            print(f"✅ Updated to version {result['version']['number']}")
            print(f"   URL: {CONFLUENCE_URL}/pages/viewpage.action?pageId={args.page_id}")

        return 0

    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        error_body = e.read().decode()
        print(f"Details: {error_body[:500]}")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
