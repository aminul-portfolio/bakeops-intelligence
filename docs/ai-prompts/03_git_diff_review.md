# 03 — Enhanced Git Diff Review Prompt

## When to Use

Use this before every commit. Paste `git diff --stat` and, when possible, `git diff`.

## Enhanced Prompt

```markdown
# Git Diff Review Prompt

## Role

Act as my senior code-review and release-risk reviewer.

Before I commit, review this diff for technical risk, portfolio risk, and product-scope accuracy.

## Project Context

Project: [PROJECT NAME]

Career positioning:
Analytics Engineer | Data Engineer | Data Analyst | BI | FinTech analytics | Python/Django data products

## Current Milestone

[PASTE CURRENT MILESTONE NAME]

## Safety Evidence

```text
Ruff: passed / failed / not run
Django check: passed / failed / not run
Tests: passed / failed / not run
GitHub Actions: green / red / not pushed yet
Git status: clean / modified / staged
```

## Diff Summary

```text
PASTE git diff --stat HERE
```

## Full Diff

```diff
PASTE git diff HERE
```

## Please Check For

- accidental file changes
- unrelated changes mixed together
- risky refactors
- migration risk
- test risk
- formatting-only changes
- hidden behaviour changes
- wrong KPI or dashboard meaning
- README overclaiming
- fake commercial claims
- fake integrations
- fake deployment claims
- whether the commit should be split
- whether any file should be reverted

## Required Output

Please return:

1. Overall safety rating: safe / mostly safe / risky / stop
2. What changed
3. What looks good
4. What is risky
5. Any semantic issue that tests may not catch
6. Whether the commit should be split
7. Files to keep
8. Files to revert, if any
9. Required commands before commit
10. Best commit message
11. Final stop/go decision

## Commit Message Rules

Use concise imperative style, for example:

- Polish waste analysis trust copy and formatting
- Add AI workflow prompt templates
- Correct waste analysis KPI formatting
- Add GitHub Actions CI workflow

## Final Decision Format

End with one of:

GO — commit this change

or:

STOP — fix these issues before committing
```
