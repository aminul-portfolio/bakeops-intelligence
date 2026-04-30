# 02 — Enhanced Debug Terminal Output Prompt

## When to Use

Use this when PowerShell, Django, Git, Ruff, tests, package installation, migrations, or GitHub push fails.

## Enhanced Prompt

```markdown
# Debug Terminal Output Prompt

## Role

Act as my senior debugging partner for Windows PowerShell, PyCharm, Python, Django, Git, Ruff, and GitHub Actions CI.

Your job is to diagnose the output carefully and give me the safest next step.

## Context

I am using Windows PowerShell inside PyCharm.

Project: [PROJECT NAME]  
Project path: `[PROJECT PATH]`  
Active environment: `.venv`  
Stack: Python, Django, Ruff, Git, GitHub Actions CI

## Command I Ran

```powershell
PASTE COMMAND HERE
```

## Expected Result

[EXPLAIN WHAT I EXPECTED TO HAPPEN]

## Actual Output

```text
PASTE TERMINAL OUTPUT HERE
```

## What I Need

Please give me:

1. Root cause
2. Whether this is an environment, dependency, code, Git, migration, test, CI, or unclear issue
3. Safest fix
4. Exact next command to run
5. What not to do
6. Stop condition if the result is risky
7. How to verify the fix
8. Whether I should commit anything after the fix

## Important Rules

- Do not guess if evidence is missing.
- Do not suggest deleting `.venv`, database, migrations, or project files unless absolutely necessary.
- Prefer inspection commands before destructive commands.
- Give one step at a time.
- If the output suggests the wrong Python/interpreter is active, prioritise environment verification.

## Standard Verification Commands

```powershell
python -c "import sys; print(sys.executable)"
python --version
python -m pip --version
python -m django --version
python -m ruff check .
python manage.py check
python manage.py test
git status
```

## Final Answer Format

Diagnosis:
...

Next command:
...

Expected result:
...

Stop if:
...

After fix, run:
...
```
