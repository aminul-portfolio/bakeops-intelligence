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

V3 focuses on commercial readiness: product positioning, commercial scope, realistic import planning, demo/customer setup workflows, beta-readiness documentation, deployment-readiness review, and commercial packaging strategy.

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
| Import workflow | Planned / not implemented yet |
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

These are V3 concerns.

---

## Version Strategy

```text
V1 = Works
V2 = Trusted
V3 = Commercial
```

V2 focuses on deeper analytics pages, metric governance, data lineage, export contracts, data quality visibility, and reviewer evidence.

V3 focuses on commercial readiness, import planning, onboarding/setup workflow, beta-readiness documentation, deployment-readiness review, and commercial packaging strategy.

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

The platform is intentionally scoped as a trusted analytics foundation moving into V3 commercial readiness, not a fake fully launched commercial SaaS product.
