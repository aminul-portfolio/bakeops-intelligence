# 05 — Enhanced Sprint Gate Review Prompt

## When to Use

Use this at the end of every milestone before moving to the next sprint.

## Enhanced Prompt

```markdown
# Sprint Gate Review Prompt

## Role

Act as my senior sprint gate reviewer.

Your job is to decide whether the milestone is complete and whether it is safe to move to the next sprint.

Be strict, evidence-based, and practical.

## Project

[PROJECT NAME]

## Milestone Completed

[PASTE MILESTONE NAME]

## What Changed

[BRIEFLY DESCRIBE WHAT WAS CHANGED]

## Evidence

```text
Ruff: passed / failed
Django check: passed / failed
Tests: passed / failed
GitHub Actions: green / red / not pushed
Git status: clean / not clean
Files changed: PASTE git diff --stat
Last commit: PASTE git log -1 --oneline
Branch: PASTE CURRENT BRANCH
```

## Product / Documentation Truth Check

Please check whether:

- README claims match implemented features
- no fake integrations are claimed
- no fake customers are claimed
- no fake billing/subscriptions are claimed
- no fake production deployment is claimed
- limitations are honest
- the change supports DA/DE/AE portfolio credibility

## Please Decide

1. Is this milestone complete?
2. Is there any technical risk?
3. Is there any data/analytics meaning risk?
4. Is there any README/product overclaiming risk?
5. Should I commit, amend, revert, or move forward?
6. Is it safe to start the next sprint?
7. What is the next safest sprint?

## Stop/Go Rule

Only approve moving forward if:

- Ruff passes
- Django check passes
- tests pass
- GitHub Actions is green
- git status is clean
- README claims match implemented reality
- the change is explainable
- the milestone has clear evidence

## Required Output

Milestone status:
...

Risks:
...

Required fixes:
...

Next safest sprint:
...

Decision:
GO / STOP

## Decision Rules

Use:

GO — safe to move to the next sprint

only when all evidence is green.

Use:

STOP — fix the following before proceeding

if any evidence is missing, risky, unclear, or uncommitted.
```
