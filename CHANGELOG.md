# Changelog

## Unreleased

## V3 Sprint 7 - Final Hardening and Release Checklist

### Added

- Added `docs/V3_FINAL_HARDENING.md` to define final V3 hardening checks, protected V2 evidence, technical verification commands, route verification, and commercial honesty rules.
- Added `docs/V3_RELEASE_CHECKLIST.md` to define the final V3 release checklist, documentation coverage, implemented/not-implemented status, safe release wording, and Git evidence.

### Changed

- Updated `README.md` with Sprint 7 final hardening and release checklist documentation references.
- Updated `README.md` with a final hardening and release checklist section.
- Updated README commercial truth and limitations sections to make V3 final release boundaries clear.
- Updated project status from V3 commercial-readiness in progress to V3 commercial foundation.

### Guardrails

- No model changes.
- No migration changes.
- No new feature code added.
- No deployment configuration changed.
- No production deployment claim added.
- No import, onboarding, billing, subscription, POS, Shopify, Square, or live customer claims added.

---

## V3 Sprint 6 - Packaging Strategy and Commercial README Polish

### Added

- Added `docs/V3_PACKAGING_PRICING_STRATEGY.md` to define realistic packaging strategy, pricing caution, future package candidates, commercial value evidence, and safe pricing language.
- Added `docs/V3_COMMERCIAL_README_POLISH.md` to define the commercial README polish direction, reviewer expectations, messaging structure, and acceptance criteria.

### Changed

- Updated `README.md` with Sprint 6 packaging/pricing and README polish documentation references.
- Updated `README.md` with a packaging, pricing strategy, and commercial README polish section.
- Updated README commercial truth and limitations sections to make billing/subscription status clear.
- Updated project positioning to include packaging/pricing strategy discipline and commercial README communication clarity.

### Guardrails

- No model changes.
- No migration changes.
- No billing code added.
- No pricing page added.
- No subscription logic added.
- No payment integration added.
- No fake customer plans, revenue, POS, Shopify, Square, or live SaaS claims added.

---

## V3 Sprint 5 - Beta Readiness and Deployment Checklist

### Added

- Added `docs/V3_BETA_READINESS.md` to define beta-readiness evidence, remaining gaps, safe beta claims, beta feedback questions, and acceptance criteria.
- Added `docs/V3_DEPLOYMENT_READINESS_CHECKLIST.md` to define deployment-readiness checks for environment configuration, database setup, static files, security, route verification, exports, and operations.

### Changed

- Updated `README.md` with Sprint 5 beta-readiness and deployment-readiness documentation references.
- Updated `README.md` with a beta and deployment readiness section.
- Updated README commercial truth and limitations sections to make production deployment status clear.

### Guardrails

- No model changes.
- No migration changes.
- No deployment configuration changed.
- No production deployment claim added.
- No import, onboarding, billing, subscription, POS, Shopify, Square, or live customer claims added.

---

## V3 Sprint 4 - Commercial Operations Dashboard Polish

### Added

- Added `docs/V3_OPERATIONS_DASHBOARD_POLISH.md` to define Sprint 4 dashboard polish scope, commercial workflow messaging, dashboard honesty rules, and acceptance criteria.
- Added a premium commercial-readiness section to the main analytics dashboard.
- Added a commercial operating workflow section to the main analytics dashboard.
- Added an evidence rail that explains implemented capabilities, documented V3 foundations, and features not claimed yet.
- Added a clearer operating-path section for product, ingredient, waste, data quality, and BI export review.

### Changed

- Updated `README.md` with the Sprint 4 dashboard polish documentation reference.
- Updated `README.md` with a commercial operations dashboard polish section.
- Updated the main analytics dashboard to feel more premium/SaaS-like while remaining honest about seeded demo data.
- Updated the main analytics dashboard to explain the operating path from bakery records to metric builds, decision pages, action review, and BI exports.
- Updated the dashboard footer from V1 wording to V3 commercial-readiness wording.

### Guardrails

- No model changes.
- No migration changes.
- No import code added.
- No onboarding UI added.
- No billing or subscription logic added.
- No fake POS, Shopify, Square, live customer, or production SaaS claims.

---

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
