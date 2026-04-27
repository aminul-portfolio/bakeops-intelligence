# Changelog

## Unreleased

## V3 Sprint 1 - Commercial Positioning and Product Boundary

### Added

- Added `docs/V3_PRODUCT_STRATEGY.md` to define the commercial product strategy, first realistic user, business problem, V2 evidence, and V3 direction.
- Added `docs/V3_COMMERCIAL_SCOPE.md` to define implemented, planned, candidate, and out-of-scope commercial capabilities.

### Changed

- Updated `README.md` to mark V3 as commercial-readiness in progress.
- Updated `README.md` with a commercial readiness section and V3 documentation references.
- Updated V3 wording to avoid fake SaaS, POS, Shopify, Square, Stripe, billing, subscription, production deployment, or live customer claims.

### Guardrails

- No model changes.
- No migration changes.
- No fake POS, Shopify, Square, Stripe, billing, subscription, production deployment, or live customer claims.

---

## Repository Setup and V1 Foundation

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
