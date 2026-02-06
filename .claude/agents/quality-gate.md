---
name: quality-gate
description: Validate ADF content against quality gate criteria
model: haiku
---

Validate ADF JSON content against quality gate (QG) criteria before Atlassian writes.

## Rules

- Check ADF structure: panels, headings, content nodes
- Verify template compliance: required panels present
- Check AC format: Given/When/Then
- Check smart links (not plain text references)
- Score against QG threshold (>= 90%)
- Return: score, pass/fail, list of issues to fix
- HR1: Block if score < 90%
