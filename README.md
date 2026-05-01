# BakeOps Intelligence

![BakeOps Django CI](https://github.com/aminul-portfolio/bakeops-intelligence/actions/workflows/django-ci.yml/badge.svg)

**BakeOps Intelligence** is a Django-based bakery operations intelligence platform that turns seeded bakery operations data into trusted KPI dashboards, profitability analysis, ingredient-risk visibility, waste analysis, data-quality review, and BI-ready CSV exports.

It demonstrates a complete analytics workflow:

```text
operational records
-> repeatable metric build
-> gold-layer snapshots
-> trusted analytics pages
-> data-quality review
-> BI-ready CSV exports
-> reviewer verification evidence
```

BakeOps is intentionally positioned as a **portfolio-grade commercial foundation**, not a falsely launched production SaaS product.

---

## Status

```text
V1 = Works
V2 = Trusted
V3 = Commercial foundation
Milestone 3 = Final UI / trust polish and reviewer-ready QA
```

| Stage | Meaning | Status |
|---|---|---|
| V1 | Working analytics dashboard from seeded operational data | Complete |
| V2 | Trusted analytics pages, metric governance, lineage, data quality, exports, tests, CI | Complete |
| V3 | Commercial-readiness foundation with honest product boundaries | Complete |
| Milestone 3 | Final UI polish, trust-surface polish, screenshot evidence, QA, merge readiness | In final QA |

---

## Core Product Positioning

BakeOps Intelligence is designed for small and growing bakeries that need clearer operational visibility before making pricing, production, waste, stock, customer, and product decisions.

It helps answer business questions such as:

- Which products look successful by revenue but weaken after waste-adjusted margin?
- Which ingredients create stock, reorder, or expiry risk?
- Which waste patterns reduce profitability?
- Which occasions drive demand and operational pressure?
- Which customers contribute repeat value?
- Which data-quality issues must be visible before trusting dashboard outputs?
- Which CSV files are available for BI/reporting workflows?

---

## Commercial Truth Boundary

BakeOps Intelligence is a credible commercial foundation, but it does **not** claim fake SaaS capabilities.

| Area | Current Status |
|---|---|
| Trusted analytics pages | Implemented |
| Gold-layer metric build | Implemented |
| Data quality visibility | Implemented |
| BI-ready CSV exports | Implemented |
| Tests and CI | Implemented |
| Screenshot evidence | Implemented |
| Commercial product positioning | Documented |
| Import readiness | Documented |
| Demo/customer setup workflow | Documented |
| Deployment-readiness checklist | Documented |
| Packaging/pricing strategy | Documented |
| External POS integration | Not implemented |
| Shopify/Square integration | Not implemented |
| Billing/subscriptions | Not implemented |
| Automated onboarding | Not implemented |
| Multi-tenant SaaS account management | Not implemented |
| Production SaaS deployment | Not claimed |
| Real customer usage | Not claimed |

This boundary is deliberate. The project prioritises evidence, verification, and honest portfolio positioning over exaggerated claims.

---

## Reviewer Evidence Snapshot

Latest verified evidence:

```text
Git status: clean
Ruff: passed
Django system check: passed
Migration dry-run: no changes detected
Tests: 37 passed
Seed command: passed
Metric build command: passed
BI export command: 11 files, 52 rows
Signature insight: Birthday Classic 1 4 review
GitHub Actions: green
```

Protected reviewer proof:

```text
Birthday Classic 1 4 review
```

Meaning:

| Product | Revenue Rank | Waste-adjusted Margin Rank | Action |
|---|---:|---:|---|
| Birthday Classic | 1 | 4 | review |

This proves the core business idea:

> The highest-revenue product is not necessarily the strongest product after ingredient cost and waste impact are included.

---

## Milestone 3 Final UI and Trust Polish

Milestone 3 finalizes the reviewer-facing analytics experience without changing the underlying analytics logic.

The milestone focused on UI consistency, clearer trust surfaces, safer template symbols, shared spacing utilities, screenshot evidence, and final reviewer QA.

| Area | Outcome |
|---|---|
| Dashboard command centre | Main analytics dashboard now communicates the source-records-to-decision workflow more clearly |
| Product profitability | Signature insight is clearer: revenue rank is not the same as margin strength |
| Data quality review | Data-quality issues are presented as visible trust evidence before relying on dashboard outputs |
| Export centre | BI exports are explained as a reviewable file contract rather than an undocumented export list |
| Shared UI foundation | Common CSS tokens, shell styles, components, and spacing utilities are loaded across analytics pages |
| Screenshot evidence | Final screenshots captured for all 8 analytics pages |
| Safety checks | Ruff, Django checks, migration dry-run, tests, seed/build/export commands, and protected proof were verified |

Final Milestone 3 screenshot set:

| Page | Screenshot |
|---|---|
| Dashboard | `docs/3e/final-screenshots/01-dashboard.png` |
| Product Profitability | `docs/3e/final-screenshots/02-product-profitability.png` |
| Ingredient Risk | `docs/3e/final-screenshots/03-ingredient-risk.png` |
| Waste Analysis | `docs/3e/final-screenshots/04-waste-analysis.png` |
| Occasion Analytics | `docs/3e/final-screenshots/05-occasion-analytics.png` |
| Customer Analytics | `docs/3e/final-screenshots/06-customer-analytics.png` |
| Data Quality Review | `docs/3e/final-screenshots/07-data-quality-review.png` |
| Export Centre | `docs/3e/final-screenshots/08-export-centre.png` |

Milestone 3 does not claim live POS integration, live customer data, billing, subscriptions, production SaaS deployment, or automated BI sync.

---

## Platform Architecture

BakeOps separates the customer-facing catalogue from the analytics and operations intelligence layer.

| App | Purpose |
|---|---|
| `cakes` | Customer-facing cake catalogue and related static assets |
| `bakeops` | Analytics, operations, metrics, data quality, exports, and decision intelligence |

High-level architecture:

```text
Seeded demo records
-> operational models
-> metric build command
-> gold-layer analytics models
-> analytics views
-> HTML dashboards
-> CSV export service
-> reviewer documentation and screenshots
```

---

## Analytics Workflow

```text
python manage.py seed_demo_data --reset
-> creates seeded bakery operations records

python manage.py build_bakery_metrics
-> creates gold-layer snapshots and data-quality issues

python manage.py export_bi_csv
-> generates BI-ready CSV export pack

analytics pages
-> read existing stored operational and gold-layer data
```

The dashboard is not treated as the source of truth. The source of truth is the stored operational records and gold-layer metric snapshots.

---

## Key Features

### Operations and Analytics

- Seeded bakery operations dataset
- Workspace, customers, loyalty, occasions, orders, ingredients, recipes, production, allocation, and waste records
- Gold-layer analytics models
- Repeatable metric build command
- Metric build run logging
- Product profitability analysis
- Ingredient risk analysis
- Waste analysis
- Occasion demand analysis
- Customer loyalty analytics
- Data-quality issue generation and review
- BI-ready CSV exports
- Export contract page

### Trust and Reviewability

- Metric governance documentation
- Data lineage documentation
- Data-quality visibility
- Export contract documentation
- Reviewer walkthrough
- Final screenshot evidence
- Tests for commands, services, views, and export parity
- GitHub Actions CI

### Commercial Readiness

- Product strategy
- Commercial scope
- Import readiness assessment
- Draft import contract
- Demo setup workflow
- Customer setup foundation
- Beta-readiness documentation
- Deployment-readiness checklist
- Packaging/pricing strategy
- Final hardening and release checklist

---

## Analytics Pages

| Page | URL | Purpose |
|---|---|---|
| Main dashboard | `/analytics/` | Executive overview, command centre, workflow summary, signature insight |
| Product profitability | `/analytics/products/` | Product ranking, waste-adjusted margin, margin-rank inversion, action flags |
| Ingredient risk | `/analytics/ingredients/` | Stock risk, reorder pressure, near-expiry lots, ingredient recommendations |
| Waste analysis | `/analytics/waste/` | Waste cost, waste reasons, product waste impact, margin reduction |
| Occasion analytics | `/analytics/occasions/` | Occasion demand, revenue, upcoming orders, delivery pressure |
| Customer analytics | `/analytics/customers/` | Customer revenue, repeat behaviour, average order value, loyalty visibility |
| Data quality review | `/analytics/data-quality/` | Open data-quality issues, severity, status, trust impact, suggested action |
| Export centre | `/analytics/exports/` | BI export contract, file names, source models, usage guidance |

---

## Signature Insight

BakeOps proves the following business idea:

> A best-selling product can become weak after ingredient cost and waste are included.

In the seeded demo:

| Product | Revenue Rank | Waste-adjusted Margin Rank | Action |
|---|---:|---:|---|
| Birthday Classic | #1 | #4 | Review |

Verify directly:

```powershell
python manage.py shell -c "from bakeops.models import ProductPerformanceSnapshot; p=ProductPerformanceSnapshot.objects.get(cake__name='Birthday Classic'); print(p.cake.name, p.revenue_rank, p.waste_adjusted_margin_rank, p.action_flag)"
```

Expected output:

```text
Birthday Classic 1 4 review
```

---

## BI Export Contract

The export command generates 11 CSV files into the `exports/` folder.

```powershell
python manage.py export_bi_csv
```

Expected output pattern:

```text
BakeOps BI CSV exports generated successfully.
Files generated: 11
Total rows exported: 52
```

| File | Layer | Purpose |
|---|---|---|
| `fact_orders.csv` | Fact | Order-level fact table |
| `fact_order_items.csv` | Fact | Order item fact table |
| `fact_waste.csv` | Fact | Waste fact table |
| `fact_production_batches.csv` | Fact | Production batch fact table |
| `dim_cake.csv` | Dimension | Cake and product dimension |
| `dim_ingredient.csv` | Dimension | Ingredient dimension |
| `dim_customer.csv` | Dimension | Customer and loyalty dimension |
| `dim_occasion.csv` | Dimension | Occasion dimension |
| `dim_collection.csv` | Dimension | Cake collection dimension |
| `daily_bakery_metrics.csv` | Gold | Daily KPI gold-layer export |
| `product_performance_snapshot.csv` | Gold | Product profitability gold-layer export |

Generated CSV files are intentionally ignored by Git because they are reproducible from seeded data and the metric build pipeline.

---

## Data Quality Visibility

BakeOps does not hide trust issues.

The metric build creates `DataQualityIssue` records when operational data needs review.

The data quality page surfaces:

- issue severity
- issue type
- status
- affected area
- trust impact
- suggested review action

Current seeded demo evidence:

```text
Total data quality issues: 12
Open issues: 12
Warning issues: 11
Info issues: 1
```

---

## Metric Governance Summary

The metric build command creates:

| Output | Purpose |
|---|---|
| `DailyBakeryMetric` | Daily KPI summary |
| `ProductPerformanceSnapshot` | Product revenue, margin, waste-adjusted margin, ranking, and action flag |
| `IngredientUsageSnapshot` | Ingredient usage, waste, stock risk, expiry pressure |
| `OccasionDemandSnapshot` | Occasion demand, revenue, upcoming orders, delivery pressure |
| `CustomerLoyaltySnapshot` | Customer revenue, order count, AOV, loyalty points, repeat status |
| `DataQualityIssue` | Data quality and operational trust issues |
| `BakeryMetricRunLog` | Metric build audit trail |

The build command records:

- rows processed
- metrics created
- snapshots created
- issues created
- start time
- finish time
- duration
- status
- error message if failed

For detail:

```text
docs/METRIC_GOVERNANCE.md
docs/LINEAGE.md
```

---

## Documentation Map

| Document | Purpose |
|---|---|
| `docs/REVIEWER_WALKTHROUGH.md` | Reviewer path for running and validating the project |
| `docs/METRIC_GOVERNANCE.md` | Metric build process, gold-layer snapshots, run logging, verification commands |
| `docs/LINEAGE.md` | Data lineage from seeded records to analytics pages and BI exports |
| `docs/MILESTONE_3_PATTERN_INVENTORY.md` | UI pattern inventory and audit evidence |
| `docs/MILESTONE_3_GO_NO_GO.md` | Milestone 3 go/no-go decision record |
| `docs/V2_RELEASE_CHECKLIST.md` | V2 release checklist |
| `docs/V3_PRODUCT_STRATEGY.md` | Commercial product strategy and first-user framing |
| `docs/V3_COMMERCIAL_SCOPE.md` | Safe commercial claims and scope boundaries |
| `docs/V3_IMPORT_READINESS.md` | Import readiness assessment |
| `docs/V3_IMPORT_CONTRACT.md` | Draft import file contract |
| `docs/V3_DEMO_SETUP_WORKFLOW.md` | Repeatable demo setup workflow |
| `docs/V3_CUSTOMER_SETUP_FOUNDATION.md` | First-customer setup planning boundary |
| `docs/V3_OPERATIONS_DASHBOARD_POLISH.md` | Commercial dashboard polish scope |
| `docs/V3_BETA_READINESS.md` | Beta-readiness evidence and remaining gaps |
| `docs/V3_DEPLOYMENT_READINESS_CHECKLIST.md` | Deployment-readiness checklist |
| `docs/V3_PACKAGING_PRICING_STRATEGY.md` | Packaging and pricing strategy |
| `docs/V3_COMMERCIAL_README_POLISH.md` | README polish strategy |
| `docs/V3_FINAL_HARDENING.md` | Final hardening evidence |
| `docs/V3_RELEASE_CHECKLIST.md` | V3 final release checklist |
| `docs/DATA_MODEL_DRAFT.md` | Operational and analytics data model draft |

---

## Local Setup

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_demo_data --reset
python manage.py build_bakery_metrics
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/analytics/
```

---

## Main Commands

### Ruff

```powershell
python -m ruff check .
```

### Django system check

```powershell
python manage.py check
```

### Migration drift check

```powershell
python manage.py makemigrations --check --dry-run
```

### Tests

```powershell
python manage.py test
```

### Seed demo data

```powershell
python manage.py seed_demo_data --reset
```

### Build metrics

```powershell
python manage.py build_bakery_metrics
```

### Export BI CSV files

```powershell
python manage.py export_bi_csv
```

### Run server

```powershell
python manage.py runserver
```

---

## Recommended Reviewer Verification Flow

Run this sequence from a clean local setup:

```powershell
git status
python -m ruff check .
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
python manage.py seed_demo_data --reset
python manage.py build_bakery_metrics
python manage.py export_bi_csv
python manage.py shell -c "from bakeops.models import ProductPerformanceSnapshot; p=ProductPerformanceSnapshot.objects.get(cake__name='Birthday Classic'); print(p.cake.name, p.revenue_rank, p.waste_adjusted_margin_rank, p.action_flag)"
python manage.py runserver
```

Expected key evidence:

```text
All checks passed!
System check identified no issues (0 silenced).
No changes detected
Ran 37 tests
OK
BakeOps demo data seeded successfully.
BakeOps bakery metrics built successfully.
BakeOps BI CSV exports generated successfully.
Birthday Classic 1 4 review
```

Then open:

```text
http://127.0.0.1:8000/analytics/
http://127.0.0.1:8000/analytics/products/
http://127.0.0.1:8000/analytics/ingredients/
http://127.0.0.1:8000/analytics/waste/
http://127.0.0.1:8000/analytics/occasions/
http://127.0.0.1:8000/analytics/customers/
http://127.0.0.1:8000/analytics/data-quality/
http://127.0.0.1:8000/analytics/exports/
```

---

## Route Verification

```powershell
python manage.py shell -c "from django.test import Client; c=Client(); routes=['/analytics/','/analytics/products/','/analytics/ingredients/','/analytics/waste/','/analytics/occasions/','/analytics/customers/','/analytics/data-quality/','/analytics/exports/']; [print(r, c.get(r).status_code) for r in routes]"
```

Expected output:

```text
/analytics/ 200
/analytics/products/ 200
/analytics/ingredients/ 200
/analytics/waste/ 200
/analytics/occasions/ 200
/analytics/customers/ 200
/analytics/data-quality/ 200
/analytics/exports/ 200
```

---

## Data Model Layers

### Operational Layer

- Workspace
- StaffMember
- Customer
- LoyaltyAccount
- CakeReview
- OccasionType
- DeliverySlot
- BakeryOrder
- BakeryOrderItem
- Supplier
- Ingredient
- IngredientLot
- Recipe
- RecipeLine
- ProductionBatch
- ProductionBatchLine
- BatchAllocation
- WasteRecord

### Gold-Layer Analytics

- DailyBakeryMetric
- ProductPerformanceSnapshot
- IngredientUsageSnapshot
- OccasionDemandSnapshot
- CustomerLoyaltySnapshot
- BakeryMetricRunLog
- DataQualityIssue

---

## Final Verification Checklist

```markdown
- [x] `git status` is clean
- [x] `python -m ruff check .` passes
- [x] `python manage.py check` passes
- [x] `python manage.py makemigrations --check --dry-run` shows no changes detected
- [x] `python manage.py test` passes with 37 tests
- [x] `python manage.py seed_demo_data --reset` works
- [x] `python manage.py build_bakery_metrics` works
- [x] `python manage.py export_bi_csv` works
- [x] `/analytics/` dashboard loads
- [x] `/analytics/products/` product profitability page loads
- [x] `/analytics/ingredients/` ingredient risk page loads
- [x] `/analytics/waste/` waste analysis page loads
- [x] `/analytics/occasions/` occasion analytics page loads
- [x] `/analytics/customers/` customer analytics page loads
- [x] `/analytics/data-quality/` data quality review page loads
- [x] `/analytics/exports/` export centre page loads
- [x] Birthday Classic signature insight is visible
- [x] Data-quality issues are visible
- [x] BakeryMetricRunLog is created by metric builds
- [x] BI exports work
- [x] Dashboard metrics match export metrics
- [x] GitHub Actions is green
```

---

## Current Limitations

BakeOps Intelligence currently uses seeded demo data and documented commercial-readiness workflows.

It does not yet include:

```markdown
- [ ] external POS imports
- [ ] Shopify, Square, Stripe, or payment integrations
- [ ] live production scheduling integrations
- [ ] automated customer onboarding flows
- [ ] multi-tenant SaaS account management
- [ ] billing or subscriptions
- [ ] production SaaS deployment
- [ ] real customer usage
```

These are future concerns and should not be claimed as implemented.

---

## Version Strategy

```text
V1 = Works
V2 = Trusted
V3 = Commercial foundation
Milestone 4 = Future SaaS-style layout transformation
```

Milestone 4 is planned as a future product-interface upgrade, including unified SaaS app shell, richer visual analytics, responsive hardening, and enterprise-style page layouts.

Milestone 4 should only begin after Milestone 3E final QA and merge readiness are complete.

---

## Project Value

BakeOps Intelligence demonstrates:

- Django application structure
- operational data modelling
- metric build pipelines
- gold-layer analytics modelling
- decision-support dashboards
- data-quality checks
- BI export contracts
- reviewer verification workflow
- analytics engineering thinking
- data engineering discipline
- commercial product-boundary discipline
- cautious import-readiness planning
- demo and first-customer setup workflow planning
- beta-readiness and deployment-readiness discipline
- packaging/pricing strategy discipline
- final release hardening discipline

The platform is intentionally scoped as a trusted analytics foundation and V3 commercial foundation, not a fake fully launched commercial SaaS product.
