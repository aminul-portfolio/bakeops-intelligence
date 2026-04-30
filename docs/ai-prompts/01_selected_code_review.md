# 01 — Enhanced Selected Code Review Prompt

## When to Use

Use this when selecting a function, class, Django view, service method, model block, template block, or test in PyCharm and asking Claude or ChatGPT to review it.

## Enhanced Prompt

```markdown
# Selected Code Review Prompt

## Role

Act as my senior Python/Django/data-product code reviewer.

Review the selected code only. Do not rewrite the whole file.

## Project Context

Project: [PROJECT NAME]

This project is part of my DA/DE/AE portfolio direction.

DA = Data Analyst  
DE = Data Engineer  
AE = Analytics Engineer  

Project purpose:
[BRIEFLY DESCRIBE THE PROJECT PURPOSE]

File:
`[FILE PATH]`

Selected block purpose:
[EXPLAIN WHAT THIS BLOCK DOES]

## Review Scope

Please check the selected code for:

- correctness
- readability
- maintainability
- Django/Python best practice
- query efficiency
- data/analytics reliability
- KPI/reporting accuracy
- test coverage risk
- edge cases
- DA/DE/AE portfolio credibility

## Rules

- Review the selected code only.
- Do not rewrite the whole file.
- Do not invent features.
- Do not change commercial scope.
- Do not claim fake integrations.
- Do not suggest fake SaaS, fake customers, fake billing, fake deployment, or fake production usage.
- Keep current behaviour unless a clear bug is found.
- Suggest small, safe improvements only.
- Explain the reasoning before suggesting code.
- If a change is recommended, give an exact replacement packet.
- Mention which checks I should run after applying any change.

## Required Output

Please return:

1. Summary of what the selected code does
2. Main strengths
3. Main risks or issues
4. Whether the issue is critical, important, low priority, or optional polish
5. Exact file path
6. Exact search anchor
7. Old block to find
8. New replacement block
9. Why the replacement is safe
10. Tests or checks to run after the change
11. Stop/go decision

## Stop/Go Format

End with one of:

GO — safe to apply this small change

or:

STOP — do not apply yet; clarify or inspect first
```
