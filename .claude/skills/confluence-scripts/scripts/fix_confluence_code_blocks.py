#!/usr/bin/env python3
"""
Script to fix Confluence code blocks from <pre class="highlight"><code>
to proper <ac:structured-macro ac:name="code"> format
"""

import urllib.request
import urllib.error
import json
import base64
import re
import html
import os
import ssl
from pathlib import Path

# Create SSL context that doesn't verify certificates (for macOS)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Load credentials from .env file
def load_credentials():
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

def fix_code_blocks(content):
    """
    Convert <pre class="highlight"><code class="language-xxx">...</code></pre>
    to <ac:structured-macro ac:name="code">...
    """

    def replace_code_block(match):
        lang_class = match.group(1) or ""
        code_content = match.group(2)

        # Extract language from class
        lang_match = re.search(r'language-(\w+)', lang_class)
        if lang_match:
            language = lang_match.group(1)
        else:
            language = "text"

        # Unescape HTML entities in code
        code_content = html.unescape(code_content)

        # Build the Confluence code macro
        macro = f'''<ac:structured-macro ac:name="code" ac:schema-version="1">
<ac:parameter ac:name="language">{language}</ac:parameter>
<ac:plain-text-body><![CDATA[{code_content}]]></ac:plain-text-body>
</ac:structured-macro>'''

        return macro

    # Pattern to match <pre class="highlight"><code class="language-xxx">...</code></pre>
    pattern = r'<pre class="highlight"><code(?: class="([^"]*)")?>(.*?)</code></pre>'

    fixed_content = re.sub(pattern, replace_code_block, content, flags=re.DOTALL)

    return fixed_content

def process_page(page_id, page_name):
    """Process a single page"""
    print(f"\n{'='*60}")
    print(f"Processing: {page_name} (ID: {page_id})")
    print('='*60)

    try:
        # Get current page
        page = get_page(page_id)
        title = page['title']
        current_content = page['body']['storage']['value']
        version = page['version']['number']

        print(f"Title: {title}")
        print(f"Current version: {version}")

        # Check if needs fixing
        if '<pre class="highlight">' in current_content:
            print("Found code blocks that need fixing...")

            # Fix code blocks
            fixed_content = fix_code_blocks(current_content)

            # Count changes
            original_count = current_content.count('<pre class="highlight">')
            fixed_count = fixed_content.count('<ac:structured-macro ac:name="code"')
            print(f"Fixed {original_count} code blocks")

            # Update page
            result = update_page(page_id, title, fixed_content, version)
            print(f"✅ Updated to version {result['version']['number']}")

            return True
        else:
            print("No code blocks need fixing (already using structured macros)")
            return False

    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        error_body = e.read().decode()
        print(f"Details: {error_body[:500]}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function"""
    print("Confluence Code Block Fixer")
    print("="*60)

    # Pages to fix
    pages = [
        ("144244902", "Credit Coupon"),
        ("144015541", "Discount Coupon"),
        ("144015575", "Cashback Coupon"),
        ("143720672", "Coupon Menu"),
    ]

    results = []
    for page_id, page_name in pages:
        success = process_page(page_id, page_name)
        results.append((page_name, success))

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for page_name, success in results:
        status = "✅ Fixed" if success else "⏭️ Skipped (no changes needed)"
        print(f"{page_name}: {status}")

if __name__ == "__main__":
    main()
