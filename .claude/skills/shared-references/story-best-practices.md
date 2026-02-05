# User Story Best Practices — Quick Reference

## INVEST Criteria (Story Quality Checklist)

| Criteria | Meaning | Red Flag |
| ---------- | ---------- | ---------- |
| **I**ndependent | No dependency on other stories | "Must do X first" |
| **N**egotiable | Invitation to conversation | AC too detailed / prescriptive |
| **V**aluable | Delivers real value to user | "Prepare DB schema" (no direct value) |
| **E**stimable | Effort can be estimated | Scope unclear |
| **S**mall | Fits in 1 sprint, 6-10 stories/sprint | Larger than 3 days |
| **T**estable | Has clear, testable AC | "System works well" (vague) |

## Story Format

```text
As a [persona],
I want to [goal],
So that [benefit/value].
```

## Story Narrative Quality

### Persona — Who + Context + Level

| ❌ Bad | ✅ Good | Why |
| -------- | --------- | ------ |
| As a user | As a platform admin managing 50+ campaigns | "user" too broad, no context |
| As an admin | As an admin reviewing coupon usage after campaign ends | Unknown what admin does or when |
| As a customer | As a new customer topping up credits for the first time | Unknown experience level or goal |

### Goal — Verb + Object + Context

| ❌ Bad | ✅ Good | Why |
| -------- | --------- | ------ |
| I want to see coupon list | I want to filter coupons by status and date range | "see" doesn't describe interaction |
| I want to add credit | I want to top up credits via coupon code before publishing an ad | No context on purpose |
| I want a dashboard | I want to monitor campaign spending in real-time | "dashboard" = solution, not goal |

### Benefit — Business Value (never restate goal)

| ❌ Bad | ✅ Good | Why |
| -------- | --------- | ------ |
| So that I can use it | So that I can identify expired coupons and reduce support tickets | Restates goal, no value |
| So that it works | So that customers complete top-up without leaving the ad flow | Not specific |
| So that we have this feature | So that campaign managers save 30 min/day on manual status checks | "have feature" is not business value |

**Value Levels:** Measurable (best) → Behavioral → Qualitative (acceptable) → None ❌

### Before/After — BEP Examples

| ❌ Before | ✅ After |
| --------- | -------- |
| As a user, I want to see coupon details, So that I can use coupons. | As a platform admin reviewing campaign performance, I want to view coupon usage history with user email and redemption timestamp, So that I can identify which campaigns drive the most conversions. |
| As a customer, I want to add credit, So that I have enough balance. | As a new customer publishing their first ad, I want to apply a top-up credit coupon during the pre-publish checkout, So that I can fund my campaign instantly without switching to a separate wallet page. |

### Narrative Anti-Patterns

| Pattern | Problem | Fix |
| --------- | -------- | ---------- |
| **Generic Persona** | "As a user" — no context | Specify role + situation |
| **Solution Masking** | "I want a modal" — UI solution, not goal | Write goal first, solution goes in AC |
| **Missing Why** | No "So that" or restates goal | Ask "so what?" until value is clear |
| **Kitchen Sink** | 1 story = 3 goals | Split with SPIDR |
| **Tech Story** | "As a developer, I want to refactor..." | Use Task instead of Story (no direct user value) |
| **Copy-Paste** | All stories look the same | Each story must have unique context |

## Acceptance Criteria — Given/When/Then

- **Given**: Initial system state (precondition)
- **When**: User action (trigger)
- **Then**: Expected outcome (expected result)

### AC Best Practices

- No vague ACs ("loads fast") → must be specific ("loads within 2 seconds")
- Separate story narrative from AC (don't duplicate)
- Cover: happy path (`success` panel) + edge case (`warning`) + error (`error`)
- Don't forget non-functional requirements (performance, accessibility, security)
- Each AC must be **independently testable**
- Use **Three Amigos**: PO + Dev + QA write together
- Don't write AC too narrow (no room for dev) or too broad (unclear)
- Write AC before sprint planning — don't change during sprint

## Story Splitting — SPIDR Method (Mike Cohn)

| Technique | Method | Example |
| ----------- | ------ | ---------- |
| **S**pike | Research before split | "Spike: try Redlock for 2 days" |
| **P**ath | Split by user path | Card payment vs Apple Pay |
| **I**nterface | Split by device/platform | iOS vs Android vs Web |
| **D**ata | Split by data type | Credit vs discount vs cashback |
| **R**ules | Split by business rules | Coupon expired vs fully used vs cancelled |

### Additional Splitting Techniques

- **Workflow Steps**: Split by workflow stages
- **CRUD**: Create / Read / Update / Delete separately
- **User Roles**: Admin vs Customer vs Influencer
- **Complexity**: manual vs automated, simple vs advanced
- **I/O Methods**: manual entry vs file upload vs API

### Vertical Slice Rules

**Always Vertical Slice** — never Horizontal (FE/BE split doesn't deliver value)

| Pattern | When to Use | Example |
| --- | --- | --- |
| **Walking Skeleton** | Navigation + empty states first | `vs1-skeleton` |
| **Business Rule Split** | Different rules/types | `vs2-credit`, `vs3-discount` |
| **Enabler Story** | Shared component for multiple VS | `vs-enabler` (Side Panel) |
| **Cross-feature** | Spans feature areas | `ad-integration` |

**VS Anti-patterns:**

| Anti-pattern | Why Bad | Fix |
| --- | --- | --- |
| **Shell-only** | No value (UI without logic) | Add minimal happy path |
| **Layer-split** | Blocked until other layers done | Combine BE+FE in one story |
| **Tab-split** | No context (Active tab / History tab) | Split by business rule |
| **Horizontal** | One layer across many flows | Group by user flow |

See: [Vertical Slice Guide](vertical-slice-guide.md) for full examples and decomposition process

### Splitting Guidelines

- Target: 6-10 stories/sprint, each story 1-3 days
- Every slice must deliver end-to-end value
- **VS Label Required:** Every story must have feature label + VS label

## Story Size Guide

| Size | Duration | Guideline |
| ------ | ---------- | ----------- |
| XS | < 1 day | May be too small — consider merging with another story |
| S | 1-2 days | Ideal |
| M | 2-3 days | Ideal |
| L | 3-4 days | Upper bound — consider splitting |
| XL | > 4 days | Must split — use SPIDR |

## Sources

- INVEST: <https://scrum-master.org/en/creating-the-perfect-user-story-with-invest-criteria/>
- Given/When/Then: <https://www.parallelhq.com/blog/given-when-then-acceptance-criteria>
- SPIDR: <https://www.mountaingoatsoftware.com/blog/five-simple-but-powerful-ways-to-split-user-stories>
- Story Splitting: <https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/>
- Acceptance Criteria: <https://www.atlassian.com/work-management/project-management/acceptance-criteria>
