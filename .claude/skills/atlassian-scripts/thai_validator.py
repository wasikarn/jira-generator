#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""X: Thai Transliteration Validator — Check technical term consistency.

Validates that text follows the Thai + English transliteration rules
defined in writing-style.md. Flags inconsistent term usage.

Usage:
    echo '{"text": "สร้าง เอพีไอ endpoint"}' | python3 thai_validator.py
    echo '{"adf": {...}}' | python3 thai_validator.py

Input JSON:
    text: Plain text to validate (optional)
    adf: ADF JSON to extract text from (optional)

Output JSON:
    issues: list of {type, text, suggestion, line}
    score: 0-100 consistency score
    summary: human-readable summary
"""
import json
import re
import sys


# Technical terms that should STAY in English (never transliterate to Thai)
KEEP_ENGLISH = {
    "endpoint", "payload", "validate", "component", "service", "API",
    "route", "model", "schema", "query", "filter", "response", "request",
    "deploy", "commit", "merge", "branch", "push", "pull", "config",
    "token", "session", "cookie", "cache", "middleware", "webhook",
    "callback", "async", "sync", "batch", "queue", "event", "handler",
    "controller", "repository", "entity", "aggregate", "domain",
    "interface", "abstract", "implement", "extend", "module",
    "provider", "consumer", "producer", "subscriber", "publisher",
    "migration", "seed", "fixture", "mock", "stub", "spy",
    "frontend", "backend", "fullstack", "database", "server", "client",
    "staging", "production", "development", "test", "debug",
    "sprint", "backlog", "epic", "story", "task", "subtask", "bug",
}

# Thai transliterations that should be replaced with English
THAI_TO_ENGLISH = {
    r"เอพีไอ": "API",
    r"เซิร์ฟเวอร์": "server",
    r"คอมโพเนนต์": "component",
    r"เอ็นพอยท์|เอ็นด์พอยต์": "endpoint",
    r"เพย์โหลด": "payload",
    r"แวลิเดท|แวลิเดต": "validate",
    r"เซอร์วิส": "service",
    r"โมเดล": "model",
    r"สคีมา": "schema",
    r"คิวรี่|คิวรี": "query",
    r"รีเควส|รีเควสท์": "request",
    r"รีสปอนส์": "response",
    r"ดีพลอย": "deploy",
    r"คอมมิต": "commit",
    r"เมิร์จ": "merge",
    r"แบรนช์": "branch",
    r"โทเคน": "token",
    r"เซสชั่น|เซสชัน": "session",
    r"แคช": "cache",
    r"มิดเดิลแวร์": "middleware",
    r"อีเวนต์|อีเว้นท์": "event",
    r"ฟิลเตอร์": "filter",
    r"เราท์|เราเตอร์": "route",
    r"ไมเกรชั่น|ไมเกรชัน": "migration",
    r"ดาต้าเบส|ดาตาเบส": "database",
}

# Patterns that suggest all-English text (should be Thai + transliteration)
ALL_ENGLISH_PATTERNS = [
    (r"^[A-Za-z\s\d\-_.,;:!?/()]+$", "Line is all English — should use Thai"),
]


def extract_text_from_adf(adf: dict) -> list[str]:
    """Extract text nodes from ADF, preserving structure."""
    texts = []

    def walk(node):
        if isinstance(node, dict):
            if node.get("type") == "text":
                text = node.get("text", "").strip()
                if text:
                    # Skip code marks (file paths, routes)
                    marks = node.get("marks", [])
                    is_code = any(m.get("type") == "code" for m in marks)
                    is_link = any(m.get("type") == "link" for m in marks)
                    if not is_code and not is_link:
                        texts.append(text)
            for child in node.get("content", []):
                walk(child)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(adf)
    return texts


def validate_text(texts: list[str]) -> list[dict]:
    """Validate text segments for transliteration issues."""
    issues = []

    for i, text in enumerate(texts):
        # Skip short texts (labels like "Given:", "When:")
        if len(text) < 5:
            continue

        # Check for Thai transliterations of technical terms
        for thai_pattern, english in THAI_TO_ENGLISH.items():
            matches = re.findall(thai_pattern, text)
            if matches:
                issues.append({
                    "type": "thai_transliteration",
                    "text": matches[0],
                    "suggestion": f"Use '{english}' instead of Thai transliteration",
                    "line": i + 1,
                    "severity": "warning",
                })

        # Check for all-English lines in non-code context
        # Skip lines that are labels, headings, or short phrases
        if len(text) > 20:
            for pattern, message in ALL_ENGLISH_PATTERNS:
                if re.match(pattern, text):
                    # Allow if it's a technical reference or path
                    if not any(
                        text.startswith(p)
                        for p in ("src/", "http", "/api", "GET ", "POST ", "BEP-")
                    ):
                        issues.append({
                            "type": "all_english",
                            "text": text[:50] + ("..." if len(text) > 50 else ""),
                            "suggestion": message,
                            "line": i + 1,
                            "severity": "info",
                        })

    return issues


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)

    # Get text segments
    texts = []
    if "text" in input_data:
        texts = input_data["text"].split("\n")
    elif "adf" in input_data:
        texts = extract_text_from_adf(input_data["adf"])

    if not texts:
        print(json.dumps({"error": "No text provided", "issues": [], "score": 100}))
        sys.exit(0)

    issues = validate_text(texts)

    # Calculate score
    total_segments = len(texts)
    issue_count = len(issues)
    warnings = len([i for i in issues if i["severity"] == "warning"])
    score = max(0, 100 - (warnings * 10) - (issue_count - warnings) * 2)

    # Summary
    if not issues:
        summary = "✅ No transliteration issues found"
    elif warnings > 0:
        summary = f"⚠️ {warnings} transliteration issue(s), {issue_count - warnings} info"
    else:
        summary = f"ℹ️ {issue_count} suggestion(s) for improvement"

    print(json.dumps({
        "issues": issues,
        "score": score,
        "total_segments": total_segments,
        "summary": summary,
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
