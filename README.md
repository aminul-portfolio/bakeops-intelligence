# BakeOps Intelligence

BakeOps Intelligence is a bakery operations analytics platform built with Django.

It transforms bakery catalogue, customer, order, ingredient, recipe, production, waste, loyalty, and review data into dashboard-ready metrics, trusted analytics pages, data quality checks, metric lineage evidence, and BI-ready CSV exports.

---

## Project Status

```text
V1 = Works
V2 = Trusted
V3 = Commercial - in progress
```

V1 delivered a working analytics dashboard powered by seeded operational data and a repeatable metric build command.

V2 delivers deeper trusted decision-support pages, data quality review, export contract visibility, metric governance documentation, data lineage documentation, and final release verification.

V3 focuses on commercial readiness: product positioning, commercial scope, realistic import planning, demo/customer setup workflows, commercial operations dashboard polish, beta-readiness documentation, deployment-readiness review, and commercial packaging strategy.

V3 should not claim fake integrations, fake customers, fake billing, fake subscriptions, fake production deployment, or fake live SaaS usage.

---

## V3 Commercial Readiness

BakeOps Intelligence V3 turns the trusted V2 analytics foundation into a commercially credible product foundation.

The commercial positioning is:

```text
A bakery operations intelligence platform for small and growing bakeries that need clearer visibility into product profitability, waste impact, ingredient risk, customer value, occasion demand, data quality issues, and BI-ready reporting outputs.
```

The realistic first user is:

```text
A bakery owner, bakery manager, or operations lead who wants better operational visibility before making pricing, production, waste, stock, and product decisions.
```

V3 is not allowed to overclaim features that are not implemented.

Current commercial truth:

| Area | Status |
|---|---|
| Trusted analytics pages | Implemented |
| Gold-layer metric build | Implemented |
| Data quality visibility | Implemented |
| BI-ready exports | Implemented |
| Commercial product positioning | V3 Sprint 1 |
| Import readiness assessment | V3 Sprint 2 |
| Draft import contract | V3 Sprint 2 |
| Demo setup workflow | V3 Sprint 3 |
| Customer setup foundation | V3 Sprint 3 |
| Commercial operations dashboard polish | V3 Sprint 4 |
| Import workflow implementation | Planned / not implemented yet |
| Customer onboarding workflow | Planned / not implemented yet |
| External POS integration | Not implemented yet |
| Shopify/Square integration | Not implemented yet |
| Billing/subscriptions | Not implemented yet |
| Production deployment | Unknown unless verified |

V3 documentation:

| Document | Purpose |
|---|---|
| `docs/V3_PRODUCT_STRATEGY.md` | Defines the commercial product strategy, first user, business problem, existing evidence, and V3 direction |
| `docs/V3_COMMERCIAL_SCOPE.md` | Defines what can be claimed, what is planned, what is out of scope, and how to avoid commercial overclaiming |
| `docs/V3_IMPORT_READINESS.md` | Assesses safe import candidates, validation categories, import risks, and future workflow design |
| `docs/V3_IMPORT_CONTRACT.md` | Defines draft file contracts for future customer, ingredient, order, order item, and waste record imports |
| `docs/V3_DEMO_SETUP_WORKFLOW.md` | Defines the repeatable demo setup, verification path, safe demo claims, and demo-to-customer bridge |
| `docs/V3_CUSTOMER_SETUP_FOUNDATION.md` | Defines the first-customer setup foundation, manual setup model, validation expectations, and customer setup boundaries |
| `docs/V3_OPERATIONS_DASHBOARD_POLISH.md` | Defines Sprint 4 dashboard polish scope, commercial workflow messaging, dashboard honesty rules, and acceptance criteria |

---

## V3 Import Readiness

V3 Sprint 2 defines how BakeOps can safely move from seeded demo data toward realistic customer-provided bakery records.

The import strategy is intentionally cautious:

```text
source files
-> staging validation
-> operational records
-> metric build command
-> gold-layer snapshots
-> trusted analytics pages
-> BI-ready exports
```

V3 Sprint 2 does not implement import code yet.

It defines the import readiness assessment and draft import contract for future files such as:

