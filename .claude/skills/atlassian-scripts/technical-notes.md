# Technical Notes

> SSL, Storage Format, Mermaid, History, Related Skills
>
> สำหรับ overview → ดู [SKILL.md](SKILL.md)

---

## Technical Notes

### SSL Certificate Issue (macOS)

Scripts ใช้ SSL context ที่ไม่ verify certificate:

```python
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
```

### Confluence Storage Format

**Code blocks ต้องใช้ format นี้:**

```xml
<ac:structured-macro ac:name="code" ac:schema-version="1">
  <ac:parameter ac:name="language">json</ac:parameter>
  <ac:plain-text-body><![CDATA[
    {"key": "value"}
  ]]></ac:plain-text-body>
</ac:structured-macro>
```

**ไม่ใช่:**

```html
<pre class="highlight"><code class="language-json">...</code></pre>
```

### Mermaid Diagrams

Scripts สร้าง code blocks สำหรับ mermaid แต่ไม่ render เป็น diagram

ถ้าต้องการให้แสดงเป็น flowchart:

1. ไปที่ Confluence page
2. Edit → พิมพ์ `/mermaid`
3. Paste mermaid code

---

## History

| Date | Version | Changes |
| --- | --- | --- |
| 2026-01-27 | 1.0.0 | Initial scripts: update_confluence_page.py |
| 2026-01-29 | 1.1.0 | Added create, move, fix scripts |
| 2026-01-29 | 2.0.0 | Refactored with SRP/OCP: lib/ modules, type hints, logging, custom exceptions |
| 2026-01-29 | 2.1.0 | Added audit_confluence_pages.py for content alignment verification |
| 2026-01-29 | 2.2.0 | Added JiraAPI (REST v3/ADF) + update_jira_description.py for Jira description fixes |
| 2026-01-29 | 3.0.0 | Renamed confluence-scripts → atlassian-scripts (covers both Confluence + Jira) |

---

## Related Skills

| Skill | Description |
| --- | --- |
| `/create-doc` | Create new Confluence page (uses MCP) |
| `/update-doc` | Update existing Confluence page (uses scripts when needed) |

---

## References

- Confluence REST API: <https://developer.atlassian.com/cloud/confluence/rest/v1/intro/>
- Jira REST API v3: <https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/>
- Credentials: `~/.config/atlassian/.env`
- Storage Format: <https://developer.atlassian.com/cloud/confluence/confluence-storage-format/>
- ADF (Atlassian Document Format): <https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/>
