# 06 — Enhanced Senior DA/DE/AE Workflow Refinement Prompt

## When to Use

Use this when you want ChatGPT or Claude to audit and improve your whole AI-assisted workflow as a senior DA/DE/AE process.

## Enhanced Prompt

```markdown
# Senior DA/DE/AE Workflow Refinement Prompt

## Role

Act as my senior DA/DE/AE workflow architect.

DA = Data Analyst  
DE = Data Engineer  
AE = Analytics Engineer  

Your job is to help me refine my Python/Django/data analytics workflow so I can work with more precision, less confusion, stronger evidence, and better portfolio credibility.

Do not rush. Prioritise correctness, clarity, verification, and professional delivery over speed.

## My Career Direction

I am building toward roles such as:

- Analytics Engineer
- Data Engineer
- Data Analyst
- BI / Reporting Analyst
- FinTech analytics
- Python/Django data-product roles

My portfolio direction focuses on:

- Python
- Django
- Pandas / analytics-style workflows
- ETL thinking
- KPI dashboards
- BI-ready exports
- data quality checks
- metric governance
- operational reporting
- FinTech or business decision-support products

## My Current Workflow Model

PyCharm is my command center.

GitHub is my source of truth.

Claude inside PyCharm is my selected-code assistant.

ChatGPT is my senior reviewer, sprint strategist, documentation editor, and risk-checking partner.

AI handoff methods include:

- selected code copied from PyCharm
- file uploads
- GitHub repository context
- terminal output
- Git diff
- reusable prompt files in `docs/ai-prompts/`

My quality gate includes:

```powershell
python -m ruff check .
python manage.py check
python manage.py test
git diff --stat
git status
```

My final release gate is:

GitHub Actions CI must be green.

## My Existing Prompt System

I already use prompt templates for:

1. Selected code review
2. Debugging terminal output
3. Git diff review
4. README/documentation polish
5. Sprint gate review

Please help me improve this system, not replace it unnecessarily.

## What I Want From You

Please review my workflow like a senior DA/DE/AE mentor.

I want you to identify:

1. What is already strong
2. What is missing
3. Where my workflow could become risky
4. How I can make my AI usage more precise
5. How I can reduce confusion when replacing code
6. How I can improve evidence before committing
7. How I can make my process more recruiter/hiring-manager credible
8. How I can use this workflow across serious portfolio projects
9. What should be standardised
10. What should remain project-specific

## Senior-Level Review Criteria

### 1. Precision

Check whether each AI request includes:

- project context
- file path
- selected block purpose
- exact search anchor
- exact replacement block
- expected behaviour
- safety checks
- stop condition

### 2. Evidence

Check whether every milestone has proof:

- Ruff passed
- Django check passed
- tests passed
- GitHub Actions CI green
- git status clean
- diff reviewed
- README claims match implemented features
- I can explain the change myself

### 3. Data / Analytics Quality

Check whether my workflow improves:

- KPI reliability
- data quality visibility
- metric lineage
- BI export trust
- dashboard consistency
- reporting accuracy
- business interpretation

### 4. Engineering Discipline

Check whether my workflow supports:

- small commits
- clear Git history
- controlled scope
- no accidental file changes
- no fake integrations
- no overclaiming
- test-first or test-aware work
- clean rollback options

### 5. Career Positioning

Check whether my workflow helps me present myself as:

- practical
- evidence-based
- commercially realistic
- technically reliable
- analytics-focused
- able to build data products, not just web pages

## Important Rules

Do not suggest large rewrites unless absolutely necessary.

Do not suggest fake production claims.

Do not invent users, customers, integrations, billing, deployment, or commercial traction.

Do not tell me to move faster if accuracy would suffer.

Do not suggest many tools at once.

Do not recommend replacing my workflow with random AI automation.

Prioritise:

- clarity
- repeatability
- verification
- small safe improvements
- recruiter-friendly evidence
- senior-level reasoning

## Output Format Required

Please return your answer in this structure:

## 1. Executive Assessment

Give me a clear rating out of 10 for my current workflow.

Explain whether it looks beginner, intermediate, professional, or senior-ready.

## 2. What Is Already Strong

Use checkboxes.

Focus on what I should keep.

## 3. Main Gaps

Use checkboxes.

Separate gaps into:

- technical workflow gaps
- AI prompt gaps
- evidence/verification gaps
- portfolio/career gaps

## 4. Recommended Workflow Upgrade

Give me a step-by-step workflow from start to finish:

1. Start-of-session check
2. Choose one small target
3. Use Claude for selected-code review
4. Use ChatGPT for risk review
5. Apply change in PyCharm
6. Review Git diff
7. Run safety commands
8. Commit and push
9. Confirm GitHub Actions green
10. Run sprint gate
11. Decide GO or STOP

## 5. Improved Prompt System

Suggest the best prompt files I should keep or add.

For each prompt file, give:

- file name
- purpose
- when to use it
- what evidence it should require

## 6. Senior-Level Replacement Workflow

Give me a precise code-replacement process that avoids confusion.

It must include:

- file path
- search anchor
- old block
- new block
- why it is safe
- checks after replacement
- stop condition

## 7. Evidence Checklist

Give me a reusable checklist before I commit.

Include:

- Ruff
- Django check
- tests
- Git diff
- Git status
- GitHub Actions
- README/product truth check
- ability to explain the change

## 8. Career Alignment

Explain how this workflow supports DA/DE/AE roles.

Map it to:

- Analytics Engineering
- Data Engineering
- Data Analysis / BI
- FinTech analytics
- hiring-manager credibility

## 9. Next Best Action

Give me only one next milestone.

Do not give me five possible next projects.

Give me:

- milestone name
- why it matters
- exact tasks
- commands to run
- definition of done
- stop condition

## 10. Final Stop/Go Decision

End with one of these:

GO — safe to proceed

or:

STOP — fix the following before proceeding

Explain why.
```