```text
customers.csv
ingredients.csv
orders.csv
order_items.csv
waste_records.csv
```

This protects the V2 trust model by ensuring future imports feed operational records first, then rebuild analytics through the existing metric pipeline.

---

## V3 Demo and Customer Setup Foundation

V3 Sprint 3 defines how BakeOps should be demonstrated and how a first customer setup could work later.

The current demo remains seeded and controlled.

Safe demo setup flow:

```text
seed_demo_data
-> build_bakery_metrics
-> review trusted analytics pages
-> export_bi_csv
-> verify Birthday Classic signature insight
```

The first-customer setup foundation is intentionally manual and evidence-based.

It describes how a bakery could eventually move from customer-provided records into operational models, metric builds, data quality checks, analytics pages, and BI-ready exports.

V3 Sprint 3 does not implement automated onboarding, workspace provisioning, billing, subscriptions, live customer imports, or multi-tenant SaaS account management.

---

## V3 Commercial Operations Dashboard Polish

V3 Sprint 4 improves the main analytics dashboard so it communicates BakeOps as a premium commercial operations intelligence workflow.

The dashboard now explains:

```text
operational records
-> trusted metric build
-> analytics pages
-> action review
-> BI-ready exports
```

Sprint 4 adds a clearer commercial-readiness narrative, a seeded-demo honesty layer, an operating workflow path, and stronger reviewer-facing dashboard communication.

V3 Sprint 4 does not add or claim live POS integration, Shopify/Square integration, customer onboarding automation, billing, subscriptions, production deployment, or live SaaS usage.

---

## Core Purpose

BakeOps Intelligence is not just a bakery catalogue website.

The project separates the application into two layers:

| App | Purpose |
|---|---|
| `cakes` | Existing customer-facing cake catalogue |
| `bakeops` | Analytics, operations, metrics, data quality, exports, and decision intelligence |

The core business idea is:

> A best-selling bakery product can become weak after ingredient cost and waste are included.

BakeOps is designed to prove this using stored operational records, repeatable metric builds, gold-layer snapshots, analytics pages, tests, and exports.

---

## Metric Workflow

```text
seed_demo_data
-> operational bakery data
-> build_bakery_metrics
-> gold-layer snapshots
-> trusted analytics pages
-> export_bi_csv
-> BI-ready CSV files
```

The dashboard is not treated as the source of truth. The platform stores operational records and gold-layer snapshots, then uses those records to power analytics pages and exports.

---

## Key Platform Features

- Realistic seeded bakery operations dataset
- Workspace, customers, loyalty, occasions, orders, ingredients, recipes, production, allocation, and waste records
- Gold-layer analytics models
- Repeatable metric build command
- Bakery metric run logging
- Data quality issue generation
- Main `/analytics/` dashboard
- Product profitability analysis
- Ingredient risk analysis
- Waste analysis
- Occasion demand analysis
- Customer loyalty analysis
- Data quality review page
- Export centre and export contract page
- BI-ready CSV exports
- Metric governance and lineage documentation
- Test coverage for key commands, services, views, and export parity
- Commercial product-boundary documentation
- Import readiness and draft import-contract documentation
- Demo setup and first-customer setup foundation documentation
- Premium commercial operations dashboard communication

---

## V2 Trusted Analytics Pages

| Page | URL | Purpose |
|---|---|---|
| Main dashboard | `/analytics/` | Executive overview of bakery metrics and signature insight |
| Product profitability | `/analytics/products/` | Product ranking, waste-adjusted margin, margin-rank inversion, and action flags |
| Ingredient risk | `/analytics/ingredients/` | Stock risk, reorder pressure, near-expiry lots, and ingredient recommendations |
| Waste analysis | `/analytics/waste/` | Waste cost, waste reasons, product waste impact, and margin reduction |
| Occasion analytics | `/analytics/occasions/` | Occasion demand, revenue, upcoming orders, and delivery pressure |
| Customer analytics | `/analytics/customers/` | Customer revenue, repeat behaviour, average order value, and loyalty visibility |
| Data quality review | `/analytics/data-quality/` | Open data quality issues, severity, status, trust impact, and suggested action |
| Export centre | `/analytics/exports/` | BI export contract, file names, source models, and export usage guidance |

