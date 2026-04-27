# Changelog

## Unreleased

## V3 Sprint 3 - Demo and Customer Setup Workflow Foundation

### Added

- Added `docs/V3_DEMO_SETUP_WORKFLOW.md` to define the repeatable demo setup, verification flow, safe demo claims, and demo-to-customer bridge.
- Added `docs/V3_CUSTOMER_SETUP_FOUNDATION.md` to define the first-customer setup foundation, manual setup model, validation expectations, and setup boundaries.

### Changed

- Updated `README.md` with V3 demo and customer setup documentation references.
- Updated `README.md` with a demo/customer setup section that clearly separates seeded demo usage from future customer onboarding.
- Updated README commercial truth table to mark demo setup workflow and customer setup foundation as V3 Sprint 3 outputs.

### Guardrails

- No model changes.
- No migration changes.
- No onboarding UI added.
- No customer signup flow added.
- No billing or subscription logic added.
- No fake live customer or production onboarding claims.

---

## V3 Sprint 2 - Import Readiness Assessment and Safe Import Design

### Added

- Added `docs/V3_IMPORT_READINESS.md` to assess safe import candidates, validation categories, import risks, and future workflow design.
- Added `docs/V3_IMPORT_CONTRACT.md` to define draft file contracts for customers, ingredients, orders, order items, and waste records.

### Changed

- Updated `README.md` with V3 import readiness documentation references.
- Updated `README.md` with a cautious import-readiness section that preserves the V2 trusted metric workflow.
- Updated README commercial truth table to mark import readiness assessment and draft import contract as V3 Sprint 2 outputs.

### Guardrails

- No model changes.
- No migration changes.
- No import parser added.
- No upload UI added.
- No fake POS, Shopify, Square, or live customer data integration claims.

---

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
