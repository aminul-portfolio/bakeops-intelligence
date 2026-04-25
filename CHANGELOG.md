@"
# Changelog

## Unreleased

### Changed

- Renamed and flattened the Django project structure for BakeOps Intelligence.
- Moved `manage.py` to the repository root.
- Confirmed the Django config package is named `bakeops_intelligence`.
- Split Django settings into `base.py`, `local.py`, and `production.py`.
- Moved environment-specific configuration into `.env`.
- Added `.env.example`.
- Added repository cleanup rules through `.gitignore`.
- Prepared `exports/` and `docs/` folders for future V1 work.

### Removed

- Removed local SQLite database from the active repository path.
- Prepared Python cache files and IDE files to be ignored by Git.
"@ | Set-Content .\CHANGELOG.md