---

## Signature Insight

BakeOps proves the following business idea:

> A best-selling product can become weak after ingredient cost and waste are included.

In the seeded demo:

| Product | Revenue Rank | Waste-adjusted Margin Rank | Action |
|---|---:|---:|---|
| Birthday Classic | #1 | #4 | Review |

This shows that the highest-revenue product is not necessarily the strongest product after waste-adjusted profitability is calculated.

The signature insight can be verified directly from the database:

```powershell
python manage.py shell -c "from bakeops.models import ProductPerformanceSnapshot; p=ProductPerformanceSnapshot.objects.get(cake__name='Birthday Classic'); print(p.cake.name, p.revenue_rank, p.waste_adjusted_margin_rank, p.action_flag)"
```

Expected output:

```text
Birthday Classic 1 4 review
```

---

## Reviewer Documentation

| Document | Purpose |
|---|---|
| `docs/REVIEWER_WALKTHROUGH.md` | Reviewer path for running the demo and validating the project |
| `docs/METRIC_GOVERNANCE.md` | Explains the metric build process, gold-layer snapshots, run logging, and verification commands |
| `docs/LINEAGE.md` | Explains the data lineage from seeded operational records to analytics pages and BI exports |
| `docs/V2_RELEASE_CHECKLIST.md` | Final V2 release checklist covering tests, routes, metrics, exports, documentation, and Git hygiene |
| `docs/V3_PRODUCT_STRATEGY.md` | V3 commercial product strategy, first user, business problem, evidence, and direction |
| `docs/V3_COMMERCIAL_SCOPE.md` | V3 commercial scope boundary, implemented/planned status, and overclaim prevention |
| `docs/V3_IMPORT_READINESS.md` | V3 import readiness assessment, first import candidates, validation categories, and safe workflow design |
| `docs/V3_IMPORT_CONTRACT.md` | Draft contract for future customer, ingredient, order, order item, and waste record imports |
| `docs/V3_DEMO_SETUP_WORKFLOW.md` | Repeatable demo setup, verification path, safe demo claims, and demo-to-customer bridge |
| `docs/V3_CUSTOMER_SETUP_FOUNDATION.md` | First-customer setup foundation, manual setup model, validation expectations, and customer setup boundaries |
| `docs/V3_OPERATIONS_DASHBOARD_POLISH.md` | Sprint 4 dashboard polish scope, commercial workflow messaging, and dashboard honesty rules |
| `docs/DATA_MODEL_DRAFT.md` | Draft view of the operational and analytics data model |

---

## Main Commands

### 1. Run Django checks

```powershell
python manage.py check
```

### 2. Seed demo data

```powershell
python manage.py seed_demo_data --reset
```

### 3. Build gold-layer metrics

```powershell
python manage.py build_bakery_metrics
```

### 4. Export BI-ready CSV files

```powershell
python manage.py export_bi_csv
```

### 5. Run tests

```powershell
python manage.py test bakeops
```

### 6. Run local server

```powershell
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/analytics/
```

---

## Recommended Reviewer Verification Flow

Run the following sequence from a clean local setup:

```powershell
python manage.py check
python manage.py test bakeops
python manage.py seed_demo_data --reset
python manage.py build_bakery_metrics
python manage.py export_bi_csv
python manage.py runserver
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

## BI Export Files

The export command generates files into the `exports/` folder:

| File | Layer | Purpose |
|---|---|---|
| `fact_orders.csv` | Fact | Order-level fact table |
| `fact_order_items.csv` | Fact | Order item fact table |
| `fact_waste.csv` | Fact | Waste fact table |
| `fact_production_batches.csv` | Fact | Production batch fact table |
| `dim_cake.csv` | Dimension | Cake and variant dimension |
| `dim_ingredient.csv` | Dimension | Ingredient dimension |
| `dim_customer.csv` | Dimension | Customer and loyalty dimension |
| `dim_occasion.csv` | Dimension | Occasion dimension |
| `dim_collection.csv` | Dimension | Cake collection dimension |
| `daily_bakery_metrics.csv` | Gold | Daily KPI gold-layer export |
| `product_performance_snapshot.csv` | Gold | Product profitability gold-layer export |

Generated CSV files are intentionally ignored by Git because they are reproducible from the seeded data and metric build.

---

## Export Verification

Run:

```powershell
python manage.py export_bi_csv
```

Expected output pattern:

```text
BakeOps BI CSV exports generated successfully.
Files generated: 11
Total rows exported: 52
```

The exact output directory depends on your local project path.

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

## Metric Governance Summary

BakeOps V2 is designed to be inspectable.

The metric build command creates:

| Output | Purpose |
|---|---|
| `DailyBakeryMetric` | Daily KPI summary |
| `ProductPerformanceSnapshot` | Product revenue, margin, waste-adjusted margin, ranking, and action flag |
| `IngredientUsageSnapshot` | Ingredient usage, waste, stock risk, and expiry pressure |
| `OccasionDemandSnapshot` | Occasion demand, revenue, upcoming orders, and delivery pressure |
| `CustomerLoyaltySnapshot` | Customer revenue, order count, AOV, loyalty points, and repeat status |
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

For full details, see:

```text
docs/METRIC_GOVERNANCE.md
docs/LINEAGE.md
```

---

## Data Quality Visibility

BakeOps does not hide trust issues.

The metric build creates `DataQualityIssue` records when operational data needs review.

The data quality review page shows:

```text
/analytics/data-quality/
```

It surfaces:

- issue severity
- issue type
- status
- affected area
- trust impact
- suggested review action

Current seeded demo pattern:

```text
Total data quality issues: 12
Open issues: 12
Warning issues: 11
Info issues: 1
```

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

---

## Environment Variables

Copy:

```text
.env.example
```

to:

```text
.env
```

Then set your local `SECRET_KEY`.

---

## Verification Checklist

```markdown
- [x] `python manage.py check` passes
- [x] `python manage.py migrate` works
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
- [x] Data quality issues are visible
- [x] BakeryMetricRunLog is created by metric builds
- [x] BI exports work
- [x] Dashboard metrics match export metrics
- [x] BakeOps tests pass
```

---

## Current Limitations

- V2 currently uses seeded demo data.
- V2 does not yet include file imports.
- V2 does not yet include external POS, Shopify, Square, Stripe, or payment integrations.
- V2 does not yet include live production scheduling feeds.
- V2 does not yet include multi-tenant SaaS permissions.
- V2 does not yet include billing, subscriptions, or commercial onboarding.
- V2 does not yet include customer-facing commercial workspace onboarding.
- V3 Sprint 2 defines import readiness and draft import contracts, but does not implement import code yet.
- V3 Sprint 3 defines demo and customer setup workflows, but does not implement automated onboarding yet.
- V3 Sprint 4 improves the commercial operations dashboard communication, but does not implement live imports, onboarding, billing, subscriptions, or external integrations.

These are V3/V4 concerns.

---

## Version Strategy

```text
V1 = Works
V2 = Trusted
V3 = Commercial
```

V2 focuses on deeper analytics pages, metric governance, data lineage, export contracts, data quality visibility, and reviewer evidence.

V3 focuses on commercial readiness, import planning, onboarding/setup workflow, beta-readiness documentation, deployment-readiness review, commercial dashboard polish, and commercial packaging strategy.

V3 does not currently claim live SaaS billing, real customer usage, external POS integration, Shopify/Square integration, or production multi-tenant operations.

---

## Project Positioning

BakeOps Intelligence is best understood as a portfolio-grade bakery operations intelligence platform.

It demonstrates:

- Django application structure
- operational data modelling
- metric build pipelines
- gold-layer analytics modelling
- decision-support dashboards
- data quality checks
- export contracts
- reviewer verification workflow
- analytics engineering thinking
- commercial product-boundary discipline
- cautious import-readiness planning
- demo and first-customer setup workflow planning
- premium commercial operations dashboard communication

The platform is intentionally scoped as a trusted analytics foundation moving into V3 commercial readiness, not a fake fully launched commercial SaaS product.
